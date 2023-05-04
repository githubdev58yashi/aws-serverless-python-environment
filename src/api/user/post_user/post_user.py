#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.aws.lambda_handler import api_handler, create_result
from common.python.logger import Logger

logger = Logger()

API_NAME = "post_user"


def process(event, context):
    # TODO: ===== debugpy start =====
    import debugpy

    debugpy.listen(5678)
    print("debugpy wait for client")
    debugpy.wait_for_client()
    debugpy.breakpoint()
    # TODO: ===== debugpy end =====

    return create_result(body={})


def lambda_handler(event: dict, context: dict):
    api_handler(event, context, process)
