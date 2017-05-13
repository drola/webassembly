# Intro

## Me
Hello,
My name is Matjaz, I am working on road management software. This is a 3D viewer that shows scan of a road surface. We display those in browser, generate reports and stuff like that. When I heard of WebAssembly I was very interested because speed of calculations on the client side is very important for us. WebAssembly also makes in convenient to reuse existing C++ libraries in browser.

## WebAssembly basics
<blockquote>WebAssembly is a format suitable for compilation to the web.</blockquote>

It is like .exe, or whatever your device runs, that can run in browser. It is portable and runs in a sandbox, so it is secure. WebAssembly code runs in the same context as other JavaScript code, in the same thread. In fact it's possible to seamlessly call functions in WebAssembly from JavaScript and the other way around. WebAssembly is not a programming language. It's a binary format produced by a compiler. At the moment there exists a very good C++ compiler called Emscripten. There are also some game engines that support targeting WebAssembly, namely Unity engine and Unreal engine. This means we are about to see some very high quality games running in browsers. I hope you will be convinced how WebAssembly is awesome and fast by the end of this presentation.

This is a really impressive WebAssembly demo. It is a scene made with Unreal Engine 4. The same engine that was used to make the newest Unreal Tournament game. It's in the top league of game engines and now it can run in a web browser!  https://s3.amazonaws.com/mozilla-games/ZenGarden/EpicZenGarden.html

No plugins. No Flash, no Java. Just WebGL and WebAssembly. And if you are a game developer, making a portable game with engines such as Unity or Unreal Engine is really simple. You design your game and the engine is capable of producing version in WebAssembly, native, Android, Playstation and so on. And if you export your game in WebAssembly you have one binary that works on phones, tablets and PCs. And who knows, maybe someday even supercomputers.
In fact WebAssembly is not restricted to browser environments. In theory it is even possible to make a hardware chip that would run WebAssembly directly without additional software. There is an experimental project called Wasmachine. https://github.com/piranna/wasmachine The goal is to run WebAssembly directly on a chip. For development they use FPGAs which are chips where you can reprogram their logic. The author of that project is Jesus  In future and with enough money there could be processors that would just run WebAssembly instead of x86. The author of Wasmachine is Jesús Leganés-Combarro and he is presenting NodeOS in the next room at the moment.

## Usage scenarios
At the moment WebAssembly can be used in a couple of different ways. Maybe you have an existing application and you want to speed up a certain algorithm in it. WebAssembly might help in scenario like that. Or maybe you want to reuse existing C++ library. There are still tons of things that we don't do in Javascript just because of lack of libraries. Encryption is one such example. Only specialists implement encryption algorithms. Just a few weeks ago there was a conference called WebCamp in Ljubljana. There was also a presentation about security and the expert who was presenting said that you should never attempt to implement encryption algorithm yourself unless you have a couple of PhDs from math and computer science. Now that we have WebAssembly we don't have to reimplement them, we can just recompile libraries that already exist. Third use case for WebAssembly is making apps that are essentially just WebAssembly with minimal amounts of JavaScript. If you are making something that uses OpenGL and some computation the Emscripten compiler will generate needed .HTML and JavaScript for you. So you only touch C++ code, compile it and run that in browser.


# Deep dive
Now let's work through an example of using WebAssembly in our existing apps. Let's say you have a web application. It mostly runs OK but there is an algorithm that is just too slow in JavaScript. We want to try writing it in C++ and see if that helps.

This is our example app. It prints the biggest prime number that is smaller than N. For example if I type 10, the biggest prime number less or equal to 10 is 7.
The application uses an algorithm called Sieve of Erathostenes. It loops through all numbers from two to whichever we want. First we have two, we know it's a prime but we also know that all other even numbers are not primes so we cross them over. Then we go to number three. It's a prime, but six, nine, twelve and so on are not. And then we get to number four which was already crossed out. And so on until we check all primes until N. Then we print out the biggest one we found.

This is an implementation of the algorithm in JavaScript. The input is N and the output is the biggest prime less or equal than N. First we make an array with elements with indexes up until N. This means the array will have N+1 elements and we will just ignore the 0 at the beginning. It makes the code easier to read because we don't have any offsets. This is the outer loop that goes from two to N. If we know the number is not prime, we do nothing. If it is prime, we go to the inner loop and cross over all it's multiples.

This implementation will be fine for small numbers but for bigger ones C++ will give us some extra performance. Algorithms like that are ideal candidates for optimizing by rewriting them in C++.

