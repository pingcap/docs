---
title: tiup mirror merge
---

# tiup mirror merge {#tiup-mirror-merge}

`tiup mirror merge`コマンドは、1つ以上のミラーを現在のミラーにマージするために使用されます。

このコマンドを実行するには、次の条件が満たされている必要があります。

-   ターゲットミラーのすべてのコンポーネントの所有者IDは、現在のミラーに存在します。
-   このコマンドを実行するユーザーの`${TIUP_HOME}/keys`ディレクトリには、現在のミラーの上記の所有者IDに対応するすべての秘密鍵が含まれています（コマンド[`tiup mirror set`](/tiup/tiup-command-mirror-set.md)を使用して、現在のミラーを現在変更が許可されているミラーに切り替えることができます）。

## 構文 {#syntax}

```shell
tiup mirror merge <mirror-dir-1> [mirror-dir-N] [flags]
```

-   `<mirror-dir-1>` ：現在のミラーにマージされる最初のミラー
-   `[mirror-dir-N]` ：現在のミラーにマージされるN番目のミラー

## オプション {#option}

なし

## 出力 {#outputs}

-   コマンドが正常に実行された場合、出力はありません。
-   現在のミラーにターゲットミラーのコンポーネント所有者がいない場合、または`${TIUP_HOME}/keys`に所有者の秘密鍵がない場合、TiUPは`Error: missing owner keys for owner %s on component %s`エラーを報告します。

[&lt;&lt;前のページに戻る-TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
