---
title: Connect to Amazon MSK Provisioned via a Private Link Connection
summary: Amazon MSK プロビジョニングされたプライベートリンク接続を使用して Amazon MSK プロビジョニングされたクラスターに接続する方法を学習します。
---

# プライベートリンク接続経由​​でプロビジョニングされた Amazon MSK に接続する {#connect-to-amazon-msk-provisioned-via-a-private-link-connection}

このドキュメントでは、 [Amazon MSK プロビジョニングされたプライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md#create-an-amazon-msk-provisioned-private-link-connection)を使用してTiDB Cloud Essentialクラスターを[Amazon MSK プロビジョニング](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html)クラスターに接続する方法について説明します。

## TiDB Cloud Essentialの前提条件 {#prerequisites-for-essential} {#prerequisites-for-essential}

-   TiDB Cloud Essentialクラスターは AWS でホストされており、アクティブです。後で使用するために、以下の情報を取得して保存してください。

    -   AWSアカウントID
    -   可用性ゾーン（AZ）

AWS アカウント ID とアベイラビリティーゾーンを表示するには:

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。
2.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。
3.  ダイアログで、AWS アカウント ID とアベイラビリティーゾーンをメモします。

## Amazon MSK プロビジョニングクラスターの前提条件 {#prerequisites-for-the-amazon-msk-provisioned-cluster}

始める前に、Amazon MSK プロビジョニングされたクラスターについて次の点を確認してください。

-   **リージョンと AZ** : Amazon MSK プロビジョニングされたクラスターは、 TiDB Cloud Essentialクラスターと同じ AWS リージョンにあり、MSK クラスターのアベイラビリティーゾーンはTiDB Cloudクラスターと同じです。
-   MSK クラスターには**認証**: [SASL/SCRAM認証](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html)が必要です。
-   **ブローカータイプ**: ブローカー`t4.small`タイプは使用しないでください。プライベートリンクをサポートしていません。

詳細な要件については、 [単一リージョンでの Amazon MSK マルチ VPC プライベート接続](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html#mvpc-requirements)参照してください。

Amazon MSK プロビジョニングされたクラスターがない場合は、 TiDB Cloud Essentialクラスターと同じリージョンおよび同じアベイラビリティーゾーンに[1つ作成する](https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html) 、作成されたクラスターに[SASL/SCRAM認証を設定する](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password-tutorial.html) 。

-   **シークレット名**: シークレット名は`AmazonMSK_`で始まる必要があります。
-   **暗号化**：デフォルトの暗号化キーは使用しないでください。シークレット用に新しいカスタムAWS KMSキーを作成してください。

## ステップ1. TiDB Cloudアクセス用にKafka ACLを設定する {#step-1-set-up-kafka-acls-for-tidb-cloud-access}

TiDB Cloud がAmazon MSK プロビジョニングクラスターにアクセスできるように、Kafka ACL を設定する必要があります。ACL の設定には、SASL/SCRAM 認証（推奨）またはIAM認証を使用できます。

<SimpleTab>
<div label="SASL/SCRAM">

この方法を使用して、SASL/SCRAM 認証を使用して MSK クラスターと同じ VPC に ACL を作成します。

1.  MSK クラスターが配置されている VPC に EC2 インスタンス (Linux) を作成し、SSH で接続します。

2.  Kafka と OpenJDK をダウンロードします。

    ```shell
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3.  環境を設定します。パスを実際のパスに置き換えてください。

    ```shell
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    ```

4.  以下の内容を含む`scram-client.properties`という名前のファイルを作成します。3と`pswd` `username` /SCRAMの認証情報に置き換えてください。

    ```properties
    security.protocol=SASL_SSL
    sasl.mechanism=SCRAM-SHA-512
    sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
        username="username" \
        password="pswd";
    ```

5.  ACLを作成します。1 `bootstrap-server` MSKブートストラップサーバーのアドレスとポート（例： `b-2.xxxxx.c18.kafka.us-east-1.amazonaws.com:9096` ）に置き換え、必要に応じてKafkaへのパスを置き換えます。

    ```shell
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --topic '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --group '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --cluster '*'
    ```

    プリンシパル`User:<username>`は、 TiDB CloudがMSKクラスターにアクセスするために使用するSASL/SCRAMユーザーです。MSK ACLでTiDB Cloud用に設定したユーザー名を使用してください。

</div>

<div label="IAM">

SASL/SCRAM の代わりに、 IAM認証を使用して MSK クラスターと同じ VPC 内に ACL を作成できますIAMユーザーまたはロールには、MSK 権限用の**Amazon MSK**および**Apache Kafka API が**必要です。

1.  MSK クラスターが配置されている VPC に EC2 インスタンス (Linux) を作成し、SSH で接続します。

2.  Kafka、OpenJDK、AWS MSK IAM認証 JAR をダウンロードします。

    ```shell
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    wget https://github.com/aws/aws-msk-iam-auth/releases/download/v2.3.5/aws-msk-iam-auth-2.3.5-all.jar
    ```

3.  環境を設定します。パスと資格情報を独自の値に置き換えてください。

    ```shell
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    export CLASSPATH=/home/ec2-user/aws-msk-iam-auth-2.3.5-all.jar
    export AWS_ACCESS_KEY_ID=<your-access-key-id>
    export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
    ```

4.  次の内容を含む`iam-client.properties`という名前のファイルを作成します。

    ```properties
    security.protocol=SASL_SSL
    sasl.mechanism=AWS_MSK_IAM
    sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
    sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
    ```

5.  ACLを作成します。1 `bootstrap-server` MSKブートストラップサーバーのアドレスとポート（例： `b-1.xxxxx.c18.kafka.us-east-1.amazonaws.com:9098` ）に置き換え、必要に応じてKafkaへのパスを置き換えます。

    ```shell
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --topic '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --group '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --cluster '*'
    ```

    プリンシパル`User:<username>`は、 TiDB CloudがMSKクラスターにアクセスするために使用するSASL/SCRAMユーザーです。MSK ACLでTiDB Cloud用に設定したユーザー名を使用してください。

</div>
</SimpleTab>

## ステップ2. MSKクラスターを構成する {#step-2-configure-the-msk-cluster}

次のクラスター構成プロパティを更新します。

-   セット`auto.create.topics.enable=true` 。
-   `allow.everyone.if.no.acl.found=false`追加します (SASL/SCRAM に必要)。
-   その他のプロパティは変更せず、必要に応じて調整します。

変更を適用し、クラスターのステータスが**Updating**から**Active**に変わるまで待ちます。

## ステップ3. クラスターポリシーをアタッチする {#step-3-attach-the-cluster-policy}

[クラスタポリシーをアタッチする](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html) [前提条件](#prerequisites-for-essential)して、 TiDB Cloud がMSK クラスターに接続できるようにします。2 で取得したTiDB Cloud AWS アカウント ID を使用してください。

## ステップ4. マルチVPC接続を有効にする {#step-4-turn-on-multi-vpc-connectivity}

クラスターがアクティブになった後、MSKクラスターの場合は[マルチVPC接続を有効にする](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-turn-on.html) 。AWS PrivateLinkにはマルチVPC接続が必要です。TiDB Cloudから接続するには、SASL/SCRAM認証を有効にする必要があります。

クラスターのステータスが**「更新中」**から**「アクティブ」**に再度変わるまで待ちます。

## ステップ 5. TiDB Cloudで Amazon MSK プロビジョニングされたプライベートリンク接続を作成する {#step-5-create-an-amazon-msk-provisioned-private-link-connection-in-tidb-cloud}

MSK クラスターの`ARN`使用して、 TiDB Cloudにプライベート リンク接続を作成します。

詳細については[Amazon MSK プロビジョニングされたプライベートリンク接続を作成する](/tidb-cloud/serverless-private-link-connection.md#create-an-amazon-msk-provisioned-private-link-connection)参照してください。
