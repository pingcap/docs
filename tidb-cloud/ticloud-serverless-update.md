---
title: ticloud serverless update
summary: ticloud serverless update` のリファレンス。
---

# ticloud サーバーレスアップデート {#ticloud-serverless-update}

TiDB Cloud Serverless クラスターを更新します。

```shell
ticloud serverless update [flags]
```

## 例 {#examples}

インタラクティブ モードでTiDB Cloud Serverless クラスターを更新します。

```shell
ticloud serverless update
```

非対話モードでTiDB Cloud Serverless クラスターの名前を更新します。

```shell
ticloud serverless update -c <cluster-id> --display-name <new-display-mame>
```

非対話モードでTiDB Cloud Serverless クラスターのラベルを更新する

```shell
ticloud serverless update -c <cluster-id> --labels "{\"label1\":\"value1\"}"
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                  | 説明                          | 必須  | 注記                       |   |
| -------------------- | --------------------------- | --- | ------------------------ | - |
| -c, --cluster-id 文字列 | クラスターの ID を指定します。           | はい  | 非対話型モードでのみ動作します。         |   |
| -n --表示名文字列          | クラスターの新しい名前を指定します。          | いいえ | 非対話型モードでのみ動作します。         | 。 |
| --labels 文字列         | クラスターの新しいラベルを指定します。         | いいえ | 非対話型モードでのみ動作します。         |   |
| --パブリックエンドポイントを無効にする | クラスターのパブリック エンドポイントを無効にします。 | いいえ | 非対話型モードでのみ動作します。         |   |
| -h, --help           | このコマンドのヘルプ情報を表示します。         | いいえ | 非対話型モードと対話型モードの両方で動作します。 |   |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |
| -D、--デバッグ         | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
