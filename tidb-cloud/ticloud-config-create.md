---
title: ticloud config create
summary: ticloud config create のリファレンス。
---

# ticloud 設定作成 {#ticloud-config-create}

ユーザー プロファイル設定を保存する[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)作成します。

```shell
ticloud config create [flags]
```

> **注記：**
>
> ユーザー プロファイルを作成する前に、 [TiDB CloudAPIキーを作成する](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)を実行する必要があります。

## 例 {#examples}

対話モードでユーザー プロファイルを作成します。

```shell
ticloud config create
```

非対話型モードでユーザー プロファイルを作成します。

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                | 説明                | 必須  | 注記                       |
| ------------------ | ----------------- | --- | ------------------------ |
| -h, --help         | このコマンドのヘルプ情報      | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| --秘密鍵文字列           | TiDB CloudAPIの秘密鍵 | はい  | 非対話型モードでのみ動作します。         |
| --profile-name 文字列 | プロファイルの名前`.`を含まない | はい  | 非対話型モードでのみ動作します。         |
| --公開鍵文字列           | TiDB CloudAPIの公開鍵 | はい  | 非対話型モードでのみ動作します。         |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------------ |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
