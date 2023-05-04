#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api.book.get_book.get_book import get_book


def test_get_book_1():
    """エラー確認"""
    id = "not_exist_id"

    assert get_book(id) == {}
