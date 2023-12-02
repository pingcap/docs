---
title: tiup mirror set
---

# tiup mirror set {#tiup-mirror-set}

`tiup mirror set`コマンドは現在のミラーを切り替えるために使用され、ローカル ファイル システムとリモート ネットワーク アドレスという 2 つの形式のミラーをサポートします。

公式ミラーのアドレスは`https://tiup-mirrors.pingcap.com`です。

## 構文 {#syntax}

```shell
tiup mirror set <mirror-addr> [flags]
```

`<mirror-addr>`はミラー アドレスで、次の 2 つの形式があります。

-   ネットワーク アドレス: `http`または`https`で始まります。たとえば、 `http://172.16.5.5:8080` 、 `https://tiup-mirrors.pingcap.com` 。
-   ローカル ファイル パス: ミラー ディレクトリの絶対パス。たとえば、 `/path/to/local-tiup-mirror` 。

## オプション {#option}

### -r、--root {#r-root}

このオプションではルート証明書を指定します。

ミラーのセキュリティの最も重要な部分として、各ミラーのルート証明書は互いに異なります。ネットワーク ミラーを使用すると、中間者攻撃の被害を受ける可能性があります。このような攻撃を回避するには、ルート ネットワーク ミラーのルート証明書をローカルに手動でダウンロードすることをお勧めします。

    wget <mirror-addr>/root.json -O /path/to/local/root.json

手動チェックを実行してルート証明書が正しいことを確認し、ルート証明書を手動で指定してミラーを切り替えます。

    tiup mirror set <mirror-addr> -r /path/to/local/root.json

上記の手順で、 `wget`コマンドの前にミラーが攻撃された場合、ルート証明書が間違っていることがわかります。 `wget`コマンドの後にミラーが攻撃された場合、 TiUP はミラーがルート証明書と一致しないことを検出します。

-   データ型: `String`
-   デフォルト: `{mirror-dir}/root.json`

## 出力 {#output}

なし

[&lt;&lt; 前のページに戻る - TiUP Mirror コマンド一覧](/tiup/tiup-command-mirror.md#command-list)
