#!/usr/bin/env python
import requests
import argparse
import sys
import os
import json

class DefaultList(list):
    def __copy__(self):
        return []
    
def run():
    parser = argparse.ArgumentParser(description='Store snippets of documentation')
    parser.add_argument('--dump','-d',
                        action='store_true',
                        help="Dump the content of db")
    parser.add_argument('--tag', '-t',
                        action='append',
                        default=DefaultList(['notag']),
                        help='Tags')
    parser.add_argument('--list-tags',
                        action='store_true',
                        help='List tags')
    parser.add_argument('text',
                        nargs='?',
                        help='The text (can be read as stdin)')
    args = parser.parse_args()
    
    url = 'http://localhost:5000/api'
    headers = {'Content-type': 'application/json'}
    
    if args.dump:
        res = requests.get(url, headers=headers)
        print res.text
        return

    if args.list_tags:
        print args.list_tags
        url = "{0}/tags".format(url)
        res = requests.get(url, headers=headers)
        print res.text
        return

    if not args.text:
        print 'No text to send...'
        sys.exit(1)

    # we can parse the stdin too!
    if not sys.stdin.isatty():
        args.text = sys.stdin.read()
    
    snippet = json.dumps({"value": args.text,
                          "tags": args.tag,
                          "user": os.getlogin(),
                          "path": os.getcwd(),
                          "hostname": os.uname()[1]
                          })
    print "Sending to server... "
    res = requests.post(url, data=snippet, headers=headers)
    print res.status_code

if __name__  == '__main__':
    run()
