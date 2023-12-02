---
title: ticloud connect
summary: The reference of `ticloud connect`.
---

# ティッククラウド接続 {#ticloud-connect}

TiDB Cloudクラスターまたはブランチに接続します。

```shell
ticloud connect [flags]
```

> **注記：**
>
> -   デフォルトのユーザーを使用するかどうかを尋ねられた場合は、 `Y`を選択してデフォルトの root ユーザーを使用するか、 `n`選択して別のユーザーを指定できます。 [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの場合、デフォルトの root ユーザーの名前には`3pTAoNNegb47Uc8`などの[接頭語](/tidb-cloud/select-cluster-tier.md#user-name-prefix)が含まれます。
> -   接続ではセッションに対して[ANSI SQL モード](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_ansi)強制されます。セッションを終了するには、 `\q`を入力します。

## 例 {#examples}

インタラクティブ モードでTiDB Cloudクラスターまたはブランチに接続します。

```shell
ticloud connect
```

デフォルト ユーザーを使用して、非対話モードでTiDB Cloudクラスターまたはブランチに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id>
ticloud connect -p <project-id> -c <cluster-id> -b <branch-id>
```

デフォルトのユーザーを使用して、非対話モードでパスワードを使用してTiDB Cloudクラスターまたはブランチに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id> --password <password>
ticloud connect -p <project-id> -c <cluster-id> -b <branch-id> --password <password>
```

特定のユーザーを使用して、非対話モードでTiDB Cloudクラスターまたはブランチに接続します。

```shell
ticloud connect -p <project-id> -c <cluster-id> -u <user-name>
ticloud connect -p <project-id> -c <cluster-id> -b <branch-id> -u <user-name>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                 | 説明            | 必須  | 注記                       |
| ------------------- | ------------- | --- | ------------------------ |
| -c、--cluster-id 文字列 | クラスタID        | はい  | 非対話モードでのみ動作します。          |
| -b、--ブランチ ID 文字列    | 支店ID          | いいえ | 非対話モードでのみ動作します。          |
| -h, --help          | このコマンドのヘルプ情報  | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| - パスワード             | ユーザーのパスワード    | いいえ | 非対話モードでのみ動作します。          |
| -p、--プロジェクトID文字列    | プロジェクトID      | はい  | 非対話モードでのみ動作します。          |
| -u、--user 文字列       | ログイン用の特定のユーザー | いいえ | 非対話モードでのみ動作します。          |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                |
| -------------- | -------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                   | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
