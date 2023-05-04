#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union

from common.error.base_error import BaseError


class ApplicationError(BaseError):
    """アプリケーションエラー（予期することができるエラー）"""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def initialize(self):
        return super().initialize()

    def __init__(self, label: str, args: Union[list[str], None] = None) -> None:
        super().__init__()
        self.__message = super().get_message(label, args)
        self.__level = super().get_level(label)

    def get_message(self):
        """エラーメッセージを取得"""
        return self.__message

    def get_level(self):
        return self.__level
