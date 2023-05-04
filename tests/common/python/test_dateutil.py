#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timezone, timedelta
import common.python.dateutil as dateutil


def test_datetime_formatted():
    dt = datetime(2023, 1, 1, 12, 30, 30)

    assert dateutil.datetime_formatted(dt) == '2023-01-01 12:30:30'


def test_to_jst():
    dt = datetime(2023, 1, 1, 12, 30, 30, tzinfo=timezone.utc)
    jst_dt = datetime(2023, 1, 1, 21, 30, 30, tzinfo=timezone(timedelta(hours=9), name='JST'))

    assert dateutil.to_jst(dt) == jst_dt


def test_to_utc():
    dt = datetime(2023, 1, 1, 12, 30, 30, tzinfo=timezone.utc)
    jst_dt = datetime(2023, 1, 1, 21, 30, 30, tzinfo=timezone(timedelta(hours=9), name='JST'))

    assert dateutil.to_utc(jst_dt) == dt


def test_to_jst_formatted():
    dt = datetime(2023, 1, 1, 12, 30, 30, tzinfo=timezone.utc)
    assert dateutil.to_jst_formatted(dt) == '2023-01-01 21:30:30'


def test_to_utc_formatted():
    dt = datetime(2023, 1, 1, 12, 30, 30, tzinfo=timezone(timedelta(hours=9), name='JST'))
    assert dateutil.to_utc_formatted(dt) == '2023-01-01 03:30:30'
