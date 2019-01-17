# Python MAT

The Emotion Viewer project is a branch of my original work, which focuses on emotion / facial expression detecting using machine learning.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Will need to be installed in this order:

* [Python 3](https://www.python.org/download/releases/3.0/) - Python x64 interpreter
* [Boost](https://www.boost.org/) - Boost C++ Libraries*
* [Dlib](https://github.com/davisking/dlib) - Machine Vision / AI Library*
* [TensorFlow GPU](https://www.tensorflow.org/install/gpu) - Deep learning and neural network framework

Follow instructions from each third party to install the prerequisites.

* Compile the boost libraries with Python bindings.
* Compile Dlib with CUDA (A Nvidia GPU is required for compiling CUDA with Dlib, it is possible to use without CUDA but it requires a code change.)

### Running the program

Once all the above prerequisites are installed, navigate to the root folder of the application, then start the tornado server.


```
python server.py
```

Then on your browser address bar enter:

```
localhost:8888
```

## License

This project is copyright of Michael Healy @ Cork Institute of Technology.

