---
title: tiup dm restart
summary: tiup dm restart`コマンドは、指定されたクラスタ内のサービスを再起動するために使用されます。再起動中は、サービスは利用できません。構文は`tiup dm restart <cluster-name> [flags]`です。オプションには、再起動するノードを指定する-N、再起動するノードの役割を指定する-R、ヘルプ情報を表示する-hがあります。出力は、サービス再起動プロセスのログです。
---

# tiup dm 再起動 {#tiup-dm-restart}

コマンド`tiup dm restart` 、指定されたクラスターのすべてまたは一部のサービスを再起動するために使用されます。

> **注記：**
>
> 再起動プロセス中は、関連するサービスが一定期間利用できなくなります。

## 構文 {#syntax}

```shell
tiup dm restart <cluster-name> [flags]
```

`<cluster-name>` : 操作対象のクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --node {#n-node}

-   再起動するノードを指定します。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドで返されるクラスタステータステーブルの最初の列から取得できます。
-   データ型: `STRING`
-   このオプションを指定しない場合、 TiUP はデフォルトですべてのノードを再起動します。

> **注記：**
>
> オプション`-R, --role`同時に指定すると、 TiUP は`-N, --node`と`-R, --role`両方の要件に一致するサービス ノードを再起動します。

### -R, --role {#r-role}

-   再起動するノードの役割を指定します。このオプションの値は、ノードの役割をカンマ区切りでリストしたものです。ノードの役割は、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドで返されるクラスターステータステーブルの2列目から取得できます。
-   データ型: `STRING`
-   このオプションを指定しない場合、 TiUP はデフォルトですべてのロールのノードを再起動します。

> **注記：**
>
> オプション`-N, --node`同時に指定すると、 TiUP は`-N, --node`と`-R, --role`両方の要件に一致するサービス ノードを再起動します。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## 出力 {#outputs}

サービスの再起動プロセスのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
