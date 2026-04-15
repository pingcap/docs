---
title: Sink to MySQL
summary: このドキュメントでは、Sink to MySQL changefeed を使用してTiDB Cloudから MySQL へデータをストリーミングする方法について説明します。制限事項、前提条件、およびデータレプリケーション用の MySQL シンクを作成する手順が含まれています。このプロセスには、ネットワーク接続の設定、既存データの MySQL へのロード、および MySQL でのターゲットテーブルの作成が含まれます。前提条件を満たした後、ユーザーは MySQL シンクを作成してデータを MySQL にレプリケートできます。
---

# MySQLにシンクする {#sink-to-mysql}

このドキュメントでは**、Sink to MySQL** changefeedを使用してTiDB CloudからMySQLにデータをストリーミングする方法について説明します。

<CustomContent plan="dedicated">

> **注記：**
>
> 変更フィード機能を使用するには、 TiDB Cloud Dedicatedクラスタのバージョンがv6.1.3以降であることを確認してください。

</CustomContent>

## 制限 {#restrictions}

-   <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>ごとに、最大 100 個の変更フィードを作成できます。
-   TiDB Cloud はTiCDC を使用して変更フィードを確立するため、同じ[TiCDCの制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)があります。
-   複製対象のテーブルに主キーまたはNULLを許容しない一意インデックスがない場合、複製中に一意制約が存在しないことで、一部の再試行シナリオにおいて、下流で重複データが挿入される可能性があります。

## 前提条件 {#prerequisites}

変更フィードを作成する前に、以下の前提条件を満たす必要があります。

-   ネットワーク接続を設定する
-   既存データをエクスポートしてMySQLにロードする（オプション）
-   既存のデータをロードせず、増分データのみをMySQLに複製する場合は、MySQLに対応するターゲットテーブルを作成してください。

### ネットワーク {#network}

<CustomContent plan="dedicated">

TiDB Cloud Dedicatedクラスターが MySQL サービスに接続できることを確認してください。

<SimpleTab>
<div label="VPC Peering">

MySQLサービスがパブリックインターネットアクセスを持たないAWS VPC内にある場合は、以下の手順を実行してください。

1.  MySQL サービスの VPC とTiDB Cloud Dedicatedクラスターの間で[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)。

2.  MySQLサービスが関連付けられているセキュリティグループの受信ルールを変更します。

    [TiDB Cloud Dedicatedクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)受信ルールに追加する必要があります。これにより、 TiDB Cloud Dedicatedクラスターから MySQL インスタンスにトラフィックが流れるようになります。

