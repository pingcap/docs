---
title: tiup mirror sign
---

# tiup mirror sign {#tiup-mirror-sign}

`tiup mirror sign`コマンドは、TiUP [鏡](/tiup/tiup-mirror-reference.md)で定義されたメタデータファイル（* .json）に署名するために使用されます。これらのメタデータファイルは、ローカルファイルシステムに保存されるか、HTTPプロトコルを使用してリモートに保存されて署名エントリを提供します。

## 構文 {#syntax}

```shell
tiup mirror sign <manifest-file> [flags]
```

`<manifest-file>`は署名するファイルのアドレスで、次の2つの形式があります。

-   `http://172.16.5.5:8080/rotate/root.json`などのHTTPまたはHTTPSで始まるネットワークアドレス
-   相対パスまたは絶対パスであるローカルファイルパス

ネットワークアドレスの場合、このアドレスは次の機能を提供する必要があります。

-   署名されたファイルの完全なコンテンツ（ `signatures`フィールドを含む）を返す`http get`を介したアクセスをサポートします。
-   `http post`を介したアクセスをサポートします。クライアントは、 `http get`によって返されるコンテンツの`signatures`フィールドに署名を追加し、このネットワークアドレスに投稿します。

## オプション {#options}

### -k、-key {#k-key}

-   `{component}.json`ファイルの署名に使用される秘密鍵の場所を指定します。
-   データ型： `STRING`
-   -   このオプションがコマンドで指定されていない場合、デフォルトで`"${TIUP_HOME}/keys/private.json"`が使用されます。

### - タイムアウト {#timeout}

-   ネットワークを介して署名するためのアクセスタイムアウト時間を指定します。単位は秒単位です。
-   データ型： `INT`
-   デフォルト：10

> **ノート：**
>
> このオプションは、 `<manifest-file>`がネットワークアドレスの場合にのみ有効です。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   ファイルが指定されたキーで署名されている場合、TiUPはエラー`Error: this manifest file has already been signed by specified key`を報告します。
-   ファイルが有効なマニフェストでない場合、TiUPはエラー`Error: unmarshal manifest: %s`を報告します。

[&lt;&lt;前のページに戻る-TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
