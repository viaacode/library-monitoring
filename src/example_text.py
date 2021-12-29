text="""
    [miker@dg-qas-tra-01 python-scsi]$ sudo sg_logs -a /dev/sg7
        IBM       ULT3580-TD6       KAJ8

    Supported log pages  (spc-2) [0x0]:
        0x00        Supported log pages
        0x02        Error counters (write)
        0x03        Error counters (read)
        0x06        Non-medium errors
        0x0c            Sequential access device (ssc-2)
        0x11            DT Device status (ssc-3)
        0x12        Tape alert response (ssc-3)
        0x14        Device statistics (ssc-3)
        0x16        Tape diagnostic (ssc-3)
        0x17        Volume statistics (ssc-4)
        0x1a        Power condition transition
        0x1b        Data compression (ssc-4)
        0x2e        TapeAlert (ssc-2)
        0x30        Tape usage (IBM specific)
        0x31        Tape capacity (IBM specific)
        0x32        Data compression (IBM specific)
        0x33        [unknown vendor specific page code]
        0x34        [unknown vendor specific page code]
        0x37        [unknown vendor specific page code]
        0x38        [unknown vendor specific page code]
        0x39        [unknown vendor specific page code]
        0x3b        [unknown vendor specific page code]
        0x3c        [unknown vendor specific page code]
        0x3d        [unknown vendor specific page code]

    Write error counter page  (spc-3) [0x2]
    Errors corrected without substantial delay = 0
    Errors corrected with possible delays = 0
    Total rewrites or rereads = 0
    Total errors corrected = 0
    Total times correction algorithm processed = 0
    Total bytes processed = 0
    Total uncorrected errors = 0
    Reserved or vendor specific [0x8000] = 0
    Reserved or vendor specific [0x8001] = 0

    Read error counter page  (spc-3) [0x3]
    Errors corrected without substantial delay = 0
    Errors corrected with possible delays = 0
    Total rewrites or rereads = 0
    Total errors corrected = 0
    Total times correction algorithm processed = 0
    Total bytes processed = 0
    Total uncorrected errors = 0
    Reserved or vendor specific [0x8000] = 0

    Non-medium error page  (spc-2) [0x6]
    Non-medium error count = 0

    Sequential access device page (ssc-3)
    Data bytes received with WRITE commands: 0 GB
    Data bytes written to media by WRITE commands: 0 GB
    Data bytes read from media by READ commands: 0 GB
    Data bytes transferred by READ commands: 0 GB
    Native capacity from BOP to EOD: 4294967295 MB
    Native capacity from BOP to EW of current partition: 4294967295 MB
    Minimum native capacity from EW to EOP of current partition: 4294967295 MB
    Native capacity from BOP to current position: 4294967295 MB
    Maximum native capacity in device object buffer: 679 MB
    Cleaning action not required (or completed)
    Vendor specific parameter [0x8000] value: 31099778
    Vendor specific parameter [0x8001] value: 419
    Vendor specific parameter [0x8002] value: 0
    Vendor specific parameter [0x8003] value: 247318918

    DT device status page (ssc-3, adc-3) [0x11]
    Very high frequency data:
    PAMR=0 HUI=1 MACC=0 CMPR=1 WRTP=1 CRQST=0 CRQRD=0 DINIT=1
    INXTN=0 RAA=1 MPRSNT=1 MSTD=0 MTHRD=0 MOUNTED=0
    DT device activity: No DT device activity
    VS=0 TDDEC=0 EPP=0 ESR=0 RRQST=0 INTFC=0 TAFC=0
    Very high frequency polling delay:  500 milliseconds
    DT device ADC data encryption control status (hex only now):
    00     00 00 00 00 00 00 00 00
    Key management error data (hex only now):
    00     00 00 00 00 00 00 00 00  00 00 00 00
    Reserved [parameter_code=0x4]:
    00     00 04 03 08 59 30 00 00  01 03 00 00                ....Y0......
    Reserved [parameter_code=0x101]:
    00     01 01 43 18 ab 5b 1c 00  00 00 00 7e 50 05 07 60    ..C..[.....~P..`
    10     44 4f 92 05 50 05 07 60  44 0f 92 05                DO..P..`D...
    Reserved [parameter_code=0x102]:
    00     01 02 43 18 ab 5c 1c 00  00 00 00 7e 50 05 07 60    ..C..\.....~P..`
    10     44 8f 92 05 50 05 07 60  44 0f 92 05                D...P..`D...
    Reserved [parameter_code=0x200]:
    00     02 00 03 01 01                                      .....
    Reserved [parameter_code=0x201]:
    00     02 01 03 2b 15 00 00 00  03 00 0a 03 00 01 7c cc    ...+..........|.
    10     d9 35 b4 00 00 00 02 00  00 00 00 00 00 00 00 10    .5..............
    20     00 00 90 fa 48 5d cb 00  00 00 00 00 00 00 00       ....H].........
    Reserved [parameter_code=0x8000]:
    00     80 00 43 08 51 49 4d 30  30 31 4c 36                ..C.QIM001L6
    Reserved [parameter_code=0x8001]:
    00     80 01 43 04 0f 45 00 00                             ..C..E..
    Reserved [parameter_code=0x8100]:
    00     81 00 43 04 00 01 00 00                             ..C.....
    Reserved [parameter_code=0x9101]:
    00     91 01 43 04 00 00 00 00                             ..C.....
    Reserved [parameter_code=0x9102]:
    00     91 02 43 04 00 00 00 00                             ..C.....
    Reserved [parameter_code=0xe000]:
    00     e0 00 43 ff 00 00 00 00  00 00 00 00 00 00 00 00    ..C.............
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    e0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    f0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    100    00 00 00                                            ...

    No ascii information for page = 0x12, here is hex:
    00     12 00 00 0c 00 00 43 08  00 00 00 00 00 00 00 00

    Device statistics page (ssc-3 and adc)
    Lifetime media loads: 419
    Lifetime cleaning operations: 0
    Lifetime power on hours: 68700
    Lifetime media motion (head) hours: 121
    Lifetime metres of tape processed: 1832585
    Lifetime media motion (head) hours when incompatible media last loaded: 112
    Lifetime power on hours when last temperature condition occurred: 0
    Lifetime power on hours when last power consumption condition occurred: 0
    Media motion (head) hours since last successful cleaning operation: 121
    Media motion (head) hours since 2nd to last successful cleaning: 121
    Media motion (head) hours since 3rd to last successful cleaning: 121
    Lifetime power on hours when last operator initiated forced reset
        and/or emergency eject occurred: 0
    Reserved parameter [0xc] value: 44
    Reserved parameter [0xd] value: 288
    Reserved parameter [0xe] value: 0
    Reserved parameter [0xf] value: 0
    Reserved parameter [0x10] value: 5184129388
    Reserved parameter [0x11] value: 0
    Reserved parameter [0x12] value: 0
    Reserved parameter [0x13] value: 0
    Reserved parameter [0x14] value: 81
    Reserved parameter [0x15] value: 9
    Reserved parameter [0x40] value: 4053856719166701568
    Reserved parameter [0x41] value: 4053856719166701568
    Reserved parameter [0x80] value: 0
    Reserved parameter [0x81] value: 0
    Media motion (head) hours for each medium type:
        <<to be decoded, dump in hex for now>>:
    00     10 00 03 30 00 00 46 48  00 00 00 00 00 00 46 4c    ...0..FH......FL
    10     00 00 00 00 00 00 58 58  00 00 00 1c 00 00 58 5c    ......XX......X\
    20     00 00 00 00 00 00 5a 68  00 00 00 5e 00 00 5a 6c    ......Zh...^..Zl
    30     00 00 00 00                                         ....

    Tape diagnostics data page (ssc-3) [0x16]
    Parameter code: 0
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 1
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 2
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 3
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 4
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 5
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 6
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 7
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 8
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 9
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 10
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00
    Parameter code: 11
        Density code: 0x0
        Medium type: 0x0
        Lifetime media motion hours: 0
        Repeat: 0
        Sense key: 0x0 [No Sense]
        Additional sense code: 0x0
        Additional sense code qualifier: 0x0
        Vendor specific code qualifier: 0x0
        Product revision level: 0
        Hours since last clean: 0
        Operation code: 0x0
        Service action: 0x0
        Medium id number (in hex):
    00     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
    10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00    ................
        Timestamp origin: 0x0
        Timestamp:
    00     00 00 00 00 00 00

    Volume statistics page (ssc-4) but subpage=0, abnormal: treat like subpage=1
    Page valid: 1
    Thread count: 107
    Total data sets written: 61423
    Total write retries: 35
    Total unrecovered write errors: 0
    Total suspended writes: 0
    Total fatal suspended writes: 0
    Total data sets read: 1921618
    Total read retries: 3
    Total unrecovered read errors: 0
    Last mount unrecovered write errors: 0
    Last mount unrecovered read errors: 0
    Last mount megabytes written: 0
    Last mount megabytes read: 17
    Lifetime megabytes written: 151840
    Lifetime megabytes read: 4750316
    Last load write compression ratio: 0
    Last load read compression ratio: 0
    Medium mount time: 505713682
    Medium ready time: 505701719
    Total native capacity: 2463234
    Total used native capacity: 151792
    Volume serial number: MF59TWPPJE
    Tape lot identifier: G6ABELGV
    Volume barcode: QIM001L6
    Volume manufacturer: FUJIFILM
    Volume license code: 0707
    Volume personality: Ultrium-6
    Write protect: 1
    WORM: 0
    Maximum recommended tape path temperature exceeded: 0
    Beginning of medium passes: 1686
    Middle of medium passes: 401
    Logical position of first encrypted logical object:
        partition number: 0, partition record data counter: 0xffffffffffff
        partition number: 1, partition record data counter: 0xffffffffffff
    Logical position of first unencrypted logical object after first
    encrypted logical object:
        partition number: 0, partition record data counter: 0xffffffffffff
        partition number: 1, partition record data counter: 0xffffffffffff
    Native capacity partition(s):
        partition number: 0, partition record data counter: 36764
        partition number: 1, partition record data counter: 2426470
    Used native capacity partition(s):
        partition number: 0, partition record data counter: 14
        partition number: 1, partition record data counter: 151778
    Remaining native capacity partition(s):
        partition number: 0, partition record data counter: 36746
        partition number: 1, partition record data counter: 2280733

    Power condition transitions page  (spc-4) [0x1a]
    Accumulated transitions to idle_a = 164
    Reserved [0x4] = 186

    Data compression page  (ssc-4) [0x1b]
    Read compression ratio x100: 0
    Write compression ratio x100: 0
    Megabytes transferred to server: 0
    Bytes transferred to server: 0
    Megabytes read from tape: 0
    Bytes read from tape: 0
    Megabytes transferred from server: 0
    Bytes transferred from server: 0
    Megabytes written to tape: 0
    Bytes written to tape: 0
    Data compression enabled: 0x1

    Tape alert page (ssc-3) [0x2e]
    Read warning: 0
    Write warning: 0
    Hard error: 0
    Media: 0
    Read failure: 0
    Write failure: 0
    Media life: 0
    Not data grade: 0
    Write protect: 0
    No removal: 0
    Cleaning media: 0
    Unsupported format: 0
    Recoverable mechanical cartridge failure: 0
    Unrecoverable mechanical cartridge failure: 0
    Memory chip in cartridge failure: 0
    Forced eject: 0
    Read only format: 0
    Tape directory corrupted on load: 0
    Nearing media life: 0
    Cleaning required: 0
    Cleaning requested: 0
    Expired cleaning media: 0
    Invalid cleaning tape: 0
    Retension requested: 0
    Dual port interface error: 0
    Cooling fan failing: 0
    Power supply failure: 0
    Power consumption: 0
    Drive maintenance: 0
    Hardware A: 0
    Hardware B: 0
    Interface: 0
    Eject media: 0
    Microcode update fail: 0
    Drive humidity: 0
    Drive temperature: 0
    Drive voltage: 0
    Predictive failure: 0
    Diagnostics required: 0
    Obsolete (28h): 0
    Obsolete (29h): 0
    Obsolete (2Ah): 0
    Obsolete (2Bh): 0
    Obsolete (2Ch): 0
    Obsolete (2Dh): 0
    Obsolete (2Eh): 0
    Reserved (2Fh): 0
    Reserved (30h): 0
    Reserved (31h): 0
    Lost statistics: 0
    Tape directory invalid at unload: 0
    Tape system area write failure: 0
    Tape system area read failure: 0
    No start of data: 0
    Loading failure: 0
    Unrecoverable unload failure: 0
    Automation interface failure: 0
    Firmware failure: 0
    WORM medium - integrity check failed: 0
    WORM medium - overwrite attempted: 0
    Reserved parameter code 0x3d, flag: 0
    Reserved parameter code 0x3e, flag: 0
    Reserved parameter code 0x3f, flag: 0
    Reserved parameter code 0x40, flag: 0

    Tape usage page  (IBM specific) [0x30]
    Thread count: 107
    Total data sets written: 61423
    Total write retries: 35
    Total unrecovered write errors: 0
    Total suspended writes: 0
    Total fatal suspended writes: 0
    Total data sets read: 1921618
    Total read retries: 3
    Total unrecovered read errors: 0
    Total suspended reads: 0
    Total fatal suspended reads: 0

    Tape capacity page  (IBM specific) [0x31]
    Main partition remaining capacity (in MiB): 35043
    Alternate partition remaining capacity (in MiB): 2175076
    Main partition maximum capacity (in MiB): 35060
    Alternate partition maximum capacity (in MiB): 2314062

    Data compression page  (IBM specific) [0x32]
    Read compression ratio x100: 0
    Write compression ratio x100: 0
    Megabytes transferred to server: 0
    Bytes transferred to server: 0
    Megabytes read from tape: 0
    Bytes read from tape: 0
    Megabytes transferred from server: 0
    Bytes transferred from server: 0
    Megabytes written to tape: 0
    Bytes written to tape: 0

    No ascii information for page = 0x33, here is hex:
    00     33 00 00 6c 00 00 40 02  00 00 00 01 40 02 00 00
    10     00 02 40 02 00 00 00 03  40 02 00 00 00 04 40 02
    20     00 00 00 05 40 02 00 00  00 06 40 02 00 00 00 07
    30     40 02 00 00 00 08 40 02  00 00 00 09 40 02 00 00
    40     00 0a 40 02 00 00 00 0b  40 02 00 00 00 0c 40 02
    50     00 00 00 0d 40 02 00 00  00 0e 40 02 00 00 00 0f
    60     40 02 00 00 00 10 40 02  00 00 00 11 40 02 00 00

    No ascii information for page = 0x34, here is hex:
    00     34 00 00 ba 00 00 40 02  00 00 00 01 40 02 00 00
    10     00 02 40 02 00 00 00 03  40 02 00 00 00 04 40 02
    20     00 00 00 05 40 02 00 00  00 06 40 02 00 00 00 07
    30     40 02 00 00 00 08 40 02  00 00 00 09 40 02 00 00
    .....  [truncated after 64 of 190 bytes (use '-H' to see the rest)]

    No ascii information for page = 0x37, here is hex:
    00     37 00 00 1e 00 00 60 01  0f 00 01 60 01 0a 00 10
    10     60 01 80 00 11 60 01 80  00 12 60 01 80 00 1a 60
    20     01 00

    No ascii information for page = 0x38, here is hex:
    00     38 00 00 8a 00 00 40 04  00 00 00 00 00 01 40 04
    10     00 00 00 00 00 02 40 04  00 00 00 00 00 03 40 04
    20     00 00 00 00 00 04 40 04  00 00 00 00 00 05 40 04
    30     00 00 00 00 00 06 40 04  00 00 00 00 00 07 40 04
    .....  [truncated after 64 of 142 bytes (use '-H' to see the rest)]

    No ascii information for page = 0x39, here is hex:
    00     39 00 00 26 00 00 40 02  00 00 00 07 40 02 00 00
    10     00 08 40 02 00 00 00 09  40 02 00 00 00 0a 40 02
    20     00 00 00 10 40 04 00 00  00 00

    No ascii information for page = 0x3b, here is hex:
    00     3b 00 00 26 00 00 40 02  00 00 00 07 40 02 00 00
    10     00 08 40 02 00 00 00 09  40 02 00 00 00 0a 40 02
    20     00 00 00 10 40 04 00 00  00 00

    No ascii information for page = 0x3c, here is hex:
    00     3c 00 00 aa 00 01 40 08  00 00 00 00 00 00 ed af
    10     00 02 40 08 00 00 00 00  00 00 00 01 00 03 40 08
    20     00 00 00 00 00 bf 09 56  00 04 40 08 00 00 00 00
    30     00 87 6a db 00 05 40 08  00 00 00 00 00 00 00 2c
    .....  [truncated after 64 of 174 bytes (use '-H' to see the rest)]

    No ascii information for page = 0x3d, here is hex:
    00     3d 00 01 08 00 20 40 04  00 00 00 6b 00 21 40 04
    10     00 02 51 20 00 22 40 04  00 48 7b ec 00 40 40 04
    20     00 00 01 a3 00 41 40 04  00 02 4b 90 00 42 40 04
    30     01 d8 3f f2 00 60 40 04  00 00 00 00 00 61 40 04
    .....  [truncated after 64 of 268 bytes (use '-H' to see the rest)]

    """
