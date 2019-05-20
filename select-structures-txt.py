#!/usr/bin/env python3
import sys
structures = open(sys.argv[1])
selstruc = {}
if sys.argv[2] == "-f":
  selected = [int(l.split()[0]) for l in open(sys.argv[3]).readlines()]
else:
  selected = [int(v) for v in sys.argv[2:]]
selected_set = set(selected)

header = True
selected = False
i = 1
for l in structures:
    if l[:2] == "#1":
        header = False
    if header:
        print(l[:-1]),
    if len(l.split()) == 1:
        if int(l[1:]) in selected_set:
            selected = True
            print("#%i"%i),
            i+=1
        else:
            selected = False
        continue
    if selected:
        print(l[:-1]),
