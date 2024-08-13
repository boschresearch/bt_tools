# Configuration file for the Sphinx documentation builder.

# -- Project information
project = 'bt_tools'
copyright = '2024, Robert Bosch GmbH'
author = 'Christian Henkel'

release = '0.1'
version = '0.1.0'

# -- General configuration
extensions = [
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
html_logo = 'logo.png'
html_extra_path = ['../../']
# this avoids copying the build directory recursively into itself 
# which not only sounds like a bad idea:
exclude_patterns = [
    'docs/build',
    'docs/source/_build',
    '__pycache__',
    '.git',
    '**/.mypy_cache',
    '**/.pytest_cache',
]
html_context = {
    "display_github": True,
    "github_user": "boschresearch",
    "github_repo": "bt_tools",
    "github_version": "main",
    "conf_py_path": "docs/source/",
}

# -- autodoc config
autodoc2_packages = [
    "../../btlib/src/btlib",
    "../../bt_view/src/bt_view",
    "../../bt_live/src/bt_live",
]
