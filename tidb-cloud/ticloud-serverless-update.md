---
title: ticloud serverless update
summary: ticloud serverless update` のリファレンス。
---

# ticloud サーバーレスアップデート {#ticloud-serverless-update}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターを更新します。

```shell
ticloud serverless update [flags]
```

## 例 {#examples}

対話モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスターを更新します。

```shell
ticloud serverless update
```

非対話型モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスターの名前を更新します。

```shell
ticloud serverless update -c <cluster-id> --display-name <new-display-mame>
```

非対話型モードでTiDB Cloud Starter またはTiDB Cloud Essential クラスターのラベルを更新する

```shell
ticloud serverless update -c <cluster-id> --labels "{\"label1\":\"value1\"}"
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                          | 必須  | 注記                       |   |
| -------------------- | --------------------------- | --- | ------------------------ | - |
| -c, --cluster-id 文字列 | クラスターの ID を指定します。           | はい  | 非対話型モードでのみ動作します。         |   |
| -n --表示名文字列          | クラスターの新しい名前を指定します。          | いいえ | 非対話型モードでのみ動作します。         | 。 |
| --labels 文字列         | クラスターの新しいラベルを指定します。         | いいえ | 非対話型モードでのみ動作します。         |   |
| --パブリックエンドポイントを無効にする | クラスターのパブリック エンドポイントを無効にします。 | いいえ | 非対話型モードでのみ動作します。         |   |
| -h, --help           | このコマンドのヘルプ情報を表示します。         | いいえ | 非対話型モードと対話型モードの両方で動作します。 |   |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
