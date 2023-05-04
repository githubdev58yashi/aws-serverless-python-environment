import json

import boto3

s3 = boto3.client("s3")

# アップロード先bucket
BUCKET = "20202303-mylearning"


def main():
    """dic配下のファイルをs3にアップロードする"""
    with open("./target.json") as f:
        target = json.load(f)

    target_folder_path = target.get("targetFolderPath", "")
    target_filenames = target.get("targetFileNames", [])

    upload_files(target_folder_path, target_filenames)


def upload_files(target_folder_path: str, target_filenames: list[str]):
    for target_filename in target_filenames:
        local_file_path = f"{target_folder_path}{target_filename}"
        upload_file_path = f"dic/{target_filename}"

        params = {
            "Bucket": BUCKET,
            "Key": upload_file_path,
            "Filename": local_file_path,
        }
        print(f"{local_file_path} => {upload_file_path}")
        s3.upload_file(**params)


if __name__ == "__main__":
    main()
