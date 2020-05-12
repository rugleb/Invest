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
	poetry env use 3.7
	poetry check

venv: .venv

.reports:
	mkdir -p $(REPORTS)

reports: .reports

setup: clean venv reports

install: .venv
	poetry install --no-root

update: venv
	poetry update

isort: venv reports
	isort -rc $(SOURCES) $(TESTS)

mypy: venv reports
	mypy $(SOURCES) $(TESTS)

pylint: venv reports
	pylint $(SOURCES) $(TESTS) > $(REPORTS)/pylint.txt

flake: venv reports
	flake8 $(SOURCES) $(TESTS)

bandit: venv reports
	bandit -f json -o $(REPORTS)/bandit.json -r $(SOURCES) $(TESTS) -s B101

test: venv reports
	pytest

cov: venv reports
	coverage run --source $(PROJECT) --module pytest
	coverage report
	coverage html -d $(COVERAGE)/html
	coverage xml -o $(COVERAGE)/cobertura.xml
	coverage erase
	cobertura-clover-transform $(COVERAGE)/cobertura.xml -o $(COVERAGE)/clover.xml

lint: isort mypy pylint flake bandit test

build: lint
	docker build . -t $(IMAGE_NAME) --pull

all: setup install lint cov build

.DEFAULT_GOAL := all
