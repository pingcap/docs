---
title: tiup clean
summary: `tiup clean`コマンドは、コンポーネントの動作中に生成されたデータをクリアするために使用されます。`tiup clean [name] [flags]`の構文を持ち、`[name]`を省略した場合は、`--all`オプションを追加する必要があります。`--all`オプションはすべての操作記録をクリアし、デフォルト値はfalseです。
---

# クリーンアップ {#tiup-clean}

`tiup clean`コマンドは、コンポーネントの動作中に生成されたデータをクリアするために使用されます。

## 構文 {#syntax}

```shell
tiup clean [name] [flags]
```

値`[name]`は、 [`status`コマンド](/tiup/tiup-command-status.md)によって出力される`Name`フィールドです。 `[name]`を省略した場合は、 `tiup clean`コマンドに`--all`オプションを追加する必要があります。

## オプション {#option}

### &#x20;--all {#all}

-   すべての操作記録をクリアします
-   データ型: ブール値
-   デフォルト: false

## 出力 {#output}

    Clean instance of `%s`, directory: %s

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
