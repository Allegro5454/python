#!/usr/bin/env python3
import json
import argparse
import hashlib
import sys
import logging
import datetime
from pathlib import Path
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument( '--init',action='store_true', help="generates sum file of given directory" )
group.add_argument('--check',action='store_true', help="initiate the check")
parser.add_argument('--target',required=True, help="specifies the target directory")
parser.add_argument('--log', help="Saves log into provided file")
parser.add_argument('--state',default="fim_state.json", help="Location of hash record")
args = parser.parse_args()
logging.basicConfig(level=logging.INFO)
def file_list(target_path):
    files = [ ]
    for i in Path(target_path).rglob('*'):
        if i.is_file() and not i.is_symlink():
            files.append(i.resolve())
    return files

def hash_read(one_file):
    with open(one_file, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    return digest.hexdigest()

def run_init(target_path, to_path):
    files = file_list(target_path)
    files_new = {}
    for path_obj in files:
        path_str = str(path_obj)
        file_hash = hash_read(path_str)
        files_new[path_str] = file_hash
    with open(to_path, 'w') as log_file:
        json.dump(files_new, log_file, indent=4)
    logging.info(f"Files hashed: {len(files_new)}")

def run_check(target_path, check_file, out_file):
    try:
        with open(check_file, 'r') as f:
           hash_old = json.load(f)       
    except FileNotFoundError:
        logging.critical("Config file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.critical("Error in config file")
        sys.exit(1)

    files = file_list(target_path)
    hash_new = { }
    date = datetime.datetime.now()
    log = {
        "Date": date.isoformat(),
        "Deleted": [],
        "Created": [],
        "Modified": []
     }
    for path_obj in files:
        path_str = str(path_obj)
        file_hash = hash_read(path_str)
        hash_new[path_str] = file_hash
    new_keys = set(hash_new.keys())
    old_keys = set(hash_old.keys())
    new_files = new_keys - old_keys
    deleted_files = old_keys - new_keys 
    combined_keys = new_keys.intersection(old_keys)
    for inter in combined_keys:
        if hash_new[inter] != hash_old[inter]:
            logging.info(f"Changed File: {inter}")
            log["Modified"].append(inter)
    for file in new_files:
        logging.info(f"New File: {file}")
        log["Created"].append(file)
    for file in deleted_files:
        logging.info(f"Deleted File: {file}")
        log["Deleted"].append(file)
    if out_file:
        with open(out_file, 'w') as log_file:
            json.dump(log, log_file, indent=4)
if args.init:
    run_init(args.target, args.state)
elif args.check:
    run_check(args.target, args.state, args.log)

 