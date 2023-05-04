#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback

from common.aws.lambda_handler import api_handler, create_result
from common.pynamodb.models.Book import Book
from common.python.logger import Logger

logger = Logger()

API_NAME = "get_book"


def process(event, context):
    query_string_parameters = event.get("queryStringParameters", {})
    id = query_string_parameters.get("id", "")

    book = get_book(id)

    res = book
    return create_result(body=res)


def get_book(id: str) -> dict:
    try:
        books = list(Book.query(hash_key=id))
        if not books:
            logger.write_info(f"存在しないIDを指定されました。 id:{id}")
            return {}
        return books[0].attribute_values

    except Exception as e:
        logger.write_error(traceback.format_exc())
        raise e


def lambda_handler(event: dict, context: dict):
    return api_handler(event, context, process)
