#!/usr/bin/env python3

import os, sys

# def in_list(L, element):
#     for couple in L:
#         if element in couple:
#             return True
#     return False

def extract_chains(pdb_id):

    os.system('pdb_download_biological_assembly {}'.format(pdb_id))

    i = 1

    interaction_chains = {}
    while True:
        try:

            with open('{}.pdb{}'.format(pdb_id, i), 'r') as file:
                interaction_chains[i] = {"protein":[], "rna":[]}
                lines = file.readlines()
                for line in lines:
                    if line.startswith('ATOM'):
                        print(line[13:15])
                        if line[13:15] == "CA":
                            if line[21] not in interaction_chains[i]["protein"]:
                                interaction_chains[i]["protein"].append(line[21])
                        elif line[13:16] == "O2\'":
                            print(line[21])
                            if line[21] not in interaction_chains[i]["rna"]:
                                interaction_chains[i]["rna"].append(line[21])
            i += 1
        except:
            break

    return interaction_chains

extract_chains(sys.args[1])
