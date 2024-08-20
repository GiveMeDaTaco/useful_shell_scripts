import os
import sys
sys.path.insert(0, os.path.abspath('../../tlptaco'))

# Project information
project = 'tlptaco'
author = 'Your Name'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        'searchbox.html',
    ]
}
