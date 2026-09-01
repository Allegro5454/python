#!/usr/bin/env python3
import hashlib
import argparse
import sys
import os
import json
import shutil
import datetime
import logging
logging.basicConfig(level=logging.info)
from pathlib import Path
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("--From", required=True, help="Path to input directory" )
parser.add_argument("--To", required=True, help="Path to output directory")
parser.add_argument("--verbose","-v",help="Shows additional information",action='store_true')
group.add_argument("--log","-l",help="Saves information to a file")
group.add_argument("--dryrun","-d",help="Let's you see what files will be moved, removed and unchanged")
args = parser.parse_args()
verbosity = args.verbose
date = datetime.datetime.now()
log_location = args.log
log_dest = f"sync_{date.isoformat()}"
log_full = f"{log_location}/{log_dest}"
desta = Path(args.From)
destb = Path(args.To)
hash_pointa = { }
hash_pointb = { }

def exist_check(pointa, pointb):
    if not pointa.exists():
        logging.critical("Source directory/file does not exist")
        sys.exit(1)
    if not pointb.exists() or not pointb.is_dir():
        logging.critical("Destination directory does not exist")
        sys.exit(1)
    else:
        logging.info("Directories exist. Ready for synchronization")
    
def hash_check_file(pointa, pointb):
    if pointa.is_file():
        position_path = pointa.relative_to(desta)
        with open(pointa, "rb") as f:
            digest = hashlib.file_digest(f, "sha256")
        hash_pointa[str(position_path)]=digest.hexdigest()
    for i in pointb.iterdir():
            if i.is_file() and not i.is_symlink():
                position_path = i.relative_to(destb)
                with open(i, "rb") as f:
                    digest = hashlib.file_digest(f, "sha256")
                hash_pointb[str(position_path)]=digest.hexdigest()
            elif i.is_dir():
                 hash_check_dir_b(i)
    if pointa.is_dir():
        for i in pointa.iterdir():
            if i.is_file() and not i.is_symlink() and not i.is_dir():
                position_path = i.relative_to(desta)
                with open(i, "rb") as f:
                    digest = hashlib.file_digest(f, "sha256")
                hash_pointa[str(position_path)]=digest.hexdigest()
            elif i.is_dir():
                hash_check_dir(i)


def hash_check_dir(dir):
    for i in dir.iterdir():
        if i.is_file() and not i.is_symlink() and not i.is_dir():
                position_path = i.relative_to(desta)
                with open(i, "rb") as f:
                    digest = hashlib.file_digest(f, "sha256")
                hash_pointa[str(position_path)]=digest.hexdigest()
        elif i.is_dir():
            hash_check_dir(i)

def hash_check_dir_b(dir):
    for i in dir.iterdir():
            if i.is_file() and not i.is_symlink() and not i.is_dir():
                    position_path = i.relative_to(destb) 
                    with open(i, "rb") as f:
                        digest = hashlib.file_digest(f, "sha256")
                    hash_pointb[str(position_path)]=digest.hexdigest()
            elif i.is_dir():
                hash_check_dir_b(i)
def equal_check():
    from_keys = set(hash_pointa.keys())
    to_keys = set(hash_pointb.keys())    
    new_files = from_keys - to_keys
    deleted_files = to_keys - from_keys 
    combined_keys = from_keys.intersection(to_keys)
    unchanged = len(combined_keys)
    moved = len(new_files)
    removed = len(deleted_files)
    if args.dryrun is None:
        sync(new_files, deleted_files, combined_keys, unchanged, removed, moved)
    else:
        dry_run_test(new_files, deleted_files, combined_keys, unchanged, removed, moved)
def sync(new_files, del_files, unchanged_files, unchanged, removed, moved):
    
    log = {
        "Date": date.isoformat(),
        "Removed": [],
        "Moved": [],
        "Unchanged": []
        }
    for i in new_files:
        file = desta/i
        if log_location is not None:
            log["Moved"].append(str(file))
        file = Path(file)
        tmp = destb/i
        tmp = Path(tmp)
        try:
            if tmp.parent.is_dir():
                shutil.copy2(file, tmp)
            else:
                os.makedirs(tmp.parent, exist_ok=True)
                shutil.copy2(file, tmp)
            if verbosity is not None:
                print("file copied:", file)
        except PermissionError:
            logging.critical("Permision Denied", file)
    for i in del_files:
        file = destb/i
        if log_location is not None:
            log["Removed"].append(str(file))    
        file = Path(file)
        if file.exists():
            try:
                os.remove(file)
            except PermissionError:
                logging.critical("Permision denied", file)
        if verbosity is not None:
            print("file removed:", file)
    print("No changes were made to:", unchanged, "files")
    print("Files moved:", moved, "files")
    print("Files removed", removed, "files")
    if log_location is not None:
        for i in unchanged_files:
            file = destb/i
            log["Unchanged"].append(str(file))
    if log_location is not None:
        with open(log_full, 'w') as log_file:
          json.dump(log, log_file, indent=4)

def dry_run_test(new_files, del_files, unchanged, removed, moved):
    print("Dry run no changes have been made")
    for i in new_files:
        file = desta/i
        file = Path(file)
        tmp = destb/i
        tmp = Path(tmp)
        if not tmp.parent.is_dir():
            print("Would create a directory", tmp.parent)
        if verbosity is not None:
            print("Would copy:", file, "to", tmp)
    for i in del_files:
        file = destb/i    
        file = Path(file)
        if verbosity is not None:
            print("Would remove:", file)
    print("No changes were made to:", unchanged, "files")
    print("Files moved:", moved, "files")
    print("Files removed", removed, "files")
    print("Dry run no changes have been made")
exist_check(desta, destb)
hash_check_file(desta, destb)
equal_check()
