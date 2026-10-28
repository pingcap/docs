---
title: ticloud serverless branch shell
summary: "`ticloud serverless branch shell` のリファレンス。"
aliases: ['/ja/tidbcloud/ticloud-connect']
---

# ticloud serverless branch shell {#ticloud-serverless-branch-shell}

TiDB Cloud Starter またはTiDB Cloud Essential インスタンスのブランチに接続します。

```shell
ticloud serverless branch shell [flags]
```

## 例 {#examples}

対話モードでブランチに接続します。

```shell
ticloud serverless branch shell
```

非対話型モードでデフォルトのユーザーを使用してブランチに接続します。

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id>
```

非対話型モードでデフォルトのユーザー名とパスワードを使用してブランチに接続します。

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id> --password <password>
```

非対話型モードで特定のユーザー名とパスワードを使用してブランチに接続します。

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id> -u <user-name> --password <password>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                  | 必須  | 注記                       |
| -------------------- | ------------------- | --- | ------------------------ |
| -b, --branch-id string  | ブランチの ID を指定します。    | はい  | 非対話型モードでのみ動作します。         |
| -c, --cluster-id string | クラスターの ID を指定します。   | はい  | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報を表示します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| --password              | ユーザーのパスワードを指定します。   | いいえ | 非対話型モードでのみ動作します。         |
| -u, --user string       | ログインするユーザーを指定します。   | いいえ | 非対話型モードでのみ動作します。         |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --no-color             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile string | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグモードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[Issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
