# Makefile

######################################

CMD := poetry run

PKG := revelation
TEST_PKG := tests

MAX_LINE_LENGTH := 79
COVERAGE_THRESHOLD := 85

IGNORE_ARGS:= --ignore=$(PKG)/static --ignore=htmlcov
COV_ARGS := --cov=$(PKG)
REPORT_ARGS := --cov-report html

######################################

.PHONY: all
all: full

.PHONY: checkflake8
checkflake8:
	$(CMD) flake8 .

.PHONY: checkruff
checkruff:
	$(CMD) ruff .

.PHONY: checkblack
checkblack:
	$(CMD) black --check --diff --color -l $(MAX_LINE_LENGTH) .

.PHONY: checkmypy
checkmypy:
	$(CMD) mypy .

.PHONY: check
check: | checkflake8 checkruff checkblack checkmypy

.PHONY: test
test:
	$(CMD) pytest $(IGNORE_ARGS) $(PKG) $(TEST_PKG)

.PHONY: covercli
covercli:
	$(CMD) pytest $(IGNORE_ARGS) $(COV_ARGS) --cov-fail-under=$(COVERAGE_THRESHOLD) $(PKG) $(TEST_PKG)

.PHONY: coverhtml
coverhtml:
	$(CMD) pytest $(IGNORE_ARGS) $(REPORT_ARGS) $(COV_ARGS) $(PKG) $(TEST_PKG)

.PHONY: coverserver
coverserver:
	$(CMD) python -m http.server -d htmlcov/ 8080

.PHONY: cover
cover: | coverhtml coverserver

.PHONY: formatruff
formatruff:
	$(CMD) ruff . --fix

.PHONY: formatblack
formatblack:
	$(CMD) black -l $(MAX_LINE_LENGTH) .

.PHONY: format
format: | formatruff formatblack

.PHONY: full
full: | format check test

.PHONY: fullcover
fullcover: | format check cover

.PHONY: clean
clean:
	rm -rf *.egg-info site dist build htmlcov .mypy_cache .pytest_cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '.coverage' -exec rm -f {} +
	find . -name '__pycache__' -exec rmdir {} +
