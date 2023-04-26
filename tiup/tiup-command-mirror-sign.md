---
title: tiup mirror sign
---

# tiup mirror sign {#tiup-mirror-sign}

`tiup mirror sign`コマンドは、 TiUP [鏡](/tiup/tiup-mirror-reference.md)で定義されているメタデータ ファイル (*.json) に署名するために使用されます。これらのメタデータ ファイルは、ローカル ファイル システムに保存されるか、HTTP プロトコルを使用してリモートに保存され、署名エントリを提供します。

## 構文 {#syntax}

```shell
tiup mirror sign <manifest-file> [flags]
```

`<manifest-file>`は署名するファイルのアドレスで、次の 2 つの形式があります。

-   `http://172.16.5.5:8080/rotate/root.json`など、HTTP または HTTPS で始まるネットワーク アドレス
-   相対パスまたは絶対パスであるローカル ファイル パス

ネットワーク アドレスの場合、このアドレスは次の機能を提供する必要があります。

-   署名されたファイルの完全なコンテンツ ( `signatures`フィールドを含む) を返す`http get`経由のアクセスをサポートします。
-   `http post`経由のアクセスをサポートします。クライアントは、 `http get`から返されたコンテンツの`signatures`フィールドに署名を追加し、このネットワーク アドレスに投稿します。

## オプション {#options}

### -k, --key {#k-key}

-   `{component}.json`ファイルの署名に使用される秘密鍵の場所を指定します。
-   データ型: `STRING`
-   -   このオプションがコマンドで指定されていない場合、デフォルトで`"${TIUP_HOME}/keys/private.json"`が使用されます。

### - タイムアウト {#timeout}

-   ネットワーク経由で署名するためのアクセス タイムアウト時間を指定します。単位は秒です。
-   データ型: `INT`
-   デフォルト: 10

> **ノート：**
>
> このオプションは、 `<manifest-file>`がネットワーク アドレスの場合にのみ有効です。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   ファイルが指定されたキーによって署名されている場合、 TiUP はエラー`Error: this manifest file has already been signed by specified key`を報告します。
-   ファイルが有効なマニフェストでない場合、 TiUP はエラー`Error: unmarshal manifest: %s`を報告します。

[&lt;&lt; 前のページに戻る - TiUP Mirror コマンド一覧](/tiup/tiup-command-mirror.md#command-list)
