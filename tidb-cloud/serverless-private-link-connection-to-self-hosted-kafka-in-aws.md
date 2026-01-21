---
title: Connect to AWS Self-Hosted Kafka via Private Link Connection
summary: AWS エンドポイントサービスプライベートリンク接続を使用して AWS セルフホスト Kafka に接続する方法を学習します。
---

# プライベートリンク接続を介して AWS セルフホスト Kafka に接続する {#connect-to-aws-self-hosted-kafka-via-private-link-connection}

このドキュメントでは、 [AWS エンドポイントサービスプライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)を使用してTiDB Cloud Essential クラスターを AWS のセルフホスト型 Kafka クラスターに接続する方法について説明します。

このメカニズムは次のように機能します。

1.  プライベートリンク接続は、すべての Kafka ブローカーのアドレスとポートを返すブートストラップブローカーアドレスを使用して AWS エンドポイントサービスに接続します。
2.  TiDB Cloud は、返されたブローカー アドレスとポートを使用して、プライベート リンク接続を介して接続を確立します。
3.  AWS エンドポイントサービスは、リクエストをロードバランサーに転送します。
4.  ロード バランサーは、ポート マッピングに基づいて、対応する Kafka ブローカーにリクエストをルーティングします。

## 前提条件 {#prerequisites}

-   AWS アカウントで Kafka クラスターを設定するには、次の権限があることを確認してください。

    -   EC2インスタンスを管理する
    -   VPCを管理する
    -   サブネットを管理する
    -   EC2 インスタンスに接続して Kafka ノードを構成する

-   AWS アカウントでロードバランサーとエンドポイントサービスを設定するには、次の権限があることを確認してください。

    -   セキュリティ グループを管理する
    -   ロードバランサーを管理する
    -   エンドポイントサービスの管理

-   TiDB Cloud Essential は AWS でホストされており、アクティブです。後で使用するために、以下の詳細情報を取得して保存してください。

    -   AWSアカウントID
    -   可用性ゾーン（AZ）

AWS アカウント ID とアベイラビリティーゾーンを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。
2.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。
3.  表示されたダイアログで、AWS アカウント ID とアベイラビリティーゾーンを見つけることができます。

次の表は、展開情報の例を示しています。

