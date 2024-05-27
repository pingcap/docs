---
title: tiup cluster meta backup
summary: TiUPメタファイルは、クラスターの運用と保守に不可欠です。`tiup cluster meta backup` を使用して、ファイルを定期的にバックアップします。`tiup dm list` を使用してクラスター名を確認します。`--file` オプションでターゲット ディレクトリを指定します。ヘルプ情報を表示するには、`-h, --help` を使用します。出力には、 tiup-clusterの実行ログが含まれます。
---

# tiup クラスタ メタ バックアップ {#tiup-cluster-meta-backup}

TiUPメタ ファイルは、クラスターの運用と保守 (OM) に使用されます。このファイルが失われると、 TiUPを使用してクラスターを管理できなくなります。この状況を回避するには、 `tiup cluster meta backup`コマンドを使用して、 TiUPメタ ファイルを定期的にバックアップします。

## 構文 {#syntax}

```shell
tiup cluster meta backup <cluster-name> [flags]
```

`<cluster-name>`は操作対象となるクラスターの名前です。クラスター名を忘れた場合は、 [`tiup dm list`](/tiup/tiup-component-dm-list.md)コマンドで確認できます。

## オプション {#options}

### --file (文字列、デフォルトは現在のディレクトリ) {#file-string-defaults-to-the-current-directory}

TiUPメタ バックアップ ファイルを保存するターゲット ディレクトリを指定します。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
