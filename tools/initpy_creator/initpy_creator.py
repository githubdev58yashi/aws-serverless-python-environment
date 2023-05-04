import json
import traceback
from pathlib import Path

# 設定ファイルのパス
config_file = "config.json"


def main():
    # 設定の読み込み
    with open(config_file, "r") as f:
        config = json.load(f)

    # 対象ディレクトリ
    target_dirs = [
        Path(config["base_dir"]) / target_dir for target_dir in config["target_dirs"]
    ]
    # 除外フォルダ
    exclude_folders = [Path(target_dir) for target_dir in config["exclude_folders"]]
    # 除外ディレクトリ
    exclude_dirs = [
        Path(config["base_dir"]) / target_dir for target_dir in config["exclude_dirs"]
    ]

    for target_dir in target_dirs:
        process_dir(target_dir, exclude_folders, exclude_dirs)


def process_dir(base_dir: Path, exclude_folders: list[Path], exclude_dirs: list[Path]):
    """対象ディレクトリを再帰的に走査し、__init__.pyを作成する

    【作成対象外】
    ・すでに__init__.pyが作成済みの場合は作成対象外
    ・exclude_foldersに設定されたフォルダは作成対象外
    ・exclude_dirsに設定されたパスは作成対象外
    """

    try:
        exclude_folder_names = [folder.name for folder in exclude_folders]

        for target in base_dir.glob("**/*"):
            parent_dir = target.parent
            parent_dir_name = target.parent.name

            # 作成対象外のディレクトリ
            if parent_dir_name in exclude_folder_names:
                continue

            # 作成対象外のパス
            if any(parent_dir == exclude_dir for exclude_dir in exclude_dirs):
                continue

            # すでに__init__.pyが存在する場合は作成対象外
            if (parent_dir / "__init__.py").exists():
                continue

            print(f"作成:f{parent_dir}")
            (parent_dir / "__init__.py").touch()

    except Exception:
        print(f"作成時にエラーが発生。 f{base_dir}")
        print(traceback.format_exc())


main()
if __name__ == "__main__":
    main()
