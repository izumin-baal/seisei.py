# Config Generator v2
## 利用方法
### 初期設定
- Pythonの仮想環境の作成
> python -m venv .venv

- Pythonの仮想環境の有効化
> source .venv/bin/active

- パッケージのダウンロード
> pip install -r requirements.txt


### ディレクトリ構造
| ディレクトリ | 説明 |
|-------------|------|
| output | 生成されたファイルが出力される |
| backup | 生成する際に同じ名前のファイルが存在する場合はbackupに保存される |
| parameter | パラメータを保管する |
| templates | テンプレートファイルを保管する |
