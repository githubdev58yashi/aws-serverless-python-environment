#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.python.ini_reader import IniReader

ini = IniReader()


def test_int():
    val = ini.get("test", "int", "int")

    assert isinstance(val, int) is True


def test_float():
    val = ini.get("test", "float", "float")

    assert isinstance(val, float) is True


def test_str1():
    val = ini.get("test", "str")

    assert isinstance(val, str) is True


def test_str2():
    val = ini.get("test", "str", "str")

    assert isinstance(val, str) is True


def test_list():
    val = ini.get("test", "list", "list")

    assert isinstance(val, list) is True


def test_dict():
    val = ini.get("test", "dict", "dict")

    assert isinstance(val, dict) is True


def test_bool():
    val = ini.get("test", "bool", "bool")

    assert isinstance(val, bool) is True
