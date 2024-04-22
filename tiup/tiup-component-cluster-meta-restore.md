---
title: tiup cluster meta restore
summary: TiUPメタファイルを復元するには、tiup cluster meta restoreコマンドを使用します。構文はtiup cluster meta restore <cluster-name> <backup-file> [flags]です。<cluster-name>は操作対象のクラスターの名前であり、<backup-file>はTiUPメタバックアップファイルへのパスです。復元操作により、現在のメタファイルが上書きされます。メタファイルが失われた場合にのみ、メタファイルを復元することをお勧めします。オプションには-h, --helpがあり、ヘルプ情報を出力します。このオプションはデフォルトでは無効になっており、デフォルト値はfalseです。
---

# tiup クラスターのメタ復元 {#tiup-cluster-meta-restore}

TiUPメタ ファイルを復元するには、 `tiup cluster meta restore`コマンドを使用してバックアップ ファイルから復元します。

## 構文 {#syntax}

```shell
tiup cluster meta restore <cluster-name> <backup-file> [flags]
```

-   `<cluster-name>`は、操作対象のクラスターの名前です。
-   `<backup-file>`は、 TiUPメタ バックアップ ファイルへのパスです。

> **注記：**
>
> 復元操作により、現在のメタ ファイルが上書きされます。メタ ファイルが失われた場合にのみ、メタ ファイルを復元することをお勧めします。

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
