#!/bin/bash

MODULE_PATH="src/filemanager/"

echo "-> running isort ..."
poetry run isort $MODULE_PATH

echo "-> running yapf ..."
poetry run yapf -r -i $MODULE_PATH

echo "-> running flake8 ..."
poetry run flake8 $MODULE_PATH
