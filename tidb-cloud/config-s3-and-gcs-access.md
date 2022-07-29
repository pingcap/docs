---
title: Configure Amazon S3 Access and GCS Access
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3) access and Google Cloud Storage (GCS) access.
---

# AmazonS3AccessとGCSAccessを設定します {#configure-amazon-s3-access-and-gcs-access}

ソースデータがAmazonS3またはGCSバケットに保存されている場合は、データをTiDB Cloudにインポートまたは移行する前に、バケットへのクロスアカウントアクセスを設定する必要があります。このドキュメントでは、これを行う方法について説明します。

-   [AmazonS3アクセスを設定する](#configure-amazon-s3-access)
-   [GCSアクセスを構成する](#configure-gcs-access)

## AmazonS3アクセスを設定する {#configure-amazon-s3-access}

TiDBCloudがTiDB Cloudバケットのソースデータにアクセスできるようにするには、次の手順を実行してTiDB Cloudのバケットアクセスを設定し、Role-ARNを取得します。プロジェクト内の1つのTiDBクラスタの設定が完了すると、そのプロジェクト内のすべてのTiDBクラスターが同じRole-ARNを使用してAmazonS3バケットにアクセスできるようになります。

1.  TiDB Cloud Consoleで、ターゲットTiDBクラスタのTiDB CloudアカウントIDと外部IDを取得します。

    1.  TiDB Cloud Consoleで、ターゲットプロジェクトを選択し、ターゲットクラスタの名前をクリックして概要ページに移動します。
    2.  左側のクラスタ概要ペインで、[**インポート**]をクリックします。 [<strong>データインポートタスク]</strong>ページが表示されます。
    3.  [**データインポートタスク**]ページで、[ <strong>AWS IAMポリシー設定の表示</strong>]をクリックして、 TiDB CloudアカウントIDとTiDB Cloud外部IDを取得します。後で使用するために、これらのIDをメモしてください。

2.  AWSマネジメントコンソールで、AmazonS3バケットのマネージドポリシーを作成します。

    1.  AWSマネジメントコンソールにサインインし、AmazonS3コンソールを[https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)で開きます。

    2.  [**バケット**]リストで、ソースデータを含むバケットの名前を選択し、[ARNの<strong>コピー</strong>]をクリックしてS3バケットのARNを取得します（たとえば、 `arn:aws:s3:::tidb-cloud-source-data` ）。後で使用するために、バケットARNをメモしておきます。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)でIAMコンソールを開き、左側のナビゲーションペインで[**ポリシー**]をクリックしてから、[ポリシーの<strong>作成</strong>]をクリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  [**ポリシーの作成**]ページで、[ <strong>JSON</strong> ]タブをクリックします。

    5.  次のアクセスポリシーテンプレートをコピーして、ポリシーテキストフィールドに貼り付けます。

        ```
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket",
                        "s3:GetBucketLocation"
                    ],
                    "Resource": "<Your S3 bucket ARN>"
                }
            ]
        }
        ```

        ポリシーテキストフィールドで、次の構成を独自の値に更新します。

        -   `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            たとえば、ソースデータが`tidb-cloud-source-data`バケットのルートディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`を使用します。ソースデータがバケットの`mydata`ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`を使用します。 TiDB Cloudがこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの最後に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"`

            たとえば、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data"` 。

    6.  [**次へ：タグ**]をクリックし、ポリシーのタグを追加して（オプション）、[<strong>次へ：レビュー</strong>]をクリックします。

    7.  ポリシー名を設定し、[**ポリシーの作成**]をクリックします。

3.  AWSマネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロールARNを取得します。

    1.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)のIAMコンソールで、左側のナビゲーションペインで[**役割**]をクリックし、[役割の<strong>作成</strong>]をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   [**信頼できるエンティティタイプ**]で、[ <strong>AWSアカウント]</strong>を選択します。
        -   [ **AWSアカウント**]で、[<strong>別のAWSアカウント</strong>]を選択し、 TiDB CloudアカウントIDを[<strong>アカウントID]</strong>フィールドに貼り付けます。
        -   [**オプション**]で、[外部IDが必要] <strong>（サードパーティがこの役割を引き受ける場合のベストプラクティス）を</strong>クリックし、 TiDB Cloud外部IDを[<strong>外部ID</strong> ]フィールドに貼り付けます。

    3.  [**次へ**]をクリックしてポリシーリストを開き、作成したポリシーを選択して、[<strong>次へ</strong>]をクリックします。

    4.  [**役割の詳細**]で、役割の名前を設定し、右下隅にある[<strong>役割の作成</strong>]をクリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックして概要ページに移動し、ロールARNをコピーします。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4.  TiDB Cloudコンソールで、 TiDB CloudアカウントIDと外部IDを取得する**[データインポートタスク**]ページに移動し、ロールARNを[<strong>ロールARN]</strong>フィールドに貼り付けます。

## GCSアクセスを構成する {#configure-gcs-access}

TiDBクラウドがGCSバケット内のソースデータにアクセスできるようにするには、各TiDB CloudのGCSアクセスをGCPプロジェクトとGCSバケットペアのサービスとして構成する必要があります。プロジェクト内の1つのクラスタの構成が完了すると、そのプロジェクト内のすべてのデータベースクラスターがGCSバケットにアクセスできるようになります。

1.  ターゲットTiDBクラスタのGoogleCloudServiceアカウントIDを取得します。

    1.  TiDB Cloud Adminコンソールで、Google Cloud Platformにデプロイされているターゲットプロジェクトとターゲットクラスタを選択し、[**インポート**]をクリックします。
    2.  [ **Google Cloud ServiceアカウントIDを表示]**をクリックして、サービスアカウントIDをコピーします。

2.  Google Cloud Platform（GCP）管理コンソールで、[ **IAMと管理**]&gt; [<strong>役割</strong>]に移動し、ストレージコンテナの次の読み取り専用権限を持つ役割が存在するかどうかを確認します。

    -   storage.buckets.get
    -   storage.objects.get
    -   storage.objects。リスト

    はいの場合、次の手順でターゲットTiDBクラスタに一致する役割を使用できます。そうでない場合は、[ **IAMと管理**]&gt;[<strong>ロール</strong>]&gt;[ <strong>CREATE ROLE</strong> ]に移動して、ターゲットTiDBクラスタのロールを定義します。

3.  [**クラウドストレージ**]&gt;[<strong>ブラウザ</strong>]に移動し、 TiDB CloudがアクセスするGCSバケットを選択して、[<strong>情報</strong>パネルの表示]をクリックします。

    パネルが表示されます。

4.  パネルで、[ **PRINCIPAL**の追加]をクリックします。

    プリンシパルを追加するためのダイアログボックスが表示されます。

5.  ダイアログボックスで、次の手順を実行します。

    1.  [**新しいプリンシパル**]フィールドに、ターゲットTiDBクラスタのGoogleCloudServiceアカウントIDを貼り付けます。
    2.  [**役割**]ドロップダウンリストで、ターゲットTiDBクラスタの役割を選択します。
    3.  [**保存]**をクリックします。

これで、 TiDB CloudクラスタがGCSバケットにアクセスできるようになりました。

> **ノート：**
>
> TiDB Cloudへのアクセスを削除するには、追加したプリンシパルを削除するだけです。
