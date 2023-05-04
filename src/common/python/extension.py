#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def get_extension(filename: str) -> str:
    """拡張子を取得

    Args:
        filename (str): ファイル名

    Returns:
        str: 拡張子
    """

    _, extension = os.path.splitext(filename)
    return extension


def is_txt(filename: str) -> bool:
    """テキストファイル(.txt)か判定

    Args:
        filename (str): ファイル名

    Returns:
        bool: 判定結果
    """

    extension = get_extension(filename)
    if extension == ".txt":
        return True
    else:
        return False


def is_csv(filename: str) -> bool:
    """CSVファイル(.csv)か判定

    Args:
        filename (str): ファイル名

    Returns:
        bool: 判定結果
    """

    extension = get_extension(filename)
    if extension == ".csv":
        return True
    else:
        return False


def is_pkl(filename: str) -> bool:
    """pickleファイル(.pkl)か判定

    Args:
        filename (str): ファイル名

    Returns:
        bool: 判定結果
    """

    extension = get_extension(filename)
    if extension == ".pkl":
        return True
    else:
        return False


def is_json(filename: str) -> bool:
    """json(.json)か判定

    Args:
        filename (str): ファイル名

    Returns:
        bool: 判定結果
    """

    extension = get_extension(filename)
    if extension == ".json":
        return True
    else:
        return False
