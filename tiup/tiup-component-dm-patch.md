---
title: Apply Hotfix to DM Clusters Online
summary: DM クラスターにホットフィックス パッチを適用する方法を学習します。
---

# DM クラスターにオンラインでホットフィックスを適用する {#apply-hotfix-to-dm-clusters-online}

クラスターの実行中にサービスのバイナリを動的に置き換える必要がある場合（つまり、置き換え中もクラスターを利用可能な状態に保つ必要がある場合）、 `tiup dm patch`コマンドを使用できます。このコマンドは、以下の処理を実行します。

-   置換用のバイナリ パッケージをターゲット マシンにアップロードします。
-   API を使用して関連するノードをオフラインにします。
-   対象サービスを停止します。
-   バイナリ パッケージを解凍し、サービスを置き換えます。
-   対象サービスを開始します。

## 構文 {#syntax}

```shell
tiup dm patch <cluster-name> <package-path> [flags]
```

-   `<cluster-name>` : 操作対象となるクラスタの名前
-   `<package-path>` : 置換に使用するバイナリパッケージへのパス

### 準備 {#preparation}

以下の手順に従って、このコマンドに必要なバイナリ パッケージを事前にパックする必要があります。

-   置換するコンポーネントの名前`${component}` (dm-master、dm-worker ...)、コンポーネントの`${version}` (v2.0.0、v2.0.1 ...)、およびコンポーネントが実行されるオペレーティング システム`${os}`とプラットフォーム`${arch}`決定します。
-   コマンド`wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz`を使用して現在のコンポーネントパッケージをダウンロードします。
-   `mkdir -p /tmp/package && cd /tmp/package`実行して、ファイルをパックするための一時ディレクトリを作成します。
-   `tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz`実行して元のバイナリ パッケージを解凍します。
-   `find .`実行して、一時パッケージ ディレクトリ内のファイル構造を表示します。
-   バイナリ ファイルまたは構成ファイルを一時ディレクトリ内の対応する場所にコピーします。
-   `tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *`実行して、一時ディレクトリにファイルをパックします。
-   最後に、 `tiup dm patch`コマンドの`<package-path>`の値として`/tmp/${component}-hotfix-${os}-${arch}.tar.gz`使用できます。

## オプション {#options}

### --overwrite {#overwrite}

-   特定のコンポーネント（dm-workerなど）にパッチを適用した後、tiup-dmがそのコンポーネントをスケールアウトすると、tiup-dmはデフォルトで元のコンポーネントバージョンを使用します。将来クラスタがスケールアウトした際にパッチを適用したバージョンを使用するには、コマンドでオプション`--overwrite`指定する必要があります。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### -N, --node {#n-node}

-   置換するノードを指定します。このオプションの値は、ノードIDのカンマ区切りのリストです。ノードIDは、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドで返されるクラスターステータステーブルの最初の列から取得できます。
-   データ型: `STRING`
-   このオプションを指定しない場合、 TiUP はデフォルトで置換するすべてのノードを選択します。

> **注記：**
>
> オプション`-R, --role`同時に指定されている場合、 TiUP は`-N, --node`と`-R, --role`両方の要件に一致するサービス ノードを置き換えます。

### -R, --role {#r-role}

-   置換するロールを指定します。このオプションの値は、ノードのロールをカンマ区切りでリストしたものです。ノードのロールは、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドで返されるクラスターステータステーブルの2列目から取得できます。
-   データ型: `STRING`
-   このオプションを指定しない場合、 TiUP はデフォルトですべてのロールを選択して置き換えます。

> **注記：**
>
> オプション`-N, --node`同時に指定されている場合、 TiUP は`-N, --node`と`-R, --role`両方の要件に一致するサービス ノードを置き換えます。

### &#x20;--offline {#offline}

-   現在のクラスタがオフラインであることを宣言します。このオプションを指定すると、 TiUP DMはサービスを再起動せずに、クラスタコンポーネントのバイナリファイルのみを置き換えます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## 例 {#example}

以下の例は、 TiUPを使用してデプロイされた`v5.3.0`クラスターに`v5.3.0-hotfix`適用する方法を示しています。他の方法でクラスターをデプロイする場合は、操作が異なる場合があります。

> **注記：**
>
> ホットフィックスは緊急時の修正にのみ使用されます。日常的なメンテナンスは複雑です。DMクラスタを正式版にアップグレードすることをお勧めします。

### 準備 {#preparations}

修正プログラムを適用する前に、修正プログラム パッケージ`dm-linux-amd64.tar.gz`準備し、現在の DM ソフトウェア バージョンを確認します。

```shell
/home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
```

出力：

    Release Version: v5.3.0

    Git Commit Hash: 20626babf21fc381d4364646c40dd84598533d66
    Git Branch: heads/refs/tags/v5.3.0
    UTC Build Time: 2021-11-29 08:29:49
    Go Version: go version go1.16.4 linux/amd64

### パッチパッケージを準備し、DMクラスタに適用する {#prepare-the-patch-package-and-apply-it-to-the-dm-cluster}

