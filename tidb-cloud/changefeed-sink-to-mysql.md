---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# MySQL にシンクする {#sink-to-mysql}

このドキュメントでは、 **Sink to MySQL**変更フィードを使用してTiDB Cloudから MySQL にデータをストリーミングする方法について説明します。

> **注記：**
>
> -   チェンジフィード機能を使用するには、TiDB 専用クラスターのバージョンが v6.4.0 以降であることを確認してください。
> -   [TiDB サーバーレスクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)の場合、チェンジフィード機能は使用できません。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 5 つの変更フィードを作成できます。
-   TiDB Cloud はTiCDC を使用して変更フィードを確立するため、同じ[TiCDC としての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)を持ちます。
-   レプリケートされるテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、レプリケーション中に一意制約がないため、一部の再試行シナリオでは重複したデータがダウンストリームに挿入される可能性があります。

## 前提条件 {#prerequisites}

変更フィードを作成する前に、次の前提条件を満たしている必要があります。

-   ネットワーク接続をセットアップする
-   既存のデータを MySQL にエクスポートしてロードします (オプション)
-   既存のデータをロードせず、増分データのみを MySQL にレプリケートする場合は、対応するターゲット テーブルを MySQL に作成します。

### 通信網 {#network}

TiDBクラスタが MySQL サービスに接続できることを確認してください。

MySQL サービスがパブリック インターネット アクセスのない AWS VPC 内にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスターの間は[VPC ピアリング接続をセットアップする](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    受信ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)を追加する必要があります。これにより、トラフィックが TiDBクラスタから MySQL インスタンスに流れるようになります。

3.  MySQL URL にホスト名が含まれている場合は、 TiDB Cloud がMySQL サービスの DNS ホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **アクセプター DNS 解決**オプションを有効にします。

MySQL サービスがパブリック インターネット アクセスのない Google Cloud VPC 内にある場合は、次の手順を実行します。

1.  MySQL サービスが Google Cloud SQL の場合は、Google Cloud SQL インスタンスの関連する VPC で MySQL エンドポイントを公開する必要があります。 Google が開発した[**Cloud SQL 認証プロキシ**](https://cloud.google.com/sql/docs/mysql/sql-proxy)を使用する必要がある場合があります。
2.  MySQL サービスの VPC と TiDB クラスターの間は[VPC ピアリング接続をセットアップする](/tidb-cloud/set-up-vpc-peering-connections.md) 。
3.  MySQL が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    受信ファイアウォール ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)を追加する必要があります。これにより、トラフィックが TiDBクラスタから MySQL エンドポイントに流れるようになります。

### 既存のデータをロードする (オプション) {#load-existing-data-optional}

**Sink to MySQL**コネクタは、特定のタイムスタンプ後に TiDB クラスターから MySQL に増分データのみをシンクできます。 TiDB クラスターに既にデータがある場合は、 **「Sink to MySQL」**を有効にする前に、TiDB クラスターの既存のデータを MySQL にエクスポートしてロードできます。

既存のデータをロードするには:

1.  [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)次の 2 つの操作の合計時間よりも長くして、その間の履歴データが TiDB によってガベージ コレクションされないようにします。

    -   既存のデータをエクスポートおよびインポートする時間
    -   **Sink to MySQL を**作成する時期が来ました

    例えば：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して TiDB クラスターからデータをエクスポートし、myloader などのコミュニティ ツールを使用してデータを MySQL サービスにロードします。

3.  [Dumplingのエクスポートされたファイル](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)から、メタデータ ファイルから MySQL シンクの開始位置を取得します。

    以下は、メタデータ ファイルの例の一部です。 `SHOW MASTER STATUS`の`Pos`既存データの TSO であり、MySQL シンクの開始位置でもあります。

        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124
        Finished dump at: 2020-11-10 10:40:20

### MySQLでターゲットテーブルを作成する {#create-target-tables-in-mysql}

既存のデータをロードしない場合は、MySQL に対応するターゲット テーブルを手動で作成し、TiDB からの増分データを保存する必要があります。そうしないと、データは複製されません。

## MySQL シンクを作成する {#create-a-mysql-sink}

前提条件を完了したら、データを MySQL にシンクできます。

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。

2.  **[Create Changefeed]**をクリックし、 **[Target Type]**として**[MySQL]**を選択します。

3.  MySQL エンドポイント、ユーザー名、およびパスワードを**MySQL Connection**に入力します。

4.  **[次へ]**をクリックして、TiDB が MySQL に正常に接続できるかどうかをテストします。

    -   「はい」の場合、次の構成ステップに進みます。
    -   そうでない場合は、接続エラーが表示されるため、エラーを処理する必要があります。エラーが解決したら、もう一度**「次へ」**をクリックします。

5.  **テーブル フィルターを**カスタマイズして、複製するテーブルをフィルターします。ルールの構文については、 [テーブルフィルタールール](/table-filter.md)を参照してください。

    -   **フィルター ルールの追加**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルを複製することを表すルール`*. *`があります。新しいルールを追加すると、 TiDB CloudはTiDB 内のすべてのテーブルをクエリし、ルールに一致するテーブルのみを右側のボックスに表示します。
    -   **複製されるテーブル**: この列には、複製されるテーブルが表示されます。ただし、今後複製​​される新しいテーブルや完全に複製されるスキーマは表示されません。
    -   **有効なキーのないテーブル**: この列には、一意キーと主キーのないテーブルが表示されます。これらのテーブルでは、ダウンストリーム システムが重複イベントを処理するために一意の識別子を使用できないため、レプリケーション中にデータが不整合になる可能性があります。このような問題を回避するには、レプリケーションの前にこれらのテーブルに一意キーまたは主キーを追加するか、これらのテーブルをフィルターで除外するフィルター ルールを設定することをお勧めします。たとえば、「!test.tbl1」を使用してテーブル`test.tbl1`を除外できます。

6.  **[開始位置]**で、MySQL シンクの開始位置を構成します。

    -   [既存のデータをロードしました](#load-existing-data-optional)を使用してDumplingを使用している場合は、 **[特定の TSO からレプリケーションを開始する]**を選択し、 Dumplingのエクスポートされたメタデータ ファイルから取得した TSO を入力します。
    -   上流の TiDB クラスターにデータがない場合は、 **「今からレプリケーションを開始する」**を選択します。
    -   それ以外の場合は、 **[Start replication from specific time]**を選択して開始時点をカスタマイズできます。

7.  **「次へ」**をクリックして、変更フィード仕様を構成します。

    -   **「変更フィードの仕様」**領域で、変更フィードで使用されるレプリケーション キャパシティ ユニット (RCU) の数を指定します。
    -   **「変更フィード名」**領域で、変更フィードの名前を指定します。

8.  **「次へ」**をクリックして、変更フィード構成を確認します。

    すべての構成が正しいことを確認したら、リージョン間のレプリケーションのコンプライアンスをチェックし、 **「作成」**をクリックします。

    一部の構成を変更する場合は、 **「前へ」**をクリックして前の構成ページに戻ります。

9.  すぐにシンクが起動し、シンクのステータスが「**作成中**」から「**実行中**」に変化することがわかります。

    変更フィード名をクリックすると、チェックポイント、レプリケーションレイテンシー、その他のメトリックなど、変更フィードに関する詳細が表示されます。

10. Dumplingを使用して[既存のデータをロードしました](#load-existing-data-optional)ある場合は、シンクの作成後に GC 時間を元の値 (デフォルト値は`10m` ) に戻す必要があります。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
