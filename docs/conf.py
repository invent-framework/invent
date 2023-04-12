# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyperCard"
copyright = "2023, Anaconda Inc."
author = "Nicholas H.Tollervey"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "autodoc2",
    "sphinx.ext.viewcode",
]

autodoc2_packages = [{"path": "../src/pypercard", "module": "pypercard"}]
autodoc2_output_dir = "api"
autodoc2_render_plugin = "myst"
autodoc2_no_index = True
autodoc2_index_template = None

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = [
    ".rst",
    ".md",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

html_logo = "logo.png"
html_theme_options = {
    "description": "A HyperCard inspired GUI framework for beginners.",
    "logo_name": True,
    "logo_text_align": "center",
    "github_user": "pyscript",
    "github_repo": "pypercard",
    "page_width": "1200px",
}

html_sidebars = {
    "**": [
        "about.html",
        "searchbox.html",
        "navigation.html",
    ]
}
