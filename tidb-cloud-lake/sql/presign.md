---
title: PRESIGN
summary: 指定した stage 名とファイルパスに基づいて、stage 上のファイル用の事前署名付き URL を生成します。事前署名付き URL を使用すると、Web ブラウザまたは API リクエストを通じてファイルにアクセスできます。
---

# PRESIGN

指定した stage 名とファイルパスに基づいて、stage 上のファイル用の事前署名付き URL を生成します。事前署名付き URL を使用すると、Web ブラウザまたは API リクエストを通じてファイルにアクセスできます。

> **Tip:**
>
> cURL を使用して S3 互換ではないストレージとやり取りする場合は、安全にファイルをアップロードまたはダウンロードするために、PRESIGN コマンドによって生成されたヘッダーを必ず含めてください。例えば、次のとおりです。
>
> ```bash
> curl -H "<header-generated-by-presign>" -o books.csv <presigned-url>
>
> curl -X PUT -T books.csv -H "<header-generated-by-presign>" <presigned-url>
> ```

関連情報:

- [LIST STAGE FILES](/tidb-cloud-lake/sql/list-stage-files.md): stage 内のファイルを一覧表示します。
- [REMOVE STAGE FILES](/tidb-cloud-lake/sql/remove-stage-files.md): stage からファイルを削除します。

## 構文 {#syntax}

```sql
PRESIGN [ { DOWNLOAD | UPLOAD }] @<stage_name>/.../<file_name> [ EXPIRE = <expire_in_seconds> ]
```

説明：

`[ { DOWNLOAD | UPLOAD }]`: 事前署名付き URL をダウンロード用またはアップロード用のどちらに使用するかを指定します。デフォルト値は `DOWNLOAD` です。

`[ EXPIRE = <expire_in_seconds> ]`: 事前署名付き URL の有効期限が切れるまでの時間（秒）を指定します。デフォルト値は 3,600 秒です。

## 例 {#examples}

### ダウンロード用の事前署名付き URL の生成と使用 {#generating-and-using-pre-signed-urls-for-download}

次の例では、stage `my-stage` 上のファイル `books.csv` をダウンロードするための事前署名付き URL を生成します。

```sql
PRESIGN @my_stage/books.csv
+--------+---------+---------------------------------------------------------------------------------+
| method | headers | url                                                                             |
+--------+---------+---------------------------------------------------------------------------------+
| GET    | {}      | https://example.s3.amazonaws.com/books.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&... |
+--------+---------+---------------------------------------------------------------------------------+
```

次の例は、前の例と同じように動作します。

```sql
PRESIGN DOWNLOAD @my_stage/books.csv
```

事前署名付き URL を使用してファイルをダウンロードし、`books.csv` として保存するには、次のコマンドを実行します。

```bash
curl <presigned-url> -o books.csv
```

次の例では、7,200 秒（2 時間）で期限切れになる事前署名付き URL を生成します。

```sql
PRESIGN @my_stage/books.csv EXPIRE = 7200
```

### アップロード用の事前署名付き URL の生成と使用 {#generating-and-using-pre-signed-urls-for-upload}

次の例では、ファイルを `books.csv` として stage `my_stage` にアップロードするための事前署名付き URL を生成します。

```sql
PRESIGN UPLOAD @my_stage/books.csv
```

事前署名付き URL を使用してファイル `books.csv` をアップロードするには、次のコマンドを実行します。

```bash
curl -X PUT -T books.csv <presigned-url>
```