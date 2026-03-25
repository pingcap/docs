---
title: Back Up and Restore TiDB Cloud Premium Data
summary: TiDB Cloud Premiumインスタンスのバックアップと復元方法を学びましょう。
aliases: ['/ja/tidbcloud/restore-deleted-tidb-cluster']
---

# TiDB Cloud Premium データのバックアップと復元 {#back-up-and-restore-tidb-cloud-premium-data}

このドキュメントでは、 TiDB Cloud Premiumインスタンス上のデータのバックアップと復元方法について説明します。TiDB TiDB Cloud Premiumは、自動バックアップと手動バックアップの両方をサポートしており、必要に応じてバックアップデータを新しいインスタンスに復元できます。

バックアップファイルは、以下のソースから生成される可能性があります。

-   アクティブなTiDB Cloud Premiumインスタンス
-   削除されたTiDB Cloud Premiumインスタンスのバックアップ用のごみ箱

> **ヒント：**
>
> -   TiDB Cloud Dedicatedクラスターでデータをバックアップおよび復元する方法については、 [TiDB Cloud Dedicatedデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。
> -   TiDB Cloud StarterまたはTiDB Cloud Essentialクラスターでデータをバックアップおよび復元する方法については、 [TiDB Cloud StarterまたはEssentialデータのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)参照してください。

## バックアップページをビュー {#view-the-backup-page}

1.  [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページ目で、対象インスタンスの名前をクリックすると、その概要ページに移動します。

    > **ヒント：**
    >
    > 左上隅にあるコンボボックスを使用して、組織とインスタンスを切り替えることができます。

2.  左側のナビゲーションペインで、 **[データ]** &gt; **[バックアップ]**をクリックします。

## 自動バックアップ {#automatic-backups}

TiDB Cloud Premiumは、本番環境向けに強化された自動バックアップ機能を提供します。高頻度スナップショットとログバックアップを組み合わせることで、データの信頼性を確保します。

### 自動バックアップポリシー {#automatic-backup-policies}

TiDB Cloud Premiumインスタンスは、以下の表に示すように、多層バックアップアーキテクチャを使用してデータを保護します。

| バックアップの種類          | 保存期間 | 粒度を復元する                                                                     |
| ------------------ | ---- | --------------------------------------------------------------------------- |
| **特定時点リカバリ（PITR）** | 7日間  | 7日間の期間内の任意の時点に復元します。                                                        |
| **時間ごとのスナップショット**  | 7日間  | 過去7日以内に生成された任意の1時間ごとのスナップショットから復元します。                                       |
| **日次スナップショット**     | 33日間 | 過去33日以内に生成された任意のデイリースナップショットから復元できます。デフォルトでは、デイリースナップショットはUTCの00:00に取得されます。 |

### バックアップ実行ルール {#backup-execution-rules}

-   **バックアップサイクル**： TiDB Cloud Premiumインスタンスは、1時間ごとおよび1日ごとの自動バックアップを実行します。

-   **バックアップスケジュール**：

    -   毎時バックアップは、毎時開始時に実行されます。
    -   毎日のバックアップは、毎日00:00（UTC）に実行されます。
    -   現在、バックアップスケジュールをカスタマイズまたは管理することはできません。

-   **保持動作**：バックアップは保持期間（7日間または33日間）を超えると自動的に期限切れとなり、復元できなくなります。

> **注記：**
>
> -   自動バックアップのstorageコストは、バックアップデータの量と保存期間によって異なります。
> -   バックアップの保持期間をデフォルトの制限を超えて延長するには、 [TiDB Cloudサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)連絡してください。

### バックアップファイルを削除する {#delete-backup-files}

TiDB Cloud Premiumインスタンスの既存のバックアップファイルを削除するには、以下の手順を実行してください。

1.  インスタンスの[**バックアップ**](#view-the-backup-page)ページ目に移動してください。

2.  削除したいバックアップファイルを見つけて、 **[アクション]**列の**[...]** &gt; **[削除]**をクリックします。

## 手動バックアップ {#manual-backups}

TiDB Cloud Premiumは、自動バックアップに加えて、手動バックアップもサポートしています。手動バックアップは、管理された確実な復元ポイントを提供します。システムアップグレード、重要なデータの削除、元に戻せないスキーマや構成の変更など、リスクの高い操作を実行する前に、手動バックアップを作成することを強くお勧めします。

### 主な特徴 {#key-characteristics}

-   **保持と削除**：自動バックアップとは異なり、手動バックアップは保持ポリシーに基づいて自動的に削除されません。明示的に削除するまで保持されます。インスタンスを削除すると、その手動バックアップはごみ箱に移動し、手動で削除するまでそこに残ります。

-   **保存場所**：手動バックアップは、TiDBが管理するクラウドstorageに保存されます。

-   **コスト**：手動バックアップは長期保存されるため、追加料金が発生する。

-   **制限事項**：手動バックアップは、ポイントインタイムリカバリ（PITR）や部分バックアップ（テーブルレベルまたはデータベースレベルのバックアップなど）をサポートしていません。手動バックアップを既存のインスタンスに復元することはできません。復元操作ごとに新しいインスタンスが作成されます。

-   **権限**： `Organization Owner`と`Instance Manager`権限を持つユーザーは手動バックアップを作成できます。システム管理の手動バックアップを復元できるのは`Organization Owner`権限を持つユーザーのみです。

### 手動バックアップを作成する {#create-a-manual-backup}

1.  インスタンスの[**バックアップ**](#view-the-backup-page)ページ目に移動してください。

2.  右上隅の「 **…」**をクリックし、次に**「手動バックアップ」**をクリックします。

3.  操作を確認してください。バックアップはTiDB Cloudに保存され、**バックアップリスト**に表示されます。

TiDB Cloudコンソールでは、外部storageの認証情報を入力することなく、手動バックアップを直接復元できます。

## 復元する {#restore}

TiDB Cloudは、偶発的なデータ損失や破損が発生した場合にデータを復旧するための復元機能を提供します。アクティブなインスタンスのバックアップ、またはごみ箱から削除されたインスタンスから復元できます。

### 復元モード {#restore-mode}

TiDB Cloudは、インスタンスのスナップショット復元と特定時点への復元をサポートしています。

-   **スナップショット復元**：特定のバックアップスナップショットからインスタンスを復元します。この方法は、自動バックアップと手動バックアップの両方の復元に使用できます。**バックアップ一覧**では、手動バックアップには**「手動」**タイプと**「永続的」有効**期限ステータスが表示されます。

-   **特定時点への復元**：インスタンスを特定の時点の状態に復元します。

    -   プレミアムインスタンス：過去7日間の任意の時点に復元できますが、インスタンス作成時刻より前、または現在時刻の1分前より後の時点には復元できません。なお、手動バックアップではPITRはサポートされていません。

### 目的地を復元する {#restore-destination}

TiDB Cloudは、新しいインスタンスへのデータ復元をサポートしています。

### 新しいインスタンスに復元する {#restore-to-a-new-instance}

データを新しいインスタンスに復元するには、以下の手順に従ってください。

1.  インスタンスの[**バックアップ**](#view-the-backup-page)ページ目に移動してください。

2.  **「復元」**をクリックしてください。

3.  **「バックアップの選択」**ページで、使用する**復元モード**を選択します。特定のバックアップスナップショットから復元することも、特定の時点に復元することもできます。

    <SimpleTab>
     <div label="Snapshot Restore">

    選択したバックアップスナップショットから復元するには、次の手順を実行します。

    1.  **「スナップショット復元」**をクリックします。
    2.  復元元のバックアップスナップショットを選択してください。

    </div>
     <div label="Point-in-Time Restore">

    Premiumインスタンスを特定の時点に復元するには、以下の手順を実行してください。

    1.  **「特定時点への復元」**をクリックします。
    2.  復元したい日時を選択してください。

    </div>
     </SimpleTab>

4.  **「次へ」**をクリックして、 **「新しいインスタンスへの復元」**ページに進んでください。

5.  新しい TiDB インスタンスを復元用に構成します。手順は[新しいTiDBインスタンスを作成しています](/tidb-cloud/premium/create-tidb-instance-premium.md)と同じです。

    > **注記：**
    >
    > 新しいインスタンスは、デフォルトではバックアップと同じクラウドプロバイダーとリージョンを使用します。

6.  **「復元」**をクリックして復元プロセスを開始してください。

    復元処理が開始されると、インスタンスの状態は最初に**「作成中」**に変わります。作成が完了すると、 **「復元中」**に変わります。復元が完了し、状態が**「利用可能」**に変わるまで、インスタンスは利用できません。

### ごみ箱から復元 {#restore-from-recycle-bin}

ごみ箱から削除したインスタンスを復元するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。右上隅に**あるごみ箱**をクリックします。

2.  **ごみ箱**ページで、復元したいTiDBインスタンスを探します。

    -   インスタンスの詳細を表示するには、 **&gt;**ボタンをクリックしてください。
    -   目的のバックアップを見つけて、 **[アクション]**列の**[...]**をクリックし、 **[復元]**を選択します。

3.  **復元**ページで、手順[新しいインスタンスに復元する](#restore-to-a-new-instance)と同じ手順に従って、バックアップを新しいインスタンスに復元します。

### 別のプランタイプからバックアップを復元する {#restore-backups-from-a-different-plan-type}

現在、AWS上でホストされているTiDB Cloud Dedicatedクラスタから新しいTiDB Cloud Premiumインスタンスへのバックアップ復元のみが可能です。

TiDB Cloud Dedicatedクラスターによって生成されたバックアップを復元するには、次の手順に従ってください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。右上隅の**...**をクリックし、次に**「別のプランから復元」**をクリックします。

2.  **「バックアップの選択」**ページで、対象のTiDB Cloud Dedicatedクラスターを含むプロジェクトを選択します。クラスターを選択し、復元するバックアップ スナップショットを選択してから、 **「次へ」**をクリックします。

    > **注記：**
    >
    > -   バックアップスナップショットを含むクラスターが、選択したプロジェクト内で**「アクティブ」**または**「削除済み」の**いずれかの状態になっていることを確認してください。
    > -   スナップショットは、 TiDB Cloud Premiumがサポートするリージョン内に配置する必要があります。リージョンがサポートされていない場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)連絡してTiDB Cloud Premium用の新しいリージョンを開設するか、別のバックアップスナップショットを選択してください。

3.  **復元**ページで、手順[新しいインスタンスに復元する](#restore-to-a-new-instance)と同じ手順に従って、バックアップを新しいインスタンスに復元します。

### クラウドstorageからバックアップを復元する {#restore-backups-from-cloud-storage}

TiDB Cloud Premiumは、クラウドstorage（Amazon S3やAlibaba Cloud Object Storage Service（OSS）など）から新しいインスタンスへのバックアップ復元をサポートしています。この機能は、 TiDB Cloud DedicatedクラスタまたはTiDB Self-Managedクラスタから生成されたバックアップと互換性があります。

> **注記：**
>
> -   現在、復元対象としてサポートされているのは、 **Amazon S3**および**Alibaba Cloud OSS**に保存されているバックアップのみです。
> -   バックアップの復元は、storageバケットと同じクラウドプロバイダーがホストする新しいインスタンスにのみ可能です。
> -   インスタンスとstorageバケットが異なるリージョンに配置されている場合、リージョン間データ転送料金が別途発生する可能性があります。

#### 手順 {#steps}

開始する前に、バックアップファイルにアクセスするための十分な権限を持つアクセスキーとシークレットキーを用意してください。

クラウドstorageからバックアップを復元するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。右上隅の**...**をクリックし、次に**「クラウド ストレージから復元」**をクリックします。

2.  **「バックアップ保存場所の選択」**ページで、以下の情報を入力してください。

    -   **クラウドプロバイダー**：バックアップファイルが保存されるクラウドプロバイダーを選択してください。

    -   **リージョン**：クラウドプロバイダーがAlibaba Cloud OSSの場合は、リージョンを選択してください。

    -   **バックアップファイルURI** ：バックアップファイルが格納されている最上位フォルダのURIを入力してください。

    -   **アクセスキーID** ：アクセスキーIDを入力してください。

    -   **アクセスキーシークレット**：アクセスキーシークレットを入力してください。

    > **ヒント：**
    >
    > storageバケットのアクセスキーを作成するには、 [AWSアクセスキーを使用してAmazon S3へのアクセスを設定する](#configure-amazon-s3-access-using-an-aws-access-key)と[Alibaba Cloud OSSへのアクセスを設定する](#configure-alibaba-cloud-oss-access)参照してください。

3.  **「バックアップの確認」をクリックし、「次へ」を**クリックします。

4.  検証が成功すると、 **「新しいインスタンスへの復元」**ページが表示されます。ページ上部に表示されるバックアップ情報を確認し、手順[TiDB Cloud Premiumインスタンスを作成する](/tidb-cloud/premium/create-tidb-instance-premium.md)に従ってバックアップを新しいインスタンスに復元してください。

    バックアップ情報が間違っている場合は、 **「前へ」**をクリックして前のページに戻り、正しい情報を入力してください。

5.  バックアップを復元するには、 **「復元」**をクリックしてください。

## 参考文献 {#references}

このセクションでは、Amazon S3とAlibaba Cloud OSSへのアクセス設定方法について説明します。

### AWSアクセスキーを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成する際は、AWSアカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセスキーを設定するには、以下の手順に従ってください。

1.  IAMユーザーとアクセスキーを作成します。

    1.  IAMユーザーを作成します。詳細については、 [AWSアカウントにIAMユーザーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。
    2.  AWSアカウントIDまたはアカウントエイリアス、およびIAMユーザー名とパスワードを使用して、 [IAMコンソール](https://console.aws.amazon.com/iam)にサインインしてください。
    3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーを管理する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)参照してください。

2.  IAMユーザーに権限を付与します。

    タスクに必要な権限のみを含むポリシーを作成し、それをIAMユーザーに割り当てます。TiDB TiDB Cloud Premiumインスタンスにデータを復元するには、 `s3:GetObject` `s3:GetBucketLocation`および`s3:ListBucket`権限を付与します。

    以下は、 TiDB CloudがAmazon S3バケット内の特定のフォルダからデータを復元できるようにするポリシーの例です。

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

    上記のポリシーにおいて、 `<Your S3 bucket name>`と`<Your backup folder>`実際のバケット名とバックアップディレクトリに置き換えてください。この設定は、必要なバックアップファイルのみにアクセスを制限することで、最小権限の原則に従っています。

> **注記：**
>
> TiDB Cloud はアクセス キーを保存しません。セキュリティを維持するため、インポートまたはエクスポート タスクが完了した後、 [アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)行ってください。

### Alibaba Cloud OSSへのアクセスを設定する {#configure-alibaba-cloud-oss-access}

TiDB CloudにAlibaba Cloud OSSバケットへのアクセス権を付与するには、そのバケット用のアクセスキーペアを作成する必要があります。

アクセスキーペアを設定するには、以下の手順に従ってください。

1.  RAMユーザーを作成し、アクセスキーペアを取得します。詳細については、 [RAMユーザーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)参照してください。

    **アクセスモードの**セクションで、 **「永続的なアクセスキーを使用してアクセスする」を**選択します。

2.  必要な権限を持つカスタムポリシーを作成します。詳細については、 [カスタムポリシーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)参照してください。

    -   **「効果」**セクションで**「許可」**を選択します。

    -   「**サービス」**セクションで、 **「オブジェクトストレージサービス」**を選択します。

    -   **「アクション」**セクションで、必要な権限を選択します。TiDB TiDB Cloudインスタンスにバックアップを復元するには、権限`oss:ListObjects`と`oss:GetObject`を付与してください。

        > **ヒント：**
        >
        > 復元操作のセキュリティを強化するために、バケット全体へのアクセスを許可するのではなく、バックアップファイルが保存されている特定のフォルダー（ `oss:Prefix` ）へのアクセスを制限することができます。

        以下の JSON の例は、復元タスクのポリシーを示しています。このポリシーは、特定のバケットとバックアップフォルダへのアクセスを制限します。

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

    -   **リソース**セクションで、バケットと、そのバケット内の特定のオブジェクトを選択します。

3.  カスタムポリシーをRAMユーザーに割り当てます。

    詳細については、 [RAMユーザーに権限を付与する](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)参照してください。
