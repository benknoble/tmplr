# This Makefile is compatible with GNU Make (not POSIX, due to shell and
# function call expansions). It provides convenience targets for developers and
# maintainers. Targets are documented where they live.

.SUFFIXES:

SHELL = /bin/sh

#  macros {{{
run_setup = $(V_PYTHON) $(SETUP)

py_module = $(1) -m $(2)
sys_py_module = $(call py_module,$(SYS_PYTHON3),$(1))
v_py_module = $(call py_module,$(V_PYTHON),$(1))

venv = $(call sys_py_module,venv)
pip = $(call v_py_module,pip)
twine = $(call v_py_module,twine)

bump_patch = $(AWK) -F. -v OFS='.' '{print $$1,$$2,$$3+1}'
bump_minor = $(AWK) -F. -v OFS='.' '{print $$1,$$2+1,0}'
bump_major = $(AWK) -F. -v OFS='.' '{print $$1+1,0,0}'
#  macros }}}

#  variables {{{
SED = sed
AWK = awk

SETUP = setup.py

VIRTUAL_ENV = .env
V_BIN = $(VIRTUAL_ENV)/bin

SYS_PYTHON3 = python3
V_PYTHON = $(V_BIN)/python
V_TWINE = $(V_BIN)/twine

DEV_REQS_FILE = dev-requirements.txt
DEV_REQS = $(V_TWINE)

TMPLR_VERSION = $(shell $(run_setup) --version)
TMPLR_FULLVERSION = $(shell $(run_setup) --fullname)

DIST = dist
TAR = $(DIST)/$(TMPLR_FULLVERSION).tar.gz
WHEEL = $(DIST)/$(TMPLR_FULLVERSION)-py3-none-any.whl
DIST_FILES = $(TAR) $(WHEEL)

BINARIES = tmplr temples
V_BINARIES = $(patsubst %,$(V_BIN)/%,$(BINARIES))
#  variables }}}

all: test

# get setup for development
develop: $(VIRTUAL_ENV) $(DEV_REQS) $(V_BINARIES)

# run the tests
test: $(VIRTUAL_ENV)
	$(run_setup) test

# for the maintainers: deploy to twine
deploy: test $(DIST_FILES)
	$(twine) check $(DIST_FILES)
	$(twine) upload $(DIST_FILES)

# clean up
clean:
	-rm -r $(DIST)
	-find -f tmplr tmplr_cli -iname '*pyc' -delete -print
	$(run_setup) clean -a

# really clean up
distclean: clean
	-rm -rf tmplr.egg-info/ $(VIRTUAL_ENV)

# for the maintainers: a full clean
maintainer-clean:
	$(warning This command is intended for maintainers to use;)
	$(warning it deletes files that may need special tools to rebuild.)
	-git clean -ffdx


patch minor major: FILE=tmplr/__init__.py
patch minor major: NEW_VERSION=$(shell echo $(TMPLR_VERSION) | $(bump_$@))

# for the maintainers: version bump
patch minor major:
	sed -e "/version/s/.*/__version__ = \"$(NEW_VERSION)\"/" $(FILE) > $(FILE).new
	mv $(FILE).new $(FILE)
	git add $(FILE)
	git commit -m 'Bump version'
	git tag v$(NEW_VERSION)

# run setup.py's check
check:
	$(run_setup) check --strict

$(DIST_FILES): test check

$(TAR):
	$(run_setup) sdist

$(WHEEL):
	$(run_setup) bdist_wheel


$(VIRTUAL_ENV):
	$(venv) $@

$(DEV_REQS):
	$(pip) install --requirement $(DEV_REQS_FILE)

$(V_BINARIES):
	$(run_setup) develop
