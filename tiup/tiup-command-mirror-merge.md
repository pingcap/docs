---
title: tiup mirror merge
summary: tiup mirror merge` コマンドは、1 つ以上のミラーを現在のミラーにマージします。実行条件には、既存の所有者 ID と対応する秘密キーが含まれます。
---

# tiup mirror merge {#tiup-mirror-merge}

`tiup mirror merge`コマンドは、1 つ以上のミラーを現在のミラーにマージするために使用されます。

このコマンドを実行するには、次の条件を満たす必要があります。

-   ターゲット ミラーのすべてのコンポーネントの所有者 ID が現在のミラーに存在します。
-   このコマンドを実行するユーザーの`${TIUP_HOME}/keys`ディレクトリには、現在のミラー内の上記の所有者 ID に対応するすべての秘密鍵が含まれています (コマンド[`tiup mirror set`](/tiup/tiup-command-mirror-set.md)使用して、現在のミラーを現在変更が許可されているミラーに切り替えることができます)。

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
-   現在のミラーにターゲット ミラーのコンポーネント所有者がいない場合、または`${TIUP_HOME}/keys`所有者の秘密キーがない場合、 TiUP は`Error: missing owner keys for owner %s on component %s`エラーを報告します。

[&lt;&lt; 前のページに戻る - TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
