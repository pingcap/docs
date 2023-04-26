---
title: tiup cluster start
---

# tiup cluster start {#tiup-cluster-start}

`tiup cluster start`コマンドは、指定されたクラスターのすべてのサービスまたは一部のサービスを開始するために使用されます。

## 構文 {#syntax}

```shell
tiup cluster start <cluster-name> [flags]
```

`<cluster-name>`は、操作するクラスターの名前です。クラスター名を忘れた場合は、 [`tiup cluster list`](/tiup/tiup-component-cluster-list.md)コマンドを使用して確認できます。

## オプション {#options}

### - 初期化 {#init}

安全な方法でクラスターを開始します。クラスタを初めて起動するときは、このオプションを使用することをお勧めします。このメソッドは、起動時に TiDB root ユーザーのパスワードを生成し、コマンド ライン インターフェイスでパスワードを返します。

> **ノート：**
>
> -   TiDB クラスターを安全に起動した後、パスワードなしで root ユーザーを使用してデータベースにログインすることはできません。したがって、今後のログインのために、コマンド ラインから返されるパスワードを記録する必要があります。
> -   パスワードは一度だけ生成されます。パスワードを記録していない、または忘れた場合は、 [`root`パスワードを忘れる](/user-account-management.md#forget-the-root-password)を参照してパスワードを変更してください。

### -N, --ノード {#n-node}

-   開始するノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。 `tiup cluster display`コマンドで返される[クラスタ ステータス テーブル](/tiup/tiup-component-cluster-display.md)の最初の列からノード ID を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、デフォルトですべてのノードが開始されます。

> **ノート：**
>
> `-R, --role`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -R, --role {#r-role}

-   起動するノードの役割を指定します。このオプションの値は、ノードの役割のコンマ区切りリストです。 `tiup cluster display`コマンドによって返される[クラスタ ステータス テーブル](/tiup/tiup-component-cluster-display.md)の 2 列目から、ノードの役割を取得できます。
-   データ型: `STRINGS`
-   このオプションがコマンドで指定されていない場合、すべての役割がデフォルトで開始されます。

> **ノート：**
>
> `-N, --node`オプションを同時に指定した場合、 `-N, --node`と`-R, --role`の両方の指定に一致するサービスノードだけが起動されます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## 出力 {#output}

サービス開始のログ。

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
