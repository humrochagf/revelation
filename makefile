# Makefile

######################################

ROOTDIR    := $(PWD)
PACKAGE    := "revelation"

######################################

.PHONY: lint
lint: # lint code
	flake8 .

.PHONY: test
test: # run tests
	nosetests tests

.PHONY: cover
cover: # coverage tests
	coverage run --source=$(PACKAGE) -m nose tests/
	coverage report -m

.PHONY: format
format:
	isort $(ROOTDIR)
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
