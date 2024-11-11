---
title: Setup Self Hosted Kafka Private Service Connect in Google Cloud
summary: This document explains how to set up private service connect for self-hosted Kafka in Google Cloud and how to make it work with TiDB Cloud.
---

# Set up Self-hosted Kafka Private Service Connect in Google Cloud

This document explains how to set up private service connect for self-hosted Kafka in Google Cloud and how to make it work with TiDB Cloud.

The main idea is the same as we do in AWS:
1. TiDB Cloud VPC connects to Kafka VPC through limit private endpoints.
2. Kafka clients need to talk directly to all Kafka brokers.
3. Therefore, we need to map every Kafka brokers to different ports to make every broker is unique in TiDB Cloud VPC.
4. We will leverage Kafka bootstrap mechanism and Google Cloud resources to achieve the mapping.

There are two ways to set up private service connect for self-hosted Kafka in Google Cloud:
1. Using PSC port mapping mechanism, which requires static port-broker mapping configuration. Require to reconfigure existing Kafka cluster to add a group of EXTERNAL listener and advertised listener. 
2. Using [Kafka-proxy](https://github.com/grepplabs/kafka-proxy), which introduces a extra running process as proxy between Kafka clients and Kafka brokers, the proxy will dynamic configure port-broker mapping and forward requests. No need to reconfigure existing Kafka cluster.

Let's show how to connect to a three AZ Kafka private service connect in Google Cloud by example. It's not the only way to set up private service connect for self-hosted Kafka. There may be other ways base on the similar port mapping mechanism. This document only used to show fundamental of Kafka private service connect. If you want to set up Kafka private service connect in production, you may need to build a more resilient Kafka private service connect with better operational maintainability and observability.


## Prerequisites
1. Make sure you have authorization to set up Kafka private service connect in your own Google Cloud account. 
    - Manage VM Nodes
    - Manage VPC
    - Manage Subnet
    - Manage Load Balancer
    - Manage Private Service Connect
    - Connect to VM Nodes to configure Kafka nodes
2. Make sure that you create a TiDB Cloud Dedicated cluster in Google Cloud first. Align Kafka deployment info with TiDB Cluster.
   1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Changefeed** in the left navigation pane.
   2. In the overview page, you can find the region of TiDB Cluster, make sure your Kafka cluster will be deployed to the same region.
   3. Click **Create Changefeed**
      1. Select **Kafka** as **Target Type**.
      2. Select **Private Service Connect** as **Connectivity Method**
   4. Take note the Google Cloud project in **Reminders before proceeding** information, which your can use it to authorize auto-accept endpoint creation request from TiDB Cloud.
   5. Take note of the **Suggested Kafka Zones**. Here are the Zones where the TiDB Cluster is deployed. It is recommended that Kafka to be deployed in these Zones as well to reduce cross-zone traffic.
   6. Pick a unique **Kafka Advertised Listener Pattern** for your Kafka private service connect
      1. Input a unique random string can only include numbers or lowercase letters, which will be used to generate **Kafka Advertised Listener Pattern** later.
      2. Click **Check usage and generate** button to check if the random string is unique and generate **Kafka Advertised Listener Pattern** which will be used to assemble EXTERNAL advertised listener for kafka brokers, or configure Kafka-proxy. 

Please take note of all this deployment information, use them to configure your Kafka private service connect.
Example of deployment information.

| Information                        | Value                                                                                                                        |
|------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Region                             | Oregon (us-west1)                                                                                                            |
| Google Cloud project of TiDB Cloud | tidbcloud-prod-000                                                                                                           |
| Zones                              | 1. us-west1-a <br/> 2. us-west1-b <br/> 3. us-west1-c                                                                        |
| Kafka Advertised Listener Pattern  | The unique random string: abc <br/> Generated pattern: &lt;broker_id&gt;.abc.us-west1.gcp.3199745.tidbcloud.com:&lt;port&gt; |



## Set up Self-hosted Kafka Private Service Connect by PSC Port Mapping

We will expose every kafka broker to TiDB Cloud VPC with unique port by using PSC port mapping mechanism. It will work as following graph.

![main idea](/media/tidb-cloud/changefeed/connect-to-google-cloud-self-hosted-kafka-private-service-connect-by-portmapping.png)

### First, Set up Kafka Cluster

Jump to "Reconfigure a Running Kafka Cluster" section if you want to expose existing cluster; Refer to "Deploy a New Kafka Cluster" if you set up a new cluster.

#### Deploy a New Kafka Cluster
##### 1. Set up Kafka VPC

We need to create 2 subnets for Kafka VPC, one for Kafka brokers, one for bastion node to make it easy to configure Kafka cluster.

Go to Google Cloud console, navigate to the page [VPC networks](https://console.cloud.google.com/networking/networks/list) to create Kafka VPC with following attributes:
- Name: kafka-vpc
- Subnets
  - Name: bastion-subnet; Region: us-west1; IPv4 range: 10.0.0.0/18
  - Name: brokers-subnet; Region: us-west1; IPv4 range: 10.64.0.0/18
- Firewall rules
  - kafka-vpc-allow-custom
  - kafka-vpc-allow-ssh

##### 2. Provisioning VMs
Go to [VM instances](https://console.cloud.google.com/compute/instances) page to provision VMs
1. Bastion node
   - Name: bastion-node
   - Region: us-west1
   - Zone: Any
   - Machine Type: e2-medium
   - Image: Debian GNU/Linux 12
   - Network: kafka-vpc
   - Subnetwork: bastion-subnet
   - External IPv4 address: Ephemeral
2. Broker node 1
   - Name: broker-node1
   - Region: us-west1
   - Zone: us-west1-a
   - Machine Type: e2-medium
   - Image: Debian GNU/Linux 12
   - Network: kafka-vpc
   - Subnetwork: brokers-subnet
   - External IPv4 address: None
3. Broker node 2
   - Name: broker-node2
   - Region: us-west1
   - Zone: us-west1-b
   - Machine Type: e2-medium
   - Image: Debian GNU/Linux 12
   - Network: kafka-vpc
   - Subnetwork: brokers-subnet
   - External IPv4 address: None
4. Broker node 3
   - Name: broker-node3
   - Region: us-west1
   - Zone: us-west1-c
   - Machine Type: e2-medium
   - Image: Debian GNU/Linux 12
   - Network: kafka-vpc
   - Subnetwork: brokers-subnet
   - External IPv4 address: None

##### 3. Prepare kafka runtime binaries

1. Go to detail page of bastion node, click "SSH" to login to bastion node, download binaries
```shell
# Download kafka & openjdk, decompress. PS: your can choose the binary version as you like
wget https://downloads.apache.org/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```
2. Copy binaries to every broker nodes
```shell
# Run this command to authorize gcloud to access the Cloud Platform with Google user credentials
# Please following the instruction in output to finish the login
gcloud auth login

# Copy binaries to broker nodes
gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node1:~ --zone=us-west1-a
gcloud compute ssh broker-node1 --zone=us-west1-a --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node2:~ --zone=us-west1-b
gcloud compute ssh broker-node2 --zone=us-west1-b --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
gcloud compute scp kafka_2.13-3.7.1.tgz openjdk-22.0.2_linux-x64_bin.tar.gz broker-node3:~ --zone=us-west1-c
gcloud compute ssh broker-node3 --zone=us-west1-c --command="tar -zxf kafka_2.13-3.7.1.tgz && tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
```

##### 4. Configure Kafka Brokers

1. We will set up a KRaft Kafka cluster with 3 nodes, each node will act as broker and controller roles. For every broker:
   1. For "listeners" item, all 3 brokers are the same and act as broker and controller roles:
      1. Configure the same CONTROLLER listener for all **controller** role node. if you want to add **broker** role only nodes, you don't need CONTROLLER listener in ```server.properties```.
      2. Configure two **broker** listeners. INTERNAL for internal access; EXTERNAL for external access from TiDB Cloud.
   2. For "advertised.listeners" item
      1. Configure a INTERNAL advertised listener for every broker with internal ip of broker node, advertise internal Kafka clients use this address to visit the broker.
      2. Configure a EXTERNAL advertised listener based on **Kafka Advertised Listener Pattern** we get from TiDB Cloud for every broker node to help TiDB Cloud differentiate between different brokers. Different EXTERNAL advertised listener helps Kafka client from TiDB Cloud side route request the right broker.
         - ```<port>``` differentiate brokers from Kafka Private Service Connect access point, so please plan a ports range for EXTERNAL advertised listener of all brokers. These ports don't have to be actual ports listened on brokers, they are ports listened on LB for Private Service Connect which will forward request to different brokers.
         - Better to configure different ```<broker_id>``` for different broker, make it easy for troubleshooting.
   3. The planing values
      - CONTROLLER port: 29092
      - INTERNAL port: 9092
      - EXTERNAL: 39092
      - EXTERNAL advertised listener ports range: 9093~9095
2. ssh login to every broker node, create configuration file "~/config/server.properties" with content as following.
```properties
# broker-node1 ~/config/server.properties
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} to real ips
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 2.1 The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"
# 2.2 So the EXTERNAL can be "b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9093) in EXTERNAL advertised listener ports range
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
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} to real ips
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 2.1 The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"
# 2.2 So the EXTERNAL can be "b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9094) in EXTERNAL advertised listener ports range
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
# 1. Replace {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} to real ips
# 2. Configure EXTERNAL in "advertised.listeners" based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 2.1 The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"
# 2.2 So the EXTERNAL can be "b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port(9095) in EXTERNAL advertised listener ports range
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

##### 5. Test Kafka Cluster in Bastion

1. Test Kafka bootstrap
```shell
export JAVA_HOME=~/jdk-22.0.2

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
b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
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

#### Reconfigure a Running Kafka Cluster
Make sure you kafka cluster is deployed in same region as the TiDB cluster. Suggest the zones are also the same to reduce cross-zone traffic.

##### 1. Configure EXTERNAL listener for brokers
The follwoing configuration is for Kafka KRaft cluster, ZK mode is similar.
1. Planning configuration changes
   1. Configure a EXTERNAL **listener** for every broker for external access from TiDB Cloud. Pick a unique port as EXTERNAL port, for example ```39092```.
   2. Configure a EXTERNAL **advertised listener** based on **Kafka Advertised Listener Pattern** we get from TiDB Cloud for every broker node to help TiDB Cloud differentiate between different brokers. Different EXTERNAL advertised listener helps Kafka client from TiDB Cloud side route request the right broker.
      - ```<port>``` differentiate brokers from Kafka Private Service Connect access point, so please plan a ports range for EXTERNAL advertised listener of all brokers. These ports don't have to be actual ports listened on brokers, they are ports listened on LB for Private Service Connect which will forward request to different brokers. Please plan a ports range for EXTERNAL advertised listener, for example ```range from 9093```
      - Better to configure different ```<broker_id>``` for different broker, make it easy for troubleshooting.
2. ssh login to every broker node, modify the configuration file of every broker, with content as following.
```properties
# Add EXTERNAL listener
listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

# Add EXTERNAL advertised listeners based on the "Kafka Advertised Listener Pattern" in "Prerequisites" section
# 1. The pattern is "<broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>"
# 2. So the EXTERNAL can be "bx.abc.us-west1.gcp.3199745.tidbcloud.com:xxxx", replace <broker_id> with "b" prefix plus "node.id" properties, replace <port> with a unique port in EXTERNAL advertised listener ports range 
# For example
advertised.listeners=...,EXTERNAL://b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093

# Configure EXTERNAL map
listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
```
3. After all the broker reconfigured, restart you Kafka brokers one by one.

##### 2. Test EXTERNAL listener setup in your internal network

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
export JAVA_HOME=~/jdk-22.0.2

# Bootstrap from EXTERNAL listener
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# Expected output(last 3 lines), order may be different.
# There will be some exceptions or errors since advertised listeners can not be resolved in your Kafka network. 
# We will make them resolvable in TiDB Cloud side and make it route to the right broker. 
b1.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

### Second, Expose Kafka Cluster as Private Service Connect
1. Go to [Network endpoint group](https://console.cloud.google.com/compute/networkendpointgroups/list) page, create a network endpoint group
   - Name: kafka-neg
   - Network endpoint group type: Port Mapping NEG(Regional)
     - Region: us-west1
     - Network: kafka-vpc
     - Subnet: brokers-subnet
2. After the creation done, go to detail page of the network endpoint group to add network endpoints to configure port mapping to broker nodes
   1. Network endpoint 1
      - Instance: broker-node1
      - VM Port: 39092
      - Client Port: 9093
   2. Network endpoint 2
      - Instance: broker-node2
      - VM Port: 39092
      - Client Port: 9094
   3. Network endpoint 3
      - Instance: broker-node3
      - VM Port: 39092
      - Client Port: 9095
3. Go to [Load balancing](https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers) page, create a LB
   - Type of load balancer: Network Load Balancer
   - Proxy or Passthrough: Passthrough
   - Public facing or internal: Internal
   - Load Balancer name: kafka-lb
   - Region: us-west1
   - Network: kafka-vpc
   - Backend configuration
     - Backend type: Port mapping network endpoint group
     - Protocol: TCP
     - Port mapping network endpoint group: kafka-neg
   - Frontend configuration
     - Subnetwork: brokers-subnet
     - Ports: All
4. Go to [Private Service Connect -> PUBLISH SERVICE](https://console.cloud.google.com/net-services/psc/list/producers)
   - Load Balancer Type: Internal passthrough Network Load Balancer
   - Internal load balancer: kafka-lb
   - Service name: kafka-psc
   - Subnets: RESERVE NEW SUBNET
     - Name: psc-subnet
     - VPC Network: kafka-vpc
     - Region: us-west1
     - IPv4 range: 10.128.0.0/18
   - Accepted projects: Google Cloud project of TiDB Cloud you got in "Prerequisites" section, for example ```tidbcloud-prod-000```
5. After creation done, navigate to the detail page of the "kafka-psc", take node the "Service attachment", for example ```projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-psc```, which will be used in TiDB Cloud to connect to this PSC.
6. Go to detail page of the VPC network "kafka-vpc", add a firewall rule to allow psc traffic to all brokers.
   - Name: allow-psc-traffic
   - Direction of traffic: Ingress
   - Action on match: Allow
   - Targets: All instances in the network
   - Source filter: IPv4 ranges
   - Source IPv4 ranges: 10.128.0.0/18. PS: the range of psc-subnet
   - Protocols and ports: Allow all

### Third, Connect from TiDB Cloud

1. Go back to TiDB Cloud console to create changefeed for the cluster to connect to Kafka cluster by **Private Service Connect**. For the detail, you can refer to [To Kafka Sink](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
2. After you proceed to the "Configure the changefeed target->Connectivity Method->Private Service Connect", you just fill the following fields with corresponding values and others fields as needed
   - Kafka Advertised Listener Pattern: abc. PS: same as the unique random string we used to generate "Kafka Advertised Listener Pattern" in "Prerequisites" section
   - Service Attachment: <the kafka service attachment of PSC>, for example ```projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-psc```
   - Bootstrap Ports: 9092,9093,9094
3. Continue follow the guideline in [To Kafka Sink](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
4. If everything go fine, you will successfully finish the job.

## Set up Self-hosted Kafka Private Service Connect by Kafka-proxy

We will expose every kafka broker to TiDB Cloud VPC with unique port by using Kafka-proxy dynamic port mapping mechanism. It will work as following graph.

![main idea](/media/tidb-cloud/changefeed/connect-to-google-cloud-self-hosted-kafka-private-service-connect-by-kafka-proxy.png)

### First, Set up Kafka-proxy
Let's say you already have a Kafka cluster running in the same region as the TiDB Cluster. You can connect to Kafka cluster from you VPC network. The Kafka cluster may be hosted by yourself or provided by others providers, for example Confluent.
1. Go to [Instance groups](https://console.cloud.google.com/compute/instanceGroups/list), create an instance group for Kafka-proxy
   - Name: kafka-proxy-ig
   - Instance template:
     - Name: kafka-proxy-tpl
     - Location: Regional
     - Region: us-west1
     - Machine type: e2-medium. PS: you can choose your own based on you workload.
     - Network: your VPC network which can connect to Kafka cluster
     - Subnetwork: your subnet which can connect to Kafka cluster
     - External IPv4 address: Ephemeral. PS: enable Internet access to make it easy configure Kafka-proxy, you can select "None" in your production environment and login to the node in your way.
   - Location: Single zone
   - Region: us-west1
   - Zone: choose your one of brokers' zones 
   - Autoscaling mode: Off
   - Minimum number of instances: 1
   - Maximum number of instances: 1 PS: Kafka-proxy doesn't have cluster mode, you should only deploy one Kafka-proxy. Let me explain why. Each Kafka-proxy randomly map local ports to brokers' ports, so different Kafka-proxy have different mapping. Multiple Kafka-proxies behind a Load Balancer may cause chaos, if Kafka client bootstrap from one Kafka-proxy, then visit a broker through another Kafka-proxy, the request may go to the wrong broker.
2. Go to detail page of node in kafka-proxy-ig, click "SSH" to login to the node, download binaries
```shell
# You can choose another version 
wget https://github.com/grepplabs/kafka-proxy/releases/download/v0.3.11/kafka-proxy-v0.3.11-linux-amd64.tar.gz
tar -zxf kafka-proxy-v0.3.11-linux-amd64.tar.gz
```
3. Run Kafka-proxy and connect to Kafka brokers
```shell
# There 3 kinds of parameters need to feed to the Kafka-proxy
# 1. --bootstrap-server-mapping defines the bootstrap mapping, suggest configure 3 mappings, one per zone for resilience.
#   a) Kafka broker address; 
#   b) Local address for the broker in Kafka-proxy; 
#   c) Advertised listener for the broker if Kafka clients bootstrap from Kafka-proxy
# 2. --dynamic-sequential-min-port defines the start port of the random mapping for others brokers
# 3. --dynamic-advertised-listener defines advertised listener address for others brokers based on the pattern got from "Prerequisites" section
#   a) The pattern: <broker_id>.abc.us-west1.gcp.3199745.tidbcloud.com:<port>
#   b) Replace <broker_id> to fixed lower case string, for example "brokers", your can use your own string, but it's MUST. This will help TiDB Cloud route requests properly.
#   c) Remove ":<port>"
#   d) The advertised listener address would be: brokers.abc.us-west1.gcp.3199745.tidbcloud.com
./kafka-proxy server \
        --bootstrap-server-mapping "{address_of_broker1},0.0.0.0:9092,b1.abc.us-west1.gcp.3199745.tidbcloud.com:9092" \
        --bootstrap-server-mapping "{address_of_broker2},0.0.0.0:9093,b2.abc.us-west1.gcp.3199745.tidbcloud.com:9093" \
        --bootstrap-server-mapping "{address_of_broker3},0.0.0.0:9094,b3.abc.us-west1.gcp.3199745.tidbcloud.com:9094" \
        --dynamic-sequential-min-port=9095 \
        --dynamic-advertised-listener=brokers.abc.us-west1.gcp.3199745.tidbcloud.com > ./kafka_proxy.log 2>&1 &
```
4. Test bootstrap in Kafka-proxy node
```shell
# Download kafka & openjdk, decompress. PS: your can choose the binary version as you like
wget https://downloads.apache.org/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz

export JAVA_HOME=~/jdk-22.0.2

./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server 0.0.0.0:9092
# Expected output(lines in tail), order may be different.
# There are exceptions or errors since advertised listeners can not be resolved in your network.
# We will make them resolvable in TiDB Cloud side and make it route to the right broker. 
b1.abc.us-west1.gcp.3199745.tidbcloud.com:9092 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.abc.us-west1.gcp.3199745.tidbcloud.com:9093 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.abc.us-west1.gcp.3199745.tidbcloud.com:9094 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
brokers.abc.us-west1.gcp.3199745.tidbcloud.com:9095 (id: 4 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
brokers.abc.us-west1.gcp.3199745.tidbcloud.com:9096 (id: 5 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
...
```

### Second, Expose Kafka-proxy as Private Service Connect

1. Go to [Load balancing](https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers) page, create a LB
   - Type of load balancer: Network Load Balancer
   - Proxy or Passthrough: Passthrough
   - Public facing or internal: Internal
   - Load Balancer name: kafka-proxy-lb
   - Region: us-west1
   - Network: your network
   - Backend configuration
      - Backend type: Instance group
      - Protocol: TCP
      - Instance group: kafka-proxy-ig
   - Frontend configuration
      - Subnetwork: your subnet
      - Ports: All
      - Heath check:
        - Name: kafka-proxy-hc
        - Scope: Regional
        - Protocol: TCP
        - Port: 9092. PS: you can choose one of the bootstrap port in Kafka-proxy.
2. Go to [Private Service Connect -> PUBLISH SERVICE](https://console.cloud.google.com/net-services/psc/list/producers)
   - Load Balancer Type: Internal passthrough Network Load Balancer
   - Internal load balancer: kafka-proxy-lb
   - Service name: kafka-proxy-psc
   - Subnets: RESERVE NEW SUBNET
      - Name: proxy-psc-subnet
      - VPC Network: your network
      - Region: us-west1
      - IPv4 range: set the CIDR based on your network planing
   - Accepted projects: Google Cloud project of TiDB Cloud you got in "Prerequisites" section, for example ```tidbcloud-prod-000```
3. After creation done, navigate to the detail page of the "kafka-proxy-psc", take node the "Service attachment", for example ```projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-proxy-psc```, which will be used in TiDB Cloud to connect to this PSC.
4. Go to detail page of your VPC network, add a firewall rule to allow psc traffic to all brokers.
   - Name: allow-proxy-psc-traffic
   - Direction of traffic: Ingress
   - Action on match: Allow
   - Targets: All instances in the network
   - Source filter: IPv4 ranges
   - Source IPv4 ranges: the CIDR of proxy-psc-subnet
   - Protocols and ports: Allow all

### Third, Connect from TiDB Cloud

1. Go back to TiDB Cloud console to create changefeed for the cluster to connect to Kafka cluster by **Private Service Connect**. For the detail, you can refer to [To Kafka Sink](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
2. After you proceed to the "Configure the changefeed target->Connectivity Method->Private Service Connect", you just fill the following fields with corresponding values and others fields as needed
   - Kafka Advertised Listener Pattern: abc. PS: same as the unique random string we used to generate "Kafka Advertised Listener Pattern" in "Prerequisites" section
   - Service Attachment: <the kafka-proxy service attachment of PSC>, for example ```projects/tidbcloud-dp-stg-000/regions/us-west1/serviceAttachments/kafka-proxy-psc```
   - Bootstrap Ports: 9092,9093,9094
3. Continue follow the guideline in [To Kafka Sink](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
4. If everything go fine, you will successfully finish the job.

## FAQ

### How to connect to the same Kafka Private Service Connect from two different TiDB Cloud projects?
1. Let's say you have already following the above document successfully set up the connection from the first project.
2. You want to set up the second connection from the second project.
3. If you set up Kafka PSC by PSC Port Mapping
   1. Go back to the head of this document proceed from beginning. When you proceed to the "First, Set up Kafka Cluster" section. Follow the "Reconfigure a Running Kafka Cluster" section, create another group of EXTERNAL listener and advertised listener, you can name it as EXTERNAL2. Please notice that the port range of EXTERNAL2 can not overlap with the EXTERNAL.
   2. After brokers reconfigured, you add another group of Network endpoints to Network endpoint group, which mapping the ports range to the EXTERNAL2 listener.
   3. Proceed TiDB Cloud connection with inputs as following to create the new changefeed
      - New Bootstrap ports
      - New Kafka Advertised Listener Group
      - The same Service Attachment
4. If you set up Kafka PSC by Kafka-proxy, you just create a new Kafka-proxy PSC from beginning with New Kafka Advertised Listener Group.
