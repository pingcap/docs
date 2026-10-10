---
title: stage へのアップロード
summary: "{{{ .lake }}} では、stage に対する 2 つのファイルアップロード方法として、PRESIGN と PUT/GET コマンドを推奨しています。これらの方法により、クライアントとストレージ間でデータを直接転送できるため、中継を不要にし、{{{ .lake }}} とストレージ間のトラフィックを削減してコストを節約できます。"
---

# stage へのアップロード

{{{ .lake }}} では、stage に対する 2 つのファイルアップロード方法として、[PRESIGN](/tidb-cloud-lake/sql/presign.md) と PUT/GET コマンドを推奨しています。これらの方法により、クライアントとストレージ間でデータを直接転送できるため、中継を不要にし、{{{ .lake }}} とストレージ間のトラフィックを削減してコストを節約できます。

![stage へのアップロード](/media/tidb-cloud-lake/staging-file.png)

PRESIGN メソッドは、署名付きの有効期限付き URL を生成し、クライアントはそれを使用して安全にファイルアップロードを開始できます。この URL は指定された stage への一時的なアクセス権を付与し、クライアントが {{{ .lake }}} サーバーに処理全体を依存することなくデータを直接転送できるようにするため、セキュリティと効率の両方が向上します。

[LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用して stage 内のファイルを管理している場合は、ファイルのアップロードに PUT コマンド、ファイルのダウンロードに GET コマンドを使用できます。

- 現在、GET コマンドでダウンロードできるのは stage 内のすべてのファイルのみで、個別のファイルはダウンロードできません。
- これらのコマンドは LakeSQL 専用であり、{{{ .lake }}} がストレージバックエンドとしてファイルシステムを使用している場合、GET コマンドは機能しません。

## Presigned URL を使用したアップロード {#uploading-with-presigned-url}

以下の例では、presigned URL を使用して、サンプルファイル ([books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet)) を user stage、internal stage、および external stage にアップロードする方法を示します。

<SimpleTab groupId="presign">

<div label="Upload to User Stage" value="user">

```sql
PRESIGN UPLOAD @~/books.parquet;
```

結果:

```
┌────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Name   │ Value                                                                                                              │
├────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ method │ PUT                                                                                                                │
│ headers│ {"host":"s3.us-east-2.amazonaws.com"}                                                                              │
│ url    │ https://s3.us-east-2.amazonaws.com/lake-toronto/stage/user/root/books.parquet?X-Amz-Algorithm...               │
└────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```shell
curl -X PUT -T books.parquet "https://s3.us-east-2.amazonaws.com/lake-toronto/stage/user/root/books.parquet?X-Amz-Algorithm=... ...
```

stage にアップロードされたファイルを確認します。

```sql
LIST @~;
```

結果:

```
┌───────────────┬──────┬──────────────────────────────────────┬─────────────────────────────────┬─────────┐
│ name          │ size │ md5                                  │ last_modified                   │ creator │
├───────────────┼──────┼──────────────────────────────────────┼─────────────────────────────────┼─────────┤
│ books.parquet │  998 │ 88432bf90aadb79073682988b39d461c     │ 2023-06-27 16:03:51.000 +0000   │         │
└───────────────┴──────┴──────────────────────────────────────┴─────────────────────────────────┴─────────┘
```

</div>

<div label="Upload to Internal Stage" value="internal">

```sql
CREATE STAGE my_internal_stage;
```

```sql
PRESIGN UPLOAD @my_internal_stage/books.parquet;
```

結果:

```
┌─────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Name    │ Value                                                                                                                                                                                                                                                                                                                                                                                                                               │
├─────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ method  │ PUT                                                                                                                                                                                                                                                                                                                                                                                                                                 │
│ headers │ {"host":"s3.us-east-2.amazonaws.com"}                                                                                                                                                                                                                                                                                                                                                                                               │
│ url     │ https://s3.us-east-2.amazonaws.com/lake-toronto/stage/internal/my_internal_stage/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=<access-key-id>%2F20230628%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230628T022951Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=9cfcdf3b3554280211f88629d60358c6d6e6a5e49cd83146f1daea7dfe37f5c1 │
└─────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```shell
curl -X PUT -T books.parquet "https://s3.us-east-2.amazonaws.com/lake-toronto/stage/internal/my_internal_stage/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=<access-key-id>%2F20230628%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230628T022951Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=9cfcdf3b3554280211f88629d60358c6d6e6a5e49cd83146f1daea7dfe37f5c1"
```

stage にアップロードされたファイルを確認します。

```sql
LIST @my_internal_stage;
```

結果:

```
┌──────────────────────────────────┬───────┬──────────────────────────────────────┬─────────────────────────────────┬─────────┐
│ name                             │ size  │ md5                                  │ last_modified                  │ creator │
├──────────────────────────────────┼───────┼──────────────────────────────────────┼─────────────────────────────────┼─────────┤
│ books.parquet                    │   998 │ "88432bf90aadb79073682988b39d461c"     │ 2023-06-28 02:32:15.000 +0000  │         │
└──────────────────────────────────┴───────┴──────────────────────────────────────┴─────────────────────────────────┴─────────┘
```

</div>

<div label="Upload to External Stage" value="external">

```sql
CREATE STAGE my_external_stage
URL = 's3://lake'
CONNECTION = (
    ENDPOINT_URL = 'http://127.0.0.1:9000',
    ACCESS_KEY_ID = 'ROOTUSER',
    SECRET_ACCESS_KEY = 'CHANGEME123'
);
```

```sql
PRESIGN UPLOAD @my_external_stage/books.parquet;
```

結果:

```
┌─────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Name    │ Value                                                                                                                                                                                                                                                                                                                             │
├─────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ method  │ PUT                                                                                                                                                                                                                                                                                                                               │
│ headers │ {"host":"127.0.0.1:9000"}                                                                                                                                                                                                                                                                                                         │
│ url     │ http://127.0.0.1:9000/lake/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ROOTUSER%2F20230628%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230628T040959Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=<signature...>                                                    │
└─────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```shell
curl -X PUT -T books.parquet "http://127.0.0.1:9000/lake/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ROOTUSER%2F20230628%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230628T040959Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=<signature...>"
```

stage にアップロードされたファイルを確認します。

```sql
LIST @my_external_stage;
```

結果:

```
┌───────────────┬──────┬──────────────────────────────────────┬─────────────────────────────────┬─────────┐
│ name          │ size │ md5                                  │ last_modified                  │ creator │
├───────────────┼──────┼──────────────────────────────────────┼─────────────────────────────────┼─────────┤
│ books.parquet │  998 │ "88432bf90aadb79073682988b39d461c"    │ 2023-06-28 04:13:15.178 +0000  │         │
└───────────────┴──────┴──────────────────────────────────────┴─────────────────────────────────┴─────────┘
```

</div>
</SimpleTab>

### PUT コマンドによるアップロード {#uploading-with-put-command}

以下の例では、LakeSQL を使用して、サンプルファイル（[books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet)）を PUT コマンドで user stage、internal stage、external stage にアップロードする方法を示します。

<SimpleTab groupId="PUT">

<div label="Upload to User Stage" value="user">

```sql
PUT fs:///Users/eric/Documents/books.parquet @~
```

結果:

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

stage に配置されたファイルを確認します。

```sql
LIST @~;
```

結果:

```
┌────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │ ··· │     last_modified    │      creator     │
├───────────────┼────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet │    998 │ ... │ 2023-09-04 03:27:... │ NULL             │
└────────────────────────────────────────────────────────────────────────┘
```

</div>

<div label="Upload to Internal Stage" value="internal">

```sql
CREATE STAGE my_internal_stage;
```

```sql
PUT fs:///Users/eric/Documents/books.parquet @my_internal_stage;
```

結果:

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

stage に配置されたファイルを確認します。

```sql
LIST @my_internal_stage;
```

結果:

```
┌────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │ ··· │     last_modified    │      creator     │
├───────────────┼────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet │    998 │ ... │ 2023-09-04 03:32:... │ NULL             │
└────────────────────────────────────────────────────────────────────────┘
```

</div>

<div label="Upload to External Stage" value="external">

```
CREATE STAGE my_external_stage
    URL = 's3://lake'
    CONNECTION = (
        ENDPOINT_URL = 'http://127.0.0.1:9000',
        ACCESS_KEY_ID = 'ROOTUSER',
        SECRET_ACCESS_KEY = 'CHANGEME123'
    );
```

```sql
PUT fs:///Users/eric/Documents/books.parquet @my_external_stage
```

結果:

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

stage に配置されたファイルを確認します。

```sql
LIST @my_external_stage;
```

結果:

```
┌──────────────────────────────────────────────────────────────────────┐
│         name         │ ··· │     last_modified    │      creator     │
├──────────────────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet        │ ... │ 2023-09-04 03:37:... │ NULL             │
└──────────────────────────────────────────────────────────────────────┘
```

</div>
</SimpleTab>

### PUT コマンドによるディレクトリのアップロード {#uploading-a-directory-with-put-command}

PUT コマンドでワイルドカードを使用すると、ディレクトリ内の複数ファイルをアップロードすることもできます。これは、多数のファイルを一度に stage に配置する必要がある場合に便利です。

```sql
PUT fs:///home/ubuntu/datas/event_data/*.parquet @your_stage;
```

結果:

```
┌───────────────────────────────────────────────────────┐
│                 file                        │status   │
├─────────────────────────────────────────────┼─────────┤
│ /home/ubuntu/datas/event_data/file1.parquet │ SUCCESS │
│ /home/ubuntu/datas/event_data/file2.parquet │ SUCCESS │
│ /home/ubuntu/datas/event_data/file3.parquet │ SUCCESS │
└───────────────────────────────────────────────────────┘
```

### GET コマンドでのダウンロード {#downloading-with-get-command}

以下の例では、GET コマンドを使用して、ユーザー stage、内部 stage、および外部 stage からサンプルファイル（[books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet)）を LakeSQL でダウンロードする方法を示します。

<SimpleTab groupId="GET">

<div label="Download from User Stage" value="user">

```sql
LIST @~;
```

結果:

```
┌────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │ ··· │     last_modified    │      creator     │
├───────────────┼────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet │    998 │ ... │ 2023-09-04 03:27:... │ NULL             │
└────────────────────────────────────────────────────────────────────────┘
```

```sql
GET @~/ fs:///Users/eric/Downloads/fromStage/;
```

結果:

```
┌─────────────────────────────────────────────────────────┐
│                      file                     │  status │
├───────────────────────────────────────────────┼─────────┤
│ /Users/eric/Downloads/fromStage/books.parquet │ SUCCESS │
└─────────────────────────────────────────────────────────┘
```

</div>

<div label="Download from Internal Stage" value="internal">

```sql
LIST @my_internal_stage;
```

結果:

```
┌────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │ ··· │     last_modified    │      creator     │
├───────────────┼────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet │    998 │ ... │ 2023-09-04 03:32:... │ NULL             │
└────────────────────────────────────────────────────────────────────────┘
```

```sql
GET @my_internal_stage/ fs:///Users/eric/Downloads/fromStage/;
```

結果:

```
┌─────────────────────────────────────────────────────────┐
│                      file                     │  status │
├───────────────────────────────────────────────┼─────────┤
│ /Users/eric/Downloads/fromStage/books.parquet │ SUCCESS │
└─────────────────────────────────────────────────────────┘
```

</div>

<div label="Download from External Stage" value="external">

```sql

LIST @my_external_stage;

```

結果:

```
┌──────────────────────────────────────────────────────────────────────┐
│         name         │ ··· │     last_modified    │      creator     │
├──────────────────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet        │ ... │ 2023-09-04 03:37:... │ NULL             │
└──────────────────────────────────────────────────────────────────────┘
```

```sql
GET @my_external_stage/ fs:///Users/eric/Downloads/fromStage/;
```

結果:

```
┌─────────────────────────────────────────────────────────┐
│                      file                     │  status │
├───────────────────────────────────────────────┼─────────┤
│ /Users/eric/Downloads/fromStage/books.parquet │ SUCCESS │
└─────────────────────────────────────────────────────────┘
```

</div>
</SimpleTab>