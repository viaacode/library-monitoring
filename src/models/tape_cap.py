from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils

@dataclass
@dataclass_json
class TapeCap:
    """Class for keeping track of an item in inventory."""
    main_partition_remaining_capacity_in_MiB: int = 0
    alternate_partition_remaining_capacity_in_MiB: int = 0
    main_partition_maximum_capacity_in_MiB: int = 0
    alternate_partition_maximum_capacity_in_MiB: int = 0

def from_arr(textarr):
    re = TapeCap()
    re.main_partition_remaining_capacity_in_MiB = utils.extract_int(textarr[0], sep=':')
    re.alternate_partition_remaining_capacity_in_MiB = utils.extract_int(textarr[1], sep=':')
    re.main_partition_maximum_capacity_in_MiB = utils.extract_int(textarr[2], sep=':')
    re.alternate_partition_maximum_capacity_in_MiB = utils.extract_int(textarr[3], sep=':')
    return re
