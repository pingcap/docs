---
title: tiup clean
summary: 「tiup clean」コマンドは、コンポーネント操作中に生成されたデータを消去します。構文は「tiup clean [name] [flags]」で、すべての操作記録を消去するには「--all」オプションを使用します。
---

# tiup clean {#tiup-clean}

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
