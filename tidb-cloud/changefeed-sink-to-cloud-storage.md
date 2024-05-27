---
title: Sink to Cloud Storage
Summary: Learn how to create a changefeed to stream data from a TiDB Dedicated cluster to cloud storage, such as Amazon S3 and GCS.
---

# クラウドストレージに保存 {#sink-to-cloud-storage}

このドキュメントでは、TiDB Cloudからクラウドstorageにデータをストリーミングするための変更フィードを作成する方法について説明します。現在、Amazon S3 と GCS がサポートされています。

> **注記：**
>
> -   データをクラウドstorageにストリーミングするには、TiDB クラスターのバージョンが v7.1.1 以降であることを確認してください。TiDB Dedicated クラスターを v7.1.1 以降にアップグレードするには、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)実行します。
> -   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターでは、changefeed 機能は使用できません。

## 制限 {#restrictions}

-   TiDB Cloudクラスターごとに、最大 100 個の変更フィードを作成できます。
-   TiDB Cloud は変更フィードを確立するために TiCDC を使用するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)持ちます。
-   複製するテーブルに主キーまたは NULL 以外の一意のインデックスがない場合、複製中に一意の制約がないと、再試行シナリオによっては下流に重複したデータが挿入される可能性があります。

## ステップ1. 宛先を設定する {#step-1-configure-destination}

ターゲット TiDB クラスターのクラスター概要ページに移動します。左側のナビゲーション ペインで**[Changefeed]**をクリックし、 **[Changefeed の作成] を**クリックして、送信先として**Amazon S3**または**GCS**を選択します。設定プロセスは、選択した送信先によって異なります。

<SimpleTab>
<div label="Amazon S3">

**Amazon S3**の場合、 **S3 エンドポイント**領域に`S3 URI` 、 `Access Key ID` 、 `Secret Access Key`を入力します。S3 バケットを TiDB クラスターと同じリージョンに作成します。

![s3\_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-s3-endpoint.jpg)

</div>
<div label="GCS">

**GCS**の場合、 **GCS エンドポイント**を入力する前に、まず GCS バケットへのアクセスを許可する必要があります。次の手順を実行します。

1.  TiDB Cloudコンソールで、**サービス アカウント ID**を記録します。この ID は、 TiDB Cloudに GCS バケットへのアクセスを許可するために使用されます。

    ![gcs\_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-endpoint.png)

