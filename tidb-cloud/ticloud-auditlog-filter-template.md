---
title: ticloud serverless audit-log filter-rule template
summary: ticloud serverless audit-log filter-rule template` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールテンプレート {#ticloud-serverless-audit-log-filter-rule-template}

TiDB Cloud Serverless クラスターの監査ログ フィルター ルール テンプレートを表示します。

```shell
ticloud serverless audit-log filter-rule template [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud serverless audit-log filter template [flags]
```

## 例 {#examples}

対話モードでフィルター テンプレートを表示します。

```shell
ticloud serverless audit-log filter template
```

非対話型モードでフィルター テンプレートを表示します。

```shell
ticloud serverless audit-log filter template --cluster-id <cluster-id>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                                             | 必須  | 注記                       |
| -------------------- | ---------------------------------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID (オプション、テンプレートがクラスター固有になる場合のコンテキスト用)。 | いいえ | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報を表示します。                            | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
