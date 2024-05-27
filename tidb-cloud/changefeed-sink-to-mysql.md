---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# MySQLに沈む {#sink-to-mysql}

このドキュメントでは**、Sink to MySQL**変更フィードを使用してTiDB Cloudから MySQL にデータをストリーミングする方法について説明します。

> **注記：**
>
> -   changefeed 機能を使用するには、TiDB 専用クラスターのバージョンが v6.1.3 以降であることを確認してください。
> -   [TiDB サーバーレス クラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)の場合、changefeed 機能は使用できません。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 100 個の変更フィードを作成できます。
-   TiDB Cloud は変更フィードを確立するために TiCDC を使用するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)持ちます。
-   複製するテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、複製中に一意の制約がないと、再試行シナリオによっては下流に重複したデータが挿入される可能性があります。

## 前提条件 {#prerequisites}

変更フィードを作成する前に、次の前提条件を完了する必要があります。

-   ネットワーク接続を設定する
-   既存のデータをエクスポートして MySQL にロードする (オプション)
-   既存のデータをロードせず、増分データのみをMySQLに複製する場合は、MySQLに対応するターゲットテーブルを作成します。

### 通信網 {#network}

TiDB クラスタ がMySQL サービスに接続できることを確認します。

MySQL サービスがパブリックインターネットアクセスのない AWS VPC 内にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスター間の接続は[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    受信ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)追加する必要があります。これにより、トラフィックが TiDBクラスタから MySQL インスタンスに流れるようになります。

3.  MySQL URL にホスト名が含まれている場合は、 TiDB Cloud がMySQL サービスの DNS ホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

MySQL サービスがパブリック インターネット アクセスのない Google Cloud VPC 内にある場合は、次の手順に従います。

