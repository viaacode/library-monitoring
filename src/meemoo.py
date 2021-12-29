import argparse
import logging
import os
from datetime import datetime
import sglogs_splitter
from example_text import text
import write_error


def process(interval, devices):
    print("bla", interval, devices)
    write_err, *rest = sglogs_splitter.split_sg_output(text)
    print(write_error.text_to_write_error(write_err))



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
