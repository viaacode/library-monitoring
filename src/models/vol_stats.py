from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils

@dataclass
@dataclass_json
class VolStats:
    """Class for keeping track of an item in inventory."""
    page_valid: int = 0
    thread_count: int = 0
    total_data_sets_written: int = 0
    total_write_retries: int = 0
    total_unrecovered_write_errors: int = 0
    total_suspended_writes: int = 0
    total_fatal_suspended_writes: int = 0
    total_data_sets_read: int = 0
    total_read_retries: int = 0
    total_unrecovered_read_errors: int = 0
    last_mount_unrecovered_write_errors: int = 0
    last_mount_unrecovered_read_errors: int = 0
    last_mount_megabytes_written: int = 0
    last_mount_megabytes_read: int = 0
    lifetime_megabytes_written: int = 0
    lifetime_megabytes_read: int = 0
    last_load_write_compression_ratio: int = 0
    last_load_read_compression_ratio: int = 0
    medium_mount_time: int = 0
    medium_ready_time: int = 0
    total_native_capacity: int = 0
    total_used_native_capacity: int = 0
    volume_serial_number: str = ""
    tape_lot_identifier: str = ""
    volume_barcode: str = ""
    volume_manufacturer: str = ""
    volume_license_code: str = ""
    volume_personality: str = ""
    write_protect: int = 0
    worm: int = 0
    maximum_recommended_tape_path_temperature_exceeded: int = 0
    beginning_of_medium_passes: int = 0
    middle_of_medium_passes: int = 0

def from_arr(textarr):
    re = VolStats()
    re.page_valid = utils.extract_int(textarr[0], sep=':')
    re.thread_count = utils.extract_int(textarr[1], sep=':')
    re.total_data_sets_written = utils.extract_int(textarr[2], sep=':')
    re.total_write_retries = utils.extract_int(textarr[3], sep=':')
    re.total_unrecovered_write_errors = utils.extract_int(textarr[4], sep=':')
    re.total_suspended_writes = utils.extract_int(textarr[5], sep=':')
    re.total_fatal_suspended_writes = utils.extract_int(textarr[6], sep=':')
    re.total_data_sets_read = utils.extract_int(textarr[7], sep=':')
    re.total_read_retries = utils.extract_int(textarr[8], sep=':')
    re.total_unrecovered_read_errors = utils.extract_int(textarr[9], sep=':')
    re.last_mount_unrecovered_write_errors = utils.extract_int(textarr[10], sep=':')
    re.last_mount_unrecovered_read_errors = utils.extract_int(textarr[11], sep=':')
    re.last_mount_megabytes_written = utils.extract_int(textarr[12], sep=':')
    re.last_mount_megabytes_read = utils.extract_int(textarr[13], sep=':')
    re.lifetime_megabytes_written = utils.extract_int(textarr[14], sep=':')
    re.lifetime_megabytes_read = utils.extract_int(textarr[15], sep=':')
    re.last_load_write_compression_ratio = utils.extract_int(textarr[16], sep=':')
    re.last_load_read_compression_ratio = utils.extract_int(textarr[17], sep=':')
    re.medium_mount_time = utils.extract_int(textarr[18], sep=':')
    re.medium_ready_time = utils.extract_int(textarr[19], sep=':')
    re.total_native_capacity = utils.extract_int(textarr[20], sep=':')
    re.total_used_native_capacity = utils.extract_int(textarr[21], sep=':')
    re.volume_serial_number = utils.extract_str(textarr[22])
    re.tape_lot_identifier = utils.extract_str(textarr[23])
    re.volume_barcode = utils.extract_str(textarr[24])
    re.volume_manufacturer = utils.extract_str(textarr[25])
    re.volume_license_code = utils.extract_str(textarr[26])
    re.volume_personality = utils.extract_str(textarr[27])
    re.write_protect = utils.extract_int(textarr[28], sep=':')
    re.worm = utils.extract_int(textarr[29], sep=':')
    re.maximum_recommended_tape_path_temperature_exceeded = utils.extract_int(textarr[30], sep=':')
    re.beginning_of_medium_passes = utils.extract_int(textarr[31], sep=':')
    re.middle_of_medium_passes = utils.extract_int(textarr[32], sep=':')
    return re