To do that we need a compiler to produce WebAssembly from some programming language. We will use Emscripten to compile C++ code.  Emscripten is based on a suite of compiler components called LLVM. This means we are actually getting a very good and stable C++ compiler. LLVM has a long history and it supports new C++ features that were added in the last couple of years. Emscripten basically just adds support for generating WebAssembly output in addition to native machine code. It also ships with standard C++ library and implements some common multimedia APIs such as OpenGL and it does that just by calling WebGL. LLVM is not limited to C++, in fact there are LLVM-based compilers for other languages but I am not aware whether you can compile to WebAssembly from any of them.

You can see the procedure for installing Emscripten in this slide. At the moment we have to install Emscripten from `incoming` branch because Webassembly support hasn't been added to the stable version yet. The slides will be online. I alredy installed Emscripten on this computer to make sure nothing goes wrong.

The implementation in C++ is mostly the same. I just copy pasted the code, added types and changed how array is initialized. At the end I used emscripten bindings to expose my function so that it can be called from Javascript.

Exposing a function that takes a number and returns a number is really simple. Emscripten is able to figure out datatypes and conversions between C++ and Javascript. For classes and more complex structures you need to put in some more work but it's not too complicated. More information about exposing C++ APIs to JavaScript is available on Emscripten home page. https://kripken.github.io/emscripten-site/docs/porting/connecting_cpp_and_javascript/embind.html

Then we compile this code using emcc and we get .js and .wasm file. Generated JavaScript file will take care of loading the .wasm module and exposing all the functions and classes that you exposed to JavaScript.

We edit `index.html` by adding `<script>` tag that loads the generated Javascript file and replace call to Javascript implementation with C++ implementation.

This example is not really realistic but I think you get the idea. More realistic example is a video editor that implements effects using WebAssembly.

## Video editor

https://d2jta7o2zej4pf.cloudfront.net/

Here we have a selection of effects that we can apply to a video. And on the right side we see two charts. The blue one shows framerate if video is processed in Javascript and the green one shows framerate when we process video in C++ and ship that as a WebAssembly binary. Multimedia is really an extreme example where a lot of data has to be moved. It't really an ideal use case for technology such as WebAssembly. But WebAssembly is not only about performance. It might also be about saving battery. If some calculation is performed faster it means that processor has to run at full frequency for less time. And that will make users of mobile devices very happy.

Let's take a closer loop at WebAssembly format.  https://mbebenita.github.io/WasmExplorer/

```
int sum(int a, int b) {
  return a+b;
}
```

This is a tool called WasmExplorer. What we see is a function in C++ and then the same function compiled to WASM and x86 binary. We can see precisely that the compiler already figured out that we want to take two parameters and do 32-bit integer addition. If you imagine a similar function in JavaScript, the types of arguments can be anything and the JavaScript engine has to figure out what the plus sign actually means. It can be summation of numbers, it can be concatenation of strings or something invalid. And after it figures that out it also needs to decide whether any of the parameters need to be converted into another data type. Only after all these steps it can actually perform the operation. In contrast compiler does all those decisions up front in the WebAssembly case. Going from WebAssembly to native machine code is mostly glorified search and replace.

Another important consideration besides performance is security. Why is WebAssembly secure? There are a couple of reasons. First, WebAssembly has a limited set of instructions compared to native x86. It only supports numerical operations, branching and loops.
Second, functions calls are controlled. WebAssembly programs can only communicate with environment using imported and exported functions and a block of linear memory. WebAssembly code is loaded with a special JavaScript API and when we run WebAssembly program, we also need to specify table of functions that WebAssembly program can call. And because we are in JavaScript there is no way to put there anything else than what is already accessible there. WebAssembly programs cannot call anything that you can't call from JavaScript already and they are restricted by same cross origin policies and similar checks.
Another important property of WebAssembly is that linear memory for the data is separated from program code. This is important because it makes it harder to corrupt the program code itself if something goes wrong. In native x86 architecture program code and data is not separated. You can have bytes of data that were entered by the user or read from file and after that you can have binary instructions for some function that you call later. But if there is a bug in the program and the program reads input that is longer than the reserved space, It will overwrite its own instructions. This is called buffer overflow and it is one of the most common reasons for security issues with software. However, because data memory of a WebAssembly program is separated from the program itself, such problems should not occur.

# OpenCV demo
Now let's take a look at another more fun demo. Here we are taking live video from the Webcam on this laptop and performing face detection. For face detection I used a library called OpenCV. It's written in C++ and obviously I wouldn't want to rewrite it to JavaScript. Fortunately, because of WebAssembly, I can just compile it with Emscripten and use it in browser.

