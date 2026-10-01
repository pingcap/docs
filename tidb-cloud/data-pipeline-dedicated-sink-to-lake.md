---
title: Sink to TiDB Cloud Lake
summary: 在 TiDB Cloud Dedicated 集群上使用 Dumpling 和 changefeed 构建 TiDB Cloud Lake Data Pipeline 的手动配置指南。
---

# Sink to TiDB Cloud Lake

本文档将指导你完成从 TiDB Cloud Dedicated 集群到 TiDB Cloud Lake 的端到端 Data Pipeline 配置：使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 将完整快照导出到 Amazon S3，创建一个 [Changefeed](/tidb-cloud/changefeed-overview.md) 持续将增量变更写入同一 S3 位置，并配置 TiDB Cloud Lake 以加载快照和增量数据。

## 限制 {#restrictions}

- TiDB Cloud Lake 的计算集群必须与 {{{ .dedicated }}} 集群位于**同一 Region**。
- 只有带有**主键**的表才能进行增量复制。
- 要创建云存储 changefeed，你的 {{{ .dedicated }}} 集群必须运行 v7.1.1 或更高版本。更多信息，参见[Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。
- 该 Data Pipeline 需要手动配置和维护 AWS IAM 资源与凭证、changefeed 以及 TiDB Cloud Lake 集成。
- 有关 DDL、DML 和列类型支持的更多信息，参见 [TiDB Cloud Lake 的 Data Pipeline SQL 兼容性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md)。

## 前提条件 {#prerequisites}

开始之前，请确保你已具备以下条件：

- 一个 {{{ .dedicated }}} 集群。请记下其部署所在的 Region。
- 运行 Dumpling 的机器能够连接到你的集群。你可以使用公网连接、VPC peering 或 private endpoint。本文以公网连接为例。
- 一个可以读取源表的 SQL 用户。本文以 `root` 为例。所需权限请参见 [Required privileges](https://docs.pingcap.com/tidb/stable/dumpling-overview#required-privileges)。
- 一个与 {{{ .dedicated }}} 集群位于同一 Region 的 Amazon S3 存储桶（例如 `s3://my-datapipeline-bucket`）。
- 一个与 {{{ .dedicated }}} 集群位于同一 Region 的 TiDB Cloud Lake 计算集群。

> **Note:**
>
> 本文假设你的源 TiDB 数据库中已经有需要复制的数据。如果你需要示例数据，请先准备好再继续。

## 第 1 步：准备 S3 存储桶访问 {#step-1-prepare-s3-bucket-access}

Data Pipeline 的各个组件（Dumpling、changefeed 和 TiDB Cloud Lake）都需要访问同一个 S3 存储桶。请为目标 S3 存储桶创建一个具有所需权限的 IAM 用户，为该用户创建 access key，并在这三个组件中使用同一个 access key。

1. 打开 [IAM Console](https://console.aws.amazon.com/iam/)，创建一个 IAM 用户（例如 `tidb-cloud-datapipeline-user`）。
2. 为该用户附加以下权限策略。将 `<your-bucket-name>` 和 `<your-prefix>` 替换为你的实际值：

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketAccess",
          "Effect": "Allow",
          "Action": [
            "s3:ListBucket",
            "s3:GetBucketLocation"
          ],
          "Resource": "arn:aws:s3:::<your-bucket-name>"
        },
        {
          "Sid": "S3ObjectAccess",
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:GetObjectVersion",
            "s3:DeleteObjectVersion"
          ],
          "Resource": "arn:aws:s3:::<your-bucket-name>/<your-prefix>/*"
        }
      ]
    }
    ```

3. 为该用户创建一个 access key，并记录 **Access Key ID** 和 **Secret Access Key**。在导出快照、创建 changefeed 和配置 TiDB Cloud Lake 时都需要用到它们。

> **Note:**
>
> 本文使用 access key 访问 S3 存储桶。changefeed 也支持 Role ARN。更多信息，参见 [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md#step-1-configure-destination)。

## 第 2 步：使用 Dumpling 导出完整快照 {#step-2-export-a-full-snapshot-with-dumpling}

TiDB Cloud Dedicated 不在 TiDB Cloud 控制台中提供导出功能，因此需要使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 导出完整快照。

### 1. 准备网络和 SQL 用户 {#1-prepare-the-network-and-sql-user}

1. 确保运行 Dumpling 的机器可以访问你的 {{{ .dedicated }}} 集群。本文使用公网连接。如果你使用公网连接，请将该机器的 IP 地址添加到集群的 IP 访问列表中。更多信息，参见 [通过公共连接接入 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md) 和 [配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。
2. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入集群概览页面并点击 **Connect**，记录连接的 host 和 port。你需要在 Dumpling 命令中使用它们。
3. 准备一个具有 Dumpling 所需权限的 SQL 用户。本文以 `root` 为例。如果你想改用专用用户，请为其授予 [Dumpling 所需的权限](https://docs.pingcap.com/tidb/stable/dumpling-overview#required-privileges)。

### 2. 使用 Dumpling 导出快照 {#2-export-the-snapshot-with-dumpling}

在一台能够连接到 {{{ .dedicated }}} 集群的机器上运行 Dumpling。通过 `-o` URI 中的 `access-key` 和 `secret-access-key` 参数传入 AWS access key：

```shell
tiup dumpling \
  -h "<host>" \
  -P <port> \
  -u "<username>" \
  -p "<password>" \
  --filetype csv \
  --csv-output-dialect snowflake \
  --escape-backslash=false \
  -o "s3://<bucket>/<prefix>/snapshot/?access-key=<access-key-id>&secret-access-key=<secret-access-key>" \
  --s3.region "<region>"
