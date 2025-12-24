---
title: Connect to AWS Self-Hosted Kafka via Private Link Connection
summary: Learn how to connect to an AWS Self-Hosted Kafka using an AWS Endpoint Service private link connection.
---

# Connect to AWS Self-Hosted Kafka via Private Link Connection

The document describes how to connect to a self-hosted Kafka cluster in AWS, using AWS Endpoint Service private link connection.

The mechanism works as follows:

1. The private link connection connects to your endpoint service with bootstrap port, it returns broker addresses with different ports. 
2. The private link connection connects to your endpoint service with broker addresses and ports.
3. Endpoint service forwards requests to your load balancers.
4. Load balancers forward requests to different Kafka brokers based on the port mapping.

## Prerequisites
   
- Ensure that you have the following permissions to set up a Kafka cluster in your own AWS account.

    - Manage EC2 nodes
    - Manage VPC
    - Manage subnets
    - Connect to EC2 nodes to configure Kafka nodes

- Ensure that you have the following authorization to set up a load balancer and endpoint service in your own AWS account.

    - Manage security groups
    - Manage load balancer
    - Manage endpoint services

- {{{ .essential }}} information: confirm that your {{{ .essential }}} is active in AWS. Retrieve and save the following details for later use:

    - Account ID
    - Availability Zones (AZ)

To view the the AWS account ID and available zones, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. On the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.
3. You can find the AWS account ID and available zones information.

The following table shows an example of the deployment information.

