---
title: tiup clean
---

# tiup clean {#tiup-clean}

`tiup clean`コマンドは、コンポーネントの操作中に生成されたデータをクリアするために使用されます。

## 構文 {#syntax}

```shell
tiup clean [name] [flags]
```

`[name]`の値は、 [`status`コマンド](/tiup/tiup-command-status.md)によって出力される`Name`フィールドです。 `[name]`を省略した場合は、 `tiup clean`コマンドに`--all`オプションを追加する必要があります。

## オプション {#option}

### - 全て {#all}

-   すべての操作レコードをクリアします
-   データ型：ブール
-   デフォルト：false

## 出力 {#output}

```
Clean instance of `%s`, directory: %s
```

[&lt;&lt;前のページに戻る-TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
