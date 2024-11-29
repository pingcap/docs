---
title: ticloud serverless export create
summary: ticloud serverless export create` のリファレンス。
---

# ticloud サーバーレス エクスポート 作成 {#ticloud-serverless-export-create}

TiDB Cloud Serverless クラスターからデータをエクスポートします。

```shell
ticloud serverless export create [flags]
```

## 例 {#examples}

インタラクティブ モードでTiDB Cloud Serverless クラスターからデータをエクスポートします。

```shell
ticloud serverless export create
```

非対話型モードでTiDB Cloud Serverless クラスターからローカル ファイルにデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --filter <database.table>
```

非対話モードでTiDB Cloud Serverless クラスターから Amazon S3 にデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter <database.table>
```

非インタラクティブ モードでTiDB Cloud Serverless クラスタから Google Cloud Storage にデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter <database.table>
```

非対話型モードでTiDB Cloud Serverless クラスターから Azure Blob Storage にデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --azblob.uri <uri> --azblob.sas-token <sas-token> --filter <database.table>
```

データを Parquet ファイルにエクスポートし、非対話型モードで`SNAPPY`で圧縮します。

```shell
ticloud serverless export create -c <cluster-id> --file-type parquet --parquet.compression SNAPPY --filter <database.table>
```

非対話モードで SQL ステートメントを使用してデータをエクスポートします。

```shell
ticloud serverless export create -c <cluster-id> --sql 'select * from database.table'
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                        | 説明                                                                                                                        | 必須  | 注記                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列       | データをエクスポートするクラスターの ID を指定します。                                                                                             | はい  | 非対話型モードでのみ動作します。         |
| --ファイルタイプ文字列               | エクスポート ファイルの種類を指定します。[&quot;SQL&quot; &quot;CSV&quot; &quot;PARQUET&quot;] のいずれかです (デフォルトは &quot;CSV&quot;)               | いいえ | 非対話型モードでのみ動作します。         |
| --ターゲットタイプ文字列              | エクスポート先を指定します。[ `"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"` ] のいずれかです。デフォルト値は`"LOCAL"`です。                                     | いいえ | 非対話型モードでのみ動作します。         |
| --s3.uri 文字列               | S3 URI を`s3://<bucket>/<file-path>`形式で指定します。ターゲット タイプが S3 の場合に必須です。                                                       | いいえ | 非対話型モードでのみ動作します。         |
| --s3.アクセスキーID文字列           | Amazon S3 のアクセスキー ID を指定します。s3.role-arn と [s3.access-key-id、s3.secret-access-key] のいずれか 1 つを設定するだけで済みます。                  | いいえ | 非対話型モードでのみ動作します。         |
| --s3.secret-access-key 文字列 | Amazon S3 のシークレットアクセスキーを指定します。s3.role-arn と [s3.access-key-id、s3.secret-access-key] のいずれか 1 つを設定するだけで済みます。                | いいえ | 非対話型モードでのみ動作します。         |
| --s3.role-arn 文字列          | Amazon S3 のロール ARN を指定します。s3.role-arn と [s3.access-key-id、s3.secret-access-key] のいずれか 1 つを設定するだけで済みます。                    | いいえ | 非対話型モードでのみ動作します。         |
| --gcs.uri 文字列              | GCS URI を`gcs://<bucket>/<file-path>`形式で指定します。ターゲット タイプが GCS の場合に必須です。                                                    | いいえ | 非対話型モードでのみ動作します。         |
| --gcs.サービス アカウント キー文字列     | GCS の base64 でエンコードされたサービス アカウント キーを指定します。                                                                                | いいえ | 非対話型モードでのみ動作します。         |
| --azblob.uri 文字列           | Azure Blob URI を`azure://<account>.blob.core.windows.net/<container>/<file-path>`形式で指定します。ターゲット タイプが AZURE_BLOB の場合に必須です。 | いいえ | 非対話型モードでのみ動作します。         |
| --azblob.sas-トークン文字列       | Azure Blob の SAS トークンを指定します。                                                                                              | いいえ | 非対話型モードでのみ動作します。         |
| --csv.delimiter 文字列        | CSV ファイル内の文字列型変数の区切り文字を指定します。(デフォルトは &quot;&quot;&quot;)                                                                  | いいえ | 非対話型モードでのみ動作します。         |
| --csv.null値文字列             | CSV ファイル内の null 値の表現を指定します。(デフォルトは &quot;\N&quot;)                                                                        | いいえ | 非対話型モードでのみ動作します。         |
| --csv.separator 文字列        | CSV ファイル内の各値の区切り文字を指定します。(デフォルトは &quot;,&quot;)                                                                           | いいえ | 非対話型モードでのみ動作します。         |
| --csv.ヘッダーをスキップ            | ヘッダーなしでテーブルの CSV ファイルをエクスポートします。                                                                                          | いいえ | 非対話型モードでのみ動作します。         |
| --parquet.compression 文字列  | Parquet圧縮アルゴリズムを指定します。[ `"GZIP"` `"SNAPPY"` `"ZSTD"` `"NONE"` ]のいずれかです。デフォルト値は`"ZSTD"`です。                                 | いいえ | 非対話型モードでのみ動作します。         |
| --フィルター文字列                 | テーブル フィルタ パターンを使用してエクスポートするテーブルを指定します。--sql と一緒に使用しないでください。詳細については、 [テーブルフィルター](/table-filter.md)参照してください。                | いいえ | 非対話型モードでのみ動作します。         |
| --sql 文字列                  | `SQL SELECT`ステートメントを使用してエクスポートされたデータをフィルターします。                                                                            | いいえ | 非対話型モードでのみ動作します。         |
| --文字列                      | エクスポートされたテーブルを`WHERE`条件でフィルタリングします。--sql と一緒に使用しないでください。                                                                  | いいえ | 非対話型モードでのみ動作します。         |
| --圧縮文字列                    | エクスポート ファイルの圧縮アルゴリズムを指定します。サポートされているアルゴリズムには、 `GZIP` 、 `SNAPPY` 、 `ZSTD` 、 `NONE`があります。デフォルト値は`GZIP`です。                   | いいえ | 非対話型モードでのみ動作します。         |
|  --force                   | 確認なしでエクスポート タスクを作成します。非対話型モードでクラスター全体をエクスポートする場合は確認する必要があります。                                                             | いいえ | 非対話型モードでのみ動作します。         |
| -h, --help                 | このコマンドのヘルプ情報を表示します。                                                                                                       | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |
| -D、--デバッグ         | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
