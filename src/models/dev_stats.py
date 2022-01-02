from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils

@dataclass
@dataclass_json
class DevStats:
    """Class for keeping track of an item in inventory."""
    lifetime_media_loads: int = 0
    lifetime_cleaning_operations: int = 0
    lifetime_power_on_hours: int = 0
    lifetime_media_motion_head_hours: int = 0
    lifetime_metres_of_tape_processed: int = 0
    lifetime_media_motion_head_hours_when_incompatible_media_last_loaded: int = 0
    lifetime_power_on_hours_when_last_temperature_condition_occurred: int = 0
    lifetime_power_on_hours_when_last_power_consumption_condition_occurred: int = 0
    media_motion_head_hours_since_last_successful_cleaning_operation: int = 0
    media_motion_head_hours_since_2nd_to_last_successful_cleaning: int = 0
    media_motion_head_hours_since_3rd_to_last_successful_cleaning: int = 0
    lifetime_power_on_hours_when_last_operator_initiated_forced_reset_and_or_emergency_eject_occurred: int = 0
    reserved_parameter_0xc_value: int = 0
    reserved_parameter_0xd_value: int = 0
    reserved_parameter_0xe_value: int = 0
    reserved_parameter_0xf_value: int = 0
    reserved_parameter_0x10_value: int = 0
    reserved_parameter_0x11_value: int = 0
    reserved_parameter_0x12_value: int = 0
    reserved_parameter_0x13_value: int = 0
    reserved_parameter_0x14_value: int = 0
    reserved_parameter_0x15_value: int = 0
    reserved_parameter_0x40_value: int = 0
    reserved_parameter_0x41_value: int = 0
    reserved_parameter_0x80_value: int = 0
    reserved_parameter_0x81_value: int = 0


def text_to_dev_stats(text):
    re = DevStats()
    textarr = text.split('\n')
    re.lifetime_media_loads = utils.extract_int(textarr[0], sep=':')
    re.lifetime_cleaning_operations = utils.extract_int(textarr[1], sep=':')
    re.lifetime_power_on_hours = utils.extract_int(textarr[2], sep=':')
    re.lifetime_media_motion_head_hours = utils.extract_int(textarr[3], sep=':')
    re.lifetime_metres_of_tape_processed = utils.extract_int(textarr[4], sep=':')
    re.lifetime_media_motion_head_hours_when_incompatible_media_last_loaded = utils.extract_int(textarr[5], sep=':')
    re.lifetime_power_on_hours_when_last_temperature_condition_occurred = utils.extract_int(textarr[6], sep=':')
    re.lifetime_power_on_hours_when_last_power_consumption_condition_occurred = utils.extract_int(textarr[7], sep=':')
    re.media_motion_head_hours_since_last_successful_cleaning_operation = utils.extract_int(textarr[8], sep=':')
    re.media_motion_head_hours_since_2nd_to_last_successful_cleaning = utils.extract_int(textarr[9], sep=':')
    re.media_motion_head_hours_since_3rd_to_last_successful_cleaning = utils.extract_int(textarr[10], sep=':')
    re.reserved_parameter_0xc_value = utils.extract_int(textarr[13], sep=':')
    re.reserved_parameter_0xd_value = utils.extract_int(textarr[14], sep=':')
    re.reserved_parameter_0xe_value = utils.extract_int(textarr[15], sep=':')
    re.reserved_parameter_0xf_value = utils.extract_int(textarr[16], sep=':')
    re.reserved_parameter_0x10_value = utils.extract_int(textarr[17], sep=':')
    re.reserved_parameter_0x11_value = utils.extract_int(textarr[18], sep=':')
    re.reserved_parameter_0x12_value = utils.extract_int(textarr[19], sep=':')
    re.reserved_parameter_0x13_value = utils.extract_int(textarr[20], sep=':')
    re.reserved_parameter_0x14_value = utils.extract_int(textarr[21], sep=':')
    re.reserved_parameter_0x15_value = utils.extract_int(textarr[22], sep=':')
    re.reserved_parameter_0x40_value = utils.extract_int(textarr[23], sep=':')
    re.reserved_parameter_0x41_value = utils.extract_int(textarr[24], sep=':')
    re.reserved_parameter_0x80_value = utils.extract_int(textarr[25], sep=':')
    re.reserved_parameter_0x81_value = utils.extract_int(textarr[26], sep=':')
    return re
