---
title: ticloud serverless audit-log describe
summary: ticloud serverless audit-log describe` のリファレンス。
---

# ticloud サーバーレス監査ログの説明 {#ticloud-serverless-audit-log-describe}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータベース監査ログ構成について説明します。

```shell
ticloud serverless audit-log describe [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud serverless audit-log get [flags]
```

## 例 {#examples}

対話モードでデータベース監査ログ構成を取得します。

```shell
ticloud serverless audit-log describe
```

非対話型モードでデータベース監査ログ構成を取得します。

```shell
ticloud serverless audit-log describe -c <cluster-id>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                  | 必須  | 注記                       |
| -------------------- | ------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列 | クラスター ID。           | はい  | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ         | 説明               | 必須  | 注記                                                      |
| ----------- | ---------------- | --- | ------------------------------------------------------- |
| --色なし       | 出力のカラーを無効にします。   | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -D, --debug | デバッグ モードを有効にします。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
