---
title: TiDB Cloud Dedicated Database Audit Logging (Preview)
summary: TiDB Cloudでクラスターを監査する方法について説明します。
---

# TiDB Cloud Dedicatedデータベース監査ログ (Preview) {#tidb-cloud-dedicated-database-audit-logging}

TiDB Cloud は、実行された SQL ステートメントなど、データベースへのユーザー アクセス アクティビティを記録する監査ログ機能を提供します。

> **Note:**
>
> データベース監査ログは、次の要件を満たす対象の TiDB Cloud Dedicated クラスターでパブリックプレビューとして利用できます。
>
> - AWS および Google Cloud でホストされるクラスターの場合: TiDB バージョンが v7.5.6 以降、または v8.5.2 以降である必要があります。
> - Azure でホストされるクラスターの場合: TiDB バージョンが v7.5.6 以降、または v8.5.2 以降であり、クラスターが 2026年 4月 15日以降に作成されている必要があります。
>
> その他のすべての TiDB バージョンまたはクラスター構成では、データベース監査ログはリクエストに応じて利用できます。対象外のクラスターへのアクセスをリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**？**をクリックし、 **Support Tickets**をクリックして[ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/portals)に進みます。チケットを作成し、 **説明**欄に「データベース監査ログの申請」と入力して、 **「送信」を**クリックしてください。
>
> このドキュメントは、監査ログ機能のパブリックプレビュー版にのみ適用されます。以前のバージョンのデータベース監査ログを使用している場合は、 [TiDB Cloud Database Audit Logging (Legacy)](/tidb-cloud/tidb-cloud-auditing-legacy.md)を参照してください。

組織のユーザー アクセス ポリシーやその他の情報セキュリティ対策の有効性を評価するには、データベース監査ログを定期的に分析することがセキュリティのベスト プラクティスです。

監査ログ機能は**デフォルトで無効に**なっています。クラスターを監査するには、まず監査ログを有効にし、次に監査フィルタルールを指定する必要があります。

> **Note:**
>
> 監査ログはクラスターのリソースを消費するため、クラスターを監査するかどうかは慎重に検討する必要があります。

## 前提条件 {#prerequisites}

-   TiDB Cloud Dedicated クラスターを使用しています。

    > **Note:**
    >
    > -   データベース監査ログは、 TiDB Cloud Starter では使用できません。
    > -   TiDB Cloud Essential については、 [TiDB Cloud Essential のデータベース監査ログ (PREVIEW)](/tidb-cloud/essential-database-audit-logging.md)を参照してください。

-   組織内で`Organization Owner`または`Project Owner`ロールに所属しています。それ以外の場合、 TiDB Cloudコンソールでデータベース監査関連のオプションは表示されません。詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)ご覧ください。

## 監査ログを有効にする {#enable-audit-logging}

TiDB Cloudは、 TiDB Cloud Dedicatedクラスタの監査ログをクラウドストレージサービスに書き込むことをサポートしています。データベース監査ログを有効にする前に、クラスタが配置されているクラウドプロバイダーでクラウドストレージサービスを設定してください。

> **Note:**
>
> AWS にデプロイされた TiDB クラスターでは、データベース監査ログを有効にする際に、監査ログファイルをTiDB Cloudに保存することを選択できます。現在、この機能はリクエストに応じてのみ利用可能です。この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**[?]**をクリックし、 **Support Tickets**をクリックして[ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/portals)に進みます。チケットを作成し、 **[説明]**フィールドに「監査ログファイルをTiDB Cloudに保存する申請」と入力して、 **[送信] を**クリックします。

### AWSの監査ログを有効にする {#enable-audit-logging-for-aws}

AWS の監査ログを有効にするには、次の手順を実行します。

#### ステップ1. Amazon S3バケットを作成する {#step-1-create-an-amazon-s3-bucket}

TiDB Cloud が監査ログを書き込む宛先として、組織所有の AWS アカウント内の Amazon S3 バケットを指定します。

