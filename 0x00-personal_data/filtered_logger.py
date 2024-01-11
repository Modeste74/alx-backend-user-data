#!/usr/bin/env python3
"""defines classes and functions on user-data protection
in logging datas"""
import re
from typing import List
import logging


'''class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError'''


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    return re.sub(
        fr'({separator}|^)({"|".join(fields)})=([^{separator}]+)',
        fr'\1\2={redaction}', message
    )
