# -*- coding: utf-8 -*-
"""
Defines the public API to certitude. This includes wrapping the C-level
function with some convenience wrappers.
"""
from .certitude import ffi, lib


def validate_cert_chain(certs, hostname):
    """
    Validate a specific cert chain is valid for a TLS connection to hostname.

    :param certs: A list of DER-encoded certificates.
    :param hostname: A unicode string containing the contacted hostname.
    :returns: True if the certificates are valid, False otherwise.
    """
    # TODO: Raise error codes with appropriate messages instead.
    encoded_certs, lengths = zip(*[
        (ffi.new("uint8_t[]", cert), len(cert)) for cert in certs
    ])
    cert_ptr_buffer = ffi.new("uint8_t*[]", encoded_certs)
    cert_size_buffer = ffi.new("size_t[]", lengths)
    cert_count = ffi.new("int *", len(certs))
    hostname = ffi.new("char[]", hostname.encode('utf-8'))

    result = lib.validate_cert_chain(
        cert_ptr_buffer,
        cert_size_buffer,
        cert_count[0],
        hostname,
    )
    return result == 1
