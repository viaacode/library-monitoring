# Meemoo tape library monitoring

## Installation

* install pipenv
* install python3 (tested on 3.9)

* `pipenv install`
* `pipenv shell`
* `./monitor.sh'

```bash
(library-monitoring)  m@ > ./monitor.sh --help
usage: meemoo.py [-h] [-i [INTERVAL]] -d DEVICES [DEVICES ...] -u USERNAME -p PASSWORD [-f] [-s] [-x]

Meemoo tape monitoring tool

optional arguments:
  -h, --help            show this help message and exit
  -i [INTERVAL], --interval [INTERVAL]
                        The polling interval used to gather scsi drive/tape information.
  -d DEVICES [DEVICES ...], --devices DEVICES [DEVICES ...]
                        List of devices to monitor
  -o HOST, --host HOST  Postgres server name
  -u USERNAME, --username USERNAME
                        Postgres username
  -p PASSWORD, --password PASSWORD
                        Postgres password
  -k, --kill            Recreate DB Table (Warning: all data will be lost!!!)
  -f, --fake            Use fake static data instead of real SCSI results
  -x, --verbose         Set logging to debug mode
```

## Running

Starting monitoring with fresh and empty database tables:
```bash
./monitor.sh -i 300 -d /dev/sg7 -o database.meemoo.be -u tapemonitor -p secret_password --kill
```
