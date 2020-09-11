SPHINX_DIR = .
SPHINX_BUILD = sphinx-build
SPHINX_BUILDDIR = _build

all: html

clean:
	rm -rf ./$(SPHINX_BUILDDIR)

html: clean
	$(SPHINX_BUILD) -b html . ./$(SPHINX_BUILDDIR)

pdf: clean
	$(SPHINX_BUILD) -b latex . ./$(SPHINX_BUILDDIR)
	make -C $(SPHINX_BUILDDIR) all-pdf

.PHONY: html pdf clean

