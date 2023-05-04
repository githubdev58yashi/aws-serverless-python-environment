# 目的
AWSを使用したAPI開発において、共通的に使用できる環境を作成することで、開発の効率化を図る

# これを使用するメリット
- コーディング関連
  - import文の自動フォーマット(isort)
  - スペルミスの可視化(code spell checker)
  - pep8への自動フォーマット(black)
  - 型チェック(mypy)
- 共通処理
  - コードの補完が効くようになります。(__init__.py)
  - 処理別にフォルダ分けをしました。
  - iniファイルからの値取得時に、型変換が出来るようにしました。
- テスト関連
  - テストを自動化できます。(pytest,pytest-conv)

# 初めに
document/インストール手順.mdを確認し、インストールを完了させてください。

# ドキュメント
「document/」の各種ファイルを参照してください。

# フォルダ構成

```
.vscode/ (VSCODEの設定ファイル)
conf/ (iniファイル)
dic/ (log_message.csvなどの定義ファイル)
document/ (説明用資料等)
logs/
src/
  api/
  common/ (共通クラス)
  tests/ (pytest用。srcと階層は合わせる)
    api/
    common/
tmp/ (一時フォルダ。.pklとかはここに配置される)
tools/ (その他ツールのフォルダ)
```

# TODO:
## document
### 終わっていないやつ

デプロイ手順

## デプロイ

### serverless Framework周り
