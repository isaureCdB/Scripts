#!/usr/bin/env python2

import sys, os
import numpy
from math import *
from multiprocessing import Pool, Queue
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
import rmsdlib

def read_pdb(pdb):
  atoms = []
  lines0 = open(pdb).readlines()
  lines = []
  extralines = []
  for l in lines0:
    if not l.startswith("ATOM"):
      extralines.append((len(lines), l))
      continue
    x = float(l[30:38])
    y = float(l[38:46])
    z = float(l[46:54])
    atoms.append((x,y,z))
    lines.append(l)
  return lines, numpy.array(atoms), extralines

def apply_matrix(atoms, pivot, rotmat, trans):
  ret = []
  for atom in atoms:
    a = atom-pivot
    atom2 = a.dot(rotmat) + pivot + trans
    ret.append(atom2)
  return ret

def write_pdb(outputfile, lines, atoms, extralines):
  print outputfile
  outp = open(outputfile, "w")
  count = 0
  pos = 0
  data = zip(lines, atoms)
  while 1:
    while pos < len(extralines):
      p,d = extralines[pos]
      if count < p: break
      print >> outp, d.rstrip("\n")
      pos += 1
    if count == len(data): break
    l,a = data[count]
    ll = l[:30] + "%8.3f%8.3f%8.3f" % (a[0],a[1],a[2]) + l[54:].rstrip("\n")
    print >> outp, ll
    count += 1
  outp.close()

import sys
import argparse
a = argparse.ArgumentParser(prog="fit-multi.py")
a.add_argument("reference")
a.add_argument("mobilelist")
a.add_argument("outputdir")
a.add_argument("--np",type=int)
a.add_argument("--rmsd", action="store_true")
a.add_argument("--iterative", action="store_true")
a.add_argument("--iterative_cycles",type=int,default=5)
a.add_argument("--iterative_cutoff",type=float,default=2)
args = a.parse_args()

#read atoms
lines1, atoms1_fit, extralines1 = read_pdb(args.reference)

mobiles = [l.strip().strip("\n") for l in open(args.mobilelist) if len(l.strip().strip("\n"))]
outputs = [args.outputdir + mobil.split("/")[-1] for mobil in mobiles]

def run(runarg):
  mobile, outputfile = runarg
  lines2, atoms2, extralines2 = read_pdb(mobile)
  atoms2_fit = atoms2
  assert len(atoms1_fit) and len(atoms1_fit) == len(atoms2_fit), (len(atoms1_fit), len(atoms2_fit))

  #perform a direct fit
  rotmat, offset, rmsd = rmsdlib.fit(atoms1_fit,atoms2_fit)
  if args.rmsd:
    print "%.3f" % rmsd
  else:
    pivot = numpy.sum(atoms2_fit,axis=0) / float(len(atoms2_fit))
    fitted_atoms = apply_matrix(atoms2, pivot, rotmat, offset)
    write_pdb(outputfile, lines2, fitted_atoms, extralines2)

if args.np == 1:
    result = [run((m,o)) for m,o in zip(mobiles, outputs)]
else:
    runargs = [(m,o) for m,o in zip(mobiles, outputs)]
    pool = Pool(args.np)
    try:
      result = pool.map(run, runargs)
    except KeyboardInterrupt:
      pool.terminate()
      sys.exit(1)
