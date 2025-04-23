---
title: tiup cluster patch
summary: tiup cluster patch` コマンドを使用すると、実行中のクラスター内でバイナリを動的に置き換えることができます。このコマンドは、バイナリパッケージをアップロードし、対象サービスを停止し、バイナリを置き換えて、サービスを起動します。準備として、バイナリパッケージをパックし、`--overwrite`、`--transfer-timeout`、`-N, --node `、`-R, --role `、`--offline` などのオプションを使用します。出力はtiup-clusterの実行ログです。
---

# tiup cluster patch {#tiup-cluster-patch}

クラスターの実行中にサービスのバイナリを動的に置き換える必要がある場合（つまり、置き換えプロセス中もクラスターを利用可能な状態に保つ必要がある場合）、 `tiup cluster patch`コマンドを使用できます。コマンドの実行後、 TiUP は以下の処理を実行します。

-   置換用のバイナリ パッケージをターゲット マシンにアップロードします。
-   ターゲット サービスが TiKV、 TiFlash、TiDB Binlogなどのstorageサービスの場合、 TiUP はまず API 経由で関連ノードをオフラインにします。
-   対象サービスを停止します。
-   バイナリ パッケージを解凍し、サービスを置き換えます。
-   対象サービスを開始します。

## 構文 {#syntax}

```shell
tiup cluster patch <cluster-name> <package-path> [flags]
```

-   `<cluster-name>` : 操作対象となるクラスターの名前。
-   `<package-path>` : 置換に使用されるバイナリ パッケージへのパス。

### 準備 {#preparation}

`tiup cluster patch`コマンドを実行する前に、必要なバイナリパッケージをパックする必要があります。以下の手順に従ってください。

1.  次の変数を決定します。

    -   `${component}` : 置換するコンポーネントの名前 ( `tidb` 、 `tikv` 、 `pd`など)。
    -   `${version}` :コンポーネントのバージョン ( `v8.1.2`や`v7.5.4`など)。
    -   `${os}` :オペレーティングシステム（ `linux` ）。
    -   `${arch}` :コンポーネント`arm64`実行されるプラットフォーム( `amd64` )。

2.  次のコマンドを使用して、現在のコンポーネントパッケージをダウンロードします。

    ```shell
    wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz
    ```

3.  ファイルをパックするための一時ディレクトリを作成し、そこに移動します。

    ```shell
    mkdir -p /tmp/package && cd /tmp/package
    ```

4.  元のバイナリ パッケージを抽出します。

    ```shell
    tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz
    ```

5.  一時ディレクトリ内のファイル構造を確認します。

    ```shell
    find .
    ```

6.  バイナリ ファイルまたは構成ファイルを一時ディレクトリ内の対応する場所にコピーします。

7.  すべてのファイルを一時ディレクトリにパックします。

    ```shell
    tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *
    ```

上記の手順を完了すると、 `tiup cluster patch`コマンドの`<package-path>`として`/tmp/${component}-hotfix-${os}-${arch}.tar.gz`使用できます。

## オプション {#options}

### --overwrite {#overwrite}

-   特定のコンポーネント（TiDBやTiKVなど）にパッチを適用した後、TiUPクラスタがそのコンポーネントをスケールアウトすると、 TiUPはデフォルトで元のコンポーネントバージョンを使用します。将来クラスタがスケールアウトする際にパッチを適用したバージョンを使用するには、コマンドでオプション`--overwrite`指定する必要があります。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### --transfer-timeout {#transfer-timeout}

-   PDまたはTiKVサービスを再起動する際、TiKV/PDはまず再起動対象ノードのリーダーを別のノードに切り替えます。切り替え処理には時間がかかるため、オプション`--transfer-timeout`最大待機時間（秒単位）を設定できます。タイムアウト後、 TiUPはサービスを直接再起動します。
-   データ型: `UINT`
-   このオプションを指定しない場合、 TiUP は`600`秒待機した後、サービスを直接再起動します。

> **注記：**
>
> タイムアウト後にTiUP がサービスを直接再起動すると、サービスのパフォーマンスが不安定になる可能性があります。

### -N, --node {#n-node}

-   置換するノードを指定します。このオプションの値は、カンマ区切りのノードIDのリストです。ノードIDは、 `tiup cluster display`コマンドで返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の最初の列から取得できます。
-   データ型: `STRINGS`
-   このオプションを指定しないと、 TiUP はデフォルトで置換するノードを選択しません。

> **注記：**
>
> オプション`-R, --role`同時に指定されている場合、 TiUP は`-N, --node`と`-R, --role`両方の要件に一致するサービス ノードを置き換えます。

### -R, --role {#r-role}

-   置換するロールを指定します。このオプションの値は、ノードのロールのコンマ区切りリストです。ノードにデプロイされているロールは、 `tiup cluster display`コマンドで返される[クラスターステータステーブル](/tiup/tiup-component-cluster-display.md)の2列目から取得できます。
-   データ型: `STRINGS`
-   このオプションを指定しないと、 TiUP はデフォルトで置き換えるロールを選択しません。

> **注記：**
>
> オプション`-N, --node`同時に指定されている場合、 TiUP は`-N, --node`と`-R, --role`両方の要件に一致するサービス ノードを置き換えます。

### &#x20;--offline {#offline}

-   現在のクラスターが実行中でないことを宣言します。このオプションが指定されると、 TiUP はサービスリーダーを別のノードに移動させたり、サービスを再起動したりせず、クラスターコンポーネントのバイナリファイルのみを置き換えます。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## 出力 {#outputs}

tiup-clusterの実行ログ。

[&lt;&lt; 前のページに戻る - TiUPクラスタコマンド リスト](/tiup/tiup-component-cluster.md#command-list)
