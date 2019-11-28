#!/usr/bin/env bash
pytest --verbose --cov=api --cov-report term-missing --cov-report xml:test-reports/coverage.xml --junitxml=test-reports/junit.xml