PROJECT := invest_api
VERSION := $(shell git describe --tags `git rev-list --tags --max-count=1`)

VENV := .venv
export PATH := $(VENV)/bin:$(PATH)

REPORTS := .reports
COVERAGE := $(REPORTS)/coverage

SOURCES := $(PROJECT) gunicorn.config.py
TESTS := tests

IMAGE_NAME := $(PROJECT)

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(REPORTS)
	rm -rf $(VENV)

.venv:
	poetry install --no-root

.reports:
	mkdir $(REPORTS)

setup: .venv .reports
	poetry check

install: setup

update: setup
	poetry update

isort: setup
	isort -rc $(SOURCES) $(TESTS)

mypy: setup
	mypy $(SOURCES) $(TESTS)

pylint: setup
	pylint $(SOURCES) $(TESTS) > $(REPORTS)/pylint.txt

flake: setup
	flake8 $(SOURCES) $(TESTS)

bandit: setup
	bandit -f json -o $(REPORTS)/bandit.json -r $(SOURCES) $(TESTS) -s B101

test: setup
	pytest

cov: setup
	coverage run --source $(PROJECT) --module pytest
	coverage report
	coverage html -d $(COVERAGE)/html
	coverage xml -o $(COVERAGE)/cobertura.xml
	coverage erase
	cobertura-clover-transform $(COVERAGE)/cobertura.xml -o $(COVERAGE)/clover.xml

lint: isort mypy pylint flake bandit test

build: lint cov
	docker build . -t $(IMAGE_NAME) --pull

all: lint cov build

.DEFAULT_GOAL := all
