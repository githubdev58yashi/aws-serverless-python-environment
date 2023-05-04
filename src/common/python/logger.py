#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from common.python.ini_reader import IniReader
from common.python.local_file_handler import LocalFileHandler
from common.python.singleton import Singleton

fh = LocalFileHandler()
ini = IniReader()

IS_LOCAL: bool = ini.get("common", "is_local", "bool")
WRITE_LOCAL_LOG: bool = ini.get("logger", "write_local_log", "bool")
LOCAL_LOG_BASE_PATH: str = ini.get("logger", "local_log_base_path")
LOCAL_LOG_FILE_NAME: str = ini.get("logger", "local_log_file_name")
LOCAL_LOG_FILE: str = f"{LOCAL_LOG_BASE_PATH}{LOCAL_LOG_FILE_NAME}"
DATE_FORMAT: str = ini.get("logger", "date_format")
LOG_FORMAT = (
    "[%(levelname)s]\t"
    "%(asctime)s.%(msecs)dZ\t"
    "%(filename)s\t"
    "%(funcName)s\t"
    "%(lineno)d\t"
    "%(message)s"
)


class Logger(Singleton):
    def __new__(cls):
        return super().__new__(cls)

    def initialize(self):
        super().initialize()
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.INFO)

        # 通常(lambda)のログ設定
        self.__set_lambda_handler()

        if WRITE_LOCAL_LOG and IS_LOCAL:
            # ローカルのログ設定
            self.__set_local_handler()

    def __init__(self) -> None:
        super().__init__()

    def __set_local_handler(self):
        """ローカルのログ設定"""

        target = fh.target(LOCAL_LOG_FILE)
        fh.make_dir(LOCAL_LOG_BASE_PATH)
        handler = logging.FileHandler(target)
        formatter = logging.Formatter(
            LOG_FORMAT,
            DATE_FORMAT,
        )
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

    def __set_lambda_handler(self):
        """lambdaのログ設定"""

        formatter = logging.Formatter(
            LOG_FORMAT,
            DATE_FORMAT,
        )

        for handler in self.__logger.handlers:
            handler.setFormatter(formatter)

    def write_debug(self, message: str):
        self.__logger.debug(message)

    def write_info(self, message: str):
        self.__logger.info(message)

    def write_warn(self, message: str):
        self.__logger.warn(message)

    def write_error(self, message: str):
        self.__logger.error(message)

    def write_critical(self, message: str):
        self.__logger.critical(message)

    def write_lambda_event(self, message: str):
        """event.jsonをログ出力

        cloudwatch上で検索しやすいように、特定の文字列を追加する。

        Args:
            message (str): 出力メッセージ
        """
        self.__logger.info("[event.json] " + message)

    def write_lambda_result(self, message: str):
        """lambdaのresultをログ出力

        cloudwatch上で検索しやすいように、特定の文字列を追加する。

        Args:
            message (str): 出力メッセージ
        """
        self.__logger.info("[result] " + message)
