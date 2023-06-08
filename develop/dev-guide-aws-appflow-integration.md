---
title: Integrate TiDB with Amazon AppFlow
summary: Introduce how to integrate TiDB with Amazon AppFlow step by step.
---

# TiDB を Amazon AppFlow と統合する {#integrate-tidb-with-amazon-appflow}

[Amazon AppFlow](https://aws.amazon.com/appflow/)は、サービスとしてのソフトウェア (SaaS) アプリケーションを AWS のサービスに接続し、データを安全に転送するために使用する完全マネージド型の API 統合サービスです。 Amazon AppFlow を使用すると、TiDB との間で、Salesforce、Amazon S3、LinkedIn、GitHub などのさまざまなタイプのデータ プロバイダーにデータをインポートおよびエクスポートできます。詳細については、AWS ドキュメントの[サポートされている送信元および宛先アプリケーション](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)参照してください。

このドキュメントでは、TiDB を Amazon AppFlow と統合する方法について説明し、例としてTiDB Cloud Serverless Tierクラスターの統合を取り上げます。

TiDB クラスターがない場合は、無料で約 30 秒で作成できる[Serverless Tier](https://tidbcloud.com/console/clusters)クラスターを作成できます。

## 前提条件 {#prerequisites}

-   [ギット](https://git-scm.com/)

-   [JDK](https://openjdk.org/install/) 11 以上

-   [メイヴン](https://maven.apache.org/install.html) 3.8 以上

-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)バージョン 2

-   [AWS サーバーレス アプリケーション モデルのコマンド ライン インターフェイス (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 以上

-   次の要件を持つ AWS [ID およびアクセス管理 (IAM) ユーザー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) :

    -   ユーザーは[アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)を使用して AWS にアクセスできます。
    -   ユーザーには次の権限があります。

        -   `AWSCertificateManagerFullAccess` : [AWS シークレット マネージャー](https://aws.amazon.com/secrets-manager/)読み取りと書き込みに使用されます。
        -   `AWSCloudFormationFullAccess` : SAM CLI は[AWS クラウドフォーメーション](https://aws.amazon.com/cloudformation/)を使用して AWS リソースを宣言します。
        -   `AmazonS3FullAccess` : AWS CloudFormation は[アマゾンS3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3)を使用して発行します。
        -   `AWSLambda_FullAccess` : 現在、Amazon AppFlow の新しいコネクタを実装するには[AWS ラムダ](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd)が唯一の方法です。
        -   `IAMFullAccess` : SAM CLI はコネクタ用に`ConnectorFunctionRole`を作成する必要があります。

-   [セールスフォース](https://developer.salesforce.com)アカウント。

## ステップ 1. TiDB コネクターを登録する {#step-1-register-a-tidb-connector}

### コードを複製する {#clone-the-code}

TiDB と Amazon AppFlow 用に[統合サンプル コード リポジトリ](https://github.com/pingcap-inc/tidb-appflow-integration)を複製します。

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### Lambda をビルドしてアップロードする {#build-and-upload-a-lambda}

1.  パッケージをビルドします。

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2.  (オプション) まだ設定していない場合は、AWS アクセス キー ID とシークレット アクセス キーを設定します。

    ```bash
    aws configure
    ```

3.  JAR パッケージを Lambda としてアップロードします。

    ```bash
    sam deploy --guided
    ```

    > **ノート：**
    >
    > -   `--guided`オプションでは、プロンプトを使用して展開をガイドします。入力は、デフォルトで`samconfig.toml`である構成ファイルに保存されます。
    > -   `stack_name`デプロイする AWS Lambda の名前を指定します。
    > -   このプロンプテッド ガイドでは、AWS をTiDB Cloud Serverless Tierのクラウド プロバイダーとして使用します。 Amazon S3 を送信元または送信先として使用するには、AWS Lambda の`region`を Amazon S3 と同じに設定する必要があります。
    > -   以前に`sam deploy --guided`を実行したことがある場合は、代わりに`sam deploy`実行できます。SAM CLI は構成ファイル`samconfig.toml`を使用して対話を簡素化します。

    次のような出力が表示された場合、この Lambda は正常にデプロイされています。

    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```

4.  [AWS ラムダ コンソール](https://console.aws.amazon.com/lambda/home)に移動すると、アップロードしたばかりの Lambda が表示されます。ウィンドウの右上隅で正しいリージョンを選択する必要があることに注意してください。

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### Lambda を使用してコネクタを登録する {#use-lambda-to-register-a-connector}

1.  [AWS マネジメント コンソール](https://console.aws.amazon.com)で[Amazon AppFlow &gt; コネクタ](https://console.aws.amazon.com/appflow/home#/gallery)に移動し、 **[Register new connector]**をクリックします。

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2.  **[新しいコネクタの登録] ダイアログ**で、アップロードした Lambda 関数を選択し、コネクタ名を使用してコネクタ ラベルを指定します。

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3.  **[登録]**をクリックします。その後、TiDB コネクタが正常に登録されます。

## ステップ 2.フローを作成する {#step-2-create-a-flow}

[Amazon AppFlow &gt; フロー](https://console.aws.amazon.com/appflow/home#/list)に移動し、 **[Create flow]**をクリックします。

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### フロー名を設定する {#set-the-flow-name}

フロー名を入力し、 **[次へ]**をクリックします。

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### ソース テーブルと宛先テーブルを設定する {#set-the-source-and-destination-tables}

**[送信元の詳細]**と<strong>[宛先の詳細]</strong>を選択します。 TiDB コネクタは両方で使用できます。

1.  ソース名を選択します。このドキュメントでは、サンプル ソースとして**Salesforce**を使用しています。

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    Salesforce に登録すると、Salesforce によっていくつかのサンプル データがプラットフォームに追加されます。次の手順では、 **Account**オブジェクトをソース オブジェクトの例として使用します。

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2.  **[接続]**をクリックします。

    1.  **[Salesforce に接続]**ダイアログで、この接続の名前を指定し、 <strong>[続行]</strong>をクリックします。

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2.  **[許可]**をクリックして、AWS が Salesforce データを読み取れることを確認します。

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **ノート：**
    >
    > 会社がすでに Salesforce の Professional Edition を使用している場合、REST API はデフォルトで有効になっていません。 REST API を使用するには、新しい Developer Edition の登録が必要になる場合があります。詳細については、 [Salesforce フォーラムのトピック](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)を参照してください。

3.  **[送信先の詳細]**領域で、送信先として<strong>TiDB-Connector</strong>を選択します。<strong>接続</strong>ボタンが表示されます。

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4.  **Connect**をクリックする前に、TiDB に Salesforce <strong>Account</strong>オブジェクト用の`sf_account`テーブルを作成する必要があります。このテーブル スキーマは[Amazon AppFlow のチュートリアル](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html)のサンプル データとは異なることに注意してください。

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

6.  **[TiDB コネクタに接続]**ダイアログで、TiDB クラスターの接続プロパティを入力します。 TiDB Cloud Serverless Tierクラスターを使用する場合は、 <strong>TLS</strong>オプションを`Yes`に設定する必要があります。これにより、TiDB コネクタが TLS 接続を使用できるようになります。次に、 <strong>[接続]</strong>をクリックします。

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7.  これで、接続用に指定したデータベース内のすべてのテーブルを取得できます。ドロップダウン リストから**sf_account**テーブルを選択します。

    ![database](/media/develop/aws-appflow-step-database.png)

    次のスクリーンショットは、Salesforce **Account**オブジェクトから TiDB の`sf_account`テーブルにデータを転送する構成を示しています。

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8.  **[エラー処理]**領域で、 <strong>[現在のフローの実行を停止する]</strong>を選択します。 <strong>[フロー トリガー]</strong>領域で、 <strong>[オンデマンドで実行</strong>] トリガー タイプを選択します。これは、フローを手動で実行する必要があることを意味します。次に、 <strong>[次へ]</strong>をクリックします。

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### マッピング ルールの設定 {#set-mapping-rules}

Salesforce の**Account**オブジェクトのフィールドを TiDB の`sf_account`テーブルにマップし、 <strong>[次へ]</strong>をクリックします。

-   `sf_account`テーブルは TiDB に新しく作成され、空です。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

-   マッピング ルールを設定するには、左側でソース フィールド名を選択し、右側で宛先フィールド名を選択します。次に、 **Map fields を**クリックすると、ルールが設定されます。

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

-   このドキュメントでは、次のマッピング ルール (ソース フィールド名 -&gt; 宛先フィールド名) が必要です。

    -   アカウント ID -&gt; id
    -   アカウント名 -&gt; 名前
    -   アカウントの種類 -&gt; タイプ
    -   請求先の都道府県 -&gt;billing_state
    -   アカウントの評価 -&gt; 評価
    -   業種 -&gt; 業種

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### (オプション) フィルターを設定する {#optional-set-filters}

データ フィールドにフィルターを追加する場合は、ここで設定できます。それ以外の場合は、この手順をスキップして**[次へ]**をクリックします。

![filters](/media/develop/aws-appflow-step-filters.png)

### フローの確認と作成 {#confirm-and-create-the-flow}

作成するフローの情報を確認します。問題がなければ、 **[Create flow]**をクリックします。

![review](/media/develop/aws-appflow-step-review.png)

## ステップ 3. フローを実行する {#step-3-run-the-flow}

新しく作成されたフローのページで、右上隅にある**[フローの実行]**をクリックします。

![run flow](/media/develop/aws-appflow-step-run-flow.png)

次のスクリーンショットは、フローが正常に実行される例を示しています。

![run success](/media/develop/aws-appflow-step-run-success.png)

`sf_account`テーブルをクエリすると、Salesforce **Account**オブジェクトのレコードが書き込まれていることがわかります。

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

## 特筆すべきこと {#noteworthy-things}

-   何か問題が発生した場合は、AWS マネジメント コンソールの[クラウドウォッチ](https://console.aws.amazon.com/cloudwatch/home)ページに移動してログを取得できます。
-   このドキュメントの手順は[Amazon AppFlow カスタム コネクタ SDK を使用してカスタム コネクタを構築する](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)に基づいています。
-   [TiDB Cloud Serverless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta)本番環境**ではありません**。
-   長すぎるのを防ぐために、このドキュメントの例では`Insert`戦略のみを示していますが、 `Update`および`Upsert`戦略もテストされており、使用できます。
