---
title: PD Recover User Guide
summary: Use PD Recover to recover a PD cluster which cannot start or provide services normally.
---

# PD リカバリ ユーザー ガイド {#pd-recover-user-guide}

PD Recover は、PD の災害復旧ツールであり、サービスが正常に起動または提供できない PD クラスターを復旧するために使用されます。

## ソースコードからコンパイルする {#compile-from-source-code}

-   [行く](https://golang.org/) Go モジュールを使用するため、1.21 以降が必要です。
-   [PDプロジェクト](https://github.com/pingcap/pd)のルート ディレクトリで、 `make pd-recover`コマンドを使用して`bin/pd-recover`をコンパイルし、生成します。

> **注記：**
>
> 通常、 PD Controlツールはリリースされたバイナリまたは Docker にすでに存在しているため、ソース コードをコンパイルする必要はありません。ただし、開発者ユーザーは、ソース コードをコンパイルするための上記の手順を参照できます。

## TiDB Toolkitをダウンロード {#download-tidb-toolkit}

PD Recover インストール パッケージは、 TiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

次のセクションでは、PD クラスターを回復する 2 つの方法、つまり、生き残った PD ノードから回復する方法と、PD クラスター全体を再構築する方法を紹介します。

## 方法 1: 存続している PD ノードを使用して PD クラスターを回復する {#method-1-recover-a-pd-cluster-using-a-surviving-pd-node}

クラスター内の大部分の PD ノードで回復不能なエラーが発生すると、クラスターはサービスを提供できなくなります。生き残っている PD ノードがある場合は、生き残っている PD ノードを選択し、 Raftグループのメンバーを強制的に変更することでサービスを回復できます。手順は次のとおりです。

### ステップ 1: すべてのノードを停止する {#step-1-stop-all-nodes}

リカバリプロセス中の PD パラメータとの相互作用によって引き起こされるデータ破損やその他の回復不能なエラーを防ぐには、クラスタ内の TiDB、TiKV、およびTiFlashプロセスを停止します。

### ステップ 2: 生き残った PD ノードを起動する {#step-2-start-the-surviving-pd-node}

`--force-new-cluster`起動パラメータを使用して、残っている PD ノードを起動します。以下は例です。

```shell
./bin/pd-server --force-new-cluster --name=pd-127.0.0.10-2379 --client-urls=http://0.0.0.0:2379 --advertise-client-urls=http://127.0.0.1:2379 --peer-urls=http://0.0.0.0:2380 --advertise-peer-urls=http://127.0.0.1:2380 --config=conf/pd.toml
```

### ステップ 3: <code>pd-recover</code>を使用してメタデータを修復する {#step-3-repair-metadata-using-code-pd-recover-code}

この方法はサービスを回復するために少数の PD ノードに依存しているため、ノードには古いデータが含まれている可能性があります。 `alloc_id`と`tso`データがロールバックすると、クラスター データが破損するか、使用できなくなる可能性があります。これを防ぐには、 `pd-recover`使用してメタデータを変更し、ノードが正しい割り当て ID と TSO サービスを提供できるようにする必要があります。以下は例です。

```shell
./bin/pd-recover --from-old-member --endpoints=http://127.0.0.1:2379 # Specify the corresponding PD address
```

> **注記：**
>
> このステップでは、storage内の`alloc_id`安全な値`100000000`だけ自動的に増加します。その結果、後続のクラスターはより大きな ID を割り当てることになります。
>
> さらに、 `pd-recover`は TSO を変更しません。したがって、この手順を実行する前に、ローカル時刻が障害が発生した時刻よりも新しいことを確認し、障害が発生する前に PD コンポーネント間で NTP クロック同期サービスが有効になっていることを確認してください。有効になっていない場合は、TSO がロールバックしないようにローカル クロックを将来の時刻に調整する必要があります。

### ステップ 4: PD ノードを再起動する {#step-4-restart-the-pd-node}

プロンプト メッセージ`recovery is successful`が表示されたら、PD ノードを再起動します。

### ステップ 5: PD をスケールアウトしてクラスターを開始する {#step-5-scale-out-pd-and-start-the-cluster}

デプロイメント ツールを使用して PD クラスターをスケールアウトし、クラスター内の他のコンポーネントを起動します。この時点で、PD サービスが利用可能になります。

## 方法 2: PD クラスターを完全に再構築する {#method-2-entirely-rebuild-a-pd-cluster}

この方法は、すべての PD データが失われたものの、TiDB、TiKV、 TiFlashなどの他のコンポーネントのデータがまだ存在しているシナリオに適用できます。

### ステップ 1: クラスター ID を取得する {#step-1-get-cluster-id}

クラスタIDはPD、TiKV、TiDBのログから取得できます。クラスター ID を取得するには、サーバー上でログを直接表示します。

#### PD ログからクラスター ID を取得する (推奨) {#get-cluster-id-from-pd-log-recommended}

PD ログからクラスター ID を取得するには、次のコマンドを実行します。

```bash
cat {{/path/to}}/pd.log | grep "init cluster id"
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

#### TiDB ログからクラスター ID を取得する {#get-cluster-id-from-tidb-log}

TiDB ログからクラスター ID を取得するには、次のコマンドを実行します。

```bash
cat {{/path/to}}/tidb.log | grep "init cluster id"
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### TiKV ログからクラスター ID を取得する {#get-cluster-id-from-tikv-log}

TiKV ログからクラスター ID を取得するには、次のコマンドを実行します。

```bash
cat {{/path/to}}/tikv.log | grep "connect to PD cluster"
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### ステップ 2: 割り当てられた ID を取得する {#step-2-get-allocated-id}

指定する割り当て ID 値は、現在割り当てられている最大 ID 値より大きくなければなりません。割り当てられた ID を取得するには、モニターから取得するか、サーバー上でログを直接表示します。

#### モニターから割り当てられたIDを取得する(推奨) {#get-allocated-id-from-the-monitor-recommended}

モニターから割り当てられた ID を取得するには、表示しているメトリクスが**最後の PD リーダー**のメトリクスであることを確認する必要があります。PD ダッシュボードの**現在の ID 割り当て**パネルから最大の割り当て ID を取得できます。

#### PDログから割り当てられたIDを取得 {#get-allocated-id-from-pd-log}

PD ログから割り当てられた ID を取得するには、表示しているログが**最後の PD リーダー**のログであることを確認する必要があります。次のコマンドを実行すると、割り当てられた最大 ID を取得できます。

```bash
cat {{/path/to}}/pd*.log | grep "idAllocator allocates a new id" |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r -n | head -n 1
```

```bash
4000
...
```

または、すべての PD サーバーで上記のコマンドを実行して、最大の PD サーバーを見つけることもできます。

### ステップ 3: 新しい PD クラスターをデプロイ {#step-3-deploy-a-new-pd-cluster}

新しい PD クラスターをデプロイする前に、既存の PD クラスターを停止し、以前のデータ ディレクトリを削除するか、 `--data-dir`を使用して新しいデータ ディレクトリを指定する必要があります。

### ステップ 4: pd-recover を使用する {#step-4-use-pd-recover}

1 つの PD ノードで`pd-recover`を実行するだけで済みます。

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### ステップ 5: クラスター全体を再起動する {#step-5-restart-the-whole-cluster}

リカバリが成功したことを示すプロンプト情報が表示されたら、クラスター全体を再起動します。

## FAQ {#faq}

### クラスター ID を取得するときに複数のクラスター ID が見つかりました {#multiple-cluster-ids-are-found-when-getting-the-cluster-id}

PD クラスターが作成されると、新しいクラスター ID が生成されます。ログを表示すると、古いクラスターのクラスター ID を確認できます。

### <code>pd-recover</code>を実行すると、エラー<code>dial tcp 10.0.1.13:2379: connect: connection refused</code>が返される {#the-error-code-dial-tcp-10-0-1-13-2379-connect-connection-refused-code-is-returned-when-executing-code-pd-recover-code}

`pd-recover`を実行する場合はPDサービスが必要です。 PD Recover を使用する前に、PD クラスターをデプロイて開始します。
