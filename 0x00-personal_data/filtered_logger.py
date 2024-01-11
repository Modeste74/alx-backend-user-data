#!/usr/bin/env python3
"""defines classes and functions on user-data protection
in logging datas"""
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialzes the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """akes a LogRecord instance (record) as an
        argument and returns a formatted string"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    return re.sub(
        fr'({separator}|^)({"|".join(fields)})=([^{separator}]+)',
        fr'\1\2={redaction}', message
    )


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger("user-data")
    loogger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> MySQLConnection:
    """return a connector to the MySQL databse"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    connector: MySQLConnection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return connector


def main():
    """Obtaining a database connection and logging user data."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")

    log = get_logger()
    for row in cursor:
        filtered_data = filter_row_dict(dict(zip(PII_FIELDS, row)))
        log.info(filtered_data)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
