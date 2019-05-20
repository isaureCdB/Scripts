#!/usr/bin/env seamless
import sys

ctx.lib_fwd_bwd = cell(("text", "code", "ipython"))
link(ctx.lib_fwd_bwd, ".", "lib_fwd_bwd.py")
reg = ctx.registrar.ipython
reg.register(ctx.lib_fwd_bwd)
tf = ctx.tf_fwd_bwd = transformer({
    "npz_file": {"pin": "input", "dtype": "str"},
    "scores_file": {"pin": "input", "dtype": "str"},
    "result": {"pin": "output", "dtype": "object"} #dict with energies,Z, z, interactions, Btot
})
ctx.code = cell(("text", "code", "python"))
link(ctx.code, ".", "cell-fwd-bwd.py")

ctx.code.connect(tf.code)
tf.npz_file.cell().set("UUU-5e5-5frags-3A.npz")
tf.scores_file.cell().set("UUU-5e5.score")
export(tf.npz_file)

reg.connect("map_npz", tf)
reg.connect("store_energies", tf)
reg.connect("fwd", tf)
reg.connect("bwd", tf)

ctx.lib_backtrack = cell(("text", "code", "ipython"))
link(ctx.lib_backtrack, ".", "lib_backtrack.py")
reg.register(ctx.lib_backtrack)

tf = ctx.tf_stochastic_backtrack = transformer({
    "num_samples": {"pin": "input", "dtype": "int"},
    "fwd_bwd_result": {"pin": "input", "dtype": "object"}, #dict with energies, Z, z, interactions, Btot
    "result": {"pin": "output", "dtype": "object"} #don't know yet
})
ctx.tf_fwd_bwd.result.cell().connect(tf.fwd_bwd_result)
ctx.code2 = cell(("text", "code", "python"))
link(ctx.code2, ".", "cell-stochastic-backtrack.py")
ctx.code2.connect(tf.code)

reg.connect("stochastic_backtrack", tf)
export(tf.num_samples)
ctx.num_samples.set(100)
edit(ctx.num_samples, "Number of samples")

tf = ctx.tf_print_bprob = transformer({
    "output_file": {"pin": "input", "dtype": "str"},
    "fwd_bwd_result": {"pin": "input", "dtype": "object"}, #dict with energies, Z, z, interactions, Btot
})
ctx.tf_fwd_bwd.result.cell().connect(tf.fwd_bwd_result)
ctx.code3 = cell(("text", "code", "python"))
link(ctx.code3, ".", "cell-print-bprob.py")
ctx.code3.connect(tf.code)
tf.output_file.set(tf.npz_file[:-5]+"-energies-z-interactions")

tf = ctx.tf_print_chains = transformer({
    "output_file": {"pin": "input", "dtype": "str"},
    "result": {"pin": "input", "dtype": "object"},
})
ctx.tf_stochastic_backtrack.result.cell().connect(ctx.tf_print_chains.result)
ctx.code4 = cell(("text", "code", "python"))
link(ctx.code4, ".", "cell-print_chains.py")
ctx.code4.connect(tf.code)
tf.output_file.set(tf.npz_file[:-5]+".chains")

'''
tf = ctx.show_cython = transformer({
    "html": {"pin": "output", "dtype": ("text", "html")},
})
reg.connect("cython_html", tf)
tf.code.cell().set("return cython_html")
from seamless.lib.gui.browser import browse
browse(tf.html.cell())
'''
