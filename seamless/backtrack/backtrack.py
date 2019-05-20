#!/usr/bin/env seamless
import sys

ctx.code.connect(tf.code)

ctx.lib_backtrack = cell(("text", "code", "ipython"))
link(ctx.lib_backtrack, ".", "lib_backtrack.py")
reg.register(ctx.lib_backtrack)
tf = ctx.tf_stochastic_backtrack = transformer({
    "num_samples": {"pin": "input", "dtype": "int"},
    "input_file": {"pin": "input", "dtype": "str"},
    "result": {"pin": "output", "dtype": "object"} #don't know yet
})
ctx.code = cell(("text", "code", "python"))
link(ctx.code, ".", "cell-stochastic-backtrack.py")
ctx.code.connect(tf.code)

export(tf.num_samples)
ctx.num_samples.set(10000)
edit(ctx.num_samples, "Number of samples")

tf.input_file.cell().set("UUU-5e5-5frags-3A-energies-z-interactions.npz")

reg.connect("stochastic_backtrack", tf)

tf = ctx.tf_print_chains = transformer({
    "output_file": {"pin": "input", "dtype": "str"},
    "result": {"pin": "input", "dtype": "object"},
})
ctx.tf_stochastic_backtrack.result.cell().connect(ctx.tf_print_chains.result)
ctx.code4 = cell(("text", "code", "python"))
link(ctx.code4, ".", "cell-print_chains.py")
ctx.code4.connect(tf.code)
tf.output_file.set("UUU-5e5-5frags-3A.chains")
