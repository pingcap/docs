---
title: Fail-Safe
summary: Fail-Safe は、オブジェクトストレージから失われた、または誤って削除されたデータのリカバリを目的とした仕組みを指します。
---

# Fail-Safe

Fail-Safe は、オブジェクトストレージから失われた、または誤って削除されたデータのリカバリを目的とした仕組みを指します。

- ストレージ互換性: 現在、Fail-Safe は S3 互換のストレージタイプのみをサポートしています。
- バケットのバージョニング: Fail-Safe を機能させるには、バケットのバージョニングを有効にする必要があります。なお、バージョニングを有効にする前に作成されたデータは、この方法ではリカバリ*できません*。

## Fail-Safe の実装 {#implementing-fail-safe}

{{{ .lake }}} は、Fail-Safe リカバリを有効にするためのテーブル関数 [SYSTEM$FUSE_AMEND](/tidb-cloud-lake/sql/system-fuse-amend.md) を提供しています。この関数を使用すると、バケットのバージョニングが有効になっている場合に、S3 互換ストレージのバケットからデータを復元できます。

## 使用例 {#usage-example}

以下は、[SYSTEM$FUSE_AMEND](/tidb-cloud-lake/sql/system-fuse-amend.md) 関数を使用して、S3 からテーブルデータをリカバリする手順の例です。

1. バケット `lake-doc` のバージョニングを有効にします。

2. 外部テーブルを作成し、テーブルデータを `lake-doc` バケット内の `fail-safe` フォルダに保存します。

    ```sql
    CREATE TABLE t(a INT)
    's3://lake-doc/fail-safe/'
    CONNECTION = (access_key_id ='<your-access-key-id>' secret_access_key ='<your-secret-accesskey>');

    -- Insert sample data
    INSERT INTO t VALUES (1), (2), (3);
    ```

    この時点でバケット内の `fail-safe` フォルダを開くと、すでにデータが存在していることを確認できます。

3. `fail-safe` フォルダ内のすべてのサブフォルダとそのファイルを削除して、データ損失をシミュレートします。

4. 削除後にテーブルをクエリしようとすると、エラーが発生します。

    ```sql
    SELECT * FROM t;

    error: APIError: ResponseError with 3001: NotFound (persistent) at read, context: { uri: https://s3.us-east-2.amazonaws.com/lake-doc/fail-safe/1/1502/_b/3f84d636dc6c40508720d1cde20d4f3b_v2.parquet, response: Parts { status: 404, version: HTTP/1.1, headers: {"x-amz-request-id": "FYSJNZX1X16T91HN", "x-amz-id-2": "EI+NQjyRlSk8jlU64EASKodjvOkzuAlhZ1CYo0nIenzOH6DP7t6mMWh7raj4mUiOxW18NQesxmA=", "x-amz-delete-marker": "true", "x-amz-version-id": "ngecunzFP0pir0ysXlbR_eJafaTPl1oh", "content-type": "application/xml", "transfer-encoding": "chunked", "date": "Mon, 09 Sep 2024 02:01:57 GMT", "server": "AmazonS3"} }, service: s3, path: 1/1502/_b/3f84d636dc6c40508720d1cde20d4f3b_v2.parquet, range: 4-47 } => S3Error { code: "NoSuchKey", message: "The specified key does not exist.", resource: "", request_id: "FYSJNZX1X16T91HN" }
    ```

5. system$fuse_amend を使用してテーブルデータをリカバリします。

    ```sql
    CALL system$fuse_amend('default', 't');

    -[ RECORD 1 ]-----------------------------------
    result: Ok
    ```

6. テーブルデータが戻っていることを確認します。

    ```sql
    SELECT * FROM t;

    ┌─────────────────┐
    │        a        │
    ├─────────────────┤
    │               1 │
    │               2 │
    │               3 │
    └─────────────────┘
    ```