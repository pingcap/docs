---
title: ticloud config edit
summary: The reference of `ticloud config edit`.
---

# ticloud 構成編集 {#ticloud-config-edit}

macOS または Linux を使用している場合は、デフォルトのテキスト エディターでプロファイル構成ファイルを開くことができます。

```shell
ticloud config edit [flags]
```

Windows を使用している場合、上記のコマンドを実行すると、代わりにプロファイル構成ファイルのパスが出力されます。

> **ノート：**
>
> フォーマット エラーや実行エラーを回避するために、構成ファイルを手動で編集することはお勧めしません。代わりに、 [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) 、 [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md) 、または[`ticloud config set`](/tidb-cloud/ticloud-config-set.md)を使用して構成を変更できます。

## 例 {#examples}

プロファイル構成ファイルを編集します。

```shell
ticloud config edit
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
