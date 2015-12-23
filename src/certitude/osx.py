# -*- coding: utf-8 -*-
"""
Access to the OS X trust store.

Provides access to the certitude API for OS X.
"""
from cryptography.hazmat.bindings.commoncrypto.binding import ffi, lib


def certificate_string():
    """
    Returns a list of certificate roots in PEM format as a Python string.
    """
    anchors = ffi.new("CFArrayRef *")

    status = lib.SecTrustCopyAnchorCertificates(anchors)
    if status != 0:
        raise RuntimeError("Unable to get anchors")

    certificates = ffi.cast("CFTypeRef", anchors[0])
    exported_data = ffi.new("CFDataRef *")
    status = lib.SecItemExport(
        certificates,  # secItemOrArray
        lib.kSecFormatPEMSequence,  # outputFormat
        0,  # flags
        ffi.NULL,  # params
        exported_data
    )
    if status != 0:
        raise RuntimeError("Unable to export certificates")

    l = lib.CFDataGetLength(exported_data[0])
    output = ffi.new("UInt8[]", l)
    lib.CFDataGetBytes(exported_data[0], lib.CFRangeMake(0, l), output)
    data = ffi.buffer(output, l)[:]

    lib.CFRelease(ffi.cast("CFTypeRef", exported_data[0]))
    lib.CFRelease(certificates)
    return data
