---
title: Integrate TiDB with Amazon AppFlow
summary: TiDBとAmazon AppFlowを統合する方法を、手順を追って説明します。
aliases: ['/ja/tidb/stable/dev-guide-aws-appflow-integration/','/ja/tidb/dev/dev-guide-aws-appflow-integration/','/ja/tidbcloud/dev-guide-aws-appflow-integration/']
---

# TiDBとAmazon AppFlowを統合する {#integrate-tidb-with-amazon-appflow}

[Amazon AppFlow](https://aws.amazon.com/appflow/) Software as a Service (SaaS) アプリケーションを AWS サービスに接続し、データを安全に転送するために使用するフルマネージド API 統合サービスです。 Amazon AppFlow を使用すると、TiDB との間で、Salesforce、Amazon S3、LinkedIn、GitHub などのさまざまなタイプのデータプロバイダーにデータをインポートおよびエクスポートできます。詳細については、AWS ドキュメントの[サポートされている送信元および送信先アプリケーション](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)参照してください。

このドキュメントでは、TiDBをAmazon AppFlowと統合する方法について説明し、 TiDB Cloud Starterインスタンスの統合を例として取り上げます。

TiDB Cloud Starterインスタンスをお持ちでない場合は、 [TiDB Cloudクイックスタート](/tidb-cloud/tidb-cloud-quickstart.md)手順に従って作成できます。インスタンスは無料で、約30秒で作成できます。

## 前提条件 {#prerequisites}

-   [Git](https://git-scm.com/)

-   [JDK](https://openjdk.org/install/) 11以降

-   [メイブン](https://maven.apache.org/install.html)3.8以上

-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)バージョン 2

-   [AWSサーバーレスアプリケーションモデルコマンドラインインターフェイス（AWS SAM CLI）](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0以降

-   次の要件を持つ AWS [IDおよびアクセス管理（IAM）ユーザー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html):

    -   ユーザーは[アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)を使用して AWS にアクセスできます。
    -   ユーザーには以下の権限が付与されています。

        -   `AWSCertificateManagerFullAccess` : [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)読み書きに使用されます。
        -   `AWSCloudFormationFullAccess` : SAM CLI は[AWS CloudFormation](https://aws.amazon.com/cloudformation/)を使用して AWS リソースを宣言します。
        -   `AmazonS3FullAccess` : AWS CloudFormation は[Amazon S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3)を使用して公開します。
        -   `AWSLambda_FullAccess` : 現在、Amazon AppFlow 用の新しいコネクタを実装する方法は[AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd)のみです。
        -   `IAMFullAccess` : SAM CLI はコネクタ用に`ConnectorFunctionRole`を作成する必要があります。

-   [セールスフォース](https://developer.salesforce.com)アカウント。

## ステップ1. TiDBコネクタを登録する {#step-1-register-a-tidb-connector}

### コードを複製する {#clone-the-code}

TiDB と Amazon AppFlow の[統合例のコードリポジトリ](https://github.com/pingcap-inc/tidb-appflow-integration)クローンを作成します。

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### Lambda関数を構築してアップロードする {#build-and-upload-a-lambda}

1.  パッケージを作成する：

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2.  （オプション）AWSアクセスキーIDとシークレットアクセスキーを設定していない場合は、設定してください。

    ```bash
    aws configure
    ```

3.  JARパッケージをLambda関数としてアップロードしてください。

    ```bash
    sam deploy --guided
    ```

    > **注記：**
    >
    > -   `--guided`オプションでは、プロンプトが表示され、デプロイの手順を案内します。入力内容は構成ファイルに保存され、デフォルトでは`samconfig.toml`というファイルになります。
    > -   `stack_name`デプロイする AWS Lambda の名前を指定します。
    > -   このガイドでは、TiDB Cloud Starterのクラウド プロバイダーとして AWS を使用しています。ソースまたは宛先として Amazon S3 を使用するには、AWS Lambda の`region`を Amazon S3 と同じに設定する必要があります。
    > -   既に`sam deploy --guided`を実行したことがある場合は、代わりに`sam deploy`を実行するだけで、SAM CLI は設定ファイル`samconfig.toml`を使用して操作を簡素化します。

    以下のような出力が表示された場合、このLambda関数は正常にデプロイされています。

        Successfully created/updated stack - <stack_name> in <region>

4.  [AWS Lambdaコンソール](https://console.aws.amazon.com/lambda/home)にアクセスすると、先ほどアップロードしたLambda関数が表示されます。ウィンドウの右上隅で正しいリージョンを選択する必要があることに注意してください。

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### Lambdaを使用してコネクタを登録します {#use-lambda-to-register-a-connector}

1.  [AWS マネジメントコンソール](https://console.aws.amazon.com)コンソールで、 [Amazon AppFlow &gt; コネクタ](https://console.aws.amazon.com/appflow/home#/gallery)クリックし、 **[新しいコネクタの登録] を**クリックします。

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2.  **「新しいコネクタを登録」ダイアログ**で、アップロードしたLambda関数を選択し、コネクタ名を使用してコネクタラベルを指定します。

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3.  **「登録」**をクリックします。すると、TiDBコネクタが正常に登録されます。

## ステップ2. フローを作成する {#step-2-create-a-flow}

[Amazon AppFlow &gt; フロー](https://console.aws.amazon.com/appflow/home#/list)し、 **[フローの作成] を**クリックします。

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### フロー名を設定します {#set-the-flow-name}

フロー名を入力し、 **「次へ」**をクリックします。

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### ソーステーブルと宛先テーブルを設定します。 {#set-the-source-and-destination-tables}

**ソースの詳細**と**宛先の詳細**を選択してください。TiDBコネクタはどちらにも使用できます。

1.  ソース名を選択してください。このドキュメントでは、例として**Salesforceを**ソースとして使用します。

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    Salesforceに登録すると、Salesforceはプラットフォームにサンプルデータを追加します。以下の手順では、**アカウント**オブジェクトをサンプルソースオブジェクトとして使用します。

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2.  **「接続」**をクリックしてください。

    1.  **「Salesforceに接続」**ダイアログで、この接続の名前を指定し、 **「続行」**をクリックします。

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2.  「許可」をクリックして、AWSがSalesforceデータを読み取ることを**許可する**ことを確認してください。

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **注記：**
    >
    > 会社がすでに Salesforce の Professional Edition を使用している場合、REST API はデフォルトでは有効になっていません。 REST API を使用するには、新しい Developer Edition の登録が必要になる場合があります。詳細については、 [Salesforceフォーラムトピック](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)を参照してください。

3.  **「接続先の詳細」**エリアで、接続先として**「TiDB-Connector」**を選択します。「**接続」**ボタンが表示されます。

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4.  **「接続」**をクリックする前に、Salesforce **Account**オブジェクト用に TiDB に`sf_account`テーブルを作成する必要があります。このテーブルスキーマは[Amazon AppFlow のチュートリアル](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html)にあるサンプルデータとは異なることに注意してください。

    ```sql
    CREATE TABLE `sf_account` (
        `id` varchar(255) NOT NULL,
        `name` varchar(150) NOT NULL DEFAULT '',
        `type` varchar(150) NOT NULL DEFAULT '',
        `billing_state` varchar(255) NOT NULL DEFAULT '',
        `rating` varchar(255) NOT NULL DEFAULT '',
        `industry` varchar(255) NOT NULL DEFAULT '',
        PRIMARY KEY (`id`)
    );
    ```

5.  `sf_account`テーブルが作成されたら、 **[接続]**をクリックします。接続ダイアログが表示されます。

6.  **TiDBコネクタへの接続**ダイアログで、 TiDB Cloud Starterインスタンスの接続プロパティを入力します。TiDB Cloud Starterの場合、 **TLS**オプションを`Yes`に設定する必要があります。これにより、TiDBコネクタがTLS接続を使用できるようになります。次に、 **[接続]**をクリックします。

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7.  これで、接続時に指定したデータベース内のすべてのテーブルを取得できます。ドロップダウンリストから**sf_account**テーブルを選択してください。

    ![database](/media/develop/aws-appflow-step-database.png)

    次のスクリーンショットは、Salesforce **Account**オブジェクトから TiDB の`sf_account`テーブルにデータを転送するための設定を示しています。

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8.  **エラー処理**領域で、 **「現在のフロー実行を停止する」**を選択します。**フローのトリガー**領域で、 **「オンデマンドで実行**」トリガータイプを選択します。これは、フローを手動で実行する必要があることを意味します。次に、 **「次へ」**をクリックします。

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### マッピングルールを設定する {#set-mapping-rules}

Salesforce の**Account**オブジェクトのフィールドを TiDB の`sf_account`テーブルにマッピングし、 **[次へ]**をクリックします。

-   `sf_account`テーブルは TiDB に新しく作成されましたが、空です。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

-   マッピングルールを設定するには、左側でソースフィールド名を選択し、右側で宛先フィールド名を選択します。次に、 **「フィールドのマッピング」**をクリックすると、ルールが設定されます。

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

-   このドキュメントでは、以下のマッピングルール（ソースフィールド名→宛先フィールド名）が必要です。

    -   アカウントID -&gt; id
    -   アカウント名 -&gt; 名前
    -   アカウントタイプ -&gt; タイプ
    -   請求先州/都道府県 -&gt; billing_state
    -   アカウント評価 -&gt; 評価
    -   産業 -&gt; 産業

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### （オプション）フィルターを設定する {#optional-set-filters}

データフィールドにフィルターを追加したい場合は、ここで設定できます。そうでない場合は、この手順をスキップして**「次へ」**をクリックしてください。

![filters](/media/develop/aws-appflow-step-filters.png)

### フローを確認して作成する {#confirm-and-create-the-flow}

作成するフローの情報を確認してください。問題がなければ、 **「フローを作成」を**クリックします。

![review](/media/develop/aws-appflow-step-review.png)

## ステップ3. フローを実行する {#step-3-run-the-flow}

新しく作成したフローのページで、右上隅にある**「フローを実行」**をクリックします。

![run flow](/media/develop/aws-appflow-step-run-flow.png)

以下のスクリーンショットは、フローが正常に実行された例を示しています。

![run success](/media/develop/aws-appflow-step-run-success.png)

`sf_account`テーブルをクエリすると、Salesforce **Account**オブジェクトのレコードがそこに書き込まれていることが確認できます。

```sql
test> SELECT * FROM sf_account;
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| id                 | name                                | type               | billing_state | rating | industry       |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| 001Do000003EDTlIAO | Sample Account for Entitlements     | null               | null          | null   | null           |
| 001Do000003EDTZIA4 | Edge Communications                 | Customer - Direct  | TX            | Hot    | Electronics    |
| 001Do000003EDTaIAO | Burlington Textiles Corp of America | Customer - Direct  | NC            | Warm   | Apparel        |
| 001Do000003EDTbIAO | Pyramid Construction Inc.           | Customer - Channel | null          | null   | Construction   |
| 001Do000003EDTcIAO | Dickenson plc                       | Customer - Channel | KS            | null   | Consulting     |
| 001Do000003EDTdIAO | Grand Hotels & Resorts Ltd          | Customer - Direct  | IL            | Warm   | Hospitality    |
| 001Do000003EDTeIAO | United Oil & Gas Corp.              | Customer - Direct  | NY            | Hot    | Energy         |
| 001Do000003EDTfIAO | Express Logistics and Transport     | Customer - Channel | OR            | Cold   | Transportation |
| 001Do000003EDTgIAO | University of Arizona               | Customer - Direct  | AZ            | Warm   | Education      |
| 001Do000003EDThIAO | United Oil & Gas, UK                | Customer - Direct  | UK            | null   | Energy         |
| 001Do000003EDTiIAO | United Oil & Gas, Singapore         | Customer - Direct  | Singapore     | null   | Energy         |
| 001Do000003EDTjIAO | GenePoint                           | Customer - Channel | CA            | Cold   | Biotechnology  |
| 001Do000003EDTkIAO | sForce                              | null               | CA            | null   | null           |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
```

## 注目すべきこと {#noteworthy-things}

-   何か問題が発生した場合は、AWS マネジメントコンソールの[CloudWatch](https://console.aws.amazon.com/cloudwatch/home)ページにアクセスしてログを取得できます。
-   このドキュメントの手順は、 [Amazon AppFlow Custom Connector SDK を使用したカスタムコネクタの構築](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)に基づいています。
-   [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)は本番環境では**ありません**。
-   長くなりすぎないように、このドキュメントの例では`Insert`戦略のみを示していますが、 `Update`および`Upsert`戦略もテスト済みで使用できます。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
