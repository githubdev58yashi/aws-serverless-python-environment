#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Union

from common.python.singleton import Singleton

if os.getenv("AWS_EXECUTION_ENV") is not None:
    # lambda上にデプロイされているとき
    ROOT_PATH = Path("/var/task")
else:
    # ローカル
    ROOT_PATH = Path(__file__).parent.parent.parent.parent

MAIN_INI_PATH = "conf/main.ini"
DEPENDENCIES_INI_PATH = "conf/dependencies.ini"

CONVERT_TYPE = ["str", "int", "float", "bool", "list", "dict"]


class IniReader(Singleton):
    def __new__(cls):
        return super().__new__(cls)

    def initialize(self):
        super().initialize()
        self._config = ConfigParser()
        # iniファイル読み込み
        self._config.read(ROOT_PATH / MAIN_INI_PATH)
        self._config.read(ROOT_PATH / DEPENDENCIES_INI_PATH)

    def __init__(self) -> None:
        super().__init__()

    def get(self, section: str, key: str, convert_type: Union[str, None] = None) -> Any:
        """iniファイルの値取得

        Args:
            section (str): セクション名
            key (str): キー名
            convert_type (str): 変換する型 'str', 'int', 'float', 'bool', 'list', 'dict'

        Returns:
            str: 値
        """
        try:
            # 変換
            if convert_type not in CONVERT_TYPE:
                return self._config.get(section, key, raw=True)
            elif convert_type == "str":
                return self._config.get(section, key, raw=True)
            elif convert_type == "int":
                return self._config.getint(section, key)
            elif convert_type == "float":
                return self._config.getfloat(section, key)
            elif convert_type == "bool":
                return self._config.getboolean(section, key)
            elif convert_type == "list":
                value = self._config[section][key]
                return list(value)
            elif convert_type == "dict":
                value = self._config[section][key]
                return json.loads(value)

            return self._config.get(section, key, raw=True)

        except KeyError:
            raise ValueError(f"{section}:{key} not found")

        except Exception as e:
            raise e
