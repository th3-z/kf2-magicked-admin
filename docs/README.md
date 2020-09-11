# Documentation

Killing Floor 2 Magicked Administrator uses Sphinx to generate web and PDF documentation.

## Requirements

The Python reqiurements are installed with `pip3 install -r requirements.txt`.

The following packages are needed to build the PDF documentation, examples are for Ubuntu Xenial.

* texlive-latex-recommended
* texlive-fonts-recommended
* texlive-latex-extra
* latexmk 

## Building

### HTML

1. `make html`

An index page will be output in `_build/`.

### PDF

1. `make pdf`

A PDF file will be output in `_build/`.
