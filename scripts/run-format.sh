#!/bin/bash

# Function to check if a command is installed globally and provide installation instructions if it's not found
check_command() {
    local command_name=$1
    local install_command=$2

    if ! command -v "$command_name" &> /dev/null; then
        echo "$command_name is not installed."
        echo "To install $command_name, run: $install_command"
        return 1
    fi

    return 0
}

# Check if isort and black are installed globally
check_command "isort" "pip install isort" || return 1
check_command "black" "pip install black" || return 1

isort --profile black ./**/*.py  # Sort imports using isort with black profile
black ./**/*.py  # Format code using black
