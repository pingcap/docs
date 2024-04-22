---
title: tiup mirror merge
summary: tiup mirror mergeコマンドは、1つ以上のミラーを現在のミラーにマージするために使用されます。このコマンドを実行するには、ターゲットミラーのすべてのコンポーネントの所有者IDが現在のミラーに存在し、ユーザーの${TIUP_HOME}/keysディレクトリには、現在のミラー内の所有者IDに対応するすべての秘密キーが含まれている必要があります。現在のミラーにマージされる最初のミラーとN番目のミラーを指定します。コマンドが正常に実行された場合、出力はありません。現在のミラーにターゲットミラーのコンポーネント所有者が存在しない場合、または${TIUP_HOME}/keys所有者の秘密キーがない場合。
---

# tiup mirror merge {#tiup-mirror-merge}

`tiup mirror merge`コマンドは、1 つ以上のミラーを現在のミラーにマージするために使用されます。

このコマンドを実行するには、次の条件が満たされる必要があります。

-   ターゲット ミラーのすべてのコンポーネントの所有者 ID は、現在のミラーに存在します。
-   このコマンドを実行するユーザーの`${TIUP_HOME}/keys`ディレクトリには、現在のミラー内の上記の所有者 ID に対応するすべての秘密キーが含まれています (コマンド[`tiup mirror set`](/tiup/tiup-command-mirror-set.md)を使用して、現在のミラーを現在変更が許可されているミラーに切り替えることができます)。

## 構文 {#syntax}

```shell
tiup mirror merge <mirror-dir-1> [mirror-dir-N] [flags]
```

-   `<mirror-dir-1>` : 現在のミラーにマージされる最初のミラー
-   `[mirror-dir-N]` : 現在のミラーにマージされる N 番目のミラー

## オプション {#option}

なし

## 出力 {#outputs}

-   コマンドが正常に実行された場合、出力はありません。
-   現在のミラーにターゲット ミラーのコンポーネント所有者が存在しない場合、または`${TIUP_HOME}/keys`所有者の秘密キーがない場合、 TiUP は`Error: missing owner keys for owner %s on component %s`エラーを報告します。

[&lt;&lt; 前のページに戻る - TiUP Mirror コマンド一覧](/tiup/tiup-command-mirror.md#command-list)
