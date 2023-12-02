---
title: tiup dm upgrade
---

# tiup dm upgrade {#tiup-dm-upgrade}

`tiup dm upgrade`コマンドは、指定したクラスターを特定のバージョンにアップグレードするために使用されます。

## 構文 {#syntax}

```shell
tiup dm upgrade <cluster-name> <version> [flags]
```

-   `<cluster-name>`は、操作対象のクラスターの名前です。クラスター名を忘れた場合は、 [`tiup dm list`](/tiup/tiup-component-dm-list.md)コマンドを使用して確認できます。
-   `<version>`は、アップグレード先のターゲット バージョンです ( `v7.5.0`など)。現在、新しいバージョンへのアップグレードのみが許可されており、以前のバージョンへのアップグレードは許可されていません。つまり、ダウングレードは許可されていません。夜間バージョンへのアップグレードも許可されていません。

## オプション {#options}

### &#x20;--offline {#offline}

-   現在のクラスターがオフラインであることを宣言します。このオプションを指定すると、 TiUP DM はサービスを再起動せずに、所定のクラスター コンポーネントのバイナリ ファイルのみを置き換えます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## 出力 {#output}

サービスのアップグレード プロセスのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