```

参数说明：

- `--filetype csv` 配合 `--csv-output-dialect snowflake`：以 **Snowflake** 方言的 CSV 格式导出数据。
- `--escape-backslash=false`：禁用反斜杠转义。
- 默认不启用压缩。
- `-o` 和 `--s3.region`：将导出的文件写入你的 S3 存储桶。`-o` URI 中的 `access-key` 和 `secret-access-key` 参数用于提供访问该存储桶的凭证。

> **Note:**
>
> 如果你的 secret access key 包含 URI 特殊字符，例如 `+`、`/` 或 `=`，请先对其进行 URL 编码。或者，你也可以设置 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY` 环境变量，或使用 `~/.aws/credentials` 文件，并从 `-o` URI 中省略 `access-key` 和 `secret-access-key` 参数。

导出成功完成后，命令输出中会包含一个 JSON 摘要。请在输出中找到 `SessionParams.tidb_snapshot` 字段，并记录其值。该值就是**快照 TSO**，创建 changefeed 时需要使用它，以便增量复制从已导出的快照位置继续进行。

## 第 3 步：为增量数据创建 changefeed {#step-3-create-a-changefeed-for-incremental-data}

在 TiDB Cloud 控制台中，你可以为 TiDB Cloud Dedicated 集群创建一个云存储 changefeed。完整步骤请参见 [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。配置 changefeed 时，请注意以下设置：

- **S3 URI**：使用与快照相同前缀下的 `incremental/` 子路径，例如 `s3://<bucket>/<prefix>/incremental/`。
- **Bucket Access**：选择 **AWS Access Key**，并输入[第 1 步：准备 S3 存储桶访问](#step-1-prepare-s3-bucket-access)中的 access key。请确保权限覆盖 `incremental/` 路径。
- **Start Replication Position**：选择 **Start replication from a specific TSO**，并输入你在[第 2 步：使用 Dumpling 导出完整快照](#step-2-export-a-full-snapshot-with-dumpling)中记录的快照 TSO。
- **Data Format**：选择 **Canal-JSON**，并同时启用 **Enable TiDB Extension** 和 **Enable Canal Content Compatibility**。这些设置会生成与 TiDB Cloud Lake 集成兼容的数据格式。

## 第 4 步：配置 TiDB Cloud Lake {#step-4-configure-tidb-cloud-lake}

在 TiDB Cloud Lake 中，你需要创建一个数据源和一个集成，以从 S3 存储桶加载数据。

### 1. 创建数据源 {#1-create-a-data-source}

1. 在 [TiDB Cloud Lake console](https://lake.tidbcloud.com/) 中，进入 **Data > Data Sources > Create**。
2. 选择 **Service: TiDB**。
3. 选择 access key 认证方式，并填写：
    - **Access Key ID** 和 **Secret Access Key**：使用[第 1 步：准备 S3 存储桶访问](#step-1-prepare-s3-bucket-access)中的凭证。
    - **S3 Bucket Name**：仅填写存储桶名称（例如 `my-datapipeline-bucket`，而不是完整 URI）。
    - **S3 Region**：与 {{{ .dedicated }}} 集群相同的 Region。
4. **SQS Queue URL** 为可选项。如果你想启用事件驱动摄取，请设置一个 SQS 队列、配置 S3 存储桶通知，并为 IAM 用户授予所需的 SQS 权限。更多信息，参见 [Amazon SQS and S3 IAM Role for TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/amazon-sqs-s3-iam-role/)。

### 2. 创建集成 {#2-create-an-integration}

1. 在 [TiDB Cloud Lake console](https://lake.tidbcloud.com/) 中，进入 **Data > Integration > Create**。
2. 填写以下字段：
    - **Data Source**：选择上面创建的数据源。
    - **Name**：为该集成任务指定一个名称。
    - **Sync Mode**：选择 `Snapshot + CDC`，先加载完整快照，再持续应用增量变更。
    - **Table Rules**：填写 `*.*` 以同步所有已导出的表。
    - **Changefeed S3 Prefix**：`<prefix>/incremental/`。
    - **Dumpling S3 Prefix**：`<prefix>/snapshot/`。
    - **Poll Interval**：TiDB Cloud Lake 扫描外部 stage 以发现新数据的时间间隔。默认值为 60 秒。更短的间隔可以降低数据延时，但会增加 TiDB Cloud Lake 托管成本。
    - **Merge Interval**：TiDB Cloud Lake 将增量数据合并到计算集群中的时间间隔。默认值为 30 秒。更短的间隔可以降低数据延时，但会增加 TiDB Cloud Lake 托管成本。
    - **Warehouse**：选择目标计算集群。
3. 点击 **Create**。
4. 创建完成后，该集成默认处于 **Stopped** 状态。点击集成操作按钮 > **Start** 开始加载数据。

## 另请参阅 {#see-also}

- 有关 DDL、DML 和列类型支持的更多信息，参见 [TiDB Cloud Lake 的 Data Pipeline SQL 兼容性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md)。