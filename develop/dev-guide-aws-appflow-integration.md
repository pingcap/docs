---
title: Integrate TiDB with Amazon AppFlow
summary: TiDB を Amazon AppFlow と統合する方法を段階的に紹介します。
---

# TiDB を Amazon AppFlow と統合する {#integrate-tidb-with-amazon-appflow}

[Amazon AppFlow](https://aws.amazon.com/appflow/) 、SaaS (Software as a Service) アプリケーションを AWS のサービスに接続し、安全にデータを転送するためのフルマネージド API 統合サービスです。Amazon AppFlow を使用すると、Salesforce、Amazon S3、LinkedIn、GitHub など、様々なデータプロバイダーとの間で TiDB のデータをインポートおよびエクスポートできます。詳細については、AWS ドキュメントの[サポートされているソースアプリケーションと宛先アプリケーション](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)ご覧ください。

このドキュメントでは、TiDB を Amazon AppFlow と統合する方法について説明し、 TiDB Cloud Serverless クラスターの統合を例として取り上げます。

TiDB クラスターがない場合は、 [TiDB Cloud Serverless クラスターを作成する](https://docs.pingcap.com/tidbcloud/create-tidb-cluster-serverless)使用できます。これは無料で、約 30 秒で作成できます。

## 前提条件 {#prerequisites}

-   [ギット](https://git-scm.com/)

-   [JDK](https://openjdk.org/install/) 11以上

-   [メイヴン](https://maven.apache.org/install.html) 3.8以上

-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)バージョン 2

-   [AWS サーバーレスアプリケーションモデルコマンドラインインターフェイス (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0以上

-   次の要件を満たす AWS [アイデンティティおよびアクセス管理 (IAM) ユーザー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) :

    -   ユーザーは[アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)使用して AWS にアクセスできます。
    -   ユーザーには次の権限があります。

        -   `AWSCertificateManagerFullAccess` : [AWS シークレットマネージャー](https://aws.amazon.com/secrets-manager/)の読み取りと書き込みに使用されます。
        -   `AWSCloudFormationFullAccess` : SAM CLI は[AWS クラウドフォーメーション](https://aws.amazon.com/cloudformation/)を使用して AWS リソースを宣言します。
        -   `AmazonS3FullAccess` : AWS CloudFormation は[アマゾンS3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3)使用して公開します。
        -   `AWSLambda_FullAccess` : 現在、Amazon AppFlow の新しいコネクタを実装するには[AWS ラムダ](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd)唯一の方法です。
        -   `IAMFullAccess` : SAM CLI はコネクタ用に`ConnectorFunctionRole`作成する必要があります。

-   [セールスフォース](https://developer.salesforce.com)アカウント。

## ステップ1. TiDBコネクタを登録する {#step-1-register-a-tidb-connector}

### コードを複製する {#clone-the-code}

TiDB と Amazon AppFlow の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-appflow-integration)クローンします。

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### Lambdaをビルドしてアップロードする {#build-and-upload-a-lambda}

1.  パッケージをビルドします。

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2.  (オプション) AWS アクセスキー ID とシークレットアクセスキーをまだ設定していない場合は設定します。

    ```bash
    aws configure
    ```

3.  JAR パッケージを Lambda としてアップロードします。

    ```bash
    sam deploy --guided
    ```

    > **注記：**
    >
    > -   `--guided`オプションでは、プロンプトが表示され、デプロイメントの手順を案内します。入力内容は設定ファイル（デフォルトでは`samconfig.toml`に保存されます。
    > -   `stack_name` 、デプロイする AWS Lambda の名前を指定します。
    > -   このガイドでは、 TiDB Cloud Serverless のクラウドプロバイダーとしてAWSを使用します。Amazon S3 をソースまたはデスティネーションとして使用するには、AWS Lambda の`region` Amazon S3 と同じ値に設定する必要があります。
    > -   すでに`sam deploy --guided`実行している場合は、代わりに`sam deploy`実行するだけで、SAM CLI は構成ファイル`samconfig.toml`を使用して対話を簡素化します。

    次のような出力が表示された場合、この Lambda は正常にデプロイされています。

        Successfully created/updated stack - <stack_name> in <region>

4.  [AWS Lambdaコンソール](https://console.aws.amazon.com/lambda/home)に移動すると、アップロードしたLambdaが表示されます。ウィンドウの右上隅で正しいリージョンを選択する必要があることに注意してください。

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### Lambdaを使用してコネクタを登録する {#use-lambda-to-register-a-connector}

1.  [AWS マネジメントコンソール](https://console.aws.amazon.com)で[Amazon AppFlow &gt; コネクタ](https://console.aws.amazon.com/appflow/home#/gallery)に移動し、 **「新しいコネクタの登録」を**クリックします。

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2.  **「新しいコネクタの登録」ダイアログ**で、アップロードした Lambda 関数を選択し、コネクタ名を使用してコネクタ ラベルを指定します。

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3.  **「登録」**をクリックします。すると、TiDBコネクタが正常に登録されます。

## ステップ2. フローを作成する {#step-2-create-a-flow}

[Amazon AppFlow &gt; フロー](https://console.aws.amazon.com/appflow/home#/list)に移動して、 **「フローの作成」を**クリックします。

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### フロー名を設定する {#set-the-flow-name}

フロー名を入力し、 **「次へ」**をクリックします。

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### ソーステーブルと宛先テーブルを設定する {#set-the-source-and-destination-tables}

**ソースの詳細**と**宛先の詳細**を選択します。TiDB コネクタはどちらでも使用できます。

1.  ソース名を選択します。このドキュメントでは、 **Salesforce を**サンプルソースとして使用します。

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    Salesforceに登録すると、Salesforceはプラットフォームにサンプルデータを追加します。以下の手順では、 **Account**オブジェクトをソースオブジェクトの例として使用します。

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2.  **[接続]**をクリックします。

    1.  **[Salesforce に接続]**ダイアログで、この接続の名前を指定して、 **[続行]**をクリックします。

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2.  **「許可」**をクリックして、AWS が Salesforce データを読み取ることができることを確認します。

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **注記：**
    >
    > 貴社で既にSalesforceのProfessional Editionをご利用の場合、REST APIはデフォルトで有効化されていません。REST APIをご利用いただくには、新しいDeveloper Editionを登録していただく必要がある場合があります。詳しくは[Salesforceフォーラムトピック](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)をご覧ください。

3.  **「宛先の詳細」**エリアで、宛先として**「TiDB-Connector」を**選択します。「**接続」**ボタンが表示されます。

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4.  **「接続」**をクリックする前に、Salesforce **Account**オブジェクト用のテーブル`sf_account`をTiDBに作成する必要があります。このテーブルスキーマは[Amazon AppFlow のチュートリアル](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html)のサンプルデータとは異なることに注意してください。

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

5.  `sf_account`テーブルが作成されたら、 **「接続」**をクリックします。接続ダイアログが表示されます。

6.  **「TiDBコネクタに接続」**ダイアログで、TiDBクラスタの接続プロパティを入力します。TiDB TiDB Cloud Serverlessクラスタを使用する場合は、 **TLS**オプションを`Yes`に設定する必要があります。これにより、TiDBコネクタはTLS接続を使用できるようになります。次に、 **「接続」**をクリックします。

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7.  これで、接続に指定したデータベース内のすべてのテーブルを取得できます。ドロップダウンリストから**sf_account**テーブルを選択してください。

    ![database](/media/develop/aws-appflow-step-database.png)

    次のスクリーンショットは、Salesforce **Account**オブジェクトから TiDB の`sf_account`のテーブルにデータを転送するための構成を示しています。

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8.  **「エラー処理」**エリアで、 **「現在のフロー実行を停止」**を選択します。 **「フロートリガー」**エリアで、 **「オンデマンド実行**」トリガータイプを選択します。これは、フローを手動で実行する必要があることを意味します。「**次へ」**をクリックします。

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### マッピングルールを設定する {#set-mapping-rules}

Salesforce の**Account**オブジェクトのフィールドを TiDB の`sf_account`テーブルにマップし、 **[次へ]**をクリックします。

-   `sf_account`テーブルが TiDB に新しく作成され、空です。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

-   マッピングルールを設定するには、左側でソースフィールド名を選択し、右側で宛先フィールド名を選択します。その後、 **「フィールドをマッピング」**をクリックすると、ルールが設定されます。

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

-   このドキュメントでは、次のマッピング ルール (ソース フィールド名 -&gt; 宛先フィールド名) が必要です。

    -   アカウントID -&gt; id
    -   アカウント名 -&gt; 名前
    -   アカウントの種類 -&gt; タイプ
    -   請求先州/県 -&gt; billing_state
    -   アカウント評価 -&gt; 評価
    -   業界 -&gt; 業界

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### （オプション）フィルターを設定する {#optional-set-filters}

データフィールドにフィルターを追加したい場合は、ここで設定できます。そうでない場合は、この手順をスキップして**「次へ」**をクリックしてください。

![filters](/media/develop/aws-appflow-step-filters.png)

### フローを確認して作成する {#confirm-and-create-the-flow}

作成するフローの情報を確認します。問題がなければ、 **「フローを作成」を**クリックします。

![review](/media/develop/aws-appflow-step-review.png)

## ステップ3. フローを実行する {#step-3-run-the-flow}

新しく作成されたフローのページで、右上隅の**[フロー実行] を**クリックします。

![run flow](/media/develop/aws-appflow-step-run-flow.png)

次のスクリーンショットは、フローが正常に実行された例を示しています。

![run success](/media/develop/aws-appflow-step-run-success.png)

`sf_account`テーブルをクエリすると、Salesforce **Account**オブジェクトのレコードがそのテーブルに書き込まれていることがわかります。

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

-   何か問題が発生した場合は、AWS マネジメントコンソールの[クラウドウォッチ](https://console.aws.amazon.com/cloudwatch/home)ページに移動してログを取得できます。
-   このドキュメントの手順は[Amazon AppFlow カスタムコネクタ SDK を使用してカスタムコネクタを構築する](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)に基づいています。
-   [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)は本番環境では**ありません**。
-   長くなりすぎないように、このドキュメントの例では`Insert`戦略のみを示していますが、 `Update`と`Upsert`戦略もテストされており、使用できます。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
