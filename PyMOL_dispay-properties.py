#! /usr/bin/env python

from pymol import cmd

def properties(cible):
 pos= cible + " and resn arg+lys+his"
 cmd.color("marine",pos)
 neg= cible + " and resn glu+asp"
 cmd.color("pink",neg)
 hydrophobes= cible + " and resn ala+gly+val+ile+leu+phe+met"
 cmd.color("yelloworange",hydrophobes)
 others= cible + " and not resn ala+gly+val+ile+leu+phe+met+arg+lys+his+glu+asp"
 cmd.color("white",others)
cmd.extend('properties',properties)

#set solvent_radius, 1
