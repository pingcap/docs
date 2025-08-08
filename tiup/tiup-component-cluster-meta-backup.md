---
title: tiup cluster meta backup
summary: TiUPメタファイルは、クラスタの運用と保守に不可欠です。定期的にファイルをバックアップするには、tiup cluster meta backup`コマンドを使用してください。クラスタ名を確認するには、`tiup dm listコマンドを使用してください。`--file`オプションでターゲットディレクトリを指定してください。ヘルプ情報を表示するには、`-h, --helpコマンドを使用してください。出力には、tiup-clusterの実行ログが含まれます。
---

# tiup クラスタメタバックアップ {#tiup-cluster-meta-backup}

TiUPメタファイルはクラスタの運用保守（OM）に使用されます。このファイルが失われると、 TiUPを使用してクラスタを管理できなくなります。このような状況を回避するには、 `tiup cluster meta backup`コマンドを使用してTiUPメタファイルを定期的にバックアップしてください。

## 構文 {#syntax}

```shell
tiup cluster meta backup <cluster-name> [flags]
```

`<cluster-name>`は操作対象となるクラスターの名前です。クラスター名を忘れた場合は、 [`tiup cluster list`](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### --file (文字列、デフォルトは現在のディレクトリ) {#file-string-defaults-to-the-current-directory}

TiUPメタ バックアップ ファイルを保存するターゲット ディレクトリを指定します。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
