#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import multiprocessing
import traceback

# 型
from typing import Any, Callable

MAX_PROCESS = 10

"""lambdaでmultiprocessingを使えるようにする

lambdaで通常のmultiprocessingは使用できないため、自前で用意する。

【注意点】
・並列処理の数が多い場合、ファイルディスクリプタの上限に達してエラーになります。
　lambdaのファイルディスクリプタは1000なので、それを超えないようにしてください。
　同一コンテナ内の話なので、並列処理を10とする場合、
　同一コンテナでlambdaが同時に11実行されると上限を超えます。


【使用例】
from common.aws.lambda_multi_processing
import call_multi_processing, multi_processing_function

def func1(arg1, arg2):
    print(arg1, arg2)
    return [arg1, arg2]

MAX_PROCESS = 3
args = list(zip(
    [func1] * MAX_PROCESS, ← 実行したい関数
    [1, 2, 3], ← func1に渡す引数(arg1)
    ["arg2"] * MAX_PROCESS ← func1に渡す引数(arg2)
))

res_list = call_multi_processing(multi_processing_function, args)
print("===== レスポンス =====")
print(res_list)

==================================================
1 arg2
2 arg2
3 arg2
===== レスポンス =====
[[1, 'arg2'], [2, 'arg2'], [3, 'arg2']]
==================================================

参考：https://qiita.com/yosiiii/items/838b11242895845cf7b1
"""


def call_multi_processing(
    function: Callable, args: list[tuple], max_process: int = MAX_PROCESS
) -> list:
    """マルチプロセスを実行する

    Args:
        function (Callable): 実行したい関数
        args (list[tuple]): 実行したい関数に渡す引数
        max_process (int, optional): 最大同時マルチプロセス数. Defaults to MAX_PROCESS.

    Returns:
        list: 実行したい関数の返り値をまとめたリスト
    """

    processes = []
    parent_connections = []
    process_responses = []

    cnt = 0
    for arg in args:
        parent_conn, child_conn = multiprocessing.Pipe()
        parent_connections.append(parent_conn)

        # 引数作成
        process_args = list(arg)
        process_args.insert(0, child_conn)
        processes.append(multiprocessing.Process(target=function, args=process_args))

        # 実行できる最大数で処理を実行
        if (cnt % max_process == 0) or len(args) <= cnt:
            for process in processes:
                process.start()

            for parent_connection in parent_connections:
                res = parent_connection.recv()
                process_responses.append(res)

            processes.clear()
            parent_connections.clear()

    return process_responses


def multi_processing_function(conn, function: Callable, *args) -> Any:
    """関数をマルチプロセスで実行させるためのラッパー

    Args:
        conn (Any): _description_
        function (Callable): 関数

    Returns:
        Any: 関数の返り値(conn経由で返す)
    """

    res = None

    try:
        res = function(*args)

    except Exception:
        print(traceback.format_exc())

    finally:
        conn.send(res)
        conn.close()
