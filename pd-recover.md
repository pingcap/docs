---
title: PD Recover User Guide
summary: Use PD Recover to recover a PD cluster which cannot start or provide services normally.
---

# PD リカバリ ユーザー ガイド {#pd-recover-user-guide}

PD Recover は PD のディザスタリカバリツールであり、正常にサービスを開始または提供できない PD クラスタをリカバリするために使用されます。

## ソースコードからコンパイル {#compile-from-source-code}

-   [行く](https://golang.org/) Go モジュールを使用するため、バージョン 1.19 以降が必要です。
-   [PDプロジェクト](https://github.com/pingcap/pd)のルート ディレクトリで、 `make pd-recover`コマンドを使用して`bin/pd-recover`をコンパイルおよび生成します。

> **ノート：**
>
> 通常、 PD Controlツールはリリース済みのバイナリまたは Docker に既に存在するため、ソース コードをコンパイルする必要はありません。ただし、開発者ユーザーは、ソース コードのコンパイルについて上記の手順を参照できます。

## TiDB Toolkitをダウンロード {#download-tidb-toolkit}

PD Recover インストール パッケージはTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

## クイックスタート {#quick-start}

このセクションでは、PD Recover を使用して PD クラスターを回復する方法について説明します。

### クラスター ID を取得する {#get-cluster-id}

クラスタ ID は、PD、TiKV、または TiDB のログから取得できます。クラスター ID を取得するには、サーバーで直接ログを表示できます。

#### PD ログからクラスター ID を取得する (推奨) {#get-cluster-id-from-pd-log-recommended}

PD ログからクラスター ID を取得するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
cat {{/path/to}}/pd.log | grep "init cluster id"
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

#### TiDB ログからクラスター ID を取得する {#get-cluster-id-from-tidb-log}

TiDB ログからクラスター ID を取得するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
cat {{/path/to}}/tidb.log | grep "init cluster id"
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### TiKV ログからクラスター ID を取得する {#get-cluster-id-from-tikv-log}

TiKV ログからクラスター ID を取得するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
cat {{/path/to}}/tikv.log | grep "connect to PD cluster"
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### 割り当てられた ID を取得する {#get-allocated-id}

指定する割り当て済み ID 値は、現在割り当てられている最大の ID 値よりも大きくする必要があります。割り当てられた ID を取得するには、モニターから取得するか、サーバーで直接ログを表示します。

#### モニターから割り当てられた ID を取得する (推奨) {#get-allocated-id-from-the-monitor-recommended}

モニターから割り当てられた ID を取得するには、表示しているメトリックが**最後の PD リーダー**のメトリックであることを確認する必要があり、PD ダッシュボードの<strong>現在の ID 割り当て</strong>パネルから最大の割り当て ID を取得できます。

#### PD ログから割り当てられた ID を取得する {#get-allocated-id-from-pd-log}

PD ログから割り当てられた ID を取得するには、表示しているログが**最後の PD リーダー**のログであることを確認する必要があります。次のコマンドを実行すると、割り当てられた最大 ID を取得できます。

{{< copyable "" >}}

```bash
cat {{/path/to}}/pd*.log | grep "idAllocator allocates a new id" |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r -n | head -n 1
```

```bash
4000
...
```

または、すべての PD サーバーで上記のコマンドを実行して、最大の PD サーバーを見つけることもできます。

### 新しい PD クラスターをデプロイ {#deploy-a-new-pd-cluster}

新しい PD クラスターをデプロイする前に、既存の PD クラスターを停止してから、以前のデータ ディレクトリを削除するか、 `--data-dir`を使用して新しいデータ ディレクトリを指定する必要があります。

### pd-recover を使用する {#use-pd-recover}

1 つの PD ノードで`pd-recover`だけ実行する必要があります。

{{< copyable "" >}}

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### クラスタ全体を再起動します {#restart-the-whole-cluster}

リカバリが成功したというプロンプトが表示されたら、クラスタ全体を再起動します。

## FAQ {#faq}

### クラスター ID の取得時に複数のクラスター ID が検出される {#multiple-cluster-ids-are-found-when-getting-the-cluster-id}

PD クラスターが作成されると、新しいクラスター ID が生成されます。ログを表示することで、古いクラスターのクラスター ID を特定できます。

### <code>pd-recover</code>を実行すると、エラー<code>dial tcp 10.0.1.13:2379: connect: connection refused</code> {#the-error-code-dial-tcp-10-0-1-13-2379-connect-connection-refused-code-is-returned-when-executing-code-pd-recover-code}

`pd-recover`を実行する場合、PD サービスが必要です。 PD Recover を使用する前に、PD クラスターをデプロイて開始します。
