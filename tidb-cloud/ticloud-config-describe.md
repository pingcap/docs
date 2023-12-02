---
title: ticloud config describe
summary: The reference of `ticloud config describe`.
---

# ticloud 構成の説明 {#ticloud-config-describe}

特定の[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)のプロパティ情報を取得します。

```shell
ticloud config describe <profile-name> [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud config get <profile-name> [flags]
```

## 例 {#examples}

ユーザー プロファイルを説明します。

```shell
ticloud config describe <profile-name>
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
