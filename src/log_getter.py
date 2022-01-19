import os
from example_text import text
import sglogs_splitter
import models.write_error as write_error
import models.read_error as read_error
import models.non_med_err as non_med_err
import models.seq_access as seq_access
import models.dev_stats as dev_stats
import models.vol_stats as vol_stats
import models.tape_alert as tape_alert
import models.tape_usage as tape_usage
import models.tape_cap as tape_cap

class LogGetter:
    """ Class for getting the logs """
    def __init__(self, fake=False):
        self.fake = fake

    def get_logpages(self, device):
        if self.fake:
            return self.sg_output_as_dict(text)
        else:
            # TODO perform a real sg_logs call
            return self.sg_output_as_dict(self.get_real_logpages(device))

    def get_real_logpages(self, device):
        return os.system(f"sg_logs {device}")

    def assert_nr_lines(self, thetext, linecount):
        assert thetext.count('\n')+1 == linecount

    def sg_output_as_dict(self, text: str):
        write_err_str, read_err_str, non_med_err_str, seq_access_str, dev_stats_str, vol_stats_str, tape_alert_str, tape_usage_str, tape_cap_str = self.split_sg_output(text)
        return {"write_err": write_error.text_to_write_error(write_err_str),
                "read_err": read_error.text_to_read_error(read_err_str),
                "non_med_err": non_med_err.text_to_non_med_error_count(non_med_err_str),
                "seq_access": seq_access.text_to_seq_access(seq_access_str),
                "dev_stats": dev_stats.text_to_dev_stats(dev_stats_str),
                "vol_stats": vol_stats.from_text(vol_stats_str),
                "tape_alert": tape_alert.from_text(tape_alert_str),
                "tape_usage": tape_usage.from_text(tape_usage_str),
                "tape_cap": tape_cap.from_text(tape_cap_str)}

    def split_sg_output(self, sg_output: str):
        _, rest = sg_output.split("Write error counter page  (spc-3) [0x2]")
        write_err, rest = rest.split("Read error counter page  (spc-3) [0x3]")
        write_err = write_err.strip()
        self.assert_nr_lines(write_err, 9)

        read_err, rest = rest.split("Non-medium error page  (spc-2) [0x6]")
        read_err = read_err.strip()
        self.assert_nr_lines(read_err, 8)

        non_med_err, rest = rest.split("Sequential access device page (ssc-3)")
        non_med_err = non_med_err.strip()
        self.assert_nr_lines(non_med_err, 1)

        seq_access, rest = rest.split("DT device status page (ssc-3, adc-3) [0x11]")
        seq_access = seq_access.strip()
        self.assert_nr_lines(seq_access, 14)

        _, rest = rest.split("Device statistics page (ssc-3 and adc)")
        dev_stats, rest = rest.split("Tape diagnostics data page (ssc-3) [0x16]")
        dev_stats = dev_stats.strip()
        self.assert_nr_lines(dev_stats, 32)

        _, rest = rest.split("Volume statistics page (ssc-4) but subpage=0, abnormal: treat like subpage=1")
        vol_stats, rest = rest.split("Power condition transitions page  (spc-4) [0x1a]")
        vol_stats = vol_stats.strip()
        self.assert_nr_lines(vol_stats, 49)

        _, rest = rest.split("Tape alert page (ssc-3) [0x2e]")
        tape_alert, rest = rest.split("Tape usage page  (IBM specific) [0x30]")
        tape_alert = tape_alert.strip()
        self.assert_nr_lines(tape_alert, 64)


        tape_usage, rest  = rest.split("Tape capacity page  (IBM specific) [0x31]")
        tape_usage = tape_usage.strip()
        self.assert_nr_lines(tape_usage, 11)

        tape_cap, rest = rest.split("Data compression page  (IBM specific) [0x32]")
        self.assert_nr_lines(tape_cap, 7)

        return write_err, read_err, non_med_err, seq_access, dev_stats, vol_stats, tape_alert, tape_usage, tape_cap
