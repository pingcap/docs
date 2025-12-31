---
title: Back Up and Restore TiDB Cloud Premium Data
summary: TiDB Cloud Premium インスタンスをバックアップおよび復元する方法を学びます。
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# TiDB Cloud Premium データのバックアップと復元 {#back-up-and-restore-tidb-cloud-premium-data}

このドキュメントでは、 TiDB Cloud Premiumインスタンスでデータをバックアップおよび復元する方法について説明します。TiDB TiDB Cloud Premiumは自動バックアップをサポートしており、必要に応じてバックアップデータを新しいインスタンスに復元できます。

バックアップ ファイルは、次のソースから作成されます。

-   アクティブなTiDB Cloud Premium インスタンス
-   削除されたプレミアムインスタンスのバックアップ用のごみ箱

> **ヒント：**
>
> -   TiDB Cloud Dedicated クラスターでデータをバックアップおよび復元する方法については、 [TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。
> -   TiDB Cloud Starter またはTiDB Cloud Essential クラスターでデータをバックアップおよび復元する方法については、 [TiDB Cloud StarterまたはEssential Dataのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)参照してください。

## バックアップページをビュー {#view-the-backup-page}

1.  [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページで、ターゲットインスタンスの名前をクリックして、概要ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織とインスタンスを切り替えることができます。

2.  左側のナビゲーション ペインで、 **[データ]** &gt; **[バックアップ]**をクリックします。

## 自動バックアップ {#automatic-backups}

TiDB Cloud Premiumは、本番環境向けに強化された自動バックアップ機能を提供します。高頻度のスナップショットとログバックアップを組み合わせることで、データの信頼性を確保します。

### 自動バックアップポリシー {#automatic-backup-policies}

TiDB Cloud Premium インスタンスは、次の表に示すように、多層バックアップアーキテクチャを使用してデータを保護します。

| バックアップの種類               | 保存期間 | 粒度を復元する                                                             |
| ----------------------- | ---- | ------------------------------------------------------------------- |
| **ポイントインタイムリカバリ（PITR）** | 7日間  | 7 日間の期間内の任意の特定の時点に復元します。                                            |
| **1時間ごとのスナップショット**      | 7日間  | 過去 7 日以内に生成された任意の 1 時間ごとのスナップショットから復元します。                           |
| **毎日のスナップショット**         | 33日間 | 過去33日以内に生成された日次スナップショットから復元します。デフォルトでは、日次スナップショットはUTCの00:00に取得されます。 |

### バックアップ実行ルール {#backup-execution-rules}

-   **バックアップ サイクル**: TiDB Cloud Premium インスタンスは、1 時間ごとと毎日の自動バックアップを実行します。

-   **バックアップスケジュール**:

    -   毎時バックアップは毎時開始時に実行されます。
    -   毎日のバックアップは毎日 00:00 UTC に実行されます。
    -   現在、バックアップ スケジュールをカスタマイズまたは管理することはできません。

-   **保持動作**: バックアップは保持期間 (7 日間または 33 日間) を超えると自動的に期限切れとなり、復元できなくなります。

> **注記：**
>
> -   自動バックアップstorageのコストは、バックアップ データの量と保持期間によって異なります。
> -   バックアップ保持期間をデフォルトの制限を超えて延長するには、 [TiDB Cloudサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

### バックアップファイルを削除する {#delete-backup-files}

TiDB Cloud Premium インスタンスの既存のバックアップ ファイルを削除するには、次の手順を実行します。

1.  インスタンスの[**バックアップ**](#view-the-backup-page)ページに移動します。

2.  削除する対応するバックアップ ファイルを見つけて、 **[アクション]**列の**[...]** &gt; **[削除]**をクリックします。

## 復元する {#restore}

TiDB Cloudは、偶発的な損失や破損が発生した場合にデータを復旧するための復元機能を提供します。アクティブなインスタンスのバックアップ、またはごみ箱内の削除されたインスタンスから復元できます。

### 復元モード {#restore-mode}

TiDB Cloud は、インスタンスのスナップショット復元とポイントインタイム復元をサポートします。

-   **スナップショットの復元**: 特定のバックアップ スナップショットからインスタンスを復元します。

-   **ポイントインタイム リストア**: インスタンスを特定の時点に復元します。

    -   プレミアム インスタンス: 過去 33 日以内の任意の時点に復元できますが、インスタンスの作成時刻より前、または現在の時刻の 1 分前より後の時点には復元できません。

### 宛先を復元 {#restore-destination}

TiDB Cloud は、新しいインスタンスへのデータの復元をサポートしています。

### 新しいインスタンスに復元する {#restore-to-a-new-instance}

データを新しいインスタンスに復元するには、次の手順を実行します。

1.  インスタンスの[**バックアップ**](#view-the-backup-page)ページに移動します。

2.  **[復元]**をクリックします。

3.  **「バックアップの選択」**ページで、使用する**復元モード**を選択します。特定のバックアップスナップショットから復元することも、特定の時点に復元することもできます。

    <SimpleTab>
     <div label="Snapshot Restore">

    選択したバックアップ スナップショットから復元するには、次の手順を実行します。

    1.  **スナップショットの復元を**クリックします。
    2.  復元するバックアップ スナップショットを選択します。

    </div>
     <div label="Point-in-Time Restore">

    Premium インスタンスを特定の時点に復元するには、次の手順を実行します。

    1.  **ポイントインタイム復元を**クリックします。
    2.  復元したい日時を選択します。

    </div>
     </SimpleTab>

4.  **「次へ」**をクリックして、 **「新しいインスタンスへの復元」**ページに進みます。

5.  新しいTiDBインスタンスを復元用に設定します。手順は[新しいTiDBインスタンスを作成する](/tidb-cloud/premium/create-tidb-instance-premium.md)と同じです。

    > **注記：**
    >
    > 新しいインスタンスは、デフォルトでバックアップと同じクラウド プロバイダーとリージョンを使用します。

6.  復元プロセスを開始するには、 **「復元」**をクリックします。

    復元プロセスが開始されると、インスタンスのステータスは最初に**「作成中」**に変わります。作成が完了すると、 **「復元中」**に変わります。復元が完了してステータスが**「使用可能」**に変わるまで、インスタンスは利用できません。

### ごみ箱から復元 {#restore-from-recycle-bin}

削除したインスタンスをごみ箱から復元するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。右上にある**「ごみ箱」**をクリックします。

2.  **ごみ箱**ページで、復元する TiDB インスタンスを見つけます。

    -   **&gt;**ボタンをクリックしてインスタンスの詳細を展開します。
    -   目的のバックアップを見つけて、 **[アクション]**列の**[...]**をクリックし、 **[復元]**を選択します。

3.  **「復元」**ページで、 [新しいインスタンスに復元する](#restore-to-a-new-instance)と同じ手順に従って、バックアップを新しいインスタンスに復元します。

### 別のプランタイプからバックアップを復元する {#restore-backups-from-a-different-plan-type}

現在、AWS でホストされているTiDB Cloud Dedicated クラスターからのバックアップを新しいTiDB Cloud Premium インスタンスに復元することのみが可能です。

TiDB Cloud Dedicated クラスターによって生成されたバックアップを復元するには、次の手順に従います。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。右上の「 **...」**をクリックし、 **「別のプランから復元」**をクリックします。

2.  **「バックアップの選択」**ページで、対象のTiDB Cloud Dedicatedクラスターを含むプロジェクトを選択します。クラスターを選択し、復元するバックアップスナップショットを選択して、 **「次へ」**をクリックします。

    > **注記：**
    >
    > -   選択したプロジェクト内で、バックアップ スナップショットを含むクラスターが**アクティブ**または**削除済みの**ステータスになっていることを確認します。
    > -   スナップショットは、 TiDB Cloud Premium がサポートするリージョンに配置する必要があります。サポートされていないリージョンの場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)ご連絡いただき、 TiDB Cloud Premium の新しいリージョンを開設するか、別のバックアップスナップショットを選択してください。

3.  **「復元」**ページで、 [新しいインスタンスに復元する](#restore-to-a-new-instance)と同じ手順に従って、バックアップを新しいインスタンスに復元します。

### クラウドstorageからバックアップを復元する {#restore-backups-from-cloud-storage}

TiDB Cloud Premiumは、クラウドstorage（Amazon S3やAlibaba Cloud Object Storage Service（OSS）など）から新しいインスタンスへのバックアップの復元をサポートしています。この機能は、 TiDB Cloud DedicatedクラスターまたはTiDB Self-Managedクラスターから生成されたバックアップと互換性があります。

> **注記：**
>
> -   現在、復元がサポートされているのは、 **Amazon S3**と**Alibaba Cloud OSS**にあるバックアップのみです。
> -   バックアップは、storageバケットと同じクラウド プロバイダーによってホストされている新しいインスタンスにのみ復元できます。
> -   インスタンスとstorageバケットが異なるリージョンにある場合は、追加のリージョン間データ転送料金が適用される場合があります。

#### 手順 {#steps}

始める前に、バックアップ ファイルにアクセスするための十分な権限を持つアクセス キーとシークレット キーがあることを確認してください。

クラウドstorageからバックアップを復元するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。右上隅の「 **...」**をクリックし、 **「クラウドストレージから復元」を**クリックします。

2.  **[バックアップ保存場所の選択]**ページで、次の情報を入力します。

    -   **クラウド プロバイダー**: バックアップ ファイルが保存されるクラウド プロバイダーを選択します。

    -   **リージョン**: クラウド プロバイダーが Alibaba Cloud OSS の場合は、リージョンを選択します。

    -   **バックアップ ファイル URI** : バックアップ ファイルが含まれている最上位フォルダーの URI を入力します。

    -   **アクセス キー ID** : アクセス キー ID を入力します。

    -   **アクセス キー シークレット**: アクセス キー シークレットを入力します。

    > **ヒント：**
    >
    > storageバケットのアクセス キーを作成するには、 [AWS アクセスキーを使用して Amazon S3 アクセスを構成する](#configure-amazon-s3-access-using-an-aws-access-key)と[Alibaba Cloud OSSアクセスを構成する](#configure-alibaba-cloud-oss-access)参照してください。

3.  **[バックアップの検証] と [次へ]**をクリックします。

4.  検証が成功すると、 **「新しいインスタンスへの復元」**ページが表示されます。ページ上部に表示されるバックアップ情報を確認し、 [TiDB Cloud Premiumインスタンスを作成する](/tidb-cloud/premium/create-tidb-instance-premium.md)の手順に従ってバックアップを新しいインスタンスに復元します。

    バックアップ情報が正しくない場合は、 **「前へ」**をクリックして前のページに戻り、正しい情報を入力してください。

5.  バックアップを復元するには、 **「復元」**をクリックします。

## 制限事項 {#limitations}

現在、 TiDB Cloud Premium インスタンスでは手動バックアップはサポートされていません。

## 参考文献 {#references}

このセクションでは、Amazon S3 および Alibaba Cloud OSS へのアクセスを構成する方法について説明します。

### AWS アクセスキーを使用して Amazon S3 アクセスを構成する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成するには、AWS アカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセス キーを構成するには、次の手順を実行します。

1.  IAMユーザーとアクセスキーを作成します。

    1.  IAMユーザーを作成します。詳細については、 [AWSアカウントにIAMユーザーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。
    2.  AWS アカウント ID またはアカウントエイリアス、 IAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインします。
    3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーを管理する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)参照してください。

2.  IAMユーザーに権限を付与します。

    タスクに必要な権限のみを付与したポリシーを作成し、 IAMユーザーにアタッチします。TiDB TiDB Cloud Premiumインスタンスにデータを復元するには、 `s3:GetObject` 、 `s3:GetBucketLocation` 、 `s3:ListBucket`権限を付与します。

    以下は、 TiDB Cloud がAmazon S3 バケット内の特定のフォルダーからデータを復元できるようにするポリシーの例です。

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowGetBucketLocation",
                "Effect": "Allow",
                "Action": "s3:GetBucketLocation",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>"
            },
            {
                "Sid": "AllowListPrefix",
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>",
                "Condition": {
                    "StringLike": {
                        "s3:prefix": "<Your backup folder>/*"
                    }
                }
            },
            {
                "Sid": "AllowReadObjectsInPrefix",
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>/<Your backup folder>/*"
            }
        ]
    }
    ```

    上記のポリシーの`<Your S3 bucket name>`と`<Your backup folder>`実際のバケット名とバックアップディレクトリに置き換えてください。この設定は、必要なバックアップファイルへのアクセスのみを制限することで、最小権限の原則に従っています。

> **注記：**
>
> TiDB Cloudはアクセスキーを保存しません。セキュリティを維持するため、インポートまたはエクスポートタスクの完了後に[アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)実行してください。

### Alibaba Cloud OSSアクセスを構成する {#configure-alibaba-cloud-oss-access}

TiDB Cloudに Alibaba Cloud OSS バケットへのアクセスを許可するには、バケットの AccessKey ペアを作成する必要があります。

AccessKey ペアを構成するには、次の手順を実行します。

1.  RAMユーザーを作成し、AccessKeyペアを取得します。詳細については、 [RAMユーザーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)参照してください。

    **[アクセス モード]**セクションで、 **[永続的な AccessKey を使用してアクセスする]**を選択します。

2.  必要な権限を持つカスタムポリシーを作成します。詳細については、 [カスタムポリシーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)参照してください。

    -   **[効果]**セクションで、 **[許可]**を選択します。

    -   **[サービス]**セクションで、 **[オブジェクト ストレージ サービス]**を選択します。

    -   **「アクション」**セクションで、必要な権限を選択します。TiDB TiDB Cloudインスタンスにバックアップを復元するには、 `oss:ListObjects`と`oss:GetObject`権限を付与します。

        > **ヒント：**
        >
        > 復元操作のセキュリティを強化するために、バケット全体へのアクセスを許可するのではなく、バックアップファイルが保存されている特定のフォルダ ( `oss:Prefix` ) へのアクセスを制限することができます。

        次のJSON例は、復元タスクのポリシーを示しています。このポリシーは、特定のバケットとバックアップフォルダへのアクセスを制限します。

        ```json
        {
        "Version": "1",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": "oss:ListObjects",
            "Resource": "acs:oss:*:*:<Your bucket name>",
            "Condition": {
                "StringLike": {
                "oss:Prefix": "<Your backup folder>/*"
                }
            }
            },
            {
            "Effect": "Allow",
            "Action": "oss:GetObject",
            "Resource": "acs:oss:*:*:<Your bucket name>/<Your backup folder>/*"
            }
        ]
        }
        ```

    -   **リソース**セクションで、バケットとバケット内の特定のオブジェクトを選択します。

3.  カスタム ポリシーを RAM ユーザーに添付します。

    詳細については[RAMユーザーに権限を付与する](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)参照してください。
