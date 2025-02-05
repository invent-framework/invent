SHELL := /bin/bash

all:
	@echo "There's no default Makefile target right now. Try:"
	@echo ""
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make tidy - tidy up the code with the 'black' formatter."
	@echo "make lint - check the code for obvious errors with flake8."
	@echo "make lint-all - check all code for obvious errors with flake8."
	@echo "make serve - serve the project at: http://0.0.0.0:8000/"
	@echo "make widgets - generate the JSON definition of available widgets."
	@echo "make test - while serving the app, run the test suite in browser."
	@echo "make dist - build the module as a package."
	@echo "make publish-test - upload the package to the PyPI test instance."
	@echo "make publish-live - upload the package to the PyPI LIVE instance."
	@echo "make package - create an archive of the framework and test suite."

clean:
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf invent.tar.gz
	rm -rf test_suite.tar.gz
	rm -rf src/tools/builder/src/python/invent.tar.gz
	rm -rf static/*.tar.gz
	rm -rf test_suite
	find . | grep -E "(__pycache__)" | xargs rm -rf

tidy:
	black -l 79 examples src/invent tests utils

lint:
	flake8 --extend-ignore=E203,E701 src/invent

lint-all:
	flake8 --extend-ignore=E203,E701 src/invent tests/*

serve: clean tidy package
	python utils/serve.py

test:
	python -m webbrowser http://localhost:8000/index.html

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

package:
	tar --no-xattrs -czf invent.tar.gz \
		-C src invent toga_invent \
		-C toga/core/src toga \
		-C ../../travertino/src travertino
	mkdir test_suite
	cp -r src/invent test_suite
	cp -r tests test_suite
	cd test_suite && tar --no-xattrs -czf ../test_suite.tar.gz tests/* invent/*
	rm -rf test_suite
	cp invent.tar.gz static/
	cp invent.tar.gz src/tools/builder/public/python/
	cp test_suite.tar.gz static/
	rm invent.tar.gz
	rm test_suite.tar.gz
