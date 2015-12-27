# -*- coding: utf-8 -*-
"""
Access to the OS X trust store.

Provides access to the certitude API for OS X.
"""
import tempfile
import os

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


class CertificateFile(object):
    """
    Provides a temporary file containing the serialized certificates, allowing
    users to pass the path to this file to OpenSSL. This works with interfaces
    that only accept paths to certificate bundles, rather than using in-memory
    bundles, e.g. Requests.

    To avoid littering the system with temporary files, this object can be used
    as a context manager. In that case, the file will exist for as long as the
    context manager is open, and will then be deleted.

    The contents of the file are static and frozen at the time of first use.
    However, if the file is kept around for a long time it may be worthwhile to
    refresh its contents from time to time. This object allows doing exactly
    that with the ``build`` method.
    """
    def __init__(self):
        self.path = None
        self._fobj = None

    def build(self):
        """
        Writes the PEM-encoded trust roots into a temporary file.

        If managing an already-existing file, will replace the contents of that
        file with the updated values. Otherwise, will allocate a temporary
        file.
        """
        if self._fobj is not None:
            self._fobj.close()
            self._fobj = None

        if self.path is None:
            self._get_tempfile()
            assert self.path is not None

        with open(self.path, 'wb') as f:
            f.write(certificate_string())
            f.truncate()

        self._fobj = open(self.path, 'rb')

    def destroy(self):
        """
        Destroys the temporary file.
        """
        if self._fobj is not None:
            self._fobj.close()
            self._fobj = None

        if self.path is not None:
            self._destroy_tempfile()
            self.path = None

    def _get_tempfile(self):
        """
        Allocates a temporary file.
        """
        fd, path = tempfile.mkstemp(suffix='.pem')

        # Don't hold the file descriptor open, we don't need it.
        os.close(fd)
        self.path = path

    def _destroy_tempfile(self):
        """
        Actually destroys the temporary file.
        """
        os.remove(self.path)

    # Context Manager Protocol
    def __enter__(self):
        self.build()
        return self

    def __exit__(self, type, value, traceback):
        self.destroy()
        return False  # Never swallow exceptions

    # Proxy
    def __getattr__(self, name):
        return getattr(self._fobj, name)

    # Annoyingly, a finalizer
    def __del__(self):
        self.destroy()
