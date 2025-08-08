---
title: ticloud config set
summary: ticloud config set` のリファレンス。
---

# ticloud 設定セット {#ticloud-config-set}

アクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)のプロパティを設定します。

```shell
ticloud config set <property-name> <value> [flags]
```

設定できるプロパティには、 `public-key` 、 `private-key` 、 `api-url`などがあります。

| プロパティ   | 説明                                                                 | 必須  |
| ------- | ------------------------------------------------------------------ | --- |
| 公開鍵     | TiDB Cloud API の公開キーを指定します。                                        | はい  |
| 秘密鍵     | TiDB Cloud API の秘密キーを指定します。                                        | はい  |
| API URL | TiDB Cloudの基本 API URL を指定します (デフォルトは`https://api.tidbcloud.com` )。 | いいえ |

> **注記：**
>
> 特定のユーザー プロファイルのプロパティを構成する場合は、 `-P`フラグを追加し、コマンドで対象のユーザー プロファイル名を指定できます。

## 例 {#examples}

アクティブ プロファイルの公開キーの値を設定します。

```shell
ticloud config set public-key <public-key>
```

特定のプロファイル`test`の公開キーの値を設定します。

```shell
ticloud config set public-key <public-key> -P test
```

API ホストを設定します。

```shell
ticloud config set api-url https://api.tidbcloud.com
```

> **注記：**
>
> TiDB Cloud APIのURLはデフォルトで`https://api.tidbcloud.com`設定されています。通常は設定する必要はありません。

## 旗 {#flags}

| フラグ        | 説明                  |
| ---------- | ------------------- |
| -h, --help | このコマンドのヘルプ情報を表示します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
