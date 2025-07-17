---
title: 外部存储服务的 URI 格式
summary: 了解外部存储服务的存储 URI 格式，包括 Amazon S3、GCS 和 Azure Blob Storage。
---

## 外部存储服务的 URI 格式

本文档描述了外部存储服务的 URI 格式，包括 Amazon S3、GCS 和 Azure Blob Storage。

URI 的基本格式如下：

```shell
[scheme]://[host]/[path]?[parameters]
```

## Amazon S3 URI 格式

<CustomContent platform="tidb">

- `scheme`: `s3`
- `host`: `bucket name`
- `parameters`:

    - `access-key`: 指定访问密钥。
    - `secret-access-key`: 指定秘密访问密钥。
    - `session-token`: 指定临时会话令牌。BR 从 v7.6.0 版本开始支持此参数。
    - `use-accelerate-endpoint`: 指定是否使用 Amazon S3 的加速终端节点（默认为 `false`）。
    - `endpoint`: 指定 S3 兼容服务的自定义端点 URL（例如 `<https://s3.example.com/>`）。
    - `force-path-style`: 使用路径样式访问而非虚拟托管样式（默认为 `true`）。
    - `storage-class`: 指定上传对象的存储类别（例如 `STANDARD` 或 `STANDARD_IA`）。
    - `sse`: 指定用于加密上传对象的服务器端加密算法（取值选项：空、`AES256` 或 `aws:kms`）。
    - `sse-kms-key-id`: 如果 `sse` 设置为 `aws:kms`，则指定 KMS ID。
    - `acl`: 指定上传对象的预定义访问控制列表（例如 `private` 或 `authenticated-read`）。
    - `role-arn`: 当你需要通过指定的 [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) 从第三方访问 Amazon S3 数据时，可以在 `role-arn` URL 查询参数中指定对应的 [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)，例如 `arn:aws:iam::888888888888:role/my-role`。关于使用 IAM role 从第三方访问 Amazon S3 数据的更多信息，请参见 [AWS 文档](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)。BR 从 v7.6.0 版本开始支持此参数。
    - `external-id`: 当你从第三方访问 Amazon S3 数据时，可能需要指定正确的 [external ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html) 来假设 [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)。在这种情况下，可以使用此 `external-id` URL 查询参数来指定 external ID，并确保你可以假设该 IAM role。external ID 是第三方提供的一个任意字符串，连同 IAM role ARN 一起，用于访问 Amazon S3 数据。假设 IAM role 时提供 external ID 是可选的，也就是说，如果第三方不要求 external ID，你可以在不提供此参数的情况下假设 IAM role 并访问相应的 Amazon S3 数据。

以下是 TiDB Lightning 和 BR 使用的 Amazon S3 URI 示例。在此示例中，你需要指定特定的文件路径 `testfolder`。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

以下是 TiCDC `sink-uri` 的 Amazon S3 URI 示例。

```shell
tiup cdc:v7.5.0 cli changefeed create \
    --server=http://172.16.201.18:8300 \
    --sink-uri="s3://cdc?endpoint=http://10.240.0.38:9000&access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --changefeed-id="cdcTest" \
    --config=cdc_csv.toml
```

</CustomContent>

<CustomContent platform="tidb-cloud">

