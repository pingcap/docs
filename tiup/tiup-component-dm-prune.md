---
title: tiup dm prune
summary: クラスターをスケールさせる際、etcd内の少量のメタデータがクリーンアップされない場合がありますが、通常は問題にはなりません。必要に応じて、「tiup dm prune」コマンドを手動で実行してメタデータをクリーンアップできます。コマンド構文は「tiup dm prune <cluster-name> [flags]」です。オプション「-h, --help」を指定するとヘルプ情報が出力、クリーンアッププロセスのログが出力されます。
---

# tiup dm プルーン {#tiup-dm-prune}

クラスターをスケールインする際(/tiup/tiup-component-dm-scale-in.md)、etcd内の少量のメタデータがクリーンアップされませんが、通常は問題ありません。メタデータをクリーンアップする必要がある場合は、 `tiup dm prune`コマンドを手動で実行してください。

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

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
