#!/bin/bash

set -v


emcc -O3 --llvm-lto 1 `#Highest optimization level` \
  -s ALLOW_MEMORY_GROWTH=1 `#Allow memory growth from default 16MB if needed` \
  -s USE_CLOSURE_COMPILER=1 `#Use closure compiler to reduce size of .js file` \
  -s EXPORTED_RUNTIME_METHODS=[] `#Don't export any runtime methods` \
  -s WASM=1 `#Generate WebAssembly` \
  -s MODULARIZE=1 `#Wrap in module` \
  -s NO_EXIT_RUNTIME=1 `#Don't destroy runtime after main() finishes` \
  -s EXPORT_NAME="'myWasmLibrary'" `#Export as 'myWasmLibrary'` \
  -std=c++11 `#Use C++11 standard` \
  --bind `#Generate bindings` \
  -o wasm.js `#Output to wasm.js` \
  findBiggestPrimeLessThan.cpp #Input file(s)
