---
title: Sink to Cloud Storage
Summary: Learn how to create a changefeed to stream data from a TiDB Dedicated cluster to cloud storage, such as Amazon S3 and GCS.
---

# クラウドストレージにシンクする {#sink-to-cloud-storage}

このドキュメントでは、 TiDB Cloudからクラウドstorageにデータをストリーミングするためのチェンジフィードを作成する方法について説明します。現在、Amazon S3 と GCS がサポートされています。

> **注記：**
>
> -   データをクラウドstorageにストリーミングするには、TiDB クラスターのバージョンが v7.1.1 以降であることを確認してください。 TiDB 専用クラスターを v7.1.1 以降にアップグレードするには、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md) .
> -   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの場合、チェンジフィード機能は使用できません。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 100 個の変更フィードを作成できます。
-   TiDB Cloud はTiCDC を使用して変更フィードを確立するため、同じ[TiCDC としての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)を持ちます。
-   レプリケートされるテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、レプリケーション中に一意制約がないため、一部の再試行シナリオでは重複したデータがダウンストリームに挿入される可能性があります。

## ステップ 1. 宛先の設定 {#step-1-configure-destination}

ターゲット TiDB クラスターのクラスター概要ページに移動します。左側のナビゲーションペインで**[Changefeed]**をクリックし、 **[Create Changefeed]**をクリックして、宛先として**Amazon S3**または**GCS**を選択します。設定プロセスは、選択した宛先によって異なります。

<SimpleTab>
<div label="Amazon S3">

**Amazon S3**の場合、 **S3 エンドポイント**領域に`S3 URI` 、 `Access Key ID` 、および`Secret Access Key`を入力します。 TiDB クラスターと同じリージョンに S3 バケットを作成します。

![s3\_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-s3-endpoint.jpg)

</div>
<div label="GCS">

**GCS**の場合、 **GCS Endpoint**を入力する前に、まず GCS バケットへのアクセスを許可する必要があります。次の手順を実行します。

1.  TiDB Cloudコンソールで、 TiDB Cloudに GCS バケットへのアクセスを許可するために使用される**サービス アカウント ID**を記録します。

    ![gcs\_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-endpoint.png)