3.  MySQLのURLにホスト名が含まれている場合、 TiDB CloudがMySQLサービスのDNSホスト名を解決できるようにする必要があります。

    1.  [VPCピアリング接続のDNS解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **アクセプターDNS解決**オプションを有効にする。

MySQL サービスがパブリック インターネット アクセスのない Google Cloud VPC 内にある場合は、以下の手順を実行してください。

1.  MySQL サービスが Google Cloud SQL の場合、Google Cloud SQL インスタンスに関連付けられた VPC に MySQL エンドポイントを公開する必要があります。Cloud [**Cloud SQL認証プロキシ**](https://cloud.google.com/sql/docs/mysql/sql-proxy)使用する必要がある場合があります。これは Google によって開発されています。
2.  MySQL サービスの VPC とTiDB Cloud Dedicatedクラスターの間で[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)。
3.  MySQLが配置されているVPCの受信ファイアウォールルールを変更します。

    [TiDB Cloud Dedicatedクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)イングレス ファイアウォール ルールに追加する必要があります。これにより、 TiDB Cloud Dedicatedクラスターから MySQL エンドポイントにトラフィックが流れるようになります。

</div>

<div label="Private Endpoint">

プライベートエンドポイントは、クラウドプロバイダーの**プライベートリンク**または**プライベートサービスコネクト**技術を活用し、VPC内のリソースがプライベートIPアドレスを介して他のVPC内のサービスに接続できるようにします。これにより、あたかもそれらのサービスがVPC内で直接ホストされているかのように動作します。

プライベート エンドポイントを介して、 TiDB Cloud Dedicatedクラスターを MySQL サービスに安全に接続できます。 MySQL サービスでプライベート エンドポイントが利用できない場合は、[Changefeeds用のプライベートエンドポイントを設定する](/tidb-cloud/set-up-sink-private-endpoint.md)に従って作成します。

</div>

</SimpleTab>

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud PremiumインスタンスがMySQLサービスに接続できることを確認してください。

> **注記：**
>
> 現在、この機能はリクエストに応じてのみ利用可能です。この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下隅にある**「？」**をクリックし、 次に**「サポートチケット」**をクリックして[ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/portals)に移動します。チケットを作成し、 **「説明」**フィールドに「TiDB Cloud PremiumインスタンスのVPCピアリングの申請」と入力して、 **「送信」を**クリックします。

プライベートエンドポイントは、クラウドプロバイダーの**プライベートリンク**または**プライベートサービスコネクト**技術を活用し、VPC内のリソースがプライベートIPアドレスを介して他のVPC内のサービスに接続できるようにします。これにより、あたかもそれらのサービスがVPC内で直接ホストされているかのように動作します。

プライベート エンドポイントを通じて、 TiDB Cloud Premium インスタンスを MySQL サービスに安全に接続できます。 MySQL サービスでプライベート エンドポイントが利用できない場合は、 [Changefeeds用のプライベートエンドポイントを設定する](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md)に従って作成します。

</CustomContent>

### 既存データの読み込み（オプション） {#load-existing-data-optional}

<CustomContent plan="dedicated">

**Sink to MySQL**コネクタは、特定のタイムスタンプ以降の増分データのみをTiDB Cloud DedicatedクラスタからMySQLにシンクできます。TiDB TiDB Cloud Dedicatedクラスタに既にデータが存在する場合は、 **Sink to MySQL**を有効にする前に、 TiDB Cloud Dedicatedクラスタの既存データをエクスポートしてMySQLにロードすることができます。

</CustomContent>
<CustomContent plan="premium">

**Sink to MySQL**コネクタは、特定のタイムスタンプ以降の増分データのみをTiDB Cloud PremiumインスタンスからMySQLにシンクできます。TiDB TiDB Cloud Premiumインスタンスに既にデータが存在する場合は、 **Sink to MySQL**を有効にする前に、 TiDB Cloud Premiumインスタンスの既存データをエクスポートしてMySQLにロードすることができます。

</CustomContent>

既存のデータを読み込むには：

1.  [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)以下の 2 つの操作の合計時間よりも長く設定することで、その期間中の履歴データが TiDB によってガベージ コレクションされないようにします。

    -   既存データのエクスポートとインポートにかかる時間
    -   **Sink to MySQL**を作成する時間

    例えば：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>インスタンスからデータをエクスポートし、 [mydumper/myloader](https://centminmod.com/mydumper.html)などのコミュニティ ツールを使用してデータを MySQL サービスにロードします。

3.  [Dumplingのエクスポートファイル](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)のメタデータ ファイルから MySQL シンクの開始位置を取得します。

    以下はメタデータファイルの例の一部です。 `Pos`の`SHOW MASTER STATUS`は、既存データの TSO であり、MySQL シンクの開始位置でもあります。

        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124
        Finished dump at: 2020-11-10 10:40:20

### MySQLでターゲットテーブルを作成する {#create-target-tables-in-mysql}

既存のデータをロードしない場合は、TiDBからの増分データを保存するために、MySQLに該当するターゲットテーブルを手動で作成する必要があります。そうしないと、データは複製されません。

## MySQLシンクを作成する {#create-a-mysql-sink}

前提条件を満たしたら、データをMySQLに取り込むことができます。

1.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[変更フィード]**をクリックします。

2.  **「変更フィードの作成」**をクリックし、**宛先**として**「MySQL」**を選択します。

3.  **「接続方法」**で、MySQLサービスへの接続方法を選択してください。

    -   **VPCピアリング**または**パブリックIP**を選択した場合は、MySQLエンドポイントを入力してください。
    -   **「プライベートリンク」**を選択した場合は、[ネットワーク](#network)セクションで作成したプライベートエンドポイントを選択し、MySQLサービスのMySQLポートを入力してください。

4.  **「認証」**欄に、MySQLサービスのユーザー名とパスワードを入力してください。

5.  **「次へ」**をクリックして、TiDBがMySQLに正常に接続できるかどうかをテストしてください。

    -   はいの場合、次の設定手順に進みます。
    -   そうでない場合は、接続エラーが表示されますので、エラーを処理してください。エラーが解決したら、もう一度**「次へ」**をクリックしてください。

6.  **テーブル フィルターを**カスタマイズして、複製するテーブルをフィルターします。ルールの構文については、[テーブルフィルタルール](/table-filter.md)を参照してください。

    -   **大文字小文字の区別**：フィルタルールにおけるデータベース名とテーブル名の照合において、大文字小文字を区別するかどうかを設定できます。デフォルトでは、大文字小文字は区別されません。
    -   **フィルタルール**：この列でフィルタルールを設定できます。デフォルトでは、すべてのテーブルを複製するルール`*.*`が設定されています。新しいルールを追加すると、 TiDB Cloud はTiDB 内のすべてのテーブルをクエリし、右側のボックスにルールに一致するテーブルのみを表示します。フィルタルールは最大 100 個まで追加できます。
    -   **有効なキーを持つテーブル**：この列には、主キーや一意インデックスなど、有効なキーを持つテーブルが表示されます。
    -   **有効なキーのないテーブル**: この列には、主キーまたは一意キーがないテーブルが表示されます。一意の識別子がないと、ダウンストリームが重複イベントを処理する際にデータの一貫性が失われる可能性があるため、これらのテーブルはレプリケーション中に問題となります。データの一貫性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意キーまたは主キーを追加することをお勧めします。または、フィルタルールを追加してこれらのテーブルを除外することもできます。たとえば、ルール`test.tbl1`を使用して、テーブル`"!test.tbl1"`除外できます。

7.  **イベントフィルター**をカスタマイズして、複製したいイベントを絞り込みます。

    -   **一致するテーブル**：この列では、イベントフィルターを適用するテーブルを設定できます。ルールの構文は、前の**テーブルフィルター**領域で使用されているものと同じです。変更フィードごとに最大10個のイベントフィルタールールを追加できます。
    -   **イベントフィルター**：以下のイベントフィルターを使用して、変更フィードから特定のイベントを除外できます。
        -   **イベントを無視する**：指定されたイベントタイプを除外します。
        -   **SQL を無視**: 指定された式に一致する DDL イベントを除外します。たとえば、 `^drop` `DROP`で始まるステートメントを除外し、 `add column`は`ADD COLUMN`を含むステートメントを除外します。
        -   **挿入値の式を無視する**: 特定の条件を満たす`INSERT`ステートメントを除外します。たとえば、 `id >= 100`は、 `INSERT`が 100 以上である`id`ステートメントを除外します。
        -   **新しい値の更新式を無視する**: 新しい値が指定された条件に一致する`UPDATE`ステートメントを除外します。たとえば、 `gender = 'male'`は`gender`が`male`になるような更新を除外します。
        -   **古い値の更新を無視する式**: 古い値が指定された条件に一致する`UPDATE`ステートメントを除外します。たとえば、 `age < 18` `age`の古い値が 18 未満である場合の更新を除外します。
        -   **削除値式を無視する**: 指定された条件を満たす`DELETE`ステートメントを除外します。たとえば、 `name = 'john'`は`DELETE`が`name`である`'john'`ステートメントを除外します。

8.  **「レプリケーション開始位置」**で、MySQLシンクの開始位置を設定します。

    -   Dumplingを使用して[既存のデータをロードしました](#load-existing-data-optional)がある場合は、 **[特定の TSO からレプリケーションを開始する]**を選択し、 Dumpling のエクスポートされたメタデータ ファイルから取得した TSO を入力します。
    -   アップストリームの TiDB にデータがない場合は、 **「今すぐレプリケーションを開始する」**を選択してください。
    -   それ以外の場合は、 **「特定の時間からレプリケーションを開始する」**を選択して、開始時刻をカスタマイズできます。

9.  **「次へ」**をクリックして、変更フィードの仕様を設定してください。

    -   **「チェンジフィードの仕様」**領域で、チェンジフィードで使用する<CustomContent plan="dedicated">複製容量単位（RCU）</CustomContent>チェンジフィード<CustomContent plan="premium">チェンジフィード容量ユニット（CCU）</CustomContent>の数を指定します。
    -   **変更フィード名**欄に、変更フィードの名前を指定します。

10. **「次へ」**をクリックして、変更フィードの設定を確認してください。

    すべての構成が正しいことを確認したら、リージョン間レプリケーションの準拠性をチェックし、 **[作成]**をクリックします。

    設定を変更したい場合は、 **「前へ」**をクリックして前の設定ページに戻ってください。

11. シンクはまもなく開始され、シンクのステータスが**「作成中」**から**「実行中」**に変わるのが確認できます。

    変更フィード名をクリックすると、チェックポイント、レプリケーションレイテンシー、その他のメトリックなど、変更フィードに関する詳細情報が表示されます。

12. Dumplingを使用している場合は、[既存のデータをロードしました](#load-existing-data-optional)後に GC 時間を元の値 (デフォルト値は`10m` ) に戻す必要があります。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
