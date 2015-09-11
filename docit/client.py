#!/usr/bin/env python
import requests
import argparse
import sys
import os
import json

def run():
    parser = argparse.ArgumentParser(description='Store snippets of documentation')
    parser.add_argument('--dump','-d',
                        action='store_true',
                        help="Dump the content of db")
    parser.add_argument('--tag', '-t',
                        action='append',
                        help='Tags')
    parser.add_argument('text',
                        nargs='?',
                        help='The text (can be read as stdin)')
    args = parser.parse_args()
    if not sys.stdin.isatty():
        args.text = sys.stdin.read()
    url = 'http://localhost:5000/api'
    headers = {'Content-type': 'application/json'}
    if args.dump:
        res = requests.get(url, headers=headers)
        print res.text
        return
    data = json.dumps({"data": args.text,
                       "tags": args.tag,
                       "user": os.getlogin(),
                       "path": os.getcwd(),
                       "hostname": os.uname()[1]
                       })
    print "Sending to server... "
    res = requests.post(url, data=data, headers=headers)
    print res.status_code

if __name__ == '__main__':
    run()
