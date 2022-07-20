---
title: tiup cluster restart
---

# tiup cluster restart {#tiup-cluster-restart}

コマンド`tiup cluster restart`は、指定されたクラスタのすべてまたは一部のサービスを再始動するために使用されます。

> **ノート：**
>
> 再起動プロセス中、関連するサービスは一定期間利用できません。

## 構文 {#syntax}

```shell
tiup cluster restart <cluster-name> [flags]
```

`<cluster-name>` ：操作するクラスタの名前。クラスタ名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N、-node {#n-node}

-   再起動するノードを指定します。このオプションの値は、ノードIDのコンマ区切りのリストです。 `tiup cluster display`コマンドによって返された[クラスタステータステーブル](/tiup/tiup-component-cluster-display.md)の最初の列からノードIDを取得できます。
-   データ型： `STRING`
-   このオプションが指定されていない場合、TiUPはデフォルトですべてのノードを再起動します。

> **ノート：**
>
> オプション`-R, --role`が同時に指定された場合、TiUPは`-N, --node`と`-R, --role`の両方の要件に一致するサービスノードを再起動します。

### -R、-role {#r-role}

-   再起動するノードの役割を指定しました。このオプションの値は、ノードの役割のコンマ区切りのリストです。 `tiup cluster display`コマンドによって返される[クラスタステータステーブル](/tiup/tiup-component-cluster-display.md)の2番目の列からノードの役割を取得できます。
-   データ型： `STRING`
-   このオプションが指定されていない場合、TiUPはデフォルトですべての役割のノードを再起動します。

> **ノート：**
>
> オプション`-N, --node`が同時に指定された場合、TiUPは`-N, --node`と`-R, --role`の両方の要件に一致するサービスノードを再起動します。

### -h、-help {#h-help}

-   ヘルプ情報を印刷します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#outputs}

サービス再開プロセスのログ。

[&lt;&lt;前のページに戻る-TiUPクラスターコマンドリスト](/tiup/tiup-component-cluster.md#command-list)
