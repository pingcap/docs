---
title: ticloud config delete
summary: ticloud config delete` のリファレンス。
---

# ticloud 設定の削除 {#ticloud-config-delete}

[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を削除:

```shell
ticloud config delete <profile-name> [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud config rm <profile-name> [flags]
```

## 例 {#examples}

ユーザー プロファイルを削除します。

```shell
ticloud config delete <profile-name>
```

## 旗 {#flags}

| フラグ        | 説明                  |
| ---------- | ------------------- |
|  --force   | 確認なしでプロファイルを削除します。  |
| -h, --help | このコマンドのヘルプ情報を表示します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
