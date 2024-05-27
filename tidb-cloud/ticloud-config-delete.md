---
title: ticloud config delete
summary: ticloud config delete のリファレンス。
---

# ticloud 設定削除 {#ticloud-config-delete}

[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)削除:

```shell
ticloud config delete <profile-name> [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud config rm <profile-name> [flags]
```

## 例 {#examples}

ユーザープロファイルを削除します。

```shell
ticloud config delete <profile-name>
```

## 旗 {#flags}

| フラグ        | 説明                |
| ---------- | ----------------- |
|  --force   | 確認なしでプロフィールを削除します |
| -h, --help | このコマンドのヘルプ情報      |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
