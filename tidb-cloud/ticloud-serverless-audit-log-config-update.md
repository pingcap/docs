---
title: ticloud serverless audit-log config update
summary: The reference of `ticloud serverless audit-log config update`.
---

# ticloud serverless audit-log config update

Update the database audit logging configuration for a TiDB Cloud Essential cluster.

```shell
ticloud serverless audit-log config update [flags]
```

## Examples

Configure database audit logging in interactive mode:

```shell
ticloud serverless audit-log config update
```

Unredact the database audit log in non-interactive mode:

```shell
ticloud serverless audit-log config update -c <cluster-id> --unredacted
```

Enable database audit logging with S3 Cloud Storage in non-interactive mode:

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-uri> --s3.access-key-id <s3-access-key-id> --s3.secret-access-key <s3-secret-access-key>
```

Configure database audit logging rotation strategy in non-interactive mode:

```shell
ticloud serverless audit-log config update -c <cluster-id> --rotation-interval-minutes <rotation-interval-minutes> --rotation-size-mib <rotation-size-mib>
```

Disable database audit logging in non-interactive mode:

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled=false
```

## Flags

| Flag | Description | Required | Note |
|------|-------------|----------|------|
| --azblob.sas-token string | The SAS token of Azure Blob. | No | Only works in non-interactive mode. |
| --azblob.uri string | The Azure Blob URI in `azure://<account>.blob.core.windows.net/<container>/<path>` format. | No | Only works in non-interactive mode. |
| --cloud-storage string | The cloud storage. One of [`"TIDB_CLOUD"`, `"S3"`, `"GCS"`, `"AZURE_BLOB"`, `"OSS"`]. | No | Only works in non-interactive mode. |
| -c, --cluster-id string | The ID of the cluster to be updated. | Yes | Only works in non-interactive mode. |
| --enabled | Enable or disable database audit logging. | No | Only works in non-interactive mode. |
| --gcs.service-account-key string | The base64 encoded service account key of GCS. | No | Only works in non-interactive mode. |
| --gcs.uri string | The GCS URI in `gs://<bucket>/<path>` format. | No | Only works in non-interactive mode. |
| --oss.access-key-id string | The access key ID of the OSS. | No | Only works in non-interactive mode. |
| --oss.access-key-secret string | The access key secret of the OSS. | No | Only works in non-interactive mode. |
| --oss.uri string | The OSS URI in `oss://<bucket>/<path>` format. | No | Only works in non-interactive mode. |
| --rotation-interval-minutes int32 | The rotation interval in minutes, range [10, 1440]. | No | Only works in non-interactive mode. |
| --rotation-size-mib int32 | The rotation size in MiB, range [1, 1024]. | No | Only works in non-interactive mode. |
| --s3.access-key-id string | The access key ID of S3. You only need to set one of the `s3.role-arn` and [`s3.access-key-id`, `s3.secret-access-key`]. | No | Only works in non-interactive mode. |
| --s3.role-arn string | The role ARN of S3. You only need to set one of the `s3.role-arn` and [`s3.access-key-id`, `s3.secret-access-key`]. | No | Only works in non-interactive mode. |
| --s3.secret-access-key string | The secret access key of S3. You only need to set one of the `s3.role-arn` and [`s3.access-key-id`, `s3.secret-access-key`]. | No | Only works in non-interactive mode. |
| --s3.uri string | The S3 URI in `s3://<bucket>/<path>` format. | No | Only works in non-interactive mode. |
| --unredacted | Unredact or redact the database audit log. | No | Only works in non-interactive mode. |
| -h, --help | Shows help information for this command. | No | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag | Description | Required | Note |
|------|-------------|----------|------|
| -D, --debug | Enable debug mode. | No | Works in both interactive and non-interactive modes. |
| --no-color | Disable color output. | No | Only works in non-interactive mode. |
| -P, --profile string | Profile to use from your configuration file. | No | Works in both interactive and non-interactive modes. |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.