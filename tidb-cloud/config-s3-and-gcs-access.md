---
title: Configure Amazon S3 Access and GCS Access
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3) access and Google Cloud Storage (GCS) access.
---

# Amazon S3 アクセスと GCS アクセスの設定 {#configure-amazon-s3-access-and-gcs-access}

ソース データが Amazon S3 または GCS バケットに保存されている場合は、データをTiDB Cloudにインポートまたは移行する前に、バケットへのクロスアカウント アクセスを構成する必要があります。このドキュメントでは、これを行う方法について説明します。

-   [Amazon S3 アクセスの構成](#configure-amazon-s3-access)
-   [GCS アクセスの構成](#configure-gcs-access)

## Amazon S3 アクセスの構成 {#configure-amazon-s3-access}

TiDB Cloudが Amazon S3 バケットのソース データにアクセスできるようにするには、次の手順TiDB Cloudのバケット アクセスを設定し、Role-ARN を取得します。プロジェクト内の 1 つの TiDBクラスタの設定が完了すると、そのプロジェクト内のすべての TiDB クラスターが同じ Role-ARN を使用して Amazon S3 バケットにアクセスできるようになります。

1.  TiDB Cloudコンソールで、ターゲットの TiDBクラスタのTiDB Cloudアカウント ID と外部 ID を取得します。

    1.  TiDB Cloudコンソールで、ターゲット プロジェクトを選択し、[**アクティブなクラスター**] ページに移動します。

    2.  ターゲットクラスタの領域を見つけて、領域の右上隅にある [**データのインポート**] をクリックします。 [<strong>データ インポート タスク]</strong>ページが表示されます。

        > **ヒント：**
        >
        > または、[**アクティブなクラスター**] ページでクラスタの名前をクリックし、右上隅にある [<strong>データのインポート</strong>] をクリックすることもできます。

    3.  [**データ インポート タスク**] ページで、[ <strong>AWS IAMポリシー設定を表示</strong>] をクリックして、 TiDB Cloudアカウント ID とTiDB Cloud外部 ID を取得します。後で使用するために、これらの ID をメモしておいてください。

2.  AWS マネジメント コンソールで、Amazon S3 バケットの管理ポリシーを作成します。

    1.  AWS マネジメント コンソールにサインインし、 [https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)で Amazon S3 コンソールを開きます。

    2.  [**バケット**] リストで、ソース データを含むバケットの名前を選択し、[ <strong>ARN のコピー</strong>] をクリックして、S3 バケット ARN (たとえば、 `arn:aws:s3:::tidb-cloud-source-data` ) を取得します。後で使用するために、バケット ARN を書き留めます。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)でIAMコンソールを開き、左側のナビゲーション ペインで [**ポリシー**] をクリックし、[ポリシーの<strong>作成</strong>] をクリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  [**ポリシーの作成**] ページで、[ <strong>JSON</strong> ] タブをクリックします。

    5.  次のアクセス ポリシー テンプレートをコピーして、ポリシー テキスト フィールドに貼り付けます。

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

        ポリシー テキスト フィールドで、次の構成を独自の値に更新します。

        -   `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            たとえば、ソース データが`tidb-cloud-source-data`バケットのルート ディレクトリに格納されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`を使用します。ソース データがバケットの`mydata`ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`を使用します。 TiDB Cloudがこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの最後に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"`

            たとえば、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data"`です。

    6.  [**次へ: タグ**] をクリックし、ポリシーのタグを追加して (オプション)、[<strong>次へ: 確認</strong>] をクリックします。

    7.  ポリシー名を設定し、[**ポリシーの作成**] をクリックします。

3.  AWS マネジメント コンソールで、 TiDB Cloudのアクセス ロールを作成し、ロール ARN を取得します。

    1.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)のIAMコンソールで、左側のナビゲーション ペインで [**ロール**] をクリックし、[ロールの<strong>作成</strong>] をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   [**信頼されたエンティティ タイプ**] で、[ <strong>AWS アカウント]</strong>を選択します。
        -   **An AWS account**で、 <strong>Another AWS account</strong>を選択し、 TiDB Cloudアカウント ID を<strong>Account ID</strong>フィールドに貼り付けます。
        -   [**オプション**] で、[<strong>外部 ID を要求する (サード パーティがこのロールを引き受ける場合のベスト プラクティス</strong>)] をクリックし、 TiDB Cloudの外部 ID を [<strong>外部 ID</strong> ] フィールドに貼り付けます。

    3.  [**次へ**] をクリックしてポリシー リストを開き、作成したポリシーを選択して、[<strong>次へ</strong>] をクリックします。

    4.  [**ロールの詳細**] で、ロールの名前を設定し、右下隅にある [<strong>ロールの作成</strong>] をクリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックしてその概要ページに移動し、ロール ARN をコピーします。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4.  TiDB Cloudコンソールで、 TiDB Cloudアカウント ID と外部 ID を取得する**Data Import Task**ページに移動し、ロール ARN を<strong>Role ARN</strong>フィールドに貼り付けます。

## GCS アクセスの構成 {#configure-gcs-access}

TiDB クラウドが GCS バケット内のソース データにアクセスできるようにするには、GCP プロジェクトと GCS バケット ペアのサービスとして各TiDB Cloudの GCS アクセスを構成する必要があります。プロジェクト内の 1 つのクラスタの構成が完了すると、そのプロジェクト内のすべてのデータベース クラスタが GCS バケットにアクセスできるようになります。

1.  ターゲット TiDBクラスタの Google Cloud サービス アカウント ID を取得します。

    1.  TiDB Cloud管理コンソールで、Google Cloud Platform にデプロイされたターゲット プロジェクトとターゲットクラスタを選択し、右上隅にある [**データのインポート**] をクリックします。
    2.  [ **Google Cloud サービス アカウント ID を表示]**をクリックし、サービス アカウント ID をコピーします。

2.  Google Cloud Platform (GCP) 管理コンソールで、[ **IAM &amp; Admin** ] &gt; [ <strong>Roles</strong> ] に移動し、ストレージ コンテナーの次の読み取り専用権限を持つロールが存在するかどうかを確認します。

    -   storage.buckets.get
    -   storage.objects.get
    -   ストレージ.オブジェクト。リスト

    はいの場合は、次の手順でターゲット TiDBクラスタに一致するロールを使用できます。そうでない場合は、[ **IAM &amp; Admin** ] &gt; [ <strong>Roles</strong> ] &gt; [ <strong>CREATE ROLE</strong> ] に移動して、ターゲットの TiDBクラスタの役割を定義します。

3.  **Cloud Storage** &gt; <strong>Browser</strong>に移動し、 TiDB Cloudがアクセスする GCS バケットを選択して、 <strong>SHOW INFO PANEL</strong>をクリックします。

    パネルが表示されます。

4.  パネルで、[**プリンシパル**を追加] をクリックします。

    プリンシパルを追加するためのダイアログ ボックスが表示されます。

5.  ダイアログ ボックスで、次の手順を実行します。

    1.  [**新しいプリンシパル**] フィールドに、ターゲットの TiDBクラスタの Google Cloud サービス アカウント ID を貼り付けます。
    2.  [**役割**] ドロップダウン リストで、ターゲットの TiDBクラスタの役割を選択します。
    3.  [**保存]**をクリックします。

TiDB Cloudクラスタが GCS バケットにアクセスできるようになりました。

> **ノート：**
>
> TiDB Cloudへのアクセスを削除するには、追加したプリンシパルを削除するだけです。
