#!/bin/bash

poetry export -f requirements.txt --output ./docs/requirements.txt --without-hashes --with buildthedocs

poetry run sphinx-apidoc ./src/flask_file_share/ -o ./docs/source/flask_file_share/ -f -E --module-first

PYTHON_PATH="$(poetry env info --path)"
source "$PYTHON_PATH/bin/activate"

cd docs
rm -r build
make html
cd ..

deactivate
open docs/build/html/index.html