1.  MySQL サービスが Google Cloud SQL の場合、Google Cloud SQL インスタンスに関連付けられた VPC で MySQL エンドポイントを公開する必要があります。Google によって開発された[**Cloud SQL 認証プロキシ**](https://cloud.google.com/sql/docs/mysql/sql-proxy)を使用する必要がある場合があります。
2.  MySQL サービスの VPC と TiDB クラスター間の接続は[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。
3.  MySQL が配置されている VPC の Ingress ファイアウォール ルールを変更します。

    入力ファイアウォール ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)追加する必要があります。これにより、トラフィックが TiDBクラスタから MySQL エンドポイントに流れるようになります。

### 既存のデータを読み込む（オプション） {#load-existing-data-optional}

**Sink to MySQL**コネクタは、特定のタイムスタンプ以降に TiDB クラスターから MySQL に増分データをシンクすることしかできません。TiDB クラスターに既にデータがある場合は、 **Sink to MySQL**を有効にする前に、TiDB クラスターの既存のデータをエクスポートして MySQL にロードできます。

既存のデータをロードするには:

1.  その間、履歴データが TiDB によってガベージ コレクションされないように、 [tidb_gc_ライフタイム](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)次の 2 つの操作の合計時間よりも長く延長します。

    -   既存のデータをエクスポートおよびインポートする時間
    -   **Sink to MySQLを**作成する時間

    例えば：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用して TiDB クラスターからデータをエクスポートし、 [マイダンパー/マイローダー](https://centminmod.com/mydumper.html)などのコミュニティ ツールを使用してデータを MySQL サービスにロードします。

3.  [Dumplingのエクスポートファイル](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)から、メタデータ ファイルから MySQL シンクの開始位置を取得します。

    以下はメタデータ ファイルの例の一部です。3 のうち`Pos` `SHOW MASTER STATUS`データの TSO であり、MySQL シンクの開始位置でもあります。

        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124
        Finished dump at: 2020-11-10 10:40:20

### MySQLでターゲットテーブルを作成する {#create-target-tables-in-mysql}

既存のデータをロードしない場合は、TiDB からの増分データを保存するために、MySQL に対応するターゲット テーブルを手動で作成する必要があります。そうしないと、データは複製されません。

## MySQLシンクを作成する {#create-a-mysql-sink}

前提条件を完了したら、データを MySQL にシンクできます。

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。

2.  **「Changefeed の作成」**をクリックし、**ターゲット タイプ**として**MySQL**を選択します。

3.  **MySQL 接続**に MySQL エンドポイント、ユーザー名、およびパスワードを入力します。

4.  **「次へ」**をクリックして、TiDB が MySQL に正常に接続できるかどうかをテストします。

    -   はいの場合は、構成の次の手順に進みます。
    -   そうでない場合は、接続エラーが表示されるので、エラーを処理する必要があります。エラーが解決したら、もう一度**[次へ]**をクリックします。

5.  **テーブル フィルターを**カスタマイズして、複製するテーブルをフィルターします。ルール構文については、 [テーブルフィルタルール](/table-filter.md)を参照してください。

    -   **フィルター ルール**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルを複製するルール`*.*`があります。新しいルールを追加すると、 TiDB Cloud はTiDB 内のすべてのテーブルを照会し、右側のボックスにルールに一致するテーブルのみを表示します。最大 100 個のフィルター ルールを追加できます。
    -   **有効なキーを持つテーブル**: この列には、主キーや一意のインデックスなど、有効なキーを持つテーブルが表示されます。
    -   **有効なキーのないテーブル**: この列には、主キーまたは一意のキーがないテーブルが表示されます。これらのテーブルは、一意の識別子がないと、ダウンストリームが重複イベントを処理するときにデータの一貫性がなくなる可能性があるため、レプリケーション中に問題が発生します。データの一貫性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意のキーまたは主キーを追加することをお勧めします。または、フィルター ルールを追加して、これらのテーブルを除外することもできます。たとえば、ルール`"!test.tbl1"`を使用してテーブル`test.tbl1`を除外できます。

6.  **イベント フィルターを**カスタマイズして、複製するイベントをフィルターします。

    -   **一致するテーブル**: この列で、イベント フィルターを適用するテーブルを設定できます。ルールの構文は、前の**テーブル フィルター**領域で使用した構文と同じです。変更フィードごとに最大 10 個のイベント フィルター ルールを追加できます。
    -   **無視されるイベント**: イベント フィルターが変更フィードから除外するイベントの種類を設定できます。

7.  **「レプリケーションの開始位置**」で、MySQL シンクの開始位置を設定します。

    -   Dumpling[既存のデータをロードしました](#load-existing-data-optional)使用している場合は、 **「特定の TSO からレプリケーションを開始」**を選択し、 Dumplingからエクスポートされたメタデータ ファイルから取得した TSO を入力します。
    -   アップストリーム TiDB クラスターにデータがない場合は、 **「今すぐレプリケーションを開始する」**を選択します。
    -   それ以外の場合は、 **「特定の時間からレプリケーションを開始する」**を選択して開始時点をカスタマイズできます。

8.  **次へ**をクリックして、変更フィード仕様を構成します。

    -   **「Changefeed 仕様」**領域で、Changefeed で使用されるレプリケーション容量単位 (RCU) の数を指定します。
    -   **「Changefeed 名」**領域で、Changefeed の名前を指定します。

9.  **「次へ」**をクリックして、変更フィード構成を確認します。

    すべての構成が正しいことを確認したら、クロスリージョンレプリケーションのコンプライアンスを確認し、 **「作成」**をクリックします。

    いくつかの設定を変更する場合は、 **「前へ」**をクリックして前の設定ページに戻ります。

10. シンクはすぐに起動し、シンクのステータスが**「作成中**」から**「実行中**」に変わるのがわかります。

    変更フィード名をクリックすると、チェックポイント、レプリケーションのレイテンシー、その他のメトリックなど、変更フィードに関する詳細が表示されます。

11. Dumpling を使用して[既存のデータをロードしました](#load-existing-data-optional)持っている場合は、シンクの作成後に GC 時間を元の値 (デフォルト値は`10m` ) に戻す必要があります。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
