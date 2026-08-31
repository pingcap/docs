---
title: TiDB Cloud Dedicated Database Audit Logging (Legacy)
summary: TiDB Cloud でクラスターを監査する方法について説明します。
---

# TiDB Cloud Dedicatedデータベース監査ログ（レガシー） {#tidb-cloud-dedicated-database-audit-logging-legacy}

TiDB Cloud は、実行された SQL 文など、データベースへのユーザーアクセスアクティビティを記録する監査ログ機能を提供します。

> **Note:**
>
> これはデータベース監査ログ機能のレガシーバージョンです。以前は限られたテストユーザー向けに有効化されており、現在はメンテナンスモードになっています。このドキュメントは、既存のそれらのユーザーを対象としています。新規デプロイについては、より細かいイベントクラスとより詳細な監査ログを提供する [TiDB Cloud データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md) を参照してください。

組織のユーザーアクセスポリシーやその他の情報セキュリティ対策の有効性を評価するために、データベース監査ログを定期的に分析することは、セキュリティのベストプラクティスです。

監査ログ機能は**デフォルトで無効**です。クラスターを監査するには、まず監査ログを有効にし、その後で監査フィルタールールを指定する必要があります。

> **Note:**
>
> 監査ログはクラスターのリソースを消費するため、クラスターを監査するかどうかは慎重に判断してください。

## 前提条件 {#prerequisites}

- TiDB Cloud Dedicated クラスターを使用していること。

    > **Note:**
    >
    > - データベース監査ログは {{{ .starter }}} では利用できません。
    > - {{{ .essential }}} については、[{{{ .essential }}} のデータベース監査ログ（プレビュー）](/tidb-cloud/essential-database-audit-logging.md) を参照してください。

- 組織内で `Organization Owner` または `Project Owner` ロールであること。そうでない場合、TiDB Cloud コンソールでデータベース監査関連のオプションを表示できません。詳細は、[ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles) を参照してください。

## 監査ログを有効にする {#enable-audit-logging}

TiDB Cloud は、TiDB Cloud Dedicated クラスターの監査ログをクラウドストレージサービスに記録することをサポートしています。データベース監査ログを有効にする前に、クラスターが配置されているクラウドプロバイダー上でクラウドストレージサービスを設定してください。

