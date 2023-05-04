#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union

from common.aws.s3_file_handler import S3FileHandler
from common.python.ini_reader import IniReader
from common.python.local_file_handler import LocalFileHandler
from common.python.singleton import Singleton

ini = IniReader()

is_local: bool = ini.get("common", "is_local", "bool")


class FileHandlerWrapper(Singleton):
    """S3FileHandler/LocalFileHandlerを使用するためのラッパー

    iniファイルのis_localにより設定を行う
    """

    def __new__(cls):
        return super().__new__(cls)

    def initialize(self):
        super().initialize()
        self.s3_file_handler = S3FileHandler()
        self.local_file_handler = LocalFileHandler()

    def __init__(self):
        pass

    def get(self, use_local: bool = is_local) -> Union[S3FileHandler, LocalFileHandler]:
        """ファイルハンドラを取得

        引数にTrueが渡された場合、LocalHandlerを読み込む

        Args:
            is_local (bool): ローカル実行かどうか

        Returns:
            Union[S3FileHandler, LocalFileHandler]: ファイルハンドラ
        """

        if use_local:
            return self.local_file_handler
        else:
            return self.s3_file_handler
