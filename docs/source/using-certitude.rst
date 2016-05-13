Using Certitude
===============

Certitude has one job: validating the TLS certificates a server has sent you.
To do that, you need to pass Certitude the TLS certificate chain sent by the
server, and the hostname you're expecting to connect to.

Getting A Certificate Chain
---------------------------

Certitude expects the TLS certificate chain as a list of TLS certificates
stored in the DER representation. Unfortunately, the Python standard library's
``ssl`` module is not capable of providing the entire certificate chain, only
the leaf certificate. This means that to use Certitude you will need to use
`pyopenssl`_ or something like it: it's just the only way to guarantee that
you get the complete certificate chain.

To get a certificate chain from PyOpenSSL, you'll want to make the connection
as normal and then call ``get_peer_cert_chain()``. This will get you your cert
chain as a list of ``X509`` objects. These will need decoding.

Given an already existing connection ``cnx``, you can get your list of
certificates like this:

.. code-block:: python

    certs = cnx.get_peer_cert_chain()

    encoded_certs = [
        OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
        for cert in certs
    ]

Validating The Chain
--------------------

Once you have the chain in place, it's simple enough to validate it. Simply
pass the chain into ``certitude.validate_cert_chain`` along with a unicode
string containing the expected hostname. For example:

.. code-block:: python

    valid = validate_cert_chain(encoded_certs, u'http2bin.org')


The ``validate_cert_chain`` function returns ``True`` if the cert chain is
valid, and ``False`` in any other case.

Notes
-----

When validating certificates using certitude you'll likely want to *disable*
OpenSSL's certificate validation. This is because OpenSSL and the
platform-specific TLS validation code will build their certificate chains
differently. In particular, OpenSSL may be *unable* to validate a chain that
the system library believes is valid. For that reason, put OpenSSL into the
``VERIFY_NONE`` mode and then handle the validation manually, *after* the
connection is made but **before you send any data on it**.

We cannot stress this enough: **you must validate the certificates before
sending or receiving data on the connection**.


.. _pyopenssl: https://pyopenssl.readthedocs.io/en/stable/
