# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Car Detection Mlops'
copyright = '2024, Pedro Altobelli'
author = 'Pedro Altobelli'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sys
import os

sys.path.insert(0, os.path.abspath("../src"))
sys.path.insert(0, os.path.abspath("../data"))
sys.path.insert(0, os.path.abspath("../deploy"))
sys.path.insert(0, os.path.abspath("../logs"))

extensions = [
    "sphinx.ext.autodoc",
    "myst_parser",
    "sphinx.ext.mathjax"
    ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ['_static']
