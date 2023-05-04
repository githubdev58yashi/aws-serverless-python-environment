#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone

from common.python.ini_reader import IniReader

ini = IniReader()

HOURS = ini.get("timezone", "hours", "int")
NAME = ini.get("timezone", "name")
TZ = timezone(timedelta(hours=HOURS), name=NAME)

DYNAMODB_DATETIME_FORMAT = ini.get("dynamodb", "datetime_format")


def datetime_formatted(target: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """日時を指定されたフォーマットの形式で取得

    Args:
        target (datetime): 日時
        format (str): フォーマット

    Returns:
        str: フォーマットされた日時
    """

    return target.strftime(format)


def local_datetime() -> datetime:
    return datetime.now(TZ)


def local_datetime_formatted(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime_formatted(local_datetime(), format)


def jst_datetime() -> datetime:
    return datetime.now(timezone(timedelta(hours=9), name="JST"))


def jst_datetime_formatted(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime_formatted(jst_datetime(), format)


def jst_datetime_dynamodb_formatted() -> str:
    return datetime_formatted(jst_datetime(), DYNAMODB_DATETIME_FORMAT)


def utc_datetime() -> datetime:
    return datetime.now(timezone.utc)


def utc_datetime_formatted(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime_formatted(utc_datetime(), format)


def to_jst(target: datetime) -> datetime:
    """JSTに変換

    Args:
        target (datetime): 日時

    Returns:
        datetime: JSTの日時
    """
    return target.astimezone(timezone(timedelta(hours=9), name="JST"))


def to_jst_formatted(target: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """JSTの指定されたフォーマットに変換

    Args:
        target (datetime): 日時
        format (str): フォーマット

    Returns:
        str: JSTのフォーマットの形式日時
    """
    return datetime_formatted(to_jst(target), format)


def to_jst_dynamodb_formatted(target: datetime) -> str:
    return to_jst_formatted(target, DYNAMODB_DATETIME_FORMAT)


def to_utc(target: datetime) -> datetime:
    """UTCに変換

    Args:
        target (datetime): 日時

    Returns:
        datetime: UTCの日時
    """
    return target.astimezone(timezone.utc)


def to_utc_formatted(target: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """UTCの指定されたフォーマットに変換

    Args:
        target (datetime): 日時
        format (str): フォーマット

    Returns:
        str: UTCのフォーマットの形式日時
    """

    return datetime_formatted(to_utc(target), format)


def to_utc_dynamodb_formatted(target: datetime) -> str:
    return to_utc_formatted(target, DYNAMODB_DATETIME_FORMAT)
