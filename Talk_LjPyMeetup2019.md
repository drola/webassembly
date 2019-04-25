Intro slide:
Hi, I'm Matjaž Drolc. I'm working on software for optimizing the maintenance of roads. We gather the data from measurements of road surfaces and do some magic to predict how the asphalt is going to perform in the future.
The data that we get is not perfect. To obtain good results we need a way to see what is happening. This is why we started using Python. Tools such as Pandas and Jupyter enable us to have fast feedback during development.
[show Jupyter notebook]

After the prototype is done, we need to make a product out of it. Algorithms from the prototype need to be deployed sometimes on servers and sometimes in the browser. This brings us into an awkward situation. The only way to run code in a browser was to use JavaScript. There exists a transpiler that converts Python code to JavaScript and there are at least two Python interpreters written in JavaScript.
However, due to the lack of Numpy and Pandas, those solutions don't really help us.

Another option is manually rewriting the Python prototypes to JavaScript. But that option is the worst of all. First and foremost, it's a waste of time. Probability of mistakes is high. Process of rewriting numpy and pandas code to JavaScript would entail finding some good library for JavaScript and currently, I am not aware of the existence of anything at that level. Even if something like that existed, one would need to know all the tiny details of both numpy and this non-existent JS library to accurately reimplement the code. To make matters worse, there are also differences between the languages themselves. Because both Python and JavaScript are dynamic languages, there are many hidden rules around type conversions that one has to be aware of.


However, things are changing.

The hell froze in 2017. Developers of Chrome, Edge, Firefox, and Safari started talking to each other after more than a decade of incompatible web browsers. They announced a thing called WebAssembly. WebAssembly is a new format for distributing program code as part of web applications.

[Open HelloWorld in WASM explorer https://mbebenita.github.io/WasmExplorer/]

WebAssembly is a low-level format. It's not designed to be written by hand. The idea is to use some kind of compiler, that produces WebAssembly binary and then run that program in a browser, similar to the way that JavaScript runs.
On the left, we see a C++ function that takes a list of numbers and sums them together. In the middle is that same function compiled to WebAssembly. This is what you distribute as part of your web application. On the right is what browser computes internally before actual execution. After a web browser downloads a WebAssembly file, it performs validation and all security checks and produces fast machine code.

The main point here is that we now have open doors to run whatever programming language we want in a web browser. We just need a compiler.
For C and C++ we have a suite of compiler and tools called Emscripten. It has existed for many years now and is quite stable. Rust compiler is also quite mature and people are also working on compilers for Go, Kotlin and .NET languages (C#, F#...).

Does anybody know which important piece of software is written in C?
It's the official Python interpreter - CPython.

Pyodide is a project that aims to bring the Python scientific stack to the web browser. So far they already ported Python interpreter, Numpy, Scipy, Pandas, matplotlib and other libraries. 

Both Jupyter and Pyodide look similar on the surface. Developer tools (F12) reveal the most significant difference.

Each time I execute some code in Jupyter, that code is sent to the server, executed there and the result is sent back to the browser.
With Pyodide there is no communication with the server. Everything, including Python interpreter, runs in the browser. And we are talking about official Python interpreter, built from the same source code, that you use elsewhere.

[Show demo with developer tools on the network tab and Jupyter]
[Show demo with developer tools on the network tab and Pyodide]

If you run Python interpreter in the web browser, you gain some superpowers. You can seamlessly interact with JavaScript. Converting data between Python and JavaScript is taken care of.
It is also possible to manipulate elements on a web page from Python.
Any global JS object can be imported from Python code. Here we import document which we can use to manipulate DOM elements. The document has exactly the same API that we are used to in JS.
Handling event is equally simple. In the example, we use a Python function as a callback for the click event.

We can get more advanced and combine several mouse events to produce a simple app for doodling.

We can flip things around and call Python code from JavaScript.

After Pyodide is loaded, it exposes an object called 'pyodide'.
API: https://github.com/iodide-project/pyodide/blob/master/docs/api_reference.md#javascript-api

With a call to pyodide.pyimport(name) we can access any Python object.  Here we first create a class called Foo and create an instance called foo. Then we request that object from JS side and read the 'val' attribute.

The reason I use Python are mostly its scientific libraries. Pyodide includes many packages, including Numpy, Pandas, SciPy and matplotlib.
Here is a tiny numpy example. First we calculate values of sine function and then we display those with matplotlib.
You can see a list of all ported packages on Github. 
https://github.com/iodide-project/pyodide/tree/master/packages

Let's summarize the benefits of running Python on the client side. First of all, hosting our application gets cheaper. Computation is happening on the client.
Another big win is related to security. In a scenario like Jupyter, the code we are running is not trusted. If we run it on a shared server, we need to isolate users from each other and also prevent doing damage to the server. Docker partially addresses this, but there are security holes or maybe wrong configuration, that can open doors to attackers.
On the other hand, web browsers take security very seriously. Whenever Google, Mozilla, Microsoft, and Apple talk about implementing new features, the main obstacle is how to do so in a way that protects users. We obviously don't want to give code from websites complete access to our devices. All WebAssembly code is running in a sandbox. Access to files, graphics card, camera, and the network is controlled in the same way as in JavaScript.

Performance is one of the main selling points of WebAssembly. 
[Video demo: https://d2jta7o2zej4pf.cloudfront.net/ ]
Here we can play with some video effects. The green chart shows us framerate for WebAssembly version and the blue one for JavaScript. The WebAssembly version has a much better frame rate than the JavaScript version.

And to make things crazy, they also ported WebM video codec to WebAssembly. There are no obstacles to making music or a video editor in a web browser.

We are also getting some new games. Unity and Unreal Engine both support WebAssembly. 
DEMO: https://s3.amazonaws.com/mozilla-games/ZenGarden/EpicZenGarden.html

There are still some open issues that will need to be solved in the future.
The Python demos that we looked at, downloaded 10s of MBs of files. This is because a web app needs to load Python interpreter and libraries before it can run them. Maybe the web will have a standard set of libraries packed together with browsers. But I don't expect this will happen soon, because it would be very hard to define any standard for that.
Another issue is performance. While WebAssembly is quite performant, there is still a performance penalty between 2 and 12-times compared to running Python interpreter directly on hardware.
And because of security, access to the network is very limited. We can use HTTP(S) and WebSockets, or in other words, exactly what we already had in JavaScript. It won't become possible to implement BitTorrent client in WebAssembly.
Another thing that doesn't work yet is multithreading. But the issue is temporary because browser vendors are preparing a standard that will solve this issue.

Other important WASM projects:
 - https://wasi.dev/ - WebAssembly System interface. Currently, the way that WebAssembly code communicates with the system around it is not standardized. People who write compilers created some ad-hoc solutions.  But WASI project is aiming to standardize this.
- https://wasmer.io/ is an universal WebAssembly runtime. They are trying to run WebAssembly outside of web browser. For example on servers.
- https://github.com/mohanson/pywasm is a WebAssembly interpreter written in pure Python. If you want to run your Python code in Python that runs in WebAssembly that runs in Python, you can.

I think the future will be interesting. In the near term, we will see better viewers of Jupyter notebooks and more web apps where we can play with data.
We might see improvements to Python documentation. The path is open to make it richer by embedding interactive code snippets.
We will also see the transition of software, that was traditionally running on the desktop, to the web. For example, software for video/audio editing, CAD, scientific computation...
