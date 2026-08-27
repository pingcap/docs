---
title: AWS PrivateLink を使用して Amazon MSK Provisioned クラスターをセットアップする
summary: このドキュメントでは、Amazon MSK Provisioned クラスターをセットアップし、AWS PrivateLink を使用して TiDB Cloud に接続する方法を説明します。
---

# AWS PrivateLink を使用して Amazon MSK Provisioned クラスターをセットアップする

TiDB Cloud で Amazon MSK Provisioned のダウンストリームサービス用に[プライベートエンドポイントを作成する](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md)前に、AWS PrivateLink を介して TiDB Cloud Premium インスタンスから接続できるように MSK クラスターを設定します。

このドキュメントでは、[multi-VPC connectivity](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html) と [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) を使用して、TiDB Cloud Premium インスタンスを [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) クラスターに接続する方法を説明します。

このガイドでは、セットアップ全体の流れを扱います。具体的には、ネットワークと認証情報の準備、MSK クラスターの作成と設定、multi-VPC connectivity の有効化、クラスター ポリシーのアタッチ、そして TiDB Cloud からの PrivateLink 接続の確立です。

## 前提条件 {#prerequisites}

- AWS 上でホストされ、**Active** 状態の [TiDB Cloud Premium インスタンス](/tidb-cloud/premium/create-tidb-instance-premium.md)。
- TiDB Cloud Premium インスタンスの **AWS Account ID** と **アベイラビリティゾーンID（AZ ID）**。

  これらの値を取得するには、次の手順を実行します。

    1. [TiDB Cloud コンソール](https://tidbcloud.com)でインスタンスの概要ページに移動し、**Settings** > **Networking** をクリックします。
    2. **Private Link Endpoint For External Services** エリアで、**Create Private Endpoint for External Services** をクリックします。
    3. ダイアログで **Connection Type** を **AWS MSK Provisioned** に切り替え、**AWS Account ID** と **アベイラビリティゾーンID**（例: `use1-az1`）を確認します。

    **AZ の整合性に関する重要事項**: AWS アカウント間でアベイラビリティゾーンの整合性を確認する際は、AZ 名（例: `us-east-1a`）ではなく AZ ID（例: `use1-az1`）を使用してください。同じ AZ 名でも、アカウントによって異なる物理ゾーンに対応している場合があります。MSK クラスターは、TiDB Cloud Premium インスタンスと同じ AZ ID を使用する必要があります。

## ステップ 1. Amazon VPC とサブネットをセットアップする {#step-1-set-up-the-amazon-vpc-and-subnets}

必要なアベイラビリティゾーンにまたがる少なくとも 3つのプライベートサブネットを持つ Amazon VPC がすでにある場合は、このステップをスキップできます。

1. [Amazon VPC コンソール](https://console.aws.amazon.com/vpc/)で、TiDB Cloud Premium インスタンスが稼働する各アベイラビリティゾーンに 1つずつ、合計3つのプライベートサブネットを持つ [VPC を作成](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html)します。これらのサブネットは、AZ 名ではなく AZ ID に基づいて、TiDB Cloud Premium インスタンスが稼働する各アベイラビリティゾーンと一致している必要があります。
2. VPC ダッシュボードで、後から起動するクライアント EC2 インスタンスがプライベートネットワーク経由で MSK クラスターと通信できるように、ルートテーブルとセキュリティグループを設定します。
3. サブネットの AZ ID を記録します。これらのサブネットは、[MSK クラスターを作成する](#step-3-create-an-amazon-msk-provisioned-cluster)際に選択します。

## ステップ 2. AWS Secrets Manager で SCRAM シークレットを作成する {#step-2-create-a-scram-secret-in-aws-secrets-manager}

[AWS Secrets Manager コンソール](https://console.aws.amazon.com/secretsmanager/)で、TiDB Cloud が MSK クラスターへの認証に使用する SASL/SCRAM 認証情報を保存するための[シークレットを作成](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html)します。

シークレットを作成する際は、次の点に注意してください。

- **Other type of secrets** を選択します。
- **Secret value** には、ユーザー名とパスワードを含む JSON オブジェクトを指定します。
- **Encryption key** には、カスタマー管理の AWS KMS キーを選択します。デフォルトの AWS 管理キーは Amazon MSK では使用できません。カスタマー管理キーがない場合は、先に[対称暗号化 KMS キーを作成](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk)してください。
- シークレット名は `AmazonMSK_` プレフィックスで始まる必要があります（例: `AmazonMSK_tidb_msk`）。

## ステップ 3. Amazon MSK Provisioned クラスターを作成する {#step-3-create-an-amazon-msk-provisioned-cluster}

次の条件を満たす既存の Amazon MSK Provisioned クラスターがある場合は、このステップをスキップしてください。

- **Region**: TiDB Cloud Premium インスタンスと同じ AWS リージョン。
- **Availability Zones**: TiDB Cloud Premium インスタンスの AZ と一致している必要があります（AZ 名ではなく AZ ID で確認）。
- **Authentication**: TiDB Cloud 接続用に [SASL/SCRAM](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html) を有効にします。AWS MSK の multi-VPC connectivity は IAM および TLS 認証もサポートしていますが、このセットアップでは SASL/SCRAM を使用します。
- **Broker type**: `t3.small` はサポートされていません。より大きい broker type を選択してください。
- **Public access**: 無効にする必要があります。
- [Amazon MSK multi-VPC private connectivity documentation](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html#mvpc-requirements) に記載されている追加要件。

上記の要件を満たす MSK クラスターがない場合は、[Amazon MSK コンソール](https://console.aws.amazon.com/msk/)に移動し、[ステップ 1](#step-1-set-up-the-amazon-vpc-and-subnets) でセットアップしたものと同じリージョン、VPC、サブネットを使用して[クラスターを作成](https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html)し、次の設定に従ってください。

- **Kafka version**: TiDB Cloud がサポートするバージョンを使用します（例: 3.7.x）。
- **Broker type**: multi-VPC private connectivity でサポートされる broker type を選択します（`t3.small` は不可）。
- **Authentication**: SASL/SCRAM 認証を有効にします。
- **Public access**: このオプションを無効にします。
- **Number of brokers**: アベイラビリティゾーンごとに少なくとも 1つ（最小 3）。
- **Encryption in transit**: セキュリティ要件に応じて設定します。
- **Client subnets**: [ステップ 1](#step-1-set-up-the-amazon-vpc-and-subnets) で作成した 3つのプライベートサブネットを選択します。
- **Cluster configuration**: 次の設定を含むカスタム設定を作成します（初期 ACL セットアップに必要）。
    - `auto.create.topics.enable=true`
    - `allow.everyone.if.no.acl.found=true`

作成後、クラスターのステータスが **Active** になるまで待ち、クラスターの **Summary** セクションから **Cluster ARN** を記録します。

## ステップ 4. SCRAM シークレットを Amazon MSK Provisioned クラスターに関連付ける {#step-4-associate-the-scram-secret-with-the-amazon-msk-provisioned-cluster}

1. [Amazon MSK コンソール](https://console.aws.amazon.com/msk/)で、MSK クラスターの **Properties** タブに移動し、**SASL/SCRAM authentication** セクションを見つけます。
2. [ステップ 2](#step-2-create-a-scram-secret-in-aws-secrets-manager) で作成したシークレットをクラスターに[関連付け](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password-tutorial.html)ます。

関連付けが完了したら、ACL セットアップに進む前に、認証情報が反映されるまで約30秒待ってください。

## ステップ 5. Kafka ACL をセットアップする {#step-5-set-up-kafka-acls}

TiDB Cloud がクラスターにメッセージを生成するには Kafka ACL が必要です。ACL は、MSK クラスターと同じ VPC 内で作成する必要があります。

### 5.1 クライアント EC2 インスタンスを準備する {#51-prepare-a-client-ec2-instance}

1. [Amazon EC2 コンソール](https://console.aws.amazon.com/ec2/home#Instances)で、MSK クラスターと同じ VPC かつ同じサブネットのいずれか 1つに Amazon Linux EC2 インスタンスを起動します。

    > **Tip:**
    >
    > パブリックインターネットに SSH アクセスを公開せずにインスタンスへアクセスするには、[AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) を使用できます。

2. EC2 インスタンスで、Apache Kafka と OpenJDK のアーカイブをダウンロードして展開します。

    ```bash
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. OpenJDK を `PATH` 環境変数に追加します。

    ```bash
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    ```

### 5.2 SCRAM クライアント properties ファイルを作成する {#52-create-the-scram-client-properties-file}

EC2 インスタンスで、次の内容を含む `scram-client.properties` という名前のファイルを作成します。

```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="<your-scram-username>" \
    password="<your-scram-password>";
```

### 5.3 bootstrap broker string を取得する {#53-get-the-bootstrap-broker-string}

1. [Amazon MSK コンソール](https://console.aws.amazon.com/msk/)で、MSK クラスターの **Summary** セクションを開きます。
2. 右上の **View client information** をクリックします。
3. ダイアログで **SASL/SCRAM Private endpoint** エントリを見つけます。これが bootstrap broker string です。後で [ステップ 5.4](#54-create-the-acls) で使用するためにコピーしておきます。

### 5.4 ACL を作成する {#54-create-the-acls}

EC2 インスタンスで、次のコマンドを実行して、SCRAM ユーザーにすべてのトピック、consumer group、およびクラスターへのフルアクセスを付与します。

```bash
export BOOTSTRAP=<sasl-scram-private-endpoint>

/home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh \
  --bootstrap-server $BOOTSTRAP --command-config scram-client.properties \
  --add --allow-principal User:<scram-username> --operation All --topic '*'

/home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh \
  --bootstrap-server $BOOTSTRAP --command-config scram-client.properties \
  --add --allow-principal User:<scram-username> --operation All --group '*'

/home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh \
  --bootstrap-server $BOOTSTRAP --command-config scram-client.properties \
  --add --allow-principal User:<scram-username> --operation All --cluster
```

認証エラーが断続的に発生する場合は、数秒待ってから再試行してください。新しい SCRAM 認証情報がすべての broker に反映されるまで、少し時間がかかることがあります。

## ステップ 6. クラスター設定を更新する {#step-6-update-the-cluster-configuration}

ACL を作成した後、クラスター設定を次のように更新します。

- `auto.create.topics.enable` は `true` のままにします。
- `allow.everyone.if.no.acl.found` を `false` に設定します。

[Amazon MSK コンソール](https://console.aws.amazon.com/msk/)で、**Cluster configuration** の下に更新した設定を適用します。クラスターのステータスが **Active** に戻るまで待ちます。

## ステップ 7. multi-VPC connectivity を有効にする {#step-7-turn-on-multi-vpc-connectivity}

multi-VPC connectivity は、MSK クラスターへの PrivateLink アクセスを可能にする AWS の機能です。明示的に有効にする必要があります。

1. [Amazon MSK コンソール](https://console.aws.amazon.com/msk/)で、MSK クラスターの **Properties** タブに移動します。**Network settings** > **Multi-VPC connectivity** で、[multi-VPC connectivity を有効にします](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-turn-on.html)。
2. VPC connectivity のクライアント認証は **SASL/SCRAM** 認証のみを使用するように設定します（TiDB Cloud 接続には IAM および mutual TLS (mTLS) 認証は不要です）。

    クラスター更新が完了するまで待ちます。この操作には通常約 40 ～ 60分かかります。進行状況は MSK コンソールの **Cluster operations** タブで確認できます。クラスターのステータスが **Active** に戻るまで待ってください。

3. 更新完了後、次の項目を確認します。

    - Multi-VPC connectivity が有効になっていること。
    - `PublicAccess` が無効になっていること。
    - VPC connectivity で SASL/SCRAM 認証が有効になっていること。

## ステップ 8. クラスター ポリシーをアタッチする {#step-8-attach-a-cluster-policy}

リソースベースのクラスター ポリシーを MSK クラスターにアタッチして、TiDB Cloud Premium インスタンスに接続権限を付与します。

1. [Amazon MSK コンソール](https://console.aws.amazon.com/msk/) で、対象の MSK クラスターに移動します。
2. **Security settings** で、**Edit cluster policy** をクリックします。
3. クラスター ポリシー エディターに、リソースベースのクラスター ポリシーの JSON を貼り付け、**Save changes** をクリックします。

    > **Warning:**
    >
    > ポリシー内の `Principal` には、TiDB Cloud Premium インスタンスの AWS アカウント ID（[prerequisites](#prerequisites) で取得）を指定する必要があります。自分の AWS アカウント ID ではありません。誤った principal を指定すると、接続は失敗します。

    以下は参考用のポリシー例です。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "<tidb-cloud-aws-account-id>"
          },
          "Action": [
            "kafka:CreateVpcConnection",
            "kafka:GetBootstrapBrokers",
            "kafka:DescribeCluster",
            "kafka:DescribeClusterV2",
            "kafka-cluster:*"
          ],
          "Resource": "arn:aws:kafka:<region>:<account-id>:cluster/<cluster-name>/*"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "<tidb-cloud-aws-account-id>"
          },
          "Action": "kafka-cluster:*",
          "Resource": "arn:aws:kafka:<region>:<account-id>:topic/<cluster-name>/*"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "<tidb-cloud-aws-account-id>"
          },
          "Action": "kafka-cluster:*",
          "Resource": "arn:aws:kafka:<region>:<account-id>:group/<cluster-name>/*"
        }
      ]
    }
    ```

詳細については、[Attach a cluster policy to the MSK cluster](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html) を参照してください。

## ステップ 9. TiDB Cloud で PrivateLink 接続を作成する {#step-9-create-the-privatelink-connection-in-tidb-cloud}

[TiDB Cloud コンソール](https://tidbcloud.com) で、MSK クラスターの ARN を使用して private link 接続を作成します。

詳細については、[Amazon MSK Provisioned プライベートリンク接続を作成する](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md#step-2-configure-the-private-endpoint-for-changefeeds) を参照してください。