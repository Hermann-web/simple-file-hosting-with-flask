#!/bin/bash

# Script to sort imports and format code using black for files in the winter_school directory

isort --profile black ./**/*.py  # Sort imports using isort with black profile
black ./**/*.py  # Format code using black
