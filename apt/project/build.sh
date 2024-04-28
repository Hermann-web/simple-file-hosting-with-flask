
sudo apt install dh-make
rm -rf debian
rm ../ffs_*
dh_make --createorig -p ffs_0.1.1-2 -y
cp ../../README.md README.md
cp ../utils/* debian

mkdir .pybuild/cpython3_3.10_ffs/build/flask_file_share/static 

# for debian
# sudo apt install debhelper dh-python python3-all python3-setuptools

# for linux
# apt install build-essential:native dh-python python3-all

dpkg-buildpackage -us -uc
