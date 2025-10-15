---
title: tiup mirror set
summary: "tiup mirror set` コマンドは、現在のミラーをローカルファイルシステムとリモートネットワークアドレスの間で切り替えます。公式ミラーアドレスは ` <a href="https://tiup-mirrors.pingcap.com`">https://tiup-mirrors.pingcap.com</a>です。ミラーアドレスを設定するには、`tiup mirror set <mirror-addr>` を使用します。中間者攻撃を防ぐため、ネットワークミラーのルート証明書を指定するには、`-r, --root` オプションを使用します。出力は生成されません。"
---

# tiup mirror set {#tiup-mirror-set}

`tiup mirror set`コマンドは現在のミラーを切り替えるために使用され、ローカル ファイル システムとリモート ネットワーク アドレスの 2 つの形式のミラーをサポートします。

公式ミラーのアドレスは`https://tiup-mirrors.pingcap.com`です。

## 構文 {#syntax}

```shell
tiup mirror set <mirror-addr> [flags]
```

`<mirror-addr>`はミラー アドレスであり、次の 2 つの形式があります。

-   ネットワークアドレス: `http`または`https`で始まります。例: `http://172.16.5.5:8080` 、 `https://tiup-mirrors.pingcap.com` 。
-   ローカルファイルパス: ミラーディレクトリの絶対パス。例: `/path/to/local-tiup-mirror` 。

## オプション {#option}

### -r, --root {#r-root}

このオプションはルート証明書を指定します。

ミラーセキュリティにおいて最も重要な要素として、各ミラーのルート証明書は互いに異なります。ネットワークミラーを使用すると、中間者攻撃の被害を受ける可能性があります。このような攻撃を回避するには、ルートネットワークミラーのルート証明書を手動でローカルにダウンロードすることをお勧めします。

    wget <mirror-addr>/root.json -O /path/to/local/root.json

手動でチェックを実行してルート証明書が正しいことを確認し、ルート証明書を手動で指定してミラーを切り替えます。

    tiup mirror set <mirror-addr> -r /path/to/local/root.json

上記の手順では、 `wget`コマンドの前にミラーが攻撃された場合、ルート証明書が正しくないことが分かります。3 `wget`コマンドの後にミラーが攻撃された場合、 TiUPはミラーがルート証明書と一致しないことを検出します。

-   データ型: `String`
-   デフォルト: `{mirror-dir}/root.json`

## 出力 {#output}

なし

[&lt;&lt; 前のページに戻る - TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
