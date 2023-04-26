---
title: tiup dm restart
---

# tiup dm 再起動 {#tiup-dm-restart}

コマンド`tiup dm restart` 、指定されたクラスターのすべてまたは一部のサービスを再起動するために使用されます。

> **ノート：**
>
> 再起動プロセス中は、関連するサービスが一定期間利用できなくなります。

## 構文 {#syntax}

```shell
tiup dm restart <cluster-name> [flags]
```

`<cluster-name>` : 操作するクラスターの名前。クラスター名を忘れた場合は、 [クラスタ リスト](/tiup/tiup-component-cluster-list.md)コマンドで確認できます。

## オプション {#options}

### -N, --ノード {#n-node}

-   再起動するノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRING`
-   このオプションが指定されていない場合、 TiUP はデフォルトですべてのノードを再起動します。

> **ノート：**
>
> オプション`-R, --role`を同時に指定すると、 TiUP は`-N, --node`と`-R, --role`の両方の要件に一致するサービス ノードを再起動します。

### -R, --role {#r-role}

-   再起動するノードの役割を指定します。このオプションの値は、ノードの役割のコンマ区切りリストです。ノードの役割は、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドで返されるクラスター ステータス テーブルの 2 番目の列から取得できます。
-   データ型: `STRING`
-   このオプションが指定されていない場合、 TiUP はデフォルトですべてのロールのノードを再起動します。

> **ノート：**
>
> オプション`-N, --node`を同時に指定すると、 TiUP は`-N, --node`と`-R, --role`の両方の要件に一致するサービス ノードを再起動します。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## 出力 {#outputs}

サービスの再起動プロセスのログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
