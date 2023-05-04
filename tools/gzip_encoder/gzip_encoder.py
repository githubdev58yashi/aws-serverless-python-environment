#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import base64
import gzip

MODE_ENCODE = "encode"
MODE_DECODE = "decode"
ENCODING = "utf-8"


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=str)
    parser.add_argument("--mode", choices=[MODE_ENCODE, MODE_DECODE], default="encode")
    args = parser.parse_args()

    return args


def main(text: str, mode: str):
    if mode == MODE_ENCODE:
        result = gzip_encode(text)
    elif mode == MODE_DECODE:
        result = gzip_decode(text)

    return result


def gzip_encode(text: str) -> str:
    input_bytes = text.encode(ENCODING)
    gzip_bytes = gzip.compress(input_bytes)
    base64_bytes = base64.b64encode(gzip_bytes)
    output_text = base64_bytes.decode(ENCODING)

    return output_text


def gzip_decode(text: str) -> str:
    input_bytes = text.encode(ENCODING)
    base64_bytes = base64.b64decode(input_bytes)
    output_bytes = gzip.decompress(base64_bytes)
    output_text = output_bytes.decode(ENCODING)

    return output_text


if __name__ == "__main__":
    args = parse()
    result = main(args.text, args.mode)
    print(result)
