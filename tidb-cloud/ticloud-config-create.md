---
title: ticloud config create
summary: The reference of `ticloud config create`.
---

# ticloud 構成の作成 {#ticloud-config-create}

ユーザー プロファイル設定を保存する[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を作成します。

```shell
ticloud config create [flags]
```

> **ノート：**
>
> ユーザー プロファイルを作成する前に、 [TiDB CloudAPI キーを作成する](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)を行う必要があります。

## 例 {#examples}

インタラクティブ モードでユーザー プロファイルを作成します。

```shell
ticloud config create
```

非インタラクティブ モードでユーザー プロファイルを作成します。

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## フラグ {#flags}

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗           | 説明                      | 必要  | ノート                                  |
| ------------ | ----------------------- | --- | ------------------------------------ |
| -h, --help   | このコマンドのヘルプ情報            | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。 |
| -- 秘密鍵文字列    | TiDB Cloud API の秘密鍵     | はい  | 非対話モードでのみ機能します。                      |
| --プロファイル名文字列 | プロファイルの名前`.`を含むことはできません | はい  | 非対話モードでのみ機能します。                      |
| --公開鍵文字列     | TiDB Cloud API の公開鍵     | はい  | 非対話モードでのみ機能します。                      |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
