SHELL := /bin/bash

all:
	@echo "There's no default Makefile target right now. Try:"
	@echo ""
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make tidy - tidy up the code with the 'black' formatter."
	@echo "make lint - check the code for obvious errors with flake8."
	@echo "make lint-all - check all code for obvious errors with flake8."
	@echo "make serve - serve the project at: http://0.0.0.0:8000/"
	@echo "make test - while serving the app, run the test suite in browser."
	@echo "make docs - use Sphinx to create project documentation."
	@echo "make dist - build the module as a package."
	@echo "make publish-test - upload the package to the PyPI test instance."
	@echo "make publish-live - upload the package to the PyPI LIVE instance."

clean:
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf docs/api/*
	rm -rf docs/_build
	find . | grep -E "(__pycache__)" | xargs rm -rf

tidy:
	black -l 79 src/pypercard
	black -l 79 tests
	black -l 79 examples
	black -l 79 docs

lint:
	flake8 src/pypercard/*

lint-all:
	flake8 src/pypercard/* tests/* examples/*

serve:
	python -m http.server

test:
	python -m webbrowser http://localhost:8000/tests.html

docs: clean
	$(MAKE) -C docs clean html
	@echo ""
	@echo "Documentation can be found here:"
	@echo file://`pwd`/docs/_build/html/index.html
	@echo ""

dist: clean lint
	@echo "Packaging module..."
	python -m pip install --upgrade build
	python -m build

publish-test: dist
	@echo "Packaging complete... Uploading to TEST instance of PyPi..."
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository test --sign dist/*

publish-live: dist
	@echo "Packaging complete... Uploading to LIVE instance of PyPi..."
	python3 -m pip install --upgrade twine
	python3 -m twine upload --sign dist/*
