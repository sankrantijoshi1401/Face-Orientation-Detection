The code is used for detecting and fixing orientation of an image. Instead of having a seperate model and API for detection of orientation and fixing of the prientation, I have combined the two in one class. The code currently takes in file names. This can be edited to take in stream of files. The system uses OpenCv built in detector for extracting facial features.

The file using dlib, opencv and imutils libraries. 

To install the same, it would be easier if numpy, scipy, matplotlib, scikit-image are already present. Due to the absence of a valid library for Python 3 in MacOs, I am using python 2.7
