---
title: ticloud import start s3
summary: ticloud import start s3 のリファレンス。
---

# ticloud インポート開始 s3 {#ticloud-import-start-s3}

Amazon S3 からTiDB Cloudにファイルをインポートします。

```shell
ticloud import start s3 [flags]
```

> **注記：**
>
> Amazon S3 からTiDB Cloudにファイルをインポートする前に、 TiDB Cloudの Amazon S3 バケットアクセスを設定し、ロール ARN を取得する必要があります。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)参照してください。

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

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                  | 説明                                                                     | 必須  | 注記                                            |
| -------------------- | ---------------------------------------------------------------------- | --- | --------------------------------------------- |
| --aws-role-arn 文字列   | Amazon S3 データソースにアクセスするために使用される AWS ロール ARN を指定します。                    | はい  | 非対話型モードでのみ動作します。                              |
| --バックスラッシュエスケープ      | CSV ファイルのフィールド内のバックスラッシュをエスケープ文字として解析するかどうか。デフォルト値は`true`です。           | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |
| -c, --cluster-id 文字列 | クラスター ID を指定します。                                                       | はい  | 非対話型モードでのみ動作します。                              |
| --データ形式文字列           | データ形式を指定します。有効な値は`CSV` 、 `SqlFile` 、 `Parquet` 、または`AuroraSnapshot`です。 | はい  | 非対話型モードでのみ動作します。                              |
| --区切り文字列             | CSV ファイルの引用符に使用する区切り文字を指定します。デフォルト値は`"`です。                             | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                    | いいえ | 非対話型モードと対話型モードの両方で動作します。                      |
| -p, --プロジェクトID 文字列   | プロジェクト ID を指定します。                                                      | はい  | 非対話型モードでのみ動作します。                              |
| --セパレータ文字列           | CSV ファイルのフィールド区切り文字を指定します。デフォルト値は`,`です。                                | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |
| --source-url 文字列     | ソース データ ファイルが保存される S3 パス。                                              | はい  | 非対話型モードでのみ動作します。                              |
| --最後の区切り文字をトリムする     | 区切り文字を行末文字として扱い、CSV ファイルの末尾の区切り文字をすべてトリミングするかどうか。デフォルト値は`false`です。     | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------------ |
| --色なし             | 出力のカラーを無効にする                                                                   | いいえ | 非対話モードでのみ機能します。対話モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎いたします。
