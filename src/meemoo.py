import argparse
import logging
from datetime import datetime
from example_text import text
import threading, time
from log_getter import LogGetter
#import postgrsql
import psycopg2

from models.dev_stats import DevStats
from models.power_conditions import PowerConditions
from models.non_med_err import NonMedErrorCount
from models.write_error import WriteError
from models.read_error import ReadError

def process(interval, devices, host, username, password, kill=False, fake_logs=False):
    try:
        addendum = "\nUsing fake data!" if fake_logs else "\n"
        addendum = addendum + " Due to the --kill flag, the DB will be destroyed !!!!" if kill else ""
        outputtext = f'Starting Meemoo monitoring with {interval} second interval, with devices: {devices}. {addendum}'
        logging.info(outputtext)
        logpages_getter = LogGetter(fake=fake_logs)
        port = 5432
        database = "tapemonitor"
        conn = psycopg2.connect(f'dbname={database} user={username} password={password} host={host}')
        if kill:
            recreate_tables(conn)
        ticker = threading.Event()
        periodicTask(devices, logpages_getter, conn)
        while not ticker.wait(interval):
            periodicTask(devices, logpages_getter, conn)
    finally:
        conn.close()

def recreate_tables(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS drive")
    cur.execute("DROP TABLE IF EXISTS tape")
    cur.execute("CREATE TABLE drive (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,   \
            device VARCHAR, lifetime_media_loads INTEGER, lifetime_cleaning_operations INTEGER, lifetime_power_on_hours INTEGER, lifetime_media_motion_head_hours INTEGER, \
            lifetime_metres_of_tape_processed INTEGER, lifetime_media_motion_head_hours_when_incompatible_media_last_loaded INTEGER, \
            lifetime_power_on_hours_when_last_temperature_condition_occurred INTEGER, lifetime_power_on_hours_when_last_power_consumption_condition_occurred INTEGER, \
            media_motion_head_hours_since_last_successful_cleaning_operation INTEGER, media_motion_head_hours_since_2nd_to_last_successful_cleaning INTEGER, \
            media_motion_head_hours_since_3rd_to_last_successful_cleaning INTEGER, lifetime_power_on_hours_when_last_operator_initiated_forced_reset_and_or_emergency_eject_occurred INTEGER, \
            accumulated_transitions_to_idle_a INTEGER, non_medium_error_count INTEGER, dev_stats JSONB, read_error JSONB, write_error JSONB)")
    cur.execute("CREATE TABLE tape (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, drive_id INTEGER,  \
                volume_serial_number TEXT,  tape_lot_identifier TEXT, volume_barcode TEXT, volume_manufacturer TEXT, volume_license_code TEXT, volume_personality TEXT, page_valid INTEGER, thread_count INTEGER, \
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
        drive_id = write_to_drive_db(logs_per_device_dict[device], device, conn)
        write_to_tape_db(logs_per_device_dict[device], drive_id, conn)

        # for key in logs_per_device_dict[device]:
        #     print("key:", key, logs_per_device_dict[device][key], '\n\n')

def write_to_tape_db(logs, drive_id, conn):
    cur = conn.cursor()
    volStats = logs['vol_stats']
    logging.debug(f"Vol_stats: {logs['vol_stats'].to_json()}")
    cur.execute(f"INSERT INTO tape (drive_id, volume_serial_number, tape_lot_identifier, volume_barcode, volume_manufacturer, volume_license_code, \
                volume_personality, page_valid, thread_count, \
                total_read_retries, total_write_retries, lifetime_megabytes_read, last_mount_megabytes_read, lifetime_megabytes_written, last_mount_megabytes_written, \
                total_unrecovered_read_errors, total_unrecovered_write_errors, \
                volstats, tapealert, tapeusage, tapecap, sequentialaccess) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (drive_id, volStats.volume_serial_number, volStats.tape_lot_identifier, volStats.volume_barcode, volStats.volume_manufacturer,
                 volStats.volume_license_code, volStats.volume_personality, volStats.page_valid, volStats.thread_count,
                 volStats.total_read_retries, volStats.total_write_retries, volStats.lifetime_megabytes_read, volStats.last_mount_megabytes_read,
                 volStats.lifetime_megabytes_written, volStats.last_mount_megabytes_written, volStats.total_unrecovered_read_errors, volStats.total_unrecovered_write_errors,
                 logs['vol_stats'].to_json(), logs['tape_alert'].to_json(),logs['tape_usage'].to_json(),logs['tape_cap'].to_json(), logs['seq_access'].to_json()))
    cur.close()
    conn.commit()

def write_to_drive_db(logs, device, conn):
    cur = conn.cursor()
    devStats: DevStats = logs['dev_stats']
    writeError: WriteError = logs['write_err']
    readError: ReadError = logs['read_err']
    powerConditions: PowerConditions = logs['power_conditions']
    nonMedErrorCount: NonMedErrorCount = logs['non_med_err']
    logging.debug(f"Dev_stats: {devStats.to_json()}")
    cur.execute(f"INSERT INTO drive (device, lifetime_media_loads, lifetime_cleaning_operations, lifetime_power_on_hours, lifetime_media_motion_head_hours, \
            lifetime_metres_of_tape_processed, lifetime_media_motion_head_hours_when_incompatible_media_last_loaded, \
            lifetime_power_on_hours_when_last_temperature_condition_occurred, lifetime_power_on_hours_when_last_power_consumption_condition_occurred, \
            media_motion_head_hours_since_last_successful_cleaning_operation, media_motion_head_hours_since_2nd_to_last_successful_cleaning, \
            media_motion_head_hours_since_3rd_to_last_successful_cleaning, lifetime_power_on_hours_when_last_operator_initiated_forced_reset_and_or_emergency_eject_occurred, \
            accumulated_transitions_to_idle_a, non_medium_error_count, dev_stats, read_error, write_error) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING ID",
            (device, devStats.lifetime_media_loads, devStats.lifetime_cleaning_operations, devStats.lifetime_power_on_hours, devStats.lifetime_media_motion_head_hours,
             devStats.lifetime_metres_of_tape_processed, devStats.lifetime_media_motion_head_hours_when_incompatible_media_last_loaded,
             devStats.lifetime_power_on_hours_when_last_temperature_condition_occurred, devStats.lifetime_power_on_hours_when_last_power_consumption_condition_occurred,
             devStats.media_motion_head_hours_since_last_successful_cleaning_operation, devStats.media_motion_head_hours_since_2nd_to_last_successful_cleaning,
             devStats.media_motion_head_hours_since_3rd_to_last_successful_cleaning, devStats.lifetime_power_on_hours_when_last_operator_initiated_forced_reset_and_or_emergency_eject_occurred,
             powerConditions.accumulated_transitions_to_idle_a, nonMedErrorCount.non_medium_error_count, devStats.to_json(), readError.to_json(), writeError.to_json()))
    id_of_new_row = cur.fetchone()[0]
    cur.close()
    conn.commit()
    return id_of_new_row


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
