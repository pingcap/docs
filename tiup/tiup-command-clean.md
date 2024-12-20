---
title: tiup clean
summary: 「tiup clean」コマンドは、コンポーネント操作中に生成されたデータをクリアします。構文は「tiup clean [name] [flags]」で、オプション「--all」を使用してすべての操作レコードをクリアします。
---

# tiupクリーン {#tiup-clean}

`tiup clean`コマンドは、コンポーネント操作中に生成されたデータをクリアするために使用されます。

## 構文 {#syntax}

```shell
tiup clean [name] [flags]
```

`[name]`の値は、 [`status`コマンド](/tiup/tiup-command-status.md)によって出力される`Name`フィールドです。 `[name]`を省略した場合は、 `tiup clean`コマンドに`--all`オプションを追加する必要があります。

## オプション {#option}

### &#x20;--all {#all}

-   すべての操作記録をクリアします
-   データ型: ブール値
-   デフォルト: false

## 出力 {#output}

    Clean instance of `%s`, directory: %s

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
