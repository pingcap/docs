---
title: ticloud serverless export create
summary: The reference of `ticloud serverless export create`.
---

# ticloud serverless export create

Create a serverless cluster export

```shell
ticloud serverless export create [flags]
```

## Examples

Create an export in interactive mode:

```shell
ticloud serverless export create
```

Create an export with local type in non-interactive mode:

```
ticloud serverless export create -c <cluster-id> --databsae <database> --table <table>
```

Create an export with s3 type in non-interactive mode:

```
ticloud serverless export create -c <cluster-id> --bucket-uri <bucket-uri> --access-key-id <access-key-id> --secret-access-key <secret-access-key>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                       | Description                                                                              | Required | Note                                                 |
|----------------------------|------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string    | The ID of the cluster, in which the export will be created                               | Yes      | Only works in non-interactive mode.                  |
| --file-type string         | The exported file type. One of ["CSV" "SQL"] (default "CSV")                             | No       | Only works in non-interactive mode.                  |
| --database string          | The database name you want to export (default "*")                                       | No       | Only works in non-interactive mode.                  |
| --table string             | The table name you want to export (default "*")                                          | No       | Only works in non-interactive mode.                  |
| --target-type string       | The exported Target. One of ["LOCAL" "S3"] (default "LOCAL")                             | No       | Only works in non-interactive mode.                  |
| --bucket-uri string        | The bucket URI of the S3 bucket. Required when target type is S3                         | No       | Only works in non-interactive mode.                  |
| --access-key-id string     | The access key ID of the S3 bucket. Required when target type is S3                      | NO       | Only works in non-interactive mode.                  |
| --secret-access-key string | The secret access key of the S3 bucket. Required when target type is S3                  | No       | Only works in non-interactive mode.                  |
| -h, --help                 | Help information for this command                                                        | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
