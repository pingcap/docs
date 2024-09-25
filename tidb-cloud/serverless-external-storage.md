---
title: Configure TiDB Cloud Serverless External Storage Access
summary: Amazon Simple Storage Service (Amazon S3) アクセスを構成する方法を学習します。
---

# TiDB Cloud Serverless の外部ストレージ アクセスを構成する {#configure-external-storage-access-for-tidb-cloud-serverless}

TiDB Cloud Serverless クラスターの外部ストレージからデータをインポートしたり、外部storageにデータをエクスポートしたりする場合は、クロスアカウント アクセスを構成する必要があります。このドキュメントでは、 TiDB Cloud Serverless クラスターの外部storageへのアクセスを構成する方法について説明します。

TiDB Cloud Dedicated クラスター用にこれらの外部ストレージを構成する必要がある場合は、 [TiDB Cloud Dedicatedの外部ストレージアクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md)参照してください。

## Amazon S3 アクセスを構成する {#configure-amazon-s3-access}

TiDB Cloud Serverless クラスターが Amazon S3 バケットにアクセスできるようにするには、クラスターのバケット アクセスを設定する必要があります。バケット アクセスを設定するには、次のいずれかの方法を使用できます。

-   ロール ARN を使用する: ロール ARN を使用して Amazon S3 バケットにアクセスします。
-   AWS アクセスキーを使用する: IAMユーザーのアクセスキーを使用して Amazon S3 バケットにアクセスします。

<SimpleTab>
<div label="Role ARN">

ロール ARN を作成するには、 [AWS クラウドフォーメーション](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)使用することをお勧めします。作成するには、次の手順を実行します。

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **新しい ARN の追加**ダイアログを開きます。

    -   Amazon S3 からデータをインポートする場合は、次のようにして**「新しい ARN の追加」**ダイアログを開きます。

        1.  **S3 からインポートを**クリックします。
        2.  **ファイル URI**フィールドに入力します。
        3.  **AWS ロール ARN を**選択し、 **[ここをクリックして AWS CloudFormation で新規作成] を**クリックします。
    -   データを Amazon S3 にエクスポートする場合は、次のようにして**「新しい ARN の追加」**ダイアログを開きます。

        1.  **[データをエクスポート...]** &gt; **[Amazon S3]**をクリックします。クラスターでこれまでにデータをインポートまたはエクスポートしたことがない場合は、ページの下部にある**[データをエクスポートするには、ここをクリックします...]** &gt; **[Amazon S3] を**クリックします。
        2.  **フォルダー URI**フィールドに入力します。
        3.  **AWS ロール ARN を**選択し、 **[ここをクリックして AWS CloudFormation で新規作成] を**クリックします。

3.  AWS CloudFormation テンプレートを使用してロール ARN を作成します。

    1.  **[新しい ARN の追加]**ダイアログで、 **[CloudFormation テンプレートを使用した AWS コンソール]**をクリックします。

    2.  [AWS マネジメントコンソール](https://console.aws.amazon.com)にログインすると、AWS CloudFormation の**クイック作成スタック**ページにリダイレクトされます。

    3.  **ロール名**を入力します。

    4.  新しいロールを作成することを確認し、 **「スタックの作成」**をクリックしてロール ARN を作成します。

    5.  CloudFormation スタックが実行された後、 **[出力]**タブをクリックし、 **[値]**列でロール ARN 値を見つけることができます。

        ![img.png](/media/tidb-cloud/serverless-external-storage/serverless-role-arn.png)

AWS CloudFormation でロール ARN を作成する際に問題が発生した場合は、次の手順に従って手動で作成できます。

<details><summary>詳細はこちらをクリック</summary>

1.  前の手順で説明した**「新しい ARN の追加」**ダイアログで、 **「問題が発生した場合は、ロール ARN を手動で作成します」を**クリックします。TiDB **TiDB Cloudアカウント ID**と**TiDB Cloud外部 ID**が取得されます。

2.  AWS マネジメントコンソールで、Amazon S3 バケットの管理ポリシーを作成します。

    1.  [AWS マネジメントコンソール](https://console.aws.amazon.com/)にサインインして[Amazon S3 コンソール](https://console.aws.amazon.com/s3/)開きます。

    2.  **[バケット]**リストで、ソース データを含むバケットの名前を選択し、 **[ARN のコピー]**をクリックして S3 バケット ARN (例: `arn:aws:s3:::tidb-cloud-source-data` ) を取得します。後で使用するために、バケット ARN をメモしておきます。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [IAMコンソール](https://console.aws.amazon.com/iam/)を開き、左側のナビゲーション ペインで**[ポリシー]**をクリックして、 **[ポリシーの作成]**をクリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **[ポリシーの作成]**ページで、 **[JSON]**タブをクリックします。

    5.  必要に応じて、ポリシー テキスト フィールドでポリシーを構成します。以下は、TiDB Cloud Serverless クラスターからデータをエクスポートしたり、 TiDB Cloud Serverless クラスターにデータをインポートしたりするために使用できる例です。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:PutObject"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Resource": "<Your S3 bucket ARN>"
                }
            ]
        }
        ```

        ポリシー テキスト フィールドで、次の構成を独自の値に置き換えます。

        -   `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"` 。例えば、

            -   ソース データが`tidb-cloud-source-data`バケットのルート ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`使用します。
            -   ソース データがバケットの`mydata`ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`使用します。

            TiDB Cloud がこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの末尾に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"` 、たとえば`"Resource": "arn:aws:s3:::tidb-cloud-source-data"` 。

        -   カスタマー管理のキー暗号化で AWS Key Management Service キー (SSE-KMS) を有効にしている場合は、ポリシーに次の設定が含まれていることを確認してください。1 `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"`バケットのサンプル KMS キーです。

                {
                    "Sid": "AllowKMSkey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:Decrypt"
                    ],
                    "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
                }

        -   バケット内のオブジェクトが別の暗号化されたバケットからコピーされた場合、KMS キー値には両方のバケットのキーを含める必要があります。たとえば、 `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`です。

    6.  **「次へ」**をクリックします。

    7.  ポリシー名を設定し、ポリシーのタグ（オプション）を追加して、 **「ポリシーの作成」**をクリックします。

