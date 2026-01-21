---
title: Connect to Alibaba Cloud Self-Hosted Kafka via Private Link Connection
summary: Alibaba Cloud Endpoint Service のプライベート リンク接続を使用して、Alibaba Cloud セルフホスト型 Kafka に接続する方法を学習します。
---

# プライベートリンク接続を介して Alibaba Cloud Self-Hosted Kafka に接続する {#connect-to-alibaba-cloud-self-hosted-kafka-via-a-private-link-connection}

このドキュメントでは、 [Alibaba Cloud Endpoint Service プライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)を使用して、 TiDB Cloud Essential クラスターを Alibaba Cloud 内のセルフホスト型 Kafka クラスターに接続する方法について説明します。

このメカニズムは次のように機能します。

1.  プライベート リンク接続は、 `advertised.listeners`で定義されたブローカー外部アドレスを返すブートストラップ ポートを使用して Alibaba Cloud エンドポイント サービスに接続します。
2.  プライベート リンク接続は、ブローカーの外部アドレスを使用してエンドポイント サービスに接続します。
3.  Alibaba Cloud エンドポイント サービスは、リクエストをロード バランサーに転送します。
4.  ロード バランサーは、ポート マッピングに基づいて、対応する Kafka ブローカーにリクエストを転送します。

たとえば、ポート マッピングは次のようになります。

| ブローカー外部アドレスポート | ロードバランサーのリスナーポート | ロードバランサバックエンドサーバー |
| -------------- | ---------------- | ----------------- |
| 9093           | 9093             | ブローカーノード1:39092   |
| 9094           | 9094             | ブローカーノード2:39092   |
| 9095           | 9095             | ブローカーノード3:39092   |

## 前提条件 {#prerequisites}

-   Kafka クラスターがあること、またはクラスターを設定するための次の権限があることを確認します。

    -   ECSノードを管理する
    -   VPCとvSwitchを管理する
    -   ECS ノードに接続して Kafka ノードを構成する

-   Alibaba Cloud アカウントでロードバランサーとエンドポイント サービスを設定するには、次の権限があることを確認してください。

    -   ロードバランサーを管理する
    -   エンドポイントサービスの管理

-   TiDB Cloud EssentialはAlibaba Cloudでホストされており、アクティブです。後で使用するために、以下の詳細情報を取得して保存してください。

    -   Alibaba CloudアカウントID
    -   可用性ゾーン（AZ）

Alibaba Cloud アカウント ID とアベイラビリティーゾーンを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。
2.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。
3.  表示されたダイアログで、Alibaba Cloud アカウント ID とアベイラビリティーゾーンを見つけることができます。

次の表は、展開情報の例を示しています。

