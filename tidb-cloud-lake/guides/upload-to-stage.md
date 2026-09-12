---
title: 上传到 Stage
summary: "{{{ .lake }}} 推荐对 stage 使用两种文件上传方法：PRESIGN 和 PUT/GET 命令。这些方法支持客户端与你的存储之间直接传输数据，无需中间环节，并通过减少 {{{ .lake }}} 与你的存储之间的流量来节省成本。"
---

# 上传到 Stage

{{{ .lake }}} 推荐对 stage 使用两种文件上传方法：[PRESIGN](/tidb-cloud-lake/sql/presign.md) 和 PUT/GET 命令。这些方法支持客户端与你的存储之间直接传输数据，无需中间环节，并通过减少 {{{ .lake }}} 与你的存储之间的流量来节省成本。

![Uploading to Stage](/media/tidb-cloud-lake/staging-file.png)

PRESIGN 方法会生成一个带签名且有时间限制的 URL，客户端可以使用该 URL 安全地发起文件上传。此 URL 会授予对指定 stage 的临时访问权限，使客户端能够直接传输数据，而无需在整个过程中依赖 {{{ .lake }}} 服务器，从而同时提升安全性和效率。

如果你使用 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) 管理 stage 中的文件，可以使用 PUT 命令上传文件，使用 GET 命令下载文件。

- GET 命令当前只能下载 stage 中的所有文件，不能下载单个文件。
- 这些命令仅适用于 LakeSQL；当 {{{ .lake }}} 使用文件系统作为存储后端时，GET 命令将无法工作。

## 使用预签名 URL 上传 {#uploading-with-presigned-url}

以下示例演示如何使用预签名 URL 将示例文件 ([books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet)) 上传到用户 stage、内部 stage 和外部 stage。

<SimpleTab groupId="presign">

<div label="Upload to User Stage" value="user">

```sql
PRESIGN UPLOAD @~/books.parquet;
```

结果：

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

检查已暂存的文件：

```sql
LIST @~;
```

结果：

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

结果：

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

检查已暂存的文件：

```sql
LIST @my_internal_stage;
```

结果：

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

结果：

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

检查已暂存的文件：

```sql
LIST @my_external_stage;
```

结果：

```
┌───────────────┬──────┬──────────────────────────────────────┬─────────────────────────────────┬─────────┐
│ name          │ size │ md5                                  │ last_modified                  │ creator │
├───────────────┼──────┼──────────────────────────────────────┼─────────────────────────────────┼─────────┤
│ books.parquet │  998 │ "88432bf90aadb79073682988b39d461c"    │ 2023-06-28 04:13:15.178 +0000  │         │
└───────────────┴──────┴──────────────────────────────────────┴─────────────────────────────────┴─────────┘
```

</div>
</SimpleTab>

### 使用 PUT 命令上传 {#uploading-with-put-command}

以下示例演示了如何使用 LakeSQL 通过 PUT 命令将示例文件（[books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet)）上传到用户 stage、内部 stage 和外部 stage。

<SimpleTab groupId="PUT">

<div label="Upload to User Stage" value="user">

```sql
PUT fs:///Users/eric/Documents/books.parquet @~
```

结果：

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

检查已暂存的文件：

```sql
LIST @~;
```

结果：

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

结果：

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

检查已暂存的文件：

```sql
LIST @my_internal_stage;
```

结果：

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

结果：

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

检查已暂存的文件：

```sql
LIST @my_external_stage;
```

结果：

```
┌──────────────────────────────────────────────────────────────────────┐
│         name         │ ··· │     last_modified    │      creator     │
├──────────────────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet        │ ... │ 2023-09-04 03:37:... │ NULL             │
└──────────────────────────────────────────────────────────────────────┘
```

</div>
</SimpleTab>

### 使用 PUT 命令上传目录 {#uploading-a-directory-with-put-command}

你还可以在 PUT 命令中使用通配符，从一个目录上传多个文件。当你需要一次性将大量文件暂存到 stage 时，这种方式非常有用。

```sql
PUT fs:///home/ubuntu/datas/event_data/*.parquet @your_stage;
```

结果：

```
┌───────────────────────────────────────────────────────┐
│                 file                        │status   │
├─────────────────────────────────────────────┼─────────┤
│ /home/ubuntu/datas/event_data/file1.parquet │ SUCCESS │
│ /home/ubuntu/datas/event_data/file2.parquet │ SUCCESS │
│ /home/ubuntu/datas/event_data/file3.parquet │ SUCCESS │
└───────────────────────────────────────────────────────┘
```

### 使用 GET 命令下载 {#downloading-with-get-command}

以下示例演示了如何使用 LakeSQL 通过 GET 命令，从用户 stage、内部 stage 和外部 stage 下载示例文件（[books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet)）。

<SimpleTab groupId="GET">

<div label="Download from User Stage" value="user">

```sql
LIST @~;
```

结果：

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

结果：

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

结果：

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

结果：

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

结果：

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

结果：

```
┌─────────────────────────────────────────────────────────┐
│                      file                     │  status │
├───────────────────────────────────────────────┼─────────┤
│ /Users/eric/Downloads/fromStage/books.parquet │ SUCCESS │
└─────────────────────────────────────────────────────────┘
```

</div>
</SimpleTab>