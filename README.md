# Meemoo tape library monitoring

## Installation

* install pipenv
* install python3 (tested on 3.9)

* `pipenv install`
* `pipenv shell`
* `./monitor.sh'

```bash
(library-monitoring)  m@ > ./monitor.sh --help
usage: meemoo.py [-h] [-i [INTERVAL]] -o HOST -d DATABASENAME -u USERNAME -p PASSWORD [-f] [-x] [--erasedb] [--erasedbonly] (--devices DEVICES [DEVICES ...] | --devicefile DEVICEFILE)

Meemoo tape monitoring tool

optional arguments:
  -h, --help            show this help message and exit
  -i [INTERVAL], --interval [INTERVAL]
                        The polling interval used to gather scsi drive/tape information.
  -o HOST, --host HOST  Postgres server name
  -d DATABASENAME, --databasename DATABASENAME
                        Postgres database name
  -u USERNAME, --username USERNAME
                        Postgres username
  -p PASSWORD, --password PASSWORD
                        Postgres password
  -f, --fake            Use fake static data instead of real SCSI results
  -x, --verbose         Set logging to debug mode
  --erasedb             Recreate DB Table (Warning: all data will be lost!!!)
  --erasedbonly         Recreate DB Table (Warning: all data will be lost!!!) and exit
  --devices DEVICES [DEVICES ...]
                        List of devices to monitor
  --devicefile DEVICEFILE
                        A txt file with each line having one device to monitor from /dev/tape/by-id/*
```

## Running
### Manual

Starting monitoring with fresh and empty database tables:
```bash
./monitor.sh -i 300 --devices /dev/tape/by-id/scsi-123 -o database.meemoo.be -d tapemonitor -u tapemonitor -p secret_password --erasedb
```

### Using systemd

Copy the systemd unit file:

```sudo cp ./support/meemoomonitor.service /etc/systemd/system```

Let systemd know there's a new unit file

```sudo systemctl daemon-reload```

Tell systemd to enable our file, so that it will start every time we boot:

```sudo systemctl enable meemoomonitor.service```

Start it now:

```sudo systemctl start meemoomonitor.service```

See it's status:

```sudo systemctl status meemoomonitor.service```

### Helper scripts

```journal.sh``` ==> show the systemd logs for meemoomoniter.service
```system.sh``` ==> perform systemd commands for meemoomoniter.service, such as 'start', 'stop', 'status', 'restart'
```dellogs.sh``` ==> delete local log files (not the systemd ones)
```monitor.sh``` ==> convenience wrapper to start the python monitoring, usually not called directly
```start.sh``` ==> main entry for starting the python monitoring, both for local testing and for the systemd unit file
