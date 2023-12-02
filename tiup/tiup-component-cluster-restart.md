---
title: tiup cluster restart
---

# tiup cluster restart {#tiup-cluster-restart}

コマンド`tiup cluster restart` 、指定したクラスターのサービスのすべてまたは一部を再起動するために使用されます。

> **注記：**
>
> 再起動プロセス中、関連サービスは一定期間利用できなくなります。

## 構文 {#syntax}

```shell
tiup cluster restart <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N、--node {#n-node}

-   再起動するノードを指定します。このオプションの値は、ノード ID のカンマ区切りリストです。ノード ID は、 `tiup cluster display`コマンドによって返される[クラスタステータステーブル](/tiup/tiup-component-cluster-display.md)の最初の列から取得できます。
-   データ型: `STRING`
-   このオプションが指定されていない場合、 TiUP はデフォルトですべてのノードを再起動します。

> **注記：**
>
> オプション`-R, --role`が同時に指定された場合、 TiUP は`-N, --node`と`-R, --role`の両方の要件を満たすサービス ノードを再起動します。

### -R、--役割 {#r-role}

-   再起動するノードの役割を指定します。このオプションの値は、ノードの役割のカンマ区切りリストです。 `tiup cluster display`コマンドによって返される[クラスタステータステーブル](/tiup/tiup-component-cluster-display.md)の 2 番目の列からノードの役割を取得できます。
-   データ型: `STRING`
-   このオプションが指定されていない場合、 TiUP はデフォルトですべてのロールのノードを再起動します。

> **注記：**
>
> オプション`-N, --node`が同時に指定された場合、 TiUP は`-N, --node`と`-R, --role`の両方の要件を満たすサービス ノードを再起動します。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## 出力 {#outputs}

サービスの再起動処理のログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
