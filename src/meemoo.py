import argparse
import logging
import os
from datetime import datetime
import sglogs_splitter
from example_text import text
import write_error
import read_error
import non_med_err
import seq_access
import dev_stats
import vol_stats
import tape_alert
import tape_usage
import tape_cap

def process(interval, devices):
    print("bla", interval, devices)
    write_err, read_err, non_med_err_str, seq_access_str, dev_stats_str, vol_stats_str, tape_alert_str, tape_usage_str, tape_cap_str = sglogs_splitter.split_sg_output(text)
    print(write_error.text_to_write_error(write_err))
    print(read_error.text_to_read_error(read_err))
    print(non_med_err.text_to_non_med_error_count(non_med_err_str))
    print(seq_access.text_to_seq_access(seq_access_str))
    print(dev_stats.text_to_dev_stats(dev_stats_str))
    print(vol_stats.from_text(vol_stats_str))
    print(tape_alert.from_text(tape_alert_str))
    print(tape_usage.from_text(tape_usage_str))
    print(tape_cap.from_text(tape_cap_str))




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
    process(args.interval, args.devices)
