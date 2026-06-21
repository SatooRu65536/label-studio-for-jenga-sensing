# Label Studio for Jenga Sensing
ジェンガセンシングのラベリング用リポジトリ

# セットアップ
venv 環境の構築

```shell
python -m venv .venv
```

インタープリターの設定
VSCode上で `Command / Ctrl + shift + p` を押して `>Python: インタープリターを選択` を選択．
`.venv (3.xx) ./.venv/bin/python` を選択．

# 実行
## Label Studio の起動
```shell
python ./scripts/run.py
```
起動前にラベリングデータが生成されます．
すでにファイルが存在する場合はスキップされます．
- data/[parent_folder]/[child_folder]/[]...]/heartbeat_converted.csv
- data/[parent_folder]-[child_folder]-[...].json

その後，Label Studio とデータ配信用 Flask サーバが起動されます．

## ラベリングデータの生成
強制的に再生成されます．

```shell
python ./scripts/prepare_labeling_data.py
```
