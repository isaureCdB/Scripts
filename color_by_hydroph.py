# Copyright (c) 2004 Robert L. Campbell
import colorsys,sys
from pymol import cmd

aa_1_3 = {
  'A': 'ALA', 
  'C': 'CYS', 
  'D': 'ASP', 
  'E': 'GLU', 
  'F': 'PHE', 
  'G': 'GLY', 
  'H': 'HIS', 
  'I': 'ILE', 
  'K': 'LYS', 
  'L': 'LEU', 
  'M': 'MET', 
  'N': 'ASN', 
  'P': 'PRO', 
  'Q': 'GLN', 
  'R': 'ARG', 
  'S': 'SER', 
  'T': 'THR', 
  'V': 'VAL', 
  'W': 'TRP', 
  'Y': 'TYR', 
}

aa_3_1 = {
  'ALA' : 'A', 
  'CYS' : 'C', 
  'ASP' : 'D', 
  'GLU' : 'E', 
  'PHE' : 'F', 
  'GLY' : 'G', 
  'HIS' : 'H', 
  'ILE' : 'I', 
  'LYS' : 'K', 
  'LEU' : 'L', 
  'MET' : 'M', 
  'ASN' : 'N', 
  'PRO' : 'P', 
  'GLN' : 'Q', 
  'ARG' : 'R', 
  'SER' : 'S', 
  'THR' : 'T', 
  'VAL' : 'V', 
  'TRP' : 'W', 
  'TYR' : 'Y', 
}

aa_types = {
  'A': 'hydrophobic',
  'D': 'hydrophilic',
  'E': 'hydrophilic',
  'F': 'hydrophobic',
  'I': 'hydrophobic',
  'K': 'hydrophilic',
  'L': 'hydrophobic',
  'M': 'hydrophobic',
  'N': 'hydrophilic',
  'Q': 'hydrophilic',
  'R': 'hydrophilic',
  'V': 'hydrophobic',
  'W': 'hydrophobic',
}


def color_by_hydroph(selection="all",
        hydrophobic='orange',
        hydrophilic='skyblue',     
        ):

  """
  usage: color_by_hydro <selection>, <optional overrides of default colors>
  e.g. color_by_hydro protein and chain A, hydrophobic=wheat

  Residue groups:               Default colours:
    hydrophobic: AILMVWF          orange
    hydrophilic: NQDEKR           skyblue
  """
  colors = {
    'hydrophobic': hydrophobic,
    'hydrophilic': hydrophilic,
  }

  for aa in aa_types:
    sel = selection + " and r. %s" % aa_1_3[aa]
#    print sel,"-->", colors[aa_types[aa]]
    cmd.color(colors[aa_types[aa]],sel)

cmd.extend("color_by_hydroph",color_by_hydroph)
