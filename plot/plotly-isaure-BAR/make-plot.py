import seamless
from seamless import context, cell
from seamless.lib.filelink import link
from seamless.lib.gui.browser import browser
from seamless.lib.templateer import templateer
from seamless.lib.gui.basic_editor import edit
from seamless.lib.gui.combobox import combobox
ctx = context()
ctx.links = context()
ctx.templates = context()
ctx.edit = context()
ctx.html = cell(("text", "html"))
ctx.links.html = link(ctx.html, "plotdata", "plotly.html")
ctx.browser = browser()
ctx.html.connect(ctx.browser.value)
ctx.templates.html_head_body = cell(("text", "html"))
ctx.links.template_html_head_body = link(
  ctx.templates.html_head_body,
  ".", "template-html-head-body.jinja"
)
ctx.params = context()
ctx.params.templateer_static = cell("cson")
ctx.links.params_templateer_static = link(ctx.params.templateer_static, ".", "params-templateer-static.cson")
params = {"environment": {"head": "text", "body": "text"}, "templates": ["head_body"]}
ctx.params.templateer_static.set(params)
ctx.templateer_static = templateer(ctx.params.templateer_static)
ctx.templateer_static.RESULT.connect(ctx.html)
ctx.temp_body = cell("text")
ctx.temp_head = cell("text")
#ctx.links.temp_head = link(ctx.temp_head, "temp", "head.txt")
#ctx.links.temp_body = link(ctx.temp_body, "temp", "body.txt")
ctx.temp_head.connect(ctx.templateer_static.head)
ctx.temp_body.connect(ctx.templateer_static.body)
ctx.templates.html_head_body.connect(ctx.templateer_static.head_body)
ctx.title = cell("text")
ctx.templates.head = cell("text")
ctx.links.template_head = link(ctx.templates.head, ".", "template-head.jinja")
ctx.temp_head.disconnect(ctx.templateer_static.head) ###
params =  {"environment": {"title": "text", "body": "text"},
            "templates": ["head", "head_body"],
            "result": "head_body"}
ctx.params.templateer_static.set(params)
del ctx.temp_head
#del ctx.links.temp_head
ctx.templates.head.connect(ctx.templateer_static.head)
ctx.title.connect(ctx.templateer_static.title)
ctx.links.title = link(ctx.title, "plotdata", "title.txt")

ctx.templates.body = cell("text")
ctx.links.template_body = link(ctx.templates.body, ".", "template-body.jinja")
params =  {"environment": {"title": "text",
                           "divname": "str",
                           "width": "int",
                           "height": "int",
                           "plotly_data": "json",
                           "layout": "json",
                           "config": "json",
                          },
            "templates": ["body", "head", "head_body"],
            "result": "head_body"}
ctx.temp_body.disconnect(ctx.templateer_static.body) ###
ctx.params.templateer_static.set(params)
ctx.divname = cell("str").set("plotlydiv")
ctx.divname.connect(ctx.templateer_static.divname)
ctx.templateer_static.width.cell().set(500)
ctx.templateer_static.height.cell().set(500)
ctx.plotly_data = cell("cson")
ctx.links.plotly_data = link(ctx.plotly_data, "plotdata", "plotly_data.cson")
ctx.plotly_layout = cell("cson")
ctx.links.plotly_layout = link(ctx.plotly_layout, "plotdata", "layout.cson")
ctx.plotly_config = cell("cson")
ctx.links.plotly_config = link(ctx.plotly_config, "plotdata", "config.cson")
ctx.plotly_data.connect(ctx.templateer_static.plotly_data)
ctx.plotly_config.connect(ctx.templateer_static.config)
ctx.plotly_layout.connect(ctx.templateer_static.layout)
ctx.templates.body.connect(ctx.templateer_static.body)

from seamless import transformer
ctx.integrate_data = transformer({
    "data": {"pin": "input", "dtype": "json"},
    "attrib": {"pin": "input", "dtype": "json"},
    "plotly_data": {"pin": "output", "dtype": "json"},
})
ctx.code = context()
ctx.code.integrate_data = cell(("text", "code","python"))
ctx.links.code_integrate_data = link(
    ctx.code.integrate_data, ".", "cell-integrate-data.py"
)
ctx.code.integrate_data.connect(ctx.integrate_data.code)
ctx.data = cell("json")
ctx.data.connect(ctx.integrate_data.data)
ctx.links.data = link(ctx.data, "plotdata", "data.json")
ctx.attrib = cell("cson")
ctx.attrib.connect(ctx.integrate_data.attrib)
ctx.links.attrib = link(ctx.attrib, "plotdata", "attrib.cson")
ctx.integrate_data.plotly_data.connect(ctx.plotly_data)

