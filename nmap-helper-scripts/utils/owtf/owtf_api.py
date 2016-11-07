import json
from requests import session
from requests.exceptions import ConnectionError
from ConfigParser import RawConfigParser, NoSectionError


def _parse_config():
    config = RawConfigParser()
    config.read('owtf.config')
    port = config.get('owtf', 'port').strip('\'')
    host = config.get('owtf', 'host').strip('\'')
    return host or '127.0.0.1', port or 8009


def addtarget(portmap):
    '''Accepts a dict of format { hostname :[<list of ports>] }'''
    COUNT = 0
    urldata = dict()
    API_HOST, API_PORT = _parse_config()
    API_URL = "http://%s:%s/api/targets" % (API_HOST, API_PORT)
    for host, ports in portmap.items():
        for port, service in ports:
            if service == 'http':
                URL = "http://%s:%s" % (host, port)
            else:
                continue

            urldata['target_url'] = URL
            with session() as c:
                try:
                    response = c.post(API_URL, data=urldata)
                    if not response.text:
                        print "\n[*] Target %s was sucessfully added to OWTF" % URL
                        COUNT += 1
                    elif "Conflict" in response.text:
                        print "\n[*] Target %s already exists in OWTF" % URL
                    else:
                        print "\n[*] Error occured while adding targets"
                except ConnectionError:
                    print "\n[!] ERROR : Please check values in owtf.config (or, is OWTF running?)"
                    exit(1)
    if COUNT:
        print "\n[*] %d targets were successfully added to OWTF :)" % COUNT
    else:
        print "\n[*] No new targets were added to OWTF. Keep hacking :)"
