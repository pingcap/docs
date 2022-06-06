---
title: tiup dm restart
---

# tiup dm restart {#tiup-dm-restart}

コマンド`tiup dm restart`は、指定されたクラスタのすべてまたは一部のサービスを再起動するために使用されます。

> **ノート：**
>
> 再起動プロセス中、関連するサービスは一定期間利用できません。

## 構文 {#syntax}

```shell
tiup dm restart <cluster-name> [flags]
```

`<cluster-name>` ：操作するクラスタの名前。クラスタ名を忘れた場合は、 [クラスタリスト](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N、-node {#n-node}

-   再起動するノードを指定します。このオプションの値は、ノードIDのコンマ区切りのリストです。 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドによって返されるクラスタステータステーブルの最初の列からノードIDを取得できます。
-   データ型： `STRING`
-   このオプションが指定されていない場合、TiUPはデフォルトですべてのノードを再起動します。

> **ノート：**
>
> オプション`-R, --role`が同時に指定された場合、TiUPは`-N, --node`と`-R, --role`の両方の要件に一致するサービスノードを再起動します。

### -R、-role {#r-role}

-   再起動するノードの役割を指定します。このオプションの値は、ノードの役割のコンマ区切りのリストです。ノードの役割は、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドによって返されるクラスタステータステーブルの2番目の列から取得できます。
-   データ型： `STRING`
-   このオプションが指定されていない場合、TiUPはデフォルトですべての役割のノードを再起動します。

> **ノート：**
>
> オプション`-N, --node`が同時に指定された場合、TiUPは`-N, --node`と`-R, --role`の両方の要件に一致するサービスノードを再起動します。

### -h、-help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#outputs}

サービス再開プロセスのログ。

[&lt;&lt;前のページに戻る-TiUPDMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
