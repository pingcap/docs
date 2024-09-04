---
title: ticloud serverless export create
summary: The reference of `ticloud serverless export create`.
---

# ticloud serverless export create

Export data from a TiDB Serverless cluster:

```shell
ticloud serverless export create [flags]
```

## Examples

Export data from a TiDB Serverless cluster in interactive mode:

```shell
ticloud serverless export create
```

Export data from a TiDB Serverless cluster to local storage in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --database <database>
```

Export data from a TiDB Serverless cluster to Amazon S3 in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --s3.bucket-uri <bucket-uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                          | Description                                                                                            | Required | Note                                                 |
|-------------------------------|--------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string       | Specifies the ID of the cluster, from which you want to export data.                                             | Yes      | Only works in non-interactive mode.                  |
| --file-type string            | Specifies the format of the exported file. The supported formats include `CSV` and `SQL`. The default value is `SQL`.                                          | No       | Only works in non-interactive mode.                  |
| --database string             | Specifies the database from which you want to export data. The default value is `*`. This flag is required when you export data to local storage.                                                    | No       | Only works in non-interactive mode.                  |
| --table string                | Specifies the table from which you want to export data. The default value is `*`.                                                         | No       | Only works in non-interactive mode.                  |
| --target-type string          | Specifies the exported location. The supported location includes `LOCAL` and `S3`. The default value is `LOCAL`.                                           | No       | Only works in non-interactive mode.                  |
| --s3.bucket-uri string        | Specifies the bucket URI of the S3. This flag is required when you export data to Amazon S3.                                              | No       | Only works in non-interactive mode.                  |
| --s3.access-key-id string     | Specifies the access key ID of the S3 bucket. This flag is required when you export data to Amazon S3.                                    | NO       | Only works in non-interactive mode.                  |
| --s3.secret-access-key string | Specifies the secret access key of the S3 bucket. This flag is required when you export data to Amazon S3.                                | No       | Only works in non-interactive mode.                  |
| --compression string          | Specifies the compression algorithm of the export file. The supported algorithms include `GZIP`, `SNAPPY`, `ZSTD`, and `NONE`. The default value is `GZIP`. | No       | Only works in non-interactive mode.                  |
| -h, --help                    | Shows help information for this command.                                                                     | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
