---
title: tiup cluster meta restore
summary: TiUPメタ ファイルを復元するには、クラスター名とバックアップ ファイル パスを指定して tiup cluster meta restore` コマンドを使用します。復元操作により現在のメタ ファイルが上書きされるため、ファイルが失われた場合にのみ実行する必要があります。`-h` または `--help` オプションはヘルプ情報を出力。出力にはtiup-clusterの実行ログが含まれます。
---

# tiup クラスタ メタ リストア {#tiup-cluster-meta-restore}

TiUPメタ ファイルを復元するには、 `tiup cluster meta restore`コマンドを使用してバックアップ ファイルから復元できます。

## 構文 {#syntax}

```shell
tiup cluster meta restore <cluster-name> <backup-file> [flags]
```

-   `<cluster-name>`操作対象となるクラスターの名前です。
-   `<backup-file>`はTiUPメタ バックアップ ファイルへのパスです。

> **注記：**
>
> 復元操作により、現在のメタ ファイルが上書きされます。メタ ファイルは、失われた場合にのみ復元することをお勧めします。

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
