---
title: Fail-Safe
summary: Fail-Safe 是指旨在从对象存储中恢复丢失或被意外删除数据的机制。
---

# Fail-Safe

Fail-Safe 是指旨在从对象存储中恢复丢失或被意外删除数据的机制。

- 存储兼容性：目前，Fail-Safe 仅支持与 S3 兼容的存储类型。
- 存储桶版本控制：要使 Fail-Safe 生效，必须启用存储桶版本控制。请注意，在启用版本控制之前创建的数据*无法*通过此方法恢复。

## 实现 Fail-Safe {#implementing-fail-safe}

{{{ .lake }}} 提供了 [SYSTEM$FUSE_AMEND](/tidb-cloud-lake/sql/system-fuse-amend.md) 表函数来启用 Fail-Safe 恢复。该函数允许你在启用存储桶版本控制时，从与 S3 兼容的存储桶中恢复数据。

## 使用示例 {#usage-example}

下面通过一个分步示例说明如何使用 [SYSTEM$FUSE_AMEND](/tidb-cloud-lake/sql/system-fuse-amend.md) 函数从 S3 恢复表数据：

1. 为存储桶 `lake-doc` 启用版本控制。

2. 创建一个外部表，并将表数据存储在 `lake-doc` 存储桶中的 `fail-safe` 文件夹下。

    ```sql
    CREATE TABLE t(a INT)
    's3://lake-doc/fail-safe/'
    CONNECTION = (access_key_id ='<your-access-key-id>' secret_access_key ='<your-secret-accesskey>');

    -- Insert sample data
    INSERT INTO t VALUES (1), (2), (3);
    ```

    如果你现在打开存储桶中的 `fail-safe` 文件夹，就可以看到数据已经存在。

3. 删除 `fail-safe` 文件夹中的所有子文件夹及其文件，以模拟数据丢失。

4. 删除后尝试查询该表会返回错误：

    ```sql
    SELECT * FROM t;

    error: APIError: ResponseError with 3001: NotFound (persistent) at read, context: { uri: https://s3.us-east-2.amazonaws.com/lake-doc/fail-safe/1/1502/_b/3f84d636dc6c40508720d1cde20d4f3b_v2.parquet, response: Parts { status: 404, version: HTTP/1.1, headers: {"x-amz-request-id": "FYSJNZX1X16T91HN", "x-amz-id-2": "EI+NQjyRlSk8jlU64EASKodjvOkzuAlhZ1CYo0nIenzOH6DP7t6mMWh7raj4mUiOxW18NQesxmA=", "x-amz-delete-marker": "true", "x-amz-version-id": "ngecunzFP0pir0ysXlbR_eJafaTPl1oh", "content-type": "application/xml", "transfer-encoding": "chunked", "date": "Mon, 09 Sep 2024 02:01:57 GMT", "server": "AmazonS3"} }, service: s3, path: 1/1502/_b/3f84d636dc6c40508720d1cde20d4f3b_v2.parquet, range: 4-47 } => S3Error { code: "NoSuchKey", message: "The specified key does not exist.", resource: "", request_id: "FYSJNZX1X16T91HN" }
    ```

5. 使用 system$fuse_amend 恢复表数据：

    ```sql
    CALL system$fuse_amend('default', 't');

    -[ RECORD 1 ]-----------------------------------
    result: Ok
    ```

6. 验证表数据已恢复：

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