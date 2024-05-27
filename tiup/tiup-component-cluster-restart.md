---
title: tiup cluster restart
summary: tiup cluster restart コマンドは、指定されたクラスター内のサービスを再起動するために使用されます。再起動中は、サービスは使用できません。`-N、--node` および `-R、--role` オプションを使用して、再起動するノードまたはロールを指定できます。出力は、サービス再起動プロセスのログです。
---

# tiup cluster restart {#tiup-cluster-restart}

コマンド`tiup cluster restart`は、指定されたクラスターのすべてまたは一部のサービスを再起動するために使用されます。

> **注記：**
>
> 再起動プロセス中は、関連するサービスが一定期間利用できなくなります。

## 構文 {#syntax}

```shell
tiup cluster restart <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスターリスト](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N、--ノード {#n-node}

-   再起動するノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 `tiup cluster display`コマンドによって返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の最初の列から取得できます。
-   データ型: `STRING`
-   このオプションを指定しない場合、 TiUP はデフォルトですべてのノードを再起動します。

> **注記：**
>
> オプション`-R, --role`を同時に指定すると、 TiUP は`-N, --node`と`-R, --role`の両方の要件に一致するサービス ノードを再起動します。

### -R, --役割 {#r-role}

-   再起動するノードのロールを指定します。このオプションの値は、ノードのロールのコンマ区切りリストです。ノードのロールは、 `tiup cluster display`コマンドによって返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の 2 番目の列から取得できます。
-   データ型: `STRING`
-   このオプションを指定しない場合、 TiUP はデフォルトですべてのロールのノードを再起動します。

> **注記：**
>
> オプション`-N, --node`を同時に指定すると、 TiUP は`-N, --node`と`-R, --role`の両方の要件に一致するサービス ノードを再起動します。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、デフォルトで値`false`で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

## 出力 {#outputs}

サービスの再起動プロセスのログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
