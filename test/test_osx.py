# -*- coding: utf-8 -*-
"""
Tests of the OS X-specific functionality in certitude. These tests will only
run on the OS X platform, and will otherwise be skipped.
"""
import os.path
import platform

import pytest

import certitude
import certitude.osx


is_osx = (platform.system() == 'Darwin')


@pytest.mark.skipif(not is_osx, reason="OS X tests skipped on this platform")
class TestOSX(object):
    def test_os_x_certificate_string_contains_pem_files(self):
        """
        Calling the OS X-specific certificate_string function gives PEM files.
        """
        data = certitude.osx.certificate_string()
        data.rstrip()
        assert data.startswith(b'-----BEGIN CERTIFICATE-----')
        assert data.endswith(b'-----END CERTIFICATE-----')

    def test_certificate_string_matches_osx_cert_string(self):
        """
        The OS X-specific certificate_string function gives the same output as
        the "general" one.
        """
        specific = certitude.osx.certificate_string()
        general = certitude.certificate_string()

        assert specific == general

    def test_certificate_file_contains_certificate_string(self):
        """
        Confirm the certificate file written out is the same as the certificate
        string generated.
        """
        with certitude.CertificateFile() as f:
            file_data = f.read()

        certstring = certitude.certificate_string()
        assert certstring == file_data

    def test_certificate_file_is_deleted_after_context_manager(self):
        """
        The certificate file gets deleted after the context manager is exited.
        """
        with certitude.CertificateFile() as f:
            path = f.path
            assert os.path.exists(path)

        assert not os.path.exists(path)

    def test_certificate_file_is_deleted_after_destroy(self):
        """
        The certificate file gets deleted after the destroy method is called.
        """
        f = certitude.CertificateFile()
        f.build()
        path = f.path
        assert os.path.exists(path)

        f.destroy()
        assert not os.path.exists(path)

    def test_cannot_read_destroyed_tempfile(self):
        """
        Destroying a tempfile prevents reading from it.
        """
        with certitude.CertificateFile() as f:
            assert len(f.read(1)) == 1

        with pytest.raises(AttributeError):
            f.read()
