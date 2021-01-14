# Makefile

######################################

PACKAGE := "revelation"

######################################

.PHONY: typecheck
typecheck: # type check code
	poetry run mypy .

.PHONY: lint
lint: # lint code
	poetry run flake8 .

.PHONY: test
test: # run tests
	poetry run pytest tests

.PHONY: cover
cover: # coverage tests
	poetry run pytest --cov=$(PACKAGE) tests/

.PHONY: format
format:
	poetry run isort .
	poetry run black .

.PHONY: clean
clean: # remove temporary files and artifacts
	rm -rf site/
	rm -rf *.egg-info dist build
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '.coverage' -exec rm -f {} +
	find . -name '__pycache__' -exec rmdir {} +
