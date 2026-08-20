---
title: "TiDB Cloud Premium Database Audit Logging"
summary: TiDB Cloud Premiumでインスタンスを監査する方法を学びましょう。
---

# TiDB Cloud Premiumデータベース監査ログ {#tidb-cloud-premium-database-audit-logging}

TiDB Cloudは、実行されたSQLステートメントなど、データベースへのユーザーアクセスアクティビティを記録する監査ログ機能を提供します。

組織のユーザーアクセスポリシーやその他の情報セキュリティ対策の有効性を評価するには、データベース監査ログを定期的に分析することがセキュリティ上のベストプラクティスです。

監査ログ機能は**デフォルトでは無効になっています**。TiDB Cloud Premiumインスタンスを監査するには、まず監査ログを有効にしてから、監査フィルタールールを設定する必要があります。

> **Note:**
>
> 監査ログはインスタンスのリソースを消費するため、インスタンスの監査を行うかどうかは慎重に検討してください。

## 前提条件 {#prerequisites}

-   あなたはTiDB Cloud Premiumインスタンスを使用しています。

    > **Note:**
    >
    > -   TiDB Cloud Starterでは、データベース監査ログは利用できません。
    > -   TiDB Cloud Essentialについては、 [TiDB Cloud Essentialのデータベース監査ログ機能 (PREVIEW)](/tidb-cloud/essential-database-audit-logging.md)を参照してください。
    > -   TiDB Cloud Dedicatedについては、 [TiDB Cloud Dedicatedデータベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)を参照してください。

-   組織内で`Organization Owner`ロールが付与されている必要があります。付与されていない場合、 TiDB Cloudコンソールでデータベース監査関連のオプションは表示されません。

## 監査ログを有効にする {#enable-audit-logging}

TiDB Cloudは、 TiDB Cloud Premiumインスタンスの監査ログをクラウドストレージサービスに記録することをサポートしています。データベース監査ログを有効にする前に、インスタンスが配置されているクラウドプロバイダーでクラウドストレージサービスを設定してください。

### AWS 上の TiDB の監査ログを有効にする {#enable-audit-logging-for-tidb-on-aws}

AWSの監査ログを有効にするには、以下の手順を実行してください。

#### ステップ1. Amazon S3バケットを作成する {#step-1-create-an-amazon-s3-bucket}

TiDB Cloudが監査ログを書き込む宛先として、組織が所有するAWSアカウント内のAmazon S3バケットを指定してください。

> **Note:**
>
> AWS S3バケットでオブジェクトロックを有効にしないでください。オブジェクトロックを有効にすると、 TiDB Cloudが監査ログファイルをS3にプッシュできなくなります。

