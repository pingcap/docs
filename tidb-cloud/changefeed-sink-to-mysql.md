---
title: Sink to MySQL
summary: このドキュメントでは、Sink to MySQL チェンジフィードを使用して、 TiDB Cloudから MySQL にデータをストリーミングする方法について説明します。制限事項、前提条件、そしてデータレプリケーション用の MySQL シンクを作成する手順について説明します。このプロセスでは、ネットワーク接続の設定、既存データの MySQL へのロード、そして MySQL でのターゲットテーブルの作成を行います。前提条件を満たせば、ユーザーは MySQL シンクを作成し、MySQL にデータをレプリケートできます。
---

# MySQLに沈む {#sink-to-mysql}

このドキュメントでは**、Sink to MySQL**変更フィードを使用してTiDB Cloudから MySQL にデータをストリーミングする方法について説明します。

<CustomContent plan="dedicated">

> **注記：**
>
> changefeed 機能を使用するには、 TiDB Cloud Dedicated クラスターのバージョンが v6.1.3 以降であることを確認してください。

</CustomContent>

## 制限 {#restrictions}

-   各TiDB Cloud<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>最大 100 個の変更フィードを作成できます。
-   TiDB Cloud は、変更フィードを確立するために TiCDC を使用するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)持ちます。
-   レプリケートするテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、レプリケーション中に一意の制約がないと、再試行シナリオによっては下流に重複したデータが挿入される可能性があります。

## 前提条件 {#prerequisites}

変更フィードを作成する前に、次の前提条件を完了する必要があります。

-   ネットワーク接続を設定する
-   既存のデータをMySQLにエクスポートしてロードする（オプション）
-   既存のデータをロードせず、増分データのみをMySQLに複製する場合は、MySQLに対応するターゲットテーブルを作成します。

### ネットワーク {#network}

<CustomContent plan="dedicated">

TiDB Cloudクラスターが MySQL サービスに接続できることを確認します。

<SimpleTab>
<div label="VPC Peering">

MySQL サービスがパブリックインターネットアクセスのない AWS VPC 内にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスター間の[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    受信ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)追加する必要があります。これにより、TiDB クラスタからMySQLインスタンスへのトラフィックが許可されます。

3.  MySQL URL にホスト名が含まれている場合は、 TiDB Cloud がMySQL サービスの DNS ホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

MySQL サービスがパブリック インターネット アクセスのない Google Cloud VPC 内にある場合は、次の手順に従います。

