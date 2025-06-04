---
title: Set Up Self-Hosted Kafka Private Link Service in Azure
summary: This document explains how to set up Private Link service for self-hosted Kafka in Azure and how to make it work with TiDB Cloud.
---

# Set Up Self-Hosted Kafka Private Link Service in Azure

This document describes how to set up Private Link service for self-hosted Kafka in Azure, and how to make it work with TiDB Cloud.

The mechanism works as follows:

1. The TiDB Cloud virtual network connects to the Kafka virtual network through private endpoints.
2. Kafka clients need to communicate directly to all Kafka brokers.
3. Each Kafka broker is mapped to a unique port of endpoints within the TiDB Cloud virtual network.
4. Leverage the Kafka bootstrap mechanism and Azure resources to achieve the mapping.

The following diagram shows the mechanism.

![Connect to Azure Self-Hosted Kafka Private Link Service](/media/tidb-cloud/changefeed/connect-to-azure-self-hosted-kafka-privatelink-service.png)

The document provides an example of connecting to a Kafka Private Link service in Azure. While other configurations are possible based on similar port-mapping principles, this document covers the fundamental setup process of the Kafka Private Link service. For production environments, a more resilient Kafka Private Link service with enhanced operational maintainability and observability is recommended.

## Prerequisites

1. Ensure that you have the following authorization to set up a Kafka Private Link service in your own Azure account.

    - Manage virtual machines
    - Manage virtual networks
    - Manage load balancers
    - Manage private link services
    - Connect to virtual machines to configure Kafka nodes

2. [Create a TiDB Cloud Dedicated cluster](/tidb-cloud/create-tidb-cluster.md) on Azure if you do not have one.

