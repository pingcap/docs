---
title: ticloud serverless import list
summary: ticloud serverless import list` のリファレンス。
---

# ticloud サーバーレス インポート リスト {#ticloud-serverless-import-list}

データインポートタスクを一覧表示します:

```shell
ticloud serverless import list [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud serverless import ls [flags]
```

## 例 {#examples}

インタラクティブ モードでインポート タスクを一覧表示します。

```shell
ticloud serverless import list
```

非対話モードでインポート タスクを一覧表示します。

```shell
ticloud serverless import list --cluster-id <cluster-id>
```

指定されたクラスターのインポート タスクを JSON 形式で一覧表示します。

```shell
ticloud serverless import list --cluster-id <cluster-id> --output json
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                  | 説明                                                                              | 必須  | 注記                       |
| -------------------- | ------------------------------------------------------------------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID を指定します。                                                               | はい  | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                             | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -o, --出力文字列          | 出力形式を指定します (デフォルトは`human` )。有効な値は`human`または`json`です。完全な結果を得るには、 `json`形式を使用します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |
| -D、--デバッグ         | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
