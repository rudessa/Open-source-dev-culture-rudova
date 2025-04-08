# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'open-source-development'
copyright = '2025, artem'
author = 'artem'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../TestingMocks/app/'))
sys.path.insert(0, os.path.abspath('../../TestingMocks/app/routes/'))
sys.path.insert(0, os.path.abspath('../../TestingMocks/'))
sys.path.insert(0, os.path.abspath('../../Alice_and_Fedor/item_keeper/'))

extensions = ['sphinx.ext.autodoc']
