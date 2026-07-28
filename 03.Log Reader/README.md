# LOG_READ = LOG READER

# INFO
A Python script that reads and parses `journalctl` JSON logs. It groups data by systemd unit, counts occurrences, and prints the output in a structured JSON format for easy access to information.

Arguments:
- `--file`: Input file. REQUIRED
-`--export`: Output file. If not specified work will be seen only on stdout
-`--level`: Level of information in 1-6 scale. 1 - critical, 6 - everything. Default value = 3. 

# EXAMPLES
Read critical errors from the last 10 minutes:
journalctl -o json -S "10 minutes ago" > your_file.log
./LOG_READ.py -l 1 -f /path/to/directory/your_file.log

Read all of the information and save it to another file 
./LOG_READ.py --file /path/to/directory/your_file.log --export report.json

# HOW TO START
chmod +x LOG_READ.py
./LOG_READ.py
