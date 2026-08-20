---
title: ticloud serverless audit-log filter-rule update
summary: ticloud serverless audit-log filter-rule update` のリファレンス。
---

# ticloud serverless audit-log filter-rule update {#ticloud-serverless-audit-log-filter-rule-update}

TiDB Cloud Essential クラスターの監査ログフィルタールールを更新します。

```shell
ticloud serverless audit-log filter-rule update [flags]
```

## 例 {#examples}

対話モードで監査ログフィルタルールを更新します。

```shell
ticloud serverless audit-log filter-rule update
```

非対話型モードで監査ログフィルタルールを有効にする:

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled
```

非対話型モードで監査ログフィルタルールを無効にする:

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```

非対話型モードで監査ログフィルタルールのフィルタを更新します。

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

## フラグ {#flags}

| フラグ                  | 説明                                                                                                                                                       | 必須  | 注記                                   |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --- | ------------------------------------ |
| -c, --cluster-id string | クラスターの ID。                                                                                                                                               | はい  | 非対話型モードでのみ動作します。                     |
| --display-name string   | フィルタールールの表示名。                                                                                                                                           | いいえ | 非対話型モードでのみ動作します。                     |
| --enabled                 | フィルタールールを有効または無効にします。                                                                                                                                   | いいえ | 非対話型モードでのみ動作します。                     |
| --filter-rule-id string | フィルタールールの ID。                                                                                                                                           | はい  | 非対話型モードでのみ動作します。                     |
| --rule string             | フィルタルール式を完了します。フィルタテンプレートを表示するには[`ticloud serverless audit-log filter template`](/tidb-cloud/ticloud-serverless-audit-log-filter-rule-template.md)を使用します。 | いいえ | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                                                                                                      | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug        | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --no-color             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile string | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
