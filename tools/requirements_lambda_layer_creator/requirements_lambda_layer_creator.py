import os

BASE_DIR = "/home/user/project1-back/"
REQ_TXT = f"{BASE_DIR}/requirements.txt"
REQ_LAMBDA_LAYER_TXT = f"{BASE_DIR}/requirements_python_layer.txt"
REQ_EXCLUDE_TXT = f"{BASE_DIR}/requirements_exclude.txt"


def main():
    """lambda layerに追加するライブラリのみが記述されたrequirements_python_layer.txtを作成"""
    # requirements.txt
    with open(REQ_TXT) as f:
        requirements = set(f.read().splitlines())

    # requirements_lambda_layer_exclude.txt
    with open(REQ_EXCLUDE_TXT) as f:
        requirements_exclude = set(f.read().splitlines())

    # 差分のみを出力
    with open(REQ_LAMBDA_LAYER_TXT, "w") as f:
        for req in requirements.difference(requirements_exclude):
            f.write(req + os.linesep)

    print("作成が完了しました。")


if __name__ == "__main__":
    main()