1.  現在のバージョンに一致する DM ソフトウェア パッケージを準備します。

    ```shell
    mkdir -p /tmp/package
    tar -zxvf /root/.tiup/storage/dm/packages/dm-master-v5.3.0-linux-amd64.tar.gz -C /tmp/package/
    tar -zxvf /root/.tiup/storage/dm/packages/dm-worker-v5.3.0-linux-amd64.tar.gz -C /tmp/package/
    ```

2.  バイナリ ファイルを修正プログラム パッケージに置き換えます。

    ```shell
    # Decompress the hotfix package and use it to replace the binary file.
    cd /root; tar -zxvf dm-linux-amd64.tar.gz
    cp /root/dm-linux-amd64/bin/dm-master /tmp/package/dm-master/dm-master
    cp /root/dm-linux-amd64/bin/dm-worker /tmp/package/dm-worker/dm-worker
    # Re-package the modified files.
    # Note that the packaging method might be different for other deployment methods.
    cd /tmp/package/ && tar -czvf dm-master-hotfix-linux-amd64.tar.gz dm-master/
    cd /tmp/package/ && tar -czvf dm-worker-hotfix-linux-amd64.tar.gz dm-worker/
    ```

3.  修正プログラムを適用します。

    クラスターのステータスを照会します。以下は、クラスター`dm-test`例にしています。

    ```shell
    tiup dm display dm-test
    ```

    出力：

        Cluster type:       dm
        Cluster name:       dm-test
        Cluster version:    v5.3.0
        Deploy user:        tidb
        SSH type:           builtin
        ID                  Role                 Host           Ports      OS/Arch       Status     Data Dir                              Deploy Dir
        --                  ----                 ----           -----      -------       ------     --------                              ----------
        172.16.100.21:9093  alertmanager         172.16.100.21  9093/9094  linux/x86_64  Up         /home/tidb/dm/data/alertmanager-9093  /home/tidb/dm/deploy/alertmanager-9093
        172.16.100.21:8261  dm-master            172.16.100.21  8261/8291  linux/x86_64  Healthy|L  /home/tidb/dm/data/dm-master-8261     /home/tidb/dm/deploy/dm-master-8261
        172.16.100.21:8262  dm-worker            172.16.100.21  8262       linux/x86_64  Free       /home/tidb/dm/data/dm-worker-8262     /home/tidb/dm/deploy/dm-worker-8262
        172.16.100.21:3000  grafana              172.16.100.21  3000       linux/x86_64  Up         -                                     /home/tidb/dm/deploy/grafana-3000
        172.16.100.21:9090  prometheus           172.16.100.21  9090       linux/x86_64  Up         /home/tidb/dm/data/prometheus-9090    /home/tidb/dm/deploy/prometheus-9090
        Total nodes: 5

    指定されたノードまたは指定されたロールにホットフィックスを適用します。1と`-N` `-R`が指定されている場合は、共通部分が採用されます。

        # Apply hotfix to a specified node.
        tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8261
        tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8262
        # Apply hotfix to a specified role.
        tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -R dm-master
        tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -R dm-worker

4.  修正プログラムの適用結果を照会します。

    ```shell
    /home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
    ```

    出力：

        Release Version: v5.3.0-20211230
        Git Commit Hash: ca7070c45013c24d34bd9c1e936071253451d707
        Git Branch: heads/refs/tags/v5.3.0-20211230
        UTC Build Time: 2022-01-05 14:19:02
        Go Version: go version go1.16.4 linux/amd64

    クラスター情報はそれに応じて変更されます。

    ```shell
    tiup dm display dm-test
    ```

    出力：

        Starting component `dm`: /root/.tiup/components/dm/v1.8.1/tiup-dm display dm-test
        Cluster type:       dm
        Cluster name:       dm-test
        Cluster version:    v5.3.0
        Deploy user:        tidb
        SSH type:           builtin
        ID                  Role                 Host           Ports      OS/Arch       Status     Data Dir                              Deploy Dir
        --                  ----                 ----           -----      -------       ------     --------                              ----------
        172.16.100.21:9093  alertmanager         172.16.100.21  9093/9094  linux/x86_64  Up         /home/tidb/dm/data/alertmanager-9093  /home/tidb/dm/deploy/alertmanager-9093
        172.16.100.21:8261  dm-master (patched)  172.16.100.21  8261/8291  linux/x86_64  Healthy|L  /home/tidb/dm/data/dm-master-8261     /home/tidb/dm/deploy/dm-master-8261
        172.16.100.21:8262  dm-worker (patched)  172.16.100.21  8262       linux/x86_64  Free       /home/tidb/dm/data/dm-worker-8262     /home/tidb/dm/deploy/dm-worker-8262
        172.16.100.21:3000  grafana              172.16.100.21  3000       linux/x86_64  Up         -                                     /home/tidb/dm/deploy/grafana-3000
        172.16.100.21:9090  prometheus           172.16.100.21  9090       linux/x86_64  Up         /home/tidb/dm/data/prometheus-9090    /home/tidb/dm/deploy/prometheus-9090
        Total nodes: 5

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
