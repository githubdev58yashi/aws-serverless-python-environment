#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
import json
import os
import traceback

# 型
from collections.abc import Callable
from typing import Any

OUTPUT_PATH = './func_handler_result/'


def save_result_to_json(func: Callable) -> Any:
    """関数の返り値をJSONに保存

    JSONに変換出来ない返り値は保存しない。

    Args:
        func (Callable): 関数

    Returns:
        Any: 関数の返り値
    """
    @wraps(func)
    def wrapper(*args: Any, **kargs: Any):
        result = func(*args, **kargs)
        try:
            if not os.path.exists(OUTPUT_PATH):
                os.mkdir(OUTPUT_PATH)
            with open(f'{OUTPUT_PATH}{func.__name__}.json', 'w') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

        except Exception:
            print(f'JSON保存エラー:{func.__name__}')
            print('JSONに変換出来なかったため、保存を行いませんでした。')
            print(traceback.format_exc())

        finally:
            return result

    return wrapper


def load_result_from_json(func: Callable) -> Any:
    """関数の返り値にJSONを設定

    save_result_to_jsonが対象の関数で実行されている前提。
    関数は実行せずに、保存済みのjsonを返却する。

    Args:
        func (Callable): 関数

    Returns:
        Any: 保存済みのjson
    """
    @wraps(func)
    def wrapper(*args: Any, **kargs: Any):
        try:
            with open(f'{OUTPUT_PATH}{func.__name__}.json') as f:
                result = json.load(f)
                return result

        except Exception as e:
            print(f'JSON取得エラー:{func.__name__}')
            print('JSONを取得出来ませんでした。')
            print(traceback.format_exc())
            raise e

    return wrapper


def print_func_name(func: Callable):
    """実行した関数を出力する

    Args:
        func (Callable): 関数

    """
    @wraps(func)
    def wrapper(*args: Any, **kargs: Any):
        print(func.__name__)
        result = func(*args, **kargs)
        return result

    return wrapper
