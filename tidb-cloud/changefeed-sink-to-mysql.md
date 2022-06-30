---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# MySQLにシンク {#sink-to-mysql}

> **警告：**
>
> 現在、 **SinktoMySQL**は実験的機能です。実稼働環境での使用はお勧めしません。

このドキュメントでは、SinktoMySQLチェンジフィードを使用してTiDB Cloud**から**MySQLにデータをストリーミングする方法について説明します。

## 前提条件 {#prerequisites}

### 通信網 {#network}

TiDBクラスターがMySQLサービスに接続できることを確認してください。

MySQLサービスがパブリックインターネットアクセスのないAWSVPCにある場合は、次の手順を実行します。

1.  MySQLサービスのVPCとTiDBクラスタの間の[VPCピアリング接続を設定します](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQLサービスが関連付けられているセキュリティグループのインバウンドルールを変更します。

    TiDB Cloudクラスタが配置されているリージョンのCIDRをインバウンドルールに追加する必要があります。 CIDRは、VPCピアリングページにあります。そうすることで、トラフィックがTiDBクラスターからMySQLインスタンスに流れるようになります。

3.  MySQL URLにホスト名が含まれている場合は、 TiDB CloudがMySQLサービスのDNSホスト名を解決できるようにする必要があります。

    1.  [VPCピアリング接続のDNS解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **AccepterDNS解決**オプションを有効にします。

MySQLサービスがパブリックインターネットアクセスのないGCPVPCにある場合は、次の手順を実行します。

1.  MySQLサービスがGoogleCloudSQLの場合、GoogleCloudSQLインスタンスの関連付けられたVPCでMySQLエンドポイントを公開する必要があります。あなたはグーグルによって開発された[**CloudSQLAuthプロキシ**](https://cloud.google.com/sql/docs/mysql/sql-proxy)を使う必要があるかもしれません。
2.  MySQLサービスのVPCとTiDBクラスタの間の[VPCピアリング接続を設定します](/tidb-cloud/set-up-vpc-peering-connections.md) 。
3.  MySQLが配置されているVPCの入力ファイアウォールルールを変更します。

    TiDB Cloudクラスタが配置されているリージョンのCIDRを入力ファイアウォールルールに追加する必要があります。 CIDRは、VPCピアリングページにあります。そうすることで、トラフィックがTiDBクラスターからMySQLエンドポイントに流れるようになります。

### 全負荷データ {#full-load-data}

**Sink to MySQL**コネクタは、特定のタイムスタンプの後にのみ、TiDBクラスタからMySQLに増分データをシンクできます。 TiDBクラスタにすでにデータがある場合は、 <strong>Sink to MySQL</strong>を有効にする前に、TiDBクラスタのフルロードデータをエクスポートしてMySQLにロードする必要があります。

1.  [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)を次の2つの操作の合計時間より長くするように拡張して、その間の履歴データがTiDBによってガベージコレクションされないようにします。

    -   全負荷データをエクスポートおよびインポートする時間
    -   **SinktoMySQL**を作成する時間

    例えば：

    {{< copyable "" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用してTiDBクラスタからデータをエクスポートしてから、 [mydumper / myloader](https://centminmod.com/mydumper.html)などのコミュニティツールを使用してMySQLサービスにデータをロードします。

3.  [Dumplingのエクスポートファイル](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)から、メタデータファイルからTSOを取得します。

    {{< copyable "" >}}

    ```shell
    cat metadata
    ```

    以下は出力例です。 「SHOWMASTERSTATUS」の「Pos」は、全負荷データのTSOです。

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

## シンクを作成する {#create-a-sink}

前提条件を完了したら、データをMySQLにシンクできます。

1.  **TiDB**クラスタの[チェンジフィード]タブに移動します。
2.  [ **MySQLにシンク]を**クリックします。
3.  MySQLのURL、ユーザー、およびパスワードを入力します。
    -   TiDBクラスターにすでにデータがある場合は、 Dumplingが提供する特定のTSO番号を入力する必要があります。
    -   TiDBクラスターにデータがない場合は、「現在の」TSOを選択できます。
4.  [**接続のテスト]**をクリックします。 TiDBクラスターがMySQLサービスに接続できる場合は、[<strong>確認</strong>]ボタンが表示されます。
5.  [**確認**]をクリックすると、しばらくするとシンクが動作を開始し、シンクのステータスが[<strong>生産</strong>中]に変わります。
6.  操作が完了したら、GC時間を元に戻します（デフォルト値は`10m`です）。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## シンクを削除する {#delete-a-sink}

1.  クラスタの[**チェンジフィード**]タブに移動します。
2.  SinktoMySQLのゴミ箱ボタンをクリック**します**。

## 制限 {#restrictions}

TiDB CloudはTiCDCを使用してチェンジフィードを確立するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions)があります。
