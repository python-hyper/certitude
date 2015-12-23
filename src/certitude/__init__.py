# -*- coding: utf-8 -*-
"""
The certitude public API.

This module exposes only the platform-specific parts of certitude.
"""
# Currently we only support OS X.
from .osx import certificate_string