> **Note:**
>
> AWS S3バケットでオブジェクトロックを有効にしないでください。オブジェクトロックを有効にすると、 TiDB Cloudが監査ログファイルをS3にプッシュできなくなります。

詳細については、AWS ユーザーガイドの[バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。

#### ステップ2. Amazon S3アクセスを構成する {#step-2-configure-amazon-s3-access}

1.  監査ログを有効にする TiDB クラスターのTiDB Cloudアカウント ID と外部 ID を取得します。

    1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **Tip:**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **DB Audit Logging**をクリックします。

    3.  **DB Audit Logging**ページで、右上隅の**[有効化]**をクリックします。

    4.  **データベース監査ログストレージ設定**ダイアログで、 **AWS IAM Policy Settings**セクションを見つけて、後で使用するために**TiDB Cloud Account ID**と**TiDB Cloud External ID**を記録します。

2.  [AWS Management Console](https://console.aws.amazon.com/)で、 **IAM** &gt; **Access Management** &gt; **Policies**に移動し、書き込み専用権限`s3:PutObject`を持つIAMポリシーがあるかどうかを確認します。

    -   はいの場合は、後で使用するために一致したポリシーを記録します。
    -   そうでない場合は、 **IAM** &gt; **Access Management** &gt; **Policies** &gt; **Create Policy**に移動し、次のポリシー テンプレートに従ってIAMポリシーを定義します。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": "<Your S3 bucket ARN>/*"
                }
            ]
        }
        ```

        テンプレート内の`<Your S3 bucket ARN>`は、監査ログファイルが書き込まれるS3バケットのAmazonリソースネーム（ARN）です。S3バケットの**プロパティ**タブに移動し、 **Bucket Overview**エリアでARN値を確認できます。「 `"Resource"`フィールドでは、ARNの後に`/*`を追加する必要があります。例えば、ARNが`arn:aws:s3:::tidb-cloud-test`の場合、 `"Resource"`フィールドの値を`"arn:aws:s3:::tidb-cloud-test/*"`に設定する必要があります。

3.  **IAM** &gt; **Access Management** &gt; **Roles**に移動し、前に記録したTiDB Cloudアカウント ID と外部 ID に対応する信頼エンティティを持つロールがすでに存在するかどうかを確認します。

    -   はいの場合は、後で使用するために一致したロールを記録します。
    -   そうでない場合は、 **Create role**をクリックし、信頼エンティティタイプとして**Another AWS account**を選択し、 **Account ID**フィールドにTiDB CloudのアカウントIDを入力します。次に、 **Require External ID**オプションを選択し、 **External ID**フィールドにTiDB Cloudの外部IDを入力します。

4.  **IAM** &gt; **Access Management** &gt; **Roles**で、前の手順のロール名をクリックして**概要**ページに移動し、次の手順を実行します。

    1.  **権限**タブで、書き込み専用権限`s3:PutObject`を持つ記録済みのポリシーがロールにアタッチされているかどうかを確認します。アタッチされていない場合は、 **Attach Policies**を選択し、必要なポリシーを検索して**Attach Policy**をクリックします。
    2.  **概要**ページに戻り、**Role ARN**値をクリップボードにコピーします。

#### ステップ3. 監査ログを有効にする {#step-3-enable-audit-logging}

TiDB Cloudコンソールで、 TiDB Cloudアカウント ID と外部 ID 値を取得した**[データベース監査ログストレージ設定]**ダイアログ ボックスに戻り、次の手順を実行します。

1.  **Bucket URI**フィールドに、監査ログファイルが書き込まれる S3 バケットの URI を入力します。

2.  **Bucket Region**ドロップダウンリストで、バケットが配置されている AWS リージョンを選択します。

3.  **Role ARN**フィールドに、 [ステップ2. Amazon S3アクセスを構成する](#step-2-configure-amazon-s3-access)でコピーしたロール ARN 値を入力します。

4.  **Test Connection and Next**をクリックして、 TiDB Cloud がバケットにアクセスして書き込むことができるかどうかを確認します。接続に成功すると、ダイアログはデータベース監査ログ設定の次のステップに進みます。

> **Note:**
>
> -   監査ログを有効にした後、バケットのURI、場所、またはARNに新しい変更を加えた場合は、監査ログを無効にしてから再度有効にする必要があります。
> -   TiDB Cloud の Amazon S3 へのアクセスを削除するには、AWS マネジメントコンソールでこのクラスターに付与された信頼ポリシーを削除するだけです。

### Google Cloud の監査ログを有効にする {#enable-audit-logging-for-google-cloud}

Google Cloud の監査ログを有効にするには、次の手順に従います。

#### ステップ1. GCSバケットを作成する {#step-1-create-a-gcs-bucket}

TiDB Cloud が監査ログを書き込む宛先として、組織所有の Google Cloud アカウント内の Google Cloud Storage（GCS）バケットを指定します。

詳細については、Google Cloud Storage ドキュメントの[ストレージバケットの作成](https://cloud.google.com/storage/docs/creating-buckets)ご覧ください。

#### ステップ2. GCSアクセスを構成する {#step-2-configure-gcs-access}

1.  監査ログを有効にする TiDB クラスタの Google Cloud サービス アカウント ID を取得します。

    1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **Tip:**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **DB Audit Logging**をクリックします。

    3.  **DB Audit Logging**ページで、右上隅の**[有効化]**をクリックします。

    4.  **[データベース監査ログストレージ設定]**ダイアログで、 **[Google Cloud Service アカウント ID]**セクションを見つけて、後で使用するために**Service Account ID**を記録します。

2.  [Google Cloud console](https://console.cloud.google.com/)で、 **IAM & Admin** &gt; **[ロール]**に移動し、ストレージバケット内のオブジェクトに対する次の書き込み専用権限を持つロールが存在するかどうかを確認します。

    -   storage.objects.create
    -   storage.objects.delete

    はいの場合は、後で使用するためにTiDBクラスターの一致したロールを記録してください。いいえの場合は、 **IAM & Admin** &gt; **ロール** &gt; **CREATE ROLE**に移動して、TiDBクラスターのロールを定義してください。

3.  **[Cloud Storage]** &gt; **[ブラウザ]**に移動し、 TiDB Cloudがアクセスする GCS バケットを選択して、 **SHOW INFO PANEL**をクリックします。

    パネルが表示されます。

4.  パネルで、 **ADD PRINCIPAL**をクリックします。

    プリンシパルを追加するためのダイアログ ボックスが表示されます。

5.  ダイアログ ボックスで、次の手順を実行します。

    1.  **New Principals**フィールドに、TiDB クラスタの Google Cloud サービス アカウント ID を貼り付けます。
    2.  **[ロール]**ドロップダウン リストで、ターゲット TiDB クラスターのロールを選択します。
    3.  **[保存]**をクリックします。

#### ステップ3. 監査ログを有効にする {#step-3-enable-audit-logging}

TiDB Cloudコンソールで、 Google Cloud サービス アカウント ID を取得した**[データベース監査ログストレージ設定]**ダイアログ ボックスに戻り、次の手順を実行します。

1.  **Bucket URI**フィールドに、完全な GCS バケット名を入力します。

2.  **Bucket Region**フィールドで、バケットが配置されている GCS リージョンを選択します。

3.  **Test Connection and Next**をクリックして、 TiDB Cloud がバケットにアクセスして書き込むことができるかどうかを確認します。接続に成功すると、ダイアログはデータベース監査ログ設定の次のステップに進みます。

> **Note:**
>
> -   監査ログを有効にした後、バケットのURIまたは場所に新たな変更を加えた場合は、監査ログを無効にしてから再度有効にする必要があります。
> -   TiDB Cloud の GCS バケットへのアクセスを削除するには、Google Cloud コンソールでこのクラスタに付与された信頼ポリシーを削除します。

### Azureの監査ログを有効にする {#enable-audit-logging-for-azure}

Azure の監査ログを有効にするには、次の手順を実行します。

#### ステップ1. Azureストレージアカウントを作成する {#step-1-create-an-azure-storage-account}

TiDB Cloudがデータベース監査ログを書き込む宛先として、組織の Azure サブスクリプションに Azureストレージアカウントを作成します。

詳細については、Azure ドキュメントの[Azureストレージアカウントを作成する](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)を参照してください。

#### ステップ2. Azure Blob Storageアクセスを構成する {#step-2-configure-azure-blob-storage-access}

1.  [Azureポータル](https://portal.azure.com/)で、データベース監査ログを保存するために使用するコンテナを作成します。

    1.  Azure ポータルの左側のナビゲーション ウィンドウで、 **Storage Accounts**をクリックし、データベース監査ログを保存するストレージアカウントをクリックします。

        > **Tip:**
        >
        > 左側のナビゲーション ペインが非表示になっている場合は、左上隅のメニュー ボタンをクリックして表示を切り替えます。

    2.  選択したストレージアカウントのナビゲーション ウィンドウで、 **Data storage > Containers**をクリックし、 **+ Container**をクリックして**New container**ウィンドウを開きます。

    3.  **New container**ペインで、新しいコンテナの名前を入力し、匿名アクセスレベル（推奨レベルは**プライベート** （匿名アクセスなし））を設定して、 **作成**をクリックします。数秒以内に新しいコンテナが作成され、コンテナリストに表示されます。

2.  ターゲット コンテナの URL を取得します。

    1.  コンテナー リストで、対象のコンテナーを選択し、コンテナーの**[...]**をクリックして、 **Container properties**を選択します。
    2.  表示されたプロパティ ページで、後で使用するために**URL**値をコピーし、コンテナー リストに戻ります。

3.  ターゲット コンテナーの SAS トークンを生成します。

    1.  コンテナー リストで、ターゲット コンテナーを選択し、コンテナーの**[...]**をクリックして、 **Generate SAS**を選択します。

    2.  表示された**Generate SAS**ペインで、**Signing method**として**Account key**を選択します。

    3.  **[権限]**ドロップダウン リストで、 **[読み取り]** 、 **[書き込み]** 、 **[作成]**を選択して、監査ログ ファイルの書き込みを許可します。

    4.  **[開始] フィールド**と**[有効期限]**フィールドで、SAS トークンの有効期間を指定します。

        > **Note:**
        >
        > -   監査機能はストレージアカウントに監査ログを継続的に書き込む必要があるため、SASトークンの有効期間は十分に長くなければなりません。ただし、有効期間が長すぎるとトークン漏洩のリスクが高まります。セキュリティ上、SASトークンは6～12か月ごとに交換することをお勧めします。
        > -   生成された SAS トークンは取り消すことができないため、有効期間を慎重に設定する必要があります。
        > -   監査ログの継続的な可用性を確保するために、SAS トークンの有効期限が切れる前に必ず再生成して更新してください。

    5.  **Allowed protocols**については、安全なアクセスを確保するために**HTTPS only**を選択します。

    6.  **[SAS トークンと URL の生成]**をクリックし、表示される**Blob SAS token**を後で使用するためにコピーします。

#### ステップ3. 監査ログを有効にする {#step-3-enable-audit-logging}

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **DB Audit Logging**をクリックします。

3.  **DB Audit Logging**ページで、右上隅の**[有効化]**をクリックします。

4.  **データベース監査ログストレージ設定**ダイアログで、 [ステップ2. Azure BLOBアクセスを構成する](#step-2-configure-azure-blob-storage-access)から取得した BLOB URL と SAS トークンを指定します。

    -   **Blob URL**フィールドに、監査ログが保存されるコンテナの URL を入力します。
    -   **SAS Token**フィールドに、コンテナーにアクセスするための SAS トークンを入力します。

5.  **Test Connection and Next**をクリックして、TiDB Cloud がコンテナにアクセスして書き込むことができるかどうかを確認します。接続に成功すると、ダイアログはデータベース監査ログ設定の次のステップに進みます。

> **Note:**
>
> 監査ログを有効にした後、 **BLOB URL**または**SAS Token**フィールドに新しい変更を加えた場合は、監査ログを無効にしてから再度有効にする必要があります。

## データベース監査ログ設定を構成する {#configure-database-audit-logging-settings}

クラウドプロバイダーのストレージを構成した後、データベース監査ログ設定のステップを完了します。

1. ログファイルのローテーションポリシーを設定します。

    ファイルサイズまたは時間間隔に基づいて監査ログファイルをローテーションできます。いずれかの条件が満たされると、TiDB Cloud は新しい監査ログファイルを生成します。

    > **Note:**
    >
    > 時間間隔に基づくログファイルのローテーションは、TiDB v8.5.2 以降にのみ適用されます。TiDB Cloud Dedicated クラスターの TiDB バージョンが v8.5.2 より前の場合、ファイルサイズに基づいてのみ監査ログファイルをローテーションできます。

2. ログの秘匿化を構成します。

    ログの秘匿化はデフォルトで有効になっています。有効にすると、SQL テキスト内の機密情報は監査ログで `?` に置き換えられます。

3. **Save and Enable** をクリックして設定を適用し、監査ログを有効にします。

> **Note:**
>
> ログの秘匿化を無効にすると、クラウドストレージに書き込まれる監査ログファイルに機密情報が含まれる可能性があります。潜在的なセキュリティリスクがあるため、この設定は推奨されません。

## 監査フィルタルールを指定する {#specify-audit-filter-rules}

監査ログを有効にした後、監査フィルタルールを指定して、どのユーザーアクセスイベントをキャプチャし、監査ログに書き込むかを制御する必要があります。フィルタルールが指定されていない場合、 TiDB Cloudは何もログに記録しません。

クラスターの監査フィルター ルールを指定するには、次の手順を実行します。

1.  **DB Audit Logging**ページで、 **Audit Filters**セクションの**Add Filter Rule**をクリックして、監査フィルタ ルールを追加します。

2.  **Add Filter Rule**ダイアログで、次の項目を設定します。

    -   **Filter Name**: フィルタルールの名前を入力します。
    -   **SQL User**: `<user>@<host>` 形式で SQL ユーザーを入力します。ユーザー名とホスト名では、0 文字以上に一致させるために `%`、ちょうど 1 文字に一致させるために `_` を使用できます。`@` 記号と `<host>` は省略可能です。
    -   **Filter Events**: ログに記録するイベントを選択します。サポートされているフィルタイベントについては、[監査フィルタイベント](#audit-filter-events)を参照してください。

3.  **確認**をクリックしてフィルタルールを追加します。

> **Note:**
>
> -   監査ログはクラスターリソースを消費するため、フィルタールールの指定には注意が必要です。リソース使用量を最小限に抑えるには、可能な限り、監査ログを特定のユーザーとイベントに限定するフィルタールールを指定してください。

## 監査ログを確認する {#view-audit-logs}

デフォルトでは、 TiDB Cloud はデータベース監査ログ ファイルをストレージサービスに保存するため、ストレージサービスから監査ログにアクセスする必要があります。

> **Note:**
>
> 監査ログ ファイルをTiDB Cloudに保存することを要求して選択した場合は、**Database Audit Logging**ページの**Audit Log Access**セクションからダウンロードできます。

TiDB Cloud監査ログは、クラスター ID、ノード ID、およびログ作成日が完全修飾ファイルパスに組み込まれた読み取り可能なテキスト ファイルです。

たとえば、 `13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log` 。この例では、 `13796619446086334065`クラスター ID を示し、 `tidb-0`ノード ID を示します。

## 監査ログを無効にする {#disable-audit-logging}

クラスターの監査が不要になった場合は、次の手順を実行します。

1. TiDB Cloudコンソールで [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、ターゲットの TiDB Cloud Dedicated クラスターの名前をクリックします。
2. 左側のナビゲーション ペインで、**Settings** &gt; **DB Audit Logging** をクリックします。
3. **Database Audit Logging** セクションで、**Settings** の横にある **...** をクリックし、**Disable** をクリックします。

> **Note:**
>
> ログファイルのサイズが10MiBに達するたびに、ログファイルはクラウドストレージバケットにプッシュされます。そのため、監査ログを無効化した後は、10MiB未満のログファイルはクラウドストレージバケットに自動的にプッシュされなくなります。この状況でログファイルを取得するには、 [PingCAPサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## 監査フィルタイベント {#audit-filter-events}

次の表は、データベース監査ログのすべてのイベントクラスを示しています。

| イベントクラス | 説明 | 親クラス |
|---------------|--------------------------------------------------------------------------------------------------|---------------|
| `CONNECTION`    | 接続ハンドシェイク、接続、切断、接続リセット、ユーザー変更など、接続に関連するすべての操作を記録します | -             |
| `CONNECT`       | すべての接続ハンドシェイク操作を記録します                                          | `CONNECTION`    |
| `DISCONNECT`    | すべての切断操作を記録します                                                      | `CONNECTION`    |
| `CHANGE_USER`   | すべてのユーザー変更操作を記録します                                                          | `CONNECTION`    |
| `QUERY`         | データのクエリまたは変更時に発生するエラーを含む、すべての SQL ステートメント操作を記録します  | -               |
| `TRANSACTION`   | `BEGIN`、`COMMIT`、`ROLLBACK` など、トランザクションに関連するすべての操作を記録します         | `QUERY`         |
| `EXECUTE`       | `EXECUTE` ステートメントのすべての操作を記録します                                                | `QUERY`         |
| `QUERY_DML`     | `INSERT`、`REPLACE`、`UPDATE`、`DELETE`、`LOAD DATA` を含む、DML ステートメントのすべての操作を記録します    | `QUERY`     |
| `INSERT`        | `INSERT` ステートメントのすべての操作を記録します                                                   | `QUERY_DML`   |
| `REPLACE`       | `REPLACE` ステートメントのすべての操作を記録します                                                  | `QUERY_DML`   |
| `UPDATE`        | `UPDATE` ステートメントのすべての操作を記録します                                                   | `QUERY_DML`   |
| `DELETE`        | `DELETE` ステートメントのすべての操作を記録します                                                   | `QUERY_DML`   |
| `LOAD DATA`     | `LOAD DATA` ステートメントのすべての操作を記録します                                                | `QUERY_DML`   |
| `SELECT`        | `SELECT` ステートメントのすべての操作を記録します                                                   | `QUERY`       |
| `QUERY_DDL`     | DDL ステートメントのすべての操作を記録します                                                        | `QUERY`       |
| `AUDIT`         | システム変数の設定やシステム関数の呼び出しを含む、TiDB Cloud データベース監査の設定に関連するすべての操作を記録します | -                   |
| `AUDIT_FUNC_CALL` | TiDB Cloud データベース監査に関連するシステム関数の呼び出しのすべての操作を記録します        | `AUDIT`       |
| `AUDIT_SET_SYS_VAR` | システム変数の設定のすべての操作を記録します        | `AUDIT`       |

## 監査ログフィールド {#audit-logging-fields}

監査ログ内の各データベースイベントレコードに対して、TiDB Cloud は次のフィールドを提供します。

### 一般情報 {#general-information}

すべてのクラスの監査ログには、次の情報が含まれます。

| フィールド | 説明 |
|---------------|-----------------------------------------------------------------------------------------------|
| `ID`            | 操作の監査レコードの一意識別子。                        |
| `TIME`          | 監査レコードのタイムスタンプ。                                                             |
| `EVENT`         | 監査レコードのイベントクラス。複数のイベントタイプはコンマ (`,`) で区切られます。     |
| `USER`          | 操作を実行したユーザーの名前。                                                              |
| `ROLES`         | 操作時点でのユーザーのロール。                                            |
| `CONNECTION_ID` | ユーザー接続の識別子。                                                       |
| `TABLES`        | 操作中にアクセスされたテーブル。                                              |
| `STATUS_CODE`   | 監査レコードのステータスコード。`1` は成功、`0` は失敗を意味します。                |
| `KEYSPACE_NAME` | 監査レコードの keyspace 名。                                                        |
| `REASON`        | 監査レコードのエラーメッセージ。操作中にエラーが発生した場合にのみ記録されます。|

### SQL 文情報 {#sql-statement-information}

イベントクラスが `QUERY` または `QUERY` のサブクラスである場合、監査ログには次の情報が含まれます。

| フィールド | 説明 |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `CURRENT_DB`     | 現在のデータベースの名前。                                                                             |
| `SQL_TEXT`       | 実行された SQL 文。監査ログの秘匿化が有効な場合、秘匿化された SQL 文が記録されます。     |
| `EXECUTE_PARAMS` | `EXECUTE` 文のパラメーター。イベントクラスに `EXECUTE` が含まれ、かつ秘匿化が無効な場合にのみ記録されます。 |
| `AFFECTED_ROWS`  | SQL 文の影響を受けた行数。イベントクラスに `QUERY_DML` が含まれる場合にのみ記録されます。  |

### 接続情報 {#connection-information}

イベントクラスが `CONNECTION` または `CONNECTION` のサブクラスである場合、監査ログには次の情報が含まれます。

| フィールド | 説明 |
|-----------------|-----------------------------------------------------------------------------------------------|
| `CURRENT_DB`      | 現在のデータベースの名前。イベントクラスに DISCONNECT が含まれる場合、この情報は記録されません。 |
| `CONNECTION_TYPE` | 接続タイプ。Socket、UnixSocket、SSL/TLS が含まれます。                                 |
| `PID`             | 現在の接続のプロセス ID。                                                          |
| `SERVER_VERSION`  | 接続先 TiDB サーバーの現在のバージョン。                                                  |
| `SSL_VERSION`     | 使用中の SSL の現在のバージョン。                                                                 |
| `HOST_IP`         | 接続先 TiDB サーバーの現在の IP アドレス。                                               |
| `HOST_PORT`       | 接続先 TiDB サーバーの現在のポート。                                                     |
| `CLIENT_IP`       | クライアントの現在の IP アドレス。                                                              |
| `CLIENT_PORT`     | クライアントの現在のポート。                                                                    |

> **Note:**
>
> トラフィックの可視性を向上させるため、`CLIENT_IP` には AWS PrivateLink 経由の接続について、Load Balancer (LB) の IP ではなく実際のクライアント IP アドレスが表示されるようになりました。現在、この機能はベータ版であり、AWS リージョン `Frankfurt (eu-central-1)` でのみ利用できます。

### 監査操作情報 {#audit-operation-information}

イベントクラスが `AUDIT` または `AUDIT` のサブクラスである場合、監査ログには次の情報が含まれます。

| フィールド | 説明 |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `AUDIT_OP_TARGET`| TiDB Cloud データベース監査設定変更の対象オブジェクト。 |
| `AUDIT_OP_ARGS`  | TiDB Cloud データベース監査設定変更で使用される引数。 |

## 監査ログの制限事項 {#audit-logging-limitations}

{{{ .dedicated }}} では、監査ログが時系列順に書き込まれることは保証されません。つまり、最新のイベントを見つけるにはすべてのログファイルを確認する必要がある場合があります。ログを時系列順に並べ替えるには、監査ログの `TIME` フィールドを使用できます。

## データベース監査ログ（レガシー）のリファレンス {#legacy-database-audit-logging-reference}

現在レガシー監査ログプラグインを利用している場合は、[Database Audit Logging (Legacy)](/tidb-cloud/tidb-cloud-auditing-legacy.md) を参照してください。