| 情報                          | 価値                                                                                                                                                                                                                                                                                                                                                 | 注記                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| リージョン                       | オレゴン州 ( `us-west-2` )                                                                                                                                                                                                                                                                                                                              | 該当なし                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| TiDB Cloud AWS アカウントのプリンシパル | `arn:aws:iam::<account_id>:root`                                                                                                                                                                                                                                                                                                                   | 該当なし                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| AZ ID                       | <li>`usw2-az1` </li><li>`usw2-az2` </li><li> `usw2-az3`</li>                                                                                                                                                                                                                                                                                       | AZ ID を AWS アカウントの AZ 名に合わせます。<br/>例：<ul><li> `usw2-az1` =&gt; `us-west-2a`</li><li> `usw2-az2` =&gt; `us-west-2c`</li><li> `usw2-az3` =&gt; `us-west-2b`</li></ul>                                                                                                                                                                                                                                                                                                                                  |
| Kafka アドバタイズドリスナーパターン       | <li>`usw2-az1` =&gt; \<broker\_id> .usw2-az1.unique\_name.aws.plc.tidbcloud.com:\<port></port></broker\_id></li><li> `usw2-az2` =&gt; \<broker\_id> .usw2-az2.unique\_name.aws.plc.tidbcloud.com:\<port></port></broker\_id></li><li> `usw2-az3` =&gt; \<broker\_id> .usw2-az3.unique\_name.aws.plc.tidbcloud.com:\<port></port></broker\_id></li> | AZ 名を AZ 指定のパターンにマッピングします。後で、特定の AZ のブローカーに適切なパターンを設定してください。<ul><li> `us-west-2a` =&gt; &lt;ブローカーID&gt;.usw2-az1.unique_name.aws.plc.tidbcloud.com:&lt;ポート&gt;</li><li> `us-west-2c` =&gt; &lt;ブローカーID&gt;.usw2-az2.unique_name.aws.plc.tidbcloud.com:&lt;ポート&gt;</li><li> `us-west-2b` =&gt; &lt;ブローカーID&gt;.usw2-az3.unique_name.aws.plc.tidbcloud.com:&lt;ポート&gt;</li></ul> `unique_name`はプレースホルダーであり、 [ステップ4](#step-4-replace-the-unique-name-placeholder-in-kafka-configuration)の実際の値に置き換えられます。 |

## ステップ1. Kafkaクラスターをセットアップする {#step-1-set-up-a-kafka-cluster}

新しいクラスターをデプロイする必要がある場合は、 [新しいKafkaクラスターをデプロイ](#deploy-a-new-kafka-cluster)手順に従ってください。

既存のクラスターを公開する必要がある場合は、 [実行中の Kafka クラスターを再構成する](#reconfigure-a-running-kafka-cluster)手順に従ってください。

### 新しいKafkaクラスターをデプロイ {#deploy-a-new-kafka-cluster}

#### 1. Kafka VPC を設定する {#1-set-up-the-kafka-vpc}

Kafka VPC には次のものが必要です。

-   ブローカー用のプライベート サブネットが 3 つ (AZ ごとに 1 つ)。
-   任意の AZ に 1 つのパブリックサブネットがあり、インターネットに接続できる要塞ノードと 3 つのプライベートサブネットがあるため、Kafka クラスターを簡単にセットアップできます。本番環境では、Kafka VPC に接続できる独自の要塞ノードが必要になる場合があります。

サブネットを作成する前に、AZ IDとAZ名のマッピングに基づいてAZ内にサブネットを作成します。以下のマッピングを例に挙げます。

-   `usw2-az1` =&gt; `us-west-2a`
-   `usw2-az2` =&gt; `us-west-2c`
-   `usw2-az3` =&gt; `us-west-2b`

次の AZ にプライベート サブネットを作成します。

-   `us-west-2a`
-   `us-west-2c`
-   `us-west-2b`

Kafka VPC を作成するには、次の手順を実行します。

**1.1. Kafka VPCを作成する**

1.  [AWSコンソール &gt; VPCダッシュボード](https://console.aws.amazon.com/vpcconsole/home?#vpcs:)に進み、Kafka をデプロイするリージョンに切り替えます。

2.  **「VPCの作成」**をクリックします。VPC**設定**ページで以下の情報を入力します。

    1.  **VPC のみ**を選択します。
    2.  **名前タグ**にタグを入力します (例: `Kafka VPC` 。
    3.  **IPv4 CIDR 手動入力**を選択し、 IPv4 CIDR を入力します (例: `10.0.0.0/16` )。
    4.  その他のオプションはデフォルト値を使用します。 **「VPC の作成」を**クリックします。
    5.  VPC の詳細ページで、VPC ID (例: `vpc-01f50b790fa01dffa` ) をメモします。

**1.2. Kafka VPC にプライベートサブネットを作成する**

1.  [サブネット一覧ページ](https://console.aws.amazon.com/vpcconsole/home?#subnets:)に進みます。

2.  **[サブネットの作成]**をクリックします。

3.  前にメモしておいた**VPC ID** (この例では`vpc-01f50b790fa01dffa` ) を選択します。

4.  以下の情報を含む3つのサブネットを追加します。TiDB TiDB Cloud、ブローカー`advertised.listener`設定でAZ IDをエンコードする必要があるため、後でブローカーを設定する際に便利なように、サブネット名にAZ IDを含めることをお勧めします。

    -   サブネット`us-west-2a`
        -   **サブネット名**: `broker-usw2-az1`
        -   **可用性ゾーン**: `us-west-2a`
        -   **IPv4サブネットCIDRブロック**： `10.0.0.0/18`

    -   サブネット2 in `us-west-2c`
        -   **サブネット名**: `broker-usw2-az2`
        -   **可用性ゾーン**: `us-west-2c`
        -   **IPv4サブネットCIDRブロック**： `10.0.64.0/18`

    -   サブネット`us-west-2b`
        -   **サブネット名**: `broker-usw2-az3`
        -   **可用性ゾーン**: `us-west-2b`
        -   **IPv4サブネットCIDRブロック**： `10.0.128.0/18`

5.  **「サブネットの作成」を**クリックします。**サブネット一覧**ページが表示されます。

**1.3. Kafka VPC にパブリックサブネットを作成する**

1.  **[サブネットの作成]**をクリックします。

2.  前にメモしておいた**VPC ID** (この例では`vpc-01f50b790fa01dffa` ) を選択します。

3.  次の情報を使用して、任意の AZ にパブリック サブネットを追加します。

    -   **サブネット名**: `bastion`
    -   **IPv4サブネットCIDRブロック**： `10.0.192.0/18`

4.  要塞サブネットをパブリック サブネットに構成します。

    1.  [VPCダッシュボード &gt; インターネットゲートウェイ](https://console.aws.amazon.com/vpcconsole/home#igws:)に進みます。3 `kafka-vpc-igw`名前のインターネットゲートウェイを作成します。

    2.  **インターネット ゲートウェイの詳細**ページの**アクション**で、 **VPC に接続を**クリックして、インターネット ゲートウェイを Kafka VPC に接続します。

    3.  [VPCダッシュボード &gt; ルートテーブル](https://console.aws.amazon.com/vpcconsole/home#CreateRouteTable:)に進みます。Kafka VPC のインターネット ゲートウェイへのルート テーブルを作成し、次の情報を含む新しいルートを追加します。

        -   **名前**: `kafka-vpc-igw-route-table`
        -   **VPC** : `Kafka VPC`
        -   **ルート**:
            -   **目的地**： `0.0.0.0/0`
            -   **ターゲット**`kafka-vpc-igw` `Internet Gateway`

    4.  ルートテーブルを要塞サブネットに接続します。ルートテーブルの**詳細**ページで、 **「サブネットの関連付け」&gt;「サブネットの関連付けの編集」**をクリックし、要塞サブネットを追加して変更を保存します。

#### 2. Kafkaブローカーを設定する {#2-set-up-kafka-brokers}

**2.1. 要塞ノードを作成する**

[EC2 リストページ](https://console.aws.amazon.com/ec2/home#Instances:)に進みます。要塞サブネットに要塞ノードを作成します。

-   **名前**: `bastion-node`
-   **Amazon マシンイメージ**: `Amazon Linux`
-   **インスタンスタイプ**: `t2.small`
-   **キーペア**: `kafka-vpc-key-pair` 。 `kafka-vpc-key-pair`という名前の新しいキーペアを作成します。 `kafka-vpc-key-pair.pem`ローカルマシンにダウンロードして、後で設定します。
-   ネットワーク設定

    -   **VPC** : `Kafka VPC`
    -   **サブネット**: `bastion`
    -   **パブリックIPの自動割り当て**: `Enable`
    -   **Securityグループ**：どこからでもSSHログインを許可する新しいセキュリティグループを作成します。本番環境の安全性を考慮して、ルールを絞り込むことができます。

**2.2. ブローカーノードを作成する**

[EC2 リストページ](https://console.aws.amazon.com/ec2/home#Instances:)に進みます。ブローカー サブネットに、各 AZ に 1 つずつ、合計 3 つのブローカー ノードを作成します。

-   サブネット`broker-usw2-az1`のブローカー 1

    -   **名前**: `broker-node1`
    -   **Amazon マシンイメージ**: `Amazon Linux`
    -   **インスタンスタイプ**: `t2.large`
    -   **キーペア**：再利用`kafka-vpc-key-pair`
    -   ネットワーク設定

        -   **VPC** : `Kafka VPC`
        -   **サブネット**: `broker-usw2-az1`
        -   **パブリックIPの自動割り当て**: `Disable`
        -   **Securityグループ**: Kafka VPCからのTCPをすべて許可する新しいセキュリティグループを作成します。本番環境での安全性を考慮して、ルールを絞り込むことができます。
            -   **プロトコル**： `TCP`
            -   **ポート範囲**: `0 - 65535`
            -   **出典**: `10.0.0.0/16`

-   サブネット`broker-usw2-az2`のブローカー 2

    -   **名前**: `broker-node2`
    -   **Amazon マシンイメージ**: `Amazon Linux`
    -   **インスタンスタイプ**: `t2.large`
    -   **キーペア**：再利用`kafka-vpc-key-pair`
    -   ネットワーク設定

        -   **VPC** : `Kafka VPC`
        -   **サブネット**: `broker-usw2-az2`
        -   **パブリックIPの自動割り当て**: `Disable`
        -   **Securityグループ**: Kafka VPCからのTCPをすべて許可する新しいセキュリティグループを作成します。本番環境での安全性を考慮して、ルールを絞り込むことができます。
            -   **プロトコル**： `TCP`
            -   **ポート範囲**: `0 - 65535`
            -   **出典**: `10.0.0.0/16`

-   サブネット`broker-usw2-az3`のブローカー 3

    -   **名前**: `broker-node3`
    -   **Amazon マシンイメージ**: `Amazon Linux`
    -   **インスタンスタイプ**: `t2.large`
    -   **キーペア**：再利用`kafka-vpc-key-pair`
    -   ネットワーク設定

        -   **VPC** : `Kafka VPC`
        -   **サブネット**: `broker-usw2-az3`
        -   **パブリックIPの自動割り当て**: `Disable`
        -   **Securityグループ**: Kafka VPCからのTCPをすべて許可する新しいセキュリティグループを作成します。本番環境での安全性を考慮して、ルールを絞り込むことができます。
            -   **プロトコル**： `TCP`
            -   **ポート範囲**: `0 - 65535`
            -   **出典**: `10.0.0.0/16`

**2.3. Kafkaランタイムバイナリの準備**

1.  要塞ノードの詳細ページに移動します。**パブリックIPv4アドレス**を取得します。SSHを使用して、先ほどダウンロードした`kafka-vpc-key-pair.pem`を使用してノードにログインします。

    ```shell
    chmod 400 kafka-vpc-key-pair.pem
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{bastion_public_ip} # replace {bastion_public_ip} with the IP address of your bastion node, for example, 54.186.149.187
    scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem ec2-user@{bastion_public_ip}:~/
    ```

2.  バイナリをダウンロードします。

    ```shell
    # Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3.  バイナリを各ブローカー ノードにコピーします。

    ```shell
    # Replace {broker-node1-ip} with your broker-node1 IP address
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # Replace {broker-node2-ip} with your broker-node2 IP address
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # Replace {broker-node3-ip} with your broker-node3 IP address
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    ```

**2.4. 各ブローカーノードにKafkaノードを設定する**

**2.4.1 3つのノードを持つKRaft Kafkaクラスターをセットアップする**

各ノードはブローカーとコントローラーの役割を担います。各ブローカーに対して以下の操作を実行してください。

1.  `listeners`項目の場合、3 つのブローカーはすべて同じであり、ブローカーとコントローラーのロールとして機能します。

    1.  すべての**コントローラー**ロールノードに同じ CONTROLLER リスナーを設定します。**ブローカー**ロールノードのみを追加する場合は、 `server.properties`の CONTROLLER リスナーは必要ありません。
    2.  **ブローカー**リスナーを 2 つ構成します。3 `INTERNAL`は内部アクセス用、 `EXTERNAL`はTiDB Cloudからの外部アクセス用です。

2.  `advertised.listeners`項目については、次の操作を行います。

    1.  各ブローカーに対して、ブローカーノードの内部IPアドレスを使用して、INTERNALアドバタイズリスナーを設定します。アドバタイズされた内部Kafkaクライアントは、このアドレスを使用してブローカーにアクセスします。
    2.  TiDB Cloudから取得した**Kafkaアドバタイズリスナーパターン**に基づいて、各ブローカーノードに外部ア​​ドバタイズリスナーを設定することで、 TiDB Cloudが複数のブローカーを区別できるようになります。異なる外部アドバタイズリスナーを設定することで、 TiDB CloudのKafkaクライアントはリクエストを適切なブローカーにルーティングできるようになります。

        -   `<port>`ブローカーと Kafka プライベートリンクサービスのアクセスポイントを区別します。すべてのブローカーの EXTERNAL アドバタイズリスナーのポート範囲を計画してください。これらのポートは、ブローカーが実際にリッスンするポートである必要はありません。これらは、リクエストを別のブローカーに転送するプライベートリンクサービスのロードバランサーがリッスンするポートです。
        -   **Kafka アドバタイズドリスナーパターン**の`AZ ID` 、ブローカーがデプロイされている場所を示します。TiDB TiDB Cloud は、 AZ ID に基づいてリクエストを異なるエンドポイント DNS 名にルーティングします。

    トラブルシューティングを容易にするために、ブローカーごとに異なるブローカー ID を構成することをお勧めします。

3.  計画値は次のとおりです。

    -   **コントローラーポート**: `29092`
    -   **内部ポート**： `9092`
    -   **外部**: `39092`
    -   **外部アドバタイズリスナーポート範囲**: `9093~9095`

**2.4.2. 設定ファイルを作成する**

SSHを使用してすべてのブローカーノードにログインします。以下の内容の設定ファイル`~/config/server.properties`を作成します。

```properties
# brokers in usw2-az1

# broker-node1 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
# 2.1 The pattern for AZ(ID: usw2-az1) is "<broker_id>.usw2-az1.unique_name.aws.plc.tidbcloud.com:<port>".
# 2.2 So the EXTERNAL can be "b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9093) in the port range of the EXTERNAL advertised listener.
# 2.3 If there are more broker role nodes in the same AZ, you can configure them in the same way.
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az2

# broker-node2 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
# 2.1 The pattern for AZ(ID: usw2-az2) is "<broker_id>.usw2-az2.unique_name.aws.plc.tidbcloud.com:<port>".
# 2.2 So the EXTERNAL can be "b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9094) in the port range of the EXTERNAL advertised listener.
# 2.3 If there are more broker role nodes in the same AZ, you can configure them in the same way.
process.roles=broker,controller
node.id=2
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az3

# broker-node3 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
# 2.1 The pattern for AZ(ID: usw2-az3) is "<broker_id>.usw2-az3.unique_name.aws.plc.tidbcloud.com:<port>".
# 2.2 So the EXTERNAL can be "b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9095) in the port range of the EXTERNAL advertised listener.
# 2.3 If there are more broker role nodes in the same AZ, you can configure them in the same way.
process.roles=broker,controller
node.id=3
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

**2.4.3 Kafkaブローカーを起動する**

スクリプトを作成し、それを実行して各ブローカー ノードで Kafka ブローカーを起動します。

```shell
#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Set JAVA_HOME to the Java installation within the script directory
export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
# Define the vars
KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
KAFKA_STORAGE_CMD=$KAFKA_DIR/kafka-storage.sh
KAFKA_START_CMD=$KAFKA_DIR/kafka-server-start.sh
KAFKA_DATA_DIR=$SCRIPT_DIR/data
KAFKA_LOG_DIR=$SCRIPT_DIR/log
KAFKA_CONFIG_DIR=$SCRIPT_DIR/config

# Cleanup step, which makes it easy for multiple experiments
# Find all Kafka process IDs
KAFKA_PIDS=$(ps aux | grep 'kafka.Kafka' | grep -v grep | awk '{print $2}')
if [ -z "$KAFKA_PIDS" ]; then
  echo "No Kafka processes are running."
else
  # Kill each Kafka process
  echo "Killing Kafka processes with PIDs: $KAFKA_PIDS"
  for PID in $KAFKA_PIDS; do
    kill -9 $PID
    echo "Killed Kafka process with PID: $PID"
  done
  echo "All Kafka processes have been killed."
fi

rm -rf $KAFKA_DATA_DIR
mkdir -p $KAFKA_DATA_DIR
rm -rf $KAFKA_LOG_DIR
mkdir -p $KAFKA_LOG_DIR

# Magic id: BRl69zcmTFmiPaoaANybiw, you can use your own
$KAFKA_STORAGE_CMD format -t "BRl69zcmTFmiPaoaANybiw" -c "$KAFKA_CONFIG_DIR/server.properties" > $KAFKA_LOG_DIR/server_format.log   
LOG_DIR=$KAFKA_LOG_DIR nohup $KAFKA_START_CMD "$KAFKA_CONFIG_DIR/server.properties" &
```

**2.5. 要塞ノードでクラスター設定をテストする**

1.  Kafka ブートストラップをテストします。

    ```shell
    export JAVA_HOME=/home/ec2-user/jdk-22.0.2

    # Bootstrap from INTERNAL listener
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
    # Expected output (the actual order might be different)
    {broker-node1-ip}:9092 (id: 1 rack: null) -> (
    {broker-node2-ip}:9092 (id: 2 rack: null) -> (
    {broker-node3-ip}:9092 (id: 3 rack: null) -> (

    # Bootstrap from EXTERNAL listener
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
    # Expected output for the last 3 lines (the actual order might be different)
    # The difference in the output from "bootstrap from INTERNAL listener" is that exceptions or errors might occur because advertised listeners cannot be resolved in Kafka VPC.
    # We will make them resolvable on the TiDB Cloud side and route requests to the right broker when you create a changefeed that connects to this Kafka cluster via Private Link. 
    b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

2.  要塞ノードにプロデューサー スクリプト`produce.sh`を作成します。

    ```shell
    #!/bin/bash
    BROKER_LIST=$1 # "{broker_address1},{broker_address2}..."

    # Get the directory of the current script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # Set JAVA_HOME to the Java installation within the script directory
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    # Define the Kafka directory
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"

    # Create a topic if it does not exist
    create_topic() {
        echo "Creating topic if it does not exist..."
        $KAFKA_DIR/kafka-topics.sh --create --topic $TOPIC --bootstrap-server $BROKER_LIST --if-not-exists --partitions 3 --replication-factor 3
    }

    # Produce messages to the topic
    produce_messages() {
        echo "Producing messages to the topic..."
        for ((chrono=1; chrono <= 10; chrono++)); do
            message="Test message "$chrono
            echo "Create "$message
            echo $message | $KAFKA_DIR/kafka-console-producer.sh --broker-list $BROKER_LIST --topic $TOPIC
        done
    }
    create_topic
    produce_messages 
    ```

3.  要塞ノードにコンシューマー スクリプト`consume.sh`を作成します。

    ```shell
    #!/bin/bash

    BROKER_LIST=$1 # "{broker_address1},{broker_address2}..."

    # Get the directory of the current script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # Set JAVA_HOME to the Java installation within the script directory
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    # Define the Kafka directory
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"
    CONSUMER_GROUP="test-group"
    # Consume messages from the topic
    consume_messages() {
        echo "Consuming messages from the topic..."
        $KAFKA_DIR/kafka-console-consumer.sh --bootstrap-server $BROKER_LIST --topic $TOPIC --from-beginning --timeout-ms 5000 --consumer-property group.id=$CONSUMER_GROUP
    }
    consume_messages
    ```

4.  `produce.sh`と`consume.sh`を実行して、Kafkaクラスターが実行中であることを確認してください。これらのスクリプトは、後ほどネットワーク接続テストにも再利用されます。スクリプトは`--partitions 3 --replication-factor 3`のトピックを作成します。これら3つのブローカーすべてにデータが含まれていることを確認してください。ネットワーク接続がテストされることを保証するために、スクリプトが3つのブローカーすべてに接続することを確認してください。

    ```shell
    # Test write message. 
    ./produce.sh {one_of_broker_ip}:9092
    ```

    ```shell
    # Expected output
    Creating topic if it does not exist...

    Producing messages to the topic...
    Create Test message 1
    >>Create Test message 2
    >>Create Test message 3
    >>Create Test message 4
    >>Create Test message 5
    >>Create Test message 6
    >>Create Test message 7
    >>Create Test message 8
    >>Create Test message 9
    >>Create Test message 10
    ```

    ```shell
    # Test read message
    ./consume.sh {one_of_broker_ip}:9092
    ```

    ```shell
    # Expected example output (the actual message order might be different)
    Consuming messages from the topic...
    Test message 3
    Test message 4
    Test message 5
    Test message 9
    Test message 10
    Test message 6
    Test message 8
    Test message 1
    Test message 2
    Test message 7
    [2024-11-01 08:54:27,547] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
    org.apache.kafka.common.errors.TimeoutException
    Processed a total of 10 messages
    ```

### 実行中の Kafka クラスターを再構成する {#reconfigure-a-running-kafka-cluster}

Kafka クラスターが TiDB クラスターと同じリージョンおよび AZ にデプロイされていることを確認してください。ブローカーが異なる AZ にある場合は、正しい AZ に移動してください。

#### 1. ブローカーの外部リスナーを構成する {#1-configure-the-external-listener-for-brokers}

以下の設定はKafka KRaftクラスターに適用されます。ZKモードの設定も同様です。

1.  構成の変更を計画します。

    1.  TiDB Cloudからの外部アクセス用に、各ブローカーに EXTERNAL**リスナー**を設定します。EXTERNAL ポートとして、一意のポート（例： `39092` ）を選択します。
    2.  TiDB Cloudから取得した**Kafkaアドバタイズリスナーパターン**に基づいて、各ブローカーノードにEXTERNAL**アドバタイズリスナー**を設定することで、 TiDB Cloudが複数のブローカーを区別できるようになります。異なるEXTERNALアドバタイズリスナーを設定することで、TiDB CloudのKafkaクライアントはリクエストを適切なブローカーにルーティングできるようになります。

        -   `<port>`ブローカーと Kafka プライベートリンクサービスのアクセスポイントを区別します。すべてのブローカーの EXTERNAL アドバタイズリスナーのポート範囲を計画してください（例： `range from 9093` ）。これらのポートは、ブローカーが実際にリッスンするポートである必要はありません。これらは、リクエストを別のブローカーに転送するプライベートリンクサービスのロードバランサーがリッスンするポートです。
        -   **Kafka アドバタイズドリスナーパターン**の`AZ ID` 、ブローカーがデプロイされている場所を示します。TiDB TiDB Cloud は、 AZ ID に基づいてリクエストを異なるエンドポイント DNS 名にルーティングします。

    トラブルシューティングを容易にするために、ブローカーごとに異なるブローカー ID を構成することをお勧めします。

2.  SSHを使用して各ブローカーノードにログインします。各ブローカーの設定ファイルを以下の内容に変更します。

    ```properties
    # brokers in usw2-az1

    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
    # 1. The pattern for AZ(ID: usw2-az1) is "<broker_id>.usw2-az1.unique_name.aws.plc.tidbcloud.com:<port>"
    # 2. So the EXTERNAL can be "b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9093) in EXTERNAL advertised listener ports range 
    advertised.listeners=...,EXTERNAL://b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093

    # Configure EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

    ```properties
    # brokers in usw2-az2

    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
    # 1. The pattern for AZ(ID: usw2-az2) is "<broker_id>.usw2-az2.unique_name.aws.plc.tidbcloud.com:<port>"
    # 2. So the EXTERNAL can be "b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port(9094) in EXTERNAL advertised listener ports range.
    advertised.listeners=...,EXTERNAL://b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094

    # Configure EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

    ```properties
    # brokers in usw2-az3

    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
    # 1. The pattern for AZ(ID: usw2-az3) is "<broker_id>.usw2-az3.unique_name.aws.plc.tidbcloud.com:<port>"
    # 2. So the EXTERNAL can be "b2.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port(9095) in EXTERNAL advertised listener ports range.
    advertised.listeners=...,EXTERNAL://b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095

    # Configure EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

3.  すべてのブローカーを再構成したら、Kafka ブローカーを 1 つずつ再起動します。

#### 2. 内部ネットワークで外部リスナーの設定をテストする {#2-test-external-listener-settings-in-your-internal-network}

Kafka と OpenJDK を Kafka クライアント ノードにダウンロードできます。

```shell
# Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

次のスクリプトを実行して、ブートストラップが期待どおりに動作するかどうかをテストします。

```shell
export JAVA_HOME=/home/ec2-user/jdk-22.0.2

# Bootstrap from the EXTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# Expected output for the last 3 lines (the actual order might be different)
# There will be some exceptions or errors because advertised listeners cannot be resolved in your Kafka network. 
# We will make them resolvable on the TiDB Cloud side and route requests to the right broker when you create a changefeed that connects to this Kafka cluster via Private Link.
b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## ステップ2. Kafkaクラスターをプライベートリンクサービスとして公開する {#step-2-expose-the-kafka-cluster-as-a-private-link-service}

### 1. ロードバランサーを設定する {#1-set-up-the-load-balancer}

異なるポートを持つ4つのターゲットグループを持つネットワークロードバランサーを作成します。1つのターゲットグループはブートストラップ用で、他のターゲットグループは異なるブローカーにマッピングされます。

1.  ブートストラップターゲットグループ =&gt; 9092 =&gt; broker-node1:39092、broker-node2:39092、broker-node3:39092
2.  ブローカーターゲットグループ1 =&gt; 9093 =&gt; broker-node1:39092
3.  ブローカーターゲットグループ2 =&gt; 9094 =&gt; broker-node2:39092
4.  ブローカーターゲットグループ3 =&gt; 9095 =&gt; broker-node3:39092

ブローカーロールノードが複数ある場合は、マッピングを追加する必要があります。ブートストラップターゲットグループに少なくとも1つのノードがあることを確認してください。耐障害性を確保するため、各AZに1つずつ、合計3つのノードを追加することをお勧めします。

ロードバランサーを設定するには、次の手順を実行します。

1.  [対象グループ](https://console.aws.amazon.com/ec2/home#CreateTargetGroup:)に進み、4 つのターゲット グループを作成します。

    -   ブートストラップターゲットグループ

        -   **ターゲットタイプ**: `Instances`
        -   **対象グループ名**： `bootstrap-target-group`
        -   **プロトコル**： `TCP`
        -   **ポート**: `9092`
        -   **IPアドレスの種類**: `IPv4`
        -   **VPC** : `Kafka VPC`
        -   **ヘルスチェックプロトコル**： `TCP`
        -   `broker-node3:39092`**対象**`broker-node2:39092` `broker-node1:39092`

    -   ブローカーターゲットグループ1

        -   **ターゲットタイプ**: `Instances`
        -   **対象グループ名**： `broker-target-group-1`
        -   **プロトコル**： `TCP`
        -   **ポート**: `9093`
        -   **IPアドレスの種類**: `IPv4`
        -   **VPC** : `Kafka VPC`
        -   **ヘルスチェックプロトコル**： `TCP`
        -   **登録対象**: `broker-node1:39092`

    -   ブローカーターゲットグループ2

        -   **ターゲットタイプ**: `Instances`
        -   **対象グループ名**： `broker-target-group-2`
        -   **プロトコル**： `TCP`
        -   **ポート**: `9094`
        -   **IPアドレスの種類**: `IPv4`
        -   **VPC** : `Kafka VPC`
        -   **ヘルスチェックプロトコル**： `TCP`
        -   **登録対象**: `broker-node2:39092`

    -   ブローカーターゲットグループ3

        -   **ターゲットタイプ**: `Instances`
        -   **対象グループ名**： `broker-target-group-3`
        -   **プロトコル**： `TCP`
        -   **ポート**: `9095`
        -   **IPアドレスの種類**: `IPv4`
        -   **VPC** : `Kafka VPC`
        -   **ヘルスチェックプロトコル**： `TCP`
        -   **登録対象**: `broker-node3:39092`

2.  [ロードバランサー](https://console.aws.amazon.com/ec2/home#LoadBalancers:)に進み、ネットワーク ロード バランサーを作成します。

    -   **ロードバランサー名**: `kafka-lb`
    -   **スキーマ**: `Internal`
    -   **ロードバランサーのIPアドレスタイプ**: `IPv4`
    -   **VPC** : `Kafka VPC`
    -   **可用性ゾーン**:
        -   `usw2-az1`と`broker-usw2-az1 subnet`
        -   `usw2-az2`と`broker-usw2-az2 subnet`
        -   `usw2-az3`と`broker-usw2-az3 subnet`
    -   **Securityグループ**: 次のルールで新しいセキュリティ グループを作成します。
        -   受信ルールは、Kafka VPCからのすべてのTCPを許可します：タイプ - `{ports of target groups}` （例： `9092-9095` ）、ソース - `{CIDR of TiDB Cloud}` 。リージョン内のTiDB CloudのCIDRを取得するには、 [TiDB Cloudコンソール](https://tidbcloud.com)の左上隅にあるコンボボックスを使用してターゲットプロジェクトに切り替え、左側のナビゲーションペインで**[プロジェクト設定]** &gt; **[ネットワークアクセス**]をクリックし、 **[プロジェクトCIDR]** &gt; **[AWS]**をクリックします。
        -   アウトバウンドルールは、Kafka VPC へのすべての TCP を許可します: タイプ - `All TCP` 、宛先 - `Anywhere-IPv4`
    -   リスナーとルーティング:
        -   プロトコル: `TCP` ; ポート: `9092` ; 転送先: `bootstrap-target-group`
        -   プロトコル: `TCP` ; ポート: `9093` ; 転送先: `broker-target-group-1`
        -   プロトコル: `TCP` ; ポート: `9094` ; 転送先: `broker-target-group-2`
        -   プロトコル: `TCP` ; ポート: `9095` ; 転送先: `broker-target-group-3`

3.  要塞ノードでロードバランサーをテストします。この例では、Kafka ブートストラップのみをテストします。ロードバランサーは Kafka EXTERNAL リスナーをリッスンしているため、EXTERNAL アドバタイズされたリスナーのアドレスは要塞ノードでは解決できません。ロードバランサーの詳細ページから`kafka-lb` DNS 名（例： `kafka-lb-77405fa57191adcb.elb.us-west-2.amazonaws.com` ）をメモしておいてください。要塞ノードでスクリプトを実行してください。

    ```shell
    # Replace {lb_dns_name} to your actual value
    export JAVA_HOME=/home/ec2-user/jdk-22.0.2
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {lb_dns_name}:9092

    # Expected output for the last 3 lines (the actual order might be different)
    b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException

    # You can also try bootstrap in other ports 9093/9094/9095. It will succeed probabilistically because NLB in AWS resolves LB DNS to the IP address of any availability zone and disables cross-zone load balancing by default. 
    # If you enable cross-zone load balancing in LB, it will succeed. However, it is unnecessary and might cause additional cross-AZ traffic.
    ```

### 2. AWSエンドポイントサービスを設定する {#2-set-up-an-aws-endpoint-service}

1.  [エンドポイントサービス](https://console.aws.amazon.com/vpcconsole/home#EndpointServices:)に進みます。 **「エンドポイント サービスの作成」**をクリックして、Kafka ロード バランサーのプライベート リンク サービスを作成します。

    -   **名前**: `kafka-pl-service`
    -   **ロードバランサータイプ**: `Network`
    -   **ロードバランサー**： `kafka-lb`
    -   `usw2-az2` `usw2-az3`**アベイラビリティゾーン**: `usw2-az1`
    -   **エンドポイントの承認が必要**: `Acceptance required`
    -   **プライベートDNS名を有効にする**： `No`

2.  **サービス名**をメモしておいてください。TiDB TiDB Cloudに提供する必要があります（例`com.amazonaws.vpce.us-west-2.vpce-svc-0f49e37e1f022cd45` ）。

3.  kafka-pl-service の詳細ページで、 **「Allow principals」**タブをクリックし、 [前提条件](#prerequisites)で取得した AWS アカウント ID (例: `arn:aws:iam::<account_id>:root`を許可リストに追加します。

## ステップ3. TiDB Cloudでプライベートリンク接続を作成する {#step-3-create-a-private-link-connection-in-tidb-cloud}

TiDB Cloudでプライベート リンク接続を作成するには、次の手順を実行します。

1.  [ステップ2](#2-set-up-an-aws-endpoint-service)で取得した AWS エンドポイントサービス名 (例: `com.amazonaws.vpce.<region>.vpce-svc-xxxx` ) を使用して、 TiDB Cloudにプライベートリンク接続を作成します。

    詳細については[AWS エンドポイントサービスプライベートリンク接続を作成する](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection)参照してください。

2.  TiDB Cloudのデータフロー サービスが Kafka クラスターにアクセスできるように、プライベート リンク接続にドメインをアタッチします。

    詳細については、 [プライベートリンク接続にドメインを添付する](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection)を参照してください。 **「ドメインのアタッチ」**ダイアログで、ドメインの種類として**「TiDB Cloud Managed」**を選択し、生成されたドメインの一意の名前を後で使用するためにコピーする必要があることに注意してください。

## ステップ4. Kafka設定内の一意の名前プレースホルダーを置き換える {#step-4-replace-the-unique-name-placeholder-in-kafka-configuration}

1.  Kafka ブローカー ノードに戻り、各ブローカーの`advertised.listeners`構成内の`unique_name`プレースホルダーを、前の手順で取得した実際の一意の名前に置き換えます。
2.  すべてのブローカーを再構成したら、Kafka ブローカーを 1 つずつ再起動します。

これで、このプライベート リンク接続と 9092 をブートストラップ ポートとして使用し、 TiDB Cloudから Kafka クラスターに接続できるようになります。
