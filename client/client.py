#!/usr/bin/env python

import argparse
import sys
import os
import json
import logging

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

try:
    from urllib.request import Request, urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import Request, urlopen
    from urlparse import urlparse
    from urllib import urlencode
    

# from documentation examples
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG) # TODO: from config
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)
    
class DefaultList(list):
    def __copy__(self):
        return []

def read_conffile(c):
    '''Read configuration file from path c and return dict
    with configuration
    '''

    config = configparser.ConfigParser()
    if not os.path.exists(c):
        log.error('Config file %s does not exists!' % c)
        sys.exit(1)
    try:
        config.read(c)
    except Exception as e:
        log.error('Cannot read configuration from file %s: %s' % (c, str(e)))
        sys.exit(2)
    url = config.get('main', 'server_url')
    log.debug('Server URL from config file %s: %s' % (c, url))
    return {'url': url}


def get_server_url():
    '''Fetches the server url from (in order):
    1 - ENVVAR
    2 - Local configuration file
    3 - Global configuration file
    4 - Autodiscover
    Returns string
    '''
    configuration_file = os.path.join(os.path.expanduser('~'), '.docit.conf')
    system_configuration_file = '/etc/docit.conf'
    if os.environ.get('DOCIT_SERVER', None):
        return os.environ['DOCIT_SERVER']
    elif os.path.exists(configuration_file):
        conf = read_conffile(configuration_file)
        return conf['url']
    elif os.path.exists(system_configuration_file):
        conf = read_conffile(systemc_configuration_file)
        return conf['url']
    return 'http://docit/api'
    
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
    
    url = get_server_url()
    headers = {'Content-type': 'application/json'}
    if args.dump:
        req = Request(url)
        res = urlopen(req)
        print(res.read().decode('utf-8'))
        return

    if args.list_tags:
        url = "{0}/tags".format(url)
        req = Request(url)
        res = urlopen(req)
        print(res.read().decode('utf-8'))
        return

    if not args.text:
        print('No text to send...')
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
    print("Sending to server... ")
    res = requests.post(url, data=snippet, headers=headers)
    print(res.status_code)

if __name__  == '__main__':
    run()






























