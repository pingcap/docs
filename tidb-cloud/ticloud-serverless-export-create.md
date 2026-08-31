---
title: ticloud serverless export create
summary: ticloud serverless export create` のリファレンス。
---

# ticloud serverless export create {#ticloud-serverless-export-create}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターからデータをエクスポートします。

```shell
ticloud serverless export create [flags]
```

## 例 {#examples}

対話モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスターからデータをエクスポートします。

```shell
ticloud serverless export create
```

非対話型モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスターからローカルファイルにデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --filter <database.table>
```

非対話型モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスターから Amazon S3 にデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter <database.table>
```

非対話型モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスタから Google Cloud Storage にデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter <database.table>
```

非対話型モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスターから Azure Blob Storage にデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --azblob.uri <uri> --azblob.sas-token <sas-token> --filter <database.table>
```

TiDB Cloud Starter またはTiDB Cloud Essential クラスターから Alibaba Cloud OSS に非対話型モードでデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter <database.table>
```

データを Parquet ファイルにエクスポートし、非対話型モードで`SNAPPY`で圧縮します。

```shell
ticloud serverless export create -c <cluster-id> --file-type parquet --parquet.compression SNAPPY --filter <database.table>
```

非対話型モードで SQL文を使用してデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --sql 'select * from database.table'
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                         | 説明                                                                                                                        | 必須  | 注記                       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --- | ------------------------ |
| -c, --cluster-id string        | データをエクスポートするクラスターの ID を指定します。                                                                                             | はい  | 非対話型モードでのみ動作します。         |
| --file-type string         | エクスポートファイルの種類を指定します。["SQL" "CSV" "PARQUET"]のいずれかです。(デフォルトは"CSV")                  | いいえ | 非対話型モードでのみ動作します。         |
| --target-type string           | エクスポート先を指定します。[ `"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"` `"OSS"` ]のいずれかです。デフォルト値は`"LOCAL"`です。                              | いいえ | 非対話型モードでのみ動作します。         |
| --s3.uri string                | S3 URIを`s3://<bucket>/<file-path>`形式で指定します。ターゲットタイプがS3の場合は必須です。                                                           | いいえ | 非対話型モードでのみ動作します。         |
| --s3.access-key-id string            | Amazon S3のアクセスキーIDを指定します。s3.role-arnと[s3.access-key-id、s3.secret-access-key]のいずれか1つだけを設定する必要があります。                        | いいえ | 非対話型モードでのみ動作します。         |
| --s3.secret-access-key string  | Amazon S3のシークレットアクセスキーを指定します。s3.role-arnと[s3.access-key-id, s3.secret-access-key]のいずれか1つだけを設定する必要があります。                   | いいえ | 非対話型モードでのみ動作します。         |
| --s3.role-arn string           | Amazon S3のロールARNを指定します。s3.role-arnと[s3.access-key-id、s3.secret-access-key]のいずれか1つだけを設定する必要があります。                          | いいえ | 非対話型モードでのみ動作します。         |
| --gcs.uri string               | GCS URIを`gcs://<bucket>/<file-path>`形式で指定します。ターゲットタイプがGCSの場合は必須です。                                                        | いいえ | 非対話型モードでのみ動作します。         |
| --gcs.service-account-key string        | GCS の base64 でエンコードされたサービスアカウント キーを指定します。                                                                                | いいえ | 非対話型モードでのみ動作します。         |
| --azblob.uri string            | Azure BLOB URI を`azure://<account>.blob.core.windows.net/<container>/<file-path>`形式で指定します。ターゲット タイプが AZURE_BLOB の場合に必須です。 | いいえ | 非対話型モードでのみ動作します。         |
| --azblob.sas-token string      | Azure Blob の SAS トークンを指定します。                                                                                              | いいえ | 非対話型モードでのみ動作します。         |
| --oss.uri string               | Alibaba Cloud OSS URIを`oss://<bucket>/<file-path>`形式で指定します。エクスポート`target-type`が`"OSS"`の場合に必須です。                            | いいえ | 非対話型モードでのみ動作します。         |
| --oss.access-key-id string     | Alibaba Cloud OSS にアクセスするための AccessKey ID を指定します。                                                                         | いいえ | 非対話型モードでのみ動作します。         |
| --oss.access-key-secret string | Alibaba Cloud OSS にアクセスするための AccessKey シークレットを指定します。                                                                      | いいえ | 非対話型モードでのみ動作します。         |
| --csv.delimiter string          | CSV ファイル内の文字列型変数の区切り文字を指定します。(デフォルトは """)                                                                  | いいえ | 非対話型モードでのみ動作します。         |
| --csv.null-value string              | CSV ファイル内の null 値の表現を指定します。(デフォルトは "\N")                                                                        | いいえ | 非対話型モードでのみ動作します。         |
| --csv.separator string         | CSV ファイル内の各値の区切り文字を指定します。(デフォルトは ",")                                                                           | いいえ | 非対話型モードでのみ動作します。         |
| --csv.skip-header              | ヘッダーなしでテーブルの CSV ファイルをエクスポートします。                                                                                          | いいえ | 非対話型モードでのみ動作します。         |
| --parquet.compression string   | Parquet圧縮アルゴリズムを指定します。[ `"GZIP"` `"SNAPPY"` `"ZSTD"` `"NONE"` ]のいずれかです。デフォルト値は`"ZSTD"`です。                                 | いいえ | 非対話型モードでのみ動作します。         |
| --filter strings                 | エクスポートするテーブルをテーブルフィルタパターンで指定します。--sql と同時に使用しないでください。詳細については、 [テーブルフィルター](/table-filter.md)を参照してください。                      | いいえ | 非対話型モードでのみ動作します。         |
| --sql string                   | `SQL SELECT`文を使用してエクスポートされたデータをフィルターします。                                                                            | いいえ | 非対話型モードでのみ動作します。         |
| --where string                       | エクスポートされたテーブルを`WHERE`条件でフィルタリングします。--sqlと同時に使用しないでください。                                                                   | いいえ | 非対話型モードでのみ動作します。         |
| --compression string                     | エクスポートファイルの圧縮アルゴリズムを指定します。サポートされているアルゴリズムは`GZIP` 、 `SNAPPY` 、 `ZSTD` 、 `NONE`です。デフォルト値は`GZIP`です。                          | いいえ | 非対話型モードでのみ動作します。         |
|  --force                    | 確認なしでエクスポートタスクを作成します。非対話型モードでクラスター全体をエクスポートする場合は、確認が必要です。                                                                 | いいえ | 非対話型モードでのみ動作します。         |
| -h, --help                  | このコマンドのヘルプ情報を表示します。                                                                                                       | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --no-color             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile string | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
