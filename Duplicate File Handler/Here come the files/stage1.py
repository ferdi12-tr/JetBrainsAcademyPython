import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("directory", nargs='?')
args = parser.parse_args()
directory_ = args.directory

if directory_ is None:
    print("Directory is not specified")
else:
    for (root, dirs, filenames) in os.walk(directory_):
        for names in filenames:
            print(os.path.join(root, names))
