.. certitude documentation master file, created by
   sphinx-quickstart on Tue Mar 15 16:45:56 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Certitude: Platform-Specific TLS Certificate Verification
=========================================================

Certitude provides Python bindings to the Windows and OS X system-native TLS
certificate libraries. This allows Python programs to validate TLS certificates
using the exact same logic used by native browsers on those platforms (e.g.
Safari and Internet Explorer/Edge).

This means that by combining Certitude with the OpenSSL used by default on most
Linuxes and BSDs, it is possible for a Python program to perform certificate
validation in a platform-native manner on all major operating systems. This
lets a Python program behave like a full native citizen of whatever platform it
is installed on.

This documentation discusses how to use Certitude.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   using-certitude
