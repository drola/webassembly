#!/bin/bash

cd "$(dirname "$(realpath "$0")")";

if [ ! -d "./opencv" ]; then
	git clone --branch 3.2.0 --depth=1 --single-branch https://github.com/opencv/opencv
        cd opencv
	cd ..
fi
rm -rf ./build_wasm
mkdir build_wasm
python2.7 ./make.py

