---
title: Uploading to Stage
summary: "{{{ .lake }}} recommends two file upload methods for stages PRESIGN and PUT/GET commands. These methods enable direct data transfer between the client and your storage, eliminating intermediaries and resulting in cost savings by reducing traffic between {{{ .lake }}} and your storage."
---

# Uploading to Stage

{{{ .lake }}} recommends two file upload methods for stages: [PRESIGN](/tidb-cloud-lake/sql/presign.md) and PUT/GET commands. These methods enable direct data transfer between the client and your storage, eliminating intermediaries and resulting in cost savings by reducing traffic between {{{ .lake }}} and your storage.

![Uploading to Stage](/media/tidb-cloud-lake/staging-file.png)

The PRESIGN method generates a time-limited URL with a signature, which clients can use to securely initiate file uploads. This URL grants temporary access to the designated stage, allowing clients to directly transfer data without relying on {{{ .lake }}} servers for the entire process, enhancing both security and efficiency.

If you're using [BendSQL](/tidb-cloud-lake/guides/connect-using-bendsql.md) to manage files in a stage, you can use the PUT command for uploading files and the GET command for downloading files.

- The GET command currently can only download all files in a stage, not individual ones.
- These commands are exclusive to BendSQL and the GET command will not function when {{{ .lake }}} uses the file system as the storage backend.

## Uploading with Presigned URL

