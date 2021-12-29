def assert_lines(thetext, linecount):
    assert thetext.count('\n')+1 == linecount

def split_sg_output(sg_output: str):
    _, rest = sg_output.split("Write error counter page  (spc-3) [0x2]")
    write_err, rest = rest.split("Read error counter page  (spc-3) [0x3]")
    write_err = write_err.strip()
    assert_lines(write_err, 9)

    read_err, rest = rest.split("Non-medium error page  (spc-2) [0x6]")
    read_err = read_err.strip()
    assert_lines(read_err, 8)

    non_med_err, rest = rest.split("Sequential access device page (ssc-3)")
    non_med_err = non_med_err.strip()
    assert_lines(non_med_err, 1)

    seq_access, rest = rest.split("DT device status page (ssc-3, adc-3) [0x11]")
    seq_access = seq_access.strip()
    assert_lines(seq_access, 14)

    _, rest = rest.split("Device statistics page (ssc-3 and adc)")
    dev_stats, rest = rest.split("Tape diagnostics data page (ssc-3) [0x16]")
    dev_stats = dev_stats.strip()
    assert_lines(dev_stats, 32)

    _, rest = rest.split("Volume statistics page (ssc-4) but subpage=0, abnormal: treat like subpage=1")
    vol_stats, rest = rest.split("Power condition transitions page  (spc-4) [0x1a]")
    vol_stats = vol_stats.strip()
    assert_lines(vol_stats, 49)

    _, rest = rest.split("Tape alert page (ssc-3) [0x2e]")
    tape_alert, rest = rest.split("Tape usage page  (IBM specific) [0x30]")
    tape_alert = tape_alert.strip()
    assert_lines(tape_alert, 64)


    tape_usage, rest  = rest.split("Tape capacity page  (IBM specific) [0x31]")
    tape_usage = tape_usage.strip()
    assert_lines(tape_usage, 11)

    tape_cap, rest = rest.split("Data compression page  (IBM specific) [0x32]")
    assert_lines(tape_cap, 7)

    return write_err, read_err, non_med_err, seq_access, dev_stats, vol_stats, tape_alert, tape_usage, tape_cap
