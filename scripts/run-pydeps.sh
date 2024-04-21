#!/bin/bash

# https://github.com/thebjorn/pydeps
poetry run pydeps --noshow ./src/flask_file_share  --cluster --rankdir LR --max-module-depth=2 -o ./docs/deps-d2.svg
poetry run pydeps --noshow ./src/flask_file_share  --cluster --rankdir LR --max-module-depth=3 -o ./docs/deps-d3.svg
