# SYS_MON = System Monitor

# INFO
Script that saves basic system information in json format.
Accessed via file or http server.
Information saved for different devices:
- `Disks = Usage`
- `Network Interface = IP address`
- `Service = State`

# REQUIREMENTS
-`psutil`
Can be installed with ```pip install psutil```

# Configuration
Configuration is read from config.json in the starting directory of the script.
```{
    "type":"StorageDrive",
    "name":"Name of the drive",
    "status":"Active",
    "mount_point":"partition mount point"
},```
Full configuration can be seen in the attached config.json file.

# HOW TO START AND ACCESS DATA?
Starting the script - `python3 SYS_MON.py`
Accessing data via console - `curl IP:PORT`