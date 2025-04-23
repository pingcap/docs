---
title: tiup mirror sign
summary: tiup mirror sign` コマンドは、 TiUPミラー内のメタデータファイルに署名するために使用されます。ネットワークアドレスとローカルファイルパスをサポートします。オプションには、秘密鍵の場所の指定や、ネットワーク署名のアクセスタイムアウトの設定などがあります。実行が成功した場合、出力は表示されませんが、署名の重複やマニフェストファイルが無効な場合はエラーが報告されます。
---

# tiup mirror sign {#tiup-mirror-sign}

`tiup mirror sign`コマンドは、 TiUP [鏡](/tiup/tiup-mirror-reference.md)で定義されたメタデータファイル (*.json) に署名するために使用されます。これらのメタデータファイルは、ローカルファイルシステムに保存されるか、署名エントリを提供するために HTTP プロトコルを使用してリモートに保存されます。

## 構文 {#syntax}

```shell
tiup mirror sign <manifest-file> [flags]
```

`<manifest-file>`は署名するファイルのアドレスであり、次の 2 つの形式があります。

-   HTTPまたはHTTPSで始まるネットワークアドレス（例： `http://172.16.5.5:8080/rotate/root.json`
-   ローカルファイルパス（相対パスまたは絶対パス）

ネットワーク アドレスの場合、このアドレスは次の機能を提供する必要があります。

-   署名されたファイルの完全な内容 ( `signatures`フィールドを含む) を返す`http get`経由のアクセスをサポートします。
-   `http post`経由のアクセスをサポートします。クライアントは`http get`から返されたコンテンツの`signatures`フィールドに署名を追加し、このネットワークアドレスに投稿します。

## オプション {#options}

### -k, --key {#k-key}

-   `{component}.json`ファイルの署名に使用される秘密キーの場所を指定します。
-   データ型: `STRING`
-   -   このオプションがコマンドで指定されていない場合は、デフォルトで`"${TIUP_HOME}/keys/private.json"`使用されます。

### - タイムアウト {#timeout}

-   ネットワーク経由での署名のアクセスタイムアウト時間を指定します。単位は秒です。
-   データ型: `INT`
-   デフォルト: 10

> **注記：**
>
> このオプションは、 `<manifest-file>`がネットワーク アドレスの場合にのみ有効です。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   ファイルが指定されたキーで署名されている場合、 TiUP はエラー`Error: this manifest file has already been signed by specified key`報告します。
-   ファイルが有効なマニフェストでない場合、 TiUP はエラー`Error: unmarshal manifest: %s`報告します。

[&lt;&lt; 前のページに戻る - TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
