---
title: ticloud serverless audit-log config update
summary: "`ticloud serverless audit-log config update` 的参考文档。"
---

# ticloud serverless audit-log config update

用于更新 TiDB Cloud Essential 集群的数据库审计日志配置。

```shell
ticloud serverless audit-log config update [flags]
```

## 示例

以交互模式配置数据库审计日志：

```shell
ticloud serverless audit-log config update
```

以非交互模式取消数据库审计日志的脱敏：

```shell
ticloud serverless audit-log config update -c <cluster-id> --unredacted
```

以非交互模式启用 Amazon S3 存储的数据库审计日志：

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-uri> --s3.access-key-id <s3-access-key-id> --s3.secret-access-key <s3-secret-access-key>
```

以非交互模式配置数据库审计日志的轮转策略：

```shell
ticloud serverless audit-log config update -c <cluster-id> --rotation-interval-minutes <rotation-interval-minutes> --rotation-size-mib <rotation-size-mib>
```

以非交互模式禁用数据库审计日志：

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled=false
```

## 参数

| 参数 | 描述 | 是否必需 | 备注 |
|------|------|----------|------|
| --azblob.sas-token string | Azure Blob Storage 的 SAS token。 | 否 | 仅在非交互模式下生效。 |
| --azblob.uri string | Azure Blob Storage 的 URI，格式为 `azure://<account>.blob.core.windows.net/<container>/<path>`。 | 否 | 仅在非交互模式下生效。 |
| --cloud-storage string | 云存储服务提供商。可选值：`"TIDB_CLOUD"`、`"S3"`、`"GCS"`、`"AZURE_BLOB"` 和 `"OSS"`。 | 否 | 仅在非交互模式下生效。 |
| -c, --cluster-id string | 需要更新的集群 ID。 | 是 | 仅在非交互模式下生效。 |
| --enabled | 启用或禁用数据库审计日志。 | 否 | 仅在非交互模式下生效。 |
| --gcs.service-account-key string | Google Cloud Storage 的 Base64 编码服务账号密钥。 | 否 | 仅在非交互模式下生效。 |
| --gcs.uri string | Google Cloud Storage 的 URI，格式为 `gs://<bucket>/<path>`。 | 否 | 仅在非交互模式下生效。 |
| --oss.access-key-id string | 阿里云对象存储服务（OSS）的 Access Key ID。 | 否 | 仅在非交互模式下生效。 |
| --oss.access-key-secret string | 阿里云 OSS 的 Access Key Secret。 | 否 | 仅在非交互模式下生效。 |
| --oss.uri string | 阿里云 OSS 的 URI，格式为 `oss://<bucket>/<path>`。 | 否 | 仅在非交互模式下生效。 |
| --rotation-interval-minutes int32 | 日志轮转的时间间隔（分钟）。有效范围：[10, 1440]。 | 否 | 仅在非交互模式下生效。 |
| --rotation-size-mib int32 | 日志轮转的大小（MiB）。有效范围：[1, 1024]。 | 否 | 仅在非交互模式下生效。 |
| --s3.access-key-id string | Amazon S3 的 Access Key ID。你只需设置 `--s3.role-arn`，或同时设置 `--s3.access-key-id` 和 `--s3.secret-access-key`。 | 否 | 仅在非交互模式下生效。 |
| --s3.role-arn string | Amazon S3 的角色 ARN。你只需设置 `--s3.role-arn`，或同时设置 `--s3.access-key-id` 和 `--s3.secret-access-key`。 | 否 | 仅在非交互模式下生效。 |
| --s3.secret-access-key string | Amazon S3 的 Secret Access Key。你只需设置 `--s3.role-arn`，或同时设置 `--s3.access-key-id` 和 `--s3.secret-access-key`。 | 否 | 仅在非交互模式下生效。 |
| --s3.uri string | Amazon S3 的 URI，格式为 `s3://<bucket>/<path>`。 | 否 | 仅在非交互模式下生效。 |
| --unredacted | 取消或启用数据库审计日志的脱敏。 | 否 | 仅在非交互模式下生效。 |
| -h, --help | 显示该命令的帮助信息。 | 否 | 交互模式和非交互模式均可用。 |

## 继承参数

| 参数 | 描述 | 是否必需 | 备注 |
|------|------|----------|------|
| -D, --debug | 启用调试模式。 | 否 | 交互模式和非交互模式均可用。 |
| --no-color | 禁用彩色输出。 | 否 | 仅在非交互模式下生效。 |
| -P, --profile string | 指定要使用的配置文件中的 profile。 | 否 | 交互模式和非交互模式均可用。 |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。我们也欢迎任何贡献。