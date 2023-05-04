#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import io
import json
import pickle
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Union

import boto3
from botocore.exceptions import ClientError

from common.python.dateutil import to_jst
from common.python.extension import is_csv, is_json, is_pkl, is_txt
from common.python.ini_reader import IniReader
from common.python.singleton import Singleton

ini = IniReader()

WORKSPACE_PATH: str = str(Path(__file__).parent.parent.parent.parent)
BUCKET = ini.get("s3_file_handler", "bucket")
ACCESS_KEY = ini.get("aws", "access_key")
SECRET_ACCESS_KEY = ini.get("aws", "secret_access_key")
REGION = ini.get("s3_file_handler", "region")
SSE_CUSTOMER_ALGORITHM = ini.get("s3_file_handler", "sse_customer_algorithm")
ENCODING = ini.get("s3_file_handler", "encode")


class S3FileHandler(Singleton):
    """S3のファイルを操作するためのクラス"""

    def __new__(cls):
        return super().__new__(cls)

    def initialize(self, bucket: str = BUCKET, prefix: str = WORKSPACE_PATH):
        super().initialize()
        self.__prefix = prefix
        self.__prefix_path = Path(self.__prefix)
        self.__resource = boto3.resource(
            "s3",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name=REGION,
        )
        self.__bucket = self.__resource.Bucket(bucket)

    def __init__(self):
        pass

    def __target(self, target: str) -> Path:
        return self.__prefix_path.joinpath(target)

    def exists(self, filename: str) -> bool:
        """ファイルの存在確認

        Args:
            filename (str): ファイル名(バケット以降のパス含む)

        Returns:
            bool: 存在有無
        """

        try:
            self.__bucket.Object(filename).get()
        except ClientError:
            return False

        return True

    def exists_dir(self, directory_path: str) -> bool:
        """ディレクトリの存在確認

        Args:
            directory_path (str): ディレクトリパス(バケット以降のパス含む)

        Returns:
            bool: 存在有無
        """

        objects = list(self.__bucket.objects.filter(Prefix=directory_path))

        if 1 <= len(objects) and objects[0].key == directory_path:
            return True
        else:
            return False

    def read(
        self,
        filename: str,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ) -> bytes:
        """ファイル取得

        Args:
            filename (str): ファイル名(バケット以降のパス含む)
            sse_customer_key (Union[str, None], optional):
                暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional):
                暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

        Returns:
            Any: バイナリ
        """

        if sse_customer_key is None:
            # 暗号化無し
            obj = self.__bucket.Object(filename).get()
        else:
            # 暗号化あり
            # TODO: 未動確
            obj = self.__bucket.Object(filename).get(
                SSECustomerAlgorithm=sse_customer_algorithm,
                SSECustomerKey=sse_customer_key,
            )

        content = obj["Body"].read()
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
            filename (str): ファイル名(バケット以降のパス含む)
            encoding (str): 文字コード
            sse_customer_key (Union[str, None], optional):
                暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional):
                暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

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
            filename (str): ファイル名(バケット以降のパス含む)
            encoding (str): 文字コード
            has_header (bool): ヘッダー行として1行目を読み込むか
            sse_customer_key (Union[str, None], optional):
                暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional):
                暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

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
            filename (str): ファイル名(バケット以降のパス含む)
            encoding (str): 文字コード
            has_header (bool): ヘッダー行として1行目を読み込むか
            sse_customer_key (Union[str, None], optional):
                暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional):
                暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

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
            filename (str): ファイル名(バケット以降のパス含む)
            encoding (str): 文字コード
            has_header (bool): ヘッダー行として1行目を読み込むか
            sse_customer_key (Union[str, None], optional):
                暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional):
                暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.

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
        """ファイルをS3に書き出し

        Args:
            local_filename (str): ファイル名(パス含む)
            target_filename (str): ファイル名(バケット以降のパス含む)
            sse_customer_key (Union[str, None], optional):
                暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional):
                暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.
        """

        if sse_customer_key is None:
            # 暗号化無し
            self.__bucket.Object(target_filename).put(
                Body=open(self.__target(local_filename), "rb")
            )
        else:
            # 暗号化あり
            # TODO: 未動確
            self.__bucket.Object(target_filename).put(
                Body=open(self.__target(local_filename), "rb"),
                SSECustomerAlgorithm=sse_customer_algorithm,
                SSECustomerKey=sse_customer_key,
            )

    def write_binary(
        self,
        data: bytes,
        target_filename: str,
        sse_customer_key: Union[str, None] = None,
        sse_customer_algorithm: Union[str, None] = SSE_CUSTOMER_ALGORITHM,
    ):
        """ファイルをS3に書き出し

        Args:
            data (bytes): バイナリデータ
            target_filename (str): ファイル名(バケット以降のパス含む)
            sse_customer_key (Union[str, None], optional):
                暗号化キー. Defaults to None.
            sse_customer_algorithm (Union[str, None], optional):
                暗号化方式. Defaults to SSE_CUSTOMER_ALGORITHM.
        """

        if sse_customer_key is None:
            # 暗号化無し
            self.__bucket.Object(target_filename).put(Body=data)
        else:
            # 暗号化あり
            # TODO: 未動確
            self.__bucket.Object(target_filename).put(
                Body=data,
                SSECustomerAlgorithm=sse_customer_algorithm,
                SSECustomerKey=sse_customer_key,
            )

    def delete(self, filename: str):
        """ファイル削除

        ファイルが存在しない場合も正常に終了する

        Args:
            filename (str): ファイル名(パス含む)
        """

        self.__bucket.Object(filename).delete()

    def delete_dir(self, target: str):
        """ディレクトリ削除

        ディレクトリ内のオブジェクト削除後にディレクトリ削除を行う

        Args:
            target (str): ディレクトリ名(パス含む)
        """

        # ディレクトリ内のすべてのオブジェクトを削除
        for obj in self.__bucket.objects.filter(Prefix=target):
            self.__bucket.Object(obj.key).delete()

        # ディレクトリ削除
        self.__bucket.objects.filter(Prefix=target).delete()

    def dir_filenames(self, target: str) -> list[str]:
        """ディレクトリのファイル名一覧取得

        Args:
            target (str): ディレクトリ名(パス含む)

        Returns:
            list[str]: ファイル名
        """

        objects = self.__bucket.objects.filter(Prefix=target)
        filenames = [obj.key for obj in objects]
        return filenames

    def get_file_size(self, filename: str) -> Union[int, float]:
        """ファイルサイズ取得

        Args:
            filename (str): ファイル名(パス含む)

        Returns:
            Union[int, float]: サイズ
        """

        obj = self.__bucket.Object(filename)
        return obj.content_length

    def get_last_modified(self, filename: str) -> datetime:
        """ファイルの最終更新日時取得

        Args:
            filename (str): ファイル名(パス含む)

        Returns:
            datetime: 最終更新日時(UTC)
        """

        obj = self.__bucket.Object(filename)
        return obj.last_modified

    def get_jst_last_modified(self, filename: str) -> datetime:
        """ファイルの最終更新日時取得

        Args:
            filename (str): ファイル名(パス含む)

        Returns:
            datetime: 最終更新日時(JST)
        """

        obj = self.__bucket.Object(filename)
        return to_jst(obj.last_modified)
