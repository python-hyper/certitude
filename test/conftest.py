# -*- coding: utf-8 -*-
"""
conftest.py
~~~~~~~~~~~

Py.test fixtures.
"""
import os.path

import pytest

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding


CERT_DELIMITER = '-----END CERTIFICATE-----\n'
HERE = os.path.dirname(__file__)


def build_chain_from_pem(chain):
    """
    Splits a PEM cert chain and converts them to DER bytes.
    """
    certs = chain.split(CERT_DELIMITER)

    parsed_certs = (
        x509.load_pem_x509_certificate(
            (cert+CERT_DELIMITER).encode('ascii'),
            default_backend()
        )
        for cert in certs if cert
    )
    encoded_certs = [
        cert.public_bytes(Encoding.DER) for cert in parsed_certs
    ]
    return encoded_certs


@pytest.fixture
def certifi_chain():
    """
    Returns the trust chain associated with certifi.io. Note that this expires
    in 2018.
    """
    with open(os.path.join(HERE, 'fixtures', 'certifi_chain.pem'), 'r') as f:
        chain = f.read()

    encoded_certs = build_chain_from_pem(chain)
    assert len(encoded_certs) == 3
    return encoded_certs


@pytest.fixture
def expired():
    """
    Returns the cert chain from expired.badssl.com.
    """
    with open(os.path.join(HERE, 'fixtures', 'expired-badssl.pem'), 'r') as f:
        chain = f.read()

    encoded_certs = build_chain_from_pem(chain)
    assert len(encoded_certs) == 3
    return encoded_certs


@pytest.fixture
def wrong_host():
    """
    Returns the cert chain from wrong.host.badssl.com.
    """
    path = os.path.join(HERE, 'fixtures', 'wronghost-badssl.pem')
    with open(path, 'r') as f:
        chain = f.read()

    encoded_certs = build_chain_from_pem(chain)
    assert len(encoded_certs) == 3
    return encoded_certs


@pytest.fixture
def self_signed():
    """
    Returns the cert chain from selfsigned.badssl.com.
    """
    path = os.path.join(HERE, 'fixtures', 'selfsigned-badssl.pem')
    with open(path, 'r') as f:
        chain = f.read()

    encoded_certs = build_chain_from_pem(chain)
    assert len(encoded_certs) == 1
    return encoded_certs
