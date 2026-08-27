---
title: Sink to Cloud Storage
summary: このドキュメントでは、TiDB Cloudからクラウドストレージへデータをストリーミングするための変更フィードの作成方法について説明します。制限事項、宛先、レプリケーション、仕様に関する設定手順、およびレプリケーションプロセスの開始方法についても説明します。
---

# クラウドストレージへのシンク {#sink-to-cloud-storage}

このドキュメントでは、<CustomContent plan="dedicated">TiDB Cloud Dedicated</CustomContent><CustomContent plan="premium">TiDB Cloud Premium</CustomContent> からクラウドストレージにデータをストリーミングするためのチェンジフィードを作成する方法について説明します。

<CustomContent plan="dedicated">

> **Note:**
>
> - {{{ .dedicated }}} からクラウドストレージにデータをストリーミングするには、TiDB クラスターのバージョンが v7.1.1 以降であることを確認してください。TiDB Cloud Dedicated クラスターを v7.1.1 以降にアップグレードするには、[TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)。
> - [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) インスタンスでは、changefeed 機能は利用できません。
> - [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) インスタンスでは、changefeed 機能はリクエスト時のみ利用できます。詳細については、[Changefeed](/tidb-cloud/essential-changefeed-overview.md) を参照してください。
> - [{{{ .premium }}}](/tidb-cloud/select-cluster-tier.md#premium) インスタンスについては、[Sink to Cloud Storage](https://docs.pingcap.com/tidbcloud/changefeed-sink-to-cloud-storage/?plan=premium) を参照してください。

</CustomContent>

<CustomContent plan="premium">

> **Note:**
>
> - [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) インスタンスでは、changefeed 機能は利用できません。
> - [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) インスタンスでは、changefeed 機能はリクエストに応じてのみ利用できます。詳細については、[Changefeed](/tidb-cloud/essential-changefeed-overview.md) を参照してください。
> - [{{{ .dedicated }}}](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) クラスターについては、[Sink to Cloud Storage](https://docs.pingcap.com/tidbcloud/changefeed-sink-to-cloud-storage/) を参照してください。

</CustomContent>

## 制限 {#restrictions}

- 各<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>では、最大 100 個のチェンジフィードを作成できます。
- TiDB Cloud は TiCDC を使用してチェンジフィードを確立するため、[TiCDC と同じ制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)があります。
- 複製対象のテーブルに主キーまたは NULL を許容しない一意インデックスがない場合、複製中に一意制約が存在しないことで、一部の再試行シナリオにおいて、下流で重複データが挿入される可能性があります。

## ステップ1. 宛先を設定する {#step-1-configure-destination}

<CustomContent plan="dedicated">

対象のTiDB Cloud Dedicatedクラスターの概要ページに移動します。左側のナビゲーションペインで**Data** > **Changefeed**をクリックし、**Create Changefeed**をクリックして**Destination**ページに移動します。次に、TiDB Cloud Dedicatedクラスターがホストされているクラウドプロバイダーに応じて、宛先として**Amazon S3**、**GCS**、または**Azure Blob Storage**を選択します。設定プロセスは、選択した宛先によって異なります。

</CustomContent>

<CustomContent plan="premium">

対象のTiDB Cloud Premiumインスタンスの概要ページに移動します。左側のナビゲーションペインで**Data** > **Changefeed**をクリックし、**Create Changefeed**をクリックして**Destination**ページに移動します。次に、TiDB Cloud Premiumインスタンスがホストされているクラウドプロバイダーに応じて、宛先として**Amazon S3**または**Alibaba Cloud OSS**を選択します。設定プロセスは、選択した宛先によって異なります。

</CustomContent>

<SimpleTab>
<div label="Amazon S3">

**Amazon S3**の認証には、**AWS Role ARN**または**AWS access key**のいずれかを使用できます。セキュリティの強化と管理の容易さのため、**AWS Role ARN**の使用をお勧めします。

**オプション1: AWS Role ARN（推奨）**

認証にIAMロールを使用するには、以下の手順に従ってください。

1. Amazon S3 の**Destination**ページで、**S3 URI**を入力します。S3 バケットが <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent> と同じ AWS リージョンにあることを確認してください。
2. **Bucket Access**で、**AWS Role ARN**を選択します。
3. 新しい Role ARN を作成するには、**Click here to create new one with AWS CloudFormation**をクリックします。このテンプレートは必要な権限を自動的に設定します。

    手動でロールを作成する場合は、**Create Role ARN manually**をクリックして、TiDB Cloudアカウント情報と必要なポリシーを確認してください。

4. IAMロールに、対象バケットに対して少なくとも以下の権限があることを確認してください。

    - `s3:ListBucket`
    - `s3:PutObject`
    - `s3:GetObject`
    - `s3:DeleteObject`

5. 生成された**Role ARN**を対応するフィールドに貼り付けます。

**オプション2: AWS access key**

> **Note:**
>
> access key と secret key（AK/SK）を使用する場合、認証情報の管理とローテーションを手動で行う必要があり、セキュリティリスクが高まります。より強力なセキュリティを確保するには、代わりに**AWS Role ARN**を使用することをお勧めします。

access key を使用して認証するには、以下の手順に従ってください。

1. Amazon S3 の**Destination**ページで、**S3 URI**を入力します。S3 バケットが <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent> と同じ AWS リージョンにあることを確認してください。
2. **Bucket Access**で、**AWS Access Key**を選択します。
3. 以下のフィールドに入力します。

    - **Access Key ID**
    - **Secret Access Key**

</div>

<CustomContent plan="dedicated">

<div label="GCS">

**GCS**の場合、**GCS Endpoint**を入力する前に、まず GCS バケットへのアクセス権を付与する必要があります。以下の手順に従ってください。

1. TiDB Cloudコンソールで、**Service Account ID**を記録します。これは、TiDB Cloudに GCS バケットへのアクセス権を付与するために使用されます。

    ![gcs_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-endpoint.png)

2. Google Cloud コンソールで、GCS バケット用の IAM ロールを作成します。

    1. [Google Cloud console](https://console.cloud.google.com/)にサインインします。
    2. [Roles](https://console.cloud.google.com/iam-admin/roles)ページに移動し、**Create role**をクリックします。

        ![Create a role](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-create-role.png)

    3. ロールの名前、説明、ID、およびロールの起動ステージを入力します。ロール名は、ロール作成後に変更できません。
    4. **Add permissions**をクリックします。ロールに以下の権限を追加し、**Add**をクリックします。

        - storage.buckets.get
        - storage.objects.create
        - storage.objects.delete
        - storage.objects.get
        - storage.objects.list
        - storage.objects.update

    ![Add permissions](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-assign-permission.png)

3. [Bucket](https://console.cloud.google.com/storage/browser)ページに移動し、TiDB Cloud にアクセスさせる GCS バケットを選択します。GCS バケットは、TiDB クラスターと同じリージョンにある必要があります。

4. **Bucket details**ページで、**Permissions**タブをクリックし、**Grant access**をクリックします。

    ![Grant Access to the bucket ](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-grant-access-1.png)

5. バケットへのアクセス権を付与するため、以下の情報を入力し、**Save**をクリックします。

    - **New Principals**フィールドに、先ほど記録した対象 TiDB クラスターの**Service Account ID**を貼り付けます。
    - **Select a role**ドロップダウンリストに、先ほど作成した IAM ロールの名前を入力し、フィルター結果からその名前を選択します。

    > **Note:**
    >
    > TiDB Cloudへのアクセス権を削除するには、付与したアクセス権を削除するだけです。

6. **Bucket details**ページで、**Objects**タブをクリックします。

    - バケットの gsutil URI を取得するには、コピー ボタンをクリックし、プレフィックスとして`gs://`を追加します。たとえば、バケット名が`test-sink-gcs`の場合、URI は`gs://test-sink-gcs/`になります。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri01.png)

    - フォルダの gsutil URI を取得するには、フォルダを開き、コピー ボタンをクリックし、プレフィックスとして`gs://`を追加します。たとえば、バケット名が`test-sink-gcs`で、フォルダ名が`changefeed-xxx`の場合、URI は`gs://test-sink-gcs/changefeed-xxx/`になります。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri02.png)

7. TiDB Cloudコンソールで、Changefeed の**Destination**ページに移動し、**bucket gsutil URI**フィールドに入力します。

</div>

</CustomContent>

<CustomContent plan="dedicated">

<div label="Azure Blob Storage">

**Azure Blob Storage**の場合、まず Azure portal でコンテナーを設定し、SAS トークンを取得する必要があります。以下の手順に従ってください。

1. [Azure portal](https://portal.azure.com/)で、changefeed データを保存するコンテナーを作成します。

    1. 左側のナビゲーションペインで**Storage Accounts**をクリックし、ストレージアカウントを選択します。
    2. ストレージアカウントのナビゲーションメニューで、**Data storage** > **Containers**を選択し、**+ Container**をクリックします。
    3. 新しいコンテナーの名前を入力し、匿名アクセスレベルを設定します（推奨レベルは**Private**です）。その後、**Create**をクリックします。

2. 対象コンテナーの URL を取得します。

    1. コンテナー一覧で、対象のコンテナーを選択します。
    2. コンテナーの**...**をクリックし、**Container properties**を選択します。
    3. **URL**の値を後で使用するために保存します。たとえば `https://<storage_account>.blob.core.windows.net/<container>` です。

3. SAS トークンを生成します。

    1. ストレージアカウントのナビゲーションメニューで、**Security + networking** > **Shared access signature**を選択します。
    2. **Allowed services**セクションで、**Blob**を選択します。
    3. **Allowed resource types**セクションで、**Container**と**Object**を選択します。
    4. **Allowed permissions**セクションで、**Read**、**Write**、**Delete**、**List**、**Create**を選択します。
    5. SAS トークンの有効期間を、要件を満たすのに十分な長さで指定します。

        > **Note:**
        >
        > - changefeed は継続的にイベントを書き込むため、SAS トークンの有効期間が十分に長いことを確認してください。セキュリティのため、トークンは6〜12か月ごとに置き換えることをお勧めします。
        > - 生成された SAS トークンは取り消せないため、有効期間は慎重に設定してください。
        > - 継続的な可用性を確保するため、SAS トークンの有効期限が切れる前に再生成して更新してください。

    6. **Generate SAS and connection string**をクリックし、**SAS token**を保存します。

        ![Generate a SAS token](/media/tidb-cloud/changefeed/sink-to-cloud-storage-azure-signature.png)

4. [TiDB Cloud console](https://tidbcloud.com/)で、Changefeed の**Destination**ページに移動し、以下のフィールドに入力します。

    - **Blob URL**: 手順 2 で取得したコンテナー URL を入力します。必要に応じてプレフィックスを追加できます。
    - **SAS Token**: 手順 3 で取得した生成済みの SAS トークンを入力します。

</div>

</CustomContent>

<CustomContent plan="premium">

<div label="Alibaba Cloud OSS">

**Alibaba Cloud OSS**の場合、以下の手順に従って changefeed を設定します。

1. [Alibaba Cloud console](https://www.alibabacloud.com/)で、以下の事前準備を行います。

    1. TiDB Cloud Premiumインスタンスと同じリージョンに OSS バケットを作成します。詳細な手順については、[Create a bucket](https://www.alibabacloud.com/help/en/oss/user-guide/create-a-bucket-4)を参照してください。
    2. changefeed 用の RAM ユーザーを作成し、AccessKey ペアを生成します。詳細な手順については、[Create an AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)を参照してください。
    3. カスタム RAM ポリシーを作成して RAM ユーザーにアタッチし、changefeed に必要な最小限の権限のみを付与します。詳細については、[Control access to OSS resources with RAM policies](https://www.alibabacloud.com/help/en/oss/user-guide/ram-policy)を参照してください。

        - `oss:ListObjects`
        - `oss:GetObject`
        - `oss:PutObject`
        - `oss:DeleteObject`

    以下の JSON 例は、必要な権限を持つポリシーを示しています。`<Your bucket name>`を OSS バケット名に置き換えてください。

    ```json
    {
      "Version": "1",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "oss:ListObjects",
            "oss:GetObject",
            "oss:PutObject",
            "oss:DeleteObject"
          ],
          "Resource": [
            "acs:oss:*:*:<Your bucket name>",
            "acs:oss:*:*:<Your bucket name>/*"
          ]
        }
      ]
    }
    ```

2. Alibaba Cloud OSS の**Destination**ページで、以下のフィールドに入力します。

    - **Bucket URI**: `oss://<Your bucket name>/<prefix>/` 形式で OSS URI を入力します。
    - **Access Key ID**: RAM ユーザーの AccessKey ID を入力します。
    - **Access Key Secret**: RAM ユーザーの AccessKey Secret を入力します。

</div>

</CustomContent>

</SimpleTab>

**Next**をクリックして、<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent> からクラウドストレージへの接続を確立します。TiDB Cloudは、接続が成功したかどうかを自動的にテストして検証します。

- 成功した場合は、次の設定ステップに進みます。
- 失敗した場合は、接続エラーが表示されるため、エラーに対処する必要があります。エラーを解消したら、**Next**をクリックして接続を再試行してください。

## ステップ2. レプリケーションの設定 {#step-2-configure-replication}

1. **Table Filter**カスタマイズして、複製するテーブルをフィルターします。ルールの構文については、 [テーブルフィルタルール](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters)を参照してください。

    ![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    - **Case Sensitive**：フィルタルールにおけるデータベース名とテーブル名の照合において、大文字小文字を区別するかどうかを設定できます。デフォルトでは、大文字小文字は区別されません。
    - **Filter Rules**：この列でフィルタルールを設定できます。デフォルトでは、すべてのテーブルを複製するルール`*.*`が設定されています。新しいルールを追加すると、 TiDB Cloud はTiDB 内のすべてのテーブルをクエリし、右側のボックスにルールに一致するテーブルのみを表示します。フィルタルールは最大 100 個まで追加できます。
    - **Tables with valid keys**：この列には、主キーや一意インデックスなど、有効なキーを持つテーブルが表示されます。
    - **Tables without valid keys**: この列には、主キーまたは一意キーがないテーブルが表示されます。一意の識別子がないと、下流で重複イベントを処理する際にデータの一貫性が失われる可能性があるため、これらのテーブルはレプリケーション中に問題となります。データの一貫性を確保するには、レプリケーションを開始する前に、これらのテーブルに一意キーまたは主キーを追加することをお勧めします。または、フィルタルールを使用してこれらのテーブルを除外することもできます。たとえば、ルール`test.tbl1`を使用して、テーブル`"!test.tbl1"` 。

2. **Event Filter**をカスタマイズして、複製したいイベントを絞り込みます。

    - **Tables matching**：この列では、イベントフィルターを適用するテーブルを設定できます。ルールの構文は、前の**Table Filter**領域で使用されているものと同じです。変更フィードごとに最大10個のイベントフィルタールールを追加できます。
    - **Event Filter**：以下のイベントフィルターを使用して、変更フィードから特定のイベントを除外できます。
        - **Ignore event**：指定されたイベントタイプを除外します。
        - **Ignore SQL**: 指定された式に一致する DDL イベントを除外します。たとえば、 `^drop` `DROP`で始まるステートメントを除外し、 `add column`は`ADD COLUMN`を含むステートメントを除外します。
        - **Ignore insert value expression**: 特定の条件を満たす`INSERT`ステートメントを除外します。たとえば、 `id >= 100`は、 `INSERT`が 100 以上である`id`ステートメントを除外します。
        - **新しい値の更新式を無視する**: 新しい値が指定された条件に一致する`UPDATE`ステートメントを除外します。たとえば、 `gender = 'male'`は`gender`が`male`になるような更新を除外します。
        - **古い値の更新を無視する式**: 古い値が指定された条件に一致する`UPDATE`ステートメントを除外します。たとえば、 `age < 18` `age`の古い値が 18 未満である場合の更新を除外します。
        - **Ignore delete value expression**: 指定された条件を満たす`DELETE`ステートメントを除外します。たとえば、 `name = 'john'`は`DELETE`が`name`である`'john'`ステートメントを除外します。

3. **Start Replication Position**領域で、以下のいずれかのレプリケーション位置を選択します。

    - 今からレプリケーションを開始します
    - 特定の[TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)からレプリケーションを開始する
    - 特定の時間からレプリケーションを開始する

4. **Data Format**領域で、 **CSV形式**または**Canal-JSON**形式のいずれかを選択してください。

     <SimpleTab>
     <div label="Configure CSV format">

    **CSV**形式を設定するには、以下の項目を入力してください。

    - **Binary Encode Method**：バイナリデータのエンコード方式。base64（デフォルト）または**hex**を選択できます。AWS DMSと連携する場合は、 **hex**を使用してください。
    - **Date Separator**：年、月、日に基づいてデータをローテーションするか、ローテーションしないかを選択します。
    - **区切り文字**：CSVファイル内の値を区切る文字を指定します。最も一般的に使用される区切り文字はカンマ（ `,` ）です。
    - **引用符**：区切り文字または特殊文字を含む値を囲むために使用する文字を指定します。通常、引用符には二重引用符（ `"` ）が使用されます。
    - **Null/Empty Values**：CSVファイル内でnull値または空値がどのように表現されるかを指定します。これは、データの適切な処理と解釈のために重要です。
    - **Include Commit Ts**：CSV行に[`commit-ts`](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#replicate-change-data-to-storage-services)を含めるかどうかを制御します。

    </div>
     <div label="Configure Canal-JSON format">

    Canal-JSONは、プレーンなJSONテキスト形式です。設定するには、以下のフィールドに入力してください。

    - **Date Separator**：年、月、日に基づいてデータをローテーションするか、ローテーションしないかを選択します。
    - **Enable TiDB Extension**: このオプションを有効にすると、TiCDC は[ウォーターマークイベント](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#watermark-event)を送信し、 [TiDB拡張フィールド](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)Canal-JSON メッセージに追加します。

    </div>
     </SimpleTab>

5. **Flush Parameters**領域では、次の2つの項目を設定できます。

    - **Flush Interval**：デフォルトでは60秒に設定されていますが、2秒から10分の範囲で調整可能です。
    - **File Size**：デフォルトでは64MBに設定されていますが、1MBから512MBの範囲で調整可能です。

    ![Flush Parameters](/media/tidb-cloud/changefeed/sink-to-cloud-storage-flush-parameters.jpg)

    > **Note:**
    >
    > これら2つのパラメータは、各データベーステーブルごとにクラウドストレージに生成されるオブジェクトの数に影響します。テーブル数が多い場合、同じ設定を使用すると生成されるオブジェクトの数が増加し、結果としてクラウドストレージAPIの呼び出しコストが上昇します。そのため、リカバリポイント目標（RPO）とコスト要件に基づいて、これらのパラメータを適切に設定することをお勧めします。

6. **Split Event**エリアで、 `UPDATE`イベントを別々の`DELETE`と`INSERT`イベントに分割するか、生の`UPDATE`イベントとして保持するかを選択します。詳細については、 [MySQL以外のシンクにおける、主キーまたは一意キーを分割したUPDATEイベント](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)を参照してください。

## ステップ3．仕様の設定 {#step-3-configure-specification}

**Next**をクリックして、変更フィードの仕様を設定してください。

1. **Changefeed Specification**領域で、変更フィードで使用するレプリケーション容量ユニット（RCU）の数を指定します。
2. **Changefeed Name**欄に、変更フィードの名前を指定します。

## ステップ4．構成を確認し、レプリケーションを開始する {#step-4-review-the-configuration-and-start-replication}

**Next**をクリックして、変更フィードの設定を確認してください。

- すべての設定が正しいことを確認したら、 **Create**をクリックして変更フィードの作成に進んでください。
- 設定を変更する必要がある場合は、 **Previous**をクリックして戻り、必要な変更を行ってください。

シンクはまもなく起動し、シンクの状態が**Creating**から**Running**に変わるのが確認できます。

変更フィードの名前をクリックすると、その詳細ページに移動します。このページでは、チェックポイントの状態、レプリケーションのレイテンシー、その他の関連メトリックなど、変更フィードに関する詳細情報を確認できます。
