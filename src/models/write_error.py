from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass
@dataclass_json
class WriteError:
    """Class for keeping track of an item in inventory."""
    errors_corrected_without_substantial_delay: int = 0
    errors_corrected_with_possible_delays: int = 0
    total_rewrites_or_rereads: int = 0
    total_errors_corrected: int = 0
    total_times_correction_algorithm_processed: int = 0
    total_bytes_processed: int = 0
    total_uncorrected_errors: int = 0
    reserved_or_vendor_specific_0x8000: int = 0
    reserved_or_vendor_specific_0x8001: int = 0

    # def total_cost(self) -> float:
    #     return self.unit_price * self.quantity_on_hand

def extract_int(thetext):
    return int(thetext.split('=')[1].strip())

def from_arr(textarr):
    we = WriteError()
    we.errors_corrected_without_substantial_delay = extract_int(textarr[0])
    we.errors_corrected_with_possible_delays = extract_int(textarr[1])
    we.total_rewrites_or_rereads = extract_int(textarr[2])
    we.total_errors_corrected = extract_int(textarr[3])
    we.total_times_correction_algorithm_processed = extract_int(textarr[4])
    we.total_bytes_processed = extract_int(textarr[5])
    we.total_uncorrected_errors = extract_int(textarr[6])
    we.reserved_or_vendor_specific_0x8000 = extract_int(textarr[7])
    we.reserved_or_vendor_specific_0x8001 = extract_int(textarr[8])
    return we
