---
title: tiup cluster meta backup
---

# tiup クラスターのメタバックアップ {#tiup-cluster-meta-backup}

TiUPメタ ファイルは、クラスターの運用と保守 (OM) に使用されます。このファイルが失われると、 TiUP を使用してクラスターを管理することができなくなります。この状況を回避するには、 `tiup cluster meta backup`コマンドを使用してTiUPメタ ファイルを定期的にバックアップします。

## 構文 {#syntax}

```shell
tiup cluster meta backup <cluster-name> [flags]
```

`<cluster-name>`は、操作対象のクラスターの名前です。クラスター名を忘れた場合は、 [`tiup dm list`](/tiup/tiup-component-dm-list.md)コマンドを使用して確認できます。

## オプション {#options}

### --file (文字列、デフォルトは現在のディレクトリ) {#file-string-defaults-to-the-current-directory}

TiUPメタ バックアップ ファイルを保存するターゲット ディレクトリを指定します。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
