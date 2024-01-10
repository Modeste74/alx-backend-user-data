#!/usr/bin/env python3
"""defines classes and functions on user-data protection
in logging datas"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    return re.sub(
        fr'({separator}|^)({"|".join(fields)})=([^{separator}]+)',
        fr'\1\2={redaction}{separator}', message
    )
