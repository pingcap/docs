---
title: ticloud config describe
summary: The reference of `ticloud config describe`.
---

# ticloud 構成の説明 {#ticloud-config-describe}

特定の[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)のプロパティ情報を取得します。

```shell
ticloud config describe <profile-name> [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud config get <profile-name> [flags]
```

## 例 {#examples}

ユーザー プロファイルを記述します。

```shell
ticloud config describe <profile-name>
```

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
