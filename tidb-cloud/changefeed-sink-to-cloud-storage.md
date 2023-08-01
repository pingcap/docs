---
title: Sink to Cloud Storage
Summary: Learn how to create a changefeed to stream data from a TiDB Dedicated cluster to cloud storage, such as Amazon S3.
---

# クラウドストレージにシンクする {#sink-to-cloud-storage}

このドキュメントでは、 TiDB Cloudからクラウドstorageにデータをストリーミングするためのチェンジフィードを作成する方法について説明します。現在、Amazon S3 のみがサポートされています。

> **ノート：**
>
> -   データをクラウドstorageにストリーミングするには、TiDB クラスターのバージョンが v7.1.0 以降であることを確認してください。 TiDB 専用クラスターを v7.1.0 以降にアップグレードするには、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md) .
> -   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの場合、チェンジフィード機能は使用できません。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 5 つの変更フィードを作成できます。
-   TiDB Cloud はTiCDC を使用して変更フィードを確立するため、同じ[TiCDC としての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)を持ちます。
-   レプリケートされるテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、レプリケーション中に一意制約がないため、一部の再試行シナリオでは重複したデータがダウンストリームに挿入される可能性があります。

## 変更フィードを作成する {#create-a-changefeed}

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。

2.  **[変更フィードの作成]**をクリックし、宛先として**Amazon S3**を選択します。

3.  **[S3 エンドポイント]**領域のフィールドに`S3 URI` 、 `Access Key ID` 、および`Secret Access Key`を入力します。

    ![create changefeed to sink to s3](/media/tidb-cloud/changefeed/sink-to-s3-01-create-changefeed.jpg)

4.  **「次へ」**をクリックして、TiDB 専用クラスターから Amazon S3 への接続を確立します。 TiDB Cloud は、接続が成功したかどうかを自動的にテストして検証します。

    -   「はい」の場合、次の構成ステップに進みます。
    -   そうでない場合は、接続エラーが表示されるため、エラーを処理する必要があります。エラーが解決したら、 **「次へ」**をクリックして接続を再試行します。

5.  **テーブル フィルターを**カスタマイズして、複製するテーブルをフィルターします。ルールの構文については、 [テーブルフィルタールール](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters)を参照してください。

    ![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    -   **フィルター ルール**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルを複製することを表すルール`*.*`があります。新しいルールを追加すると、 TiDB CloudはTiDB 内のすべてのテーブルをクエリし、ルールに一致するテーブルのみを右側のボックスに表示します。
    -   **有効なキーを持つテーブル**: この列には、主キーや一意のインデックスなどの有効なキーを持つテーブルが表示されます。
    -   **有効なキーのないテーブル**: この列には、主キーまたは一意のキーがないテーブルが表示されます。これらのテーブルでは、一意の識別子がないと、ダウンストリームで重複イベントを処理するときにデータの不整合が生じる可能性があるため、レプリケーション中に課題が生じます。データの一貫性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意キーまたは主キーを追加することをお勧めします。あるいは、フィルタ ルールを使用してこれらのテーブルを除外することもできます。たとえば、ルール`"!test.tbl1"`を使用してテーブル`test.tbl1`を除外できます。

6.  **「レプリケーション開始位置」**領域で、次のレプリケーション位置のいずれかを選択します。

    -   これからレプリケーションを開始します
    -   特定の[TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)からレプリケーションを開始します
    -   特定の時刻からレプリケーションを開始する

7.  **[データ形式]**領域で、 **CSV 形式**または**Canal-JSON**形式のいずれかを選択します。

    <SimpleTab>
     <div label="Configure CSV format">

    **CSV**形式を設定するには、次のフィールドに入力します。

    ![the data format of CSV](/media/tidb-cloud/changefeed/sink-to-s3-02-data-format-csv-conf.jpg)

    -   **日付区切り文字**: 年、月、日に基づいてデータをローテーションするか、まったくローテーションしないことを選択します。
    -   **区切り文字**: CSV ファイル内の値を区切るために使用する文字を指定します。カンマ ( `,` ) は最も一般的に使用される区切り文字です。
    -   **引用符**: 区切り文字または特殊文字を含む値を囲むために使用する文字を指定します。通常、二重引用符 ( `"` ) が引用符文字として使用されます。
    -   **Null/空の値**: CSV ファイル内で Null または空の値をどのように表現するかを指定します。これは、データを適切に処理および解釈するために重要です。
    -   **Include Commit Ts** : CSV 行に[`commit-ts`](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#replicate-change-data-to-storage-services)を含めるかどうかを制御します。

    </div>
     <div label="Configure Canal-JSON format">

    Canal-JSON はプレーンな JSON テキスト形式です。設定するには、次のフィールドに入力します。

    ![the data format of Canal-JSON](/media/tidb-cloud/changefeed/sink-to-s3-02-data-format-canal-json.jpg)

    -   **日付区切り文字**: 年、月、日に基づいてデータをローテーションするか、まったくローテーションしないことを選択します。
    -   **TiDB 拡張機能を有効にする**: このオプションを有効にすると、TiCDC は[ウォーターマークイベント](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#watermark-event)を送信し、 [TiDB 拡張フィールド](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field) Canal-JSON メッセージに追加します。

    </div>
     </SimpleTab>

8.  **「次へ」**をクリックして、変更フィード仕様を構成します。

    -   **「変更フィードの仕様」**領域で、変更フィードで使用するレプリケーション キャパシティ ユニット (RCU) の数を指定します。
    -   **「変更フィード名」**領域で、変更フィードの名前を指定します。

9.  **「次へ」**をクリックして、変更フィード構成を確認します。

    -   すべての構成が正しいことを確認したら、 **「作成」を**クリックして変更フィードの作成に進みます。

    -   構成を変更する必要がある場合は、 **「前**へ」をクリックして戻り、必要な変更を加えます。

10. シンクがすぐに起動し、シンクのステータスが**[作成中]**から**[実行中]**に変化するのがわかります。

11. 変更フィードの名前をクリックして、詳細ページに移動します。このページでは、チェックポイントのステータス、レプリケーションのレイテンシー、その他の関連メトリックなど、変更フィードに関する詳細情報を表示できます。
