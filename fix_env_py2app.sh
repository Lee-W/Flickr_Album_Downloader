#!/usr/bin/env bash

system=$(uname -a)
file_path="./env/lib/python*/site-packages/py2app/recipes/virtualenv.py"
if [[ $system == *"Linux"* ]]
then
    sed -i 's/mf.load_module/mf._load_module/g' "$file_path"
    sed -i 's/mf.scan_code/mf._scan_code/g' "$file_path"
else
    sed -i ''  's/mf.load_module/mf._load_module/g' "$file_path"
    sed -i ''  's/mf.scan_code/mf._scan_code/g' "$file_path"
fi
