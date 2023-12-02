---
title: ticloud import start s3
summary: The reference of `ticloud import start s3`.
---

# ticloud インポート開始 s3 {#ticloud-import-start-s3}

Amazon S3 からTiDB Cloudにファイルをインポートします。

```shell
ticloud import start s3 [flags]
```

> **注記：**
>
> Amazon S3 からTiDB Cloudにファイルをインポートする前に、 TiDB Cloudの Amazon S3 バケット アクセスを設定し、ロール ARN を取得する必要があります。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

## 例 {#examples}

対話モードでインポート タスクを開始します。

```shell
ticloud import start s3
```

非対話モードでインポート タスクを開始します。

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format <data-format> --source-url <source-url>
```

カスタム CSV 形式でインポート タスクを開始します。

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format CSV --source-url <source-url> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                 | 説明                                                                     | 必須  | 注記                                           |
| ------------------- | ---------------------------------------------------------------------- | --- | -------------------------------------------- |
| --aws-role-arn 文字列  | Amazon S3 データソースへのアクセスに使用される AWS ロール ARN を指定します。                       | はい  | 非対話モードでのみ動作します。                              |
| --バックスラッシュ-エスケープ    | フィールド内のバックスラッシュを CSV ファイルのエスケープ文字として解析するかどうか。デフォルト値は`true`です。          | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。 |
| -c、--cluster-id 文字列 | クラスターIDを指定します。                                                         | はい  | 非対話モードでのみ動作します。                              |
| --データ形式文字列          | データ形式を指定します。有効な値は`CSV` 、 `SqlFile` 、 `Parquet` 、または`AuroraSnapshot`です。 | はい  | 非対話モードでのみ動作します。                              |
| --区切り文字列            | CSVファイルの引用符に使用する区切り文字を指定します。デフォルト値は`"`です。                              | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。 |
| -h, --help          | このコマンドのヘルプ情報を表示します。                                                    | いいえ | 非対話型モードと対話型モードの両方で動作します。                     |
| -p、--プロジェクトID文字列    | プロジェクトIDを指定します。                                                        | はい  | 非対話モードでのみ動作します。                              |
| --区切り文字列            | CSV ファイルのフィールド区切り文字を指定します。デフォルト値は`,`です。                                | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。 |
| --source-url 文字列    | ソース データ ファイルが保存されている S3 パス。                                            | はい  | 非対話モードでのみ動作します。                              |
| --最後の区切り文字をトリミング    | CSV ファイルの区切り文字を行終端文字として扱い、末尾の区切り文字をすべてトリミングするかどうか。デフォルト値は`false`です。    | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                 |
| -------------- | -------------------------------------------------------------------------------- | --- | ------------------------------------------------------------------ |
| --色なし          | 出力のカラーを無効にします                                                                    | いいえ | 非対話型モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                           |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
