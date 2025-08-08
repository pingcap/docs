---
title: Set Up Self-Hosted Kafka Private Service Connect in Google Cloud
summary: このドキュメントでは、Google Cloud でセルフホスト型 Kafka 用に Private Service Connect を設定し、それをTiDB Cloudで動作させる方法について説明します。
---

# Google Cloud でセルフホスト型 Kafka プライベート サービス接続を設定する {#set-up-self-hosted-kafka-private-service-connect-in-google-cloud}

このドキュメントでは、Google Cloud でセルフホスト型 Kafka 用に Private Service Connect を設定する方法と、それをTiDB Cloudで動作させる方法について説明します。

このメカニズムは次のように機能します。

1.  TiDB Cloud VPC は、プライベート エンドポイントを介して Kafka VPC に接続します。
2.  Kafka クライアントはすべての Kafka ブローカーと直接通信する必要があります。
3.  各 Kafka ブローカーは、 TiDB Cloud VPC 内の一意のポートにマッピングされます。
4.  マッピングを実現するには、Kafka ブートストラップ メカニズムと Google Cloud リソースを活用します。

Google Cloud でセルフホスト型 Kafka に Private Service Connect を設定するには、次の 2 つの方法があります。

-   Private Service Connect（PSC）ポートマッピングメカニズムを使用します。この方法では、静的なポートブローカーマッピング設定が必要です。EXTERNALリスナーとアドバタイズリスナーのグループを追加するには、既存のKafkaクラスターを再構成する必要があります。1 [PSC ポート マッピングによるセルフホスト型 Kafka Private Service Connect サービスの設定](#set-up-self-hosted-kafka-private-service-connect-service-by-psc-port-mapping)参照してください。

-   [Kafkaプロキシ](https://github.com/grepplabs/kafka-proxy)使用してください。この方法では、Kafka クライアントと Kafka ブローカー間のプロキシとして、追加の実行プロセスが導入されます。プロキシはポートとブローカーのマッピングを動的に設定し、リクエストを転送します。既存の Kafka クラスターを再設定する必要はありません。3 [Kafka-proxy によるセルフホスト型 Kafka プライベート サービス接続のセットアップ](#set-up-self-hosted-kafka-private-service-connect-by-kafka-proxy)参照してください。

このドキュメントでは、Google Cloud の 3 つのアベイラビリティゾーン（AZ）にデプロイされた Kafka Private Service Connect サービスへの接続例を示します。同様のポートマッピング原則に基づいて他の構成も可能ですが、このドキュメントでは Kafka Private Service Connect サービスの基本的な設定プロセスについて説明します。本番環境では、運用の保守性と可観測性を強化した、より回復力の高い Kafka Private Service Connect サービスの使用を推奨します。

## 前提条件 {#prerequisites}

1.  独自の Google Cloud アカウントで Kafka Private Service Connect を設定するには、次の権限があることを確認してください。

    -   VMノードを管理する
    -   VPCを管理する
    -   サブネットを管理する
    -   ロードバランサーを管理する
    -   プライベートサービス接続の管理
    -   VMノードに接続してKafkaノードを構成する

2.  持っていない場合は[TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md) 。

3.  TiDB Cloud Dedicated クラスターから Kafka デプロイメント情報を取得します。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com)で[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
    2.  概要ページで、TiDB クラスターのリージョンを確認します。Kafka クラスターが同じリージョンにデプロイされることを確認してください。
    3.  左側のナビゲーション ペインで**[データ]** &gt; **[Changefeed] を**クリックし、右上隅の**[Changefeed の作成]**をクリックして、次の情報を入力します。
        1.  **宛先**で、 **Kafka**を選択します。
        2.  **[接続方法]**で、 **[プライベート サービス接続]**を選択します。
    4.  **先に進む前に、Google Cloud プロジェクトをリマインダー**に書き留めておいてください。このプロジェクトは、 TiDB Cloudからのエンドポイント作成リクエストの自動承認を承認するために使用します。
    5.  **TiDBクラスタのゾーン**をメモしておいてください。これらのゾーンに TiDB クラスターをデプロイします。ゾーン間のトラフィックを削減するため、これらのゾーンに Kafka をデプロイすることをお勧めします。
    6.  Kafka プライベート サービス接続サービスに固有の**Kafka アドバタイズ リスナー パターン**を選択します。
        1.  一意のランダム文字列を入力してください。数字または小文字のみ使用できます。この文字列は、後ほど**Kafkaアドバタイズリスナーパターンを**生成する際に使用します。
        2.  **「使用状況を確認して生成」を**クリックすると、ランダム文字列が一意であるかどうかが確認され、Kafka ブローカーの外部アドバタイズ リスナーを組み立てるために使用される**Kafka アドバタイズ リスナー パターンが**生成されるか、Kafka プロキシが構成されます。

すべてのデプロイメント情報をメモしてください。後でKafka Private Service Connectサービスを設定する際に必要になります。

次の表は、展開情報の例を示しています。

| 情報                              | 価値                                                                                                     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| リージョン                           | オレゴン州 ( `us-west1` )                                                                                   |
| TiDB Cloudの Google Cloud プロジェクト | `tidbcloud-prod-000`                                                                                   |
| ゾーン                             | <li> `us-west1-a` </li><li> `us-west1-b` </li><li> `us-west1-c` </li>                                  |
| Kafka アドバタイズド リスナー パターン         | 一意のランダム文字列: `abc`<br/>生成されたパターン: &lt;broker_id&gt;.abc.us-west1.gcp.3199745.tidbcloud.com:&lt;port&gt; |

## PSC ポート マッピングによるセルフホスト型 Kafka Private Service Connect サービスの設定 {#set-up-self-hosted-kafka-private-service-connect-service-by-psc-port-mapping}

PSCポートマッピングメカニズムを使用して、各KafkaブローカーをTiDB Cloud VPCに固有のポートで公開します。次の図は、その仕組みを示しています。

![Connect to Google Cloud self-hosted Kafka Private Service Connect by port mapping](/media/tidb-cloud/changefeed/connect-to-google-cloud-self-hosted-kafka-private-service-connect-by-portmapping.jpeg)

### ステップ1. Kafkaクラスターをセットアップする {#step-1-set-up-the-kafka-cluster}

新しいクラスターをデプロイする必要がある場合は、 [新しいKafkaクラスターをデプロイ](#deploy-a-new-kafka-cluster)の手順に従ってください。

既存のクラスターを公開する必要がある場合は、 [実行中の Kafka クラスターを再構成する](#reconfigure-a-running-kafka-cluster)の手順に従ってください。

#### 新しいKafkaクラスターをデプロイ {#deploy-a-new-kafka-cluster}

**1. Kafka VPC をセットアップする**

Kafka クラスターを簡単に構成できるように、Kafka VPC 用に 2 つのサブネット (1 つは Kafka ブローカー用、もう 1 つは要塞ノード用) を作成する必要があります。

[Google Cloud コンソール](https://cloud.google.com/cloud-console)に進み、 [VPCネットワーク](https://console.cloud.google.com/networking/networks/list)ページに移動して、次の属性を持つ Kafka VPC を作成します。

-   **名前**: `kafka-vpc`
-   サブネット
    -   **名前**: `bastion-subnet` ;**リージョン**: `us-west1` ; **IPv4範囲**: `10.0.0.0/18`
    -   **名前**: `brokers-subnet` ;**リージョン**: `us-west1` ; **IPv4範囲**: `10.64.0.0/18`
-   ファイアウォールルール
    -   `kafka-vpc-allow-custom`
    -   `kafka-vpc-allow-ssh`

**2. VMのプロビジョニング**

VM をプロビジョニングするには、 [VMインスタンス](https://console.cloud.google.com/compute/instances)ページに移動します。

1.  バスティオンノード

    -   **名前**: `bastion-node`
    -   **リージョン**: `us-west1`
    -   **ゾーン**: `Any`
    -   **マシンタイプ**： `e2-medium`
    -   **画像**： `Debian GNU/Linux 12`
    -   **ネットワーク**: `kafka-vpc`
    -   **サブネットワーク**: `bastion-subnet`
    -   **外部 IPv4 アドレス**: `Ephemeral`

2.  ブローカーノード1

    -   **名前**: `broker-node1`
    -   **リージョン**: `us-west1`
    -   **ゾーン**: `us-west1-a`
    -   **マシンタイプ**： `e2-medium`
    -   **画像**： `Debian GNU/Linux 12`
    -   **ネットワーク**: `kafka-vpc`
    -   **サブネットワーク**: `brokers-subnet`
    -   **外部 IPv4 アドレス**: `None`

3.  ブローカーノード2

    -   **名前**: `broker-node2`
    -   **リージョン**: `us-west1`
    -   **ゾーン**: `us-west1-b`
    -   **マシンタイプ**： `e2-medium`
    -   **画像**： `Debian GNU/Linux 12`
    -   **ネットワーク**: `kafka-vpc`
    -   **サブネットワーク**: `brokers-subnet`
    -   **外部 IPv4 アドレス**: `None`

4.  ブローカーノード3

    -   **名前**: `broker-node3`
    -   **リージョン**: `us-west1`
    -   **ゾーン**: `us-west1-c`
    -   **マシンタイプ**： `e2-medium`
    -   **画像**： `Debian GNU/Linux 12`
    -   **ネットワーク**: `kafka-vpc`
    -   **サブネットワーク**: `brokers-subnet`
    -   **外部 IPv4 アドレス**: `None`

**3. Kafkaランタイムバイナリを準備する**

1.  要塞ノードの詳細ページに移動します。SSH**を**クリックして要塞ノードにログインします。バイナリをダウンロードします。

    ```shell
    # Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

2.  バイナリを各ブローカー ノードにコピーします。

    ```shell
    # Run this command to authorize gcloud to access the Cloud Platform with Google user credentials
    # Follow the instruction in output to finish the login
    gcloud auth login

    # Copy binaries to broker nodes
    gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node1:~ --zone=us-west1-a
    gcloud compute ssh broker-node1 --zone=us-west1-a --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node2:~ --zone=us-west1-b
    gcloud compute ssh broker-node2 --zone=us-west1-b --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node3:~ --zone=us-west1-c
    gcloud compute ssh broker-node3 --zone=us-west1-c --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    ```

**4. Kafkaブローカーを構成する**

1.  3つのノードでKRaft Kafkaクラスターをセットアップします。各ノードはブローカーとコントローラーの役割を持ちます。各ブローカーに対して、以下の手順を実行します。

    1.  `listeners`の場合、3 つのブローカーはすべて同じであり、ブローカーとコントローラーのロールとして機能します。
        1.  すべての**コントローラー**ロールノードに同じ CONTROLLER リスナーを設定します。**ブローカー**ロールノードのみを追加する場合は、 `server.properties`の CONTROLLER リスナーは必要ありません。
        2.  2 つの**ブローカー**リスナーを構成します。内部アクセスの場合は INTERNAL、 TiDB Cloudからの外部アクセスの場合は EXTERNAL です。
    2.  `advertised.listeners`については、次の操作を行います。
        1.  ブローカー ノードの内部 IP アドレスを使用して、各ブローカーの内部アドバタイズ リスナーを構成します。これにより、内部 Kafka クライアントはアドバタイズ アドレスを介してブローカーに接続できるようになります。
        2.  TiDB Cloudから取得した**Kafkaアドバタイズリスナーパターン**に基づいて、各ブローカーノードにEXTERNALアドバタイズリスナーを設定することで、TiDB TiDB Cloudが複数のブローカーを区別できるようになります。異なるEXTERNALアドバタイズリスナーを設定することで、 TiDB Cloud側のKafkaクライアントはリクエストを適切なブローカーにルーティングできるようになります。
            -   `<port>`ブローカーと Kafka Private Service Connect アクセスポイントを区別します。すべてのブローカーの EXTERNAL アドバタイズリスナーのポート範囲を計画してください。これらのポートは、ブローカーが実際にリッスンするポートである必要はありません。これらは、リクエストを別のブローカーに転送する Private Service Connect のロードバランサーがリッスンするポートです。
            -   トラブルシューティングを容易にするために、ブローカーごとに異なるブローカー ID を構成することをお勧めします。
    3.  計画値:
        -   コントローラーポート: `29092`
        -   内部ポート: `9092`
        -   外部: `39092`
        -   外部アドバタイズされたリスナーポートの範囲: `9093~9095`

2.  SSHを使用して各ブローカーノードにログインします。各ブローカーノードごとに、以下の内容を含む設定ファイル`~/config/server.properties`作成します。

    ```properties
    # broker-node1 ~/config/server.properties
    # 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
    # 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
    # 2.1 The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>".
    # 2.2 So the EXTERNAL can be "b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9093) in the port range of the EXTERNAL advertised listener.
    process.roles=broker,controller
    node.id=1
    controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node2 ~/config/server.properties
    # 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
    # 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
    # 2.1 The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>".
    # 2.2 So the EXTERNAL can be "b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9094) in the port range of the EXTERNAL advertised listener.
    process.roles=broker,controller
    node.id=2
    controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node3 ~/config/server.properties
    # 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} with the actual IP addresses.
    # 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
    # 2.1 The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>".
    # 2.2 So the EXTERNAL can be "b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9095) in the port range of the EXTERNAL advertised listener.
    process.roles=broker,controller
    node.id=3
    controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

3.  スクリプトを作成し、それを実行して各ブローカー ノードで Kafka ブローカーを起動します。

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

    # Magic id: BRl69zcmTFmiPaoaANybiw. You can use your own magic ID.
    $KAFKA_STORAGE_CMD format -t "BRl69zcmTFmiPaoaANybiw" -c "$KAFKA_CONFIG_DIR/server.properties" > $KAFKA_LOG_DIR/server_format.log   
    LOG_DIR=$KAFKA_LOG_DIR nohup $KAFKA_START_CMD "$KAFKA_CONFIG_DIR/server.properties" &
    ```

**5. 要塞ノードでKafkaクラスターをテストする**

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
    # We will make them resolvable in TiDB Cloud side and make it route to the right broker when you create a changefeed connect to this Kafka cluster by Private Service Connect. 
    b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
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

4.  `produce.sh`と`consume.sh`実行して、Kafkaクラスターが実行中であることを確認してください。これらのスクリプトは、後ほどネットワーク接続テストにも再利用されます。スクリプトは`--partitions 3 --replication-factor 3`のトピックを作成します。3つのブローカーすべてにデータが含まれていることを確認してください。ネットワーク接続がテストされるよう、スクリプトが3つのブローカーすべてに接続されることを確認してください。

    ```shell
    # Test write message. 
    ./produce.sh {one_of_broker_ip}:9092
    ```

    ```text
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

    ```text
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

#### 実行中の Kafka クラスターを再構成する {#reconfigure-a-running-kafka-cluster}

Kafka クラスターが TiDB クラスターと同じリージョンにデプロイされていることを確認してください。ゾーン間のトラフィックを削減するため、ゾーンも同じリージョンに配置することをお勧めします。

**1. ブローカーの外部リスナーを構成する**

以下の設定はKafka KRaftクラスターに適用されます。ZKモードの設定も同様です。

1.  構成の変更を計画します。

    1.  TiDB Cloudからの外部アクセス用に、各ブローカーに EXTERNAL**リスナー**を設定します。EXTERNAL ポートとして一意のポート（例： `39092` ）を選択します。
    2.  TiDB Cloudから取得した**Kafkaアドバタイズリスナーパターン**に基づいて、各ブローカーノードにEXTERNAL**アドバタイズリスナー**を設定することで、TiDB TiDB Cloudが複数のブローカーを区別できるようになります。異なるEXTERNALアドバタイズリスナーを設定することで、 TiDB Cloud側のKafkaクライアントはリクエストを適切なブローカーにルーティングできるようになります。
        -   `<port>`ブローカーと Kafka Private Service Connect アクセスポイントを区別します。すべてのブローカーの EXTERNAL アドバタイズリスナーのポート範囲を計画します（例： `range from 9093` ）。これらのポートは、ブローカーが実際にリッスンするポートである必要はありません。これらは、リクエストを別のブローカーに転送する Private Service Connect のロードバランサーがリッスンするポートです。
        -   トラブルシューティングを容易にするために、ブローカーごとに異なるブローカー ID を構成することをお勧めします。

2.  SSHを使用して各ブローカーノードにログインします。各ブローカーの設定ファイルを以下の内容に変更します。

    ```properties
    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section
    # 1. The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>".
    # 2. So the EXTERNAL can be "bx.abc.us-west1.gcp.3199745.tidbcloud.com:xxxx". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port in the port range of the EXTERNAL advertised listener.
    # For example
    advertised.listeners=...,EXTERNAL://b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093

    # Configure EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

3.  すべてのブローカーを再構成したら、Kafka ブローカーを 1 つずつ再起動します。

**2. 内部ネットワークで外部リスナーの設定をテストする**

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
export JAVA_HOME=~/jdk-22.0.2

# Bootstrap from the EXTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# Expected output for the last 3 lines (the actual order might be different)
# There will be some exceptions or errors because advertised listeners cannot be resolved in your Kafka network. 
# We will make them resolvable in TiDB Cloud side and make it route to the right broker when you create a changefeed connect to this Kafka cluster by Private Service Connect. 
b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

### ステップ2. KafkaクラスターをPrivate Service Connectとして公開する {#step-2-expose-the-kafka-cluster-as-private-service-connect}

1.  [ネットワークエンドポイントグループ](https://console.cloud.google.com/compute/networkendpointgroups/list)ページ目に進みます。以下の手順でネットワークエンドポイントグループを作成します。

    -   **名前**: `kafka-neg`
    -   **ネットワークエンドポイントグループタイプ**: `Port Mapping NEG(Regional)`
        -   **リージョン**: `us-west1`
        -   **ネットワーク**: `kafka-vpc`
        -   **サブネット**: `brokers-subnet`

2.  ネットワーク エンドポイント グループの詳細ページに移動し、ネットワーク エンドポイントを追加して、ブローカー ノードへのポート マッピングを構成します。

    1.  ネットワークエンドポイント1
        -   **インスタンス**: `broker-node1`
        -   **VMポート**: `39092`
        -   **クライアントポート**: `9093`
    2.  ネットワークエンドポイント2
        -   **インスタンス**: `broker-node2`
        -   **VMポート**: `39092`
        -   **クライアントポート**: `9094`
    3.  ネットワークエンドポイント3
        -   **インスタンス**: `broker-node3`
        -   **VMポート**: `39092`
        -   **クライアントポート**: `9095`

3.  [負荷分散](https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers)ページ目に進みます。以下の手順でロードバランサーを作成します。

    -   **ロードバランサーの種類**: `Network Load Balancer`
    -   **プロキシまたはパススルー**: `Passthrough`
    -   **対外向けまたは社内向け**： `Internal`
    -   **ロードバランサー名**: `kafka-lb`
    -   **リージョン**: `us-west1`
    -   **ネットワーク**: `kafka-vpc`
    -   バックエンド構成
        -   **バックエンドタイプ**： `Port mapping network endpoint group`
        -   **プロトコル**： `TCP`
        -   **ポートマッピングネットワークエンドポイントグループ**: `kafka-neg`
    -   フロントエンド構成
        -   **サブネットワーク**: `brokers-subnet`
        -   **ポート**: `All`

4.  [**プライベートサービス接続**&gt;**公開サービス**](https://console.cloud.google.com/net-services/psc/list/producers)に進みます。

    -   **ロードバランサータイプ**: `Internal passthrough Network Load Balancer`
    -   **内部ロードバランサ**： `kafka-lb`
    -   **サービス名**： `kafka-psc`
    -   **サブネット**: `RESERVE NEW SUBNET`
        -   **名前**: `psc-subnet`
        -   **VPC ネットワーク**: `kafka-vpc`
        -   **リージョン**: `us-west1`
        -   **IPv4範囲**: `10.128.0.0/18`
    -   **承認されたプロジェクト**: [前提条件](#prerequisites)で取得したTiDB Cloudの Google Cloud プロジェクト (例: `tidbcloud-prod-000` )。

5.  `kafka-psc`の詳細ページに移動します。**サービスアタッチメント**（例： `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-psc` ）を書き留めます。TiDB TiDB Cloudでこの PSC に接続する際に使用します。

6.  VPC ネットワーク`kafka-vpc`の詳細ページに移動し、すべてのブローカーへの PSC トラフィックを許可するファイアウォール ルールを追加します。

    -   **名前**: `allow-psc-traffic`
    -   **交通方向**： `Ingress`
    -   **試合のアクション**： `Allow`
    -   **ターゲット**： `All instances in the network`
    -   **ソースフィルター**: `IPv4 ranges`
    -   **ソースIPv4範囲**: `10.128.0.0/18` -subnetの範囲。
    -   **プロトコルとポート**: すべて許可

### ステップ3. TiDB Cloudから接続する {#step-3-connect-from-tidb-cloud}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)に戻り、クラスターが**Private Service Connect**経由で Kafka クラスターに接続するための changefeed を作成します。詳細については、 [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)参照してください。

2.  **「ChangeFeed ターゲットの構成」&gt;「接続方法」&gt;「プライベート サービス接続」**に進むときは、次のフィールドに対応する値を入力し、必要に応じてその他のフィールドを入力します。

    -   **Kafka アドバタイズ リスナー パターン**: `abc` 。これは、 [前提条件](#prerequisites)で**Kafka アドバタイズ リスナー パターン**を生成するために使用する一意のランダム文字列と同じです。
    -   **サービス アタッチメント**: PSC の Kafka サービス アタッチメント (例: `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-psc` )。
    -   **ブートストラップポート**: `9092,9093,9094`

3.  [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)の手順に進みます。

## Kafka-proxy によるセルフホスト型 Kafka プライベート サービス接続のセットアップ {#set-up-self-hosted-kafka-private-service-connect-by-kafka-proxy}

Kafkaプロキシの動的ポートマッピングメカニズムを使用して、各KafkaブローカーをTiDB Cloud VPCに固有のポートで公開します。次の図は、その仕組みを示しています。

![Connect to Google Cloud self-hosted Kafka Private Service Connect by Kafka proxy](/media/tidb-cloud/changefeed/connect-to-google-cloud-self-hosted-kafka-private-service-connect-by-kafka-proxy.jpeg)

### ステップ1. Kafka-proxyを設定する {#step-1-set-up-kafka-proxy}

TiDB クラスターと同じリージョンで既に Kafka クラスターが稼働していると仮定します。VPC ネットワークから Kafka クラスターに接続できます。Kafka クラスターは、セルフホスト型でも、Confluent などのサードパーティプロバイダーが提供するものでも構いません。

1.  [インスタンスグループ](https://console.cloud.google.com/compute/instanceGroups/list)ページに移動し、Kafka-proxy のインスタンス グループを作成します。

    -   **名前**: `kafka-proxy-ig`
    -   インスタンステンプレート:
        -   **名前**: `kafka-proxy-tpl`
        -   **場所**： `Regional`
        -   **リージョン**: `us-west1`
        -   **マシンタイプ**: `e2-medium`ワークロードに応じて独自のマシンタイプを選択できます。
        -   **ネットワーク**: Kafka クラスターに接続できる VPC ネットワーク。
        -   **サブネットワーク**: Kafka クラスターに接続できるサブネット。
        -   **外部IPv4アドレス**： `Ephemeral` -proxyの設定を容易にするため、インターネットアクセスを有効にしてください。本番環境では**「なし」**を選択し、任意の方法でノードにログインできます。
    -   **場所**： `Single zone`
    -   **リージョン**: `us-west1`
    -   **ゾーン**: ブローカーのゾーンの 1 つを選択します。
    -   **自動スケーリングモード**: `Off`
    -   **インスタンスの最小数**: `1`
    -   **インスタンスの最大数**: `1` 。Kafkaプロキシはクラスターモードをサポートしていないため、デプロイできるインスタンスは1つだけです。各Kafkaプロキシはローカルポートをブローカーのポートにランダムにマッピングするため、プロキシごとにマッピングが異なります。ロードバランサーの背後に複数のKafkaプロキシをデプロイすると、問題が発生する可能性があります。Kafkaクライアントが1つのプロキシに接続し、別のプロキシを経由してブローカーにアクセスすると、リクエストが誤ったブローカーにルーティングされる可能性があります。

2.  kafka-proxy-ig のノードの詳細ページに移動します。SSH**を**クリックしてノードにログインします。バイナリをダウンロードします。

    ```shell
    # You can choose another version 
    wget https://github.com/grepplabs/kafka-proxy/releases/download/v0.3.11/kafka-proxy-v0.3.11-linux-amd64.tar.gz
    tar -zxf kafka-proxy-v0.3.11-linux-amd64.tar.gz
    ```

3.  Kafka-proxy を実行し、Kafka ブローカーに接続します。

    ```shell
    # There are three kinds of parameters that need to feed to the Kafka-proxy
    # 1. --bootstrap-server-mapping defines the bootstrap mapping. Suggest that you configure three mappings, one for each zone for resilience.
    #   a) Kafka broker address; 
    #   b) Local address for the broker in Kafka-proxy; 
    #   c) Advertised listener for the broker if Kafka clients bootstrap from Kafka-proxy
    # 2. --dynamic-sequential-min-port defines the start port of the random mapping for other brokers
    # 3. --dynamic-advertised-listener defines advertised listener address for other brokers based on the pattern obtained from the "Prerequisites" section
    #   a) The pattern: <broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>
    #   b) Make sure to replace <broker_id> with a fixed lowercase string, for example, "brokers". You can use your own string. This step will help TiDB Cloud route requests properly.
    #   c) Remove ":<port>"
    #   d) The advertised listener address would be: brokers.abc.us-west1.gcp.3199745.tidbcloud.com
    ./kafka-proxy server \
            --bootstrap-server-mapping "{address_of_broker1},0.0.0.0:9092,b1.abc.us-west1.gcp.3199745.tidbcloud.com:9092" \
            --bootstrap-server-mapping "{address_of_broker2},0.0.0.0:9093,b2.abc.us-west1.gcp.3199745.tidbcloud.com:9093" \
            --bootstrap-server-mapping "{address_of_broker3},0.0.0.0:9094,b3.abc.us-west1.gcp.3199745.tidbcloud.com:9094" \
            --dynamic-sequential-min-port=9095 \
            --dynamic-advertised-listener=brokers.abc.us-west1.gcp.3199745.tidbcloud.com > ./kafka_proxy.log 2>&1 &
    ```

4.  Kafka-proxy ノードでブートストラップをテストします。

    ```shell
    # Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz

    export JAVA_HOME=~/jdk-22.0.2

    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server 0.0.0.0:9092
    # Expected output of the last few lines (the actual order might be different)
    # There might be exceptions or errors because advertised listeners cannot be resolved in your network.
    # We will make them resolvable in TiDB Cloud side and make it route to the right broker when you create a changefeed connect to this Kafka cluster by Private Service Connect. 
    b1.abc.us-west1.gcp.3199745.tidbcloud.com:9092 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    brokers.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 4 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    brokers.abc.us-west1.gcp.3199745.tidbcloud.com:9096 (id: 5 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ...
    ```

### ステップ2. Kafka-proxyをプライベートサービス接続サービスとして公開する {#step-2-expose-kafka-proxy-as-private-service-connect-service}

1.  [負荷分散](https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers)ページに移動して、ロードバランサーを作成します。

    -   **ロードバランサーの種類**: `Network Load Balancer`
    -   **プロキシまたはパススルー**: `Passthrough`
    -   **対外向けまたは社内向け**： `Internal`
    -   **ロードバランサー名**: `kafka-proxy-lb`
    -   **リージョン**: `us-west1`
    -   **ネットワーク**: あなたのネットワーク
    -   バックエンド構成
        -   **バックエンドタイプ**： `Instance group`
        -   **プロトコル**： `TCP`
        -   **インスタンスグループ**: `kafka-proxy-ig`
    -   フロントエンド構成
        -   **サブネットワーク**: サブネット
        -   **ポート**: `All`
        -   健康チェック:
            -   **名前**: `kafka-proxy-hc`
            -   **範囲**： `Regional`
            -   **プロトコル**： `TCP`
            -   **ポート**: `9092` -proxy でブートストラップ ポートの 1 つを選択できます。

2.  [**プライベートサービス接続**&gt;**公開サービス**](https://console.cloud.google.com/net-services/psc/list/producers)に進みます。

    -   **ロードバランサータイプ**: `Internal passthrough Network Load Balancer`
    -   **内部ロードバランサ**： `kafka-proxy-lb`
    -   **サービス名**： `kafka-proxy-psc`
    -   **サブネット**: `RESERVE NEW SUBNET`
        -   **名前**: `proxy-psc-subnet`
        -   **VPCネットワーク**: あなたのネットワーク
        -   **リージョン**: `us-west1`
        -   **IPv4 範囲**: ネットワーク計画に基づいて CIDR を設定します
    -   **承認されたプロジェクト**: [前提条件](#prerequisites)で取得したTiDB Cloudの Google Cloud プロジェクト (例: `tidbcloud-prod-000` )。

3.  **kafka-proxy-psc**の詳細ページに移動します。3 （例： `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-proxy-psc` ） `Service attachment`メモします。これは、 TiDB Cloudがこの PSC に接続する際に使用されます。

4.  VPC ネットワークの詳細ページに移動し、すべてのブローカーの PSC トラフィックを許可するファイアウォール ルールを追加します。

    -   **名前**: `allow-proxy-psc-traffic`
    -   **交通方向**： `Ingress`
    -   **試合のアクション**： `Allow`
    -   **対象**: ネットワーク内のすべてのインスタンス
    -   **ソースフィルター**: `IPv4 ranges`
    -   **ソース IPv4 範囲**: proxy-psc-subnet の CIDR
    -   **プロトコルとポート**: すべて許可

### ステップ3. TiDB Cloudから接続する {#step-3-connect-from-tidb-cloud}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)に戻り、クラスターが**Private Service Connect**経由で Kafka クラスターに接続するための changefeed を作成します。詳細については、 [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)参照してください。

2.  **「ChangeFeed ターゲットの構成」** &gt; **「接続方法」** &gt; **「プライベート サービス接続」**に進んだ後、次のフィールドに対応する値を入力し、必要に応じてその他のフィールドを入力します。

    -   **Kafka アドバタイズ リスナー パターン**: `abc` . [前提条件](#prerequisites)で**Kafka アドバタイズ リスナー パターン**を生成するために使用する一意のランダム文字列と同じです。
    -   **サービス アタッチメント**: PSC の kafka-proxy サービス アタッチメント (例: `projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-proxy-psc` )。
    -   **ブートストラップポート**: `9092,9093,9094`

3.  引き続き[Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)ガイドラインに従ってください。

## FAQ {#faq}

### 2 つの異なるTiDB Cloudプロジェクトから同じ Kafka Private Service Connect サービスに接続するにはどうすればよいですか? {#how-to-connect-to-the-same-kafka-private-service-connect-service-from-two-different-tidb-cloud-projects}

すでにこのドキュメントの手順に従って最初のプロジェクトからの接続を正常に設定していて、2 番目のプロジェクトから 2 番目の接続を設定する場合は、次のようにして 2 つの異なるTiDB Cloudプロジェクトから同じ Kafka Private Service Connect サービスに接続できます。

-   PSC ポート マッピングによって Kafka PSC を設定する場合は、次の手順を実行します。

    1.  このドキュメントの冒頭の指示に従ってください[ステップ1. Kafkaクラスタのセットアップ](#step-1-set-up-the-kafka-cluster)に進んだら、 [実行中の Kafka クラスターを再構成する](#reconfigure-a-running-kafka-cluster)セクションに従って、EXTERNAL リスナーとアドバタイズリスナーの別のグループを作成してください。このグループの名前は`EXTERNAL2`とします。ポート範囲`EXTERNAL2`は EXTERNAL と重複できないことに注意してください。

    2.  ブローカーを再構成した後、ネットワーク エンドポイントの別のグループをネットワーク エンドポイント グループに追加し、ポート範囲を`EXTERNAL2`リスナーにマップします。

    3.  新しい変更フィードを作成するには、次の入力でTiDB Cloud接続を構成します。

        -   新しいブートストラップポート
        -   新しい Kafka アドバタイズ リスナー パターン
        -   同じサービスアタッチメント

-   [Kafka-proxy によるセルフホスト型 Kafka プライベート サービス コネクトのセットアップ](#set-up-self-hosted-kafka-private-service-connect-by-kafka-proxy)場合は、新しい Kafka アドバタイズ リスナー パターンを使用して、最初から新しい Kafka プロキシ PSC を作成します。
