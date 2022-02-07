import argparse
import logging
from datetime import datetime
from example_text import text
import threading, time
from log_getter import LogGetter
#import postgrsql

from state import State
import utils
import database


state = State()

def process(interval, raw_devices, host, username, password, kill=False, fake_logs=False):
    conn = None
    try:
        addendum = "\nUsing fake data!" if fake_logs else "\n"
        addendum = addendum + " Due to the --kill flag, the DB will be destroyed !!!!" if kill else ""
        outputtext = f'Starting Meemoo monitoring with {interval} second interval, with devices: {raw_devices}. {addendum}'
        logging.info(outputtext)
        logpages_getter = LogGetter(fake=fake_logs)
        port = 5432
        database_name = "tapemonitor"
        conn = database.connect(database_name, username, password, host)
        if kill:
            database.recreate_tables(conn)

        ticker = threading.Event()
        # convert raw device names (e.g. /dev/sg7) to their unique identifier
        devices = list(map(utils.get_drive_id, raw_devices))
        logging.info(f"Converted {raw_devices} to {devices}")
        # set the current session id to the highest available number (or 0)
        state.session_dict = get_session_dict(conn, devices)
        logging.info(f"Setting session id to: {state.session_dict}")
        periodicTask(devices, logpages_getter, conn)
        while not ticker.wait(interval):
            periodicTask(devices, logpages_getter, conn)
    finally:
        if(conn):
            conn.close()


def periodicTask(devices, logpages_getter, conn):
    logging.debug("Periodic task...")
    logs_per_device_dict = {}
    for device in devices:
        logs_per_device_dict[device] = logpages_getter.get_logpages(device)
    write_to_db(logs_per_device_dict, conn)


def write_to_db(logs_per_device_dict, conn):
    logging.debug("writing to db ...")
    for device in logs_per_device_dict:
        device_logs = logs_per_device_dict[device]
        session_id = state.get_session_id(device, device_logs['vol_stats'].volume_serial_number)
        database.write_to_drive_db(device_logs, state, device, session_id, conn)
        database.write_to_tape_db(device_logs, state, device, session_id, conn)


def get_session_dict(conn, devices):
    cur = conn.cursor()
    result = {}
    for drive in devices:
        cur.execute(f"select max(session_id) from drive where drive_id = %s", (drive,))
        output = cur.fetchone()[0]
        if output:
            result[drive] = int(output)
        else:
            result[drive] = 0
    return result


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(format="%(asctime)s %(name)s: %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Meemoo tape monitoring tool")
    parser.add_argument(
        "-i",
        "--interval",
        help="The polling interval used to gather scsi drive/tape information.",
        nargs="?",
        default=1,
    )
    parser.add_argument(
        "-o",
        "--host",
        help="Postgres server name",
        required=True,
    )

    parser.add_argument(
        "-u",
        "--username",
        help="Postgres username",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Postgres password",
        required=True,
    )
    parser.add_argument(
        "-k",
        "--kill",
        help="Recreate DB Table (Warning: all data will be lost!!!)",
	default=False,
	action="store_true"
    )
    parser.add_argument(
        "-f",
        "--fake",
        help="Use fake static data instead of real SCSI results",
	default=False,
	action="store_true"
    )

    parser.add_argument(
        "-x", "--verbose", help="Set logging to debug mode", action="store_true"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-d",
        "--devices",
        help="List of devices to monitor",
        nargs="+",
    )
    group.add_argument(
        "--devicefile",
        help="A txt file with each line having one device to monitor from /dev/tape/by-id/*",
        nargs="1",
    )


    args = parser.parse_args()
    # datadir = utils.add_trailing_slash(args.datadir)
    datenow = datetime.now()
    filehandler = f"meemooscsi-{datenow:%Y%M%d-%H_%M_%S}.log"
    fh = logging.FileHandler(filehandler)
    fh.setLevel(logging.INFO)
    # add the handlers to the logger
    logger.addHandler(fh)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)

    if args.devicefile:
        with open(args.devicefile, "r") as f: devices = list(map(str.strip, f.read().splitlines()))
    else:
        devices = args.devices
    logging.debug(f"Read the device list as being: {devices}")
    # assert os.path.exists(args.datadir), "datadir does not exist"
    # assert os.path.exists(args.resultdir), "resultdir does not exist"
    # assert os.path.exists(args.fitsdir), "fitsdir does not exist"
    process(int(args.interval), devices, args.host, args.username, args.password, args.kill, args.fake)
