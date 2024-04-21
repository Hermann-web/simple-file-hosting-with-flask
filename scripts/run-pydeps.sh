#!/bin/bash

# https://github.com/thebjorn/pydeps
pydeps  --noshow ./lissajou/  --cluster --rankdir LR -o ./docs/pydeps.svg
