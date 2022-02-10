import logging
import re
from hashlib import sha256
import subprocess
from pathlib import Path

def extract_int(thetext, sep='='):
    logging.debug(f"extract int: {thetext}")
    return int(thetext.split(sep)[1].strip())

def extract_str(thetext, sep=':'):
    logging.debug(f"extract str: {thetext}")
    return thetext.split(sep)[1].strip()


def extract_size(thetext):
    logging.debug("extract size: {thetext}")
    content = thetext.split(':')[1].strip()
    GB = content[-2:] == "GB"
    result = ""
    if GB:
        result = int(content[:-2]) * 1024
    else:
        result = int(content[:-2])
    return result

def get_sglogs_value_of(lines, tosearch):
    p = re.compile(f'.*{tosearch}.*')
    for idx, line in enumerate(lines):
        match = p.match(line)
        if match:
            logging.debug(f"Match with {tosearch}: {match} at idx {idx}")
            return idx
    return None

# concat all arguments and return the sha256 hash
def hash_strings(*args):
    concats = "#".join(args)
    hash = sha256(concats.encode('utf-8')).hexdigest()
    return hash

# go from /dev/sg7 to "0440F9201"
# def get_drive_id(drive: str):
#     stem = Path(drive).stem.split('-')[1][-10:]  # go from /dev/tape/by-id/scsi-0004151515 to scsi-0004151515 to 0004151515
#     return stem


def get_drive_id(drive: str):
    output  = None
    dev = Path(drive).stem
    try:
            output = subprocess.run(['cat', f'/sys/class/scsi_tape/{dev}/device/wwid'], check=True, stdout=subprocess.PIPE, text=True).stdout
            output = output.split('.')[1]
    except subprocess.CalledProcessError as err:
            logging.error(f"An error occurred getting the id: {err}")
    return output



