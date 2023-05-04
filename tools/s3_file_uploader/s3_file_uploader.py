import argparse

import boto3

s3 = boto3.client('s3')

# アップロード先bucket
DEFAULT_BUCKET = '20202303-mylearning'

# ダウンロードするファイル
DEFAULT_UPLOAD_FILENAME = 'test0321_1.txt'

# ローカル
DEFAULT_LOCAL_FOLDER = './upload'
DEFAULT_LOCAL_FILE_PATH = f'{DEFAULT_LOCAL_FOLDER}/{DEFAULT_UPLOAD_FILENAME}'

# アップロード先
DEFAULT_UPLOAD_FOLDER = 'upload'
DEFAULT_UPLOAD_FILE_PATH = f'{DEFAULT_UPLOAD_FOLDER}/{DEFAULT_UPLOAD_FILENAME}'

# 暗号化キー
DEFAULT_ENCRYPTION_KEY = ''


def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", type=str, default=DEFAULT_BUCKET)
    parser.add_argument("--localFilePath", type=str, default=DEFAULT_LOCAL_FILE_PATH)
    parser.add_argument("--uploadFilePath", type=str, default=DEFAULT_UPLOAD_FILE_PATH)
    parser.add_argument("--key", type=str, default=DEFAULT_ENCRYPTION_KEY)
    args = parser.parse_args()

    return args


def main(bucket: str, local_file_path: str, upload_file_path: str, encryption_key: str):
    """S3にファイルをアップロードする

    ■コマンド例
    python s3_file_uploader.py
    python s3_file_uploader.py --bucket xxxx --localFilePath xxxx --uploadFilePath xxx --key xxx
    """

    params = {
        'Bucket': bucket,
        'Key': upload_file_path,
        'Filename': local_file_path
    }

    if encryption_key:
        params['SSECustomerAlgorithm'] = 'AES256'
        params['SSECustomerKey'] = encryption_key

    res = s3.upload_file(**params)
    print(res)


if __name__ == '__main__':
    args = parse()
    main(args.bucket, args.localFilePath, args.uploadFilePath, args.key)
