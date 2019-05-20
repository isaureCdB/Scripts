#!/usr/bin/env python3
import json, sys, os, argparse
from collections import OrderedDict

'''
Give the n first rows of a json file as a new json file.
Input : - the number of rows n (int)
        - the json file (name.json)
Output : - a new json file (name_nrows.json)
'''

parser = argparse.ArgumentParser(description=__doc__,
                          formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--top", type=int, help="the number of entries you want (int)")
parser.add_argument("--entries", type=str, help="entries you want (int)", nargs='+')
parser.add_argument("file", type=str, help="the file you want to cut")
parser.add_argument("outp", type=str)
args = parser.parse_args()

# Put input in variable names
json_file=args.file

# Open the json file
js = json.load(open(json_file))

if args.top:
    n = args.top
    # Sort names of PDB files
    n_js = {}
    kk = sorted(js.keys())
    n_js = kk[:n]

elif args.entries:
    n_js = args.entries

js_dict = {}
# For elements kept, sort different parts
for element in n_js:
    print(element)
    js_dict[element] = js[element]
    #js_dict[element] = OrderedDict(sorted(js[element].items(), key=lambda t: t[0]))

# Write the new file
with open(args.outp, 'w') as outfile:
    json.dump(js_dict, outfile, indent = 2, sort_keys = True)
