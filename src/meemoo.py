import argparse
import logging
from datetime import datetime
import sglogs_splitter
from example_text import text
import threading, time
from log_getter import LogGetter
#import postgrsql
import psycopg2

from models.dev_stats import DevStats
from models.power_conditions import PowerConditions

def process(interval, devices, username, password, fresh=False, static_logs=False):
    try:
        outputtext = f'Starting Meemoo monitoring with {interval} second interval, with devices: {devices}. Using fake data: {static_logs}'
        logging.debug(outputtext)
        logpages_getter = LogGetter(fake=static_logs)
        host = "do-qas-dbs-md.do.viaa.be"
        port = 5432
        database = "tapemonitor"
        conn = psycopg2.connect(f'dbname={database} user={username} password={password} host={host}')
        if fresh:
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
            lifetime_media_loads INTEGER, lifetime_cleaning_operations INTEGER, lifetime_power_on_hours INTEGER, lifetime_media_motion_head_hours INTEGER, \
            lifetime_metres_of_tape_processed INTEGER, lifetime_media_motion_head_hours_when_incompatible_media_last_loaded INTEGER, \
            lifetime_power_on_hours_when_last_temperature_condition_occurred INTEGER, lifetime_power_on_hours_when_last_power_consumption_condition_occurred INTEGER, \
            media_motion_head_hours_since_last_successful_cleaning_operation INTEGER, media_motion_head_hours_since_2nd_to_last_successful_cleaning INTEGER, \
            media_motion_head_hours_since_3rd_to_last_successful_cleaning INTEGER, lifetime_power_on_hours_when_last_operator_initiated_forced_reset_and_or_emergency_eject_occurred INTEGER, \
            accumulated_transitions_to_idle_a INTEGER, dev_stats JSON)")
    cur.execute("CREATE TABLE tape (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,   \
                volume_serial_number TEXT,  tape_lot_identifier TEXT, volume_barcode TEXT, volume_manufacturer TEXT, volume_license_code TEXT, volume_personality TEXT, page_valid INTEGER, thread_count INTEGER, \
                volstats JSON, tapealert JSON, tapeusage JSON, tapecap JSON, sequentialaccess JSON)")
    cur.close()
    conn.commit()

def periodicTask(devices, logpages_getter, conn):
    logging.info("Periodic task...")
    logs_per_device_dict = {}
    for device in devices:
        logs_per_device_dict[device] = logpages_getter.get_logpages(device)
    write_to_db(logs_per_device_dict, conn)

def write_to_db(logs_per_device_dict, conn):
    print("writing to db ...")
    for device in logs_per_device_dict:
        write_to_tape_db(logs_per_device_dict[device], conn)
        write_to_drive_db(logs_per_device_dict[device], conn)
        # for key in logs_per_device_dict[device]:
        #     print("key:", key, logs_per_device_dict[device][key], '\n\n')

def write_to_tape_db(logs, conn):
    cur = conn.cursor()
    volStats = logs['vol_stats']
    logging.debug(f"Vol_stats: {logs['vol_stats'].to_json()}")
    cur.execute(f"INSERT INTO tape (volume_serial_number, tape_lot_identifier, volume_barcode, volume_manufacturer, volume_license_code, \
                volume_personality, page_valid, thread_count, volstats, tapealert, \
                tapeusage, tapecap, sequentialaccess) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (volStats.volume_serial_number, volStats.tape_lot_identifier, volStats.volume_barcode, volStats.volume_manufacturer, volStats.volume_license_code, volStats.volume_personality, volStats.page_valid, volStats.thread_count, logs['vol_stats'].to_json(), logs['tape_alert'].to_json(),logs['tape_usage'].to_json(),logs['tape_cap'].to_json(), logs['seq_access'].to_json()))
    cur.close()
    conn.commit()

def write_to_drive_db(logs, conn):
    cur = conn.cursor()
    devStats: DevStats = logs['dev_stats']
    powerConditions: PowerConditions = logs['power_conditions']
    logging.debug(f"Dev_stats: {devStats.to_json()}")
    cur.execute(f"INSERT INTO drive (lifetime_media_loads, lifetime_cleaning_operations, lifetime_power_on_hours, lifetime_media_motion_head_hours, \
            lifetime_metres_of_tape_processed, lifetime_media_motion_head_hours_when_incompatible_media_last_loaded, \
            lifetime_power_on_hours_when_last_temperature_condition_occurred, lifetime_power_on_hours_when_last_power_consumption_condition_occurred, \
            media_motion_head_hours_since_last_successful_cleaning_operation, media_motion_head_hours_since_2nd_to_last_successful_cleaning, \
            media_motion_head_hours_since_3rd_to_last_successful_cleaning, lifetime_power_on_hours_when_last_operator_initiated_forced_reset_and_or_emergency_eject_occurred, \
            accumulated_transitions_to_idle_a, dev_stats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (devStats.lifetime_media_loads, devStats.lifetime_cleaning_operations, devStats.lifetime_power_on_hours, devStats.lifetime_media_motion_head_hours,
             devStats.lifetime_metres_of_tape_processed, devStats.lifetime_media_motion_head_hours_when_incompatible_media_last_loaded,
             devStats.lifetime_power_on_hours_when_last_temperature_condition_occurred, devStats.lifetime_power_on_hours_when_last_power_consumption_condition_occurred,
             devStats.media_motion_head_hours_since_last_successful_cleaning_operation, devStats.media_motion_head_hours_since_2nd_to_last_successful_cleaning,
             devStats.media_motion_head_hours_since_3rd_to_last_successful_cleaning, devStats.lifetime_power_on_hours_when_last_operator_initiated_forced_reset_and_or_emergency_eject_occurred,
             powerConditions.accumulated_transitions_to_idle_a, devStats.to_json()))
    cur.close()
    conn.commit()


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(format="%(asctime)s %(name)s: %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="munipack automation cli")
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
        "--fresh",
        help="Recreate DB Table (Warning: all data will be lost!!!)",
	default=False,
	action="store_true"
    )
    parser.add_argument(
        "-s",
        "--static",
        help="Use static data instead of real SCSI results",
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
    process(int(args.interval), args.devices, args.username, args.password, args.fresh, args.static)
