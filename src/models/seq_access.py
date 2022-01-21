from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils
# Non-medium error count = 0

@dataclass
@dataclass_json
class SequentialAccess:
    data_bytes_received_with_write_commands: int = 0
    data_bytes_written_to_media_by_write_commands: int = 0
    data_bytes_read_from_media_by_read_commands: int = 0
    data_bytes_transferred_by_read_commands: int = 0
    native_capacity_from_bop_to_eod: int = 0
    native_capacity_from_bop_to_ew_of_current_partition: int = 0
    minimum_native_capacity_from_ew_to_eop_of_current_partition: int = 0
    native_capacity_from_bop_to_current_position: int = 0
    maximum_native_capacity_in_device_object_buffer: int = 0
    maximum_native_capacity_in_device_object_buffer: int = 0
    vendor_specific_parameter_0x8000_value: int = 0
    vendor_specific_parameter_0x8001_value: int = 0
    vendor_specific_parameter_0x8002_value: int = 0
    vendor_specific_parameter_0x8003_value: int = 0
    vendor_specific_parameter_0x8003_value: int = 0

def from_arr(textarr):
    re = SequentialAccess()
    re.data_bytes_received_with_write_commands = utils.get_sglogs_value_of(textarr, "Data bytes received with WRITE commands")
    re.data_bytes_written_to_media_by_write_commands = utils.get_sglogs_value_of(textarr, "Data bytes written to media by WRITE commands")
    re.data_bytes_read_from_media_by_read_commands = utils.get_sglogs_value_of(textarr, "Data bytes read from media by READ commands")
    re.data_bytes_transferred_by_read_commands = utils.get_sglogs_value_of(textarr, "Data bytes transferred by READ commands")
    re.native_capacity_from_bop_to_eod = utils.get_sglogs_value_of(textarr, "Native capacity from BOP to EOD")
    re.native_capacity_from_bop_to_ew_of_current_partition = utils.get_sglogs_value_of(textarr, "Native capacity from BOP to EW of current partition")
    re.minimum_native_capacity_from_ew_to_eop_of_current_partition = utils.get_sglogs_value_of(textarr, "Minimum native capacity from EW to EOP of current partition")
    re.native_capacity_from_bop_to_current_position = utils.get_sglogs_value_of(textarr, "Native capacity from BOP to current position")
    re.maximum_native_capacity_in_device_object_buffer = utils.get_sglogs_value_of(textarr, "Maximum native capacity in device object buffer")
    re.maximum_native_capacity_in_device_object_buffer = utils.get_sglogs_value_of(textarr, "Maximum native capacity in device object buffer")
    re.vendor_specific_parameter_0x8000_value = utils.get_sglogs_value_of(textarr, "Vendor specific parameter [0x8000] value")
    re.vendor_specific_parameter_0x8001_value = utils.get_sglogs_value_of(textarr, "Vendor specific parameter [0x8001] value")
    re.vendor_specific_parameter_0x8002_value = utils.get_sglogs_value_of(textarr, "Vendor specific parameter [0x8002] value")
    re.vendor_specific_parameter_0x8003_value = utils.get_sglogs_value_of(textarr, "Vendor specific parameter [0x8003] value")
    re.vendor_specific_parameter_0x8003_value = utils.get_sglogs_value_of(textarr, "Vendor specific parameter [0x8003] value")
    return re
