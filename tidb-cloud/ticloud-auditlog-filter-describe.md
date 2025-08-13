---
title: ticloud serverless audit-log filter-rule describe
summary: ticloud serverless audit-log filter-rule describe` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールの説明 {#ticloud-serverless-audit-log-filter-rule-describe}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターの監査ログ フィルター ルールについて説明します。

```shell
ticloud serverless audit-log filter-rule describe [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud serverless audit-log filter describe [flags]
```

## 例 {#examples}

インタラクティブ モードで監査ログ フィルタ ルールを記述します。

```shell
ticloud serverless audit-log filter describe
```

非対話型モードで監査ログ フィルタ ルールを記述します。

```shell
ticloud serverless audit-log filter describe --cluster-id <cluster-id> --name <rule-name>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                  | 必須  | 注記                       |
| -------------------- | ------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID。          | はい  | 非対話型モードでのみ動作します。         |
| --name 文字列           | フィルター ルールの名前。       | はい  | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
