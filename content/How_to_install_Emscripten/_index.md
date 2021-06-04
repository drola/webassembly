+++
title = "How to install Emscripten"
+++


```
#!/bin/bash

# Install git cmake build-essential python2.7 nodejs default-jre
sudo apt-get install git cmake build-essential python2.7 nodejs default-jre
wget https://s3.amazonaws.com/mozilla-games/emscripten/releases/emsdk-portable.tar.gz
tar -zxvf emsdk-portable.tar.gz
cd ./emsdk-portable
./emsdk update
./emsdk install sdk-incoming-64bit #If you are getting "collect2: error: ld returned 1 exit status" error, try running ./emsdk install -j1 sdk-incoming-64bit
./emsdk activate sdk-incoming-64bit
cd emcscripten/incoming
./embuilder.py build binaryen
cd ../..
source ./emsdk_env.sh
```
