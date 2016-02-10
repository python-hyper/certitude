# -*- coding: utf-8 -*-
"""
The certitude public API.

This module exposes only the platform-specific parts of certitude.
"""
from .api import validate_cert_chain

__all__ = ['validate_cert_chain']
