# SYNC = Synchronization agent

# INFO
A Python Script that synchronizes two directories or files

Arguments:
- `--From`: Starting location. Required
- `--To`: End location. Required
- `--verbose`: Shows additional information
- `--log`: Logs information into a specified directory
- `--dryrun`: Shows effects of the command without making changes 
# HOW TO USE
**Synchronization of 2 directories**
sync --From /path/to/first/directory --To /path/to/second/directory
**Synchronization with additional information and log to a file**
sync --From /path/to/first/directory --To /path/to/second/directory --log /path/to/log/directory --verbose
**Dry run beetwen 2 directories**
sync --From /path/to/first/directory --To /path/to/second/directory --dryrun

# HOW TO START
chmod +x SYNC.py
./SYNC.py ...
or 
chmod +x SYNC.py
sudo cp chmod +x SYNC.py /usr/local/bin/sync
sync ...
