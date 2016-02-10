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


@pytest.fixture
def certifi_chain():
    """
    Returns the trust chain associated with certifi.io. Note that this expires
    in 2018.
    """
    with open(os.path.join(HERE, 'certifi_chain.pem'), 'r') as f:
        chain = f.read()

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
    assert len(encoded_certs) == 3
    return encoded_certs