- `scheme`: `s3`
- `host`: `bucket name`
- `parameters`:

    - `access-key`: 指定访问密钥。
    - `secret-access-key`: 指定秘密访问密钥。
    - `session-token`: 指定临时会话令牌。
    - `use-accelerate-endpoint`: 指定是否使用 Amazon S3 的加速终端节点（默认为 `false`）。
    - `endpoint`: 指定 S3 兼容服务的自定义端点 URL（例如 `<https://s3.example.com/>`）。
    - `force-path-style`: 使用路径样式访问而非虚拟托管样式（默认为 `true`）。
    - `storage-class`: 指定上传对象的存储类别（例如 `STANDARD` 或 `STANDARD_IA`）。
    - `sse`: 指定用于加密上传对象的服务器端加密算法（取值选项：空、`AES256` 或 `aws:kms`）。
    - `sse-kms-key-id`: 如果 `sse` 设置为 `aws:kms`，则指定 KMS ID。
    - `acl`: 指定上传对象的预定义访问控制列表（例如 `private` 或 `authenticated-read`）。
    - `role-arn`: 为了让 TiDB Cloud 使用特定的 [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) 访问 Amazon S3 数据，可以在 `role-arn` URL 查询参数中提供角色的 [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)。例如：`arn:aws:iam::888888888888:role/my-role`。

        > **Note:**
        >
        > - 若要自动创建 IAM role，可以在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中的集群“导入数据自 Amazon S3”页面，填写 **Folder URI** 字段，在 **Role ARN** 字段下点击 **Click here to create new one with AWS CloudFormation**，然后按照弹出的 **Add New Role ARN** 对话框中的指示操作。
        > - 如果在使用 AWS CloudFormation 创建 IAM role 时遇到困难，可以在 **Add New Role ARN** 对话框中点击 **click Having trouble? Create Role ARN manually**，获取 TiDB Cloud 账户 ID 和 TiDB Cloud External ID，然后按照 [Configure Amazon S3 access using a Role ARN](https://docs.pingcap.com/tidbcloud/dedicated-external-storage#configure-amazon-s3-access-using-a-role-arn) 中的步骤手动创建角色。在配置 IAM role 时，确保在 **Account ID** 字段中输入 TiDB Cloud 账户 ID，并选择 **Require external ID**，以防止 [confused deputy attacks](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)。
        > - 为了增强安全性，可以通过配置较短的 **Max session duration** 来缩短 IAM role 的有效期。更多信息请参见 AWS 文档中的 [Update the maximum session duration for a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_update-role-settings.html#id_roles_update-session-duration)。

    - `external-id`: 指定 TiDB Cloud External ID，TiDB Cloud 访问 Amazon S3 数据时需要此 ID。你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的 **Add New Role ARN** 对话框中获取此 ID。更多信息请参见 [Configure Amazon S3 access using a Role ARN](https://docs.pingcap.com/tidbcloud/dedicated-external-storage#configure-amazon-s3-access-using-a-role-arn)。

以下是 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 使用的 Amazon S3 URI 示例。此示例使用文件路径 `testfolder`。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

</CustomContent>

## GCS URI 格式

- `scheme`: `gcs` 或 `gs`
- `host`: `bucket name`
- `parameters`:

    - `credentials-file`: 指定迁移工具节点上的凭证 JSON 文件路径。
    - `storage-class`: 指定上传对象的存储类别（例如 `STANDARD` 或 `COLDLINE`）
    - `predefined-acl`: 指定上传对象的预定义访问控制列表（例如 `private` 或 `project-private`）

<CustomContent platform="tidb">

以下是 TiDB Lightning 和 BR 使用的 GCS URI 示例。在此示例中，你需要指定特定的文件路径 `testfolder`。

```shell
gcs://external/testfolder?credentials-file=${credentials-file-path}
```

</CustomContent>

以下是 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 使用的 GCS URI 示例。在此示例中，你需要指定特定的文件名 `test.csv`。

```shell
gcs://external/test.csv?credentials-file=${credentials-file-path}
```

## Azure Blob Storage URI 格式

- `scheme`: `azure` 或 `azblob`
- `host`: `container name`
- `parameters`:

    - `account-name`: 指定存储账户名。
    - `account-key`: 指定访问密钥。
    - `sas-token`: 指定共享访问签名（SAS）令牌。
    - `access-tier`: 指定上传对象的访问层，例如 `Hot`、`Cool` 或 `Archive`。默认值为存储账户的默认访问层。
    - `encryption-scope`: 指定服务器端加密的 [encryption scope](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)。
    - `encryption-key`: 指定用于服务器端加密的 [encryption key](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys)，使用 AES256 加密算法。

以下是 BR 使用的 Azure Blob Storage URI 示例。在此示例中，你需要指定特定的文件路径 `testfolder`。

```shell
azure://external/testfolder?account-name=${account-name}&account-key=${account-key}
```


请确保：
1. 保持原有的Markdown格式（标题、列表、代码块、链接等）
2. 使用专业、准确的中文术语
3. 保持文档的逻辑结构和可读性
4. 代码示例和文件名保持英文不变
5. 链接地址保持不变
6. 不要翻译 **包裹的加粗的文字**
7. 你 翻译成 “你”，而不是 “您”
8. 不要额外新增翻译内容，保证只翻译输入的内容
9. 代码块内的内容不需要翻译
10. 中文和英文之间需要加空格，中文和阿拉伯数字之间需要加空格
11. 如果你在文中发现以下 key，不需要翻译，只要将匹配的 key 替换为对应的 value 就行:
{}