2.  Google Cloud コンソールで、GCS バケットのIAMロールを作成します。

    1.  [Google Cloud コンソール](https://console.cloud.google.com/)にサインインします。

    2.  [役割](https://console.cloud.google.com/iam-admin/roles)ページに移動し、 **[ロールの作成]**をクリックします。

        ![Create a role](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-create-role.png)

    3.  ロールの名前、説明、ID、およびロール起動ステージを入力します。ロールの作成後にロール名を変更することはできません。

    4.  **[アクセス許可の追加]**をクリックします。次の読み取り専用権限をロールに追加し、 **[追加]**をクリックします。

        -   storage.buckets.get
        -   storage.objects.create
        -   storage.オブジェクト.削除
        -   storage.objects.get
        -   storage.objects.list
        -   storage.objects.update

    ![Add permissions](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-assign-permission.png)

3.  [バケツ](https://console.cloud.google.com/storage/browser)ページに移動し、 TiDB Cloudがアクセスする GCS バケットを選択します。 GCS バケットは TiDB クラスターと同じリージョンに存在する必要があることに注意してください。

4.  **[バケットの詳細]**ページで、 **[アクセス許可]**タブをクリックし、 **[アクセスの許可]**をクリックします。

    ![Grant Access to the bucket ](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-grant-access-1.png)

5.  次の情報を入力してバケットへのアクセスを許可し、 **[保存]**をクリックします。

    -   **[新しいプリンシパル]**フィールドに、前に記録したターゲット TiDB クラスターの**サービス アカウント ID を**貼り付けます。

    -   **[ロールの選択]**ドロップダウン リストに、作成したIAMロールの名前を入力し、フィルター結果から名前を選択します。

    > **注記：**
    >
    > TiDB Cloudへのアクセスを削除するには、付与したアクセスを削除するだけです。

6.  **「バケットの詳細」**ページで、 **「オブジェクト」**タブをクリックします。

    -   バケットの gsutil URI を取得するには、コピー ボタンをクリックし、プレフィックスとして`gs://`を追加します。たとえば、バケット名が`test-sink-gcs`の場合、URI は`gs://test-sink-gcs/`になります。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri01.png)

    -   フォルダーの gsutil URI を取得するには、フォルダーを開いてコピー ボタンをクリックし、プレフィックスとして`gs://`を追加します。たとえば、バケット名が`test-sink-gcs` 、フォルダー名が`changefeed-xxx`の場合、URI は`gs://test-sink-gcs/changefeed-xxx/`になります。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri02.png)

7.  TiDB Cloudコンソールで、Changefeed の**「宛先の構成」**ページに移動し、**バケットの gsutil URI**フィールドに入力します。

</div>
</SimpleTab>

**[次へ]**をクリックして、TiDB 専用クラスターから Amazon S3 または GCS への接続を確立します。 TiDB Cloud は、接続が成功したかどうかを自動的にテストして検証します。

-   「はい」の場合、次の構成ステップに進みます。
-   そうでない場合は、接続エラーが表示されるため、エラーを処理する必要があります。エラーが解決したら、 **「次へ」**をクリックして接続を再試行します。

## ステップ 2. レプリケーションを構成する {#step-2-configure-replication}

1.  **テーブル フィルターを**カスタマイズして、複製するテーブルをフィルターします。ルールの構文については、 [テーブルフィルタールール](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters)を参照してください。

    ![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    -   **フィルター ルール**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルを複製することを表すルール`*.*`があります。新しいルールを追加すると、 TiDB CloudはTiDB 内のすべてのテーブルをクエリし、ルールに一致するテーブルのみを右側のボックスに表示します。最大 100 個のフィルター ルールを追加できます。
    -   **有効なキーを持つテーブル**: この列には、主キーや一意のインデックスなどの有効なキーを持つテーブルが表示されます。
    -   **有効なキーのないテーブル**: この列には、主キーまたは一意のキーがないテーブルが表示されます。これらのテーブルでは、一意の識別子がないと、ダウンストリームで重複イベントを処理するときにデータの不整合が生じる可能性があるため、レプリケーション中に課題が生じます。データの一貫性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意キーまたは主キーを追加することをお勧めします。あるいは、フィルタ ルールを使用してこれらのテーブルを除外することもできます。たとえば、ルール`"!test.tbl1"`を使用してテーブル`test.tbl1`を除外できます。

2.  **イベント フィルターを**カスタマイズして、複製するイベントをフィルターします。

    -   **一致するテーブル**: この列でイベント フィルターを適用するテーブルを設定できます。ルールの構文は、前述の**テーブル フィルター**領域で使用されるものと同じです。変更フィードごとに最大 10 個のイベント フィルター ルールを追加できます。
    -   **無視されるイベント**: イベント フィルターが変更フィードから除外するイベントのタイプを設定できます。

3.  **「レプリケーション開始位置」**領域で、次のレプリケーション位置のいずれかを選択します。

    -   これからレプリケーションを開始します
    -   特定の[TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)からレプリケーションを開始します
    -   特定の時刻からレプリケーションを開始する

4.  **[データ形式]**領域で、 **CSV 形式**または**Canal-JSON**形式のいずれかを選択します。

    <SimpleTab>
     <div label="Configure CSV format">

    **CSV**形式を設定するには、次のフィールドに入力します。

    -   **バイナリエンコード方式**: バイナリデータのエンコード方式です。 **Base64** (デフォルト) または**hex**を選択できます。 AWS DMS と統合する場合は、 **hex**を使用します。
    -   **日付区切り文字**: 年、月、日に基づいてデータをローテーションするか、まったくローテーションしないことを選択します。
    -   **区切り文字**: CSV ファイル内の値を区切るために使用する文字を指定します。カンマ ( `,` ) は最も一般的に使用される区切り文字です。
    -   **引用符**: 区切り文字または特殊文字を含む値を囲むために使用する文字を指定します。通常、二重引用符 ( `"` ) が引用符文字として使用されます。
    -   **Null/空の値**: CSV ファイル内で Null または空の値をどのように表現するかを指定します。これは、データを適切に処理および解釈するために重要です。
    -   **Include Commit Ts** : CSV 行に[`commit-ts`](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#replicate-change-data-to-storage-services)を含めるかどうかを制御します。

    </div>
     <div label="Configure Canal-JSON format">

    Canal-JSON はプレーンな JSON テキスト形式です。設定するには、次のフィールドに入力します。

    -   **日付区切り文字**: 年、月、日に基づいてデータをローテーションするか、まったくローテーションしないことを選択します。
    -   **TiDB 拡張機能を有効にする**: このオプションを有効にすると、TiCDC は[ウォーターマークイベント](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#watermark-event)を送信し、 [TiDB 拡張フィールド](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field) Canal-JSON メッセージに追加します。

    </div>
     </SimpleTab>

5.  **「フラッシュパラメータ」**領域では、次の 2 つの項目を設定できます。

    -   **フラッシュ間隔**: デフォルトでは 60 秒に設定されていますが、2 秒から 10 分の範囲で調整可能です。
    -   **ファイル サイズ**: デフォルトでは 64 MB に設定されていますが、1 MB ～ 512 MB の範囲で調整できます。

    ![Flush Parameters](/media/tidb-cloud/changefeed/sink-to-cloud-storage-flush-parameters.jpg)

    > **注記：**
    >
    > これら 2 つのパラメーターは、クラウドstorage内で個々のデータベース テーブルごとに生成されるオブジェクトの量に影響します。テーブルの数が多い場合、同じ構成を使用すると、生成されるオブジェクトの数が増加し、クラウドstorageAPI を呼び出すコストが増加します。したがって、目標復旧時点 (RPO) とコスト要件に基づいて、これらのパラメーターを適切に構成することをお勧めします。

## ステップ 3. 仕様の構成 {#step-3-configure-specification}

**「次へ」**をクリックして、変更フィード仕様を構成します。

1.  **「変更フィードの仕様」**領域で、変更フィードで使用するレプリケーション キャパシティ ユニット (RCU) の数を指定します。
2.  **「変更フィード名」**領域で、変更フィードの名前を指定します。

## ステップ 4. 構成を確認してレプリケーションを開始する {#step-4-review-the-configuration-and-start-replication}

**「次へ」**をクリックして、変更フィード構成を確認します。

-   すべての構成が正しいことを確認したら、 **「作成」を**クリックして変更フィードの作成に進みます。
-   構成を変更する必要がある場合は、 **「前**へ」をクリックして戻り、必要な変更を加えます。

シンクがすぐに起動し、シンクのステータスが**[作成中]**から**[実行中]**に変化するのがわかります。

変更フィードの名前をクリックして、詳細ページに移動します。このページでは、チェックポイントのステータス、レプリケーションのレイテンシー、その他の関連メトリックなど、変更フィードに関する詳細情報を表示できます。
