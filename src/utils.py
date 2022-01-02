import logging

def extract_int(thetext, sep='='):
    logging.debug("extract int"+ thetext)
    return int(thetext.split(sep)[1].strip())

def extract_str(thetext, sep=':'):
    logging.debug("extract str"+ thetext)
    return thetext.split(sep)[1].strip()


def extract_size(thetext):
    logging.debug("extract size"+ thetext)
    content = thetext.split(':')[1].strip()
    GB = content[-2:] == "GB"
    result = ""
    if GB:
        result = int(content[:-2]) * 1024
    else:
        result = int(content[:-2])
    return result
