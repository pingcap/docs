---
title: ticloud import start local
summary: The reference of `ticloud import start local`.
---

# ticloud インポートをローカルで開始 {#ticloud-import-start-local}

ローカル ファイルを[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターにインポートします。

```shell
ticloud import start local <file-path> [flags]
```

> **ノート：**
>
> 現在、1 つのインポート タスクに対して 1 つの CSV ファイルのみをインポートできます。

## 例 {#examples}

対話モードでインポート タスクを開始します。

```shell
ticloud import start local <file-path>
```

非対話モードでインポート タスクを開始します。

```shell
ticloud import start local <file-path> --project-id <project-id> --cluster-id <cluster-id> --data-format <data-format> --target-database <target-database> --target-table <target-table>
```

カスタム CSV 形式でインポート タスクを開始します。

```shell
ticloud import start local <file-path> --project-id <project-id> --cluster-id <cluster-id> --data-format CSV --target-database <target-database> --target-table <target-table> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                  | 説明                              | 必要  | ノート                      |
| ------------------- | ------------------------------- | --- | ------------------------ |
| -c、--cluster-id 文字列 | クラスタID                          | はい  | 非対話モードでのみ動作します。          |
| --データ形式文字列          | データ形式 (現在サポートされているのは`CSV`つだけです) | はい  | 非対話モードでのみ動作します。          |
| -h, --help          | このコマンドのヘルプ情報                    | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -p、--プロジェクトID文字列    | プロジェクトID                        | はい  | 非対話モードでのみ動作します。          |
| --ターゲットデータベース文字列    | データをインポートするターゲットデータベース          | はい  | 非対話モードでのみ動作します。          |
| --ターゲットテーブル文字列      | データをインポートするターゲットテーブル            | はい  | 非対話モードでのみ動作します。          |

## 継承されたフラグ {#inherited-flags}

| 国旗               | 説明                                                                                                                                       | 必要  | ノート                                                               |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --バックスラッシュ-エスケープ | フィールド内のバックスラッシュを CSV ファイルのエスケープ文字 (デフォルトでは`true` ) として解析します。                                                                             | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。                      |
| --区切り文字列         | CSV ファイルの引用符に使用する区切り文字を指定します (デフォルトでは`"` )。                                                                                              | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。                      |
| --色なし            | 出力のカラーを無効にします                                                                                                                            | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列   | このコマンドで使用されるアクティブな[<a href="/tidb-cloud/cli-reference.md#user-profile">ユーザープロフィール</a>](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |
| --区切り文字列         | CSV ファイルのフィールド区切り文字を指定します (デフォルトでは`,` )                                                                                                  | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。                      |
| --最後の区切り文字をトリミング | 区切り文字を行終端文字として扱い、CSV ファイルの末尾の区切り文字をすべてトリミングします。                                                                                          | いいえ | `--data-format CSV`が指定された場合は、非対話モードでのみ機能します。                      |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[<a href="https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose">問題</a>](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
