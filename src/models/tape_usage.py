from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils

@dataclass
@dataclass_json
class TapeUsage:
    """Class for keeping track of an item in inventory."""
    thread_count: int = 0
    total_data_sets_written: int = 0
    total_write_retries: int = 0
    total_unrecovered_write_errors: int = 0
    total_suspended_writes: int = 0
    total_fatal_suspended_writes: int = 0
    total_data_sets_read: int = 0
    total_read_retries: int = 0
    total_unrecovered_read_errors: int = 0
    total_suspended_reads: int = 0
    total_fatal_suspended_reads: int = 0

def from_arr(textarr):
    re = TapeUsage()
    # re.read_warning = utils.extract_int(textarr[0], sep=':')
    re.thread_count = utils.extract_int(textarr[0], sep=':')
    re.total_data_sets_written = utils.extract_int(textarr[1], sep=':')
    re.total_write_retries = utils.extract_int(textarr[2], sep=':')
    re.total_unrecovered_write_errors = utils.extract_int(textarr[3], sep=':')
    re.total_suspended_writes = utils.extract_int(textarr[4], sep=':')
    re.total_fatal_suspended_writes = utils.extract_int(textarr[5], sep=':')
    re.total_data_sets_read = utils.extract_int(textarr[6], sep=':')
    re.total_read_retries = utils.extract_int(textarr[7], sep=':')
    re.total_unrecovered_read_errors = utils.extract_int(textarr[8], sep=':')
    re.total_suspended_reads = utils.extract_int(textarr[9], sep=':')
    re.total_fatal_suspended_reads = utils.extract_int(textarr[10], sep=':')
    return re
