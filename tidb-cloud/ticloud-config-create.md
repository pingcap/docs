---
title: ticloud config create
summary: The reference of `ticloud config create`.
---

# ticloud 構成の作成 {#ticloud-config-create}

ユーザー プロファイル設定を保存するには[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を作成します。

```shell
ticloud config create [flags]
```

> **注記：**
>
> ユーザー プロファイルを作成する前に、 [TiDB CloudAPI キーを作成する](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)を行う必要があります。

## 例 {#examples}

対話モードでユーザー プロファイルを作成します。

```shell
ticloud config create
```

非対話モードでユーザー プロファイルを作成します。

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ          | 説明                        | 必須  | 注記                       |
| ------------ | ------------------------- | --- | ------------------------ |
| -h, --help   | このコマンドのヘルプ情報              | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| --秘密鍵文字列     | TiDB CloudAPI の秘密鍵        | はい  | 非対話モードでのみ動作します。          |
| --プロファイル名文字列 | プロファイルの名前`.`を含めることはできません。 | はい  | 非対話モードでのみ動作します。          |
| --公開鍵文字列     | TiDB CloudAPI の公開キー       | はい  | 非対話モードでのみ動作します。          |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                |
| -------------- | -------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                   | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
