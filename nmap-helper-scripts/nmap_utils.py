import argparse
from utils.fileparsers.xmlparser import parse_xml, map_ports
from utils.owtf.owtf_api import addtarget


def init_args():
    '''Initializes argparser and returns the parser object'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file", required=True)
    parser.add_argument('--owtf', '-O', action="store_true", help="Feed all http/https interfaces found to OWTF")
    parser.add_argument('--services', nargs="*", help="Look for specific services. 'all' is supported",
                        )
    args = parser.parse_args()
    return args


def check_services(service_list):
    ''' Only allow supported services'''
    # Add to this as new service support is added.
    supported_services = ['http', 'ftp', 'ssh', 'sftp']
    for x in supported_services:
        if not service_list:
            return
        else:
            try:
                service_list.remove(x)
            except ValueError:
                pass

    if service_list:
        print "[*] Uh-oh! The following services are not supported yet : ", service_list


def main():
        args = init_args()
        if args.services:
            check_services(list(args.services))

        # Parse the XML and get useful info and a dict with port mappings.
        report = parse_xml(args.input)
        portmap = map_ports(report)
        # If the OWTF argument is set, map the ports and add found targets to OWTF.
        if args.owtf:
            addtarget(portmap)
        # If offensive flag is set, look for exploitable services.


if __name__ == '__main__':
    main()
