---
title: tiup dm upgrade
---

# tiup dm upgrade {#tiup-dm-upgrade}

`tiup dm upgrade`コマンドは、指定されたクラスタを特定のバージョンにアップグレードするために使用されます。

## 構文 {#syntax}

```shell
tiup dm upgrade <cluster-name> <version> [flags]
```

-   `<cluster-name>`は、操作対象のクラスタの名前です。クラスタ名を忘れた場合は、 [`tiup dm list`](/tiup/tiup-component-dm-list.md)コマンドで確認できます。
-   `<version>`は、アップグレード先のターゲットバージョンです。現在、新しいバージョンへのアップグレードのみが許可されており、以前のバージョンへのアップグレードは許可されていません。つまり、ダウングレードは許可されていません。ナイトリーバージョンへのアップグレードも許可されていません。

## オプション {#options}

### - オフライン {#offline}

-   現在のクラスタがオフラインであることを宣言します。このオプションを指定すると、TiUP DMは、サービスを再起動せずに、クラスタコンポーネントのバイナリファイルのみを置き換えます。

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#output}

サービスアップグレードプロセスのログ。

[&lt;&lt;前のページに戻る-TiUPDMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
