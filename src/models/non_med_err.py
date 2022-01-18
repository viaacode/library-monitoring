from dataclasses import dataclass
from dataclasses_json import dataclass_json

# Non-medium error count = 0

@dataclass
@dataclass_json
class NonMedErrorCount:
    """Class for keeping track of an item in inventory."""
    non_medium_error_count: int = 0

def extract_int(thetext):
    return int(thetext.split('=')[1].strip())

def text_to_non_med_error_count(text):
    re = NonMedErrorCount()
    textarr = text.split('\n')
    re.non_medium_error_count = extract_int(textarr[0])
    return re