3.  AWS マネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロール ARN を取得します。

    1.  [IAMコンソール](https://console.aws.amazon.com/iam/)で、左側のナビゲーション ペインで**[ロール]**をクリックし、 **[ロールの作成]**をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   **信頼されたエンティティタイプ**で、 **AWS アカウントを**選択します。
        -   **「AWS アカウント」**で**「別の AWS アカウント」**を選択し、 TiDB Cloudアカウント ID を**「アカウント ID」**フィールドに貼り付けます。
        -   **オプション**で、**外部 ID が必要 (サードパーティがこのロールを引き受ける場合のベストプラクティス)**をクリックし、 TiDB Cloud外部 ID を**外部 ID**フィールドに貼り付けます。外部 ID が必要 なしでロールを作成した場合、プロジェクト内の 1 つの TiDB クラスターの設定が完了すると、そのプロジェクト内のすべての TiDB クラスターが同じロール ARN を使用して Amazon S3 バケットにアクセスできます。アカウント ID と外部 ID を使用してロールを作成した場合、対応する TiDB クラスターのみがバケットにアクセスできます。

    3.  **[次へ]**をクリックしてポリシー リストを開き、作成したポリシーを選択して、 **[次へ]**をクリックします。

    4.  **ロールの詳細**で、ロールの名前を設定し、右下隅の**ロールの作成を**クリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックして概要ページに移動し、ロール ARN を取得できます。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

</details>

</div>

<div label="Access Key">

アクセスキーを作成するには、AWS アカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセス キーを構成するには、次の手順を実行します。

1.  IAMユーザーを作成します。詳細については、 [IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。

2.  AWS アカウント ID またはアカウントエイリアスと、 IAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインします。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)参照してください。

> **注記：**
>
> TiDB Cloud はアクセス キーを保存しません。インポートまたはエクスポートが完了したら、 [アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)実行することをお勧めします。

</div>
</SimpleTab>

## GCS アクセスを構成する {#configure-gcs-access}

TiDB Serverless クラスターが GCS バケットにアクセスできるようにするには、バケットの GCS アクセスを構成する必要があります。サービス アカウント キーを使用してバケット アクセスを構成できます。

サービス アカウント キーを構成するには、次の手順を実行します。

1.  Google Cloud [サービスアカウントページ](https://console.cloud.google.com/iam-admin/serviceaccounts)で、 **[サービス アカウントの作成]**をクリックしてサービス アカウントを作成します。詳細については、 [サービスアカウントの作成](https://cloud.google.com/iam/docs/creating-managing-service-accounts)参照してください。

    1.  サービス アカウント名を入力します。
    2.  オプション: サービス アカウントの説明を入力します。
    3.  サービス アカウントを作成するには**、[作成して続行]**をクリックします。
    4.  `Grant this service account access to project`で、必要な権限を持つ[IAMロール](https://cloud.google.com/iam/docs/understanding-roles)選択します。たとえば、 TiDB Cloud Serverless クラスターにデータをエクスポートするには、権限`storage.objects.create`を持つロールが必要です。
    5.  **「続行」**をクリックして次のステップに進みます。
    6.  オプション: `Grant users access to this service account`で、 [サービスアカウントを他のリソースに接続する](https://cloud.google.com/iam/docs/attach-service-accounts)が必要なメンバーを選択します。
    7.  **[完了]**をクリックして、サービス アカウントの作成を完了します。

    ![service-account](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2.  サービス アカウントをクリックし、 `KEYS`ページで**[キーの追加]**をクリックしてサービス アカウント キーを作成します。

    ![service-account-key](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3.  デフォルトのキー タイプ`JSON`を選択し、 **[作成]**ボタンをクリックしてサービス アカウント キーをダウンロードします。

## Azure Blob Storage アクセスを構成する {#configure-azure-blob-storage-access}

TiDB Serverless が Azure Blob コンテナーにアクセスできるようにするには、コンテナーの Azure Blob アクセスを構成する必要があります。コンテナー アクセスを構成するには、サービス SAS トークンを使用できます。

1.  [Azure ストレージ アカウント](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)ページで、コンテナーが属するstorageアカウントをクリックします。

2.  **ストレージ アカウント**ページで、[**Security+ ネットワーク]**をクリックし、 **[共有アクセス署名]**をクリックします。

    ![sas-position](/media/tidb-cloud/serverless-external-storage/azure-sas-position.png)

3.  **Shared Access Signature**ページで、次のように必要なアクセス許可を持つサービス SAS トークンを作成します。詳細については、 [サービスSASトークンを作成する](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)参照してください。

    1.  **[許可されたサービス]**セクションで、 **Blob**サービスを選択します。
    2.  **許可されたリソース タイプ**セクションで、**コンテナー**と**オブジェクトを**選択します。
    3.  **[許可された権限]**セクションで、必要に応じて権限を選択します。たとえば、 TiDB Cloud Serverless クラスターにデータをエクスポートするには、**読み取り**権限と**書き込み**権限が必要です。
    4.  必要に応じて**開始日時と有効期限**を調整します。
    5.  その他の設定はデフォルト値のままにしておきます。

    ![sas-create](/media/tidb-cloud/serverless-external-storage/azure-sas-create.png)

4.  SAS トークンを生成するには、 **[SAS と接続文字列の生成]**をクリックします。
