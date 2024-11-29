---
title: tiup cluster destroy
summary: tiup cluster destroyコマンドは、クラスターを停止し、各サービスのログ、デプロイメント、およびデータ ディレクトリを削除します。また、 tiup-clusterによって作成された親ディレクトリも削除します。オプションには、エラーを無視する--force 、データを保持するノードを指定する --retain-node-data、データを保持するロールを指定する --retain-role-data、ヘルプ情報を出力する -h または --help があります。出力は、 tiup-clusterの実行ログです。
---

# tiup cluster destroy {#tiup-cluster-destroy}

アプリケーションがオフラインになった後、クラスターが占有しているマシンを解放して他のアプリケーションで使用できるようにするには、クラスター上のデータとデプロイされたバイナリ ファイルをクリーンアップする必要があります。クラスターを破棄するには、 `tiup cluster destroy`コマンドで次の操作を実行します。

-   クラスターを停止します。
-   各サービスについて、ログ ディレクトリ、デプロイメント ディレクトリ、およびデータ ディレクトリを削除します。
-   tiup-clusterによって各サービスのデータディレクトリまたはデプロイメントディレクトリの親ディレクトリが作成されている場合は、親ディレクトリも削除します。

## 構文 {#syntax}

```shell
tiup cluster destroy <cluster-name> [flags]
```

`<cluster-name>` : 破棄するクラスターの名前。

## オプション {#options}

### &#x20;--force {#force}

-   場合によっては、クラスター内の一部のノードがダウンし、SSH 経由でノードに接続して操作することができなくなります。このとき、 `--force`オプションを使用してこれらのエラーを無視できます。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

### --ノードデータを保持 {#retain-node-data}

-   データを保持する必要があるノードを指定します。複数のノードを指定する必要がある場合は、このオプションを複数回使用します: `--retain-node-data <node-A> --retain-node-data <node-B>` 。
-   データ型: `StringArray`
-   デフォルト: 空

### --ロールデータを保持 {#retain-role-data}

-   データを保持する必要があるロールを指定します。複数のロールを指定する必要がある場合は、このオプションを複数回使用します: `--retain-role-data <role-A> --retain-role-data <role-B>` 。
-   データ型: `StringArray`
-   デフォルト: 空

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
