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

> **注記：**
>
> フォーマット エラーや実行エラーを避けるために、構成ファイルを手動で編集することはお勧めしません。代わりに、 [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) 、 [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md) 、または[`ticloud config set`](/tidb-cloud/ticloud-config-set.md)を使用して構成を変更できます。

## 例 {#examples}

プロファイル構成ファイルを編集します。

```shell
ticloud config edit
```

## フラグ {#flags}

| フラグ        | 説明           |
| ---------- | ------------ |
| -h, --help | このコマンドのヘルプ情報 |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                 |
| -------------- | -------------------------------------------------------------------------------- | --- | ------------------------------------------------------------------ |
| --色なし          | 出力のカラーを無効にします。                                                                   | いいえ | 非対話型モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                           |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
