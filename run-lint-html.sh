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

check_command "prettier" "npm install prettier --global" || return 1
prettier src/templates/*.html --write
