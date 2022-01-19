import argparse
import logging
from datetime import datetime
import sglogs_splitter
from example_text import text
import threading, time
from log_getter import LogGetter
#import postgrsql
import psycopg2

def process(interval, devices, username, password, fresh=False, static=False):
    try:
        logging.info(f"Starting Meemoo monitoring with {interval} second interval, with devices: {devices}. Using fake data: {static}")
        logpages_getter = LogGetter(fake=static)
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
    cur.execute("CREATE TABLE drive (id serial PRIMARY KEY, data text, number numeric)")
    cur.execute("CREATE TABLE tape (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, volstats JSON, tapealert JSON, tapeusage JSON, tapecap JSON, sequentialaccess JSON)")
    cur.close()
    conn.commit()

l
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
        # for key in logs_per_device_dict[device]:
        #     print("key:", key, logs_per_device_dict[device][key], '\n\n')

def write_to_tape_db(logs, conn):
    cur = conn.cursor()
    print(logs['vol_stats'].to_json())
    cur.execute(f"INSERT INTO tape (volstats, tapealert, tapeusage, tapecap, sequentialaccess) VALUES (%s, %s, %s, %s, %s)",
                (logs['vol_stats'].to_json(), logs['tape_alert'].to_json(),logs['tape_usage'].to_json(),logs['tape_cap'].to_json(), logs['seq_access'].to_json()))
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
