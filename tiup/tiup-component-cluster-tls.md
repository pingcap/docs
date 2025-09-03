---
title: tiup cluster tls
summary: tiup cluster tls` コマンドは、クラスター コンポーネント間の TLS (トランスポート層Security) を有効または無効にするために使用されます。
---

# tiup クラスター tls {#tiup-cluster-tls}

`tiup cluster tls`コマンドは、クラスタコンポーネント間の TLS (Transport Layer Security) を有効にするために使用されます。このコマンドは、クラスタ内の各ノードに自己署名証明書を自動的に生成し、配布します。

## 構文 {#syntax}

```shell
tiup cluster tls <cluster-name> <enable/disable> [flags]
```

`<cluster-name>` 、TLS を有効または無効にするクラスターを指定します。

## オプション {#options}

### --クリーン証明書 {#clean-certificate}

-   TLS を無効にする場合は、このオプションを使用して、以前に生成された証明書をクリーンアップします。
-   データ型: `BOOLEAN`
-   デフォルト: `false`
-   このオプションを指定しないと、TLS を再度有効にしたときに古い証明書が再利用される可能性があります。

### &#x20;--force {#force}

-   クラスターの現在の TLS ステータスに関係なく、TLS を強制的に有効化または無効化します。
-   データ型: `BOOLEAN`
-   デフォルト: `false`
-   このオプションを指定しないと、クラスターがすでに要求された状態にある場合、操作はスキップされます。

### --reload-certificate {#reload-certificate}

-   TLS を有効にする場合は、このオプションを使用して証明書を再生成します。
-   データ型: `BOOLEAN`
-   デフォルト: `false`
-   このオプションを指定しないと、証明書がすでに存在する場合は新しい証明書は生成されません。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: `false`

## 出力 {#output}

tiup-clusterコマンドの実行ログ。
