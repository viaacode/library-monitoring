from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils

@dataclass
@dataclass_json
class TapeAlert:
    """Class for keeping track of an item in inventory."""
    read_warning: int = 0
    write_warning: int = 0
    hard_error: int = 0
    media: int = 0
    read_failure: int = 0
    write_failure: int = 0
    media_life: int = 0
    not_data_grade: int = 0
    write_protect: int = 0
    no_removal: int = 0
    cleaning_media: int = 0
    unsupported_format: int = 0
    recoverable_mechanical_cartridge_failure: int = 0
    unrecoverable_mechanical_cartridge_failure: int = 0
    memory_chip_in_cartridge_failure: int = 0
    forced_eject: int = 0
    read_only_format: int = 0
    tape_directory_corrupted_on_load: int = 0
    nearing_media_life: int = 0
    cleaning_required: int = 0
    cleaning_requested: int = 0
    expired_cleaning_media: int = 0
    invalid_cleaning_tape: int = 0
    retension_requested: int = 0
    dual_port_interface_error: int = 0
    cooling_fan_failing: int = 0
    power_supply_failure: int = 0
    power_consumption: int = 0
    drive_maintenance: int = 0
    hardware_A: int = 0
    hardware_B: int = 0
    interface: int = 0
    eject_media: int = 0
    microcode_update_fail: int = 0
    drive_humidity: int = 0
    drive_temperature: int = 0
    drive_voltage: int = 0
    predictive_failure: int = 0
    diagnostics_required: int = 0
    obsolete_28h: int = 0
    obsolete_29h: int = 0
    obsolete_2Ah: int = 0
    obsolete_2Bh: int = 0
    obsolete_2Ch: int = 0
    obsolete_2Dh: int = 0
    obsolete_2Eh: int = 0
    reserved_2Fh: int = 0
    reserved_30h: int = 0
    reserved_31h: int = 0
    lost_statistics: int = 0
    tape_directory_invalid_at_unload: int = 0
    tape_system_area_write_failure: int = 0
    tape_system_area_read_failure: int = 0
    no_start_of_data: int = 0
    loading_failure: int = 0
    unrecoverable_unload_failure: int = 0
    automation_interface_failure: int = 0
    firmware_failure: int = 0
    worm_medium_integrity_check_failed: int = 0
    worm_medium_overwrite_attempted: int = 0
    reserved_parameter_code_0x3d_flag: int = 0
    reserved_parameter_code_0x3e_flag: int = 0
    reserved_parameter_code_0x3f_flag: int = 0
    reserved_parameter_code_0x40_flag: int = 0


