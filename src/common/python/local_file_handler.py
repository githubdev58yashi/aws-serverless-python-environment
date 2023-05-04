#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import io
import json
import os
import pickle
import shutil
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Union

from common.python.dateutil import to_jst, to_utc
from common.python.extension import is_csv, is_json, is_pkl, is_txt
from common.python.ini_reader import IniReader
from common.python.singleton import Singleton

ini = IniReader()

WORKSPACE_PATH: str = str(Path(__file__).parent.parent.parent.parent)
SSE_CUSTOMER_ALGORITHM = ini.get("s3_file_handler", "sse_customer_algorithm")
ENCODING = ini.get("s3_file_handler", "encode")


class LocalFileHandler(Singleton):
    """ローカルのファイルを操作するためのクラス"""

    def __new__(cls):
        return super().__new__(cls)

    def initialize(self, prefix: str = WORKSPACE_PATH):
        super().initialize()
        self.__prefix = prefix
        self.__prefix_path = Path(self.__prefix)

    def __init__(self) -> None:
        super().__init__()

    def target(self, target: str) -> Path:
        return self.__prefix_path.joinpath(target)

    def make_dir(self, target: str):
        if not os.path.exists(self.target(target)):
            os.mkdir(self.target(target))

    def exists(self, filename: str) -> bool:
        """ファイルの存在確認

        Args:
            filename (str): ファイル名(基底パス以降のパス含む)

        Returns:
            bool: 存在有無
        """

        return os.path.isfile(self.target(filename))

    def exists_dir(self, directory_path: str) -> bool:
        """ディレクトリの存在確認

        Args:
            directory_path (str): ディレクトリパス(基底パス以降のパス含む)

        Returns:
            bool: 存在有無
        """

        return os.path.isdir(self.target(directory_path))

    def read(
        self,
        filename: str,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ) -> bytes:
        """ファイル取得

        Args:
            filename (str): ファイル名(基底パス以降のパス含む)
            sse_customer_key (Union[str, None], optional): 暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional): 暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

        Returns:
            Any: バイナリ
        """

        content = bytes()
        with open(self.target(filename), mode="rb") as f:
            content = f.read()

        return content

    def read_txt(
        self,
        filename: str,
        encoding: str = ENCODING,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ) -> str:
        """ファイル取得

        Args:
            filename (str): ファイル名(基底パス以降のパス含む)
            encoding (str): 文字コード
            sse_customer_key (Union[str, None], optional): 暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional): 暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

        Returns:
            Any: ファイルの中身
        """

        if not is_txt(filename):
            print(f"拡張子が.txt以外のファイルのため、空文字を返却しました。 ファイル名:{filename}")
            return ""

        obj = self.read(filename, sse_customer_key, sse_customer_algorithm)
        content = obj.decode(encoding)
        return content

    def read_csv(
        self,
        filename: str,
        encoding: str = ENCODING,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ) -> list:
        """CSVファイル取得

        Args:
            filename (str): ファイル名(基底パス以降のパス含む)
            encoding (str): 文字コード
            has_header (bool): ヘッダー行として1行目を読み込むか
            sse_customer_key (Union[str, None], optional): 暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional): 暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

        Returns:
            list: list
        """

        if not is_csv(filename):
            print(f"拡張子が.csv以外のファイルが指定されました。 ファイル名:{filename}")
            return []

        obj = self.read(filename, sse_customer_key, sse_customer_algorithm)
        content = BytesIO(obj)
        text_io = io.TextIOWrapper(content, encoding=encoding)
        reader = csv.DictReader(text_io, quoting=csv.QUOTE_ALL)
        results = [r for r in reader]
        return results

    def read_pkl(
        self,
        filename: str,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ) -> Any:
        """pklファイル取得

        Args:
            filename (str): ファイル名(基底パス以降のパス含む)
            encoding (str): 文字コード
            has_header (bool): ヘッダー行として1行目を読み込むか
            sse_customer_key (Union[str, None], optional): 暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional): 暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

        Returns:
            Any: ファイルによる
        """

        if not is_pkl(filename):
            print(f"拡張子が.pkl以外のファイルが指定されました。 ファイル名:{filename}")
            return None

        obj = self.read(filename, sse_customer_key, sse_customer_algorithm)
        content = pickle.loads(obj)
        return content

    def read_json(
        self,
        filename: str,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ) -> Any:
        """jsonファイル取得

        Args:
            filename (str): ファイル名(基底パス以降のパス含む)
            encoding (str): 文字コード
            has_header (bool): ヘッダー行として1行目を読み込むか
            sse_customer_key (Union[str, None], optional): 暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional): 暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

        Returns:
            Any: ファイルによる
        """

        if not is_json(filename):
            print(f"拡張子が.json以外のファイルが指定されました。 ファイル名:{filename}")
            return None

        obj = self.read(filename, sse_customer_key, sse_customer_algorithm)
        content = json.loads(obj)
        return content

    def write(
        self,
        local_filename: str,
        target_filename: str,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ):
        """ファイルを書き出し

        Args:
            local_filename (str): ファイル名(パス含む)
            target_filename (str): ファイル名(基底パス以降のパス含む)
            sse_customer_key (Union[str, None], optional): 暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional): 暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.
        """

        obj = self.read(local_filename, sse_customer_key, sse_customer_algorithm)
        self.make_dir(os.path.dirname(target_filename))
        with open(self.target(target_filename), "wb") as f:
            f.write(obj)

    def write_binary(
        self,
        data: bytes,
        target_filename: str,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ):
        """ファイルを書き出し

        Args:
            data (bytes): バイナリデータ
            target_filename (str): ファイル名(バケット以降のパス含む)
            sse_customer_key (Union[str, None], optional): 暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional): 暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.
        """

        self.make_dir(os.path.dirname(target_filename))
        with open(self.target(target_filename), "wb") as f:
            f.write(data)

    def delete(self, filename: str):
        """ファイル削除

        ファイルが存在しない場合も正常に終了する

        Args:
            filename (str): ファイル名(パス含む)
        """

        if os.path.exists(self.target(filename)):
            os.remove(self.target(filename))

    def delete_dir(self, target: str):
        """ディレクトリ削除

        Args:
            target (str): ディレクトリ名(パス含む)
        """

        shutil.rmtree(self.target(target))

    def dir_filenames(self, target: str) -> list[str]:
        """ディレクトリのファイル名一覧取得

        Args:
            target (str): ディレクトリ名(パス含む)

        Returns:
            list[str]: ファイル名
        """

        objects = os.listdir(self.target(target))
        filenames = [
            obj
            for obj in objects
            if os.path.isfile(os.path.join(self.target(target), obj))
        ]
        return filenames

    def get_file_size(self, filename: str) -> Union[int, float]:
        """ファイルサイズ取得

        Args:
            filename (str): ファイル名(パス含む)

        Returns:
            Union[int, float]: サイズ
        """

        return os.path.getsize(self.target(filename))

    def get_last_modified(self, filename: str) -> datetime:
        """ファイルの最終更新日時取得

        Args:
            filename (str): ファイル名(パス含む)

        Returns:
            datetime: 最終更新日時(UTC)
        """

        timestamp = os.path.getmtime(self.target(filename))
        last_modified: datetime = datetime.fromtimestamp(timestamp)

        return to_utc(last_modified)

    def get_jst_last_modified(self, filename: str) -> datetime:
        """ファイルの最終更新日時取得

        Args:
            filename (str): ファイル名(パス含む)

        Returns:
            datetime: 最終更新日時(JST)
        """

        timestamp = os.path.getmtime(self.target(filename))
        last_modified: datetime = datetime.fromtimestamp(timestamp)

        return to_jst(last_modified)
