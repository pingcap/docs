---
title: tiup cluster meta restore
summary: TiUPメタファイルを復元するには、クラスター名とバックアップファイルのパスを指定して「tiup cluster meta restore」コマンドを使用します。復元操作は現在のメタファイルを上書きするため、ファイルが失われた場合にのみ実行してください。「-h」または「--help」オプションを指定するとヘルプ情報が出力。出力には、 tiup-clusterの実行ログが含まれます。
---

# tiup クラスタ メタ リストア {#tiup-cluster-meta-restore}

TiUPメタ ファイルを復元するには、 `tiup cluster meta restore`コマンドを使用してバックアップ ファイルから復元できます。

## 構文 {#syntax}

```shell
tiup cluster meta restore <cluster-name> <backup-file> [flags]
```

-   `<cluster-name>`は操作対象となるクラスターの名前です。
-   `<backup-file>`はTiUPメタ バックアップ ファイルへのパスです。

> **注記：**
>
> 復元操作により、現在のメタファイルが上書きされます。メタファイルは、失われた場合にのみ復元することをお勧めします。

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
