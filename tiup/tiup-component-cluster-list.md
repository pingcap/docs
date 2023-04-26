---
title: tiup cluster list
---

# tiup cluster list {#tiup-cluster-list}

tiup-cluster は、同じ制御マシンを使用した複数のクラスターのデプロイをサポートしています。 `tiup cluster list`コマンドは、この制御マシンを使用して現在ログインしているユーザーによってデプロイされたすべてのクラスターを出力します。

> **ノート：**
>
> デプロイされたクラスター データは、デフォルトで`~/.tiup/storage/cluster/clusters/`ディレクトリに保存されるため、同じ制御マシンで、現在ログインしているユーザーは、他のユーザーによってデプロイされたクラスターを表示できません。

## 構文 {#syntax}

```shell
tiup cluster list [flags]
```

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を何も渡さないようにします。

## 出力 {#outputs}

次のフィールドを含むテーブルを出力します。

-   名前: クラスター名
-   ユーザー: 展開ユーザー
-   バージョン: クラスターのバージョン
-   パス: 制御マシン上のクラスター展開データのパス
-   PrivateKey: クラスターの接続に使用される秘密鍵のパス

[&lt;&lt; 前のページに戻る - TiUP クラスタコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
