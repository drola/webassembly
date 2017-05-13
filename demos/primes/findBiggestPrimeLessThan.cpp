#include <algorithm>
#include <iterator>
#include <vector>
#include "emscripten/bind.h"

int findBiggestPrimeLessThan(int N) {
  std::vector<char> isPrime(N+1);
  std::fill(std::begin(isPrime), std::end(isPrime), 1);
  isPrime[0] = 0;
  isPrime[1] = 0;

  int i, j;

  for(i = 2; i <= N; i++) {
    if (!isPrime[i]) {
      continue;
    }

    for(j = i + i; j <= N; j += i) {
      isPrime[j] = 0;
    }
  }

  for(i = N; i >= 0; i--) {
    if (isPrime[i]) {
      return i;
    }
  }

  return -1; //error
}

// This exposes the function to JavaScript.
// Documentation is available at
// https://kripken.github.io/emscripten-site/docs/porting/connecting_cpp_and_javascript/embind.html
EMSCRIPTEN_BINDINGS(my_module) {
    emscripten::function("findBiggestPrimeLessThan", &findBiggestPrimeLessThan);
}
