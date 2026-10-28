---
title: ticloud serverless audit-log config describe
summary: "`ticloud serverless audit-log config describe` のリファレンス。"
---

# ticloud serverless audit-log config describe {#ticloud-serverless-audit-log-config-describe}

TiDB Cloud Essential インスタンスのデータベース監査ログ構成の詳細を表示します。

```shell
ticloud serverless audit-log config describe [flags]
```

## 例 {#examples}

対話モードでデータベース監査ログ構成を取得します。

```shell
ticloud serverless audit-log config describe
```

非対話型モードでデータベース監査ログ構成を取得します。

```shell
ticloud serverless audit-log config describe -c <cluster-id>
```

## フラグ {#flags}

| フラグ                  | 説明                  | 必須  | 注記                                   |
| -------------------- | ------------------- | --- | ------------------------------------ |
| -c, --cluster-id string | クラスター ID。           | はい  | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | 対話モードと非対話モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug       | デバッグモードを有効にします。          | いいえ | 対話モードと非対話モードの両方で動作します。 |
| --no-color             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile string | 設定ファイルから使用するプロファイルを指定します。 | いいえ | 対話モードと非対話モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[Issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
