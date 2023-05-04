#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import gzip
import io
import json
import traceback
from datetime import date, datetime

# 型
from typing import Any, Callable

from common.error.application_error import ApplicationError
from common.error.fatal_error import FatalError
from common.python.ini_reader import IniReader
from common.python.logger import Logger

ini = IniReader()
logger = Logger()


# http status code
STATUS_CODE_SUCCESS: int = ini.get("status_code", "success", "int")
STATUS_CODE_APPLICATION_ERROR: int = ini.get("status_code", "application_error", "int")
STATUS_CODE_FATAL_ERROR: int = ini.get("status_code", "fatal_error", "int")

DATETIME_FORMAT = ini.get("lambda_handler", "datetime_format")
DATE_FORMAT = ini.get("lambda_handler", "date_format")


DEFAULT_HEADERS = {
    # CORS対策
    "Access-Control-Allow-Origin": "*",
    # キャッシュさせるか
    "Cache-Control": "max-age=0",
    # クリックジャッキング
    "X-FRAME-OPTIONS": "DENY",
    # Cross-Site Scripting
    "X-Content-Security-Policy": "default-src 'self'",
}


def handler(
    event: dict, context: Any, function: Callable, is_raise_exception: bool = True
):
    """S3やSNS等から呼ばれる際の処理

    Args:
        event (dict): イベント
        context (Any): lambdaコンテキスト
        function (Callable): 関数
        is_raise_exception (bool, optional): 例外発生時にエラーとして終了するか. Defaults to True.
    """

    try:
        # ログ出力
        event_json: str = json.dumps(event, ensure_ascii=False)
        logger.write_lambda_event(event_json)

        return function(event, context)

    except Exception as e:
        logger.write_error(traceback.format_exc())
        if is_raise_exception:
            raise e


def api_handler(
    event: dict,
    context: Any,
    function: Callable,
    is_convert_event: bool = True,
    is_gzip_compress: bool = False,
    gzip_compress_encoding: str = "utf-8",
):
    try:
        # ログ出力
        event_json: str = json.dumps(event, ensure_ascii=False)
        logger.write_lambda_event(event_json)

        return function(event, context)

    except ApplicationError as e:
        # status code 290
        body = {"message": e.get_message()}
        logger.write_error(json.dumps(body, ensure_ascii=False))
        return create_result(
            STATUS_CODE_APPLICATION_ERROR,
            body=body,
            is_gzip_compress=is_gzip_compress,
            gzip_compress_encoding=gzip_compress_encoding,
        )

    except FatalError as e:
        # status code 500
        body = {"message": e.get_message()}
        logger.write_error(json.dumps(body, ensure_ascii=False))
        return create_result(
            STATUS_CODE_FATAL_ERROR,
            body=body,
            is_gzip_compress=is_gzip_compress,
            gzip_compress_encoding=gzip_compress_encoding,
        )

    except Exception:
        # status code 500
        logger.write_error(traceback.format_exc())
        return create_result(
            STATUS_CODE_FATAL_ERROR,
            is_gzip_compress=is_gzip_compress,
            gzip_compress_encoding=gzip_compress_encoding,
        )


def create_result(
    status: int = STATUS_CODE_SUCCESS,
    headers: dict = {},
    body: dict = {},
    is_gzip_compress: bool = False,
    gzip_compress_encoding: str = "utf-8",
) -> dict:
    return_headers: dict = {}
    return_body: str = ""
    try:
        # ヘッダー
        return_headers = DEFAULT_HEADERS.copy()
        return_headers.update(headers)

        # bodyをjsonに変換
        body_json = json.dumps(body, ensure_ascii=False, default=default)
        if is_gzip_compress:
            # 圧縮
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb") as f:
                f.write(body_json.encode(gzip_compress_encoding))
            buf.seek(0)
            value = base64.b64encode(buf.read())
            return_body = value.decode(gzip_compress_encoding)
        else:
            return_body = body_json

    except Exception:
        print(traceback.format_exc())
        body = {}

    finally:
        res = {"statusCode": status, "headers": return_headers, "body": return_body}
        json_res = json.dumps(res, ensure_ascii=False)
        logger.write_lambda_result(json_res)
        return res


def default(obj: object):
    if isinstance(obj, datetime):
        return obj.strftime(DATETIME_FORMAT)
    if isinstance(obj, date):
        return obj.strftime(DATE_FORMAT)
