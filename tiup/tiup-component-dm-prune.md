---
title: tiup dm prune
summary: クラスターをスケーリングすると、etcd 内の少量のメタデータがクリーンアップされない場合がありますが、通常は問題にはなりません。必要に応じて、手動で「tiup dm prune」コマンドを実行してメタデータをクリーンアップできます。コマンド構文は「tiup dm prune <cluster-name> [flags]」です。オプション「-h, --help」はヘルプ情報を出力、出力はクリーンアップ プロセスのログです。
---

# ティアップ DM プルーン {#tiup-dm-prune}

クラスターをスケールインすると (/tiup/tiup-component-dm-scale-in.md)、etcd 内の少量のメタデータがクリーンアップされませんが、通常は問題にはなりません。メタデータをクリーンアップする必要がある場合は、 `tiup dm prune`コマンドを手動で実行できます。

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

クリーンアップ プロセスのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
