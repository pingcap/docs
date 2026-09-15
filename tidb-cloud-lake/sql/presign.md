---
title: PRESIGN
summary: 根据你提供的 stage 名称和文件路径，为 stage 中的文件生成预签名 URL。预签名 URL 使你能够通过 Web 浏览器或 API 请求访问该文件。
---

# PRESIGN

根据你提供的 stage 名称和文件路径，为 stage 中的文件生成预签名 URL。预签名 URL 使你能够通过 Web 浏览器或 API 请求访问该文件。

> **Tip:**
>
> 使用 cURL 与非 S3-like 存储交互时，请记得包含由 PRESIGN 命令生成的 headers，以便安全地上传或下载文件。例如：
>
> ```bash
> curl -H "<header-generated-by-presign>" -o books.csv <presigned-url>
>
> curl -X PUT -T books.csv -H "<header-generated-by-presign>" <presigned-url>
> ```

另请参阅：

- [LIST STAGE FILES](/tidb-cloud-lake/sql/list-stage-files.md)：列出 stage 中的文件。
- [REMOVE STAGE FILES](/tidb-cloud-lake/sql/remove-stage-files.md)：删除 stage 中的文件。

## 语法 {#syntax}

```sql
PRESIGN [ { DOWNLOAD | UPLOAD }] @<stage_name>/.../<file_name> [ EXPIRE = <expire_in_seconds> ]
```

其中：

`[ { DOWNLOAD | UPLOAD }]`：指定预签名 URL 用于下载还是上传。默认值为 `DOWNLOAD`。

`[ EXPIRE = <expire_in_seconds> ]`：指定预签名 URL 过期前的时长（以秒为单位）。默认值为 3,600 秒。

## 示例 {#examples}

### 生成并使用用于下载的预签名 URL {#generating-and-using-pre-signed-urls-for-download}

以下示例为 stage `my-stage` 上的文件 `books.csv` 生成用于下载的预签名 URL：

```sql
PRESIGN @my_stage/books.csv
+--------+---------+---------------------------------------------------------------------------------+
| method | headers | url                                                                             |
+--------+---------+---------------------------------------------------------------------------------+
| GET    | {}      | https://example.s3.amazonaws.com/books.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&... |
+--------+---------+---------------------------------------------------------------------------------+
```

以下示例与前一个示例作用相同：

```sql
PRESIGN DOWNLOAD @my_stage/books.csv
```

要使用预签名 URL 下载文件并将其保存为 `books.csv`，执行以下命令：

```bash
curl <presigned-url> -o books.csv
```

以下示例生成一个在 7,200 秒（2 小时）后过期的预签名 URL：

```sql
PRESIGN @my_stage/books.csv EXPIRE = 7200
```

### 生成并使用用于上传的预签名 URL {#generating-and-using-pre-signed-urls-for-upload}

以下示例生成一个预签名 URL，用于将文件以上传为 `books.csv` 的方式上传到 stage `my_stage`：

```sql
PRESIGN UPLOAD @my_stage/books.csv
```

要使用预签名 URL 上传文件 `books.csv`，执行以下命令：

```bash
curl -X PUT -T books.csv <presigned-url>
```