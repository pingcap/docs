---
title: ticloud serverless audit-log filter-rule list
summary: ticloud serverless audit-log filter-rule list` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールリスト {#ticloud-serverless-audit-log-filter-rule-list}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターの監査ログ フィルター ルールを一覧表示します。

```shell
ticloud serverless audit-log filter-rule list [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud serverless audit-log filter list [flags]
```

## 例 {#examples}

対話モードですべての監査ログ フィルタ ルールを一覧表示します。

```shell
ticloud serverless audit-log filter list
```

非対話型モードですべての監査ログ フィルタ ルールを一覧表示します。

```shell
ticloud serverless audit-log filter list -c <cluster-id>
```

非対話型モードで JSON 形式のすべての監査ログ フィルター ルールを一覧表示します。

```shell
ticloud serverless audit-log filter list -c <cluster-id> -o json
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                                                                                | 必須  | 注記                       |
| -------------------- | --------------------------------------------------------------------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列 | 監査ログ フィルタ ルールを一覧表示するクラスターの ID。                                                    | いいえ | 非対話型モードでのみ動作します。         |
| -o, --出力文字列          | 出力形式を指定します（デフォルトは`human` ）。有効な値は`human`または`json`です。完全な結果を得るには、 `json`形式を使用してください。 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
