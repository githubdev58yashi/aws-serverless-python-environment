#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import pickle
from typing import Union

from common.aws.file_handler_wrapper import FileHandlerWrapper
from common.python.ini_reader import IniReader
from common.python.singleton import Singleton

fhw = FileHandlerWrapper().get()
ini = IniReader()

# エラーメッセージ
ERROR_MESSAGE_BASE_PATH: str = ini.get("error", "error_message_base_path")
ERROR_MESSAGE_PKL_BASE_PATH: str = ini.get("error", "error_message_pkl_base_path")
ERROR_MESSAGE_FILE_NAME: str = ini.get("error", "error_message_file_name")
ERROR_MESSAGE_FILE_EXTENSION: str = ini.get("error", "error_message_file_extension")

ERROR_MESSAGE_PATH: str = (
    f"{ERROR_MESSAGE_BASE_PATH}{ERROR_MESSAGE_FILE_NAME}{ERROR_MESSAGE_FILE_EXTENSION}"
)
ERROR_MESSAGE_PKL_PATH: str = (
    f"{ERROR_MESSAGE_PKL_BASE_PATH}{ERROR_MESSAGE_FILE_NAME}.pkl"
)


class BaseError(Singleton, Exception):
    """継承元となるエラークラス"""

    def __new__(cls, *args, **kwargs):
        return Singleton.__new__(cls)

    def initialize(self):
        super().initialize()
        self.error_message_list = list()
        self.error_message_dict = dict()

        if self.__is_exists_pkl():
            # pklが最新ではない場合、pklを作成しなおす。
            if self.__is_latest_pickle():
                self.error_message_list = self.__read_error_message_pkl()
            else:
                self.error_message_list = self.__read_error_message_csv()
                self.__create_error_message_pkl(self.error_message_list)

        else:
            self.error_message_list = self.__read_error_message_csv()
            self.__create_error_message_pkl(self.error_message_list)

        self.error_message_dict = {row["label"]: row for row in self.error_message_list}

    def __init__(self):
        pass

    def get_message(self, label: str, args: Union[list[str], None] = None) -> str:
        message: str = self.error_message_dict[label]["message"]
        if args is not None:
            message = message.format(*args)
        return message

    def get_level(self, label: str) -> str:
        return self.error_message_dict[label]["level"]

    @staticmethod
    def error(label: str, args: Union[list[str], None] = None) -> dict:
        return {"label": label, "args": args}

    def __is_exists_pkl(self):
        return fhw.exists(ERROR_MESSAGE_PKL_PATH)

    def __read_error_message_csv(self) -> list:
        return fhw.read_csv(ERROR_MESSAGE_PATH)

    def __read_error_message_pkl(self) -> list:
        return fhw.read_pkl(ERROR_MESSAGE_PKL_PATH)

    def __create_error_message_pkl(self, target: list):
        # バイナリ取得
        data = io.BytesIO()
        pickle.dump(target, data)
        fhw.write_binary(data.getvalue(), ERROR_MESSAGE_PKL_PATH)

    def __is_latest_pickle(self) -> bool:
        """pklファイルが最新かどうか判定

        ファイルの更新日時を元に判定する

        Returns:
            bool: 判定結果
        """

        base_last_modified = fhw.get_jst_last_modified(ERROR_MESSAGE_PATH)
        pkl_last_modified = fhw.get_jst_last_modified(ERROR_MESSAGE_PKL_PATH)
        if base_last_modified < pkl_last_modified:
            return True

        return False
