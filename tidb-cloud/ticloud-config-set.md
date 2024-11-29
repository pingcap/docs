---
title: ticloud config set
summary: ticloud config set` のリファレンス。
---

# ticloud 設定セット {#ticloud-config-set}

アクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)のプロパティを設定します。

```shell
ticloud config set <property-name> <value> [flags]
```

設定できるプロパティには、 `public-key` 、 `private-key` 、 `api-url`があります。

| プロパティ   | 説明                                                                  | 必須  |
| ------- | ------------------------------------------------------------------- | --- |
| 公開鍵     | TiDB Cloud API の公開キーを指定します。                                         | はい  |
| 秘密鍵     | TiDB Cloud API の秘密キーを指定します。                                         | はい  |
| API URL | TiDB Cloudのベース API URL を指定します (デフォルトは`https://api.tidbcloud.com` )。 | いいえ |

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
> TiDB Cloud API URLはデフォルトで`https://api.tidbcloud.com`なっています。通常は設定する必要はありません。

## 旗 {#flags}

| フラグ        | 説明                  |
| ---------- | ------------------- |
| -h, --help | このコマンドのヘルプ情報を表示します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |
| -D、--デバッグ         | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
