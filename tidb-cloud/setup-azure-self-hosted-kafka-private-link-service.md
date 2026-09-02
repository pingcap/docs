---
title: Set Up Self-Hosted Kafka Private Link Service in Azure
summary: このドキュメントでは、Azure でセルフホスト型 Kafka 用の Private Link サービスを設定し、それをTiDB Cloudで動作させる方法について説明します。
---

# Azure でセルフホスト型 Kafka プライベートリンクサービスをセットアップする {#set-up-self-hosted-kafka-private-link-service-in-azure}

このドキュメントでは、Azure でセルフホスト型 Kafka 用の Private Link サービスを設定し、それをTiDB Cloudで動作させる方法について説明します。

このメカニズムは次のように機能します。

1. TiDB Cloud仮想ネットワークは、プライベートエンドポイントを介して Kafka 仮想ネットワークに接続します。
2. Kafka クライアントはすべての Kafka ブローカーと直接通信する必要があります。
3. 各 Kafka ブローカーは、 TiDB Cloud仮想ネットワーク内のエンドポイントの一意のポートにマップされます。
4. マッピングを実現するには、Kafka ブートストラップ メカニズムと Azure リソースを活用します。

次の図にその仕組みを示します。

![Connect to Azure Self-Hosted Kafka Private Link Service](/media/tidb-cloud/changefeed/connect-to-azure-self-hosted-kafka-privatelink-service.png)

このドキュメントでは、Azure で Kafka Private Link サービスに接続する例を示します。同様のポートマッピング原則に基づいて他の構成も可能ですが、このドキュメントでは Kafka Private Link サービスの基本的なセットアップ手順について説明します。本番環境では、運用の保守性と可観測性を強化した、より回復力の高い Kafka Private Link サービスの使用をお勧めします。

## 前提条件 {#prerequisites}

1. 独自の Azure アカウントで Kafka Private Link サービスを設定するには、次の承認があることを確認してください。

    - 仮想マシンを管理する
    - 仮想ネットワークを管理する
    - ロードバランサーを管理する
    - プライベートリンクサービスを管理する
    - 仮想マシンに接続して Kafka ノードを構成する

2. Azure をお持ちでない場合は[TiDB Cloud Dedicatedクラスタを作成する](/tidb-cloud/create-tidb-cluster.md) 。

