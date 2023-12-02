---
title: tiup mirror sign
---

# tiup mirror sign {#tiup-mirror-sign}

`tiup mirror sign`コマンドは、 TiUP [鏡](/tiup/tiup-mirror-reference.md)で定義されたメタデータ ファイル (*.json) に署名するために使用されます。これらのメタデータ ファイルは、ローカル ファイル システムに保存されるか、署名エントリを提供するために HTTP プロトコルを使用してリモートに保存される場合があります。

## 構文 {#syntax}

```shell
tiup mirror sign <manifest-file> [flags]
```

`<manifest-file>`は署名されるファイルのアドレスで、次の 2 つの形式があります。

-   HTTP または HTTPS で始まるネットワーク アドレス ( `http://172.16.5.5:8080/rotate/root.json`など)
-   ローカル ファイル パス。相対パスまたは絶対パスです。

ネットワーク アドレスの場合、このアドレスは次の機能を提供する必要があります。

-   署名されたファイルの完全なコンテンツ ( `signatures`フィールドを含む) を返す`http get`経由のアクセスをサポートします。
-   `http post`によるアクセスをサポートします。クライアントは、 `http get`によって返されたコンテンツの`signatures`フィールドに署名を追加し、このネットワーク アドレスにポストします。

## オプション {#options}

### -k、--キー {#k-key}

-   `{component}.json`ファイルの署名に使用される秘密キーの場所を指定します。
-   データ型: `STRING`
-   -   このオプションがコマンドで指定されていない場合、デフォルトで`"${TIUP_HOME}/keys/private.json"`が使用されます。

### - タイムアウト {#timeout}

-   ネットワーク経由の署名のアクセス タイムアウト時間を指定します。単位は秒です。
-   データ型: `INT`
-   デフォルト: 10

> **注記：**
>
> このオプションは、 `<manifest-file>`がネットワーク アドレスの場合にのみ有効です。

## 出力 {#output}

-   コマンドが正常に実行された場合、出力はありません。
-   ファイルが指定されたキーで署名されている場合、 TiUP はエラー`Error: this manifest file has already been signed by specified key`を報告します。
-   ファイルが有効なマニフェストではない場合、 TiUP はエラー`Error: unmarshal manifest: %s`を報告します。

[&lt;&lt; 前のページに戻る - TiUP Mirror コマンド一覧](/tiup/tiup-command-mirror.md#command-list)
