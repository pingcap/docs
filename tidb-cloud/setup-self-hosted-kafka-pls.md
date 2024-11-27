---
title: Set Up Self-Hosted Kafka Private Link Service in AWS
summary: This document explains how to set up Private Link service for self-hosted Kafka in AWS and how to make it work with TiDB Cloud.
---

# Set up Self-Hosted Kafka Private Link Service in AWS

This document describes how to set up Private Link service for self-hosted Kafka in AWS, and how to make it work with TiDB Cloud.

The mechanism works as follows:

1. TiDB Cloud VPC connects to Kafka VPC through limit private endpoints.
2. Kafka clients need to talk directly to all Kafka brokers.
3. Map every Kafka brokers to different ports to make every broker is unique in TiDB Cloud VPC.
4. Leverage Kafka bootstrap mechanism and AWS cloud resources to achieve the mapping.

The following diagram shows the mechanism. 

![main idea](/media/tidb-cloud/changefeed/connect-to-aws-self-hosted-kafka-privatelink-service.png)

The document uses an example to show how to connect to a three AZ Kafka Private Link service in AWS. There are other ways based on the similar port mapping mechanism. This document only shows fundamental process of the Kafka Private Link service. If you want to set up Kafka Private Link service in a production envrionment, you need to build a more resilient Kafka Private Link service with better operational maintainability and observability.

## Prerequisites

1. Ensure that you have authorization to set up Kafka Private Link service in your own AWS account. 

    - Manage EC2 Nodes
    - Manage VPC
    - Manage Subnet
    - Manage Security Group
    - Manage Load Balancer
    - Manage Endpoint Service
    - Connect to EC2 Nodes to configure Kafka nodes

2. Make sure that you create a TiDB Cloud Dedicated cluster in AWS first. Align Kafka deployment info with TiDB Cluster.

    1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Changefeed** in the left navigation pane.
    2. In the overview page, you can find the region of TiDB Cluster, make sure your Kafka cluster will be deployed to the same region.
    3. Click **Create Changefeed**
       1. Select **Kafka** as **Target Type**.
       2. Select **Private Link** as **Connectivity Method**
    4. Take note the principal of TiDB Cloud AWS account in **Reminders before proceeding** information, which your will use it to authorize TiDB Cloud to create endpoint for the Kafka Private Link service.
    5. Select **Number of AZs**, confirm you will deploy Kafka cluster to **Single AZ** or **3 AZ**. Here we select **3 AZ**. Take note of the AZ IDs you want to deploy your Kafka cluster. If you don't know the relationship between your AZ names and AZ IDs, please refer to [AWS document](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html) to find it.
    6. Pick a unique **Kafka Advertised Listener Pattern** for your Kafka Private Link service
        1. Input a unique random string can only include numbers or lowercase letters, which will be used to generate **Kafka Advertised Listener Pattern** later.
        2. Click **Check usage and generate** button to check if the random string is unique and generate **Kafka Advertised Listener Pattern** which will be used to assemble EXTERNAL advertised listener for kafka brokers. 

Note down all the deployment information. You need to use is to configure your Kafka Private Link service later.


The following is an example of the deployment information.

| Information                         | Value                                                                                                                                                                                                                                                                                                                                                                                   | Reminder                                                                                                                                                                                                                                                                                                                                                                                                                                     | 
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Region                              | Oregon (us-west-2)                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Principal of TiDB Cloud AWS Account | arn:aws:iam::<account_id>:root                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| AZ IDs                              | 1. usw2-az1 <br/> 2. usw2-az2 <br/> 3. usw2-az3                                                                                                                                                                                                                                                                                                                                         | Align AZ IDs to AZ names in your AWS account.<br/>Example: <br/> 1. usw2-az1 => us-west-2a <br/> 2. usw2-az2 => us-west-2c <br/> 3. usw2-az3 => us-west-2b                                                                                                                                                                                                                                                                            |
| Kafka Advertised Listener Pattern   | The unique random string: abc <br/> Generated pattern for AZs <br/> 1. usw2-az1 => &lt;broker_id&gt;.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; <br/> 2. usw2-az2 => &lt;broker_id&gt;.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; <br/> 3. usw2-az3 => &lt;broker_id&gt;.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt;            | Map AZ names to AZ-specified patterns. Make sure you can configure the right pattern to the broker in specific AZ later <br/> 1. us-west-2a => &lt;broker_id&gt;.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; <br/> 2. us-west-2c => &lt;broker_id&gt;.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; <br/> 3. us-west-2b => &lt;broker_id&gt;.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; |


