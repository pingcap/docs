---
title: ticloud config list
summary: The reference of `ticloud config list`.
---

# ticloud 構成リスト {#ticloud-config-list}

すべてリスト[<a href="/tidb-cloud/cli-reference.md#user-profile">ユーザープロファイル</a>](/tidb-cloud/cli-reference.md#user-profile) :

```shell
ticloud config list [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud config ls [flags]
```

## 例 {#examples}

利用可能なすべてのユーザー プロファイルをリストします。

```shell
ticloud config list
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
