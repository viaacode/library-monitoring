from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass
@dataclass_json
class ReadError:
    """Class for keeping track of an item in inventory."""
    errors_corrected_without_substantial_delay: int = 0
    errors_corrected_with_possible_delays: int = 0
    total_rewrites_or_rereads: int = 0
    total_errors_corrected: int = 0
    total_times_correction_algorithm_processed: int = 0
    total_bytes_processed: int = 0
    total_uncorrected_errors: int = 0
    reserved_or_vendor_specific_0x8000: int = 0

    # def total_cost(self) -> float:
    #     return self.unit_price * self.quantity_on_hand

def extract_int(thetext):
    return int(thetext.split('=')[1].strip())

def text_to_read_error(text):
    re = ReadError()
    textarr = text.split('\n')
    re.errors_corrected_without_substantial_delay = extract_int(textarr[0])
    re.errors_corrected_with_possible_delays = extract_int(textarr[1])
    re.total_rewrites_or_rereads = extract_int(textarr[2])
    re.total_errors_corrected = extract_int(textarr[3])
    re.total_times_correction_algorithm_processed = extract_int(textarr[4])
    re.total_bytes_processed = extract_int(textarr[5])
    re.total_uncorrected_errors = extract_int(textarr[6])
    re.reserved_or_vendor_specific_0x8000 = extract_int(textarr[7])
    return re