3. Get the Kafka deployment information from your [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster.

    1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.
    2. In the left navigation pane, click **Changefeed**.
    3. On the **Changefeed** page, click **Create Changefeed** in the upper-right corner.
        1. In **Destination**, select **Kafka**.
        2. In **Connectivity Method**, select **Private Link**.
    4. Note down the region information and the subscription of the TiDB Cloud Azure account in **Reminders before proceeding**. You will use it to authorize TiDB Cloud to access the Kafka Private Link service.
    5. Generate the **Kafka Advertised Listener Pattern** for your Kafka Private Link service by providing a unique random string.
        1. Input a unique random string. It can only include numbers or lowercase letters. You will use it to generate **Kafka Advertised Listener Pattern** later.
        2. Click **Check usage and generate** to check if the random string is unique and generate **Kafka Advertised Listener Pattern** that will be used to assemble the EXTERNAL advertised listener for Kafka brokers.

Note down all the deployment information. You need to use it to configure your Kafka Private Link service later.

The following table shows an example of the deployment information.

| Information     | Value    | Note    |
|--------|-----------------|---------------------------|
| Region | Virginia (`eastus`) | N/A |
| Subscription of TiDB Cloud Azure account | `99549169-6cee-4263-8491-924a3011ee31` | N/A |
| Kafka Advertised Listener Pattern | The unique random string: `abc` | Generated pattern: `<broker_id>.abc.eastus.azure.3199745.tidbcloud.com:<port>`; |

## Step 1. Set up a Kafka cluster

If you need to deploy a new cluster, follow the instructions in [Deploy a new Kafka cluster](#deploy-a-new-kafka-cluster).

If you need to expose an existing cluster, follow the instructions in [Reconfigure a running Kafka cluster](#reconfigure-a-running-kafka-cluster).

### Deploy a new Kafka cluster

#### 1. Set up the Kafka virtual network

1. Log in to the [Azure portal](https://portal.azure.com/), go to the [Virtual networks](https://portal.azure.com/#browse/Microsoft.Network%2FvirtualNetworks) page, and then click **+ Create** to create a virtual network.
2. In the **Basic** tab, select your **Subscription**, **Resource group**, and **Region**, enter a name (for example, `kafka-pls-vnet`) in the **Virtual network name** field, and then click **Next**.
3. In the **Security** tab, enable Azure Bastion, and then click **Next**.
4. In the **IP addresses** tab, do the following:

    1. Set the address space of your virtual network, for example, `10.0.0.0/16`.
    2. Click **Add a subnet** to create a subnet for brokers, fill in the following information, and then click **Add**.
        - **Name**: `brokers-subnet`
        - **IP address range**: `10.0.0.0/24`
        - **Size**: `/24 (256 addresses)`

        An `AzureBastionSubnet` will be created by default.

5. Click **Review + create** to verify the information.
6. Click **Create**.

#### 2. Set up Kafka brokers

**2.1. Create broker nodes**

1. Log in to the [Azure portal](https://portal.azure.com/), go to the [Virtual machines](https://portal.azure.com/#view/Microsoft_Azure_ComputeHub/ComputeHubMenuBlade/~/virtualMachinesBrowse) page, click **+ Create**, and then select **Azure virtual machine**.
2. In the **Basic** tab, select your **Subscription**, **Resource group**, and **Region**, fill in the following information, and then click **Next : Disks**.
    - **Virtual machine name**: `broker-node`
    - **Availability options**: `Availability zone`
    - **Zone options**: `Self-selected zone`
    - **Availability zone**: `Zone 1`, `Zone 2`, `Zone 3`
    - **Image**: `Ubuntu Server 24.04 LTS - x64 Gen2`
    - **VM architecture:** `x64`
    - **Size**: `Standard_D2s_v3`
    - **Authentication type**: `SSH public key`
    - **Username**: `azureuser`
    - **SSH public key source:** `Generate new key pair`
    - **Key pair name**: `kafka_broker_key`
    - **Public inbound ports**: `Allow selected ports`
    - **Select inbound ports**: `SSH (22)`
3. Click **Next : Networking**, and then fill in the following information in the **Networking** tab:
    - **Virtual network**: `kafka-pls-vnet`
    - **Subnet**: `brokers-subnet`
    - **Public IP**: `None`
    - **NIC network security group**: `Basic`
    - **Public inbound ports**: `Allow selected ports`
    - Select inbound ports: `SSH (22)`
    - **Load balancing options**: `None`
4. Click **Review + create** to verify the information.
5. Click **Create**. A **Generate new key pair** message is displayed.
6. Click **Download private key and create resource** to download the private key to your local machine. You can see the progress of virtual machine creation.

**2.2. Prepare Kafka runtime binaries**

After the deployment of your virtual machine is completed, take the following steps:

1. In the [Azure portal](https://portal.azure.com/), go to the [**Resource groups**](https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView) page, click your resource group name, and then navigate to the page of each broker node (`broker-node-1`, `broker-node-2`, and `broker-node-3`).

2. On each page of the broker node, click **Connect > Bastion** in the left navigation pane, and then fill in the following information:

    - **Authentication Type**: `SSH Private Key from Local File`
    - **Username**: `azureuser`
    - **Local File**: select the private key file that you downloaded before
    - Select the **Open in new browser tab** option

3. On each page of the broker node, click **Connect** to open a new browser tab with a Linux terminal. For the three broker nodes, you need to open three browser tabs with Linux terminals.

4. In each Linux terminal, run the following commands to download binaries in each broker node.

    ```shell
    # Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

**2.3. Set up Kafka nodes on each broker node**

1. Set up a KRaft Kafka cluster with three nodes. Each node serves both as a broker and a controller. For each broker node:

    1. Configure `listeners`. All three brokers are the same and act as brokers and controller roles.
        1. Configure the same CONTROLLER listener for all **controller** role nodes. If you only want to add the broker role nodes, you can omit the CONTROLLER listener in `server.properties`.
        2. Configure two broker listeners: **INTERNAL** for internal Kafka client access and **EXTERNAL** for access from TiDB Cloud.

    2. For `advertised.listeners`, do the following:
        1. Configure an INTERNAL advertised listener for each broker using the internal IP address of the broker node, which allows internal Kafka clients to connect to the broker via the advertised address.
        2. Configure an EXTERNAL advertised listener based on **Kafka Advertised Listener Pattern** you get from TiDB Cloud for each broker node to help TiDB Cloud distinguish between different brokers. Different EXTERNAL advertised listeners help Kafka clients from the TiDB Cloud side route requests to the right broker.
            - Use different `<port>` values to differentiate brokers in Kafka Private Link service access. Plan a port range for the EXTERNAL advertised listeners of all brokers. These ports do not have to be actual ports listened to by brokers. They are ports listened to by the load balancer in the Private Link service that will forward requests to different brokers.
            - It is recommended to configure different broker IDs for different brokers to make it easy for troubleshooting.

    3. The planning values:
        - CONTROLLER port: `29092`
        - INTERNAL port: `9092`
        - EXTERNAL port: `39092`
        - Range of the EXTERNAL advertised listener ports: `9093~9095`

2. Use SSH to log in to each broker node. Create a configuration file `~/config/server.properties` with the following content for each broker node respectively.

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

3. Create a script, and then execute it to start the Kafka broker in each broker node.

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

**2.4. Test the cluster setting**

1. Test the Kafka bootstrap.

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

2. Create a producer script `produce.sh` in the bastion node.

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

3. Create a consumer script `consume.sh` in the bastion node.

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

4. Run the `produce.sh` and `consume.sh` scripts. These scripts automatically test connectivity and message flow to verify that the Kafka cluster is functioning correctly. The `produce.sh` script creates a topic with `--partitions 3 --replication-factor 3`, sends test messages, and connects to all three brokers using the `--broker-list` parameter. The `consume.sh` script reads messages from the topic to confirm successful message delivery.

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

### Reconfigure a running Kafka cluster

Ensure that your Kafka cluster is deployed in the same region as the TiDB cluster.

**1. Configure the EXTERNAL listener for brokers**

The following configuration applies to a Kafka KRaft cluster. The ZK mode configuration is similar.

1. Plan configuration changes.

    1. Configure an EXTERNAL **listener** for every broker for external access from TiDB Cloud. Select a unique port as the EXTERNAL port, for example, `39092`.
    2. Configure an EXTERNAL **advertised listener** based on **Kafka Advertised Listener Pattern** you get from TiDB Cloud for every broker node to help TiDB Cloud differentiate between different brokers. Different EXTERNAL advertised listeners help Kafka clients from TiDB Cloud side route requests to the right broker.
       - `<port>` differentiates brokers from Kafka Private Link service access points. Plan a port range for EXTERNAL advertised listeners of all brokers, for example, `range from 9093`. These ports do not have to be actual ports listened to by brokers. They are ports listened to by the load balancer for Private Link service that will forward requests to different brokers.
        - It is recommended to configure different broker IDs for different brokers to make it easy for troubleshooting.

2. Use SSH to log in to each broker node. Modify the configuration file of each broker with the following content:

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

3. After you reconfigure all the brokers, restart your Kafka brokers one by one.

**2. Test EXTERNAL listener settings in your internal network**

You can download Kafka and OpenJDK in your Kafka client node.

```shell
# Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

Execute the following script to test if the bootstrap works as expected.

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

## Step 2. Expose the Kafka cluster as Private Link Service

### 1. Set up the load balancer

1. Log in to the [Azure portal](https://portal.azure.com/), go to the [Load balancing](https://portal.azure.com/#view/Microsoft_Azure_Network/LoadBalancingHubMenuBlade/~/loadBalancers) page, and then click **+ Create** to create a load balancer.
2. In the **Basic** tab, select your **Subscription**, **Resource group**, and **Region**, fill in the following instance information, and then click **Next : Frontend IP configuration >**.

    - **Name**: `kafka-lb`
    - **SKU**: `Standard`
    - **Type**: `Internal`
    - **Tier**: `Regional`

3. In the **Frontend IP configuration** tab, click **+ Add a frontend IP configuration**, fill in the following information, click **Save**, and then click **Next : Backend pools >**.

    - **Name**: `kafka-lb-ip`
    - **IP version**: `IPv4`
    - **Virtual network**: `kafka-pls-vnet`
    - **Subnet**: `brokers-subnet`
    - **Assignment**: `Dynamic`
    - **Availability zone**: `Zone-redundant`

4. In the **Backend pools** tab, add three backend pools as follows, and then click **Next : Inbound rules**.

    - Name: `pool1`; Backend Pool Configuration: `NIC`; IP configurations: `broker-node-1`
    - Name: `pool2`; Backend Pool Configuration: `NIC`; IP configurations: `broker-node-2`
    - Name: `pool3`; Backend Pool Configuration: `NIC`; IP configurations: `broker-node-3`

5. In the **Inbound rules** tab, add three load balancing rules as follows:

    1. Rule 1

        - **Name**: `rule1`
        - **IP version**: `IPv4`
        - **Frontend IP address**: `kafka-lb-ip`
        - **Backend pool**: `pool1`
        - **Protocol**: `TCP`
        - **Port**: `9093`
        - **Backend port**: `39092`
        - **Health probe**: click **Create New** and fill in the probe information.
            - **Name**: `kafka-lb-hp`
            - **Protocol**: `TCP`
            - **Port**: `39092`

    2. Rule 2

        - **Name**: `rule2`
        - **IP version**: `IPv4`
        - **Frontend IP address**: `kafka-lb-ip`
        - **Backend pool**: `pool2`
        - **Protocol**: `TCP`
        - **Port**: `9094`
        - **Backend port**: `39092`
        - **Health probe**: click **Create New** and fill in the probe information.
            - **Name**: `kafka-lb-hp`
            - **Protocol**: `TCP`
            - **Port**: `39092`

    3. Rule 3

        - **Name**: `rule3`
        - **IP version**: `IPv4`
        - **Frontend IP address**: `kafka-lb-ip`
        - **Backend pool**: `pool3`
        - **Protocol**: `TCP`
        - **Port**: `9095`
        - **Backend port**: `39092`
        - **Health probe**: click **Create New** and fill in the probe information.
            - **Name**: `kafka-lb-hp`
            - **Protocol**: `TCP`
            - **Port**: `39092`

6. Click **Next : Outbound rule**, click **Next : Tags >**, and then click **Next : Review + create** to verify the information.

7. Click **Create**.

### 2. Set up Private Link Service

1. Log in to the [Azure portal](https://portal.azure.com/), go to the [Private link services](https://portal.azure.com/#view/Microsoft_Azure_Network/PrivateLinkCenterBlade/~/privatelinkservices) page, and then click **+ Create** to create a Private Link service for the Kafka load balancer.

2. In the **Basic** tab, select your **Subscription**, **Resource group**, and **Region**, fill in `kafka-pls` in the **Name** field, and then click **Next : Outbound settings >**.

3. In the **Outbound settings** tab, fill in the parameters as follows, and then click **Next : Access security >**.

    - **Load balancer**: `kafka-lb`
    - **Load balancer frontend IP address**: `kafka-lb-ip`
    - **Source NAT subnet**: `kafka-pls-vnet/brokers-subnet`

4. In the **Access security** tab, do the following:

    - For **Visibility**, select **Restricted by subscription** or **Anyone with your alias**.
    - For **Subscription-level access and auto-approval**, click **Add subscriptions** to add the subscription of TiDB Cloud Azure account you got in [Prerequisites](#prerequisites).

5. Click **Next : Tags >**, and then click **Next : Review + create >** to verify the information.

6. Click **Create**. When the operation is done, note down the alias of the Private Link service for later use.

## Step 3. Connect from TiDB Cloud

1. Return to the [TiDB Cloud console](https://tidbcloud.com) to create a changefeed for the cluster to connect to the Kafka cluster by **Private Link**. For more information, see [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md).

2. When you proceed to **Configure the changefeed target > Connectivity Method > Private Link**, fill in the following fields with corresponding values and other fields as needed.

    - **Kafka Advertised Listener Pattern**: the unique random string that you use to generate **Kafka Advertised Listener Pattern** in [Prerequisites](#prerequisites).
    - **Alias of the Private Link Service**: the alias of the Private Link service that you got in [2. Set up Private Link Service](#2-set-up-private-link-service).
    - **Bootstrap Ports**: `9093,9094,9095`.

3. Proceed with the steps in [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md).

Now you have successfully finished the task.

## FAQ

### How to connect to the same Kafka Private Link service from two different TiDB Cloud projects?

If you have already followed this document to successfully set up the connection from the first project, you can connect to the same Kafka Private Link service from the second project as follows:

1. Follow instructions from the beginning of this document.

2. When you proceed to [Step 1. Set up a Kafka cluster](#step-1-set-up-a-kafka-cluster), follow [Reconfigure a running Kafka cluster](#reconfigure-a-running-kafka-cluster) to create another group of EXTERNAL listeners and advertised listeners. You can name it as **EXTERNAL2**. Note that the port range of **EXTERNAL2** can overlap with the **EXTERNAL**.

3. After reconfiguring brokers, create a new load balancer and a new Private Link service.

4. Configure the TiDB Cloud connection with the following information:

    - New Kafka Advertised Listener Group
    - New Private Link service
