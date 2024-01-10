#!/usr/bin/env python3
"""defines classes and functions on user-data protection
in logging datas"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    obf = re.compile(
        fr'({separator}|^)({"|".join(fields)})=([^{separator}]+)')
    return obf.sub(fr'\1\2={redaction}{separator}', message)
