from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils
# Non-medium error count = 0

@dataclass
@dataclass_json
class SequentialAccess:
    """Class for keeping track of an item in inventory."""
    data_bytes_received_with_WRITE_commands: int = 0
    data_bytes_written_to_media_by_WRITE_commands: int = 0
    data_bytes_read_from_media_by_READ_commands: int = 0
    data_bytes_transferred_by_READ_commands: int = 0
    native_capacity_from_BOP_to_EOD: int = 0
    native_capacity_from_BOP_to_EW_of_current_partition: int = 0
    minimum_native_capacity_from_EW_to_EOP_of_current_partition: int = 0
    native_capacity_from_BOP_to_current_position: int = 0
    maximum_native_capacity_in_device_object_buffer: int = 0
    vendor_specific_parameter_0x8000_value: int = 0
    vendor_specific_parameter_0x8001_value: int = 0
    vendor_specific_parameter_0x8002_value: int = 0
    vendor_specific_parameter_0x8003_value: int = 0

def text_to_seq_access(text):
    re = SequentialAccess()
    textarr = text.split('\n')
    re.non_medium_error_count = utils.extract_size(textarr[0])
    re.data_bytes_received_with_WRITE_commands = utils.extract_size(textarr[0])
    re.data_bytes_written_to_media_by_WRITE_commands = utils.extract_size(textarr[1])
    re.data_bytes_read_from_media_by_READ_commands = utils.extract_size(textarr[2])
    re.data_bytes_transferred_by_READ_commands = utils.extract_size(textarr[3])
    re.native_capacity_from_BOP_to_EOD = utils.extract_size(textarr[4])
    re.native_capacity_from_BOP_to_EW_of_current_partition = utils.extract_size(textarr[5])
    re.minimum_native_capacity_from_EW_to_EOP_of_current_partition = utils.extract_size(textarr[6])
    re.native_capacity_from_BOP_to_current_position = utils.extract_size(textarr[7])
    re.maximum_native_capacity_in_device_object_buffer = utils.extract_size(textarr[8])
    re.vendor_specific_parameter_0x8000_value = utils.extract_int(textarr[10], sep=':')
    re.vendor_specific_parameter_0x8001_value = utils.extract_int(textarr[11], sep=':')
    re.vendor_specific_parameter_0x8002_value = utils.extract_int(textarr[12], sep=':')
    re.vendor_specific_parameter_0x8003_value = utils.extract_int(textarr[13], sep=':')
    return re
