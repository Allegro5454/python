#!/usr/bin/env python3
import argparse
import json
import logging
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', required=True, help="Path to the scaned file")
parser.add_argument('--level', '-l', default=3, help="Filter data by importancy level in 1-6 scale")
parser.add_argument('--export', '-e', help="Exports wanted information into json" )
args = parser.parse_args()
logging.basicConfig(level="INFO")
def make_dicts(log_input, level, export ):
    log = { }
    level = int(level)
    with open(log_input, 'r') as file:
        try:
            for line in file:
                data = json.loads(line)
                name = data.get("_SYSTEMD_UNIT")
                message = data.get("MESSAGE")
                priority = data.get("PRIORITY")
                if priority is not None and name is not None:
                    priority = int(priority)
                    if priority <= level and name is not None:
                        if name not in log:
                            log[name] = {"count": 0, "messages": []}
                        log[name]["count"] += 1
                        if message:
                            log[name]["messages"].append(message)
            asc = {k: v for k, v in sorted(log.items(), key=lambda item: item[1]["count"], reverse=True)}
            logging.info(json.dumps(asc, indent=4)) 
            if export:
                with open(export, 'w') as f:
                    json.dump(asc, f, indent=4 )    
        except json.JSONDecodeError:
            logging.critical("Failed to open json file")
make_dicts(args.file, args.level, args.export)
