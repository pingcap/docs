---
title: ticloud serverless import start
summary: ticloud serverless import start` のリファレンス。
aliases: ['/tidbcloud/ticloud-import-start-local','/tidbcloud/ticloud-import-start-mysql','/tidbcloud/ticloud-import-start-s3']
---

# ticloud サーバーレスインポート開始 {#ticloud-serverless-import-start}

データ インポート タスクを開始します。

```shell
ticloud serverless import start [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud serverless import create [flags]
```

> **注記：**
>
> 現在、1 つのローカル インポート タスクにつき 1 つの CSV ファイルのみをインポートできます。

## 例 {#examples}

対話モードでインポート タスクを開始します。

```shell
ticloud serverless import start
```

非対話モードでローカル インポート タスクを開始します。

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type <file-type> --local.target-database <target-database> --local.target-table <target-table>
```

カスタムアップロード同時実行でローカルインポートタスクを開始します。

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type <file-type> --local.target-database <target-database> --local.target-table <target-table> --local.concurrency 10
```

カスタム CSV 形式でローカル インポート タスクを開始します。

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type CSV --local.target-database <target-database> --local.target-table <target-table> --csv.separator \" --csv.delimiter \' --csv.backslash-escape=false --csv.trim-last-separator=true
```

非対話型モードで S3 インポート タスクを開始します。

```shell
ticloud serverless import start --source-type S3 --s3.uri <s3-uri> --cluster-id <cluster-id> --file-type <file-type> --s3.role-arn <role-arn>
```

非対話モードで GCS インポート タスクを開始します。

```shell
ticloud serverless import start --source-type GCS --gcs.uri <gcs-uri> --cluster-id <cluster-id> --file-type <file-type> --gcs.service-account-key <service-account-key>
```

非対話型モードで Azure BLOB インポート タスクを開始します。

```shell
ticloud serverless import start --source-type AZURE_BLOB --azblob.uri <azure-blob-uri> --cluster-id <cluster-id> --file-type <file-type> --azblob.sas-token <sas-token>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                         | 説明                                                                                                                   | 必須  | 注記                       |   |     |                          |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------- | --- | ------------------------ | - | --- | ------------------------ |
| --azblob.sas-トークン文字列        | Azure Blob の SAS トークンを指定します。                                                                                         | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --azblob.uri 文字列            | Azure Blob URI を`azure://<account>.blob.core.windows.net/<container>/<path>`形式で指定します。                                | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --gcs.サービス アカウント キー文字列      | GCS の base64 でエンコードされたサービス アカウント キーを指定します。                                                                           | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --gcs.uri 文字列               | GCS URI を`gcs://<bucket>/<path>`形式で指定します。ソース タイプが GCS の場合に必須です。                                                      | はい  | 非対話型モードでのみ動作します。         |   |     |                          |
| --s3.アクセスキーID文字列            | Amazon S3 のアクセスキー ID を指定します。1 と [ `s3.access-key-id` 、 `s3.secret-access-key` ] のいずれか`s3.role-arn`つだけを設定する必要があります。   | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --s3.role-arn 文字列           | Amazon S3 のロール ARN を指定します。1 と [ `s3.access-key-id` 、 `s3.secret-access-key` ] のいずれか`s3.role-arn`つだけを設定する必要があります。     | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --s3.secret-access-key 文字列  | Amazon S3 のシークレットアクセスキーを指定します。1 と [ `s3.access-key-id` 、 `s3.secret-access-key` ] のいずれか`s3.role-arn`つだけを設定する必要があります。 | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --s3.uri 文字列                | S3 URI を`s3://<bucket>/<path>`形式で指定します。ソース タイプが S3 の場合に必須です。                                                         | はい  | 非対話型モードでのみ動作します。         |   |     |                          |
| --ソースタイプ文字列                 | インポートソースの種類を [ `"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"` ] のいずれかで指定します。デフォルト値は`"LOCAL"`です。                             | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| -c, --cluster-id 文字列        | クラスター ID を指定します。                                                                                                     | はい  | 非対話型モードでのみ動作します。         |   |     |                          |
| --local.concurrency 整数      | ファイルのアップロードの同時実行性を指定します。デフォルト値は`5`です。                                                                                | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --local.file-path 文字列       | インポートするローカル ファイルのパスを指定します。                                                                                           | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --local.target-database 文字列 | データをインポートするターゲット データベースを指定します。                                                                                       | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --local.target-table 文字列    | データのインポート先のターゲット テーブルを指定します。                                                                                         | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --ファイルタイプ文字列                | インポート ファイルの種類を [&quot;CSV&quot; &quot;SQL&quot; &quot;AURORA_SNAPSHOT&quot; &quot;PARQUET&quot;] のいずれかで指定します。        | はい  | 非対話型モードでのみ動作します。         |   |     |                          |
| --csv.バックスラッシュエスケープ         | CSV ファイル内のフィールド内のバックスラッシュをエスケープ文字として解析するかどうかを指定します。デフォルト値は`true`です。                                                  | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --csv.delimiter 文字列         | CSV ファイルを引用する際に使用する区切り文字を指定します。デフォルト値は`\`です。                                                                         | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --csv.separator 文字列         | CSV ファイル内のフィールド区切り文字を指定します。デフォルト値は`,`です。                                                                             | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --csv.ヘッダーをスキップ             | CSV ファイルにヘッダー行が含まれているかどうかを指定します。                                                                                     | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --csv.trim-最後の区切り文字         | 区切り文字を行末文字として扱い、CSV ファイル内の末尾の区切り文字をすべてトリミングするかどうかを指定します。                                                             | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --csv.nullではない              | CSV ファイルに NULL 値を含めることができるかどうかを指定します。                                                                                | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| --csv.null値文字列              | CSV ファイル内の NULL 値の表現を指定します。(デフォルトは &quot;\N&quot;)                                                                   | いいえ | 非対話型モードでのみ動作します。         |   |     |                          |
| -h, --help                  | このコマンドのヘルプ情報を表示します。                                                                                                  | いいえ | 非対話型モードと対話型モードの両方で動作します。 |   | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |
| -D、--デバッグ         | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
