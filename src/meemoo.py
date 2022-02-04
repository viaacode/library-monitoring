import argparse
import logging
from datetime import datetime
from example_text import text
import threading, time
from log_getter import LogGetter
#import postgrsql
import psycopg2
from state import State
import utils

from models.dev_stats import DevStats
from models.power_conditions import PowerConditions
from models.non_med_err import NonMedErrorCount
from models.write_error import WriteError
from models.read_error import ReadError

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
        database = "tapemonitor"
        conn = psycopg2.connect(f'dbname={database} user={username} password={password} host={host}')
        if kill:
            recreate_tables(conn)

        ticker = threading.Event()
        # convert raw device names (e.g. /dev/sg7) to their unique identifier
        devices = list(map(utils.get_drive_id, raw_devices))
        logging.debug(f"Converted {raw_devices} to {devices}")
        # set the current session id to the highest available number (or 0)
        state.session_dict = get_session_dict(conn, devices)
        logging.debug(f"Setting session id to: {state.session_dict}")
        periodicTask(devices, logpages_getter, conn)
        while not ticker.wait(interval):
            periodicTask(devices, logpages_getter, conn)
    finally:
        if(conn):
            conn.close()

def recreate_tables(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS drive")
    cur.execute("DROP TABLE IF EXISTS tape")
    cur.execute("CREATE TABLE drive (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,   \
            drive_id VARCHAR, session_id VARCHAR, non_medium_error_count INTEGER, total_errors_corrected_read INTEGER, total_bytes_processed_read INTEGER, total_uncorrected_errors_read INTEGER, total_errors_corrected_write INTEGER, total_bytes_processed_write INTEGER, total_uncorrected_errors_write INTEGER, dev_stats JSONB, read_error JSONB, write_error JSONB)")
    cur.execute("CREATE TABLE tape (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, drive_id VARCHAR, session_id INTEGER, \
                volume_serial_number TEXT, volume_barcode TEXT, volume_personality TEXT, page_valid INTEGER, thread_count INTEGER, \
                total_read_retries INTEGER, total_write_retries INTEGER, lifetime_megabytes_read INTEGER, last_mount_megabytes_read INTEGER, lifetime_megabytes_written INTEGER, last_mount_megabytes_written  INTEGER, \
                total_unrecovered_read_errors INTEGER, total_unrecovered_write_errors INTEGER, \
                volstats JSONB, tapealert JSONB, tapeusage JSONB, tapecap JSONB, sequentialaccess JSONB)")
    cur.close()
    conn.commit()

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
        write_to_drive_db(device_logs, device, session_id, conn)
        write_to_tape_db(device_logs, device, session_id, conn)

        # for key in logs_per_device_dict[device]:
        #     print("key:", key, logs_per_device_dict[device][key], '\n\n')

def write_to_tape_db(logs, drive_id, session_id, conn):
    volStats = logs['vol_stats']
    volStats_json = logs['vol_stats'].to_json()
    tape_alert_json = logs['tape_alert'].to_json()
    tape_usage_json = logs['tape_usage'].to_json()
    tape_cap_json = logs['tape_cap'].to_json()
    seq_access_json = logs['seq_access'].to_json()
    prev_hash, curr_hash, hash_updated = state.update_tape_hash(drive_id, utils.hash_strings(volStats_json, tape_alert_json, tape_usage_json, tape_cap_json, seq_access_json))
    if hash_updated:
        logging.debug(f"TAPE Row written: {prev_hash} != {curr_hash}")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO tape (drive_id, session_id, volume_serial_number, volume_barcode, volume_personality, page_valid, thread_count, \
                    total_read_retries, total_write_retries, lifetime_megabytes_read, last_mount_megabytes_read, lifetime_megabytes_written, last_mount_megabytes_written, \
                    total_unrecovered_read_errors, total_unrecovered_write_errors, \
                    volstats, tapealert, tapeusage, tapecap, sequentialaccess) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (drive_id, session_id, volStats.volume_serial_number, volStats.volume_barcode, volStats.volume_personality, volStats.page_valid, volStats.thread_count,
                    volStats.total_read_retries, volStats.total_write_retries, volStats.lifetime_megabytes_read, volStats.last_mount_megabytes_read,
                    volStats.lifetime_megabytes_written, volStats.last_mount_megabytes_written, volStats.total_unrecovered_read_errors, volStats.total_unrecovered_write_errors,
                    volStats_json, tape_alert_json,tape_usage_json, tape_cap_json, seq_access_json))
        cur.close()
        conn.commit()
    else:
        logging.debug(f"TAPE Row not written due to {prev_hash} equal to {curr_hash}")

def write_to_drive_db(logs, drive_id, session_id, conn):
    devStats: DevStats = logs['dev_stats']
    writeError: WriteError = logs['write_err']
    readError: ReadError = logs['read_err']
    powerConditions: PowerConditions = logs['power_conditions']
    nonMedErrorCount: NonMedErrorCount = logs['non_med_err']
    prev_hash, curr_hash, hash_updated = state.update_tape_hash(drive_id, utils.hash_strings(devStats.to_json(), writeError.to_json(), readError.to_json()))
    if hash_updated:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO drive (drive_id, session_id, non_medium_error_count, total_errors_corrected_read, total_bytes_processed_read,\
                    total_uncorrected_errors_read, total_errors_corrected_write, total_bytes_processed_write, total_uncorrected_errors_write, \
                    dev_stats, read_error, write_error) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (drive_id, session_id, nonMedErrorCount.non_medium_error_count, readError.total_errors_corrected, readError.total_bytes_processed,
                readError.total_uncorrected_errors, writeError.total_errors_corrected, writeError.total_bytes_processed, writeError.total_uncorrected_errors
                ,devStats.to_json(), readError.to_json(), writeError.to_json()))
        cur.close()
        conn.commit()
    else:
        logging.debug(f"DRIVE Row not written due to {prev_hash} equal to {curr_hash}")

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
        "-d",
        "--devices",
        help="List of devices to monitor",
        nargs="+",
        required=True,
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

    # assert os.path.exists(args.datadir), "datadir does not exist"
    # assert os.path.exists(args.resultdir), "resultdir does not exist"
    # assert os.path.exists(args.fitsdir), "fitsdir does not exist"
    process(int(args.interval), args.devices, args.host, args.username, args.password, args.kill, args.fake)
