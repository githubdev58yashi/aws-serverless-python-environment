#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
import time
import traceback

# 型
from collections.abc import Callable
from typing import Any


def stop_watch(func: Callable):
    """関数の処理時間を計測する

    Args:
        func (Callable): 対象の関数
    """
    @wraps(func)
    def wrapper(*args: Any, **kargs: Any):
        try:
            start = time.time()
            result = func(*args, **kargs)
            elapsed_time = time.time() - start
            print(f"処理時間計測 対象処理:{func.__name__} 処理時間:{elapsed_time:.8f}秒")

        except Exception as e:
            print(f'JSON保存エラー:{func.__name__}')
            print('JSONに変換出来なかったため、保存を行いませんでした。')
            print(traceback.format_exc())
            raise e

        return result
    return wrapper
