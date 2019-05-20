#!/usr/bin/env python3
import sys, json

inp = json.load(open(sys.argv[1]))

outp = {}

def remove_empty(d_struct, k):
    out_k = {}
    for m in d_struct[k]:
        d_model = d_struct[k][m]
        if not isinstance(d_model, dict):
            if 'MSE' in d_model:
                d_model.remove('MSE')
            out_k[m] = d_model
            continue
        out_model = {}
        for c in d_model:
            d_chain = d_model[c]
            out_chain = {}
            for r in d_chain:
                if not isinstance(d_chain[r], dict):
                    out_chain[r] = d_chain[r]
                elif len(d_chain[r]) > 0:
                    out_chain[r] = d_chain[r]
            out_model[c] = out_chain
        out_k[m] = out_model
    return out_k

def rename_keys(d_struct, k):
    out_k = {}
    for m in d_struct[k]:
        d_model = d_struct[k][m]
        newm = "model_%s"%m
        if not isinstance(d_model, dict):
            if 'MSE' in d_model:
                d_model.remove('MSE')
            out_k[newm] = d_model
            continue
        else:
            out_model = {}
            for c in d_model:
                d_chain = d_model[c]
                out_chain = {}
                newc = "chain_%s"%c
                for r in d_chain:
                    newr = "res_%s"%r
                    if not isinstance(d_chain[r], dict):
                        out_chain[newr] = d_chain[r]
                    elif len(d_chain[r]) > 0:
                        out_chain[newr] = d_chain[r]
                out_model[newc] = out_chain
            out_k[newm] = out_model
    return out_k


for struct in inp:
    d_struct = inp[struct]
    out_struct = {}
    try:
        for k in d_struct:
            if not isinstance(d_struct[k], dict):
                out_struct[k] = d_struct[k]
                continue
            if 'model_1' in d_struct[k]:
                out_struct[k] = remove_empty(d_struct, k)
                continue
            if '1' not in d_struct[k]:
                out_struct[k] = d_struct[k]
                continue
            out_struct[k] = rename_keys(d_struct, k)
    except:
        print(k, d_struct[k], file=sys.stderr)
        raise
    outp[struct] = out_struct

json.dump(outp, sys.stdout)
