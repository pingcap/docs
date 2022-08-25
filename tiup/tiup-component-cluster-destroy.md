---
title: tiup cluster destroy
---

# tiup cluster destroy {#tiup-cluster-destroy}

アプリケーションがオフラインになった後、クラスタが占有していたマシンを解放して他のアプリケーションが使用できるようにする場合は、クラスタ上のデータとデプロイされたバイナリ ファイルをクリーンアップする必要があります。クラスタを破棄するには、 `tiup cluster destroy`コマンドで次の操作を実行します。

-   クラスタを停止します。
-   サービスごとに、そのログ ディレクトリ、展開ディレクトリ、およびデータ ディレクトリを削除します。
-   tiup-cluster で各サービスのデータディレクトリやデプロイディレクトリの親ディレクトリを作成した場合は、親ディレクトリも削除してください。

## 構文 {#syntax}

```shell
tiup cluster destroy <cluster-name> [flags]
```

`<cluster-name>` : 破棄するクラスタの名前。

## オプション {#options}

### &#x20;--force {#force}

-   場合によっては、クラスタの一部のノードがダウンしており、SSH 経由でノードに接続して操作することができません。現時点では、 `--force`オプションを使用してこれらのエラーを無視できます。
-   データ型: `Boolean`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`を渡すか、値を何も渡さないようにします。

### --retain-node-data {#retain-node-data}

-   データを保持する必要があるノードを指定します。複数のノードを指定する必要がある場合は、このオプションを複数回使用します: `--retain-node-data <node-A> --retain-node-data <node-B>` .
-   データ型: `StringArray`
-   デフォルト: 空

### --retain-role-data {#retain-role-data}

-   データを保持する必要がある役割を指定します。複数のロールを指定する必要がある場合は、このオプションを複数回使用します: `--retain-role-data <role-A> --retain-role-data <role-B>` .
-   データ型: `StringArray`
-   デフォルト: 空

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`を渡すか、値を何も渡さないようにします。

## 出力 {#output}

tiup-cluster の実行ログ。

[&lt;&lt; 前のページに戻る - TiUP Clusterコマンド一覧](/tiup/tiup-component-cluster.md#command-list)