1.  MySQLサービスがGoogle Cloud SQLの場合、Google Cloud SQLインスタンスに関連付けられたVPCでMySQLエンドポイントを公開する必要があります。Googleが開発した[**Cloud SQL 認証プロキシ**](https://cloud.google.com/sql/docs/mysql/sql-proxy)を使用する必要がある場合があります。
2.  MySQL サービスの VPC と TiDB クラスター間の[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。
3.  MySQL が配置されている VPC の受信ファイアウォール ルールを変更します。

    入口ファイアウォールルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)追加する必要があります。これにより、 TiDB Cloudクラスターから MySQL エンドポイントへのトラフィックが許可されます。

</div>

<div label="Private Endpoint">

プライベート エンドポイントは、クラウド プロバイダーの**Private Link**または**Private Service Connect**テクノロジーを活用し、VPC 内のリソースが、あたかもそれらのサービスが VPC 内で直接ホストされているかのように、プライベート IP アドレスを介して他の VPC 内のサービスに接続できるようにします。

TiDB Cloudクラスターは、プライベートエンドポイントを介して MySQL サービスに安全に接続できます。MySQL サービスでプライベートエンドポイントが利用できない場合は、手順[Changefeeds のプライベート エンドポイントを設定する](/tidb-cloud/set-up-sink-private-endpoint.md)に従って作成してください。

</div>

</SimpleTab>

</CustomContent>

<CustomContent plan="premium">

TiDB Cloudインスタンスが MySQL サービスに接続できることを確認します。

> **注記：**
>
> 現在、 TiDB Cloud PremiumインスタンスのVPCピアリング機能は、リクエストに応じてのみご利用いただけます。この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポートをリクエスト」**をクリックしてください。次に、「**説明」**欄に「 TiDB Cloud PremiumインスタンスのVPCピアリングを申請」と入力し、 **「送信」を**クリックしてください。

プライベート エンドポイントは、クラウド プロバイダーの**Private Link**または**Private Service Connect**テクノロジーを活用し、VPC 内のリソースが、あたかもそれらのサービスが VPC 内で直接ホストされているかのように、プライベート IP アドレスを介して他の VPC 内のサービスに接続できるようにします。

TiDB Cloudインスタンスは、プライベートエンドポイントを介してMySQLサービスに安全に接続できます。MySQLサービスでプライベートエンドポイントが利用できない場合は、手順[Changefeeds のプライベート エンドポイントを設定する](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md)に従って作成してください。

</CustomContent>

### 既存のデータを読み込む（オプション） {#load-existing-data-optional}

<CustomContent plan="dedicated">

**Sink to MySQL**コネクタは、特定のタイムスタンプ以降の増分データをTiDBクラスタからMySQLにシンクすることのみ可能です。TiDBクラスタに既にデータがある場合は、 **Sink to MySQL**を有効にする前に、TiDBクラスタの既存データをエクスポートしてMySQLにロードすることができます。

</CustomContent>
<CustomContent plan="premium">

**Sink to MySQL**コネクタは、特定のタイムスタンプ以降の増分データをTiDBインスタンスからMySQLにシンクすることのみ可能です。TiDBインスタンスに既にデータがある場合は、 **Sink to MySQL**を有効にする前に、TiDBインスタンスの既存データをエクスポートしてMySQLにロードすることができます。

</CustomContent>

既存のデータをロードするには:

1.  その間、履歴データが TiDB によってガベージ コレクションされないように、 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50)次の 2 つの操作の合計時間よりも長く延長します。

    -   既存のデータをエクスポートおよびインポートする時間
    -   **Sink to MySQL**を作成する時間

    例えば：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2.  [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用してTiDBからデータをエクスポートします<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>次に、 [マイダンパー/マイローダー](https://centminmod.com/mydumper.html)などのコミュニティ ツールを使用して、MySQL サービスにデータをロードします。

3.  [Dumplingのエクスポートファイル](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)から、メタデータ ファイルから MySQL シンクの開始位置を取得します。

    以下はメタデータファイルの例の一部です。1/ `Pos` `SHOW MASTER STATUS`既存データのTSOであり、MySQLシンクの開始位置でもあります。

        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124
        Finished dump at: 2020-11-10 10:40:20

### MySQLでターゲットテーブルを作成する {#create-target-tables-in-mysql}

既存データをロードしない場合は、TiDBからの増分データを保存するために、MySQLに対応するターゲットテーブルを手動で作成する必要があります。そうしないと、データは複製されません。

## MySQLシンクを作成する {#create-a-mysql-sink}

前提条件を完了したら、データを MySQL にシンクできます。

1.  ターゲットTiDBの概要ページに移動します<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>をクリックし、左側のナビゲーション ウィンドウで**[データ]** &gt; **[Changefeed]**をクリックします。

2.  **「Changefeed の作成」**をクリックし、**宛先**として**MySQL**を選択します。

3.  **「接続方法」**で、MySQL サービスに接続する方法を選択します。

    -   **VPC ピアリング**または**パブリック IP**を選択した場合は、MySQL エンドポイントを入力します。
    -   **Private Link**を選択した場合は、セクション[ネットワーク](#network)で作成したプライベート エンドポイントを選択し、MySQL サービスの MySQL ポートを入力します。

4.  **「認証」**で、MySQL サービスの MySQL ユーザー名とパスワードを入力します。

5.  **「次へ」**をクリックして、TiDB が MySQL に正常に接続できるかどうかをテストします。

    -   はいの場合は、構成の次の手順に進みます。
    -   そうでない場合は接続エラーが表示されるので、エラーに対処する必要があります。エラーが解決したら、もう一度**「次へ」**をクリックしてください。

6.  **テーブルフィルター**をカスタマイズして、複製するテーブルをフィルタリングします。ルールの構文については、 [テーブルフィルタルール](/table-filter.md)を参照してください。

    -   **大文字と小文字を区別**: フィルタールール内のデータベース名とテーブル名のマッチングで大文字と小文字を区別するかどうかを設定できます。デフォルトでは、大文字と小文字は区別されません。
    -   **フィルタールール**: この列でフィルタールールを設定できます。デフォルトでは、すべてのテーブルを複製するルール`*.*`が設定されています。新しいルールを追加すると、 TiDB CloudはTiDB内のすべてのテーブルをクエリし、ルールに一致するテーブルのみを右側のボックスに表示されます。フィルタールールは最大100件まで追加できます。
    -   **有効なキーを持つテーブル**: この列には、主キーや一意のインデックスなどの有効なキーを持つテーブルが表示されます。
    -   **有効なキーのないテーブル**: この列には、主キーまたは一意キーを持たないテーブルが表示されます。これらのテーブルは、一意の識別子がないと、下流で重複イベントを処理する際にデータの不整合が発生する可能性があるため、レプリケーション中に問題が発生します。データの整合性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意のキーまたは主キーを追加することをお勧めします。または、これらのテーブルを除外するフィルタールールを追加することもできます。例えば、ルール`"!test.tbl1"`を使用してテーブル`test.tbl1`を除外できます。

7.  **イベント フィルター**をカスタマイズして、複製するイベントをフィルターします。

    -   **一致するテーブル**: この列では、イベントフィルターを適用するテーブルを設定できます。ルールの構文は、前述の**「テーブルフィルター」**領域で使用した構文と同じです。変更フィードごとに最大10個のイベントフィルタールールを追加できます。
    -   **イベント フィルター**: 次のイベント フィルターを使用して、変更フィードから特定のイベントを除外できます。
        -   **イベントを無視**: 指定されたイベント タイプを除外します。
        -   **SQLを無視**: 指定した式に一致するDDLイベントを除外します。例えば、 `^drop`指定すると`DROP`で始まる文が除外され、 `add column`指定すると`ADD COLUMN`を含む文が除外されます。
        -   **挿入値式を無視**: 特定の条件を満たす`INSERT`文を除外します。例えば、 `id >= 100`指定すると、 `id`が100以上の`INSERT`文が除外されます。
        -   **新しい値の更新式を無視**: 新しい値が指定条件に一致する`UPDATE`文を除外します。例えば、 `gender = 'male'`指定すると、 `gender`が`male`になる更新は除外されます。
        -   **更新前の値を無視**: 指定した条件に一致する古い値を持つステートメントを`UPDATE`除外します。例えば、 `age < 18`指定すると、古い値`age`が18未満となる更新は除外されます。
        -   **削除値式を無視**: 指定された条件を満たす`DELETE`文を除外します。例えば、 `name = 'john'`指定すると、 `name`が`'john'`となる`DELETE`文が除外されます。

8.  **「レプリケーションの開始位置」**で、MySQL シンクの開始位置を設定します。

    -   [既存のデータをロードしました](#load-existing-data-optional)を使用している場合は、 **[特定の TSO からレプリケーションを開始]**を選択し、 Dumplingからエクスポートされたメタデータ ファイルから取得した TSO を入力します。
    -   上流TiDBにデータがない場合<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>で、 **[今すぐレプリケーションを開始する]**を選択します。
    -   それ以外の場合は、 **[特定の時刻からレプリケーションを開始する]**を選択して開始時刻をカスタマイズできます。

9.  **次へ**をクリックして、変更フィード仕様を構成します。

    -   **チェンジフィード仕様**エリアで、<customcontent plan="dedicated">レプリケーション容量単位（RCU）</customcontent><customcontent plan="premium">チェンジフィード容量単位（CCU）</customcontent>チェンジフィードによって使用されます。
    -   **「Changefeed 名」**領域で、Changefeed の名前を指定します。

10. **「次へ」**をクリックして、変更フィード構成を確認します。

    すべての構成が正しいことを確認したら、リージョン間レプリケーションのコンプライアンスをチェックし、 **「作成」**をクリックします。

    設定を変更する場合は、 **「前へ」**をクリックして前の設定ページに戻ります。

11. シンクはすぐに起動し、シンクのステータスが**「作成中」**から**「実行中」**に変わることがわかります。

    変更フィード名をクリックすると、チェックポイント、レプリケーションのレイテンシー、その他のメトリックなど、変更フィードに関する詳細が表示されます。

12. Dumplingを使用して[既存のデータをロードしました](#load-existing-data-optional)持っている場合は、シンクが作成された後に GC 時間を元の値 (デフォルト値は`10m` ) に戻す必要があります。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
