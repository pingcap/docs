---
title: tiup cluster tls
summary: tiup cluster tls` コマンドは、クラスタコンポーネント間の TLS (Transport Layer Security) を有効または無効にするために使用されます。
---

# TIUP クラスター TLS {#tiup-cluster-tls}

`tiup cluster tls`コマンドは、クラスタコンポーネント間で TLS (Transport Layer Security) を有効にするために使用されます。このコマンドは、自己署名証明書を自動的に生成し、クラスタ内の各ノードに配布します。

## 構文 {#syntax}

```shell
tiup cluster tls <cluster-name> <enable/disable> [flags]
```

`<cluster-name>` TLS を有効または無効にするクラスターを指定します。

> **Note:**
>
> 現在、 `tiup cluster tls`コマンドは、単一の PD ノードを持つクラスタでのみ TLS の有効化または無効化をサポートしています。複数の PD ノードを持つクラスタの場合、TLS ステータスの切り替えによって PD ノード間で通信例外が発生する可能性があるため、 `tiup cluster tls`コマンドを直接実行するとエラーが返されます。複数の PD ノードを持つクラスタで TLS を有効化または無効化するには、まず PD ノードを 1 つのノードに[`scale-in`](/tiup/tiup-component-cluster-scale-in.md)から、 `tiup cluster tls`コマンドを実行してください。

## オプション {#options}

### --クリーン証明書 {#clean-certificate}

-   TLSを無効にする場合は、このオプションを使用して以前に生成された証明書を削除してください。
-   データタイプ: `BOOLEAN`
-   デフォルト: `false`
-   このオプションを指定しない場合、TLSを再度有効にした際に、古い証明書が再利用される可能性があります。

### &#x20;--force {#force}

-   クラスターの現在のTLSステータスに関係なく、TLSを強制的に有効または無効にします。
-   データタイプ: `BOOLEAN`
-   デフォルト: `false`
-   このオプションを指定しない場合、クラスターが既に要求された状態にある場合は、操作はスキップされます。

### --証明書を再読み込み {#reload-certificate}

-   TLSを有効にする場合は、このオプションを使用して証明書を再生成してください。
-   データタイプ: `BOOLEAN`
-   デフォルト: `false`
-   このオプションを指定しない場合、既に証明書が存在する場合は、新しい証明書は生成されません。

### -h, --help {#h-help}

-   ヘルプ情報を表示します。
-   データタイプ: `BOOLEAN`
-   デフォルト: `false`

## 出力 {#output}

tiup-clusterコマンドの実行ログ。
