---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# MySQL にシンク {#sink-to-mysql}

このドキュメントでは、 **Sink to MySQL** changefeed を使用してTiDB Cloudから MySQL にデータをストリーミングする方法について説明します。

> **ノート：**
>
> Changefeed 機能を使用するには、TiDB クラスターのバージョンが v6.4.0 以降であり、TiKV ノードのサイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。
>
> 現在、 TiDB Cloudでは、クラスターごとに最大 10 個の変更フィードしか許可されていません。
>
> [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)の場合、changefeed 機能は使用できません。

## 前提条件 {#prerequisites}

### 通信網 {#network}

TiDBクラスタが MySQL サービスに接続できることを確認してください。

MySQL サービスがパブリック インターネット アクセスのない AWS VPC にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    インバウンド規則に[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)を追加する必要があります。そうすることで、トラフィックが TiDBクラスタから MySQL インスタンスに流れるようになります。

3.  MySQL URL にホスト名が含まれている場合、 TiDB Cloudが MySQL サービスの DNS ホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

MySQL サービスがパブリック インターネット アクセスのない GCP VPC にある場合は、次の手順を実行します。

1.  MySQL サービスが Google Cloud SQL の場合、Google Cloud SQL インスタンスの関連付けられた VPC で MySQL エンドポイントを公開する必要があります。 Google が開発した[**Cloud SQL 認証プロキシ**](https://cloud.google.com/sql/docs/mysql/sql-proxy)を使用する必要がある場合があります。
2.  MySQL サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。
3.  MySQL が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    イングレス ファイアウォール ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)を追加する必要があります。そうすることで、トラフィックが TiDBクラスタから MySQL エンドポイントに流れるようになります。

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

3.  [Dumplingのエクスポートファイル](/dumpling-overview.md#format-of-exported-files)から、メタデータ ファイルから MySQL シンクの開始位置を取得します。

    以下は、メタデータ ファイルの例の一部です。 `Pos` of `SHOW MASTER STATUS`は全ロード データの TSO であり、MySQL シンクの開始位置でもあります。

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

## MySQL シンクを作成する {#create-a-mysql-sink}

前提条件を完了したら、データを MySQL にシンクできます。

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで [ **Changefeed** ] をクリックします。

2.  **Create Changefeed**をクリックし、<strong>ターゲット タイプ</strong>として<strong>MySQL</strong>を選択します。

3.  **MySQL Connection**に MySQL エンドポイント、ユーザー名、およびパスワードを入力します。

4.  [**次へ**] をクリックして、TiDB が MySQL に正常に接続できるかどうかをテストします。

    -   はいの場合、構成の次のステップに進みます。
    -   そうでない場合は、接続エラーが表示され、エラーを処理する必要があります。エラーが解決したら、もう一度 [**次へ**] をクリックします。

5.  **テーブル フィルタ**をカスタマイズして、複製するテーブルをフィルタリングします。ルールの構文については、 [テーブル フィルター規則](/table-filter.md)を参照してください。

    -   **フィルター ルールの追加**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルをレプリケートすることを表すルール`*. *`があります。新しいルールを追加すると、 TiDB Cloudは TiDB 内のすべてのテーブルに対してクエリを実行し、右側のボックスのルールに一致するテーブルのみを表示します。
    -   **レプリケートされる**テーブル: この列は、レプリケートされるテーブルを示します。ただし、将来レプリケートされる新しいテーブルや、完全にレプリケートされるスキーマは表示されません。
    -   **有効なキーのない**テーブル : この列には、一意キーと主キーのないテーブルが表示されます。これらのテーブルでは、重複イベントを処理するためにダウンストリーム システムで一意の識別子を使用できないため、レプリケーション中にデータの一貫性が失われる可能性があります。このような問題を回避するには、レプリケーションの前にこれらのテーブルに一意のキーまたは主キーを追加するか、これらのテーブルを除外するフィルター ルールを設定することをお勧めします。たとえば、「!test.tbl1」を使用してテーブル`test.tbl1`を除外できます。

6.  **[開始位置]**で、MySQL シンクの開始位置を構成します。

    -   Dumplingを使用して[全負荷データ](#full-load-data)を実行した場合は、[**特定の TSO からレプリケーションを開始する] を**選択し、エクスポートされたDumplingメタデータ ファイルから取得した TSO を入力します。
    -   上流の TiDB クラスターにデータがない場合は、[**今からレプリケーションを開始する] を選択し**ます。
    -   それ以外の場合は、 **[Start replication from a specific time]**を選択して開始時点をカスタマイズできます。

7.  [**次へ**] をクリックして、Changefeed 構成を確認します。

    すべての構成が正しいことを確認したら、クロスリージョン レプリケーションのコンプライアンスを確認し、 [**作成**] をクリックします。

    一部の構成を変更する場合は、[**前**へ] をクリックして前の構成ページに戻ります。

8.  シンクはすぐに開始され、シンクのステータスが「**作成**中」から「<strong>実行中</strong>」に変化することがわかります。

    [ **Sink to MySQL** ] カードをクリックすると、チェックポイント、レプリケーションレイテンシー、およびその他のメトリックを含む、Changfeed の実行ステータスがポップアップ ウィンドウに表示されます。

9.  Dumplingを使用して[全負荷データ](#full-load-data)を実行した場合は、シンクの作成後に GC 時間を元の値 (デフォルト値は`10m` ) に戻す必要があります。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 10 個の変更フィードを作成できます。
-   TiDB Cloudは TiCDC を使用して変更フィードを確立するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions)を持ちます。