## Step 2. Set up Kafka Cluster

Jump to "Reconfigure a Running Kafka Cluster" section if you want to expose existing cluster; Refer to "Deploy a New Kafka Cluster" if you set up a new cluster.

### Deploy a New Kafka Cluster

#### 1. Set up Kafka VPC

Kafka VPC requirements:

1. 3 private subnets for brokers, one per AZ. 
2. 1 public subnet in any AZ with a bastion node that can connect to Internet and the 3 private subnets, which make kafka cluster setup easy. In the real production environment, your may have your own bastion node that can connect to the Kafka VPC.

Before creating subnets, you should create subnets in AZs based on the AZ ID to AZ names mapping. Take following mapping as an example.

1. usw2-az1 => us-west-2a
2. usw2-az2 => us-west-2c
3. usw2-az3 => us-west-2b

You should create private subnets in this three AZs: us-west-2a, us-west-2c, us-west-2b.

Here is the detail steps to create Kafka VPC:

##### 1.1. Create Kafka VPC

1. Go to [AWS Console->VPC dashboard](https://console.aws.amazon.com/vpcconsole/home?#vpcs:), switch to the region you want to deploy Kafka.

2. Click "Create VPC" button, fill the form in "VPC settings" page.
   1. Select "VPC only".
   2. Fill the "Name tag", for example ```Kafka VPC```.
   3. Select "IPv4 CIDR manual input", fill "IPv4 CIDR", for example ```10.0.0.0/16```.
   4. Leave other options as default, click "Create VPC" button.
   5. If nothing wrong, page will navigate to the VPC detail page. Take note of the VPC ID,for example ```vpc-01f50b790fa01dffa```

##### 1.2. Create private subnets in Kafka VPC

1. Go to [Subnets Listing Page](https://console.aws.amazon.com/vpcconsole/home?#subnets:)
2. Click "Create subnet" button, navigate "Create subnet" page.
3. Select "VPC ID" (```vpc-01f50b790fa01dffa```) we take note before.
4. Add 3 subnets with following inputs, suggest put AZ ID in subnet name to make it easy to configure broker later since TiDB Cloud require encoding AZ ID in broker's "advertised.listener" configuration

   1. Subnet1 in us-west-2a
      - Subnet name: broker-usw2-az1
      - Availability Zone: us-west-2a
      - IPv4 subnet CIDR block: 10.0.0.0/18
   2. Subnet2 in us-west-2c
      - Subnet name: broker-usw2-az2
      - Availability Zone: us-west-2c
      - IPv4 subnet CIDR block: 10.0.64.0/18
   3. Subnet3 in us-west-2b
      - Subnet name: broker-usw2-az3
      - Availability Zone: us-west-2b
      - IPv4 subnet CIDR block: 10.0.128.0/18

5. Click "Create subnet" button, if nothing wrong, it will navigate to "Subnets Listing Page".

##### 1.3. Create the public subnet in Kafka VPC

1. Click "Create subnet" button, navigate to "Create subnet" page.
2. Select "VPC ID" (```vpc-01f50b790fa01dffa```) we take note before.
3. Add the public subnet in any AZ with following inputs

   - Subnet name: bastion
   - IPv4 subnet CIDR block: 10.0.192.0/18

4. Click "Create subnet" button, if nothing wrong, it will navigate to "Subnets Listing Page".
5. Config the "bastion" subnet to Public subnet

   1. Go to [VPC dashboard -> Internet gateways](https://console.aws.amazon.com/vpcconsole/home#igws:), create an Internet Gateway with name as "kafka-vpc-igw".
   2. If nothing wrong, it will navigate to "Internet gateways Detail Page", click "Actions->Attach to VPC" attach the Internet Gateway to Kafka VPC.
   3. Go to [VPC dashboard -> Route tables](https://console.aws.amazon.com/vpcconsole/home#CreateRouteTable:), create a route table to the Internet Gateway in Kafka VPC and add a new route as following values

      - Name: kafka-vpc-igw-route-table
      - VPC: Kafka VPC
      - Route:  Destination - 0.0.0.0/0; Target - Internet Gateway, kafka-vpc-igw

   4. Attach the route table to bastion subnet. At the "Detail Page" of the route table, click "Subnet associations-> Edit subnet associations" to add bastion subnet and save changes.

#### 2. Set up Kafka Brokers

##### 2.1. Create bastion node

Go to [EC2 Listing Page](https://console.aws.amazon.com/ec2/home#Instances:), create the bastion node in bastion subnet.

   - Name: bastion-node
   - Amazon Machine Image: Amazon linux
   - Instance Type: t2.small
   - Key pair: kafka-vpc-key-pair. PS: create a new key pair name "kafka-vpc-key-pair", download "kafka-vpc-key-pair.pem" to your local for following configuration.
   - Network settings

       - VPC: Kafka VPC
       - Subnet: bastion
       - Auto-assign public IP: Enable
       - Security Group: create a new security group allow ssh from anywhere. PS: you may narrow the rule for safety in production environment.

##### 2.2. Create broker nodes

Go to [EC2 Listing Page](https://console.aws.amazon.com/ec2/home#Instances:), create 3 broker nodes in broker subnet, one per AZ.

1. Broker 1 in subnet broker-usw2-az1
   - Name: broker-node1
   - Amazon Machine Image: Amazon linux
   - Instance Type: t2.large
   - Key pair: reuse "kafka-vpc-key-pair"
   - Network settings
       - VPC: Kafka VPC
       - Subnet: broker-usw2-az1
       - Auto-assign public IP: Disable
       - Security Group: create a new security group allow all TCP from Kafka VPC. PS: you may narrow the rule for safety in production environment.
          - Protocol: TCP
          - Port range: 0 - 65535
          - Source: 10.0.0.0/16

2. Broker 2 in subnet broker-usw2-az2

   - Name: broker-node2
   - Amazon Machine Image: Amazon linux
   - Instance Type: t2.large
   - Key pair: reuse "kafka-vpc-key-pair"
   - Network settings

       - VPC: Kafka VPC
       - Subnet: broker-usw2-az2
       - Auto-assign public IP: Disable
       - Security Group: create a new security group allow all TCP from Kafka VPC. PS: you may narrow the rule for safety in production environment.
          - Protocol: TCP
          - Port range: 0 - 65535
          - Source: 10.0.0.0/16

3. Broker 3 in subnet broker-usw2-az3

   - Name: broker-node3
   - Amazon Machine Image: Amazon linux
   - Instance Type: t2.large
   - Key pair: reuse "kafka-vpc-key-pair"
   - Network settings
       - VPC: Kafka VPC
       - Subnet: broker-usw2-az3
       - Auto-assign public IP: Disable
       - Security Group: create a new security group allow all TCP from Kafka VPC. PS: you may narrow the rule for safety in production environment.
          - Protocol: TCP
          - Port range: 0 - 65535
          - Source: 10.0.0.0/16

##### 2.3. Prepare kafka runtime binaries

1. Go to detail page of bastion node, get the "Public IPv4 address", ssh login to the node with previous download "kafka-vpc-key-pair.pem".

```shell
chmod 400 kafka-vpc-key-pair.pem
ssh -i "kafka-vpc-key-pair.pem" ec2-user@{bastion_public_ip} # replace {bastion_public_ip} to your bastion's ip, for example 54.186.149.187
scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem ec2-user@{bastion_public_ip}:~/
```

2. Download binaries

```shell
# Download kafka & openjdk, decompress. PS: your can choose the binary version as you like
wget https://downloads.apache.org/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```
3. Copy binaries to every broker nodes

```shell
# Replace {broker-node1-ip} to your broker-node1 ip
scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node1-ip}:~/
ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node1-ip}:~/
ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

# Replace {broker-node2-ip} to your broker-node2 ip
scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node2-ip}:~/
ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node2-ip}:~/
ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

# Replace {broker-node3-ip} to your broker-node3 ip
scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node3-ip}:~/
ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node3-ip}:~/
ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
```
##### 2.4. Set up kafka nodes in every broker node.

1. We will set up a KRaft Kafka cluster with 3 nodes, each node will act as broker and controller roles. For every broker:

   1. For "listeners" item, all 3 brokers are the same and act as broker and controller roles: 
      1. Configure the same CONTROLLER listener for all **controller** role node. if you want to add **broker** role only nodes, you don't need CONTROLLER listener in ```server.properties```.
      2. Configure two **broker** listeners. INTERNAL for internal access; EXTERNAL for external access from TiDB Cloud.
   2. For "advertised.listeners" item
      1. Configure a INTERNAL advertised listener for every broker with internal ip of broker node, advertise internal Kafka clients use this address to visit the broker.
      2. Configure a EXTERNAL advertised listener based on **Kafka Advertised Listener Pattern** we get from TiDB Cloud for every broker node to help TiDB Cloud differentiate between different brokers. Different EXTERNAL advertised listener helps Kafka client from TiDB Cloud side route request the right broker.
         - ```<port>``` differentiate brokers from Kafka Private Link Service access point, so please plan a ports range for EXTERNAL advertised listener of all brokers. These ports don't have to be actual ports listened on brokers, they are ports listened on LB for Private Link Service which will forward request to different brokers.
         - ```AZ ID``` in **Kafka Advertised Listener Pattern** indicate where the broker is deployed. TiDB Cloud will route request to different endpoint dns name based on the AZ ID.
         - Better to configure different ```<broker_id>``` for different broker, make it easy for troubleshooting.
   3. The planing values
      - CONTROLLER port: 29092
      - INTERNAL port: 9092
      - EXTERNAL: 39092
      - EXTERNAL advertised listener ports range: 9093~9095

2. ssh login to every broker node, create configuration file "~/config/server.properties" with content as following.  

```properties
# brokers in usw2-az1

# broker-node1 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} to real ips
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 2.1 The pattern for AZ(ID: usw2-az1) is "<broker_id>.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
# 2.2 So the EXTERNAL can be "b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9093) in EXTERNAL advertised listener ports range 
# 2.3 If there are more broker role node in same AZ, you can configure them in same way
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az2

# broker-node2 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} to real ips
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 2.1 The pattern for AZ(ID: usw2-az2) is "<broker_id>.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
# 2.2 So the EXTERNAL can be "b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9094) in EXTERNAL advertised listener ports range 
# 2.3 If there are more broker role node in same AZ, you can configure them in same way
process.roles=broker,controller
node.id=2
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az3

# broker-node3 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} to real ips
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 2.1 The pattern for AZ(ID: usw2-az3) is "<broker_id>.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
# 2.2 So the EXTERNAL can be "b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9095) in EXTERNAL advertised listener ports range 
# 2.3 If there are more broker role node in same AZ, you can configure them in same way
process.roles=broker,controller
node.id=3
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

2. Create script and execute it to start kafka broker in every broker node.

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

# Cleanup step make it easy to multiple experiments
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

##### 2.5. Test cluster setup in bastion node.

1. Test Kafka bootstrap

```shell
export JAVA_HOME=/home/ec2-user/jdk-22.0.2

# Bootstrap from INTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
# Expected output, order may be different.
{broker-node1-ip}:9092 (id: 1 rack: null) -> (
{broker-node2-ip}:9092 (id: 2 rack: null) -> (
{broker-node3-ip}:9092 (id: 3 rack: null) -> (

# Bootstrap from EXTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
# Expected output(last 3 lines), order may be different.
# The differences of output from "bootstrap from INTERNAL listener" is that there are exceptions or errors since advertised listeners can not be resolved in Kafka VPC.
# We will make them resolvable in TiDB Cloud side and make it route to the right broker. 
b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

2. Create producer script - "produce.sh" in bastion node

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

3. Create consumer script - "consume.sh" in bastion node

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

4. Execute "produce.sh" and "consume.sh" to verify kafka cluster is working. These scripts will also be reused for later network connection testing. The script will create a topic with ```--partitions 3 --replication-factor 3```, make sure all 3 brokers have data, make sure script will connect to all 3 brokers to guarantee network connection will be tested.

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
# Expected example output (message order may be different)
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

### Reconfigure a Running Kafka Cluster

Make sure you kafka cluster is deployed in same region as the TiDB cluster. Make sure the AZs are also the same, if not please move brokers not in same AZ to the right one.

#### 1. Configure EXTERNAL listener for brokers

The follwoing configuration is for Kafka KRaft cluster, ZK mode is similar.

1. Planning configuration changes
   1. Configure a EXTERNAL **listener** for every broker for external access from TiDB Cloud. Pick a unique port as EXTERNAL port, for example ```39092```.
   2. Configure a EXTERNAL **advertised listener** based on **Kafka Advertised Listener Pattern** we get from TiDB Cloud for every broker node to help TiDB Cloud differentiate between different brokers. Different EXTERNAL advertised listener helps Kafka client from TiDB Cloud side route request the right broker.
      - ```<port>``` differentiate brokers from Kafka Private Link Service access point, so please plan a ports range for EXTERNAL advertised listener of all brokers. These ports don't have to be actual ports listened on brokers, they are ports listened on LB for Private Link Service which will forward request to different brokers. Please plan a ports range for EXTERNAL advertised listener, for example ```range from 9093```
      - ```AZ ID``` in **Kafka Advertised Listener Pattern** indicate where the broker is deployed. TiDB Cloud will route request to different endpoint dns name based on the AZ ID.
      - Better to configure different ```<broker_id>``` for different broker, make it easy for troubleshooting.
2. ssh login to every broker node, modify the configuration file of every broker, with content as following.  

```properties
# brokers in usw2-az1

# Add EXTERNAL listener
listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

# Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 1. The pattern for AZ(ID: usw2-az1) is "<broker_id>.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
# 2. So the EXTERNAL can be "b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9093) in EXTERNAL advertised listener ports range 
advertised.listeners=...,EXTERNAL://b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093

# Configure EXTERNAL map
listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
```

```properties
# brokers in usw2-az2

# Add EXTERNAL listener
listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

# Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 1. The pattern for AZ(ID: usw2-az2) is "<broker_id>.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
# 2. So the EXTERNAL can be "b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9094) in EXTERNAL advertised listener ports range 
advertised.listeners=...,EXTERNAL://b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094

# Configure EXTERNAL map
listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
```

```properties
# brokers in usw2-az3

# Add EXTERNAL listener
listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

# Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 1. The pattern for AZ(ID: usw2-az3) is "<broker_id>.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
# 2. So the EXTERNAL can be "b2.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9095) in EXTERNAL advertised listener ports range 
advertised.listeners=...,EXTERNAL://b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095

# Configure EXTERNAL map
listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
```

3. After all the broker reconfigured, restart you Kafka brokers one by one.

#### 2. Test EXTERNAL listener setup in your internal network

You can download the Kafka and OpenJDK in you Kafka client node

```shell
# Download kafka & openjdk, decompress. PS: your can choose the binary version as you like
wget https://downloads.apache.org/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```
Test if the bootstrap is work as expected by executing following script
```shell
export JAVA_HOME=/home/ec2-user/jdk-22.0.2

# Bootstrap from EXTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# Expected output(last 3 lines), order may be different.
# There will be some exceptions or errors since advertised listeners can not be resolved in your Kafka network. 
# We will make them resolvable in TiDB Cloud side and make it route to the right broker. 
b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## Step 1. Expose the Kafka cluster as Private Link Service

### 1. Set up Load Balancer

We will need to create a NLB with 4 target groups with different ports, one for bootstrap, others will map to different brokers.

1. bootstrap target group => 9092 => broker-node1:39092,broker-node2:39092,broker-node3:39092
2. broker target group 1  => 9093 => broker-node1:39092
3. broker target group 2  => 9094 => broker-node2:39092
4. broker target group 3  => 9095 => broker-node3:39092

If you have more broker role nodes, you will need add more mapping here. There should be at least one node in bootstrap target group, it's recommend to add 3 nodes, one per AZ for resilience.

Here are the operations steps

1. Go to [Target groups](https://console.aws.amazon.com/ec2/home#CreateTargetGroup:) to create 4 Target Groups

   1. Bootstrap target group 
      - Target type: Instances
      - Target group name: bootstrap-target-group
      - Protocol: TCP
      - Port: 9092
      - IP address type: IPv4
      - VPC: Kafka VPC
      - Health check protocol: TCP
      - Register targets: broker-node1:39092,broker-node2:39092,broker-node3:39092
   2. Broker target group 1
       - Target type: Instances
       - Target group name: broker-target-group-1
       - Protocol: TCP
       - Port: 9093
       - IP address type: IPv4
       - VPC: Kafka VPC
       - Health check protocol: TCP
       - Register targets: broker-node1:39092
   3. Broker target group 2
       - Target type: Instances
       - Target group name: broker-target-group-2
       - Protocol: TCP
       - Port: 9094
       - IP address type: IPv4
       - VPC: Kafka VPC
       - Health check protocol: TCP
       - Register targets: broker-node2:39092
   4. Broker target group 3
       - Target type: Instances
       - Target group name: broker-target-group-3
       - Protocol: TCP
       - Port: 9095
       - IP address type: IPv4
       - VPC: Kafka VPC
       - Health check protocol: TCP
       - Register targets: broker-node3:39092

2. Go to [Load balancers](https://console.aws.amazon.com/ec2/home#LoadBalancers:) to create a Network Load Balancer

    - Load balancer name: kafka-lb
    - Schema: Internal
    - Load balancer IP address type: IPv4
    - VPC: Kafka VPC
    - Availability Zones: 
        - usw2-az1 with broker-usw2-az1 subnet
        - usw2-az2 with broker-usw2-az2 subnet
        - usw2-az3 with broker-usw2-az3 subnet
    - Security groups: create a new security group with rules
        - Inbound rule allows all TCP from Kafka VPC: Type - All TCP; Source - Anywhere-IPv4
        - Outbound rule allows all TCP to Kafka VPC: Type - All TCP; Destination - Anywhere-IPv4
    - Listeners and routing:
        - Protocol: TCP; Port: 9092; Forward to: bootstrap-target-group
        - Protocol: TCP; Port: 9093; Forward to: broker-target-group-1
        - Protocol: TCP; Port: 9094; Forward to: broker-target-group-2
        - Protocol: TCP; Port: 9095; Forward to: broker-target-group-3

3. Test LB in bastion node. We can only test Kafka bootstrap since LB is listening on Kafka EXTERNAL listener, the addresses of EXTERNAL advertised listeners can not be resolvable in bastion node. Take note kafka-lb DNS name from LB Detail Page, for example `kafka-lb-77405fa57191adcb.elb.us-west-2.amazonaws.com`. Execute script in bastion node

```shell
# Please replace {lb_dns_name} to the actual
export JAVA_HOME=/home/ec2-user/jdk-22.0.2
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {lb_dns_name}:9092

# Expected output(last 3 lines), order may be different.
b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException


# You can also try bootstrap in others ports 9093/9094/9095, it will succeed probabilistically since NLB in AWS resolve LB DNS to IP address of Any Availability Zone and disable cross-zone load balancing by default. 
# If you enable cross-zone load balancing in LB, it will be certainly success, but it's unnecessary, it may introduce potential cross AZ traffic.
```

### 2. Set up Private Link Service

1. Go to [Endpoint service](https://console.aws.amazon.com/vpcconsole/home#EndpointServices:), click button "Create endpoint service" to create a Private Link service for the Kafka LB.
   - Name: kafka-pl-service
   - Load balancer type: Network
   - Load balancers: kafka-lb
   - Included Availability Zones: usw2-az1, usw2-az2, usw2-az3
   - Require acceptance for endpoint: Acceptance required
   - Enable private DNS name: No

2. After creation done, take note of the **Service name** which will be provided to TiDB Cloud, for example ```com.amazonaws.vpce.us-west-2.vpce-svc-0f49e37e1f022cd45```

3. In detail page of the kafka-pl-service, click "Allow principals" tab, allow AWS account of TiDB Cloud to create endpoint. You can get the AWS account of TiDB Cloud in "Prerequisites" section, for example ```arn:aws:iam::<account_id>:root```

## Step 3. Connect from TiDB Cloud

1. Go back to TiDB Cloud console to create changefeed for the cluster to connect to Kafka cluster by **Private Link**. For the detail, you can refer to [To Kafka Sink](/tidb-cloud/changefeed-sink-to-apache-kafka.md)

2. After you proceed to the "Configure the changefeed target->Connectivity Method->Private Link", you just fill the following fields with corresponding values and others fields as needed
   - Kafka Type: 3 AZs. PS: make sure your Kafka is deployed in same 3 AZs 
   - Kafka Advertised Listener Pattern: abc. PS: same as the unique random string we used to generate "Kafka Advertised Listener Pattern" in "Set up Self-hosted Kafka Private Link Service in AWS" section
   - Endpoint Service Name: <the kafka service name> 
   - Bootstrap Ports: 9092. PS: only one port is fine since we configure a special bootstrap target group behind this port.

3. Continue follow the guideline in [To Kafka Sink](/tidb-cloud/changefeed-sink-to-apache-kafka.md)

4. If everything go fine, you will successfully finish the job.

## FAQ

### How to connect to the same Kafka Private Link service from two different TiDB Cloud projects?

Suppose that you have already followed the above document successfully to set up the connection from the first project. You want to set up the second connection from the second project. Do the following:

1. Go back to the beginning of this document to start from beginning. 
2. When you proceed to [Step 2. Set up Kafka Cluster](#step-2-set-up-kafka-cluster), follow [Reconfigure a Running Kafka Cluster](#reconfigure-a-running-kafka-cluster) to create another group of EXTERNAL listener and advertised listener. You can name it as **EXTERNAL2**. Note that the port range of **EXTERNAL2** cannot overlap with the **EXTERNAL**.
3. After reconfiguring brokers, add another group of target groups in LB, including bootstrap and brokers target groups.
4. Proceed TiDB Cloud connection with the following:
    - New Bootstrap port
    - New Kafka Advertised Listener Group
    - The same Endpoint Service
