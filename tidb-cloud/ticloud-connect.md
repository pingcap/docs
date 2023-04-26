---
title: ticloud connect
summary: The reference of `ticloud connect`.
---

# タイクラウドコネクト {#ticloud-connect}

TiDB Cloudクラスターに接続します。

```shell
ticloud connect [flags]
```

> **ノート：**
>
> -   デフォルトのユーザーを使用するかどうかを尋ねられた場合は、 `Y`を選択してデフォルトの root ユーザーを使用するか、 `n`選択して別のユーザーを指定できます。 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの場合、デフォルトの root ユーザーの名前には`3pTAoNNegb47Uc8`などの[プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)があります。
> -   接続は、セッションの[ANSI SQL モード](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_ansi)強制します。セッションを終了するには、 `\q`と入力します。

## 例 {#examples}

インタラクティブ モードでTiDB Cloudクラスターに接続します。

```shell
ticloud connect
```

デフォルトのユーザーを使用して、非インタラクティブ モードでTiDB Cloudクラスターに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id>
```

デフォルトのユーザーを使用して、非対話モードでパスワードを使用してTiDB Cloudクラスターに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id> --password <password>
```

特定のユーザーを使用して、非インタラクティブ モードでTiDB Cloudクラスターに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id> -u <user-name>
```

## フラグ {#flags}

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                   | 説明            | 必要  | ノート                                  |
| -------------------- | ------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスタID        | はい  | 非対話モードでのみ機能します。                      |
| -h, --help           | このコマンドのヘルプ情報  | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。 |
| - パスワード              | ユーザーのパスワード    | いいえ | 非対話モードでのみ機能します。                      |
| -p, --project-id 文字列 | プロジェクト ID     | はい  | 非対話モードでのみ機能します。                      |
| -u, --user 文字列       | ログイン用の特定のユーザー | いいえ | 非対話モードでのみ機能します。                      |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