> **Note:**
>
> AWS にデプロイされた TiDB クラスターでは、データベース監査ログを有効にする際に、監査ログファイルを TiDB Cloud に保存することも選択できます。現在、この機能はリクエストベースでのみ利用可能です。この機能をリクエストするには、[TiDB Cloud console](https://tidbcloud.com) の右下にある **?** をクリックし、**Support Tickets** をクリックして [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals) に移動します。チケットを作成し、**Description** フィールドに "Apply to store audit log files in TiDB Cloud" と入力して、**Submit** をクリックしてください。

### AWS の監査ログを有効にする {#enable-audit-logging-for-aws}

AWS の監査ログを有効にするには、次の手順を実行します。

#### Step 1. Amazon S3 bucket を作成する {#step-1-create-an-amazon-s3-bucket}

TiDB Cloud が監査ログを書き込む宛先として、組織所有の AWS アカウント内の Amazon S3 bucket を指定します。

> **Note:**
>
> AWS S3 bucket で object lock を有効にしないでください。object lock を有効にすると、TiDB Cloud が監査ログファイルを S3 に送信できなくなります。

詳細は、AWS User Guide の [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) を参照してください。

#### Step 2. Amazon S3 access を設定する {#step-2-configure-amazon-s3-access}

1. 監査ログを有効にする対象 TiDB クラスターの TiDB Cloud Account ID と External ID を取得します。

    1. TiDB Cloud コンソールで [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動します。

        > **Tip:**
        >
        > 複数の組織に所属している場合は、まず左上のコンボボックスを使用して対象の組織に切り替えてください。

    2. 対象の TiDB Cloud Dedicated クラスター名をクリックして概要ページに移動し、左側のナビゲーションペインで **Settings** > **DB Audit Logging** をクリックします。
    3. **DB Audit Logging** ページで、右上の **Enable** をクリックします。
    4. **Enable Database Audit Logging** ダイアログで、**AWS IAM Policy Settings** セクションを見つけ、後で使用するために **TiDB Cloud Account ID** と **TiDB Cloud External ID** を記録します。

2. AWS Management Console で **IAM** > **Access Management** > **Policies** に移動し、`s3:PutObject` の書き込み専用権限を持つストレージ bucket policy があるか確認します。

    - ある場合は、後で使用するために一致するストレージ bucket policy を記録します。
    - ない場合は、**IAM** > **Access Management** > **Policies** > **Create Policy** に移動し、次の policy template に従って bucket policy を定義します。

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

        このテンプレートで、`<Your S3 bucket ARN>` は監査ログファイルの書き込み先となる S3 bucket の Amazon Resource Name (ARN) です。S3 bucket の **Properties** タブに移動し、**Bucket Overview** で ARN 値を取得できます。`"Resource"` フィールドでは、ARN の後ろに `/*` を追加する必要があります。たとえば、ARN が `arn:aws:s3:::tidb-cloud-test` の場合、`"Resource"` フィールドの値は `"arn:aws:s3:::tidb-cloud-test/*"` と設定する必要があります。

3. **IAM** > **Access Management** > **Roles** に移動し、先ほど記録した TiDB Cloud Account ID と External ID に対応する trust entity を持つ role がすでに存在するか確認します。

    - ある場合は、後で使用するために一致する role を記録します。
    - ない場合は、**Create role** をクリックし、trust entity type として **Another AWS account** を選択して、**Account ID** フィールドに TiDB Cloud Account ID の値を入力します。次に、**Require External ID** オプションを選択し、**External ID** フィールドに TiDB Cloud External ID の値を入力します。

4. **IAM** > **Access Management** > **Roles** で、前の手順の role 名をクリックして **Summary** ページに移動し、次の手順を実行します。

    1. **Permissions** タブで、記録した `s3:PutObject` 書き込み専用権限を持つ policy がその role にアタッチされているか確認します。アタッチされていない場合は、**Attach Policies** を選択し、必要な policy を検索して、**Attach Policy** をクリックします。
    2. **Summary** ページに戻り、**Role ARN** の値をクリップボードにコピーします。

#### Step 3. 監査ログを有効にする {#step-3-enable-audit-logging}

TiDB Cloud コンソールで、TiDB Cloud account ID と External ID の値を取得した **Enable Database Audit Logging** ダイアログボックスに戻り、次の手順を実行します。

1. **Bucket URI** フィールドに、監査ログファイルの書き込み先となる S3 bucket の URI を入力します。
2. **Bucket Region** ドロップダウンリストで、bucket が存在する AWS リージョンを選択します。
3. **Role ARN** フィールドに、[Step 2. Configure Amazon S3 access](#step-2-configure-amazon-s3-access) でコピーした Role ARN の値を入力します。
4. **Test Connection** をクリックして、TiDB Cloud が bucket にアクセスして書き込めるかを確認します。

    成功すると、**The connection is successful** と表示されます。そうでない場合は、アクセス設定を確認してください。

5. **Enable** をクリックして、クラスターの監査ログを有効にします。

    TiDB Cloud は、指定したクラスターの監査ログを Amazon S3 bucket に書き込む準備が整います。

> **Note:**
>
> - 監査ログを有効にした後、bucket URI、location、または ARN に新しい変更を加えた場合は、TiDB Cloud が bucket に接続できることを確認するために、再度 **Test Connection** をクリックする必要があります。その後、**Enable** をクリックして変更を適用します。
> - TiDB Cloud から Amazon S3 へのアクセスを削除するには、AWS Management Console でこのクラスターに付与した trust policy を削除するだけです。

### Google Cloud の監査ログを有効にする {#enable-audit-logging-for-google-cloud}

Google Cloud の監査ログを有効にするには、次の手順を実行します。

#### Step 1. GCS bucket を作成する {#step-1-create-a-gcs-bucket}

TiDB Cloud が監査ログを書き込む宛先として、組織所有の Google Cloud アカウント内の Google Cloud Storage (GCS) bucket を指定します。

詳細は、Google Cloud Storage ドキュメントの [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets) を参照してください。

#### Step 2. GCS access を設定する {#step-2-configure-gcs-access}

1. 監査ログを有効にする対象 TiDB クラスターの Google Cloud Service Account ID を取得します。

    1. TiDB Cloud コンソールで [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動します。

        > **Tip:**
        >
        > 複数の組織に所属している場合は、まず左上のコンボボックスを使用して対象の組織に切り替えてください。

    2. 対象の TiDB Cloud Dedicated クラスター名をクリックして概要ページに移動し、左側のナビゲーションペインで **Settings** > **DB Audit Logging** をクリックします。
    3. **DB Audit Logging** ページで、右上の **Enable** をクリックします。
    4. **Enable Database Audit Logging** ダイアログで、**Google Cloud Server Account ID** セクションを見つけ、後で使用するために **Service Account ID** を記録します。

2. Google Cloud console で **IAM & Admin** > **Roles** に移動し、ストレージコンテナに対して次の書き込み専用権限を持つ role が存在するか確認します。

    - storage.objects.create
    - storage.objects.delete

    ある場合は、後で使用するために対象 TiDB クラスターに一致する role を記録します。ない場合は、**IAM & Admin** > **Roles** > **CREATE ROLE** に移動して、対象 TiDB クラスター用の role を定義します。

3. **Cloud Storage** > **Browser** に移動し、TiDB Cloud にアクセスさせたい GCS bucket を選択して、**SHOW INFO PANEL** をクリックします。

    パネルが表示されます。

4. パネルで **ADD PRINCIPAL** をクリックします。

    principal を追加するためのダイアログボックスが表示されます。

5. ダイアログボックスで、次の手順を実行します。

    1. **New Principals** フィールドに、TiDB クラスターの Google Cloud Service Account ID を貼り付けます。
    2. **Role** ドロップダウンリストで、対象 TiDB クラスターの role を選択します。
    3. **SAVE** をクリックします。

#### Step 3. 監査ログを有効にする {#step-3-enable-audit-logging}

TiDB Cloud コンソールで、TiDB Cloud account ID を取得した **Enable Database Audit Logging** ダイアログボックスに戻り、次の手順を実行します。

1. **Bucket URI** フィールドに、GCS bucket の完全な名前を入力します。
2. **Bucket Region** フィールドで、bucket が存在する GCS リージョンを選択します。
3. **Test Connection** をクリックして、TiDB Cloud が bucket にアクセスして書き込めるかを確認します。

    成功すると、**The connection is successful** と表示されます。そうでない場合は、アクセス設定を確認してください。

4. **Enable** をクリックして、クラスターの監査ログを有効にします。

    TiDB Cloud は、指定したクラスターの監査ログを GCS bucket に書き込む準備が整います。

> **Note:**
>
> - 監査ログを有効にした後、bucket URI または location に新しい変更を加えた場合は、TiDB Cloud が bucket に接続できることを確認するために、再度 **Test Connection** をクリックする必要があります。その後、**Enable** をクリックして変更を適用します。
> - TiDB Cloud から GCS bucket へのアクセスを削除するには、Google Cloud console でこのクラスターに付与した trust policy を削除してください。

### Azure の監査ログを有効にする {#enable-audit-logging-for-azure}

Azure の監査ログを有効にするには、次の手順を実行します。

#### Step 1. Azure storage account を作成する {#step-1-create-an-azure-storage-account}

TiDB Cloud がデータベース監査ログを書き込む宛先として、組織の Azure subscription 内に Azure storage account を作成します。

詳細は、Azure ドキュメントの [Create an Azure storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal) を参照してください。

#### Step 2. Azure Blob Storage アクセスを設定する {#step-2-configure-azure-blob-storage-access}

1. [Azure portal](https://portal.azure.com/) で、データベース監査ログの保存に使用するコンテナーを作成します。

    1. Azure portal の左側のナビゲーションペインで **Storage Accounts** をクリックし、次にデータベース監査ログを保存するストレージアカウントをクリックします。

        > **Tip:**
        >
        > 左側のナビゲーションペインが非表示の場合は、左上隅のメニューボタンをクリックして表示を切り替えます。

    2. 選択したストレージアカウントのナビゲーションペインで **Data storage > Containers** をクリックし、次に **+ Container** をクリックして **New container** ペインを開きます。

    3. **New container** ペインで、新しいコンテナーの名前を入力し、匿名アクセスレベルを設定します（推奨レベルは **Private** で、匿名アクセスなしを意味します）。その後、**Create** をクリックします。数秒後に新しいコンテナーが作成され、コンテナー一覧に表示されます。

2. 対象コンテナーの URL を取得します。

    1. コンテナー一覧で対象コンテナーを選択し、そのコンテナーの **...** をクリックして、**Container properties** を選択します。
    2. 表示されたプロパティページで、後で使用するために **URL** の値をコピーし、その後コンテナー一覧に戻ります。

3. 対象コンテナーの SAS トークンを生成します。

    1. コンテナー一覧で対象コンテナーを選択し、そのコンテナーの **...** をクリックして、**Generate SAS** を選択します。
    2. 表示された **Generate SAS** ペインで、**Signing method** に **Account key** を選択します。
    3. **Permissions** ドロップダウンリストで、監査ログファイルの書き込みを許可するために **Read**、**Write**、**Create** を選択します。
    4. **Start** フィールドと **Expiry** フィールドで、SAS トークンの有効期間を指定します。

        > **Note:**
        >
        > - 監査機能では監査ログをストレージアカウントに継続的に書き込む必要があるため、SAS トークンには十分に長い有効期間が必要です。ただし、有効期間が長いほどトークン漏えいのリスクは高まります。セキュリティのため、SAS トークンは 6 か月から 12 か月ごとに置き換えることを推奨します。
        > - 生成された SAS トークンは取り消せないため、有効期間は慎重に設定する必要があります。
        > - 監査ログを継続して利用できるようにするため、有効期限が切れる前に必ず SAS トークンを再生成して更新してください。

    5. **Allowed protocols** では、安全なアクセスを確保するために **HTTPS only** を選択します。
    6. **Generate SAS token and URL** をクリックし、表示された **Blob SAS token** を後で使用するためにコピーします。

#### Step 3. 監査ログを有効にする {#step-3-enable-audit-logging}

1. TiDB Cloud コンソールで [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上隅のコンボボックスを使用して対象の組織に切り替えます。

2. 対象の TiDB Cloud Dedicated クラスター名をクリックして概要ページに移動し、左側のナビゲーションペインで **Settings** > **DB Audit Logging** をクリックします。
3. **DB Audit Logging** ページの右上隅で **Enable** をクリックします。
4. **Enable Database Audit Logging** ダイアログで、[Step 2. Configure Azure Blob access](#step-2-configure-azure-blob-storage-access) で取得した blob URL と SAS トークンを入力します。

    - **Blob URL** フィールドに、監査ログを保存するコンテナーの URL を入力します。
    - **SAS Token** フィールドに、コンテナーへアクセスするための SAS トークンを入力します。

5. **Test Connection** をクリックして、TiDB Cloud がコンテナーにアクセスして書き込みできるかを確認します。

    成功すると、**The connection is successful** と表示されます。失敗した場合は、アクセス設定を確認してください。

6. **Enable** をクリックして、クラスターの監査ログを有効にします。

    TiDB Cloud は、指定したクラスターの監査ログを Azure blob コンテナーに書き込む準備が整います。

> **Note:**
>
> 監査ログを有効にした後、**Blob URL** または **SAS Token** フィールドに新しい変更を加えた場合は、TiDB Cloud がコンテナーに接続できることを確認するために、再度 **Test Connection** をクリックする必要があります。その後、**Enable** をクリックして変更を適用します。

## 監査フィルタールールを指定する {#specify-auditing-filter-rules}

監査ログを有効にした後は、どのユーザーアクセスイベントを取得して監査ログに書き込むかを制御するために、監査フィルタールールを指定する必要があります。フィルタールールが指定されていない場合、TiDB Cloud は何も記録しません。

クラスターの監査フィルタールールを指定するには、次の手順を実行します。

1. **DB Audit Logging** ページの **Log Filter Rules** セクションで **Add Filter Rule** をクリックし、監査フィルタールールを追加します。

    一度に追加できる監査ルールは 1つです。各ルールでは、ユーザー式、データベース式、テーブル式、およびアクセス種別を指定します。監査要件に応じて複数の監査ルールを追加できます。

2. **Log Filter Rules** セクションで **>** をクリックして展開し、追加した監査ルールの一覧を表示します。

> **Note:**
>
> - フィルタールールは正規表現であり、大文字と小文字を区別します。ワイルドカードルール `.*` を使用すると、クラスター内のすべてのユーザー、データベース、またはテーブルイベントが記録されます。
> - 監査ログはクラスターリソースを消費するため、フィルタールールの指定は慎重に行ってください。消費を最小限に抑えるため、可能であれば、特定のデータベースオブジェクト、ユーザー、およびアクションに監査ログの範囲を限定するフィルタールールを指定することを推奨します。

## 監査ログを表示する {#view-audit-logs}

デフォルトでは、TiDB Cloud はデータベース監査ログファイルをお使いのストレージサービスに保存するため、監査ログ情報はそのストレージサービスから読み取る必要があります。

> **Note:**
>
> 監査ログファイルを TiDB Cloud に保存するようリクエストして選択している場合は、**Database Audit Logging** ページの **Audit Log Access** セクションからダウンロードできます。

TiDB Cloud の監査ログは可読なテキストファイルであり、完全修飾ファイル名にはクラスター ID、ノード ID、およびログ作成日が含まれます。

たとえば、`13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log` です。この例では、`13796619446086334065` はクラスター ID、`tidb-0` はノード ID を示します。

## 監査ログを無効にする {#disable-audit-logging}

クラスターの監査が不要になった場合は、そのクラスターのページに移動し、**Settings** > **Audit Settings** をクリックして、右上隅の監査設定を **Off** に切り替えます。

> **Note:**
>
> ログファイルのサイズが 10 MiB に達するたびに、そのログファイルはクラウドストレージバケットにプッシュされます。そのため、監査ログを無効にした後は、サイズが 10 MiB 未満のログファイルはクラウドストレージバケットに自動的にはプッシュされません。この状況でログファイルを取得するには、[PingCAPサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。

## 監査ログフィールド {#audit-log-fields}

監査ログ内の各データベースイベントレコードについて、TiDB は次のフィールドを提供します。

> **Note:**
>
> 次の表では、フィールドの最大長が空欄である場合、そのフィールドのデータ型は明確に定義された固定長を持つことを意味します（たとえば、INTEGER は 4 バイトです）。

| 列番号 | フィールド名 | TiDB データ型 | 最大長 | 説明 |
|---|---|---|---|---|
| 1 | N/A | N/A | N/A | 内部使用のために予約済み |
| 2 | N/A | N/A | N/A | 内部使用のために予約済み |
| 3 | N/A | N/A | N/A | 内部使用のために予約済み |
| 4 | ID       | INTEGER |  | 一意のイベント ID  |
| 5 | TIMESTAMP | TIMESTAMP |  | イベント発生時刻   |
| 6 | EVENT_CLASS | VARCHAR | 15 | イベントタイプ     |
| 7 | EVENT_SUBCLASS     | VARCHAR | 15 | イベントサブタイプ |
| 8 | STATUS_CODE | INTEGER |  | ステートメントの応答ステータス   |
| 9 | COST_TIME | FLOAT |  | ステートメントの実行に要した時間    |
| 10 | HOST | VARCHAR | 16 | サーバー IP    |
| 11 | CLIENT_IP         | VARCHAR | 16 | クライアント IP   |
| 12 | USER | VARCHAR | 17 | ログインユーザー名    |
| 13 | DATABASE | VARCHAR | 64 | イベントに関連するデータベース      |
| 14 | TABLES | VARCHAR | 64 | イベントに関連するテーブル名          |
| 15 | SQL_TEXT | VARCHAR | 64 KB | マスクされた SQL文   |
| 16 | ROWS | INTEGER |  | 影響を受けた行数（`0` は影響を受けた行がないことを示します）      |

TiDB によって設定される EVENT_CLASS フィールドの値に応じて、監査ログ内のデータベースイベントレコードには次の追加フィールドも含まれます。

- EVENT_CLASS の値が `CONNECTION` の場合、データベースイベントレコードには次のフィールドも含まれます。

    | 列番号 | フィールド名 | TiDB データ型 | 最大長 | 説明 |
    |---|---|---|---|---|
    | 17 | CLIENT_PORT | INTEGER |  | クライアントポート番号 |
    | 18 | CONNECTION_ID | INTEGER |  | 接続 ID |
    | 19 | CONNECTION_TYPE  | VARCHAR | 12 | `socket` または `unix-socket` 経由の接続 |
    | 20 | SERVER_ID | INTEGER |  | TiDB サーバー ID |
    | 21 | SERVER_PORT | INTEGER |  | TiDB サーバーが MySQL プロトコル経由で通信するクライアントを待ち受けるために使用するポート |
    | 22 | SERVER_OS_LOGIN_USER | VARCHAR | 17 | TiDB プロセスを起動したシステムのユーザー名  |
    | 23 | OS_VERSION | VARCHAR | N/A | TiDB サーバーが配置されているオペレーティングシステムのバージョン  |
    | 24 | SSL_VERSION | VARCHAR | 6 | TiDB の現在の SSL バージョン |
    | 25 | PID | INTEGER |  | TiDB プロセスの PID |

- EVENT_CLASS の値が `TABLE_ACCESS` または `GENERAL` の場合、データベースイベントレコードには次のフィールドも含まれます。

    | 列番号 | フィールド名 | TiDB データ型 | 最大長 | 説明 |
    |---|---|---|---|---|
    | 17 | CONNECTION_ID | INTEGER |  | 接続 ID   |
    | 18 | COMMAND | VARCHAR | 14 | MySQL プロトコルのコマンドタイプ |
    | 19 | SQL_STATEMENT  | VARCHAR | 17 | SQL文タイプ |
    | 20 | PID | INTEGER |  | TiDB プロセスの PID  |