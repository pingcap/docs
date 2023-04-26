---
title: ticloud config set
summary: The reference of `ticloud config set`.
---

# ticloud 構成セット {#ticloud-config-set}

アクティブな[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)のプロパティを構成します。

```shell
ticloud config set <property-name> <value> [flags]
```

設定できるプロパティには、 `public-key` 、 `private-key` 、および`api-url`があります。

| プロパティ   | 説明                                                           | 必要  |
| ------- | ------------------------------------------------------------ | --- |
| 公開鍵     | TiDB Cloud API の公開鍵                                          | はい  |
| 秘密鍵     | TiDB Cloud API の秘密鍵                                          | はい  |
| api-url | TiDB Cloudのベース API URL (デフォルトでは`https://api.tidbcloud.com` ) | いいえ |

> **ノート：**
>
> 特定のユーザー プロファイルのプロパティを構成する場合は、 `-P`フラグを追加して、コマンドで対象のユーザー プロファイル名を指定できます。

## 例 {#examples}

アクティブなプロファイルの公開鍵の値を設定します。

```shell
ticloud config set public-key <public-key>
```

特定のプロファイル`test`の公開鍵の値を設定します。

```shell
ticloud config set public-key <public-key> -P test
```

API ホストを設定します。

```shell
ticloud config set api-url https://api.tidbcloud.com
```

> **ノート：**
>
> TiDB CloudAPI の URL はデフォルトで`https://api.tidbcloud.com`です。通常、設定する必要はありません。

## フラグ {#flags}

| 国旗         | 説明           |
| ---------- | ------------ |
| -h, --help | このコマンドのヘルプ情報 |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
