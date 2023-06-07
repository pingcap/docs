---
title: ticloud config edit
summary: The reference of `ticloud config edit`.
---

# ticloud設定編集 {#ticloud-config-edit}

macOS または Linux を使用している場合は、デフォルトのテキスト エディタでプロファイル構成ファイルを開くことができます。

```shell
ticloud config edit [flags]
```

Windows を使用している場合は、前述のコマンドを実行すると、代わりにプロファイル構成ファイルのパスが表示されます。

> **ノート：**
>
> フォーマット エラーや実行エラーを避けるために、構成ファイルを手動で編集することはお勧めしません。代わりに、 [<a href="/tidb-cloud/ticloud-config-create.md">`ticloud config create`</a>](/tidb-cloud/ticloud-config-create.md) 、 [<a href="/tidb-cloud/ticloud-config-delete.md">`ticloud config delete`</a>](/tidb-cloud/ticloud-config-delete.md) 、または[<a href="/tidb-cloud/ticloud-config-set.md">`ticloud config set`</a>](/tidb-cloud/ticloud-config-set.md)を使用して構成を変更できます。

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

| 国旗             | 説明                                                                                                                                       | 必要  | ノート                                                               |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                                                                           | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[<a href="/tidb-cloud/cli-reference.md#user-profile">ユーザープロフィール</a>](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[<a href="https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose">問題</a>](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
