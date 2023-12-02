---
title: tiup dm prune
---

# ティアップDMプルーン {#tiup-dm-prune}

クラスター (/tiup/tiup-component-dm-scale-in.md) をスケールインすると、etcd 内の少量のメタデータがクリーンアップされませんが、通常は問題は発生しません。メタデータをクリーンアップする必要がある場合は、 `tiup dm prune`コマンドを手動で実行できます。

## 構文 {#syntax}

```shell
tiup dm prune <cluster-name> [flags]
```

## オプション {#option}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

クリーンアッププロセスのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
