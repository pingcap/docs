---
title: ticloud import start local
summary: The reference of `ticloud import start local`.
---

# ticloud インポート開始ローカル {#ticloud-import-start-local}

ローカル ファイルをTiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターにインポートします。

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

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                   | 説明                      | 必要  | ノート                                  |
| -------------------- | ----------------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスタID                  | はい  | 非対話モードでのみ機能します。                      |
| --データ形式文字列           | データ形式（現在`CSV`のみ対応）      | はい  | 非対話モードでのみ機能します。                      |
| -h, --help           | このコマンドのヘルプ情報            | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。 |
| -p, --project-id 文字列 | プロジェクト ID               | はい  | 非対話モードでのみ機能します。                      |
| -- ターゲット データベース文字列   | データのインポート先のターゲット データベース | はい  | 非対話モードでのみ機能します。                      |
| -- 対象テーブル文字列         | データのインポート先のターゲット テーブル   | はい  | 非対話モードでのみ機能します。                      |

## 継承されたフラグ {#inherited-flags}

| 国旗                    | 説明                                                                               | 必要  | ノート                                                             |
| --------------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --バックスラッシュエスケープ       | フィールド内のバックスラッシュを CSV ファイルのエスケープ文字 (デフォルトでは`true` ) として解析します                      | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |
| --区切り文字列              | CSV ファイルの引用に使用する区切り文字を指定します (デフォルトでは`"` )。                                       | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |
| --無色                  | 出力の色を無効にします                                                                      | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列       | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |
| --区切り文字列              | CSV ファイルのフィールド セパレータを指定します (デフォルトでは`,` )。                                        | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |
| --trim-last-separator | 区切り記号を行末記号として扱い、CSV ファイルの末尾のすべての区切り記号を削除します                                      | いいえ | `--data-format CSV`が指定されている場合、非対話モードでのみ機能します。                   |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