ctx.load_data_columns = transformer({
    "csv": {"pin": "input", "dtype": "text"},
    "point_shift": {"pin": "input", "dtype": "float"},
    "data": {"pin": "output", "dtype": "json"},
})
ctx.code.load_data_columns = cell(("text", "code","python"))
ctx.code.load_data_columns.connect(ctx.load_data_columns.code)
ctx.links.code_load_data_columns = link(
    ctx.code.load_data_columns, ".", "cell-load-data-columns.py"
)
ctx.csv = cell("text")
ctx.links.csv = link(ctx.csv, "plotdata", "data.csv")
ctx.csv.resource.mode = 3
ctx.csv.connect(ctx.load_data_columns.csv)
ctx.load_data_columns.data.connect(ctx.data)
#ctx.edit_point_shift = edit(ctx.load_data_columns.point_shift.cell())
ctx.load_data_columns.point_shift.cell().set(0.2)


ctx.html_dynamic = cell(("text", "html"))
ctx.links.html_dynamic = link(ctx.html_dynamic, "plotdata", "plotly_dynamic.html")
ctx.browser_dynamic = browser()
ctx.html_dynamic.connect(ctx.browser_dynamic.value)

ctx.params.templateer_dynamic = cell("cson")
params =  {"environment": {"title": "text",
                           "divname": "text",
                           "width": "int",
                           "height": "int",
                           "dynamic_html": ("text","html")
                          },
            "templates": ["body", "head", "head_body"],
            "result": "head_body"}
ctx.params.templateer_dynamic.set(params)
ctx.templateer_dynamic = templateer(ctx.params.templateer_dynamic)
ctx.templateer_dynamic.RESULT.connect(ctx.html_dynamic)
ctx.title.connect(ctx.templateer_dynamic.title)
ctx.divname.connect(ctx.templateer_dynamic.divname)
ctx.templateer_dynamic.width.cell().set(500)
ctx.templateer_dynamic.height.cell().set(500)
ctx.templates.head.connect(ctx.templateer_dynamic.head)
ctx.templates.body_dynamic = cell("text")
ctx.links.template_body_dynamic = link(
    ctx.templates.body_dynamic, ".", "template-body-dynamic.jinja"
)
ctx.templates.body_dynamic.connect(ctx.templateer_dynamic.body)
ctx.templates.html_head_body.connect(ctx.templateer_dynamic.head_body)

#print(ctx.templateer_dynamic.ed.editor._pending_inputs)

from seamless.lib.dynamic_html import dynamic_html
ctx.params.dynamic_html = cell("json")
dynamic_html_params = {
    "divname": {"type": "var", "dtype": "str"},
    "plotly_data": {"type": "var", "dtype": "json"},
    "config": {"type": "var", "dtype": "json"},
    "layout": {"type": "var", "dtype": "json"},
    "make_plot": {"type": "eval", "on_start": True},
}
ctx.params.dynamic_html.set(dynamic_html_params)
ctx.dynamic_html_maker = dynamic_html(ctx.params.dynamic_html)
ctx.dynamic_html_maker.dynamic_html.cell().connect(
    ctx.templateer_dynamic.dynamic_html
)
#ctx.divname.connect(ctx.dynamic_html_maker.divname) ###
ctx.plotly_data.connect(ctx.dynamic_html_maker.plotly_data)
ctx.plotly_config.connect(ctx.dynamic_html_maker.config)
ctx.plotly_layout.connect(ctx.dynamic_html_maker.layout)
ctx.dynamic_html_maker.make_plot.cell().set("""
Plotly.purge(divname);
Plotly.newPlot(divname, plotly_data, layout, config);
""")

dynamic_html_params = {
    "divname": {"type": "var", "dtype": "str"},
    "plotly_data": {"type": "var", "dtype": "json", "evals":["make_plot"]},
    "attrib": {"type": "var", "dtype": "json", "evals":["make_plot"]},
    "config": {"type": "var", "dtype": "json", "evals":["make_plot"]},
    "layout": {"type": "var", "dtype": "json", "evals":["make_plot"]},
    "make_plot": {"type": "eval", "on_start": True},
}
ctx.params.dynamic_html.set(dynamic_html_params)
ctx.attrib.connect(ctx.dynamic_html_maker.attrib)
ctx.divname.connect(ctx.dynamic_html_maker.divname) ###

if not seamless.ipython:
    seamless.run_work()
    import time
    time.sleep(1)
    seamless.run_work()


ctx.generate_attrib = transformer({
"csv": {"pin": "input", "dtype": "text"},
"attrib": {"pin": "output", "dtype": "json"}
})
ctx.code.generate_attrib = cell(("text", "code", "python"))
ctx.code.generate_attrib.connect(ctx.generate_attrib.code)
ctx.links.generate_attrib = link(ctx.code.generate_attrib, ".", "cell-generate-attrib.py")
ctx.csv.connect(ctx.generate_attrib.csv)
ctx.generate_attrib.attrib.connect(ctx.attrib)

ctx.tofile("plotly-dynamic.seamless", backup=False)
