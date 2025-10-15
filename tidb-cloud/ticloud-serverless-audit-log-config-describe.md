---
title: ticloud serverless audit-log config describe
summary: ticloud serverless audit-log config describe` のリファレンス。
---

# ticloud サーバーレス監査ログ設定の説明 {#ticloud-serverless-audit-log-config-describe}

TiDB Cloud Essential クラスターのデータベース監査ログ構成について説明します。

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

## 旗 {#flags}

| フラグ                  | 説明                  | 必須  | 注記                                   |
| -------------------- | ------------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスター ID。           | はい  | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug       | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --色なし             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile 文字列 | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
