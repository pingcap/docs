---
title: ticloud import start local
summary: ticloud import start local の参照。
---

# ticloud インポート ローカル開始 {#ticloud-import-start-local}

ローカル ファイルを[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターにインポートします。

```shell
ticloud import start local <file-path> [flags]
```

> **注記：**
>
> 現在、1 つのインポート タスクにつき 1 つの CSV ファイルのみをインポートできます。

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

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                  | 説明                                                                 | 必須  | 注記                                            |
| -------------------- | ------------------------------------------------------------------ | --- | --------------------------------------------- |
| --バックスラッシュエスケープ      | CSV ファイルのフィールド内のバックスラッシュをエスケープ文字として解析するかどうか。デフォルト値は`true`です。       | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |
| -c, --cluster-id 文字列 | クラスター ID を指定します。                                                   | はい  | 非対話型モードでのみ動作します。                              |
| --データ形式文字列           | データ形式を指定します。現在サポートされているのは`CSV`のみです。                                | はい  | 非対話型モードでのみ動作します。                              |
| --区切り文字列             | CSV ファイルの引用符に使用する区切り文字を指定します。デフォルト値は`"`です。                         | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                | いいえ | 非対話型モードと対話型モードの両方で動作します。                      |
| -p, --プロジェクトID 文字列   | プロジェクト ID を指定します。                                                  | はい  | 非対話型モードでのみ動作します。                              |
| --セパレータ文字列           | CSV ファイルのフィールド区切り文字を指定します。デフォルト値は`,`です。                            | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |
| --ターゲットデータベース文字列     | データをインポートするターゲット データベースを指定します。                                     | はい  | 非対話型モードでのみ動作します。                              |
| --ターゲットテーブル文字列       | データをインポートするターゲット テーブルを指定します。                                       | はい  | 非対話型モードでのみ動作します。                              |
| --最後の区切り文字をトリムする     | 区切り文字を行末文字として扱い、CSV ファイルの末尾の区切り文字をすべてトリミングするかどうか。デフォルト値は`false`です。 | いいえ | `--data-format CSV`が指定されている場合は非対話モードでのみ機能します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------------ |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
