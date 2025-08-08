---
title: ticloud config create
summary: ticloud config create` のリファレンス。
---

# ticloud 設定作成 {#ticloud-config-create}

ユーザー プロファイル設定を保存する[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)作成します。

```shell
ticloud config create [flags]
```

> **注記：**
>
> ユーザー プロファイルを作成する前に、 [TiDB CloudAPIキーを作成する](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)行う必要があります。

## 例 {#examples}

対話型モードでユーザー プロファイルを作成します。

```shell
ticloud config create
```

非対話型モードでユーザー プロファイルを作成します。

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                | 説明                                 | 必須  | 注記                       |
| ------------------ | ---------------------------------- | --- | ------------------------ |
| -h, --help         | このコマンドのヘルプ情報を表示します。                | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| --秘密鍵文字列           | TiDB Cloud API の秘密キーを指定します。        | はい  | 非対話型モードでのみ動作します。         |
| --profile-name 文字列 | プロファイルの名前を指定します ( `.`含めることはできません)。 | はい  | 非対話型モードでのみ動作します。         |
| --公開鍵文字列           | TiDB Cloud API の公開キーを指定します。        | はい  | 非対話型モードでのみ動作します。         |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