2.  Google Cloud コンソールで、GCS バケットのIAMロールを作成します。

    1.  [Google Cloud コンソール](https://console.cloud.google.com/)にサインインします。

    2.  [役割](https://console.cloud.google.com/iam-admin/roles)ページに移動し、 **[ロールの作成] を**クリックします。

        ![Create a role](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-create-role.png)

    3.  ロールの名前、説明、ID、およびロール起動ステージを入力します。ロールの作成後は、ロール名を変更できません。

    4.  **[権限の追加]**をクリックします。次の読み取り専用権限をロールに追加し、 **[追加]**をクリックします。

        -   storage.buckets.get
        -   storage.オブジェクト.作成
        -   storage.オブジェクト.削除
        -   storage.objects.get
        -   storage.objects.list
        -   storage.objects.update

    ![Add permissions](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-assign-permission.png)

3.  [バケツ](https://console.cloud.google.com/storage/browser)ページに移動し、 TiDB Cloudがアクセスする GCS バケットを選択します。GCS バケットは TiDB クラスターと同じリージョンにある必要があることに注意してください。

4.  **バケットの詳細**ページで、 **「権限」**タブをクリックし、 **「アクセス権の付与」**をクリックします。

    ![Grant Access to the bucket ](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-grant-access-1.png)

5.  バケットへのアクセスを許可するには次の情報を入力し、 **「保存」**をクリックします。

    -   **[新しいプリンシパル]**フィールドに、前に記録したターゲット TiDB クラスターの**サービス アカウント ID**を貼り付けます。

    -   **[ロールの選択]**ドロップダウン リストに、作成したIAMロールの名前を入力し、フィルター結果から名前を選択します。

    > **注記：**
    >
    > TiDB Cloudへのアクセスを削除するには、許可したアクセスを削除するだけです。

6.  **バケットの詳細**ページで、 **「オブジェクト」**タブをクリックします。

    -   バケットの gsutil URI を取得するには、コピー ボタンをクリックし、プレフィックスとして`gs://`追加します。たとえば、バケット名が`test-sink-gcs`の場合、URI は`gs://test-sink-gcs/`になります。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri01.png)

    -   フォルダの gsutil URI を取得するには、フォルダを開き、コピー ボタンをクリックし、プレフィックスとして`gs://`追加します。たとえば、バケット名が`test-sink-gcs`でフォルダ名が`changefeed-xxx`場合、URI は`gs://test-sink-gcs/changefeed-xxx/`になります。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri02.png)

7.  TiDB Cloudコンソールで、Changefeed の**[宛先の構成]**ページに移動し、**バケットの gsutil URI**フィールドに入力します。

</div>
</SimpleTab>

**「次へ」**をクリックして、TiDB 専用クラスターから Amazon S3 または GCS への接続を確立します。TiDB TiDB Cloud は、接続が成功したかどうかを自動的にテストして検証します。

-   はいの場合は、構成の次の手順に進みます。
-   そうでない場合は、接続エラーが表示されるので、エラーを処理する必要があります。エラーが解決したら、 **[次へ]**をクリックして接続を再試行してください。

## ステップ2. レプリケーションを構成する {#step-2-configure-replication}

1.  **テーブル フィルターを**カスタマイズして、複製するテーブルをフィルターします。ルール構文については、 [テーブルフィルタルール](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters)を参照してください。

    ![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    -   **フィルター ルール**: この列でフィルター ルールを設定できます。デフォルトでは、すべてのテーブルを複製するルール`*.*`があります。新しいルールを追加すると、 TiDB Cloud はTiDB 内のすべてのテーブルを照会し、右側のボックスにルールに一致するテーブルのみを表示します。最大 100 個のフィルター ルールを追加できます。
    -   **有効なキーを持つテーブル**: この列には、主キーや一意のインデックスなど、有効なキーを持つテーブルが表示されます。
    -   **有効なキーのないテーブル**: この列には、主キーまたは一意のキーがないテーブルが表示されます。これらのテーブルは、一意の識別子がないと、下流で重複イベントを処理するときにデータの不整合が発生する可能性があるため、レプリケーション中に問題が発生します。データの一貫性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意のキーまたは主キーを追加することをお勧めします。または、フィルター ルールを使用してこれらのテーブルを除外することもできます。たとえば、ルール`"!test.tbl1"`を使用してテーブル`test.tbl1`を除外できます。

2.  **イベント フィルターを**カスタマイズして、複製するイベントをフィルターします。

    -   **一致するテーブル**: この列で、イベント フィルターを適用するテーブルを設定できます。ルールの構文は、前の**テーブル フィルター**領域で使用した構文と同じです。変更フィードごとに最大 10 個のイベント フィルター ルールを追加できます。
    -   **無視されるイベント**: イベント フィルターが変更フィードから除外するイベントの種類を設定できます。

3.  **[レプリケーションの開始位置]**領域で、次のいずれかのレプリケーション位置を選択します。

    -   今からレプリケーションを開始します
    -   特定の[TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)からレプリケーションを開始する
    -   特定の時間からレプリケーションを開始する

4.  **データ形式**領域で、 **CSV**または**Canal-JSON**形式のいずれかを選択します。

    <SimpleTab>
     <div label="Configure CSV format">

    **CSV**形式を設定するには、次のフィールドに入力します。

    -   **バイナリエンコード方式**: バイナリデータのエンコード方式。base64 (デフォルト) または**hex****を**選択できます。AWS DMS と統合する場合は**hex**を使用します。
    -   **日付区切り**: 年、月、日に基づいてデータを回転するか、まったく回転しないことを選択します。
    -   **区切り文字**: CSV ファイル内の値を区切る文字を指定します。最もよく使用される区切り文字はコンマ ( `,` ) です。
    -   **引用符**: 区切り文字または特殊文字を含む値を囲むために使用する文字を指定します。通常、引用符文字として二重引用符 ( `"` ) が使用されます。
    -   **Null/空の値**: CSV ファイルで Null または空の値をどのように表現するかを指定します。これは、データを適切に処理および解釈するために重要です。
    -   **コミット Ts を含める**: CSV 行に[`commit-ts`](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#replicate-change-data-to-storage-services)を含めるかどうかを制御します。

    </div>
     <div label="Configure Canal-JSON format">

    Canal-JSON はプレーンな JSON テキスト形式です。設定するには、次のフィールドに入力します。

    -   **日付区切り**: 年、月、日に基づいてデータを回転するか、まったく回転しないことを選択します。
    -   **TiDB 拡張を有効にする**: このオプションを有効にすると、TiCDC は[ウォーターマークイベント](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#watermark-event)送信し、 [TiDB拡張フィールド](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field) Canal-JSON メッセージに追加します。

    </div>
     </SimpleTab>

5.  **フラッシュ パラメータ**領域では、次の 2 つの項目を設定できます。

    -   **フラッシュ間隔**: デフォルトでは 60 秒に設定されていますが、2 秒から 10 分の範囲で調整可能です。
    -   **ファイル サイズ**: デフォルトでは 64 MB に設定されていますが、1 MB ～ 512 MB の範囲で調整可能です。

    ![Flush Parameters](/media/tidb-cloud/changefeed/sink-to-cloud-storage-flush-parameters.jpg)

    > **注記：**
    >
    > これら 2 つのパラメータは、個々のデータベース テーブルごとにクラウドstorageに生成されるオブジェクトの量に影響します。テーブルが多数ある場合、同じ構成を使用すると生成されるオブジェクトの数が増え、クラウドstorageAPI の呼び出しコストが増加します。したがって、復旧ポイント目標 (RPO) とコスト要件に基づいてこれらのパラメータを適切に構成することをお勧めします。

## ステップ3.仕様を構成する {#step-3-configure-specification}

**次へ**をクリックして、変更フィード仕様を構成します。

1.  **「Changefeed 仕様」**領域で、変更フィードで使用されるレプリケーション容量単位 (RCU) の数を指定します。
2.  **「Changefeed 名」**領域で、Changefeed の名前を指定します。

## ステップ4. 構成を確認してレプリケーションを開始する {#step-4-review-the-configuration-and-start-replication}

**「次へ」**をクリックして、変更フィード構成を確認します。

-   すべての構成が正しいことを確認したら、 **「作成」を**クリックして変更フィードの作成を続行します。
-   設定を変更する必要がある場合は、 **「前へ」**をクリックして戻って必要な変更を加えます。

シンクはすぐに起動し、シンクのステータスが**「作成中**」から**「実行中**」に変わります。

変更フィードの名前をクリックすると、その詳細ページに移動します。このページでは、チェックポイントのステータス、レプリケーションのレイテンシー、その他の関連メトリックなど、変更フィードに関する詳細情報を表示できます。
