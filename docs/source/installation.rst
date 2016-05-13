Installing Certitude
====================

Certitude involves bindings to native-code libraries, and is a library that
functions only on Windows and OS X. These two platforms traditionally have
problems with native-code bindings from Python, due to their lack of compilers
or fully-fledged dependency resolution.

For this reason, while Certitude is available as a source distribution, it also
provides pre-compiled binary wheels for both Windows and OS X. For this reason
it is *strongly preferred* that a recent pip is used for installing Certitude,
as this will remove the need for a compiler toolchain that you may not have
installed.

To install Certitude, the pip command is very simple:

.. code-block:: bash

    $ pip install certitude

This should download and install a wheel that makes certitude available.
