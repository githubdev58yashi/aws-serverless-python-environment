import argparse

import boto3

s3 = boto3.client('s3')

# ダウンロードbucket
DEFAULT_BUCKET = '20202303-mylearning'

# ダウンロードするファイル
DEFAULT_DOWNLOAD_FILENAME = 'test0321_1.txt'

# ローカル
DEFAULT_LOCAL_FOLDER = './download'
DEFAULT_LOCAL_FILE_PATH = f'{DEFAULT_LOCAL_FOLDER}/{DEFAULT_DOWNLOAD_FILENAME}'

# ダウンロードするS3のファイルパス
DEFAULT_DOWNLOAD_FOLDER = 'upload'
DEFAULT_DOWNLOAD_FILE_PATH = f'{DEFAULT_DOWNLOAD_FOLDER}/{DEFAULT_DOWNLOAD_FILENAME}'

# 暗号化キー
DEFAULT_ENCRYPTION_KEY = ''


def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", type=str, default=DEFAULT_BUCKET)
    parser.add_argument("--localFilePath", type=str, default=DEFAULT_LOCAL_FILE_PATH)
    parser.add_argument("--downloadFilePath", type=str, default=DEFAULT_DOWNLOAD_FILE_PATH)
    parser.add_argument("--key", type=str, default=DEFAULT_ENCRYPTION_KEY)
    args = parser.parse_args()

    return args


def main(bucket: str, local_file_path: str, download_file_path: str, encryption_key: str):
    """S3からファイルをダウンロードする

    ■コマンド例
    python s3_file_downloader.py
    python s3_file_downloader.py --bucket xxxx --localFilePath xxxx --uploadFilePath xxx --key xxx
    """

    params = {
        'Bucket': bucket,
        'Key': download_file_path,
        'Filename': local_file_path
    }

    if encryption_key:
        params['SSECustomerAlgorithm'] = 'AES256'
        params['SSECustomerKey'] = encryption_key

    res = s3.download_file(**params)
    print(res)


if __name__ == '__main__':
    args = parse()
    main(args.bucket, args.localFilePath, args.downloadFilePath, args.key)