| 情報                             | 価値                                                                                | 注記                                                                                                                    |
| ------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| リージョン                          | `ap-southeast-1`                                                                  | 該当なし                                                                                                                  |
| TiDB Cloud Alibaba Cloud アカウント | `<account_id>`                                                                    | 該当なし                                                                                                                  |
| AZ ID                          | <li>`ap-southeast-1a` </li><li>`ap-southeast-1b` </li><li> `ap-southeast-1c`</li> | 該当なし                                                                                                                  |
| Kafka アドバタイズドリスナーパターン          | &lt;ブローカーID&gt;.unique_name.alicloud.plc.tidbcloud.com:&lt;ポート&gt;                | `unique_name`はプレースホルダーであり、 [ステップ4](#step-4-replace-the-unique-name-placeholder-in-kafka-configuration)の実際の値に置き換えられます。 |

## ステップ1. Kafkaクラスターをセットアップする {#step-1-set-up-a-kafka-cluster}

新しいクラスターをデプロイする必要がある場合は、 [新しいKafkaクラスターをデプロイ](#deploy-a-new-kafka-cluster)手順に従ってください。

既存のクラスターを公開する必要がある場合は、 [実行中の Kafka クラスターを再構成する](#reconfigure-a-running-kafka-cluster)手順に従ってください。

### 新しいKafkaクラスターをデプロイ {#deploy-a-new-kafka-cluster}

#### 1. Kafka VPC を設定する {#1-set-up-the-kafka-vpc}

Kafka VPC には次のものが必要です。

-   ブローカー用のプライベート vSwitch が 3 つ (AZ ごとに 1 つ)。
-   任意の AZ にパブリック vSwitch を 1 つ、インターネットに接続できる Bastion ノードを 1 つ、プライベート vSwitch を 3 つ配置することで、Kafka クラスターを簡単にセットアップできます。本番環境では、Kafka VPC に接続できる独自の Bastion ノードを配置することもできます。

Kafka VPC を作成するには、次の手順を実行します。

**1.1. Kafka VPCを作成する**

1.  [Alibaba Cloud コンソール &gt; VPC ダッシュボード](https://vpc.console.alibabacloud.com/vpc)に進み、Kafka をデプロイするリージョンに切り替えます。

2.  **「VPCの作成」**をクリックします。VPC**設定**ページで以下の情報を入力します。

    1.  **名前**を入力します (例: `Kafka VPC` )。

    2.  TiDB Cloudでプライベート リンク接続を設定するリージョンを選択します。

    3.  **[IPv4 CIDR ブロックを手動で入力]**を選択し、IPv4 CIDR (例: `10.0.0.0/16`を入力します。

    4.  Kafkaブローカーをデプロイする各AZごとにvSwitchを作成し、IPv4 CIDRを設定します。例：

        -   broker-ap-southeast-1a vSwitch `ap-southeast-1a` : 10.0.0.0/18
        -   broker-ap-southeast-1b vSwitch `ap-southeast-1b` : 10.0.64.0/18
        -   broker-ap-southeast-1c vSwitch `ap-southeast-1c` : 10.0.128.0/18
        -   `ap-southeast-1a`の bastion vSwitch: 10.0.192.0/18

    5.  その他のオプションはデフォルト値を使用します。 **「OK」**をクリックします。

3.  VPC の詳細ページで、VPC ID (例: `vpc-t4nfx2vcqazc862e9fg06` ) をメモします。

#### 2. Kafkaブローカーを設定する {#2-set-up-kafka-brokers}

**2.1. 要塞ノードを作成する**

[ECSコンソール](https://ecs.console.alibabacloud.com/home#/)に進みます。要塞 vSwitch に要塞ノードを作成します。

-   **ネットワークとゾーン**: `Kafka VPC`および`bastion` vSwitch。
-   **インスタンスとイメージ**: インスタンス タイプが`ecs.t5-lc1m2.small` 、イメージが`Alibaba Cloud Linux` 。
-   **ネットワークとSecurityグループ**: `Assign Public IPv4 Address`を選択します。
-   **キーペア**: `kafka-vpc-key-pair` 。 `kafka-vpc-key-pair`という名前の新しいキーペアを作成します。 `kafka-vpc-key-pair.pem`ローカルマシンにダウンロードして、後で設定します。
-   **Securityグループ**：どこからでもSSHログインを許可する新しいセキュリティグループを作成します。本番環境の安全性を確保するために、ルールを絞り込むことができます。
-   **インスタンス名**: `bastion-node` 。

**2.2. ブローカーノードを作成する**

[ECSコンソール](https://ecs.console.alibabacloud.com/home#/)に進みます。vSwitch に 3 つのブローカー ノード (AZ ごとに 1 つ) を作成します。

-   vSwitch 1 のブローカー`broker-ap-southeast-1a`

    -   **ネットワークとゾーン**: `Kafka VPC`および`broker-ap-southeast-1a` vSwitch
    -   **インスタンスとイメージ**: `ecs.t5-lc1m2.small`インスタンスタイプと`Alibaba Cloud Linux`イメージ
    -   **キーペア**:再利用`kafka-vpc-key-pair` 。
    -   **インスタンス名**: `broker-node1`
    -   **Securityグループ**: Kafka VPCからのすべてのTCPを許可する新しいセキュリティグループを作成します。本番環境では、安全性を考慮してルールを絞り込むことができます。インバウンドルール: -**プロトコル**: `TCP` -**ポート範囲**: `All` -**ソース**: `10.0.0.0/16`

-   vSwitch `broker-ap-southeast-1b`のブローカー 2

    -   **ネットワークとゾーン**: `Kafka VPC`および`broker-ap-southeast-1b` vSwitch
    -   **インスタンスとイメージ**: `ecs.t5-lc1m2.small`インスタンスタイプと`Alibaba Cloud Linux`イメージ
    -   **キーペア**:再利用`kafka-vpc-key-pair` 。
    -   **インスタンス名**: `broker-node2`
    -   **Securityグループ**: Kafka VPCからのすべてのTCPを許可する新しいセキュリティグループを作成します。本番環境では、安全性を考慮してルールを絞り込むことができます。インバウンドルール: -**プロトコル**: `TCP` -**ポート範囲**: `All` -**ソース**: `10.0.0.0/16`

-   vSwitch `broker-ap-southeast-1c`のブローカー 3

    -   **ネットワークとゾーン**: `Kafka VPC`および`broker-ap-southeast-1c` vSwitch
    -   **インスタンスとイメージ**: `ecs.t5-lc1m2.small`インスタンスタイプと`Alibaba Cloud Linux`イメージ
    -   **キーペア**:再利用`kafka-vpc-key-pair` 。
    -   **インスタンス名**: `broker-node3`
    -   **Securityグループ**: Kafka VPCからのすべてのTCPを許可する新しいセキュリティグループを作成します。本番環境では、安全性を考慮してルールを絞り込むことができます。インバウンドルール: -**プロトコル**: `TCP` -**ポート範囲**: `All` -**ソース**: `10.0.0.0/16`

**2.3. Kafkaランタイムバイナリの準備**

1.  要塞ノードの詳細ページに移動します。**パブリックIPv4アドレス**を取得します。SSHを使用して、先ほどダウンロードした`kafka-vpc-key-pair.pem`を使用してノードにログインします。

    ```shell
    chmod 400 kafka-vpc-key-pair.pem
    scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem root@{bastion_public_ip}:~/ # replace {bastion_public_ip} with the IP address of your bastion node
    ssh -i "kafka-vpc-key-pair.pem" root@{bastion_public_ip}
    ```

2.  バイナリを要塞ノードにダウンロードします。

    ```shell
    # Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3.  要塞ノードから各ブローカー ノードにバイナリをコピーします。

    ```shell
    # Replace {broker-node1-ip} with your broker-node1 IP address
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz root@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node1-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz root@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node1-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # Replace {broker-node2-ip} with your broker-node2 IP address
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz root@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node2-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz root@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node2-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # Replace {broker-node3-ip} with your broker-node3 IP address
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz root@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node3-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz root@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node3-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
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
# brokers in ap-southeast-1a

# broker-node1 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
# 2.1 The pattern is "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>".
# 2.2 If there are more broker role nodes, you can configure them in the same way.
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.unique_name.alicloud.plc.tidbcloud.com:9093
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in ap-southeast-1b

# broker-node2 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
# 2.1 The pattern is "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>".
# 2.2 If there are more broker role nodes, you can configure them in the same way.
process.roles=broker,controller
node.id=2
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.unique_name.alicloud.plc.tidbcloud.com:9094
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in ap-southeast-1c

# broker-node3 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
# 2.1 The pattern is "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>".
# 2.2 If there are more broker role nodes, you can configure them in the same way.
process.roles=broker,controller
node.id=3
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.ap-southeast-1c.unique_name.alicloud.plc.tidbcloud.com:9095
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
    export JAVA_HOME=~/jdk-22.0.2

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
    b1.unique_name.alicloud.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.unique_name.alicloud.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.unique_name.alicloud.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
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
    sh produce.sh {one_of_broker_ip}:9092
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
    sh consume.sh {one_of_broker_ip}:9092
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

    トラブルシューティングを容易にするために、ブローカーごとに異なるブローカー ID を構成することをお勧めします。

2.  SSHを使用して各ブローカーノードにログインします。各ブローカーの設定ファイルを以下の内容に変更します。

    ```properties
    # brokers in ap-southeast-1a

    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
    # 1. The pattern is "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"
    # 2. So the EXTERNAL can be "b1.unique_name.alicloud.plc.tidbcloud.com:9093", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9093) in EXTERNAL advertised listener ports range 
    advertised.listeners=...,EXTERNAL://b1.unique_name.alicloud.plc.tidbcloud.com:9093

    # Configure EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

    ```properties
    # brokers in ap-southeast-1b

    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
    # 1. The pattern is "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"
    # 2. So the EXTERNAL can be "b2.unique_name.alicloud.plc.tidbcloud.com:9094". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port(9094) in EXTERNAL advertised listener ports range.
    advertised.listeners=...,EXTERNAL://b2.unique_name.alicloud.plc.tidbcloud.com:9094

    # Configure EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

    ```properties
    # brokers in ap-southeast-1c

    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
    # 1. The pattern is "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"
    # 2. So the EXTERNAL can be "b2.unique_name.alicloud.plc.tidbcloud.com:9095". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port(9095) in EXTERNAL advertised listener ports range.
    advertised.listeners=...,EXTERNAL://b3.unique_name.alicloud.plc.tidbcloud.com:9095

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
export JAVA_HOME=/root/jdk-22.0.2

# Bootstrap from the EXTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# Expected output for the last 3 lines (the actual order might be different)
# There will be some exceptions or errors because advertised listeners cannot be resolved in your Kafka network. 
# We will make them resolvable on the TiDB Cloud side and route requests to the right broker when you create a changefeed that connects to this Kafka cluster via Private Link.
b1.ap-southeast-1a.unique_name.alicloud.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.ap-southeast-1b.unique_name.alicloud.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.ap-southeast-1c.unique_name.alicloud.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## ステップ2. Kafkaクラスターをプライベートリンクサービスとして公開する {#step-2-expose-the-kafka-cluster-as-a-private-link-service}

### 1. ロードバランサーを設定する {#1-set-up-the-load-balancer}

異なるポートを持つ4つのサーバーグループを持つネットワークロードバランサーを作成します。1つのサーバーグループはブートストラップ用で、他のサーバーグループは異なるブローカーにマッピングされます。

1.  ブートストラップサーバーグループ =&gt; 9092 =&gt; broker-node1:39092、broker-node2:39092、broker-node3:39092
2.  ブローカーサーバーグループ 1 =&gt; 9093 =&gt; broker-node1:39092
3.  ブローカーサーバーグループ 2 =&gt; 9094 =&gt; broker-node2:39092
4.  ブローカーサーバーグループ 3 =&gt; 9095 =&gt; broker-node3:39092

ブローカーロールノードが複数ある場合は、マッピングを追加する必要があります。ブートストラップターゲットグループに少なくとも1つのノードがあることを確認してください。耐障害性を確保するため、各AZに1つずつ、合計3つのノードを追加することをお勧めします。

ロードバランサーを設定するには、次の手順を実行します。

1.  [サーバーグループ](https://slb.console.alibabacloud.com/nlb/ap-southeast-1/server-groups)に進み、4 つのサーバーグループを作成します。

    -   ブートストラップサーバーグループ

        -   **サーバーグループタイプ**: `Server`を選択
        -   **サーバーグループ名**: `bootstrap-server-group`
        -   **VPC** : `Kafka VPC`
        -   **バックエンドサーバープロトコル**: `TCP`を選択
        -   **バックエンドサーバー**: 作成したサーバーグループをクリックし、 `broker-node1:39092` `broker-node3:39092`含むバックエンドサーバーを追加します`broker-node2:39092`

    -   ブローカーサーバーグループ1

        -   **サーバーグループタイプ**: `Server`を選択
        -   **サーバーグループ名**: `broker-server-group-1`
        -   **VPC** : `Kafka VPC`
        -   **バックエンドサーバープロトコル**: `TCP`を選択
        -   **バックエンドサーバー**: 作成したサーバーグループをクリックし、バックエンドサーバー`broker-node1:39092`を追加します。

    -   ブローカーサーバーグループ2

        -   **サーバーグループタイプ**: `Server`を選択
        -   **サーバーグループ名**: `broker-server-group-2`
        -   **VPC** : `Kafka VPC`
        -   **バックエンドサーバープロトコル**: `TCP`を選択
        -   **バックエンドサーバー**: 作成したサーバーグループをクリックし、バックエンドサーバー`broker-node2:39092`を追加します。

    -   ブローカーサーバーグループ3

        -   **サーバーグループタイプ**: `Server`を選択
        -   **サーバーグループ名**: `broker-server-group-3`
        -   **VPC** : `Kafka VPC`
        -   **バックエンドサーバープロトコル**: `TCP`を選択
        -   **バックエンドサーバー**: 作成したサーバーグループをクリックし、バックエンドサーバー`broker-node3:39092`を追加します。

2.  [ナショナルリーグ](https://slb.console.alibabacloud.com/nlb)に進み、ネットワーク ロード バランサーを作成します。

    -   **ネットワークタイプ**: `Internal-facing`を選択
    -   **VPC** : `Kafka VPC`
    -   **ゾーン**:
        -   `ap-southeast-1a`と`broker-ap-southeast-1a vswitch`
        -   `ap-southeast-1b`と`broker-ap-southeast-1b vswitch`
        -   `ap-southeast-1c`と`broker-ap-southeast-1c vswitch`
    -   **IPバージョン**: `IPv4`を選択
    -   **インスタンス名**: `kafka-nlb`
    -   **「今すぐ作成」**をクリックしてロードバランサーを作成します。

3.  作成したロード バランサーを見つけて、 **[リスナーの作成]**をクリックして 4 つの TCP リスナーを作成します。

    -   ブートストラップサーバーグループ

        -   **リスナープロトコル**: `TCP`を選択
        -   **リスナーポート**: `9092`
        -   **サーバー グループ**: 以前に作成したサーバーグループ`bootstrap-server-group`を選択します。

    -   ブローカーサーバーグループ1

        -   **リスナープロトコル**: `TCP`を選択
        -   **リスナーポート**: `9093`
        -   **サーバー グループ**: 以前に作成したサーバーグループ`broker-server-group-1`を選択します。

    -   ブローカーサーバーグループ2

        -   **リスナープロトコル**: `TCP`を選択
        -   **リスナーポート**: `9094`
        -   **サーバー グループ**: 以前に作成したサーバーグループ`broker-server-group-2`を選択します。

    -   ブローカーサーバーグループ3

        -   **リスナープロトコル**: `TCP`を選択
        -   **リスナーポート**: `9095`
        -   **サーバー グループ**: 以前に作成したサーバーグループ`broker-server-group-3`を選択します。

4.  要塞ノードでロードバランサーをテストします。この例では、Kafka ブートストラップのみをテストします。ロードバランサーは Kafka EXTERNAL リスナーをリッスンしているため、EXTERNAL アドバタイズされたリスナーのアドレスは要塞ノードでは解決できません。ロードバランサーの詳細ページから`kafka-lb` DNS 名（例： `nlb-o21d6wyjknamw8hjxb.ap-southeast-1.nlb.aliyuncsslbintl.com` ）をメモしておいてください。要塞ノードでスクリプトを実行してください。

    ```shell
    # Replace {lb_dns_name} to your actual value
    export JAVA_HOME=~/jdk-22.0.2
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {lb_dns_name}:9092

    # Expected output for the last 3 lines (the actual order might be different)
    b1.unique_name.alicloud.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.unique_name.alicloud.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.unique_name.alicloud.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

### 2. Alibaba Cloudエンドポイントサービスを設定する {#2-set-up-an-alibaba-cloud-endpoint-service}

同じリージョンにエンドポイント サービスを設定します。

1.  エンドポイント サービスを作成するには、 [エンドポイントサービス](https://vpc.console.alibabacloud.com/endpointservice)に進みます。

    -   **サービスリソースタイプ**: `NLB`選択
    -   **サービス リソースの選択**: NLB が含まれるすべてのゾーンを選択し、前の手順で作成した NLB を選択します。
    -   **エンドポイント接続を自動的に受け入れる**: `No`選択することをお勧めします

2.  エンドポイントサービスの詳細ページに移動し、**エンドポイントサービス名**（例： `com.aliyuncs.privatelink.<region>.xxxxx` ）をコピーします。これは後でTiDB Cloudで使用する必要があります。

3.  エンドポイントサービスの詳細ページで、「**サービスホワイトリスト」**タブをクリックし、 **「ホワイトリストに追加」**をクリックして、 [前提条件](#prerequisites)で取得した Alibaba Cloud アカウント ID を入力します。

## ステップ3. TiDB Cloudでプライベートリンク接続を作成する {#step-3-create-a-private-link-connection-in-tidb-cloud}

TiDB Cloudでプライベート リンク接続を作成するには、次の手順を実行します。

1.  [ステップ2](#2-set-up-an-alibaba-cloud-endpoint-service)で取得した Alibaba Cloud エンドポイント サービス名 (例: `com.aliyuncs.privatelink.<region>.xxxxx` ) を使用して、 TiDB Cloudにプライベート リンク接続を作成します。

    詳細については[Alibaba Cloud Endpoint Service のプライベートリンク接続を作成する](/tidb-cloud/serverless-private-link-connection.md#create-an-alibaba-cloud-endpoint-service-private-link-connection)参照してください。

2.  TiDB Cloudのデータフロー サービスが Kafka クラスターにアクセスできるように、プライベート リンク接続にドメインをアタッチします。

    詳細については、 [プライベートリンク接続にドメインを添付する](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection)を参照してください。 **「ドメインのアタッチ」**ダイアログで、ドメインの種類として**「TiDB Cloud Managed」**を選択し、生成されたドメインの一意の名前を後で使用するためにコピーする必要があることに注意してください。

## ステップ4. Kafka設定内の一意の名前プレースホルダーを置き換える {#step-4-replace-the-unique-name-placeholder-in-kafka-configuration}

1.  Kafka ブローカー ノードに戻り、各ブローカーの`advertised.listeners`構成内の`unique_name`プレースホルダーを、前の手順で取得した実際の一意の名前に置き換えます。
2.  すべてのブローカーを再構成したら、Kafka ブローカーを 1 つずつ再起動します。

これで、このプライベート リンク接続と 9092 をブートストラップ ポートとして使用し、 TiDB Cloudから Kafka クラスターに接続できるようになります。
