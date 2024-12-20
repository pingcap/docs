---
title: ticloud config edit
summary: ticloud config edit` のリファレンス。
---

# ticloud 設定編集 {#ticloud-config-edit}

macOS または Linux を使用している場合は、デフォルトのテキスト エディターでプロファイル構成ファイルを開くことができます。

```shell
ticloud config edit [flags]
```

Windows を使用している場合は、上記のコマンドを実行すると、代わりにプロファイル構成ファイルのパスが出力されます。

> **注記：**
>
> フォーマットエラーや実行エラーを回避するために、構成ファイルを手動で編集することはお勧めしません。代わりに、 [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) 、 [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md) 、または[`ticloud config set`](/tidb-cloud/ticloud-config-set.md)使用して構成を変更することができます。

## 例 {#examples}

プロファイル構成ファイルを編集します。

```shell
ticloud config edit
```

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
