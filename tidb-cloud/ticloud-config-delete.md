---
title: ticloud config delete
summary: The reference of `ticloud config delete`.
---

# ticloud 構成の削除 {#ticloud-config-delete}

[<a href="/tidb-cloud/cli-reference.md#user-profile">ユーザープロフィール</a>](/tidb-cloud/cli-reference.md#user-profile)を削除します:

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

## フラグ {#flags}

| 国旗         | 説明                |
| ---------- | ----------------- |
|  --force   | 確認なしでプロファイルを削除します |
| -h, --help | このコマンドのヘルプ情報      |

## 継承されたフラグ {#inherited-flags}

| 国旗             | 説明                                                                                                                                       | 必要  | ノート                                                               |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                                                                           | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[<a href="/tidb-cloud/cli-reference.md#user-profile">ユーザープロフィール</a>](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[<a href="https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose">問題</a>](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
