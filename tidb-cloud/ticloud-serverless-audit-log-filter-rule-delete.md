---
title: ticloud serverless audit-log filter-rule delete
summary: ticloud serverless audit-log filter-rule delete` のリファレンス。
---

# ticloud serverless audit-log filter-rule delete {#ticloud-serverless-audit-log-filter-rule-delete}

TiDB Cloud Essential クラスターの監査ログフィルタールールを削除します。

```shell
ticloud serverless audit-log filter-rule delete [flags]
```

## 例 {#examples}

対話モードで監査ログフィルタルールを削除します。

```shell
ticloud serverless audit-log filter-rule delete
```

非対話型モードで監査ログフィルタルールを削除します。

```shell
ticloud serverless audit-log filter-rule delete --cluster-id <cluster-id> --filter-rule-id <rule-id>
```

## フラグ {#flags}

| フラグ                  | 説明                  | 必須  | 注記                                   |
| -------------------- | ------------------- | --- | ------------------------------------ |
| -c, --cluster-id string | クラスターの ID。          | はい  | 非対話型モードでのみ動作します。                     |
| --filter-rule-id string | フィルタールールの ID。      | はい  | 非対話型モードでのみ動作します。                     |
|  --force             | 確認なしで削除します。         | いいえ | インタラクティブモードと非インタラクティブモードの両方で動作します。 |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | インタラクティブモードと非インタラクティブモードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug       | デバッグ モードを有効にします。          | いいえ | インタラクティブモードと非インタラクティブモードの両方で動作します。 |
| --no-color             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile string | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブモードと非インタラクティブモードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
