# Makefile

######################################

ROOTDIR    := $(PWD)
PACKAGE    := "revelation"

######################################

.PHONY: install
install: # system-wide standard python installation
	pip install .

.PHONY: install.hack
install.hack: # install development requirements
	pip install -r requirements.txt
	pip install -e .[test]

.PHONY: build
build: # build package for distribuition
	rm -rf dist
	python setup.py sdist
	python setup.py bdist_wheel --universal

.PHONY: publish
publish: # publish package to the pypi
	twine upload dist/*

.PHONY: lint
lint: # lint code
	flake8 .

.PHONY: test
test: # run tests
	nosetests tests

.PHONY: cover
cover: # coverage tests
	nosetests -w tests --with-coverage --cover-package=$(PACKAGE)

.PHONY: format
format:
	isort $(ROOTDIR) --recursive --apply
	black -l 79 .

.PHONY: clean
clean: # remove temporary files and artifacts
	rm -rf site/
	rm -rf *.egg-info dist build
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '.coverage' -exec rm -f {} +
	find . -name '__pycache__' -exec rmdir {} +
