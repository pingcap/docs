---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# MySQL にシンク {#sink-to-mysql}

> **警告：**
>
> 現在、 **Sink to MySQL**機能はベータ版です。

このドキュメントでは、 **Sink to MySQL** changefeed を使用してTiDB Cloudから MySQL にデータをストリーミングする方法について説明します。

## 前提条件 {#prerequisites}

### 通信網 {#network}

TiDBクラスタが MySQL サービスに接続できることを確認してください。

MySQL サービスがパブリック インターネット アクセスのない AWS VPC にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR をインバウンド ルールに追加する必要があります。 CIDR は、VPC Peering Page で見つけることができます。そうすることで、トラフィックが TiDBクラスタから MySQL インスタンスに流れるようになります。

3.  MySQL URL にホスト名が含まれている場合、 TiDB Cloudが MySQL サービスの DNS ホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

MySQL サービスがパブリック インターネット アクセスのない GCP VPC にある場合は、次の手順を実行します。

1.  MySQL サービスが Google Cloud SQL の場合、Google Cloud SQL インスタンスの関連付けられた VPC で MySQL エンドポイントを公開する必要があります。 Google が開発した[**Cloud SQL 認証プロキシ**](https://cloud.google.com/sql/docs/mysql/sql-proxy)を使用する必要がある場合があります。
2.  MySQL サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。
3.  MySQL が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR をイングレス ファイアウォール ルールに追加する必要があります。 CIDR は、VPC Peering Page で見つけることができます。そうすることで、トラフィックが TiDBクラスタから MySQL エンドポイントに流れるようになります。

### 全負荷データ {#full-load-data}

**Sink to MySQL**コネクタは、特定のタイムスタンプの後にのみ、TiDB クラスターから MySQL に増分データをシンクできます。 TiDB クラスターに既にデータがある場合は、 <strong>Sink to MySQL</strong>を有効にする前に、TiDB クラスターの全ロード データをエクスポートして MySQL にロードする必要があります。

1.  次の 2 つの操作の合計時間よりも長くなるように[tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)を拡張して、その間の履歴データが TiDB によってガベージ コレクションされないようにします。

    -   全負荷データをエクスポートおよびインポートする時間
    -   **Sink to MySQL**を作成する時間

    例えば：

    {{< copyable "" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  [Dumpling](/dumpling-overview.md)を使用して TiDB クラスターからデータをエクスポートし、 [マイダンパー/マイローダー](https://centminmod.com/mydumper.html)などのコミュニティ ツールを使用してデータを MySQL サービスにロードします。

3.  [Dumplingのエクスポートファイル](/dumpling-overview.md#format-of-exported-files)から、メタデータ ファイルから TSO を取得します。

    {{< copyable "" >}}

    ```shell
    cat metadata
    ```

    以下は出力例です。 「SHOW MASTER STATUS」の「Pos」は全負荷データのTSOです。

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

## シンクを作成する {#create-a-sink}

前提条件を完了したら、データを MySQL にシンクできます。

1.  TiDB クラスターの**Changefeed**タブに移動します。
2.  [ **MySQL にシンク] を**クリックします。
3.  MySQL の URL、ユーザー、およびパスワードを入力します。
    -   TiDB クラスタに既にデータがある場合は、 Dumplingが提供する特定の TSO 番号を入力する必要があります。
    -   TiDB クラスタにデータがない場合は、「現在の」TSO を選択できます。
4.  [**接続のテスト]**をクリックします。 TiDBクラスタが MySQL サービスに接続できる場合は、[<strong>確認</strong>] ボタンが表示されます。
5.  [**確認**] をクリックすると、しばらくするとシンクが動作を開始し、シンクのステータスが [作成中] に<strong>変わり</strong>ます。
6.  操作が完了したら、GC 時間を元に戻します (デフォルト値は`10m`です)。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## シンクを削除する {#delete-a-sink}

1.  クラスターの**Changefeed**タブに移動します。
2.  **Sink to MySQL**のゴミ箱ボタンをクリックします。

## 制限 {#restrictions}

TiDB Cloudは TiCDC を使用して変更フィードを確立するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions)を持ちます。
