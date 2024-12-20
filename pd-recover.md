---
title: PD Recover User Guide
summary: PD Recover を使用して、正常に起動またはサービスを提供できない PD クラスターを回復します。
---

# PD Recover ユーザーガイド {#pd-recover-user-guide}

PD Recover は、正常に起動またはサービスを提供できない PD クラスターを復旧するために使用される PD の災害復旧ツールです。

## ソースコードからコンパイルする {#compile-from-source-code}

-   Go モジュールが使用されるため、 [行く](https://golang.org/)以降が必要です。
-   [PDプロジェクト](https://github.com/pingcap/pd)のルート ディレクトリで、 `make pd-recover`コマンドを使用して`bin/pd-recover`コンパイルして生成します。

> **注記：**
>
> 通常、 PD Controlツールはリリースされたバイナリまたは Docker にすでに存在するため、ソース コードをコンパイルする必要はありません。ただし、開発者ユーザーは、上記の手順を参照してソース コードをコンパイルできます。

## TiDB Toolkitをダウンロード {#download-tidb-toolkit}

PD Recover インストール パッケージはTiDB Toolkitに含まれています。TiDB TiDB Toolkit をダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

次のセクションでは、PD クラスターを回復するための 2 つの方法 (存続している PD ノードからの回復と PD クラスター全体の再構築) を紹介します。

## 方法1: 残存PDノードを使用してPDクラスターを回復する {#method-1-recover-a-pd-cluster-using-a-surviving-pd-node}

クラスター内の PD ノードの過半数で回復不能なエラーが発生すると、クラスターはサービスを提供できなくなります。残っている PD ノードがある場合は、残っている PD ノードを選択し、 Raftグループのメンバーを強制的に変更することでサービスを回復できます。手順は次のとおりです。

### ステップ1: すべてのノードを停止する {#step-1-stop-all-nodes}

リカバリ プロセス中に PD パラメータとのやり取りによって発生するデータ破損やその他の回復不能なエラーを防ぐには、クラスター内の TiDB、TiKV、およびTiFlashプロセスを停止します。

### ステップ2: 生き残ったPDノードを起動する {#step-2-start-the-surviving-pd-node}

`--force-new-cluster`起動パラメータを使用して、生き残った PD ノードを起動します。次に例を示します。

```shell
./bin/pd-server --force-new-cluster --name=pd-127.0.0.10-2379 --client-urls=http://0.0.0.0:2379 --advertise-client-urls=http://127.0.0.1:2379 --peer-urls=http://0.0.0.0:2380 --advertise-peer-urls=http://127.0.0.1:2380 --config=conf/pd.toml
```

### ステップ3: <code>pd-recover</code>を使用してメタデータを修復する {#step-3-repair-metadata-using-code-pd-recover-code}

この方法では、少数の PD ノードを使用してサービスを回復するため、ノードに古いデータが含まれている可能性があります。1 と`alloc_id` `tso`データがロールバックされると、クラスター データが破損したり、使用できなくなったりする可能性があります。これを防ぐには、 `pd-recover`使用してメタデータを変更し、ノードが正しい割り当て ID と TSO サービスを提供できるようにする必要があります。次に例を示します。

```shell
./bin/pd-recover --from-old-member --endpoints=http://127.0.0.1:2379 # Specify the corresponding PD address
```

> **注記：**
>
> このステップでは、storage内の`alloc_id`安全な値である`100000000`だけ自動的に増加します。その結果、後続のクラスターではより大きな ID が割り当てられます。
>
> また、 `pd-recover` TSO を変更しません。したがって、この手順を実行する前に、ローカル時間が障害発生時刻よりも後であることを確認し、障害発生前に PD コンポーネント間で NTP クロック同期サービスが有効になっていることを確認します。有効になっていない場合は、TSO がロールバックしないように、ローカル クロックを将来の時刻に調整する必要があります。

### ステップ4: PDノードを再起動する {#step-4-restart-the-pd-node}

プロンプトメッセージ`recovery is successful`が表示されたら、PD ノードを再起動します。

### ステップ5: PDをスケールアウトしてクラスターを起動する {#step-5-scale-out-pd-and-start-the-cluster}

デプロイメント ツールを使用して PD クラスターをスケールアウトし、クラスター内の他のコンポーネントを起動します。この時点で、PD サービスは利用可能になります。

## 方法2: PDクラスターを完全に再構築する {#method-2-entirely-rebuild-a-pd-cluster}

この方法は、PD データはすべて失われたが、TiDB、TiKV、 TiFlashなどの他のコンポーネントのデータがまだ存在するシナリオに適用できます。

### ステップ1: クラスターIDを取得する {#step-1-get-cluster-id}

クラスター ID は、PD、TiKV、または TiDB のログから取得できます。クラスター ID を取得するには、サーバー上で直接ログを表示します。

#### PD ログからクラスター ID を取得する (推奨) {#get-cluster-id-from-pd-log-recommended}

PD ログからクラスター ID を取得するには、次のコマンドを実行します。

```bash
grep "init cluster id" {{/path/to}}/pd.log
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

#### TiDBログからクラスタIDを取得する {#get-cluster-id-from-tidb-log}

TiDB ログからクラスター ID を取得するには、次のコマンドを実行します。

```bash
grep "init cluster id" {{/path/to}}/tidb.log
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### TiKVログからクラスターIDを取得する {#get-cluster-id-from-tikv-log}

TiKV ログからクラスター ID を取得するには、次のコマンドを実行します。

```bash
grep "connect to PD cluster" {{/path/to}}/tikv.log
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### ステップ2: 割り当てられたIDを取得する {#step-2-get-allocated-id}

指定する割り当て ID 値は、現在割り当てられている最大の ID 値よりも大きくなければなりません。割り当て ID を取得するには、モニターから取得するか、サーバー上で直接ログを表示します。

#### モニターから割り当てられたIDを取得する（推奨） {#get-allocated-id-from-the-monitor-recommended}

モニターから割り当てられた ID を取得するには、表示しているメトリックが**最後の PD リーダー**のメトリックであることを確認する必要があります。また、PD ダッシュボードの**現在の ID 割り当て**パネルから最大の割り当て ID を取得できます。

#### PDログから割り当てられたIDを取得する {#get-allocated-id-from-pd-log}

PD ログから割り当てられた ID を取得するには、表示しているログが**最後の PD リーダー**のログであることを確認する必要があります。次のコマンドを実行すると、割り当てられた最大の ID を取得できます。

```bash
grep "idAllocator allocates a new id" {{/path/to}}/pd*.log |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r -n | head -n 1
```

```bash
4000
...
```

または、すべての PD サーバーで上記のコマンドを実行して、最大のサーバーを見つけることもできます。

### ステップ3: 新しいPDクラスターをデプロイ {#step-3-deploy-a-new-pd-cluster}

新しい PD クラスターをデプロイする前に、既存の PD クラスターを停止し、以前のデータ ディレクトリを削除するか、 `--data-dir`使用して新しいデータ ディレクトリを指定する必要があります。

### ステップ4: pd-recoverを使用する {#step-4-use-pd-recover}

1 つの PD ノードで`pd-recover`実行するだけで済みます。再割り当てを回避するために、 `-alloc-id`パラメータを割り当てられた ID よりも大きい値に設定することをお勧めします。たとえば、監視やログから取得した最大の割り当て ID が`9000`の場合、 `-alloc-id`パラメータに`10000`以上の値を渡すことをお勧めします。

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### ステップ5: クラスター全体を再起動する {#step-5-restart-the-whole-cluster}

リカバリが成功したことを示すプロンプト情報が表示されたら、クラスター全体を再起動します。

## FAQ {#faq}

### クラスターIDを取得する際に複数のクラスターIDが見つかりました {#multiple-cluster-ids-are-found-when-getting-the-cluster-id}

PD クラスターが作成されると、新しいクラスター ID が生成されます。ログを表示することで、古いクラスターのクラスター ID を確認できます。

### <code>pd-recover</code>を実行すると、エラー「 <code>dial tcp 10.0.1.13:2379: connect: connection refused</code>が返されます。 {#the-error-code-dial-tcp-10-0-1-13-2379-connect-connection-refused-code-is-returned-when-executing-code-pd-recover-code}

PD リカバリを使用する前に、 `pd-recover` . PD クラスターをデプロイ起動するを実行する場合は、PD サービスが必要です。
