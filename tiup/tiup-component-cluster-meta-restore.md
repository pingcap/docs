---
title: tiup cluster meta restore
---

# tiup クラスタ メタ リストア {#tiup-cluster-meta-restore}

TiUPメタ ファイルを復元するには、 `tiup cluster meta restore`コマンドを使用してバックアップ ファイルから復元します。

## 構文 {#syntax}

```shell
tiup cluster meta restore <cluster-name> <backup-file> [flags]
```

-   `<cluster-name>`は操作対象のクラスターの名前です。
-   `<backup-file>`は、 TiUPメタ バックアップ ファイルへのパスです。

> **ノート：**
>
> 復元操作は、現在のメタ ファイルを上書きします。メタ ファイルは、失われた場合にのみ復元することをお勧めします。

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を何も渡さないようにします。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
