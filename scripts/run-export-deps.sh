#!/bin/bash

poetry export -f requirements.txt --output ./docs/requirements.txt --without-hashes --with buildthedocs
poetry export -f requirements.txt --output ./requirements.txt --without-hashes
