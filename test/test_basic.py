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
