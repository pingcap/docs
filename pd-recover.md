---
title: PD Recover User Guide
summary: Use PD Recover to recover a PD cluster which cannot start or provide services normally.
---

# PDRecoverユーザーガイド {#pd-recover-user-guide}

PD Recoverは、PDのディザスタリカバリツールであり、サービスを正常に開始または提供できないPDクラスタをリカバリするために使用されます。

## ソースコードからコンパイルする {#compile-from-source-code}

-   [行け](https://golang.org/) Goモジュールを使用するため、バージョン1.13以降が必要です。
-   [PDプロジェクト](https://github.com/pingcap/pd)のルートディレクトリで、 `make pd-recover`コマンドを使用して`bin/pd-recover`をコンパイルおよび生成します。

> **ノート：**
>
> 通常、PD制御ツールはリリースされたバイナリまたはDockerにすでに存在するため、ソースコードをコンパイルする必要はありません。ただし、開発者ユーザーは、ソースコードのコンパイルについて上記の手順を参照できます。

## TiDBインストールパッケージをダウンロードする {#download-tidb-installation-package}

PD RecoverはTiDBパッケージに含まれているため、最新バージョンのPD Recoverをダウンロードするには、TiDBパッケージを直接ダウンロードしてください。

| パッケージ名                                                                        | OS    | 建築    | SHA256チェックサム                                                     |
| :---------------------------------------------------------------------------- | :---- | :---- | :--------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` （pd-recover） | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **ノート：**
>
> `{version}`はTiDBのバージョン番号を示します。たとえば、 `{version}`が`v5.4.2`の場合、パッケージのダウンロードリンクは`https://download.pingcap.org/tidb-v5.4.2-linux-amd64.tar.gz`です。

## クイックスタート {#quick-start}

このセクションでは、PDリカバリを使用してPDクラスタをリカバリする方法について説明します。

### クラスタIDを取得する {#get-cluster-id}

クラスタIDは、PD、TiKV、またはTiDBのログから取得できます。クラスタIDを取得するには、サーバーでログを直接表示できます。

#### PDログからクラスタIDを取得する（推奨） {#get-cluster-id-from-pd-log-recommended}

PDログからクラスタIDを取得するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
cat {{/path/to}}/pd.log | grep "init cluster id"
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

#### TiDBログからクラスタIDを取得する {#get-cluster-id-from-tidb-log}

TiDBログからクラスタIDを取得するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
cat {{/path/to}}/tidb.log | grep "init cluster id"
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### TiKVログからクラスタIDを取得する {#get-cluster-id-from-tikv-log}

TiKVログからクラスタIDを取得するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
cat {{/path/to}}/tikv.log | grep "connect to PD cluster"
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### 割り当てられたIDを取得します {#get-allocated-id}

指定する割り当て済みID値は、現在最大の割り当て済みID値よりも大きくする必要があります。割り当てられたIDを取得するには、モニターから取得するか、サーバーで直接ログを表示します。

#### モニターから割り当てられたIDを取得します（推奨） {#get-allocated-id-from-the-monitor-recommended}

モニターから割り当てられたIDを取得するには、表示しているメトリックが**最後のPDリーダー**のメトリックであることを確認する必要があります。また、PDダッシュボードの[<strong>現在のID割り当て</strong>]パネルから最大の割り当てIDを取得できます。

#### PDログから割り当てられたIDを取得します {#get-allocated-id-from-pd-log}

PDログから割り当てられたIDを取得するには、表示しているログが**最後のPDリーダー**のログであることを確認する必要があります。次のコマンドを実行して、割り当てられた最大IDを取得できます。

{{< copyable "" >}}

```bash
cat {{/path/to}}/pd*.log | grep "idAllocator allocates a new id" |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r -n | head -n 1
```

```bash
4000
...
```

または、すべてのPDサーバーで上記のコマンドを実行するだけで、最大のサーバーを見つけることができます。

### 新しいPDクラスタをデプロイします {#deploy-a-new-pd-cluster}

新しいPDクラスタをデプロイする前に、既存のPDクラスタを停止してから、前のデータディレクトリを削除するか、 `--data-dir`を使用して新しいデータディレクトリを指定する必要があります。

### pd-recoverを使用する {#use-pd-recover}

1つのPDノードで`pd-recover`つだけ実行する必要があります。

{{< copyable "" >}}

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### クラスタ全体を再起動します {#restart-the-whole-cluster}

リカバリが成功したというプロンプト情報が表示されたら、クラスタ全体を再起動します。

## FAQ {#faq}

### クラスタIDを取得すると、複数のクラスタIDが見つかります {#multiple-cluster-ids-are-found-when-getting-the-cluster-id}

PDクラスタが作成されると、新しいクラスタIDが生成されます。ログを表示することで、古いクラスタのクラスタIDを確認できます。

### エラー<code>dial tcp 10.0.1.13:2379: connect: connection refused</code> <code>pd-recover</code>実行時に接続が拒否されました {#the-error-code-dial-tcp-10-0-1-13-2379-connect-connection-refused-code-is-returned-when-executing-code-pd-recover-code}

`pd-recover`を実行する場合はPDサービスが必要です。 PDリカバリを使用する前に、PDクラスタをデプロイして開始します。
