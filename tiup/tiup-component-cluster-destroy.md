---
title: tiup cluster destroy
---

# tiup cluster destroy {#tiup-cluster-destroy}

アプリケーションがオフラインになった後、クラスターによって占有されていたマシンを他のアプリケーションで使用できるように解放したい場合は、クラスター上のデータとデプロイされたバイナリ ファイルをクリーンアップする必要があります。クラスターを破棄するには、 `tiup cluster destroy`コマンドは次の操作を実行します。

-   クラスターを停止します。
-   サービスごとに、ログ ディレクトリ、デプロイメント ディレクトリ、およびデータ ディレクトリを削除します。
-   各サービスのデータディレクトリやデプロイメントディレクトリの親ディレクトリがtiup-clusterで作成されている場合は、親ディレクトリも削除してください。

## 構文 {#syntax}

```shell
tiup cluster destroy <cluster-name> [flags]
```

`<cluster-name>` : 破棄するクラスターの名前。

## オプション {#options}

### &#x20;--force {#force}

-   場合によっては、クラスター内の一部のノードがダウンし、SSH 経由でノードに接続して操作できなくなることがあります。現時点では、 `--force`オプションを使用してこれらのエラーを無視できます。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

### --ノードデータの保持 {#retain-node-data}

-   データを保持する必要があるノードを指定します。複数のノードを指定する必要がある場合は、このオプションを`--retain-node-data <node-A> --retain-node-data <node-B>`回使用します。
-   データ型: `StringArray`
-   デフォルト: 空

### --ロールデータの保持 {#retain-role-data}

-   データを保持する必要があるロールを指定します。複数のロールを指定する必要がある場合は、このオプションを`--retain-role-data <role-A> --retain-role-data <role-B>`回使用します。
-   データ型: `StringArray`
-   デフォルト: 空

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `Boolean`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

## 出力 {#output}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
