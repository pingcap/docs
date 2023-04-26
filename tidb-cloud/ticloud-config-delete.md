---
title: ticloud config delete
summary: The reference of `ticloud config delete`.
---

# ticloud 構成の削除 {#ticloud-config-delete}

[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を削除:

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
|  --force   | 確認せずにプロファイルを削除します |
| -h, --help | このコマンドのヘルプ情報      |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
