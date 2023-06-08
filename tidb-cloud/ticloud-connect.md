---
title: ticloud connect
summary: The reference of `ticloud connect`.
---

# ティッククラウド接続 {#ticloud-connect}

TiDB Cloudクラスターに接続します。

```shell
ticloud connect [flags]
```

> **ノート：**
>
> -   デフォルトのユーザーを使用するかどうかを尋ねられた場合は、 `Y`を選択してデフォルトの root ユーザーを使用するか、 `n`選択して別のユーザーを指定できます。 [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターの場合、デフォルトの root ユーザーの名前には`3pTAoNNegb47Uc8`などの[<a href="/tidb-cloud/select-cluster-tier.md#user-name-prefix">接頭語</a>](/tidb-cloud/select-cluster-tier.md#user-name-prefix)が含まれます。
> -   接続ではセッションに対して[<a href="https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_ansi">ANSI SQL モード</a>](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_ansi)強制されます。セッションを終了するには、 `\q`を入力します。

## 例 {#examples}

インタラクティブ モードでTiDB Cloudクラスターに接続します。

```shell
ticloud connect
```

デフォルト ユーザーを使用して、非対話モードでTiDB Cloudクラスターに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id>
```

デフォルトのユーザーを使用して、非対話モードでパスワードを使用してTiDB Cloudクラスターに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id> --password <password>
```

特定のユーザーを使用して、非対話モードでTiDB Cloudクラスターに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id> -u <user-name>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                  | 説明            | 必要  | ノート                      |
| ------------------- | ------------- | --- | ------------------------ |
| -c、--cluster-id 文字列 | クラスタID        | はい  | 非対話モードでのみ動作します。          |
| -h, --help          | このコマンドのヘルプ情報  | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| - パスワード             | ユーザーのパスワード    | いいえ | 非対話モードでのみ動作します。          |
| -p、--プロジェクトID文字列    | プロジェクトID      | はい  | 非対話モードでのみ動作します。          |
| -u、--user 文字列       | ログイン用の特定のユーザー | いいえ | 非対話モードでのみ動作します。          |

## 継承されたフラグ {#inherited-flags}

| 国旗             | 説明                                                                                                                                       | 必要  | ノート                                                               |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                                                                           | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[<a href="/tidb-cloud/cli-reference.md#user-profile">ユーザープロフィール</a>](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[<a href="https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose">問題</a>](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
