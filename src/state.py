from collections import defaultdict
from typing import Dict


class State:
    def __init__(self):
        # HASH dicts
        self.drive_hash_dict: Dict[str, str] = defaultdict(None)
        self.tape_hash_dict: Dict[str, str] = defaultdict(None)

        # Device id dicts

        # Device.id -> session_id
        self.session_dict: Dict[str, int] = defaultdict(None)
        # Device.id -> volume_id
        self.session_serial_dict: Dict[str, str] = defaultdict(None)

    # returns (prev_hash, current_hash, changed?)
    def update_drive_hash(self, drive, hash):
        return self._update_hash(self.drive_hash_dict, drive, hash)

    # returns (prev_hash, current_hash, changed?)
    def update_tape_hash(self, drive, hash):
        return self._update_hash(self.tape_hash_dict, drive, hash)

    def _update_hash(self, adict, drive, hash):
        if drive in adict and adict[drive] == hash:
            return adict[drive], hash, False
        adict[drive] = hash
        return "empty", hash, True

    # returns the session id for current drive
    def get_session_id(self, device_id, volume_serial_number):
        # if we don't have a serial number for this device, assign it this one - we might miss tape changes when the monitoring is not running (TODO)
        if self.session_serial_dict.get(device_id) is None:
            self.session_serial_dict[device_id] = volume_serial_number
        if volume_serial_number != self.session_serial_dict[device_id]:
            self.session_dict[device_id] = self.session_dict[device_id] + 1
            self.session_serial_dict[device_id] = volume_serial_number
        return self.session_dict[device_id]

