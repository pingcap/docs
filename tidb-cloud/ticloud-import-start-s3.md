---
title: ticloud import start s3
summary: The reference of `ticloud import start s3`.
---

# ticloud インポート開始 s3 {#ticloud-import-start-s3}

Amazon S3 からTiDB Cloudにファイルをインポートします。

```shell
ticloud import start s3 [flags]
```

> **ノート：**
>
> Amazon S3 からTiDB Cloudにファイルをインポートする前に、 TiDB Cloudの Amazon S3 バケット アクセスを設定し、Role ARN を取得する必要があります。詳細については、 [Amazon S3 アクセスの構成](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

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

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                   | 説明                                                               | 必要  | ノート                                  |
| -------------------- | ---------------------------------------------------------------- | --- | ------------------------------------ |
| --aws-role-arn 文字列   | AWS S3 IAMロール ARN                                                | はい  | 非対話モードでのみ機能します。                      |
| -c, --cluster-id 文字列 | クラスタID                                                           | はい  | 非対話モードでのみ機能します。                      |
| --データ形式文字列           | データ形式。有効な値は`CSV` 、 `SqlFile` 、 `Parquet` 、または`AuroraSnapshot`です。 | はい  | 非対話モードでのみ機能します。                      |
| -h, --help           | このコマンドのヘルプ情報                                                     | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。 |
| -p, --project-id 文字列 | プロジェクト ID                                                        | はい  | 非対話モードでのみ機能します。                      |
| --source-url 文字列     | ソースデータファイルが保存されている S3 パス                                         | はい  | 非対話モードでのみ機能します。                      |

## 継承されたフラグ {#inherited-flags}

| 国旗                    | 説明                                                                               | 必要  | ノート                                                             |
| --------------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --バックスラッシュエスケープ       | フィールド内のバックスラッシュを CSV ファイルのエスケープ文字 (デフォルトでは`true` ) として解析します                      | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |
| --区切り文字列              | CSV ファイルの引用に使用する区切り文字を指定します (デフォルトでは`"` )。                                       | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |
| --無色                  | 出力の色を無効にします                                                                      | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列       | このコマンドで使用されるアクティブな[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |
| --区切り文字列              | CSV ファイルのフィールド セパレータを指定します (デフォルトでは`,` )。                                        | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |
| --trim-last-separator | 区切り記号を行末記号として扱い、CSV ファイルの末尾のすべての区切り記号を削除します                                      | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
