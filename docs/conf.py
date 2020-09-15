import sphinx_rtd_theme


def replace_tokens(app, docname, source):
    result = source[0]
    for key in app.config.tokens:
        result = result.replace(key, app.config.tokens[key])
    source[0] = result


def setup(app):
    app.add_config_value('tokens', {}, True)
    app.connect('source-read', replace_tokens)


tokens = {
    "{ma_ver}": "0.2.0",
    "{ap_ver}": "0.0.2",
}

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
html_favicon = 'img/kf2-ma.png'

html_css_files = [
    'css/custom.css',
]
