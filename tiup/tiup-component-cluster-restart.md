---
title: tiup cluster restart
summary: tiup cluster restart` コマンドは、指定されたクラスター内のサービスを再起動するために使用されます。再起動中は、サービスは利用できません。`-N, --node` オプションと `-R, --role` オプションを使用して、再起動するノードまたはロールを指定できます。出力は、サービス再起動プロセスのログです。
---

# tiup cluster restart {#tiup-cluster-restart}

コマンド`tiup cluster restart` 、指定されたクラスターのすべてまたは一部のサービスを再起動するために使用されます。

> **注記：**
>
> 再起動プロセス中は、関連するサービスが一定期間利用できなくなります。

## 構文 {#syntax}

```shell
tiup cluster restart <cluster-name> [flags]
```

`<cluster-name>` : 操作対象のクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --node {#n-node}

-   再起動するノードを指定します。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、コマンド`tiup cluster display`で返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の最初の列から取得できます。
-   データ型: `STRING`
-   このオプションを指定しない場合、 TiUP はデフォルトですべてのノードを再起動します。

> **注記：**
>
> オプション`-R, --role`同時に指定すると、 TiUP は`-N, --node`と`-R, --role`両方の要件に一致するサービス ノードを再起動します。

### -R, --role {#r-role}

-   再起動するノードのロールを指定します。このオプションの値は、ノードのロールをカンマ区切りでリストしたものです。ノードのロールは、 `tiup cluster display`コマンドで返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の2列目から取得できます。
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

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
