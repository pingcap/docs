---
title: ticloud serverless audit-log filter-rule list
summary: ticloud serverless audit-log filter-rule list` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールリスト {#ticloud-serverless-audit-log-filter-rule-list}

TiDB Cloud Essential クラスターの監査ログ フィルター ルールを一覧表示します。

```shell
ticloud serverless audit-log filter-rule list [flags]
```

## 例 {#examples}

対話モードですべての監査ログ フィルタ ルールを一覧表示します。

```shell
ticloud serverless audit-log filter-rule list
```

非対話型モードですべての監査ログ フィルタ ルールを一覧表示します。

```shell
ticloud serverless audit-log filter-rule list -c <cluster-id>
```

非対話型モードで JSON 形式のすべての監査ログ フィルター ルールを一覧表示します。

```shell
ticloud serverless audit-log filter-rule list -c <cluster-id> -o json
```

## 旗 {#flags}

| フラグ                  | 説明                                                                        | 必須  | 注記                                   |
| -------------------- | ------------------------------------------------------------------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID。                                                                | いいえ | 非対話型モードでのみ動作します。                     |
| -o, --出力文字列          | 出力形式を指定します。有効な値は`human` （デフォルト）または`json`です。完全な結果を得るには、 `json`形式を使用してください。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                       | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug       | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --色なし             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile 文字列 | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
