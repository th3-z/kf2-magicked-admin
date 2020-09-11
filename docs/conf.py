import sphinx_rtd_theme

project = 'Killing Floor 2 Magicked Admin'
copyright = '2020, th3-z'
author = 'th3-z'
release = '0.2.0'

extensions = [
    "sphinx_rtd_theme",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
