
text = """Data bytes received with WRITE commands: 0 GB
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
"""
def convert_to_var(input):
    return input.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('[', '').replace(']', '')

if __name__ == "__main__":
    codelist = []
    varlist = []
    for line in text.split('\n'):
        strl = line.strip()
        try:
            first, _ = strl.split(':')
        except:
            print("Could not split", strl)
        varname = convert_to_var(first)
        varlist.append(f'{varname}: int = 0')
        codelist.append(f're.{varname} = utils.get_sglogs_value_of(textarr, "{first}")')
    print('\n'.join(varlist), '\n\n', '\n'.join(codelist))
