# -*- coding: utf-8 -*-
"""
Test basic Certitude functionality.
"""
import certitude


class TestValidation(object):
    def test_basic_validation(self, certifi_chain):
        """
        We can safely validate a good certificate chain.

        Note that this certificate chain belongs to certifi.io, and will expire
        in 2018.
        """
        assert certitude.validate_cert_chain(
            certifi_chain, u'certifi.io'
        )

    def test_hostname_validation(self, certifi_chain):
        """
        We fail to validate if the hostname doesn't match the provided cert.
        """
        assert not certitude.validate_cert_chain(
            certifi_chain, u'http2bin.org'
        )

    def test_reject_expired(self, expired):
        """
        We fail to validate expired certificates.
        """
        assert not certitude.validate_cert_chain(
            expired, u'expired.badssl.com'
        )

    def test_reject_invalid_host(self, wrong_host):
        """
        We fail to validate certificates that don't match their host.
        """
        assert not certitude.validate_cert_chain(
            wrong_host, u'wrong.host.badssl.com'
        )

    def test_reject_self_signed(self, self_signed):
        """
        We fail to validate self-signed certs.
        """
        assert not certitude.validate_cert_chain(
            self_signed, u'self-signed.badssl.com'
        )
