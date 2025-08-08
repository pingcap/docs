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
> フォーマットエラーや実行エラーを避けるため、設定ファイルを手動で編集することは推奨されません。代わりに、 [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) 、 [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md) 、または[`ticloud config set`](/tidb-cloud/ticloud-config-set.md)使用して設定を変更できます。

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

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
