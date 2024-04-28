#!/bin/bash

# Store the current working directory
HERE=$(pwd)
CUR_FILE_DIR=$(dirname $(realpath "$0"))

# Define variables

## package name
PACKAGE_NAME=flask-file-share
VERSION=0.1.1
DEB_VERSION_NUM=2
PACKAGE_FULL_NAME="$PACKAGE_NAME"_"$VERSION" #-"$DEB_VERSION_NUM"

echo "PACKAGE_FULL_NAME=$PACKAGE_FULL_NAME"

# copyright data
AUTHOR_FULLNAME="Hermann Agossou"
AUTHOR_EMAIL="agossouhermann7@gmail.com"
# UPSTREAM_NAME="flask-file-share"
# UPSTREAM_CONTACT="$AUTHOR_FULLNAME <$AUTHOR_EMAIL>"
# COPYRIGHT_YEARS="2022-2024"
# AUTHOR="$AUTHOR_FULLNAME <$AUTHOR_EMAIL>"
# LICENSE="BSD-3-Clause"
# UPSTREAM_URL="<https://flask-file-share.readthedocs.io>"

## python package dirs
MAIN_FOLDER=$(realpath "$CUR_FILE_DIR/../..")
SRC_FOLDER=$(realpath "$MAIN_FOLDER/src")
README_FILE=$(realpath "$MAIN_FOLDER/README.md")

## build dirs
BUILD_FOLDER=$(realpath "$CUR_FILE_DIR")
UTILS_FOLDER=$(realpath "$CUR_FILE_DIR/../utils")

echo "SRC_FOLDER=$SRC_FOLDER"
echo "BUILD_FOLDER=$BUILD_FOLDER"
echo "UTILS_FOLDER=$UTILS_FOLDER"

# Clean previous build artifacts
rm -rf "$BUILD_FOLDER/debian"
rm $(dirname $BUILD_FOLDER)/"$PACKAGE_FULL_NAME"*
rm -rf "$SRC_FOLDER/flask_file_share.egg-info"

# Change directory to the build directory
cd $BUILD_FOLDER

# Install required tools
# sudo apt install -y dh-make

# Create Debian package files
DEBFULLNAME="$AUTHOR_FULLNAME" dh_make --createorig --packagename "$PACKAGE_FULL_NAME" --packageclass p --yes --email $AUTHOR_EMAIL --copyright bsd

# Copy necessary files
cp $README_FILE "$BUILD_FOLDER/README.md"
# cp "$UTILS_FOLDER/changelog" "$BUILD_FOLDER/debian/changelog"
sed "s/<PKGNAME>/$PACKAGE_NAME/g" "$UTILS_FOLDER/control" > "$BUILD_FOLDER/debian/control" # Replace 'ffs' with 'flask-file-share'
sed "s/<PKGNAME>/$PACKAGE_NAME/g" "$UTILS_FOLDER/copyright" > "$BUILD_FOLDER/debian/copyright" # Replace 'ffs' with 'flask-file-share'

# # update copyright
# ## Temporarily store the updated content
# temp_file=$(mktemp)
# # Read the content of the copyright file
# while IFS= read -r line; do
#     # Replace Upstream-Name
#     if [[ $line == Upstream-Name:* ]]; then
#         echo "Upstream-Name: $UPSTREAM_NAME" >> "$temp_file"
#     # Replace Upstream-Contact
#     elif [[ $line == Upstream-Contact:* ]]; then
#         echo "Upstream-Contact: $UPSTREAM_CONTACT" >> "$temp_file"
#     # Replace Source
#     elif [[ $line == Source:* ]]; then
#         echo "Source: $UPSTREAM_URL" >> "$temp_file"
#     # Replace Copyright years and author
#     elif [[ $line == Copyright:* ]]; then
#         echo "Copyright: $COPYRIGHT_YEARS $AUTHOR" >> "$temp_file"
#     # Copy other lines as they are
#     else
#         echo "$line" >> "$temp_file"
#     fi
# done < "debian/copyright"
# # Replace the original file with the updated content
# mv "$temp_file" "debian/copyright"


# Build dependencies
# You may need to install additional dependencies here if needed
# sudo apt install -y debhelper dh-python python3-all python3-setuptools # on debian
# apt install build-essential:native dh-python python3-all # build on ubuntu

# Build the Debian package
dpkg-buildpackage -us -uc 
#--release-by="Hermann Agossou" --build-by="Hermann Agossou" #useless

# Change back to the original directory
cd "$HERE"
