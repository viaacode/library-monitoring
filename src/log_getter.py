import os
import logging
from example_text import text
import models.write_error as write_error
import models.read_error as read_error
import models.non_med_err as non_med_err
import models.seq_access as seq_access
import models.dev_stats as dev_stats
import models.vol_stats as vol_stats
import models.power_conditions as power_conditions
import models.tape_alert as tape_alert
import models.tape_usage as tape_usage
import models.tape_cap as tape_cap
import utils
import subprocess

class LogGetter:
    """ Class for getting the logs """
    def __init__(self, fake=False):
        self.fake = fake

    def get_logpages(self, device):
        output = None
        if self.fake:
            output = self.sg_output_as_dict(text)
        else:
            real_logpages = self.get_real_logpages(device)
            if real_logpages:
                output = self.sg_output_as_dict(real_logpages)
        return output

    def get_real_logpages(self, device):
        output  = None
        try:
             output = subprocess.run(['sg_logs', '-a', device], check=True, stdout=subprocess.PIPE, text=True).stdout
        except subprocess.CalledProcessError as err:
             logging.error(f"An error occurred calling sg_logs: {err}")
        return output

    def assert_nr_lines(self, textarr, linecount):
        counted_lines = len(textarr)
        assert counted_lines >= linecount, f"Linecount should be >= {linecount} but is {counted_lines} for text {textarr}"

    def sg_output_as_dict(self, text: str):
        if text is None:
            return text
        write_err_arr, read_err_arr, non_med_err_arr, seq_access_arr, dev_stats_arr, vol_stats_arr, power_conditions_arr, tape_alert_arr, tape_usage_arr, tape_cap_arr = self.split_sg_output(text)
        return {"write_err": write_error.from_arr(write_err_arr),
                "read_err": read_error.from_arr(read_err_arr),
                "non_med_err": non_med_err.from_arr(non_med_err_arr),
                "seq_access": seq_access.from_arr(seq_access_arr),
                "dev_stats": dev_stats.from_arr(dev_stats_arr),
                "vol_stats": vol_stats.from_arr(vol_stats_arr),
                "power_conditions": power_conditions.from_arr(power_conditions_arr),
                "tape_alert": tape_alert.from_arr(tape_alert_arr),
                "tape_usage": tape_usage.from_arr(tape_usage_arr),
                "tape_cap": tape_cap.from_arr(tape_cap_arr)}

    def split_sg_output(self, sg_output: str, debug=False):
        lines = [x.strip() for x in sg_output.strip().split('\n') if x is not None and x.strip() != '']

        write_err = self.get_lines_between_ids('\[0x2\]', '\[0x3\]', lines)
        self.assert_nr_lines(write_err, 9)
        logging.debug(f"write_err: {write_err}")

        read_err  = self.get_lines_between_ids('\[0x3\]', '\[0x6\]', lines)
        self.assert_nr_lines(read_err, 8)
        logging.debug(f"read_err: {read_err}")

        non_med_err  = self.get_lines_between_ids('\[0x6\]', 'Sequential access device page', lines)
        self.assert_nr_lines(non_med_err, 1)
        logging.debug(f"non med err: {non_med_err}")

        seq_access  = self.get_lines_between_ids('Sequential access device page', '\[0x11\]', lines)
        self.assert_nr_lines(seq_access, 14)
        logging.debug(f"seq access: {seq_access}")

        dev_stats = self.get_lines_between_ids('Device statistics page', '\[0x16\]', lines)
        self.assert_nr_lines(dev_stats, 32)
        logging.debug(f"dev stats: {dev_stats}")

        vol_stats = self.get_lines_between_ids('Volume statistics page', '\[0x1a\]', lines)
        self.assert_nr_lines(vol_stats, 49)
        logging.debug(f"vol_stats: {vol_stats}")

        power_conditions = self.get_lines_between_ids('\[0x1a\]', '\[0x1b\]', lines)
        self.assert_nr_lines(power_conditions, 2)
        logging.debug(f"power_conditions: {power_conditions}")

        tape_alert = self.get_lines_between_ids('\[0x2e\]', '\[0x30\]', lines)
        self.assert_nr_lines(tape_alert, 64)
        logging.debug(f"tape_alert: {tape_alert}")

        tape_usage = self.get_lines_between_ids('\[0x30\]', '\[0x31\]', lines)
        self.assert_nr_lines(tape_usage, 11)
        logging.debug(f"tape_usage: {tape_usage}")

        tape_cap = self.get_lines_between_ids('\[0x31\]', '\[0x32\]', lines)
        self.assert_nr_lines(tape_cap, 4)
        logging.debug(f"tape_cap: {tape_cap}")

        return write_err, read_err, non_med_err, seq_access, dev_stats, vol_stats, power_conditions, tape_alert, tape_usage, tape_cap

    def get_lines_between_ids(self, start_id, end_id, lines):
        start = utils.get_sglogs_value_of(lines, start_id)
        end = utils.get_sglogs_value_of(lines, end_id)
        logging.debug(f"start is {start}, end is {end}, len lines is {len(lines)}")
        return lines[start+1:end]



