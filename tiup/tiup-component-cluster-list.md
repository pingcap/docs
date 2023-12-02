---
title: tiup cluster list
---

# tiup cluster list {#tiup-cluster-list}

tiup-cluster は、同じ制御マシンを使用した複数のクラスターの展開をサポートします。 `tiup cluster list`コマンドは、この制御マシンを使用して現在ログインしているユーザーによってデプロイされているすべてのクラスターを出力します。

> **注記：**
>
> デプロイされたクラスター データはデフォルトで`~/.tiup/storage/cluster/clusters/`ディレクトリに保存されるため、同じ制御マシン上では、現在ログインしているユーザーは他のユーザーがデプロイしたクラスターを表示できません。

## 構文 {#syntax}

```shell
tiup cluster list [flags]
```

## オプション {#options}

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#outputs}

次のフィールドを含むテーブルを出力します。

-   名前: クラスター名
-   ユーザー: 導入ユーザー
-   バージョン: クラスターのバージョン
-   パス: 制御マシン上のクラスター展開データのパス
-   PrivateKey: クラスターの接続に使用される秘密キーのパス

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