| Information     | Value    | Note    | 
|--------|-----------------|---------------------------|
| Region    | Oregon (`us-west-2`)    |  N/A |
| Principal of TiDB Cloud AWS Account | `arn:aws:iam::<account_id>:root`     |    N/A  |
| AZ IDs                              | <ul><li>`usw2-az1` </li><li>`usw2-az2` </li><li> `usw2-az3`</li></ul>  | Align AZ IDs to AZ names in your AWS account.<br/>Example: <ul><li> `usw2-az1` => `us-west-2a` </li><li> `usw2-az2` => `us-west-2c` </li><li>`usw2-az3` => `us-west-2b`</li></ul>  |
| Kafka Advertised Listener Pattern   | <ul><li> `usw2-az1` => &lt;broker_id&gt;.usw2-az1.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az2` => &lt;broker_id&gt;.usw2-az2.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az3` => &lt;broker_id&gt;.usw2-az3.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li></ul>    | Map AZ names to AZ-specified patterns. Make sure that you configure the right pattern to the broker in a specific AZ later. <ul><li> `us-west-2a` => &lt;broker_id&gt;.usw2-az1.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2c` => &lt;broker_id&gt;.usw2-az2.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2b` => &lt;broker_id&gt;.usw2-az3.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li></ul> `unique_name` is a placeholder. The actual value of `unique_name` will be replaced in [Step 4](#step-4-replace-the-unique-name-placeholder-in-kafka-configuration).  |

## Step 1. Set up a Kafka cluster

If you need to deploy a new cluster, follow the instructions in [Deploy a new Kafka cluster](#deploy-a-new-kafka-cluster).

If you need to expose an existing cluster, follow the instructions in [Reconfigure a running Kafka cluster](#reconfigure-a-running-kafka-cluster). 

### Deploy a new Kafka cluster

#### 1. Set up the Kafka VPC

The Kafka VPC requires the following:

- Three private subnets for brokers, one for each AZ. 
- One public subnet in any AZ with a bastion node that can connect to the internet and three private subnets, which makes it easy to set up the Kafka cluster. In a production environment, you might have your own bastion node that can connect to the Kafka VPC.

Before creating subnets, create subnets in AZs based on the mappings of AZ IDs and AZ names. Take the following mapping as an example.

- `usw2-az1` => `us-west-2a`
- `usw2-az2` => `us-west-2c`
- `usw2-az3` => `us-west-2b`

Create private subnets in the following AZs: 

- `us-west-2a`
- `us-west-2c`
- `us-west-2b`

Take the following steps to create the Kafka VPC.

**1.1. Create the Kafka VPC**

1. Go to [AWS Console > VPC dashboard](https://console.aws.amazon.com/vpcconsole/home?#vpcs:), and switch to the region in which you want to deploy Kafka.

2. Click **Create VPC**. Fill in the information on the **VPC settings** page as follows.

    1. Select **VPC only**.
    2. Enter a tag in **Name tag**, for example, `Kafka VPC`.
    3. Select **IPv4 CIDR manual input**, and enter the IPv4 CIDR, for example, `10.0.0.0/16`.
    4. Use the default values for other options. Click **Create VPC**.
    5. On the VPC detail page, take note of the VPC ID, for example, `vpc-01f50b790fa01dffa`.

**1.2. Create private subnets in the Kafka VPC**

1. Go to the [Subnets Listing page](https://console.aws.amazon.com/vpcconsole/home?#subnets:).
2. Click **Create subnet**.
3. Select **VPC ID** (`vpc-01f50b790fa01dffa` in this example) that you noted down before.
4. Add three subnets with the following information. It is recommended that you put the AZ IDs in the subnet names to make it easy to configure the brokers later, because TiDB Cloud requires encoding the AZ IDs in the broker's `advertised.listener` configuration.

    - Subnet1 in `us-west-2a`
        - **Subnet name**: `broker-usw2-az1`
        - **Availability Zone**: `us-west-2a`
        - **IPv4 subnet CIDR block**: `10.0.0.0/18`

    - Subnet2 in `us-west-2c`
        - **Subnet name**: `broker-usw2-az2`
        - **Availability Zone**: `us-west-2c`
        - **IPv4 subnet CIDR block**: `10.0.64.0/18`

    - Subnet3 in `us-west-2b`
        - **Subnet name**: `broker-usw2-az3`
        - **Availability Zone**: `us-west-2b`
        - **IPv4 subnet CIDR block**: `10.0.128.0/18`

5. Click **Create subnet**. The **Subnets Listing** page is displayed.

**1.3. Create the public subnet in the Kafka VPC**

1. Click **Create subnet**.
2. Select **VPC ID** (`vpc-01f50b790fa01dffa` in this example) that you noted down before.
3. Add the public subnet in any AZ with the following information:

   - **Subnet name**: `bastion`
   - **IPv4 subnet CIDR block**: `10.0.192.0/18`

4. Configure the bastion subnet to the Public subnet.

    1. Go to [VPC dashboard > Internet gateways](https://console.aws.amazon.com/vpcconsole/home#igws:). Create an Internet Gateway with the name `kafka-vpc-igw`.
    2. On the **Internet gateways Detail** page, in **Actions**, click **Attach to VPC** to attach the Internet Gateway to the Kafka VPC.
    3. Go to [VPC dashboard > Route tables](https://console.aws.amazon.com/vpcconsole/home#CreateRouteTable:). Create a route table to the Internet Gateway in Kafka VPC and add a new route with the following information:

       - **Name**: `kafka-vpc-igw-route-table`
       - **VPC**: `Kafka VPC`
       - **Route**: 
           - **Destination**: `0.0.0.0/0`
           - **Target**: `Internet Gateway`, `kafka-vpc-igw`

    4. Attach the route table to the bastion subnet. On the **Detail** page of the route table, click **Subnet associations > Edit subnet associations** to add the bastion subnet and save changes.

#### 2. Set up Kafka brokers

**2.1. Create a bastion node**

Go to the [EC2 Listing page](https://console.aws.amazon.com/ec2/home#Instances:). Create the bastion node in the bastion subnet.

- **Name**: `bastion-node`
- **Amazon Machine Image**: `Amazon Linux`
- **Instance Type**: `t2.small`
- **Key pair**: `kafka-vpc-key-pair`. Create a new key pair named `kafka-vpc-key-pair`. Download **kafka-vpc-key-pair.pem** to your local for later configuration.
- Network settings

    - **VPC**: `Kafka VPC`
    - **Subnet**: `bastion`
    - **Auto-assign public IP**: `Enable`
    - **Security Group**: create a new security group allow SSH login from anywhere. You can narrow the rule for safety in the production environment.

**2.2. Create broker nodes**

Go to the [EC2 Listing page](https://console.aws.amazon.com/ec2/home#Instances:). Create three broker nodes in broker subnets, one for each AZ.

- Broker 1 in subnet `broker-usw2-az1`

    - **Name**: `broker-node1`
    - **Amazon Machine Image**: `Amazon linux`
    - **Instance Type**: `t2.large`
    - **Key pair**: reuse `kafka-vpc-key-pair`
    - Network settings

        - **VPC**: `Kafka VPC`
        - **Subnet**: `broker-usw2-az1`
        - **Auto-assign public IP**: `Disable`
        - **Security Group**: create a new security group to allow all TCP from Kafka VPC. You can narrow the rule for safety in the production environment.
            - **Protocol**: `TCP`
            - **Port range**: `0 - 65535`
            - **Source**: `10.0.0.0/16`

- Broker 2 in subnet `broker-usw2-az2`

    - **Name**: `broker-node2`
    - **Amazon Machine Image**: `Amazon linux`
    - **Instance Type**: `t2.large`
    - **Key pair**: reuse `kafka-vpc-key-pair`
    - Network settings

        - **VPC**: `Kafka VPC`
        - **Subnet**: `broker-usw2-az2`
        - **Auto-assign public IP**: `Disable`
        - **Security Group**: create a new security group to allow all TCP from Kafka VPC. You can narrow the rule for safety in the production environment.
            - **Protocol**: `TCP`
            - **Port range**: `0 - 65535`
            - **Source**: `10.0.0.0/16`

- Broker 3 in subnet `broker-usw2-az3`

    - **Name**: `broker-node3`
    - **Amazon Machine Image**: `Amazon linux`
    - **Instance Type**: `t2.large`
    - **Key pair**: reuse `kafka-vpc-key-pair`
    - Network settings

        - **VPC**: `Kafka VPC`
        - **Subnet**: `broker-usw2-az3`
        - **Auto-assign public IP**: `Disable`
        - **Security Group**: create a new security group to allow all TCP from Kafka VPC. You can narrow the rule for safety in the production environment.
            - **Protocol**: `TCP`
            - **Port range**: `0 - 65535`
            - **Source**: `10.0.0.0/16`

**2.3. Prepare Kafka runtime binaries**

1. Go to the detail page of the bastion node. Get the **Public IPv4 address**. Use SSH to log in to the node with the previously downloaded `kafka-vpc-key-pair.pem`.

    ```shell
    chmod 400 kafka-vpc-key-pair.pem
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{bastion_public_ip} # replace {bastion_public_ip} with the IP address of your bastion node, for example, 54.186.149.187
    scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem ec2-user@{bastion_public_ip}:~/
    ```

2. Download binaries.

    ```shell
    # Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. Copy binaries to each broker node.

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

**2.4. Set up Kafka nodes on each broker node**

**2.4.1 Set up a KRaft Kafka cluster with three nodes**

Each node will act as a broker and controller role. Do the following for each broker:

1. For the `listeners` item, all three brokers are the same and act as broker and controller roles: 

    1. Configure the same CONTROLLER listener for all **controller** role nodes. If you only want to add the **broker** role nodes, you do not need the CONTROLLER listener in `server.properties`.
    2. Configure two **broker** listeners, `INTERNAL` for internal access and `EXTERNAL` for external access from TiDB Cloud.

2. For the `advertised.listeners` item, do the following:

    1. Configure an INTERNAL advertised listener for every broker with the internal IP of the broker node. Advertised internal Kafka clients use this address to visit the broker.
    2. Configure an EXTERNAL advertised listener based on **Kafka Advertised Listener Pattern** you get from TiDB Cloud for each broker node to help TiDB Cloud differentiate between different brokers. Different EXTERNAL advertised listeners help the Kafka client from TiDB Cloud route requests to the right broker.

        - `<port>` differentiates brokers from Kafka Private Link Service access points. Plan a port range for EXTERNAL advertised listeners of all brokers. These ports do not have to be actual ports listened to by brokers. They are ports listened to by the load balancer for Private Link Service that will forward requests to different brokers.
        - `AZ ID` in **Kafka Advertised Listener Pattern** indicates where the broker is deployed. TiDB Cloud will route requests to different endpoint DNS names based on the AZ ID.
     
      It is recommended to configure different broker IDs for different brokers to make it easy for troubleshooting.

3. The planning values are as follows:

    - **CONTROLLER port**: `29092`
    - **INTERNAL port**: `9092`
    - **EXTERNAL**: `39092`
    - **EXTERNAL advertised listener ports range**: `9093~9095`

**2.4.2. Create a configuration file**

Use SSH to log in to every broker node. Create a configuration file `~/config/server.properties` with the following content.  

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

**2.4.3 Start Kafka brokers**

Create a script, and then execute it to start the Kafka broker in each broker node.

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

**2.5. Test the cluster setting in the bastion node**

1. Test the Kafka bootstrap.

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

2. Create a producer script `produce.sh` in the bastion node.

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

3. Create a consumer script `consume.sh` in the bastion node.

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

4. Execute `produce.sh` and `consume.sh` to verify that the Kafka cluster is running. These scripts will also be reused for later network connection testing. The script will create a topic with `--partitions 3 --replication-factor 3`. Ensure that all these three brokers contain data. Ensure that the script will connect to all three brokers to guarantee that network connection will be tested.

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

Ensure that your Kafka cluster is deployed in the same region and AZs as the TiDB cluster. If any brokers are in different AZs, move them to the correct ones.

#### 1. Configure the EXTERNAL listener for brokers

The following configuration applies to a Kafka KRaft cluster. The ZK mode configuration is similar.

1. Plan configuration changes.

    1. Configure an EXTERNAL **listener** for every broker for external access from TiDB Cloud. Select a unique port as the EXTERNAL port, for example, `39092`.
    2. Configure an EXTERNAL **advertised listener** based on **Kafka Advertised Listener Pattern** you get from TiDB Cloud for every broker node to help TiDB Cloud differentiate between different brokers. Different EXTERNAL advertised listeners help Kafka clients from TiDB Cloud route requests to the right broker.

        - `<port>` differentiates brokers from Kafka Private Link Service access points. Plan a port range for EXTERNAL advertised listeners of all brokers, for example, `range from 9093`. These ports do not have to be actual ports listened to by brokers. They are ports listened to by the load balancer for Private Link Service that will forward requests to different brokers.
        - `AZ ID` in **Kafka Advertised Listener Pattern** indicates where the broker is deployed. TiDB Cloud will route requests to different endpoint DNS names based on the AZ ID.
      
      It is recommended to configure different broker IDs for different brokers to make it easy for troubleshooting.

2. Use SSH to log in to each broker node. Modify the configuration file of each broker with the following content:

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

3. After you reconfigure all the brokers, restart your Kafka brokers one by one.

#### 2. Test EXTERNAL listener settings in your internal network

You can download the Kafka and OpenJDK on you Kafka client node.

```shell
# Download Kafka and OpenJDK, and then extract the files. You can choose the binary version based on your preference.
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

Execute the following script to test if the bootstrap works as expected.

```shell
export JAVA_HOME=/home/ec2-user/jdk-22.0.2

# Bootstrap from the EXTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# Expected output for the last 3 lines (the actual order might be different)
# There will be some exceptions or errors because advertised listeners cannot be resolved in your Kafka network. 
# We will make them resolvable in TiDB Cloud side and make it route to the right broker when you create a changefeed connect to this Kafka cluster by Private Link. 
b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## Step 2. Expose the Kafka cluster as a private link service

### 1. Set up the load balancer

Create a network load balancer with four target groups with different ports. One target group is for bootstrap, and the others will map to different brokers.

1. bootstrap target group => 9092 => broker-node1:39092,broker-node2:39092,broker-node3:39092
2. broker target group 1  => 9093 => broker-node1:39092
3. broker target group 2  => 9094 => broker-node2:39092
4. broker target group 3  => 9095 => broker-node3:39092

If you have more broker role nodes, you need to add more mappings. Ensure that you have at least one node in the bootstrap target group. It is recommended to add three nodes, one for each AZ for resilience.

Do the following to set up the load balancer:

1. Go to [Target groups](https://console.aws.amazon.com/ec2/home#CreateTargetGroup:) to create four target groups.

    - Bootstrap target group 

        - **Target type**: `Instances`
        - **Target group name**: `bootstrap-target-group`
        - **Protocol**: `TCP`
        - **Port**: `9092`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node1:39092`, `broker-node2:39092`, `broker-node3:39092`

    - Broker target group 1

        - **Target type**: `Instances`
        - **Target group name**: `broker-target-group-1`
        - **Protocol**: `TCP`
        - **Port**: `9093`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node1:39092`

    - Broker target group 2

        - **Target type**: `Instances`
        - **Target group name**: `broker-target-group-2`
        - **Protocol**: `TCP`
        - **Port**: `9094`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node2:39092`

    - Broker target group 3

        - **Target type**: `Instances`
        - **Target group name**: `broker-target-group-3`
        - **Protocol**: `TCP`
        - **Port**: `9095`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node3:39092`

2. Go to [Load balancers](https://console.aws.amazon.com/ec2/home#LoadBalancers:) to create a network load balancer.

    - **Load balancer name**: `kafka-lb`
    - **Schema**: `Internal`
    - **Load balancer IP address type**: `IPv4`
    - **VPC**: `Kafka VPC`
    - **Availability Zones**: 
        - `usw2-az1` with `broker-usw2-az1 subnet`
        - `usw2-az2` with `broker-usw2-az2 subnet`
        - `usw2-az3` with `broker-usw2-az3 subnet`
    - **Security groups**: create a new security group with the following rules.
        - Inbound rule allows all TCP from Kafka VPC: Type - `{ports of target groups}`, for example, `9092-9095`; Source - `{CIDR of TiDB Cloud}`. To get the CIDR of TiDB Cloud in the region, switch to your target project using the combo box in the upper-left corner of the [TiDB Cloud console](https://tidbcloud.com), click **Project Settings** > **Network Access** in the left navigation pane, and then click **Project CIDR** > **AWS**.
        - Outbound rule allows all TCP to Kafka VPC: Type - `All TCP`; Destination - `Anywhere-IPv4`
    - Listeners and routing:
        - Protocol: `TCP`; Port: `9092`; Forward to: `bootstrap-target-group`
        - Protocol: `TCP`; Port: `9093`; Forward to: `broker-target-group-1`
        - Protocol: `TCP`; Port: `9094`; Forward to: `broker-target-group-2`
        - Protocol: `TCP`; Port: `9095`; Forward to: `broker-target-group-3`

3. Test the load balancer in the bastion node. This example only tests the Kafka bootstrap. Because the load balancer is listening on the Kafka EXTERNAL listener, the addresses of EXTERNAL advertised listeners can not be resolved in the bastion node. Note down the `kafka-lb` DNS name from the load balancer detail page, for example `kafka-lb-77405fa57191adcb.elb.us-west-2.amazonaws.com`. Execute the script in the bastion node.

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

### 2. Set up AWS Endpoint Service

1. Go to [Endpoint service](https://console.aws.amazon.com/vpcconsole/home#EndpointServices:). Click **Create endpoint service** to create a Private Link service for the Kafka load balancer.

    - **Name**: `kafka-pl-service`
    - **Load balancer type**: `Network`
    - **Load balancers**: `kafka-lb`
    - **Included Availability Zones**: `usw2-az1`,`usw2-az2`, `usw2-az3`
    - **Require acceptance for endpoint**: `Acceptance required`
    - **Enable private DNS name**: `No`

2. Note down the **Service name**. You need to provide it to TiDB Cloud, for example `com.amazonaws.vpce.us-west-2.vpce-svc-0f49e37e1f022cd45`.

3. On the detail page of the kafka-pl-service, click the **Allow principals** tab, and allow the AWS account of TiDB Cloud to create the endpoint. You can get the AWS account of TiDB Cloud in [Prerequisites](#prerequisites), for example, `arn:aws:iam::<account_id>:root`.

## Step 3. Create a Private Link Connection in TiDB Cloud

### 1. Create the AWS Endpoint Service Private Link connection

You can also refer to [Create an AWS Endpoint Service Private Link Connection](/tidbcloud/serverless-private-link-connection#create-an-aws-endpoint-service-private-link-connection) for more details.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.

4. Enter the required information in the **Create Private Link Connection** dialog:

    - **Private Link Connection Name**: Enter a name for the Private Link Connection.
    - **Connection Type**: Choose **AWS Endpoint Service**, if you can not find this option, please ensure that your cluster is created in AWS provider.
    - **Endpoint Service Name**: Enter the endpoint service name (for example, `com.amazonaws.vpce.<region>.vpce-svc-xxxx`).

5. Click the **Create Connection** button.

6. Then go to the detail page of your endpoint service on AWS console. In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
```

Then go to the detail page of your endpoint service on AWS console. In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

</div>
</SimpleTab>

### 2. Attach Domains to the Private Link Connection

You can also refer to [Attach Domains to a Private Link Connection](/tidbcloud/serverless-private-link-connection#attach-domains-to-a-private-link-connection) for more details.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target Private Link Connection and click **...**.

4. Click **Attach Domains**.

5. In the **Attach Domains** dialog, select the **TiDB Cloud Managed** domain type. The domains will be auto-generated by TiDB Cloud. Copy the unique name for later use and click **Attach Domains** to confirm. For example, if the generated domain is `*.use1-az1.dvs6nl5jgveztmla3pxkxgh76i.aws.plc.tidbcloud.com`, then the unique name is `dvs6nl5jgveztmla3pxkxgh76i`.

</div>

<div label="CLI">

First, use a dry run to preview the domains to be attached. This will output a `unique-name` for the next step. Copy it for later use.

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --dry-run
```

Then, attach the domains with the `unique-name` from the previous step.

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --unique-name <unique-name>
```

</div>
</SimpleTab>

## Step 4. Replace the Unique Name placeholder in Kafka configuration

1. Go back to your Kafka broker nodes, replace the `unique_name` placeholder in `advertised.listeners` configuration of each broker with the actual unique name you get from the previous step.
2. After you reconfigure all the brokers, restart your Kafka brokers one by one.

Now, you can use this private link connection and 9092 as bootstrap port to connect to your Kafka cluster from TiDB Cloud.
