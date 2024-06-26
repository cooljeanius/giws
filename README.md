GIWS
====

Description
-----------

GIWS is basically the opposite of SWIG.

When SWIG generates wrappers to call C/C++ functions/methods from other 
languages, GIWS creates wrapper for those who wants to call Java methods 
from C/C++.

GIWS is widely used in Scilab (from version 5.0) to drive the rendering and 
the GUI.

Documentation
-------------

The best way to understand how to use GIWS is to read the examples

Code using C++ generated files
`examples/*/main.cpp`

XML declaration files:
`examples/*/*.xml`


Usage
-----

`./giws -h` to see the help

Options :

* `-o` / `--output-dir=<dir>`
  Where files should be generated

* `-f` / `--description-file=<file>`
  Specify the declaration file to use

* `-p` / `--per-package`
  Creates a file per package instead of a file per object

* `-e` / `--throws-exception-on-error`
  Throws a C++ exception instead of an `exit(EXIT_FAILURE)`

* `--header-extension-file`: 
  Specify the extension of the header file generated \[Default: `.hxx`]

* `--body-extension-file`:
  Specify the extension of the body file generated \[Default: `.cpp`]

* `-v` / `--version`:
  Displays the version and other information

* `-h` / `--help`:
  Displays the help

	

Dependencies
------------

Obviously, as GIWS has been written in Python, it needs the Python interpreter
to work... and that's it!

