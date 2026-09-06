#!/usr/bin/env python3
import argparse
import socket
parser = argparse.ArgumentParser()
parser.add_argument("--IP","-i",help="helps with scanning a specific IP address",required=True)
parser.add_argument("--verbose","-v",help="Shows additional information",action='store_true')
parser.add_argument("--ports","-p",help="specifies the ports to scan, default is 1-7 65535",default="1-65535")
args = parser.parse_args()  

router = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
router