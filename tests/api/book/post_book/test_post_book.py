#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from api.book.post_book.post_book import NgTitleError, check_parameters


def test_check_parameters_1():
    """エラー確認"""
    body = {
        "title": "Error 1",
    }

    with pytest.raises(NgTitleError):
        check_parameters(body)


def test_check_parameters_2():
    """正常確認"""
    body = {
        "title": "book1",
    }

    assert check_parameters(body) is None
