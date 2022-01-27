import logging
import re

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