3. [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから Kafka デプロイメント情報を取得します。

    1. [TiDB Cloudコンソール](https://tidbcloud.com)で[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットクラスターの名前をクリックして概要ページに移動します。
    2. 左側のナビゲーションペインで、 **Data** &gt; **Changefeed**をクリックします。
    3. **Changefeed**ページで、右上隅の**Create Changefeed**をクリックし、次の情報を入力します。
        1. **Destination**で、 **Kafka**を選択します。
        2. **Connectivity Method**で**Private Link**を選択します。
    4. 続行する前に、 TiDB Cloud Azureアカウントのリージョン情報とサブスクリプションを**リマインダー**に書き留めておいてください。この情報は、TiDB CloudがKafka Private Linkサービスにアクセスできるように承認する際に使用します。
    5. 一意のランダム文字列を指定して、Kafka プライベートリンクサービス用の**Kafka Advertised Listener Pattern**を生成します。
        1. 一意のランダム文字列を入力してください。数字または小文字のみ使用できます。この文字列は、後ほど**Kafka Advertised Listener Pattern**を生成する際に使用します。
        2. **Check usage and generate**をクリックすると、ランダム文字列が一意であるかどうかが確認され、Kafka ブローカーの外部アドバタイズリスナーを組み立てるために使用される**Kafka Advertised Listener Pattern**が生成されます。

すべてのデプロイメント情報をメモしてください。後でKafka Private Linkサービスを設定する際に必要になります。

次の表は、デプロイメント情報の例を示しています。

| 情報                              | 値                                     | 注記                                                                       |
| ------------------------------- | -------------------------------------- | ------------------------------------------------------------------------ |
| リージョン                           | バージニア ( `eastus` )                     | 該当なし                                                                     |
| TiDB Cloud Azureアカウントのサブスクリプション | `99549169-6cee-4263-8491-924a3011ee31` | 該当なし                                                                     |
| Kafka アドバタイズド リスナー パターン         | 一意のランダム文字列: `abc`                      | 生成されたパターン: `<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>` ; |

## ステップ1. Kafkaクラスターをセットアップする {#step-1-set-up-a-kafka-cluster}

新しいクラスターをデプロイする必要がある場合は、 [新しいKafkaクラスターをデプロイ](#deploy-a-new-kafka-cluster)の手順に従ってください。

既存のクラスターを公開する必要がある場合は、 [実行中の Kafka クラスターを再構成する](#reconfigure-a-running-kafka-cluster)の手順に従ってください。

### 新しいKafkaクラスターをデプロイ {#deploy-a-new-kafka-cluster}

#### 1. Kafka仮想ネットワークを設定する {#1-set-up-the-kafka-virtual-network}

1. [Azureポータル](https://portal.azure.com/)にログインし、 [仮想ネットワーク](https://portal.azure.com/#browse/Microsoft.Network%2FvirtualNetworks)ページに移動して、 **+ Create**をクリックして仮想ネットワークを作成します。

2. **Basic**タブで、 **Subscription** 、 **Resource group** 、および**Region**を選択し、 **[仮想ネットワーク名]**フィールドに名前 (たとえば、 `kafka-pls-vnet` ) を入力して、 **Next**をクリックします。

3. **Security**タブで、Azure Bastion を有効にし、 **Next**をクリックします。

4. **IP addresses**タブで、次の操作を行います。

    1. 仮想ネットワークのアドレス空間を設定します (例: `10.0.0.0/16` )。
    2. ブローカーのサブネットを作成するには、 **[サブネットの追加]**をクリックし、次の情報を入力して、 **[追加]**をクリックします。

        - **Name**: `brokers-subnet`
        - **IPアドレス範囲**: `10.0.0.0/24`
        - **Size**: `/24 (256 addresses)`

        デフォルトでは`AzureBastionSubnet`が作成されます。

5. 情報を確認するには、 **Review + create**をクリックします。

6. **Create**をクリックします。

#### 2. Kafkaブローカーを設定する {#2-set-up-kafka-brokers}

**2.1. ブローカーノードを作成する**

1. [Azureポータル](https://portal.azure.com/)にログインし、 [仮想マシン](https://portal.azure.com/#view/Microsoft_Azure_ComputeHub/ComputeHubMenuBlade/~/virtualMachinesBrowse)ページに移動して**+ Create**をクリックし、 **[Azure 仮想マシン]**を選択します。
2. **Basic**タブで、**Subscription**、**Resource group**、**Region**を選択し、次の情報を入力して、 **[次へ: ディスク]**をクリックします。
    - **仮想マシン名**: `broker-node`
    - **Availability options**: `Availability zone`
    - **Zone options**: `Self-selected zone`
    - `Zone 3` `Zone 2`**Availability zone**: `Zone 1`
    - **Image**： `Ubuntu Server 24.04 LTS - x64 Gen2`
    - **VM architecture:** `x64`
    - **Size**: `Standard_D2s_v3`
    - **Authentication type**: `SSH public key`
    - **Username**: `azureuser`
    - **SSH public key source:** `Generate new key pair`
    - **Key pair name**: `kafka_broker_key`
    - **Public inbound ports**: `Allow selected ports`
    - **Select inbound ports**: `SSH (22)`
3. **Next : Networking**をクリックし、 **Networking**タブに次の情報を入力します。
    - **Virtual network**： `kafka-pls-vnet`
    - **サブネット**: `brokers-subnet`
    - **Public IP** : `None`
    - **NIC network security group**: `Basic`
    - **Public inbound ports**: `Allow selected ports`
    - 受信ポートを選択: `SSH (22)`
    - **Load balancing options**: `None`
4. 情報を確認するには、 **Review + create**をクリックします。
5. **Create**をクリックします。**Generate new key pair**メッセージが表示されます。
6. **Download private key and create resource**をクリックして、秘密鍵をローカルマシンにダウンロードします。仮想マシンの作成の進行状況を確認できます。

**2.2. Kafka ランタイムバイナリの準備**

仮想マシンのデプロイが完了したら、次の手順を実行します。

1. [Azureポータル](https://portal.azure.com/)で[**Resource groups**](https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView)ページに移動し、リソースグループ名をクリックして、各ブローカーノード ( `broker-node-1` 、 `broker-node-2` 、および`broker-node-3` ) のページに移動します。

2. ブローカーノードの各ページで、左側のナビゲーションペインの**Connect > Bastion**をクリックし、次の情報を入力します。

    - **Authentication Type**: `SSH Private Key from Local File`
    - **Username**: `azureuser`
    - **Local File**: 以前にダウンロードした秘密鍵ファイルを選択します
    - **Open in new browser tab**オプションを選択します

3. ブローカーノードの各ページで**Connect**をクリックすると、Linuxターミナルで新しいブラウザタブが開きます。3つのブローカーノードごとに、Linuxターミナルで3つのブラウザタブを開く必要があります。

4. 各 Linux ターミナルで次のコマンドを実行して、各ブローカーノードにバイナリをダウンロードします。

    ```shell
    # Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

**2.3. 各ブローカーノードにKafkaノードを設定する**

1. 3つのノードでKRaft Kafkaクラスターをセットアップします。各ノードはブローカーとコントローラーの両方の役割を果たします。各ブローカーノードに対して、以下の手順を実行します。

    1. `listeners`を構成します。3つのブローカーはすべて同じであり、ブローカーとコントローラーのロールとして機能します。
        1. すべての**コントローラー**ロールノードに同じ CONTROLLER リスナーを設定します。ブローカーロールノードのみを追加する場合は、 `server.properties`の CONTROLLER リスナーを省略できます。
        2. 2 つのブローカー リスナーを構成します。内部 Kafka クライアント アクセス用の**INTERNAL**と、 TiDB Cloudからのアクセス用の**EXTERNAL です**。

    2. `advertised.listeners`については、次の操作を行います。
        1. ブローカーノードの内部 IP アドレスを使用して、各ブローカーの内部アドバタイズリスナーを構成します。これにより、内部 Kafka クライアントはアドバタイズ アドレスを介してブローカーに接続できるようになります。
        2. TiDB Cloudから取得した**Kafka Advertised Listener Pattern**に基づいて、各ブローカーノードにEXTERNALアドバタイズリスナーを設定することで、TiDB Cloudが異なるブローカーを区別できるようになります。異なるEXTERNALアドバタイズリスナーを設定することで、 TiDB Cloud側のKafkaクライアントはリクエストを適切なブローカーにルーティングできるようになります。
            - Kafka Private Link サービスへのアクセスにおいて、ブローカーを区別するために異なる`<port>`値を使用してください。すべてのブローカーの EXTERNAL アドバタイズリスナーのポート範囲を計画してください。これらのポートは、ブローカーが実際にリッスンするポートである必要はありません。これらのポートは、Private Link サービス内のロードバランサーがリッスンするポートであり、ロードバランサーはリクエストを異なるブローカーに転送します。
            - トラブルシューティングを容易にするために、ブローカーごとに異なるブローカー ID を構成することをお勧めします。

    3. 計画値:
        - コントローラーポート: `29092`
        - 内部ポート: `9092`
        - 外部ポート: `39092`
        - EXTERNALアドバタイズリスナーポートの範囲: `9093~9095`

2. SSHを使用して各ブローカーノードにログインします。各ブローカーノードごとに、以下の内容を含む設定ファイル`~/config/server.properties`を作成します。

    ```properties
    # broker-node-1 ~/config/server.properties
    # 1. Replace {broker-node-1-ip}, {broker-node-2-ip}, {broker-node-3-ip} with the actual IP addresses.
    # 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
    # 2.1 The pattern is "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>".
    # 2.2 So the EXTERNAL can be "b1.abc.eastus.azure.3199745.tidbcloud.com:9093". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9093) in the port range of the EXTERNAL advertised listener.
    process.roles=broker,controller
    node.id=1
    controller.quorum.voters=1@{broker-node-1-ip}:29092,2@{broker-node-2-ip}:29092,3@{broker-node-3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node-1-ip}:9092,EXTERNAL://b1.abc.eastus.azure.3199745.tidbcloud.com:9093
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node-2 ~/config/server.properties
    # 1. Replace {broker-node-1-ip}, {broker-node-2-ip}, {broker-node-3-ip} with the actual IP addresses.
    # 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
    # 2.1 The pattern is "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>".
    # 2.2 So the EXTERNAL can be "b2.abc.eastus.azure.3199745.tidbcloud.com:9094". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9094) in the port range of the EXTERNAL advertised listener.
    process.roles=broker,controller
    node.id=2
    controller.quorum.voters=1@{broker-node-1-ip}:29092,2@{broker-node-2-ip}:29092,3@{broker-node-3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node-2-ip}:9092,EXTERNAL://b2.abc.eastus.azure.3199745.tidbcloud.com:9094
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

    ```properties
    # broker-node-3 ~/config/server.properties
    # 1. Replace {broker-node-1-ip}, {broker-node-2-ip}, {broker-node-3-ip} with the actual IP addresses.
    # 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section.
    # 2.1 The pattern is "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>".
    # 2.2 So the EXTERNAL can be "b3.abc.eastus.azure.3199745.tidbcloud.com:9095". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port (9095) in the port range of the EXTERNAL advertised listener.
    process.roles=broker,controller
    node.id=3
    controller.quorum.voters=1@{broker-node-1-ip}:29092,2@{broker-node-2-ip}:29092,3@{broker-node-3-ip}:29092
    listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
    inter.broker.listener.name=INTERNAL
    advertised.listeners=INTERNAL://{broker-node-3-ip}:9092,EXTERNAL://b3.abc.eastus.azure.3199745.tidbcloud.com:9095
    controller.listener.names=CONTROLLER
    listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
    log.dirs=./data
    ```

3. スクリプトを作成し、それを実行して各ブローカーノードで Kafka ブローカーを起動します。

    ```shell
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    KAFKA_STORAGE_CMD=$KAFKA_DIR/kafka-storage.sh
    KAFKA_START_CMD=$KAFKA_DIR/kafka-server-start.sh
    KAFKA_DATA_DIR=$SCRIPT_DIR/data
    KAFKA_LOG_DIR=$SCRIPT_DIR/log
    KAFKA_CONFIG_DIR=$SCRIPT_DIR/config

    KAFKA_PIDS=$(ps aux | grep 'kafka.Kafka' | grep -v grep | awk '{print $2}')
    if [ -z "$KAFKA_PIDS" ]; then
    echo "No Kafka processes are running."
    else
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

    $KAFKA_STORAGE_CMD format -t "BRl69zcmTFmiPaoaANybiw" -c "$KAFKA_CONFIG_DIR/server.properties" > $KAFKA_LOG_DIR/server_format.log
    LOG_DIR=$KAFKA_LOG_DIR nohup $KAFKA_START_CMD "$KAFKA_CONFIG_DIR/server.properties" &
    ```

**2.4. クラスター設定をテストする**

1. Kafka ブートストラップをテストします。

    ```shell
    export JAVA_HOME=/home/azureuser/jdk-22.0.2

    # Bootstrap from INTERNAL listener
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
    # Expected output (the actual order might be different)
    {broker-node-1-ip}:9092 (id: 1 rack: null) -> (
    {broker-node-2-ip}:9092 (id: 2 rack: null) -> (
    {broker-node-3-ip}:9092 (id: 3 rack: null) -> (

    # Bootstrap from EXTERNAL listener
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
    # Expected output for the last 3 lines (the actual order might be different)
    # The difference in the output from "bootstrap from INTERNAL listener" is that exceptions or errors might occur because advertised listeners cannot be resolved in kafka-pls-vnet.
    # TiDB Cloud will make these addresses resolvable and route requests to the correct broker when you create a changefeed connected to this Kafka cluster via Private Link Service.
    b1.abc.eastus.azure.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.abc.eastus.azure.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.abc.eastus.azure.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

2. 要塞ノードにプロデューサー スクリプト`produce.sh`を作成します。

    ```shell
    BROKER_LIST=$1

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"

    create_topic() {
        echo "Creating topic if it does not exist..."
        $KAFKA_DIR/kafka-topics.sh --create --topic $TOPIC --bootstrap-server $BROKER_LIST --if-not-exists --partitions 3 --replication-factor 3
    }

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

3. 要塞ノードにコンシューマー スクリプト`consume.sh`を作成します。

    ```shell
    BROKER_LIST=$1
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"
    CONSUMER_GROUP="test-group"
    consume_messages() {
        echo "Consuming messages from the topic..."
        $KAFKA_DIR/kafka-console-consumer.sh --bootstrap-server $BROKER_LIST --topic $TOPIC --from-beginning --timeout-ms 5000 --consumer-property group.id=$CONSUMER_GROUP
    }
    consume_messages
    ```

4. `produce.sh`と`consume.sh`スクリプトを実行します。これらのスクリプトは、接続とメッセージフローを自動的にテストし、Kafkaクラスターが正しく機能していることを確認します。`produce.sh`スクリプトは、 `--partitions 3 --replication-factor 3`でトピックを作成し、テストメッセージを送信し、 `--broker-list`パラメータを使用して3つのブローカーすべてに接続します。`consume.sh`スクリプトは、トピックからメッセージを読み取り、メッセージの配信が成功したことを確認します。

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

Kafka クラスターが TiDB クラスターと同じリージョンにデプロイされていることを確認します。

**1. ブローカーの外部リスナーを構成する**

以下の設定はKafka KRaftクラスターに適用されます。ZKモードの設定も同様です。

1. 構成の変更を計画します。

    1. TiDB Cloudからの外部アクセス用に、各ブローカーに EXTERNAL**リスナー**を設定します。EXTERNAL ポートとして一意のポート（例： `39092` ）を選択します。
    2. TiDB Cloudから取得した**advertised listener**に基づいて、各ブローカーノードにEXTERNAL**アドバタイズリスナー**を設定することで、TiDB Cloudが複数のブローカーを区別できるようになります。異なるEXTERNALアドバタイズリスナーを設定することで、 TiDB Cloud側のKafkaクライアントはリクエストを適切なブローカーにルーティングできるようになります。
        - `<port>` 、ブローカーと Kafka Private Link サービスのアクセスポイントを区別します。すべてのブローカーの EXTERNAL アドバタイズリスナーのポート範囲（例： `range from 9093` ）を計画してください。これらのポートは、ブローカーが実際にリッスンするポートである必要はありません。これらは、リクエストを別のブローカーに転送する Private Link サービスのロードバランサーがリッスンするポートです。
        - トラブルシューティングを容易にするために、ブローカーごとに異なるブローカー ID を構成することをお勧めします。

2. SSHを使用して各ブローカーノードにログインします。各ブローカーの設定ファイルを以下の内容に変更します。

    ```properties
    # Add EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in the "Prerequisites" section
    # 1. The pattern is "<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>".
    # 2. So the EXTERNAL can be "bx.abc.eastus.azure.3199745.tidbcloud.com:xxxx". Replace <broker_id> with "b" prefix plus "node.id" properties, and replace <port> with a unique port in the port range of the EXTERNAL advertised listener.
    # For example
    advertised.listeners=...,EXTERNAL://b1.abc.eastus.azure.3199745.tidbcloud.com:9093

    # Configure the EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

3. すべてのブローカーを再構成したら、Kafka ブローカーを 1つずつ再起動します。

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
# TiDB Cloud will make these addresses resolvable and route requests to the correct broker when you create a changefeed connected to this Kafka cluster via Private Link Service.
b1.abc.eastus.azure.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.abc.eastus.azure.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.abc.eastus.azure.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## ステップ2. Kafka クラスターをプライベートリンクサービスとして公開する {#step-2-expose-the-kafka-cluster-as-private-link-service}

### 1. ロードバランサーを設定する {#1-set-up-the-load-balancer}

1. [Azureポータル](https://portal.azure.com/)にログインし、 [負荷分散](https://portal.azure.com/#view/Microsoft_Azure_Network/LoadBalancingHubMenuBlade/~/loadBalancers)ページに移動して、 **+ Create**をクリックしてロードバランサーを作成します。

2. **Basic**タブで、**Subscription**、**Resource group**、**Region**を選択し、次のインスタンス情報を入力して、 **[次へ: フロントエンド IP 構成 &gt;]**をクリックします。

    - **Name**: `kafka-lb`
    - **SKU** : `Standard`
    - **Type**: `Internal`
    - **Tier**: `Regional`

3. **Frontend IP configuration**タブで、 **[+ フロントエンド IP 構成の追加]**をクリックし、次の情報を入力して**Save**をクリックし、 **[次へ: バックエンド プール &gt;]**をクリックします。

    - **Name**: `kafka-lb-ip`
    - **IP version**: `IPv4`
    - **Virtual network**： `kafka-pls-vnet`
    - **Subnet**: `brokers-subnet`
    - **Assignment**： `Dynamic`
    - **Availability zone**: `Zone-redundant`

4. **Backend pools**タブで、次の3つのバックエンド プールを追加し、 **Next : Inbound rules**をクリックします。

    - 名前: `pool1` ; バックエンド プールコンフィグレーション: `NIC` ; IP 構成: `broker-node-1`
    - 名前: `pool2` ; バックエンド プールコンフィグレーション: `NIC` ; IP 構成: `broker-node-2`
    - 名前: `pool3` ; バックエンド プールコンフィグレーション: `NIC` ; IP 構成: `broker-node-3`

5. **Inbound rules**タブで、次の3つの負荷分散規則を追加します。

    1. ルール1

        - **Name**: `rule1`
        - **IP version**: `IPv4`
        - **Frontend IP address**: `kafka-lb-ip`
        - **Backend pool**: `pool1`
        - **Protocol**： `TCP`
        - **Port**: `9093`
        - **Backend port**: `39092`
        - **Health probe**: **Create New**をクリックし、プローブ情報を入力します。
            - **Name**: `kafka-lb-hp`
            - **Protocol**： `TCP`
            - **Port**: `39092`

    2. ルール2

        - **Name**: `rule2`
        - **IP version**: `IPv4`
        - **Frontend IP address**: `kafka-lb-ip`
        - **Backend pool**: `pool2`
        - **Protocol**： `TCP`
        - **Port**: `9094`
        - **Backend port**: `39092`
        - **Health probe**: **Create New**をクリックし、プローブ情報を入力します。
            - **Name**: `kafka-lb-hp`
            - **Protocol**： `TCP`
            - **Port**: `39092`

    3. ルール3

        - **Name**: `rule3`
        - **IP version**: `IPv4`
        - **Frontend IP address**: `kafka-lb-ip`
        - **Backend pool**: `pool3`
        - **Protocol**： `TCP`
        - **Port**: `9095`
        - **Backend port**: `39092`
        - **Health probe**: **Create New**をクリックし、プローブ情報を入力します。
            - **Name**: `kafka-lb-hp`
            - **Protocol**： `TCP`
            - **Port**: `39092`

6. **Next : Outbound rule**をクリックし、 **Next : Tags >**をクリックしてから、 **[次へ: 確認と作成]**をクリックして情報を確認します。

7. **Create**をクリックします。

### 2. プライベートリンクサービスを設定する {#2-set-up-private-link-service}

1. [Azureポータル](https://portal.azure.com/)にログインし、 [プライベートリンクサービス](https://portal.azure.com/#view/Microsoft_Azure_Network/PrivateLinkCenterBlade/~/privatelinkservices)ページに移動して、 **+ Create**をクリックし、Kafka ロードバランサーのプライベートリンクサービスを作成します。

2. **Basic**タブで、 **Subscription** 、 **Resource group** 、 **Region**を選択し、 **Name**フィールドに`kafka-pls`と入力して、 **[次へ: 送信設定 &gt;]**をクリックします。

3. **Outbound settings**タブで、次のようにパラメータを入力し、 **Next : Access security &gt;**をクリックします。

    - **Load balancer**： `kafka-lb`
    - **ロードバランサのフロントエンド IP アドレス**: `kafka-lb-ip`
    - **Source NAT subnet**: `kafka-pls-vnet/brokers-subnet`

4. **Access security**タブで、次の操作を行います。

    - **表示**については、 **Restricted by subscription**または**Anyone with your alias**を選択します。
    - **Subscription-level access and auto-approval**については、**Add subscriptions**をクリックして、 [前提条件](#prerequisites)で取得したTiDB Cloud Azure アカウントのサブスクリプションを追加します。

5. **Next : Tags >**をクリックし、 **Next : Review + create &gt;**をクリックして情報を確認します。

6. **Create**をクリックします。操作が完了したら、後で使用するためにプライベートリンクサービスのエイリアスを書き留めておきます。

## ステップ3. TiDB Cloudから接続する {#step-3-connect-from-tidb-cloud}

1. [TiDB Cloudコンソール](https://tidbcloud.com)に戻り、クラスターが**Private Link**経由で Kafka クラスターに接続するための変更フィードを作成します。詳細については、 [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)を参照してください。

2. **Configure the changefeed target** &gt; **Connectivity Method** &gt; **Private Link**に進むときは、次のフィールドに対応する値を入力し、必要に応じてその他のフィールドを入力します。

    - **Kafka Advertised Listener Pattern**: [前提条件](#prerequisites)で**Kafka Advertised Listener Pattern**を生成するために使用する一意のランダム文字列。
    - **プライベートリンクサービスのエイリアス**: [2. プライベートリンクサービスを設定する](#2-set-up-private-link-service)で取得したプライベートリンクサービスのエイリアス。
    - **Bootstrap Ports**: `9093,9094,9095` 。

3. [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)の手順に進みます。

これでタスクは正常に完了しました。

## FAQ {#faq}

### 2つの異なるTiDB Cloudプロジェクトから同じ Kafka Private Link サービスに接続するにはどうすればよいですか? {#how-to-connect-to-the-same-kafka-private-link-service-from-two-different-tidb-cloud-projects}

このドキュメントの手順に従って最初のプロジェクトからの接続をすでに正常に設定している場合は、次のようにして 2 番目のプロジェクトから同じ Kafka Private Link サービスに接続できます。

1. このドキュメントの冒頭の指示に従ってください。

2. [ステップ1. Kafkaクラスターをセットアップする](#step-1-set-up-a-kafka-cluster)に進んだら、 [実行中の Kafka クラスターを再構成する](#reconfigure-a-running-kafka-cluster)に進み、EXTERNAL リスナーとアドバタイズリスナーの別のグループを作成します。このグループの名前は**EXTERNAL2**とします。EXTERNAL2**の**ポート範囲は**EXTERNAL**と重複する可能性があることに注意してください。

3. ブローカーを再構成した後、新しいロードバランサーと新しいプライベートリンクサービスを作成します。

4. 次の情報を使用してTiDB Cloud接続を構成します。

    - 新しい Kafka 広告リスナー グループ
    - 新しいプライベートリンクサービス