We are getting video from camera and then we send video frame to some C++ code that runs OpenCV algorithm for detecting faces. C++ returns coordinates of those faces and the eyes and we render them on a canvas. Computer vision code is running in a WebWorker to keep the browser responsive. WebWorker is some JavaScript code that takes care of passing data between computer vision algorithm in WebAssembly format and JavaScript that runs on the page. WebAssembly is produced by compiling OpenCV and a tiny C++ program that uses the library to do exactly what we need here and exposes those functions to JavaScript.

# Browser support, polyfilling
According to caniuse.com 52% of internet users can already run WebAssembly. It was developed in consensus between Chrome, Edge, Firefox and WebKit. This means that support is coming to all major browsers. For older browsers you can also compile to asm.js which should work on all browsers that have typed arrays.

# Conclusion


## Problems I faced
Before I conclude I will say a few words about problems I faced when experimenting with WebAssembly.
One of the problems was that I was expecting documentation at WebAssembly.org. But as it turns out as a developer you should mostly read documentation provided by your compiler, for example Emscripten. Which Emscripten I needed to figure out what various parameters mean. Example of an important parameter is `-s NO_EXIT_RUNTIME=1`. Normally, without this option, Emscripten will clean up everything after main() function in C++ code terminates. This is fine, if you wrote the whole application in C++ but it's bad if you are calling specific functions from JavaScript when you need them. That option will prevent cleaning up of memory and other important stuff after main() is done.

I've been also spending time on finding ways to efficiently transfer data between JavaScript and C++. These data transfers are very expensive when you are trying to transfer pixels at 60 frames per second. You want to do the least amount of copying as possible.

Another awkward subject when interfacing C++ and JavaScript are objects. JavaScript has a garbage collector that detects which objects cannot be accessed and deletes them automatically. However in C++ memory management is manual. You need to know which objects have to be manually deleted and when. Otherwise you either run out of memory or try to access an object that does not exist anymore.

In bigger applications that use Angular I found it convenient to wrap calls to WebAssembly inside a service. That way angular calls a function before service or a component is destroyed so I know exactly when I need to clean up WebAssembly stuff.

## Suggested path for learning all this
WebAssembly is an opportunity to learn new programming languages. I would say it's best to learn C++ first without WebAssembly and just learn how C++ programmers think and what tools they use and only add WebAssembly later. Limiting yourself like that is a good tactic to not get overwhelmed by all new stuff that you need to learn. Make sure the literature is up to date because a lot has changed in the last 6 years in the C++ land. There were lots of improvements to the language and the standard library.

## Planned WebAssembly features

WebAssembly as it is now is only a so called minimum viable product. It's a start but to make it really useful it still needs some work. Currently the browser vendors are working on multithreading and SIMD instructions.

### Threads
Browsers already have support for WebWorkers which is a way of multithreading but it is limited. Data between WebWorkers cannot be shared. It can be copied or moved but two WebWorkers cannot work on same piece of data at the same time. WebAssembly will have actual threads as they exist in other languages. This will offer great speed improvements, way beyond of what is available now. In optimistic benchmarks WebAssembly is 10, 20, 30 or so percent faster. Multithreading will speed up some algorithms 2, 4 or 8 times, depending on have many cores you have on your processor.

### SIMD instructions
Another important feature that is planned is support for SIMD instructions. Modern processors have special instructions that can execute same operation on multiple pieces of data. Let's imagine we have two three-dimensional vectors and we want to compute their SUM. How do you do that? First you take x components of both vectors and add them together. Then you do the same for Y and then you do the same for Z. But if you have access to SIMD instructions you can do all three in one step. Again this speeds up computations a lot. All algorithms involving graphics or sound or linear algebra have tons of computations like that. SIMD instructions mean we can again expect speed-ups of around 4-times for ideal case.

Both of these features mean that we will get around 16-times faster calculations. Of course this will only be valid for ideal algorithms. But surely it will be noticeable for the multimedia.


### More tooling, more compilers
Currently Emscripten is a very decent C++ compiler and there is a compiler for Rust as well. There was an experiment to bring languages from .NET ecosystem to WebAssembly but unfortunately that project doesn't seem to be active. I am hoping there will be more and more compilers after as time passes.

# Conclusion
Hopefully this talk will inspire you to try WebAssembly and get inspired by new possibilities. Although C++ can look frightening, it becomes fun when you know that you can control what you program does. It gives you kind of power that you don't get from languages such as JavaScript. You can control exactly when piece of memory is allocated and when something is deleted. You know exactly how many bytes you an instance of you class needs. You get to tweak your code and watch compiler's output and see when you get most done with least amount of processor instructions.

I invite you to hack and make better developer tools related to this technology. I just recently heard that developer tools in Firefox are actually a separate project on GitHub. It's a React application so any JavaScript developer can change it. And I am hoping someone will bring Go, Haskell and other cool languages to the web as well.

# Thank you
