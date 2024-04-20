#!/bin/bash

MODULE_PATH="src/filemanager/"

poetry run isort $MODULE_PATH
poetry run yapf -r -i $MODULE_PATH
poetry run flake8 $MODULE_PATH
