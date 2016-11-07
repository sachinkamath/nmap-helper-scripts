import argparse
from utils.fileparsers.xmlparser import parse_xml, map_ports
from utils.owtf.owtf_api import addtarget


def init_args():
    '''Initializes argparser and returns the parser object'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file", required=True)
    parser.add_argument('--owtf', '-O', action="store_true", help="Feed all http/https interfaces found to OWTF")
    parser.add_argument('--offensive', action="store_true", help="Launch in offensive mode")
    args = parser.parse_args()
    return args


def main():
        args = init_args()
        # Parse the XML and get useful info.
        report = parse_xml(args.input)

        # If the OWTF argument is set, map the ports and add found targets to OWTF.
        if args.owtf:
            portmap = map_ports(report)
            addtarget(portmap)

        # If offensive flag is set, look for exploitable services.
        #if args.offensive:


if __name__ == '__main__':
    main()
