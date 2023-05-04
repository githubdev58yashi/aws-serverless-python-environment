import json
import subprocess


def main():
    """lambda layerのzipファイルを作成する

    対象はrequirementsフォルダに入っているrequirements.txt
    target.jsonにzip名と対象のrequirements.txtの紐づけを行う。
    excludeに記載されたフォルダは除外される。
    """

    with open("./target.json") as f:
        targets = json.load(f)

    clear()

    for target in targets:
        zip_filename = target.get("zipFileName", "")
        target_filename = target.get("targetFileName", "")
        target_folder_path = target.get("targetFolderPath", "")
        excludes = target.get("exclude", [])
        create_zip(zip_filename, target_filename, target_folder_path, excludes)


def clear():
    """初期化"""

    subprocess.run(["rm", "-rf", "python"])
    # subprocess.run(["rm", "-rf", "../../lambda_layer/zip"])
    # subprocess.run(["mkdir", "../../lambda_layer/zip"])


def create_zip(
    zip_filename: str,
    target_filename: str,
    target_folder_path: str,
    excludes: list[str],
):
    """zipファイル作成"""

    # 一時フォルダ作成
    subprocess.run(["mkdir", "python"])

    if target_filename != "":
        # requirements.txtからのpip install
        target_filepath = f"./requirements/{target_filename}"
        subprocess.run(["pip", "install", "-r", target_filepath, "-t", "python"])

        # 不要なフォルダは削除
        cmd = "rm -rf python/*dist-info"
        subprocess.run(cmd, shell=True)

        # 除外対象のフォルダの削除
        for exclude in excludes:
            exclude_filepath = f"python/{exclude}"
            subprocess.run(["rm", "-rf", exclude_filepath])

    elif target_folder_path != "":
        # 対象フォルダのzip化
        # TODO: test
        subprocess.run(["ls"])
        subprocess.run(["cp", "-rf", target_folder_path, "python"])

        # 除外対象のフォルダの削除
        for exclude in excludes:
            exclude_filepath = f"python/{exclude}"
            subprocess.run(["rm", "-rf", exclude_filepath])

    # zip
    zip_filepath = f"../../lambda_layer/zip/{zip_filename}"
    subprocess.run(["zip", "-r", zip_filepath, "python", "-x", "*.pyc", "__pycache__"])

    # 一時フォルダ削除
    subprocess.run(["rm", "-rf", "python"])


if __name__ == "__main__":
    main()
