---
title: ticloud serverless sql-user update
summary: ticloud serverless sql-user update` のリファレンス。
---

# ticloud サーバーレス SQL ユーザーの更新 {#ticloud-serverless-sql-user-update}

TiDB Cloud Serverless SQL ユーザーを更新します。

```shell
ticloud serverless sql-user update [flags]
```

## 例 {#examples}

対話モードでTiDB Cloud Serverless SQL ユーザーを更新します。

```shell
ticloud serverless sql-user update
```

非対話モードでTiDB Cloud Serverless SQL ユーザーを更新します。

```shell
ticloud serverless sql-user update -c <cluster-id> --user <user-name> --password <password> --role <role>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                  | 説明                                               | 必須  | 注記                       |
| -------------------- | ------------------------------------------------ | --- | ------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID を指定します。                                | はい  | 非対話型モードでのみ動作します。         |
| --パスワード文字列           | SQL ユーザーの新しいパスワードを指定します。                         | いいえ | 非対話型モードでのみ動作します。         |
| --role 文字列           | SQL ユーザーの新しいロールを指定します。このフラグを渡すと、既存のロールが置き換えられます。 | いいえ | 非対話型モードでのみ動作します。         |
| --add-role 文字列       | SQL ユーザーに追加するロールを指定します。                          | いいえ | 非対話型モードでのみ動作します。         |
| --delete-role 文字列    | SQL ユーザーから削除するロールを指定します。                         | いいえ | 非対話型モードでのみ動作します。         |
| -u, --user 文字列       | 更新する SQL ユーザーの名前を指定します。                          | いいえ | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報を表示します。                              | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------------ |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |
| -D、--デバッグ         | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
