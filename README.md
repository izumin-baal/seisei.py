# Seisei.py
## 利用方法
### 初期設定
- Pythonの仮想環境の作成
> python -m venv .venv

- Pythonの仮想環境の有効化
> source .venv/bin/active

- パッケージのダウンロード
> pip install -r requirements.txt

### 必要なファイル
- template_file
- parameter_file

### 実行方法
> python seisei.py [-h] [-a] [-g] <template_file> <parameter_file>

#### オプション
- -a : 追記モード。出力をファイルに上書きせず、末尾に追記する。
- -g : グループ出力。 出力先を`./output/<group>/`にすることができる。オプションを入れるとgroup名を入力する必要がある

### ディレクトリ構造
| ディレクトリ | 説明 |
|-------------|------|
| output | 生成されたファイルが出力される |
| backup | 生成する際に同じ名前のファイルが存在する場合はbackupに保存される |
| parameter | パラメータを保管する |
| templates | テンプレートファイルを保管する |

### テンプレートファイル ###
テンプレートファイルの命名は何でも良い。

#### 構文
- 構文: `{% ... %}`  
- 変数: `{{ ... }}`
- コメント: `{# ... #}`

### パラメータについて
- 対応パラメータ形式
    - CSV
    - JSON
- パラメータは勝手に判断します
- ファイル名の末尾を確認しているため.csvまたは.jsonに変更が必要

#### JSON(例)
```json
{
    "name" : "izumin",
    "age" : 23
}
```
```json
[
    {
        "name" : "izumin",
        "age" : 23,
        "filename" : "izumin-info.txt"
    },
    {
        "name" : "satsumariko",
        "age" : 14,
        "filename" : "satsumariko-info.txt"
    }
]
```

#### CSV(例)
- 1行目のヘッダがkeyです
```csv
name,age
izumin,23
```
```csv
name,age,filename
izumin,23,izumin-info.txt
satsumariko,14,satsumariko-info.txt
```

#### 特殊なKeyについて
| Key | 形式 | 説明 |
| ----| ---- | ---- |
| filename | 文字列 | 指定したファイル名で出力します |
