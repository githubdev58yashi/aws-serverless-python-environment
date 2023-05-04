#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common.aws.lambda_multi_processing as lmp


def test_call_multi_processing1():
    """返り値がNoneの場合"""

    def return_none_func():
        print("return_none_func")
        return None

    PROCESSES = 5
    args = list(zip(
        [return_none_func] * PROCESSES
    ))
    res_list = lmp.call_multi_processing(lmp.multi_processing_function, args)

    assert res_list == [None, None, None, None, None]


def test_call_multi_processing2():
    """返り値がiniとか"""

    def return_int_func():
        print("return_int_func")
        return 1

    PROCESSES = 5
    args = list(zip(
        [return_int_func] * PROCESSES
    ))
    res_list = lmp.call_multi_processing(lmp.multi_processing_function, args)

    assert res_list == [1, 1, 1, 1, 1]


def test_call_multi_processing3():
    """返り値がlistとか"""

    RETURN_LIST = ["1111", 1111, None, ["aaa", "bbb"]]

    def return_list_func():
        print("return_list_func")
        return RETURN_LIST

    PROCESSES = 3
    args = list(zip(
        [return_list_func] * PROCESSES
    ))
    res_list = lmp.call_multi_processing(lmp.multi_processing_function, args)

    assert res_list == [RETURN_LIST, RETURN_LIST, RETURN_LIST]
