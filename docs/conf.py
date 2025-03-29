# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../pygression'))


project = 'pygression'
copyright = '2025, Arthur Nguyen'
author = 'Arthur Nguyen'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]
autoclass_content = "class"
autodoc_typehints = "description"
autodoc_default_options = {
    'members': True,
    'special-members': '__iadd__, __add__, __isub__, __sub__, __idiv__, __truediv__, __irshift__, __rshift__, __ilshift__, __lshift__, __eq__, __ne__',
    'undoc-members': False,  # Don't include members without docstrings
}


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']