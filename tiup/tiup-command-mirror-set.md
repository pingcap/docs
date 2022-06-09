---
title: tiup mirror set
---

# tiup mirror set {#tiup-mirror-set}

`tiup mirror set`コマンドは、現在のミラーを切り替えるために使用され、ローカルファイルシステムとリモートネットワークアドレスの2つの形式のミラーをサポートします。

公式ミラーのアドレスは`https://tiup-mirrors.pingcap.com`です。

## 構文 {#syntax}

```shell
tiup mirror set <mirror-addr> [flags]
```

`<mirror-addr>`はミラーアドレスで、次の2つの形式があります。

-   ネットワークアドレス： `http`または`https`で始まります。 `https://tiup-mirrors.pingcap.com` `http://172.16.5.5:8080`
-   ローカルファイルパス：ミラーディレクトリの絶対パス。たとえば、 `/path/to/local-tiup-mirror` 。

## オプション {#option}

### -r、-root {#r-root}

このオプションは、ルート証明書を指定します。

ミラーセキュリティの最も重要な部分として、各ミラーのルート証明書は互いに異なります。ネットワークミラーを使用すると、man-in-the-middle攻撃を受ける可能性があります。このような攻撃を回避するには、ルートネットワークミラーのルート証明書をローカルに手動でダウンロードすることをお勧めします。

```
wget <mirror-addr>/root.json -O /path/to/local/root.json
```

手動チェックを実行してルート証明書が正しいことを確認してから、ルート証明書を手動で指定してミラーを切り替えます。

```
tiup mirror set <mirror-addr> -r /path/to/local/root.json
```

上記の手順で、 `wget`コマンドの前にミラーが攻撃された場合、ルート証明書が正しくないことがわかります。 `wget`コマンドの後にミラーが攻撃された場合、TiUPはミラーがルート証明書と一致しないことを検出します。

-   データ型： `String`
-   デフォルト： `{mirror-dir}/root.json`

## 出力 {#output}

なし

[&lt;&lt;前のページに戻る-TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
