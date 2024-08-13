# Configuration file for the Sphinx documentation builder.

# -- Project information
project = 'bt_tools'
copyright = '2024, Robert Bosch GmbH'
author = 'Christian Henkel'

release = '0.1'
version = '0.1.0'

# -- General configuration
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    
    # 'myst_parser',
    'autodoc2',
    'sphinx_mdinclude',
]
templates_path = ['_templates']

# -- HTML Theming
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    'style_nav_header_background': '#364C3B'  # Dark contrast to the logo
}
html_static_path = ['_static']
html_logo = 'logo.png'

# -- Options for EPUB output
epub_show_urls = 'footnote'

autodoc2_packages = [
    "../../btlib/src/btlib",
    "../../bt_view/src/bt_view",
    "../../bt_live/src/bt_live",
]
