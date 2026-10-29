---
title: ticloud serverless audit-log filter-rule template
summary: "`ticloud serverless audit-log filter-rule template` のリファレンス。"
---

# ticloud serverless audit-log filter-rule template {#ticloud-serverless-audit-log-filter-rule-template}

TiDB Cloud Essential インスタンスの監査ログフィルタールールテンプレートを表示します。

```shell
ticloud serverless audit-log filter-rule template [flags]
```

## 例 {#examples}

対話型モードでフィルターテンプレートを表示します。

```shell
ticloud serverless audit-log filter-rule template
```

非対話型モードでフィルターテンプレートを表示します。

```shell
ticloud serverless audit-log filter-rule template --cluster-id <cluster-id>
```

## フラグ {#flags}

| フラグ                  | 説明                  | 必須  | 注記                                   |
| -------------------- | ------------------- | --- | ------------------------------------ |
| -c, --cluster-id string | クラスターの ID。          | いいえ | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | 対話型モードと非対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug        | デバッグモードを有効にします。          | いいえ | 対話型モードと非対話型モードの両方で動作します。 |
| --no-color             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile string | 設定ファイルから使用するプロファイルを指定します。 | いいえ | 対話型モードと非対話型モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[Issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
