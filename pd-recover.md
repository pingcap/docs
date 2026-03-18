---
title: PD Recover User Guide
summary: PD Recover を使用すると、正常に起動またはサービスを提供できない PD クラスタを復旧できます。
---

# PDリカバリーユーザーガイド {#pd-recover-user-guide}

PD RecoverはPDのディザスタリカバリツールであり、正常に起動またはサービスを提供できないPDクラスタを復旧するために使用されます。

## ソースコードからコンパイル {#compile-from-source-code}

-   Goモジュールが使用されるため、 [行く](https://golang.org/) 1.23以降が必要です。
-   [PDプロジェクト](https://github.com/pingcap/pd)のルートディレクトリで、 `make pd-recover`コマンドを使用して`bin/pd-recover`コンパイルおよび生成します。

> **注記：**
>
> 通常、 PD Controlツールはリリース済みのバイナリまたはDockerに既に含まれているため、ソースコードをコンパイルする必要はありません。ただし、開発者ユーザーは上記のソースコードコンパイル手順を参照してください。

## TiDB Toolkitをダウンロード {#download-tidb-toolkit}

PD Recover インストール パッケージはTiDB Toolkitに含まれています。TiDB TiDB Toolkit をダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

以下のセクションでは、PDクラスタを復旧するための2つの方法、すなわち、稼働中のPDノードからの復旧と、PDクラスタ全体の再構築について説明します。

## 方法1：残存するPDノードを使用してPDクラスタを復旧する {#method-1-recover-a-pd-cluster-using-a-surviving-pd-node}

クラスタ内のPDノードの過半数で回復不能なエラーが発生すると、クラスタはサービスを提供できなくなります。PDノードが残っている場合は、残っているPDノードを選択し、 Raftグループのメンバーを強制的に変更することでサービスを復旧できます。手順は以下のとおりです。

### ステップ1：すべてのノードを停止する {#step-1-stop-all-nodes}

リカバリプロセス中にPDパラメータとの相互作用によって発生するデータ破損やその他の回復不能なエラーを防ぐため、クラスタ内のTiDB、TiKV、およびTiFlashプロセスを停止してください。

### ステップ2：生存しているPDノードを起動する {#step-2-start-the-surviving-pd-node}

起動パラメータ`--force-new-cluster`を使用して、残存PDノードを起動し、ノードが元のデータディレクトリを使用するようにします。これは、コマンドラインで`--data-dir`使用して明示的に指定するか、 `conf/pd.toml`で`data-dir`事前に設定することができます。例：

```shell
./bin/pd-server --force-new-cluster --name=pd-127.0.0.10-2379 --data-dir=/path/to/existing/pd/data --client-urls=http://0.0.0.0:2379 --advertise-client-urls=http://127.0.0.1:2379 --peer-urls=http://0.0.0.0:2380 --advertise-peer-urls=http://127.0.0.1:2380 --config=conf/pd.toml
```

> **注記：**
>
> -   コマンドラインで`--data-dir`指定されていない場合は、 `conf/pd.toml`の`data-dir` 、存続しているPDノードの元のデータディレクトリを正しく指していることを確認してください。そうでない場合、 `pd-recover`後続の操作で失敗する可能性があります。
> -   `conf/pd.toml`とコマンドライン引数の両方で`data-dir`指定されている場合、 `conf/pd.toml`の`data-dir`設定が優先されます。

### ステップ3： <code>pd-recover</code>を使用してメタデータを修復する {#step-3-repair-metadata-using-code-pd-recover-code}

この方法は少数派のPDノードがサービスを復旧することに依存するため、ノードに古いデータが含まれている可能性があります。1 `alloc_id` `tso`データがロールバックされると、クラスタデータが破損したり、利用できなくなったりする可能性があります。これを防ぐには、 `pd-recover`使用してメタデータを変更し、ノードが正しい割り当てIDとTSOサービスを提供できるようにする必要があります。以下に例を示します。

```shell
./bin/pd-recover --from-old-member --endpoints=http://127.0.0.1:2379 # Specify the corresponding PD address
```

> **注記：**
>
> このステップでは、storage内の「 `alloc_id`が自動的に安全な値である`100000000`だけ増加します。その結果、後続のクラスタはより大きなIDを割り当てることになります。
>
> さらに、手順`pd-recover`ではTSOは変更されません。したがって、この手順を実行する前に、ローカル時刻が障害発生時刻よりも後であることを確認し、障害発生前にPDコンポーネント間でNTPクロック同期サービスが有効になっていることを確認してください。有効になっていない場合は、TSOのロールバックを防ぐために、ローカルクロックを将来の時刻に調整する必要があります。

### ステップ4：PDノードを再起動する {#step-4-restart-the-pd-node}

プロンプトメッセージ`recovery is successful`が表示されたら、PDノードを再起動してください。

### ステップ5：PDをスケールアウトしてクラスターを起動する {#step-5-scale-out-pd-and-start-the-cluster}

デプロイツールを使用してPDクラスタをスケールアウトし、クラスタ内の他のコンポーネントを起動します。これでPDサービスが利用可能になります。

## 方法2：PDクラスタを完全に再構築する {#method-2-entirely-rebuild-a-pd-cluster}

この方法は、PDデータがすべて失われたものの、TiDB、TiKV、 TiFlashなどの他のコンポーネントのデータは残っているようなシナリオに適用可能です。

### ステップ1：クラスターIDを取得する {#step-1-get-cluster-id}

クラスタIDは、PD、TiKV、またはTiDBのログから取得できます。クラスタIDを取得するには、サーバー上でログを直接表示してください。

#### PDログからクラスタIDを取得する（推奨） {#get-cluster-id-from-pd-log-recommended}

PDログからクラスタIDを取得するには、次のコマンドを実行します。

```bash
grep "init cluster id" {{/path/to}}/pd.log
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

#### TiDBログからクラスタIDを取得する {#get-cluster-id-from-tidb-log}

TiDBログからクラスタIDを取得するには、次のコマンドを実行します。

```bash
grep "init cluster id" {{/path/to}}/tidb.log
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### TiKVログからクラスタIDを取得する {#get-cluster-id-from-tikv-log}

TiKVログからクラスタIDを取得するには、次のコマンドを実行します。

```bash
grep "connect to PD cluster" {{/path/to}}/tikv.log
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### ステップ2：割り当てられたIDを取得する {#step-2-get-allocated-id}

指定する割り当て済みID値は、現在割り当てられている最大のID値よりも大きくなければなりません。割り当て済みIDを取得するには、モニターから取得するか、サーバー上で直接ログを確認してください。

#### モニターから割り当てられたIDを取得する（推奨） {#get-allocated-id-from-the-monitor-recommended}

モニターから割り当てられたIDを取得するには、表示しているメトリックが**前回のPDリーダー**のメトリックであることを確認する必要があります。また、PDダッシュボードの**「現在のID割り当て」**パネルから、最大の割り当て済みIDを取得できます。

#### PDログから割り当てられたIDを取得する {#get-allocated-id-from-pd-log}

PDログから割り当てられたIDを取得するには、表示しているログが**最後のPDリーダー**のログであることを確認する必要があります。また、次のコマンドを実行することで、割り当てられた最大IDを取得できます。

```bash
grep "idAllocator allocates a new id" {{/path/to}}/pd*.log |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r -n | head -n 1
```

```bash
4000
...
```

または、上記のコマンドをすべてのPDサーバーで実行して、最大のサーバーを見つけることもできます。

### ステップ3：新しいPDクラスタをデプロイ {#step-3-deploy-a-new-pd-cluster}

新しい PD クラスターをデプロイする前に、既存の PD クラスターを停止し、以前のデータ ディレクトリを削除するか、 `--data-dir`を使用して新しいデータ ディレクトリを指定する必要があります。

### ステップ4：pd-recoverを使用する {#step-4-use-pd-recover}

PDノード1でのみ`pd-recover`プログラムを実行してください。再割り当てを避けるため、 `-alloc-id`パラメータには割り当て済みIDよりも大きな値を設定することをお勧めします。たとえば、監視またはログから取得した最大割り当て済みIDが`9000`の場合、 `-alloc-id`パラメータには`10000`以上の値を渡すことをお勧めします。

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### ステップ5：クラスター全体を再起動する {#step-5-restart-the-whole-cluster}

リカバリが成功したことを示すメッセージが表示されたら、クラスター全体を再起動してください。

## FAQ {#faq}

### クラスターIDを取得する際に、複数のクラスターIDが見つかりました。 {#multiple-cluster-ids-are-found-when-getting-the-cluster-id}

PDクラスタが作成されると、新しいクラスタIDが生成されます。古いクラスタのクラスタIDは、ログを確認することで確認できます。

### <code>pd-recover</code>を実行すると、エラー「 <code>dial tcp 10.0.1.13:2379: connect: connection refused</code>が返されます。 {#the-error-code-dial-tcp-10-0-1-13-2379-connect-connection-refused-code-is-returned-when-executing-code-pd-recover-code}

PD サービスは、 `pd-recover`実行する際に必要です。PD Recover を使用する前に、PD クラスタをデプロイ起動してください。