The following examples demonstrate how to upload a sample file ([books.parquet](https://datafuse-1253727613.cos.ap-hongkong.myqcloud.com/data/books.parquet)) to the user stage, an internal stage, and an external stage with presigned URLs.

<SimpleTab groupId="presign">

<div label="Upload to User Stage" value="user">

```sql
PRESIGN UPLOAD @~/books.parquet;
```

Result:

```
┌────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Name   │ Value                                                                                                              │
├────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ method │ PUT                                                                                                                │
│ headers│ {"host":"s3.us-east-2.amazonaws.com"}                                                                              │
│ url    │ https://s3.us-east-2.amazonaws.com/databend-toronto/stage/user/root/books.parquet?X-Amz-Algorithm...               │
└────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```shell
curl -X PUT -T books.parquet "https://s3.us-east-2.amazonaws.com/databend-toronto/stage/user/root/books.parquet?X-Amz-Algorithm=... ...
```

Check the staged file:

```sql
LIST @~;
```

Result:

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

Result:

```
┌─────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Name    │ Value                                                                                                                                                                                                                                                                                                                                                                                                                               │
├─────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ method  │ PUT                                                                                                                                                                                                                                                                                                                                                                                                                                 │
│ headers │ {"host":"s3.us-east-2.amazonaws.com"}                                                                                                                                                                                                                                                                                                                                                                                               │
│ url     │ https://s3.us-east-2.amazonaws.com/databend-toronto/stage/internal/my_internal_stage/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASTQNLUZWP2UY2HSN%2F20230628%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230628T022951Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=9cfcdf3b3554280211f88629d60358c6d6e6a5e49cd83146f1daea7dfe37f5c1 │
└─────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```shell
curl -X PUT -T books.parquet "https://s3.us-east-2.amazonaws.com/databend-toronto/stage/internal/my_internal_stage/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASTQNLUZWP2UY2HSN%2F20230628%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230628T022951Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=9cfcdf3b3554280211f88629d60358c6d6e6a5e49cd83146f1daea7dfe37f5c1"
```

Check the staged file:

```sql
LIST @my_internal_stage;
```

Result:

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
URL = 's3://databend'
CONNECTION = (
    ENDPOINT_URL = 'http://127.0.0.1:9000',
    ACCESS_KEY_ID = 'ROOTUSER',
    SECRET_ACCESS_KEY = 'CHANGEME123'
);
```

```sql
PRESIGN UPLOAD @my_external_stage/books.parquet;
```

Result:

```
┌─────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Name    │ Value                                                                                                                                                                                                                                                                                                                             │
├─────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ method  │ PUT                                                                                                                                                                                                                                                                                                                               │
│ headers │ {"host":"127.0.0.1:9000"}                                                                                                                                                                                                                                                                                                         │
│ url     │ http://127.0.0.1:9000/databend/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ROOTUSER%2F20230628%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230628T040959Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=<signature...>                                                │
└─────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```shell
curl -X PUT -T books.parquet "http://127.0.0.1:9000/databend/books.parquet?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ROOTUSER%2F20230628%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230628T040959Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=<signature...>"
```

Check the staged file:

```sql
LIST @my_external_stage;
```

Result:

```
┌───────────────┬──────┬──────────────────────────────────────┬─────────────────────────────────┬─────────┐
│ name          │ size │ md5                                  │ last_modified                  │ creator │
├───────────────┼──────┼──────────────────────────────────────┼─────────────────────────────────┼─────────┤
│ books.parquet │  998 │ "88432bf90aadb79073682988b39d461c"    │ 2023-06-28 04:13:15.178 +0000  │         │
└───────────────┴──────┴──────────────────────────────────────┴─────────────────────────────────┴─────────┘
```

</div>
</SimpleTab>

### Uploading with PUT Command

The following examples demonstrate how to use BendSQL to upload a sample file ([books.parquet](https://datafuse-1253727613.cos.ap-hongkong.myqcloud.com/data/books.parquet)) to the user stage, an internal stage, and an external stage with the PUT command.

<SimpleTab groupId="PUT">

<div label="Upload to User Stage" value="user">

```sql
PUT fs:///Users/eric/Documents/books.parquet @~
```

Result:

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

Check the staged file:

```sql
LIST @~;
```

Result:

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

Result:

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

Check the staged file:

```sql
LIST @my_internal_stage;
```

Result:

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
    URL = 's3://databend'
    CONNECTION = (
        ENDPOINT_URL = 'http://127.0.0.1:9000',
        ACCESS_KEY_ID = 'ROOTUSER',
        SECRET_ACCESS_KEY = 'CHANGEME123'
    );
```

```sql
PUT fs:///Users/eric/Documents/books.parquet @my_external_stage
```

Result:

```
┌───────────────────────────────────────────────┐
│                 file                │  status │
├─────────────────────────────────────┼─────────┤
│ /Users/eric/Documents/books.parquet │ SUCCESS │
└───────────────────────────────────────────────┘
```

Check the staged file:

```sql
LIST @my_external_stage;
```

Result:

```
┌──────────────────────────────────────────────────────────────────────┐
│         name         │ ··· │     last_modified    │      creator     │
├──────────────────────┼─────┼──────────────────────┼──────────────────┤
│ books.parquet        │ ... │ 2023-09-04 03:37:... │ NULL             │
└──────────────────────────────────────────────────────────────────────┘
```

</div>
</SimpleTab>

### Uploading a Directory with PUT Command

You can also upload multiple files from a directory using the PUT command with wildcards. This is useful when you need to stage a large number of files at once.

```sql
PUT fs:///home/ubuntu/datas/event_data/*.parquet @your_stage;
```

Result:

```
┌───────────────────────────────────────────────────────┐
│                 file                        │status   │
├─────────────────────────────────────────────┼─────────┤
│ /home/ubuntu/datas/event_data/file1.parquet │ SUCCESS │
│ /home/ubuntu/datas/event_data/file2.parquet │ SUCCESS │
│ /home/ubuntu/datas/event_data/file3.parquet │ SUCCESS │
└───────────────────────────────────────────────────────┘
```

### Downloading with GET Command

The following examples demonstrate how to use BendSQL to download a sample file ([books.parquet](https://datafuse-1253727613.cos.ap-hongkong.myqcloud.com/data/books.parquet)) from the user stage, an internal stage, and an external stage with the GET command.

<SimpleTab groupId="GET">

<div label="Download from User Stage" value="user">

```sql
LIST @~;
```

Result:

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

Result:

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

Result:

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

Result:

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

Result:

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

Result:

```
┌─────────────────────────────────────────────────────────┐
│                      file                     │  status │
├───────────────────────────────────────────────┼─────────┤
│ /Users/eric/Downloads/fromStage/books.parquet │ SUCCESS │
└─────────────────────────────────────────────────────────┘
```

</div>
</SimpleTab>
