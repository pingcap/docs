---
title: ticloud serverless audit-log config update
summary: ticloud serverless audit-log config update` のリファレンス。
---

# ticloud serverless audit-log config update {#ticloud-serverless-audit-log-config-update}

TiDB Cloud Essential クラスターのデータベース監査ログ構成を更新します。

```shell
ticloud serverless audit-log config update [flags]
```

## 例 {#examples}

対話モードでデータベース監査ログを構成します。

```shell
ticloud serverless audit-log config update
```

非対話型モードでデータベース監査ログを編集解除します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --unredacted
```

非対話型モードで Amazon S3ストレージを使用してデータベース監査ログを有効にします。

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-uri> --s3.access-key-id <s3-access-key-id> --s3.secret-access-key <s3-secret-access-key>
```

非対話型モードでデータベース監査ログのローテーション戦略を構成します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --rotation-interval-minutes <rotation-interval-minutes> --rotation-size-mib <rotation-size-mib>
```

非対話型モードでデータベース監査ログを無効にします。

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled=false
```

## 旗 {#flags}

| フラグ                         | 説明                                                                                                           | 必須  | 注記                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ | --- | ------------------------------------ |
| --azblob.sas-token 文字列      | Azure Blob Storage の SAS トークン。                                                                               | いいえ | 非対話型モードでのみ動作します。                     |
| --azblob.uri 文字列            | `azure://<account>.blob.core.windows.net/<container>/<path>`形式の Azure Blob Storage URI。                      | いいえ | 非対話型モードでのみ動作します。                     |
| --cloud-storage              | クラウドストレージ`"GCS"` 。 `"AZURE_BLOB"` `"OSS"`オプション: `"TIDB_CLOUD"` `"S3"`                                      | いいえ | 非対話型モードでのみ動作します。                     |
| -c, --cluster-id 文字列        | 更新するクラスターの ID。                                                                                               | はい  | 非対話型モードでのみ動作します。                     |
| --enabled                        | データベース監査ログを有効または無効にします。                                                                                      | いいえ | 非対話型モードでのみ動作します。                     |
| --gcs.サービスアカウントキー文字列        | Google Cloud Storage の Base64 でエンコードされたサービス アカウント キー。                                                        | いいえ | 非対話型モードでのみ動作します。                     |
| --gcs.uri 文字列               | `gs://<bucket>/<path>`形式の Google Cloud Storage URI。                                                          | いいえ | 非対話型モードでのみ動作します。                     |
| --oss.access-key-id 文字列     | Alibaba Cloud Object Storage Service (OSS) のアクセス キー ID。                                                      | いいえ | 非対話型モードでのみ動作します。                     |
| --oss.access-key-secret 文字列 | Alibaba Cloud OSS のアクセスキーシークレット。                                                                             | いいえ | 非対話型モードでのみ動作します。                     |
| --oss.uri 文字列               | `oss://<bucket>/<path>`形式の Alibaba Cloud OSS URI。                                                            | いいえ | 非対話型モードでのみ動作します。                     |
| --rotation-interval-minutes int32             | ローテーション間隔（分）。有効な範囲： `[10, 1440]` 。                                                                           | いいえ | 非対話型モードでのみ動作します。                     |
| --rotation-size-mib int32           | 回転サイズ（MiB）。有効な範囲： `[1, 1024]` 。                                                                              | いいえ | 非対話型モードでのみ動作します。                     |
| --s3.アクセスキーID文字列            | Amazon S3のアクセスキーID。 `--s3.role-arn`のいずれか、または`--s3.access-key-id`と`--s3.secret-access-key`の両方を設定する必要があります。      | いいえ | 非対話型モードでのみ動作します。                     |
| --s3.role-arn 文字列           | Amazon S3 のロール ARN。 `--s3.role-arn`のいずれか、または`--s3.access-key-id`と`--s3.secret-access-key`の両方を設定する必要があります。      | いいえ | 非対話型モードでのみ動作します。                     |
| --s3.secret-access-key 文字列  | Amazon S3のシークレットアクセスキー。`--s3.role-arn`のいずれか、または`--s3.access-key-id`と`--s3.secret-access-key`の両方を設定する必要があります。 | いいえ | 非対話型モードでのみ動作します。                     |
| --s3.uri 文字列                | `s3://<bucket>/<path>`形式の Amazon S3 URI。                                                                     | いいえ | 非対話型モードでのみ動作します。                     |
| --unredacted                      | データベース監査ログを編集解除または編集します。                                                                                     | いいえ | 非対話型モードでのみ動作します。                     |
| -h, --help                  | このコマンドのヘルプ情報を表示します。                                                                                          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug        | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --no-color             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile 文字列 | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
