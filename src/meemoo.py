import argparse
import logging
from datetime import datetime
import sglogs_splitter
from example_text import text
import threading, time
from log_getter import LogGetter
#import postgrsql
import psycopg2

def process(interval, devices, username, password, fresh=False):
    try:
	    logging.info(f"Starting Meemoo monitoring with {interval} second interval, with devices: {devices}")
	    logpages_getter = LogGetter(fake=True)
	    host = "do-qas-dbs-md.do.viaa.be"
	    port = 5432
	    database = "tapemonitor"
	    print(f'pq://{username}:{password}@{host}:{port}/{database}')
	    #db = postgresql.open(f'pq://{username}:{password}@{host}:{port}/{database}')
	    conn = psycopg2.connect(f'dbname={database} user={username} password={password} host={host}')
	    #db.execute("CREATE TABLE test (emp_first_name text, emp_last_name text, emp_salary numeric)")
	    cur = conn.cursor()
	    if fresh:
		cur.execute("DROP TABLE IF EXISTS test")
		cur.execute("CREATE TABLE test (id serial PRIMARY KEY, data text, number numeric)")
	    cur.execute(f"INSERT INTO test (data, number) VALUES (%s, %s)", ("abc'def", 100))
	    conn.commit()

	    ticker = threading.Event()
	    while not ticker.wait(interval):
		periodicTask(devices, logpages_getter, db)
    finally:
    	print("finally")


def periodicTask(devices, logpages_getter, db):
    logging.info("Periodic task...")
    logs_per_device_dict = {}
    for device in devices:
        logs_per_device_dict[device] = logpages_getter.get_logpages()
    write_to_db(logs_per_device_dict, db)

def write_to_db(logs_per_device_dict, db):
    print("writing to db ...", logs_per_device_dict)
        

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
    process(int(args.interval), args.devices, args.username, args.password, args.fresh)
