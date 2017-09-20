import argparse

parser = argparse.ArgumentParser(description='Graph embedding based music search.')

parser.add_argument('-i --input', dest='inputFolder', help='data input folder path', required=True)
parser.add_argument('-o --output', dest='outputFolder', help='data output folder path', required=True)
parser.add_argument('-u --userContext', dest='userContext', help='boolean flag to ', default=True)

args = parser.parse_args()

from pprint import pprint
pprint(args)
pprint(args.inputFolder)

