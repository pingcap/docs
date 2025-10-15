---
title: ticloud serverless audit-log filter-rule describe
summary: ticloud serverless audit-log filter-rule describe` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールの説明 {#ticloud-serverless-audit-log-filter-rule-describe}

TiDB Cloud Essential クラスターの監査ログ フィルター ルールについて説明します。

```shell
ticloud serverless audit-log filter-rule describe [flags]
```

## 例 {#examples}

インタラクティブ モードで監査ログ フィルタ ルールを記述します。

```shell
ticloud serverless audit-log filter-rule describe
```

非対話型モードで監査ログ フィルタ ルールを記述します。

```shell
ticloud serverless audit-log filter-rule describe --cluster-id <cluster-id> --filter-rule-id <rule-id>
```

## 旗 {#flags}

| フラグ                  | 説明                  | 必須  | 注記                                   |
| -------------------- | ------------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID。          | はい  | 非対話型モードでのみ動作します。                     |
| --filter-rule-id 文字列 | フィルター ルールの ID。      | はい  | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --デバッグ        | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --色なし             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile 文字列 | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
