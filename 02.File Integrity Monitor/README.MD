# FIM - FILE INTEGRITY MONITOR

# INFO
Script that saves or compares hash record of specified directory.
Works in 2 major modes:
- `--init`: Saves hash record of content of directory
- `--check`: Compares previous hash record with current state
Remaining arguments:
- `--target`: Directory for checking. Required in both modes.
- `--log`: Saves a log file in JSON in specified path.
- `--state`: If used in init mode: saves hash state into specified file.
             If used in check mode: Compares hash record in the specified file with current state.
             If not specified it defaults to fim_state.json
# EXAMPLES
Initialize monitoring for a directory:
./FIM.py --init --target /path/to/directory

Check directory against default state file and save log:
./FIM.py --check --target /path/to/directory --log report.json

Use custom state file:
./FIM.py --init --target /path/to/directory --state my_custom_state.json

# HOW TO START
chmod +x FIM.py
./FIM.py
