---
title: ticloud config set
summary: The reference of `ticloud config set`.
---

# ticloud 構成セット {#ticloud-config-set}

アクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)のプロパティを構成します。

```shell
ticloud config set <property-name> <value> [flags]
```

設定できるプロパティには、 `public-key` 、 `private-key` 、および`api-url`があります。

| プロパティ   | 説明                                                           | 必須  |
| ------- | ------------------------------------------------------------ | --- |
| 公開鍵     | TiDB CloudAPI の公開キー                                          | はい  |
| 秘密鍵     | TiDB CloudAPI の秘密鍵                                           | はい  |
| API URL | TiDB Cloudのベース API URL (デフォルトでは`https://api.tidbcloud.com` ) | いいえ |

> **ノート：**
>
> 特定のユーザー プロファイルのプロパティを構成する場合は、コマンドに`-P`フラグを追加してターゲット ユーザー プロファイル名を指定できます。

## 例 {#examples}

アクティブなプロファイルの公開キーの値を設定します。

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
> TiDB CloudAPI URL はデフォルトで`https://api.tidbcloud.com`です。通常は設定する必要はありません。

## フラグ {#flags}

| フラグ        | 説明           |
| ---------- | ------------ |
| -h, --help | このコマンドのヘルプ情報 |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                |
| -------------- | -------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                   | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
