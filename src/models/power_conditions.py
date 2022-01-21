from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass
@dataclass_json
class PowerConditions:
    accumulated_transitions_to_idle_a: int = 0
    reserved_0x4: int = 0

def extract_int(thetext):
    return int(thetext.split('=')[1].strip())

def from_arr(textarr):
    re = PowerConditions()
    re.accumulated_transations_to_idla_a = extract_int(textarr[0])
    re.reserved_0x4 = extract_int(textarr[1])
    return re
