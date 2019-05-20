import sys
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
from _read_struc import read_struc
'''
usage: select-dat-perrank.py <dat file> <rank cutoff> [--percent]
write the top-ranked poses (dat file) from an unsorted input.dat
'''
########################
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('dat')
parser.add_argument('rank', help="number of structures to select")
#parser.add_argument('--list', help="file containing the list of indices of structures to select")
#parser.add_argument('--index', help="indices of structure to select")
parser.add_argument('--percent', help="percentage of structures to select", action='store_true')
args = parser.parse_args()
########################

def check(l1, cutoff):
    for ll in l1:
        if ll.startswith("## Energy:"):
            ee = ll[10:].strip()
            if ee.startswith("nan") or float(ee) > cutoff :
                return False
    return True

header,structures = read_struc(args.dat)
rank = float(args.rank)

structures = list(structures)

scores = []
for l1,l2 in structures:
    for ll in l1:
        if ll.startswith("## Energy:"):
            ee = ll[10:].strip()
            if ee.startswith("nan"): ee = 10000
            scores.append(ee)

sorted_scores = sorted(scores)
if args.percent:
    rank = round(rank * len(sorted_scores)/100)
cutoff = sorted_scores[rank]

for l in header:
    print l

for l1,l2 in structures:
    if check(l1, cutoff):
        for l in l1 + l2:
            print l
