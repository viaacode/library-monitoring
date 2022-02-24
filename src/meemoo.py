import argparse
import logging
from datetime import datetime
from typing import List
from example_text import text
import threading, time
from log_getter import LogGetter
from pathlib import Path
from utils import Device




#import postgrsql

from state import State
import utils
import database


state = State()


def process(interval, raw_devices, host, database_name, username, password, erase_db=False, fake_logs=False):
    conn = None
    try:
        addendum = "\nUsing fake data!" if fake_logs else "\n"
        addendum = addendum + " Due to the --erasedb flag, the DB will be destroyed !!!!" if erase_db else ""
        outputtext = f'Starting Meemoo monitoring with {interval} second interval, with devices: {raw_devices}. {addendum}'
        logging.info(outputtext)
        logpages_getter = LogGetter(fake=fake_logs)
        conn = establish_connection(database_name, username, password, host, erase_db)

        ticker = threading.Event()
        # convert raw device names (e.g. /dev/sg7) to their unique identifier
        devices: List[Device] = list(map(utils.get_drive_id, raw_devices))
        logging.info(f"Converted {raw_devices} to {devices}")
        # set the current session id to the highest available number (or 0)
        state.session_dict = get_session_dict(conn, devices)
        logging.info(f"Setting session id to: {state.session_dict}")
        periodicTask(devices, logpages_getter, conn)
        while not ticker.wait(interval):
            periodicTask(devices, logpages_getter, conn)
    except Exception as e:
        logging.error(f"Encountered error in main process loop: {e}")
    finally:
        if(conn):
            conn.close()

def establish_connection(db_name, username, password, host, erase_db):
        conn = database.connect(db_name, username, password, host)
        if erase_db:
            database.recreate_tables(conn)
        return conn

def periodicTask(devices, logpages_getter, conn):
    logging.debug("Periodic task...")
    logs_per_device_dict = {}
    for original, resolved, id in devices:
        logs_per_device_dict[id] = logpages_getter.get_logpages(original)
    write_to_db(logs_per_device_dict, conn)


def write_to_db(logs_per_device_dict, conn):
    logging.debug("writing to db ...")
    for device in logs_per_device_dict:
        device_logs = logs_per_device_dict[device]
        if device_logs is not None:
            session_id = state.get_session_id(device, device_logs['vol_stats'].volume_serial_number)
            database.write_to_drive_db(device_logs, state, device, session_id, conn)
            database.write_to_tape_db(device_logs, state, device, session_id, conn)


def get_session_dict(conn, devices):
    cur = conn.cursor()
    result = {}
    for _, _, id in devices:
        cur.execute(f"select max(session_id) from drive where drive_id = %s", (id,))
        output = cur.fetchone()[0]
        if output:
            result[id] = int(output)
        else:
            result[id] = 0
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
        "-d",
        "--databasename",
        help="Postgres database name",
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
        "-f",
        "--fake",
        help="Use fake static data instead of real SCSI results",
	default=False,
	action="store_true"
    )

    parser.add_argument(
        "-x", "--verbose", help="Set logging to debug mode", action="store_true"
    )
    parser.add_argument(
        "--erasedb",
        help="Recreate DB Table (Warning: all data will be lost!!!)",
	default=False,
	action="store_true"
    )
    parser.add_argument(
        "--erasedbonly",
        help="Recreate DB Table (Warning: all data will be lost!!!) and exit",
	default=False,
	action="store_true"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--devices",
        help="List of devices to monitor",
        nargs="+",
    )
    group.add_argument(
        "--devicefile",
        help="A txt file with each line having one device to monitor from /dev/tape/by-id/*",
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
    # delete DB and exit
    if args.erasedbonly:
        establish_connection(args.databasename, args.username, args.password, args.host, True)
        logging.info(f"DB {args.databasename} was erased at {args.host}")
        exit()

    if args.devicefile:
        with open(args.devicefile, "r") as f: devices = list(map(str.strip, f.read().splitlines()))
    else:
        devices = args.devices
    logging.debug(f"Read the device list as being: {devices}")
    process(int(args.interval), devices, args.host, args.databasename, args.username, args.password, args.erasedb, args.fake)
