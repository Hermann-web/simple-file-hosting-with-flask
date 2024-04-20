#!/bin/bash

MODULE_PATH="src/flask_file_share/"

echo "-> running isort ..."
poetry run isort $MODULE_PATH

echo "-> running yapf ..."
poetry run yapf -r -i $MODULE_PATH

echo "-> running flake8 ..."
poetry run flake8 $MODULE_PATH

echo "-> running mypy ..."
poetry run mypy $MODULE_PATH
