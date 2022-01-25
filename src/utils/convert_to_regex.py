
text = """ Lifetime media loads: 420
  Lifetime cleaning operations: 0
  Lifetime power on hours: 70459
  Lifetime media motion (head) hours: 123
  Lifetime metres of tape processed: 1878268
  Lifetime media motion (head) hours when incompatible media last loaded: 112
  Lifetime power on hours when last temperature condition occurred: 0
  Lifetime power on hours when last power consumption condition occurred: 0
  Media motion (head) hours since last successful cleaning operation: 123
  Media motion (head) hours since 2nd to last successful cleaning: 123
  Media motion (head) hours since 3rd to last successful cleaning: 123
  Lifetime power on hours when last operator initiated forced reset
    and/or emergency eject occurred: 0
  Lifetime power cycles: 44
  Volume loads since last parameter reset: 289
  Hard write errors: 0
  Hard read errors: 0
  Duty cycle sample time (ms): 11515778172
  Read duty cycle: 0
  Write duty cycle: 0
  Activity duty cycle: 0
  Volume not present duty cycle: 65
  Ready duty cycle: 23
  Drive manufacturer's serial number: 0
  Drive serial number: 0
  Medium removal prevented: 0
  Maximum recommended mechanism temperature exceeded: 0
  Media motion (head) hours for each medium type:
    Density code: 0x46, Medium type: 0x48
      Medium motion hours: 0
    Density code: 0x46, Medium type: 0x4c
      Medium motion hours: 0
    Density code: 0x58, Medium type: 0x58
      Medium motion hours: 28
    Density code: 0x58, Medium type: 0x5c
      Medium motion hours: 0
    Density code: 0x5a, Medium type: 0x68
      Medium motion hours: 96
    Density code: 0x5a, Medium type: 0x6c
      Medium motion hours: 0
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
