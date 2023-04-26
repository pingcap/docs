---
title: tiup dm upgrade
---

# tiup dm upgrade {#tiup-dm-upgrade}

`tiup dm upgrade`コマンドは、指定されたクラスターを特定のバージョンにアップグレードするために使用されます。

## 構文 {#syntax}

```shell
tiup dm upgrade <cluster-name> <version> [flags]
```

-   `<cluster-name>`は操作対象のクラスターの名前です。クラスター名を忘れた場合は、 [`tiup dm list`](/tiup/tiup-component-dm-list.md)コマンドを使用して確認できます。
-   `<version>`は、 `v6.5.2`などのアップグレード先のターゲット バージョンです。現在、新しいバージョンへのアップグレードのみが許可されており、以前のバージョンへのアップグレードは許可されていません。つまり、ダウングレードは許可されていません。夜間バージョンへのアップグレードも許可されていません。

## オプション {#options}

### &#x20;--offline {#offline}

-   現在のクラスターがオフラインであることを宣言します。このオプションを指定すると、 TiUP DM はサービスを再起動せずに、クラスタ コンポーネントのバイナリ ファイルのみを置き換えます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## 出力 {#output}

サービスのアップグレード プロセスのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
