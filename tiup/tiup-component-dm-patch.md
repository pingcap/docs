---
title: Apply Hotfix to DM Clusters Online
summary: Learn how to apply hotfix patches to DM clusters.
---

# オンラインで DM クラスターにホットフィックスを適用する {#apply-hotfix-to-dm-clusters-online}

クラスターの実行中にサービスのバイナリを動的に置き換える必要がある場合 (つまり、置き換え中にクラスターを利用できるようにするため)、 `tiup dm patch`コマンドを使用できます。このコマンドは次のことを行います。

-   置換用のバイナリ パッケージをターゲット マシンにアップロードします。
-   API を使用して、関連するノードをオフラインにします。
-   対象のサービスを停止します。
-   バイナリ パッケージを展開し、サービスを置き換えます。
-   対象のサービスを開始します。

## 構文 {#syntax}

```shell
tiup dm patch <cluster-name> <package-path> [flags]
```

-   `<cluster-name>` : 運用するクラスタ名
-   `<package-path>` : 置換に使用されるバイナリ パッケージへのパス

### 準備 {#preparation}

次の手順に従って、このコマンドに必要なバイナリ パッケージを事前にパックする必要があります。

-   置き換えるコンポーネントの名前`${component}` (dm-master、dm-worker ...)、コンポーネントの名前`${version}` (v2.0.0、v2.0.1 ...)、オペレーティング システム`${os}`およびプラットフォーム`${arch}`を特定します。コンポーネントが実行するもの。
-   コマンド`wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz`を使用して、現在のコンポーネントパッケージをダウンロードします。
-   `mkdir -p /tmp/package && cd /tmp/package`を実行して、ファイルをパックするための一時ディレクトリを作成します。
-   `tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz`を実行して、元のバイナリ パッケージを解凍します。
-   `find .`を実行して、一時パッケージ ディレクトリのファイル構造を表示します。
-   バイナリ ファイルまたは構成ファイルを、一時ディレクトリ内の対応する場所にコピーします。
-   `tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *`を実行して、ファイルを一時ディレクトリにパックします。
-   最後に、 `tiup dm patch`コマンドで`<package-path>`の値として`/tmp/${component}-hotfix-${os}-${arch}.tar.gz`使用できます。

## オプション {#options}

### --overwrite {#overwrite}

-   特定のコンポーネント(dm-worker など) にパッチを適用した後、tiup-dm がコンポーネントをスケールアウトすると、tiup-dm はデフォルトで元のコンポーネントバージョンを使用します。将来クラスターがスケールアウトするときにパッチを適用するバージョンを使用するには、コマンドでオプション`--overwrite`を指定する必要があります。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

### -N, --ノード {#n-node}

-   置き換えるノードを指定します。このオプションの値は、ノード ID のコンマ区切りリストです。ノード ID は、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドによって返されるクラスター ステータス テーブルの最初の列から取得できます。
-   データ型: `STRING`
-   このオプションが指定されていない場合、 TiUP はデフォルトで置換するすべてのノードを選択します。

> **ノート：**
>
> オプション`-R, --role`が同時に指定された場合、 TiUP は`-N, --node`と`-R, --role`の両方の要件に一致するサービス ノードを置き換えます。

### -R, --role {#r-role}

-   置き換えるロールを指定します。このオプションの値は、ノードの役割のコンマ区切りリストです。ノードの役割は、 `[tiup dm display](/tiup/tiup-component-dm-display.md)`コマンドで返されるクラスター ステータス テーブルの 2 番目の列から取得できます。
-   データ型: `STRING`
-   このオプションが指定されていない場合、 TiUP はデフォルトで置換するすべてのロールを選択します。

> **ノート：**
>
> オプション`-N, --node`が同時に指定された場合、 TiUP は`-N, --node`と`-R, --role`の両方の要件に一致するサービス ノードを置き換えます。

### &#x20;--offline {#offline}

-   現在のクラスターがオフラインであることを宣言します。このオプションを指定すると、 TiUP DM はサービスを再起動せずに、クラスタ コンポーネントのバイナリ ファイルのみを置き換えます。

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## 例 {#example}

次の例は、 TiUP を使用してデプロイされた`v5.3.0`クラスターに`v5.3.0-hotfix`適用する方法を示しています。他の方法を使用してクラスターをデプロイすると、操作が異なる場合があります。

> **ノート：**
>
> ホットフィックスは、緊急の修正にのみ使用されます。その日常のメンテナンスは複雑です。 DM クラスターがリリースされたらすぐに正式バージョンにアップグレードすることをお勧めします。

### 準備 {#preparations}

ホットフィックスを適用する前に、ホットフィックス パッケージ`dm-linux-amd64.tar.gz`を準備し、現在の DM ソフトウェア バージョンを確認します。

```shell
/home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
```

出力：

```
Release Version: v5.3.0

Git Commit Hash: 20626babf21fc381d4364646c40dd84598533d66
Git Branch: heads/refs/tags/v5.3.0
UTC Build Time: 2021-11-29 08:29:49
Go Version: go version go1.16.4 linux/amd64
```

### パッチ パッケージを準備し、DM クラスタに適用します。 {#prepare-the-patch-package-and-apply-it-to-the-dm-cluster}

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

3.  ホットフィックスを適用します。

    クラスターの状態を照会します。以下では、例として`dm-test`という名前のクラスターを使用しています。

    ```shell
    tiup dm display dm-test
    ```

    出力：

    ```
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
    ```

    指定したノードまたは指定した役割に修正プログラムを適用します。 `-R`と`-N`両方が指定されている場合は、交差が取得されます。

    ```
    # Apply hotfix to a specified node.
    tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8261
    tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8262
    # Apply hotfix to a specified role.
    tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -R dm-master
    tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -R dm-worker
    ```

4.  ホットフィックス アプリケーションの結果を照会します。

    ```shell
    /home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
    ```

    出力：

    ```
    Release Version: v5.3.0-20211230
    Git Commit Hash: ca7070c45013c24d34bd9c1e936071253451d707
    Git Branch: heads/refs/tags/v5.3.0-20211230
    UTC Build Time: 2022-01-05 14:19:02
    Go Version: go version go1.16.4 linux/amd64
    ```

    それに応じてクラスター情報が変更されます。

    ```shell
    tiup dm display dm-test
    ```

    出力：

    ```
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
    ```

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
