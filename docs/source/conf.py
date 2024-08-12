# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'RTD Demo'
copyright = '2024, ct2034'
author = 'ct2034'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    
    'myst_parser',
    'autodoc2',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'networkx': ('https://networkx.org/documentation/stable/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- HTML Theming

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    'style_nav_header_background': '#ED6A5A'
}
html_static_path = ['_static']
html_logo = '_static/logo.png'

# -- Options for EPUB output
epub_show_urls = 'footnote'

autodoc2_packages = [
    "../../src/rtd_demo_pkg"
]
