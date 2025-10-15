---
title: ticloud serverless audit-log filter-rule template
summary: ticloud serverless audit-log filter-rule template` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールテンプレート {#ticloud-serverless-audit-log-filter-rule-template}

TiDB Cloud Essential クラスターの監査ログ フィルター ルール テンプレートを表示します。

```shell
ticloud serverless audit-log filter-rule template [flags]
```

## 例 {#examples}

対話モードでフィルター テンプレートを表示します。

```shell
ticloud serverless audit-log filter-rule template
```

非対話型モードでフィルター テンプレートを表示します。

```shell
ticloud serverless audit-log filter-rule template --cluster-id <cluster-id>
```

## 旗 {#flags}

| フラグ                  | 説明                  | 必須  | 注記                                   |
| -------------------- | ------------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID。          | いいえ | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --デバッグ        | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --色なし             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile 文字列 | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
