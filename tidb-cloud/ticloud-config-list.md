---
title: ticloud config list
summary: ticloud config list のリファレンス。
---

# ticloud 設定リスト {#ticloud-config-list}

すべて表示[ユーザープロファイル](/tidb-cloud/cli-reference.md#user-profile) :

```shell
ticloud config list [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud config ls [flags]
```

## 例 {#examples}

利用可能なすべてのユーザー プロファイルを一覧表示します。

```shell
ticloud config list
```

## 旗 {#flags}

| フラグ        | 説明           |
| ---------- | ------------ |
| -h, --help | このコマンドのヘルプ情報 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