def from_text(text):
    re = TapeAlert()
    textarr = text.split('\n')
    re.read_warning = utils.extract_int(textarr[0], sep=':')
    re.write_warning = utils.extract_int(textarr[1], sep=':')
    re.hard_error = utils.extract_int(textarr[2], sep=':')
    re.media = utils.extract_int(textarr[3], sep=':')
    re.read_failure = utils.extract_int(textarr[4], sep=':')
    re.write_failure = utils.extract_int(textarr[5], sep=':')
    re.media_life = utils.extract_int(textarr[6], sep=':')
    re.not_data_grade = utils.extract_int(textarr[7], sep=':')
    re.write_protect = utils.extract_int(textarr[8], sep=':')
    re.no_removal = utils.extract_int(textarr[9], sep=':')
    re.cleaning_media = utils.extract_int(textarr[10], sep=':')
    re.unsupported_format = utils.extract_int(textarr[11], sep=':')
    re.recoverable_mechanical_cartridge_failure = utils.extract_int(textarr[12], sep=':')
    re.unrecoverable_mechanical_cartridge_failure = utils.extract_int(textarr[13], sep=':')
    re.memory_chip_in_cartridge_failure = utils.extract_int(textarr[14], sep=':')
    re.forced_eject = utils.extract_int(textarr[15], sep=':')
    re.read_only_format = utils.extract_int(textarr[16], sep=':')
    re.tape_directory_corrupted_on_load = utils.extract_int(textarr[17], sep=':')
    re.nearing_media_life = utils.extract_int(textarr[18], sep=':')
    re.cleaning_required = utils.extract_int(textarr[19], sep=':')
    re.cleaning_requested = utils.extract_int(textarr[20], sep=':')
    re.expired_cleaning_media = utils.extract_int(textarr[21], sep=':')
    re.invalid_cleaning_tape = utils.extract_int(textarr[22], sep=':')
    re.retension_requested = utils.extract_int(textarr[23], sep=':')
    re.dual_port_interface_error = utils.extract_int(textarr[24], sep=':')
    re.cooling_fan_failing = utils.extract_int(textarr[25], sep=':')
    re.power_supply_failure = utils.extract_int(textarr[26], sep=':')
    re.power_consumption = utils.extract_int(textarr[27], sep=':')
    re.drive_maintenance = utils.extract_int(textarr[28], sep=':')
    re.hardware_A = utils.extract_int(textarr[29], sep=':')
    re.hardware_B = utils.extract_int(textarr[30], sep=':')
    re.interface = utils.extract_int(textarr[31], sep=':')
    re.eject_media = utils.extract_int(textarr[32], sep=':')
    re.microcode_update_fail = utils.extract_int(textarr[33], sep=':')
    re.drive_humidity = utils.extract_int(textarr[34], sep=':')
    re.drive_temperature = utils.extract_int(textarr[35], sep=':')
    re.drive_voltage = utils.extract_int(textarr[36], sep=':')
    re.predictive_failure = utils.extract_int(textarr[37], sep=':')
    re.diagnostics_required = utils.extract_int(textarr[38], sep=':')
    re.obsolete_28h = utils.extract_int(textarr[39], sep=':')
    re.obsolete_29h = utils.extract_int(textarr[40], sep=':')
    re.obsolete_2Ah = utils.extract_int(textarr[41], sep=':')
    re.obsolete_2Bh = utils.extract_int(textarr[42], sep=':')
    re.obsolete_2Ch = utils.extract_int(textarr[43], sep=':')
    re.obsolete_2Dh = utils.extract_int(textarr[44], sep=':')
    re.obsolete_2Eh = utils.extract_int(textarr[45], sep=':')
    re.reserved_2Fh = utils.extract_int(textarr[46], sep=':')
    re.reserved_30h = utils.extract_int(textarr[47], sep=':')
    re.reserved_31h = utils.extract_int(textarr[48], sep=':')
    re.lost_statistics = utils.extract_int(textarr[49], sep=':')
    re.tape_directory_invalid_at_unload = utils.extract_int(textarr[50], sep=':')
    re.tape_system_area_write_failure = utils.extract_int(textarr[51], sep=':')
    re.tape_system_area_read_failure = utils.extract_int(textarr[52], sep=':')
    re.no_start_of_data = utils.extract_int(textarr[53], sep=':')
    re.loading_failure = utils.extract_int(textarr[54], sep=':')
    re.unrecoverable_unload_failure = utils.extract_int(textarr[55], sep=':')
    re.automation_interface_failure = utils.extract_int(textarr[56], sep=':')
    re.firmware_failure = utils.extract_int(textarr[57], sep=':')
    re.worm_medium_integrity_check_failed = utils.extract_int(textarr[58], sep=':')
    re.worormm_medium_overwrite_attempted = utils.extract_int(textarr[59], sep=':')
    re.reserved_parameter_code_0x3d_flag = utils.extract_int(textarr[60], sep=':')
    re.reserved_parameter_code_0x3e_flag = utils.extract_int(textarr[61], sep=':')
    re.reserved_parameter_code_0x3f_flag = utils.extract_int(textarr[62], sep=':')
    re.reserved_parameter_code_0x40_flag = utils.extract_int(textarr[63], sep=':')

    # re.page_valid = utils.extract_int(textarr[0], sep=':')
    return re
