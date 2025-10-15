---
title: ticloud serverless audit-log filter-rule update
summary: ticloud serverless audit-log filter-rule update` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールの更新 {#ticloud-serverless-audit-log-filter-rule-update}

TiDB Cloud Essential クラスターの監査ログ フィルター ルールを更新します。

```shell
ticloud serverless audit-log filter-rule update [flags]
```

## 例 {#examples}

対話モードで監査ログ フィルタ ルールを更新します。

```shell
ticloud serverless audit-log filter-rule update
```

非対話型モードで監査ログフィルタルールを有効にする:

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled
```

非対話型モードで監査ログ フィルタ ルールを無効にする:

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```

非対話型モードで監査ログ フィルタ ルールのフィルタを更新します。

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

## 旗 {#flags}

| フラグ                  | 説明                                                                                                                                                       | 必須  | 注記                                   |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID。                                                                                                                                               | はい  | 非対話型モードでのみ動作します。                     |
| --display-name 文字列   | フィルター ルールの表示名。                                                                                                                                           | いいえ | 非対話型モードでのみ動作します。                     |
| --有効                 | フィルター ルールを有効または無効にします。                                                                                                                                   | いいえ | 非対話型モードでのみ動作します。                     |
| --filter-rule-id 文字列 | フィルター ルールの ID。                                                                                                                                           | はい  | 非対話型モードでのみ動作します。                     |
| --ルール文字列             | フィルタルール式を完了します。フィルタテンプレートを表示するには[`ticloud serverless audit-log filter template`](/tidb-cloud/ticloud-serverless-audit-log-filter-rule-template.md)使用します。 | いいえ | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                                                                                                      | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --デバッグ        | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --色なし             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile 文字列 | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
