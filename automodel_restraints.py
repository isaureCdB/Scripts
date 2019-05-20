import sys
# Addition of restraints to the default ones
from modeller import *
from modeller.automodel import *    # Load the automodel class

ali = sys.argv[1]
Nmodel = int(sys.argv[2])

class MyModel(automodel):
    def select_atoms(self):
        # Select residues 1 and 2 (PDB numbering)
        return selection(self.residue_range('14:', '15:'), self.residue_range('36:','40:'))

        # The same thing from chain A (required for multi-chain models):
        # return selection(self.residue_range('1:A', '2:A'))

        # Residues 4, 6, 10:
        # return selection(self.residues['4'], self.residues['6'],
        #                  self.residues['10'])

        # All residues except 1-5:
        # return selection(self) - selection(self.residue_range('1', '5'))


for l in open(ali).readlines():
    ll = l.split(':')
    if ll[0] == "sequence":
        model = ll[1]
    if ll[0] == "structure":
        template = ll[1]

print >> sys.stderr, template
print >> sys.stderr, model

log.verbose()
env = environ()

# Read in HETATM records from template PDBs
env.io.hetatm = True

env.io.atom_files_directory = ['.', '../atom_files']

a = automodel(env,
            alnfile  = ali,  # alignment filename
            knowns   = template,   # codes of the templates
            sequence = model,)   # code of the target

a.starting_model= 1                 # index of the first model
a.ending_model  = Nmodel             # index of the last model
                                    # (determines how many models to calculate)
a.make()                            # do homology modeling