詳細については、AWS ユーザーガイドの[汎用バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。

#### ステップ2. Amazon S3へのアクセスを設定する {#step-2-configure-amazon-s3-access}

1.  監査ログを有効にするTiDB Cloud PremiumインスタンスのTiDB CloudアカウントIDと外部IDを取得してください。

    1.  TiDB Cloudコンソールで、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    2.  対象インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** > **DB Audit Logging**をクリックします。

    3.  **DB Audit Logging**ページで、右上隅にある**「有効にする」**をクリックします。

    4.  **データベース監査ログストレージコンフィグレーション**ダイアログで、 **AWS IAM Policy Settings**セクションを探し、後で使用するために**TiDB Cloud Account ID**と**TiDB Cloud External ID**を記録してください。

2.  AWS マネジメント コンソールで、 **IAM** > **Access Management** > **Policies**に移動し、 `s3:PutObject`書き込み専用権限を持つストレージバケット ポリシーが存在するかどうかを確認します。

    -   はいの場合、後で使用するために、一致したストレージバケットポリシーを記録してください。
    -   そうでない場合は、 **IAM** > **Access Management** > **Policies** > **Create Policy**に移動し、次のポリシー テンプレートに従ってバケット ポリシーを定義します。

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

        テンプレートでは、 `<Your S3 bucket ARN>`は監査ログファイルが書き込まれる S3 バケットの Amazon リソース ネーム (ARN) です。S3 バケットの**[プロパティ]**タブに移動し、 **Bucket Overview**領域で ARN の値を取得できます。 `"Resource"`フィールドでは、ARN の後に`/*`を追加する必要があります。たとえば、ARN が`arn:aws:s3:::tidb-cloud-test`の場合、 `"Resource"`フィールドの値を`"arn:aws:s3:::tidb-cloud-test/*"`に設定する必要があります。

3.  **IAM** > **Access Management** > **Roles**に移動し、以前に記録したTiDB Cloudアカウント ID と外部 ID に対応する信頼エンティティを持つロールが既に存在するかどうかを確認します。

    -   はいの場合、後で使用するために一致した役割を記録してください。
    -   そうでない場合は、 **Create role**をクリックし、信頼エンティティタイプとして**Another AWS account**を選択してから、 **Account ID**フィールドにTiDB CloudアカウントIDの値を入力します。次に、 **Require External ID**オプションを選択し、**External ID**フィールドにTiDB Cloud外部IDの値を入力します。

4.  **IAM** > **Access Management** > **Roles**で、前の手順で確認したロール名をクリックして**概要**ページに移動し、以下の手順を実行します。

    1.  **「アクセス許可」**タブで、 `s3:PutObject`書き込み専用アクセス許可を持つ記録済みポリシーがロールに添付されているかどうかを確認します。添付されていない場合は、 **Attach Policies**を選択し、必要なポリシーを検索して、 **Attach Policy**をクリックします。
    2.  **概要**ページに戻り、**Role ARN**値をクリップボードにコピーしてください。

#### ステップ3．監査ログを有効にする {#step-3-enable-audit-logging}

TiDB Cloudコンソールで、 TiDB CloudアカウントIDと外部IDの値を取得した**「データベース監査ログストレージコンフィグレーション」**ダイアログに戻り、以下の手順を実行します。

1.  **Bucket URI**フィールドに、監査ログファイルが書き込まれるS3バケットのURIを入力してください。

2.  **Bucket Region**ドロップダウンリストから、バケットが配置されているAWSリージョンを選択します。

3.  **[Role ARN]**フィールドに、[ステップ2. Amazon S3へのアクセスを設定する](#step-2-configure-amazon-s3-access)。

4.  **Test Connection and Next**をクリックして、 TiDB Cloudがバケットにアクセスして書き込みできるかどうかを確認します。

    **The connection is successful**と表示されます。そうでない場合は、アクセス設定を確認してください。

5.  インスタンスの監査ログを有効にするには、 **「有効にする」**をクリックしてください。

    TiDB Cloudは、指定されたインスタンスの監査ログをAmazon S3バケットに書き込む準備ができています。

> **Note:**
>
> -   監査ログを有効にした後、バケットURI、場所、またはARNに変更を加えた場合は、 TiDB Cloudがバケットに接続できることを確認するために、再度**Test Connection**をクリックする必要があります。その後、 **「有効にする」**をクリックして変更を適用してください。
> -   TiDB CloudによるAmazon S3へのアクセス権を削除するには、AWSマネジメントコンソールでこのインスタンスに付与されている信頼ポリシーを削除するだけです。

<CustomContent language="en,zh">

### Alibaba Cloud 上の TiDB の監査ログを有効にする {#enable-audit-logging-for-tidb-on-alibaba-cloud}

Alibaba Cloud 上の TiDB クラウドでデータベース監査ログを有効にするには、以下の手順を実行してください。

#### ステップ1. OSSバケットを作成する {#step-1-create-an-oss-bucket}

TiDB Cloudが監査ログを書き込む宛先として、組織が所有するAlibaba Cloudアカウントにオブジェクトストレージサービス（OSS）バケットを作成します。

詳細については、Alibaba Cloud Storage ドキュメントの[バケットを作成する](https://www.alibabacloud.com/help/en/oss/user-guide/create-a-bucket-4)を参照してください。

#### ステップ2. OSSアクセスを設定する {#step-2-configure-oss-access}

この手順では、 TiDB Cloudが監査ログをOSSバケットに書き込めるように、Alibaba Cloud RAMの権限を設定します。OSSバケットとRAMロールが異なるAlibaba Cloudアカウントにある場合は、このセクションのアカウント間設定手順に従ってください。

##### 標準OSSバケット構成 {#standard-oss-bucket-configuration}

監査ログを保存するOSSバケットと、そのOSSバケットにアクセスするロールが同じクラウドアカウントにある場合は、OSSアクセスを次のように構成します。

1.  監査ログを有効にしたいTiDB Cloud PremiumインスタンスのAlibaba CloudサービスアカウントIDを取得してください。

    1.  TiDB Cloudコンソールで、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。
    2.  対象インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** > **DB Audit Logging**をクリックします。
    3.  **DB Audit Logging**ページで、右上隅にある**「有効にする」**をクリックします。
    4.  **データベース監査ログストレージコンフィグレーション**ダイアログで、 **Alibaba Cloud RAM Policy Settings**セクションを探し、後で使用するために**TiDB Cloud Account ID**と**TiDB Cloud External ID**を記録してください。

2.  Alibaba Cloud コンソールで、 **[RAM]** > **[権限]** > **[ポリシー]**に移動し、監査ログ OSS バケットに対して`oss:PutObject`書き込み専用権限を持つポリシーが既に存在するかどうかを確認します。

    -   はいの場合、後で使用するためにポリシー名を記録してください。

    -   そうでない場合は、 **Create Policy**をクリックし、以下のポリシーテンプレートを使用してポリシーを定義してください。

        ```json
        {
        "Version": "1",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": [
                "oss:PutObject"
            ],
            "Resource": "acs:oss:*:*:<Your-Bucket-Name>/*"
            }
        ]
        }
        ```

    `<Your-Bucket-Name>` TiDB Cloud が監査ログを書き込む OSS バケットの名前に置き換えてください。たとえば、バケット名が`auditlog-bucket`の場合は、 `"Resource": "acs:oss:*:*:auditlog-bucket/*"`を使用します。

3.  Alibaba Cloudコンソールで、 **[RAM]** > **[ID]** > **[ロール]**に移動し、**trusted entity**が以前に記録したTiDB CloudアカウントIDと外部IDに一致するロールが既に存在するかどうかを確認します。

    -   はいの場合、後で使用するために役割名を記録してください。

    -   そうでない場合は、以下の手順に従って**Create Role**をクリックしてください。

        1.  役割作成ページで、 **[ポリシーエディターに切り替える]**をクリックします。
        2.  **「プリンシパル」**で**Cloud Account**を選択し、フィールドに**TiDB Cloud Account Id**を入力します。
        3.  **「アクション」**の下にあるドロップダウンリストから**「sts:AssumeRole」**を選択します。
        4.  **Add condition**をクリックし、次のように条件を設定します。
            -   **キーを**`sts:ExternalId`に設定します。
            -   **演算子を**`StringEquals`に設定します。
            -   **TiDB Cloud外部ID**に**値**を設定します。
        5.  **OK**をクリックして**Create Role**ダイアログを開きます。
        6.  **Role Name**フィールドに役割名を入力し、 **OK**をクリックして役割を作成します。

4.  役割が作成されたら、 **[権限]**タブに移動して、 **Grant Permission**をクリックします。

    ダイアログで、以下の設定を構成してください。

    -   **Resource Scope**については、 **「アカウント」**を選択してください。
    -   **「ポリシー」**フィールドで、以前に作成したOSS書き込みポリシーを選択します。
    -   **Grant Permissions**をクリックしてください。

5.  後で使用するために、**Role ARN** (例: `acs:ram::<Your-Account-ID>:role/tidb-cloud-audit-role` ) をコピーしてください。

##### クロスアカウントOSSバケット構成 {#cross-account-oss-bucket-configuration}

監査ログを保存するOSSバケットと、そのOSSバケットにアクセスするロールが異なるクラウドアカウントにある場合、設定プロセスは若干異なります。

1.  RAMポリシーを設定します。

    RAMポリシーを作成する際は、**リソース**フィールドに2番目のユーザーアカウントの情報を追加する必要があります。以下のJSONスクリプトを使用してポリシーを定義してください。

    ```json
    {
      "Version": "1",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "oss:PutObject",
          "Resource": "acs:oss:*:<User Account 2>:<bucket-name>/*"
        }
      ]
    }
    ```

2.  バケットポリシーを設定します。

    さらに、宛先OSSバケットにバケットポリシーを設定し、別のアカウントから引き受けたロールがアクセスできるようにする必要があります。以下の設定を使用してください。

    ```json
    {
        "Version": "1",
        "Statement": [
            {
                "Action": [
                    "oss:PutObject"
                ],
                "Effect": "Allow",
                "Principal": [
                    "arn:sts::<User Account 1>:assumed-role/<role-name>/*"
                ],
                "Resource": [
                    "acs:oss:*:<User Account 2>:<bucket-name>/*"
                ]
            }
        ]
    }
    ```

#### ステップ3．監査ログを有効にする {#step-3-enable-audit-logging}

TiDB Cloudコンソールで、 TiDB CloudアカウントIDを取得した**「データベース監査ログストレージコンフィグレーション」**ダイアログに戻り、以下の手順を実行します。

1.  **Bucket URI**フィールドに、OSSバケットのURIを入力します。例： `oss://tidb-cloud-audit-log` 。

2.  **Bucket Region**フィールドで、バケットが配置されているAlibaba Cloudリージョンを選択します（ TiDB Cloud Premiumインスタンスのリージョンと一致させることをお勧めします）。

3.  **[Role ARN]**フィールドに、[ステップ2. OSSアクセスを設定する](#step-2-configure-oss-access)。

4.  **Test Connection**をクリックして、 TiDB CloudがOSSバケットにアクセスして書き込みできるかどうかを確認してください。

    -   接続が成功すると、 **The connection is successful**と表示されます。
    -   そうでない場合は、OSSバケットのアクセス許可、RAMロールの設定、およびポリシーを確認してください。

5.  インスタンスの監査ログを有効にするには、 **「有効にする」**をクリックしてください。

    TiDB Cloudは、指定されたインスタンスの監査ログをOSSバケットに書き込む準備ができています。

> **Note:**
>
> -   監査ログを有効にした後、バケットのURIまたは場所に変更を加えた場合は、 TiDB Cloudがバケットに接続できることを確認するために、再度**Test Connection**をクリックする必要があります。その後、 **「有効にする」**をクリックして変更を適用してください。
> -   TiDB CloudによるOSSバケットへのアクセス権を削除するには、Alibaba Cloudコンソールでこのインスタンスに付与されている信頼ポリシーを削除してください。

</CustomContent>

## データベース監査ログ設定を構成する {#configure-database-audit-logging-settings}

クラウドプロバイダーのストレージを設定した後、データベース監査ログ設定の手順を完了します。

1. ログファイルのローテーションポリシーを設定します。

    ファイルサイズまたは時間間隔に基づいて監査ログファイルをローテーションできます。いずれかの条件が満たされると、TiDB Cloud は新しい監査ログファイルを生成します。

2. ログのリダクションを設定します。

    ログのリダクションはデフォルトで有効になっています。有効にすると、SQL テキスト内の機密情報は監査ログで `?` に置き換えられます。

3. **Save and Enable** をクリックして、設定を適用し、監査ログを有効にします。

> **Note:**
>
> ログのリダクションを無効にすると、クラウドストレージに書き込まれる監査ログファイルに機密情報が含まれる可能性があります。潜在的なセキュリティリスクがあるため、この設定は推奨されません。

## 監査フィルタルールを指定します {#specify-audit-filter-rules}

監査ログを有効にした後、どのユーザーアクセスイベントをキャプチャして監査ログに書き込むかを制御するために、監査フィルタルールを指定する必要があります。フィルタルールが指定されていない場合、 TiDB Cloudは何もログに記録しません。

インスタンスの監査フィルタルールを指定するには、次の手順を実行します。

1.  **DB Audit Logging**ページで、 **「ログフィルタルール」**セクションの**Add Filter Rule**をクリックして、監査フィルタルールを追加します。

2. **Add Filter Rule** ダイアログで、次の項目を設定します:

    - **Filter Name**: フィルタルールの名前を入力します。
    - **SQL User**: SQL ユーザーを `<user>@<host>` 形式で入力します。ユーザー名とホスト名では、`%` を使用して 0 文字以上の任意の文字に一致させることができ、`_` を使用してちょうど 1 文字に一致させることができます。`@` 記号と `<host>` は省略可能です。
    - **Filter Events**: ログに記録するイベントを選択します。サポートされているフィルタイベントについては、[監査フィルタイベント](#audit-filter-events) を参照してください。

3. **Confirm** をクリックしてフィルタルールを追加します。

> **Note:**
>
> -   監査ログはインスタンスのリソースを消費するため、フィルタルールを指定する際には注意が必要です。リソース使用量を最小限に抑えるには、可能な限り、監査ログを特定のユーザーとイベントに限定するフィルタルールを指定してください。

## 監査ログを確認する {#view-audit-logs}

TiDB Cloudはデフォルトではデータベース監査ログファイルをストレージサービスに保存するため、ストレージサービスから監査ログ情報を読み取る必要があります。

TiDB Cloudの監査ログは、インスタンスID、内部ID、およびログ作成日が完全修飾ファイル名に組み込まれた読み取り可能なテキストファイルです。

例えば、 `13796619446086334065/tidb-5m5z34/tidb-audit-2022-04-21T18-16-29.529.log`のようになります。この例では、 `13796619446086334065`はインスタンス ID を示し、 `tidb-5m5z34`は内部 ID を示します。

## 監査ログを無効にする {#disable-audit-logging}

インスタンスの監査を停止したい場合は、インスタンスのページに移動し、 **[設定]** > **Audit Settings**をクリックして、右上隅の監査設定を**[無効]**に切り替えます。

> **Note:**
>
> ログファイルのサイズが10MiBに達するたびに、ログファイルはクラウドストレージバケットにプッシュされます。そのため、監査ログを無効にした後は、サイズが10MiB未満のログファイルは自動的にクラウドストレージバケットにプッシュされません。この状況でログファイルを取得するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## 監査フィルタイベント {#audit-filter-events}

次の表は、データベース監査ログのすべてのイベントクラスを示しています。

| イベントクラス   | 説明                                                                                      | 親クラス   |
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
| `AUDIT_FUNC_CALL` | TiDB Cloud データベース監査に関連するシステム関数の呼び出しに関するすべての操作を記録します        | `AUDIT`       |
| `AUDIT_SET_SYS_VAR` | システム変数の設定に関するすべての操作を記録します        | `AUDIT`       |

## 監査ログフィールド {#audit-logging-fields}

TiDB Cloudは、監査ログ内の各データベースイベントレコードに対して、以下のフィールドを提供します。

### 一般情報 {#general-information}

すべての監査ログレコードには、以下のフィールドが含まれています。

| フィールド              | 説明                                         |
| --------------- | ------------------------------------------ |
| `ID`            | 監査記録の一意の識別子。                               |
| `EVENT`         | 監査記録のイベントクラス。複数のイベントクラスはカンマで区切られます（ `,` ）。 |
| `USER`          | 操作を実行したユーザーの名前。                            |
| `ROLES`         | 操作実行時にユーザーに割り当てられた役割。                      |
| `CONNECTION_ID` | ユーザーの接続を識別する識別子。                           |
| `TABLES`        | 操作中にアクセスされたテーブル。                           |
| `STATUS_CODE`   | 操作のステータスコード。 `1`は成功、 `0`は失敗を示します。          |
| `REASON`        | 操作のエラーメッセージ。エラーが発生した場合にのみ記録されます。           |

### SQLステートメント情報 {#sql-statement-information}

イベントクラスが`QUERY`または`QUERY`のサブクラスである場合、監査ログには次のフィールドが含まれます。

| フィールド               | 説明                                                                         |
| ---------------- | -------------------------------------------------------------------------- |
| `CURRENT_DB`     | 現在使用しているデータベースの名前。                                                         |
| `SQL_TEXT`       | 実行されたSQL文。監査ログのマスキングが有効になっている場合は、マスキングされた文が記録されます。                         |
| `EXECUTE_PARAMS` | `EXECUTE`ステートメントに渡されるパラメータ。イベントクラスに`EXECUTE`が含まれ、かつ編集が無効になっている場合にのみ記録されます。 |
| `AFFECTED_ROWS`  | SQL ステートメントによって影響を受けた行数。イベント クラスに`QUERY_DML`が含まれている場合にのみ記録されます。            |

### 接続情報 {#connection-information}

イベントクラスが`CONNECTION`または`CONNECTION`のサブクラスである場合、監査ログには次のフィールドが含まれます。

| フィールド                | 説明                                                  |
| ----------------- | --------------------------------------------------- |
| `CURRENT_DB`      | 現在のデータベースの名前。イベントクラスに`DISCONNECT`が含まれている場合は記録されません。 |
| `CONNECTION_TYPE` | 接続タイプ（ソケット、Unixソケット、SSL/TLSなど）。                     |
| `PID`             | 現在の接続のプロセスID。                                       |
| `SERVER_VERSION`  | 接続されているTiDBサーバーのバージョン。                              |
| `SSL_VERSION`     | 使用されているSSLのバージョン。                                   |
| `HOST_IP`         | 接続されたTiDBサーバーのIPアドレス。                               |
| `HOST_PORT`       | 接続されているTiDBサーバーのポート番号。                              |
| `CLIENT_IP`       | クライアントのIPアドレス。                                      |
| `CLIENT_PORT`     | クライアントのポート。                                         |

> **Note:**
>
> トラフィックの可視性を向上させるため、 `CLIENT_IP` 、ロードバランサーの IP アドレスではなく、AWS PrivateLink を経由する接続の実際のクライアント IP アドレスが表示されます。この機能はパブリックプレビューであり、AWS リージョン`Frankfurt (eu-central-1)`でのみ利用可能です。

### 監査操作情報 {#audit-operation-information}

イベントクラスが`AUDIT`または`AUDIT`のサブクラスである場合、監査ログには次のフィールドが含まれます。

| フィールド                | 説明                                   |
| ----------------- | ------------------------------------ |
| `AUDIT_OP_TARGET` | TiDB Cloudデータベース監査設定変更の対象オブジェクト。     |
| `AUDIT_OP_ARGS`   | TiDB Cloudデータベース監査設定で使用される引数が変更されます。 |

## 監査ログの制限 {#audit-logging-limitations}

TiDB Cloud Premium では、監査ログが時系列順に書き込まれることを保証していません。最新のイベントを確認するには、すべてのログファイルを確認する必要がある場合があります。ログを時系列順に並べ替えるには、各監査レコードの`TIME`フィールドを使用してください。
