extensions = ["sphinx_proof", "sphinx.ext.ifconfig"]
project = "Shared counter tests"
html_theme = "alabaster"
numfig_secnum_depth = 2
show_solutions = True
show_private = True


def setup(app):
    app.add_config_value("show_solutions", True, "env")
    app.add_config_value("show_private", True, "env")
