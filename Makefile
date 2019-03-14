INSTANCE_ID ?= main
APACHE_ENTRY_POINT ?= /

MO_FILES = $(addprefix c2cgeoform_project/locale/, fr/LC_MESSAGES/c2cgeoform_project.mo de/LC_MESSAGES/c2cgeoform_project.mo)

ifneq (,$(findstring CYGWIN, $(shell uname)))
PYTHON3 =
VENV_BIN = .build/venv/Scripts
PIP_UPGRADE = python.exe -m pip install --upgrade pip setuptools
else
PYTHON3 = -p python3
VENV_BIN = .build/venv/bin
PIP_UPGRADE = pip install --upgrade pip==9.0.1 setuptools==36.5.0
endif

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo
	@echo "Possible targets:"
	@echo
	@echo "- build                   Install c2cgeoform_project"
	@echo "- initdb                  (Re-)initialize the database"
	@echo "- serve                   Run the dev server"
	@echo "- check                   Check the code with flake8"
	@echo "- modwsgi                 Create files for Apache mod_wsgi"
	@echo "- test                    Run the unit tests"
	@echo "- dist                    Build a source distribution"
	@echo "- update-catalog          Update message catalog"
	@echo "- compile-catalog         Compile message catalog"
	@echo

.PHONY: build
build: \
		.build/requirements.timestamp \
		.build/node_modules.timestamp \
		compile-catalog

.PHONY: initdb
initdb: .build/requirements.timestamp
	$(VENV_BIN)/initialize_c2cgeoform_project_db development.ini

.PHONY: serve
serve: build
	$(VENV_BIN)/pserve --reload development.ini

.PHONY: check
check: flake8

.PHONY: flake8
flake8: .build/requirements-dev.timestamp
	$(VENV_BIN)/flake8 c2cgeoform_project

.PHONY: modwsgi
modwsgi: build .build/c2cgeoform_project.wsgi .build/apache.conf

.PHONY: test
test: build .build/requirements-dev.timestamp
	$(VENV_BIN)/pytest

.PHONY: update-catalog
update-catalog: .build/requirements.timestamp
	$(VENV_BIN)/pot-create -c lingua.cfg --keyword _ -o c2cgeoform_project/locale/c2cgeoform_project.pot \
	    c2cgeoform_project/models/ \
	    c2cgeoform_project/views/ \
	    c2cgeoform_project/templates/
	msgmerge --update c2cgeoform_project/locale/fr/LC_MESSAGES/c2cgeoform_project.po c2cgeoform_project/locale/c2cgeoform_project.pot
	msgmerge --update c2cgeoform_project/locale/de/LC_MESSAGES/c2cgeoform_project.po c2cgeoform_project/locale/c2cgeoform_project.pot

.PHONY: compile-catalog
compile-catalog: $(MO_FILES)

.PHONY: dist
dist: .build/venv.timestamp compile-catalog
	$(VENV_BIN)/python setup.py sdist

%.mo: %.po
	msgfmt $< --output-file=$@

.build/node_modules.timestamp: package.json
	npm install
	touch $@

.build/venv.timestamp:
	# Create a Python virtual environment.
	virtualenv $(PYTHON3) .build/venv
	# Upgrade packaging tools.
	$(VENV_BIN)/$(PIP_UPGRADE)
	touch $@

.build/requirements.timestamp: .build/venv.timestamp requirements.txt
	$(VENV_BIN)/pip install -r requirements.txt -e .

.build/requirements-dev.timestamp: .build/venv.timestamp requirements-dev.txt
	$(VENV_BIN)/pip install -r requirements-dev.txt > /dev/null 2>&1
	touch $@

.build/c2cgeoform_project.wsgi: c2cgeoform_project.wsgi
	sed 's#\[DIR\]#$(CURDIR)#' $< > $@
	chmod 755 $@

.build/apache.conf: apache.conf .build/venv.timestamp
	sed -e 's#\[WSGISCRIPT\]#$(abspath .build/c2cgeoform_project.wsgi)#' \
        -e 's#\[INSTANCE_ID\]#$(INSTANCE_ID)#' \
        -e 's#\[APACHE_ENTRY_POINT\]#$(APACHE_ENTRY_POINT)#' $< > $@

.PHONY: clean
clean:
	rm -f .build/venv/c2cgeoform_project.wsgi
	rm -f .build/apache.conf
	rm -f $(MO_FILES)

.PHONY: cleanall
cleanall:
	rm -rf .build
	rm -rf node_modules
