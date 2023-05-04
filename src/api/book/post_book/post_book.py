#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback

from common.aws.lambda_handler import api_handler, create_result
from common.error.application_error import ApplicationError
from common.pynamodb.models.Book import Book
from common.python.logger import Logger

logger = Logger()

API_NAME = "post_book"


def process(event, context):
    body = event.get("body", {})

    check_parameters(body)
    id = post_book(body)

    res: dict = {"id": id}
    return create_result(body=res)


def check_parameters(body: dict):
    """パラメータチェック"""

    if (title := body.get("title")) == "Error 1":
        raise NgTitleError([f"[{title}]"])


def post_book(body: dict) -> str:
    try:
        book = Book(
            title=body["title"],
            author=body["author"],
            publisher=body["publisher"],
            published_date=body["publishedDate"],
            isbn=body["isbn"],
            cover_image_url=body["coverImageUrl"],
            updated_user=API_NAME,
        )

        book.save()
        return book.id

    except Exception as e:
        logger.write_error(traceback.format_exc())
        raise e


def lambda_handler(event: dict, context: dict):
    return api_handler(event, context, process)


class NgTitleError(ApplicationError):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args):
        super().__init__("NgTitleError", *args)
