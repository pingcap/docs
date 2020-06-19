---
title: Deployment Solution for Three Data Centers in Two Cities
summary: Learn the deployment solution for three data centers in two cities.
category: how-to
---

# Deployment Solution for Three Data Centers in Two Cities

This document introduces the architecture and configuration of the deployment solution for three data centers (DC) in two cities.

## Overview

The model of three DCs in two cities is a highly available and disaster tolerant deployment solution. In this model, the three DCs in two cities are interconnected. If one DC fails or suffers from disaster, other DCs can operate as normal and take over the the key applications or all applications. Compared with the the deployment solution for multi-DC in one city, this solution has the advantage of cross-city high availability and can survive city-level natural disasters.

TiDB, a distributed database, natively supports the three-DC-in-two-city architecture by the virtue of Raft algorithm, and guarantees the consistency and high availability of data within a database cluster. Because the network latency across DCs in the same city is relatively low, the application traffic can be dispatched to two DCs in the same city, and the traffic load can be shared by these two DCs by controlling the distribution of Region leaders and PD leaders.

## Architecture

This document takes the example of Beijing and Xi'an to explain the deployment model of three DCs in two cities for the distributed database of TiDB.

In this example, two DCs (IDC1 and IDC2) are located in Beijing and the other DC (IDC3) is located in Xi'an. The network latency between IDC1 and IDC2 is lower than 3 milliseconds. The network latency between IDC3 and IDC1/IDC2 in Beijing is about 20 milliseconds (ISP dedicated network is used).

The architecture of the cluster deployment is as follows:

- The TiDB cluster is deployed with the three-DC-in-two-city model: IDC1 in Beijing, IDC2 in Beijing, and IDC3 in Xi'an.
- The cluster has five replicas, two in IDC1, two in IDC2, and one in IDC3. In the TiKV component, each rack has a label, which means that each rack has a replica.
- The Raft protocol is adopted to ensure the consistency and high availability of data, which is transparent to users.

![3-DC-in-2-city architecture](/media/three-data-centers-in-two-cities-deployment-01.png)

This architecture is highly available. The distribution of Region leaders is restricted to the two DCs (IDC1 and IDC2) that are in the same city (Beijing). Compared with the three-DC solution in which the distribution of Region leaders is not restricted, this architecture has the following advantages and disadvantages:

- **Advantages**

    - Region leaders are in DCs of the same city with low latency, so the write speed is faster.
    - The two DCs can provide services to the outside at the same time, so the resources usage rate is higher.
    - When one DC fails, services are still available and data safety is ensured.

- **Disadvantages**

    - Because the data consistency is achieved by the Raft algorithm, when two DCs in the same city fail at the same time, there is only one surviving replica in the disaster recovery DC in another city (Xi'an), which does not meet the requirement of Raft algorithm that most replicas survive. As a result, the cluster will be temporarily unavailable. Maintenance staff needs to recover the cluster from the one surviving replica, and some hot data that has not been replicated is lost. Occurrence of such a case is few.
    - Because dedicated network is used, the network infrastructure of this architecture has a high cost.
    - Five replicas are configured in three DCs in two cities, data redundancy increases, which has higher storage cost.

### Deployment details

The configuration of the three DCs in two cities (Beijing and Xi'an) deployment plan is illustrated as follows:

![3-DC-2-city](/media/three-data-centers-in-two-cities-deployment-02.png)

- From the illustration above, you can see that Beijing has two DCs: IDC1 and IDC2. IDC1 has three sets of racks: RAC1, RAC2, and RAC3. IDC2 has two racks: RAC4 and RAC5. The IDC3 DC in Xi'an has the RAC6 rack.
- From the RAC1 rack illustrated above, TiDB and PD services are deployed on the same server. There are another two TiKV servers, each with two TiKV instances (tikv-server) deployed, which is similar to RAC2, RAC4, RAC5 and RAC6.
- The TiDB server, the control machine, and the monitoring server are on RAC3. The TiDB server is deployed for regular maintenance and backup. TiDB Ansible, Prometheus, Grafana, and the restore tool are deployed on the control machine and monitoring machine.
- Another backup server can be added to deploy Mydumper and Drainer. Drainer exports `file` files to save binlog data to a specified location, thus achieving incremental backup.

## Configuration

### Example

See the following `tiup topology.yaml` yaml file for example:

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"

server_configs:
  tikv:
    server.grpc-compression-type: gzip
  pd:
    replication.location-labels:  ["dc","rack","zone","host"]
    schedule.tolerant-size-ratio: 20.0

pd_servers:
  - host: 10.63.10.10
    name: "pd-10"
  - host: 10.63.10.11
    name: "pd-11"
  - host: 10.63.10.12
    name: "pd-12"
  - host: 10.63.10.13
    name: "pd-13"
  - host: 10.63.10.14
    name: "pd-14"

tidb_servers:
  - host: 10.63.10.10
  - host: 10.63.10.11
  - host: 10.63.10.12
  - host: 10.63.10.13
  - host: 10.63.10.14

tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { dc: "1", zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { dc: "1", zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { dc: "2", zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { dc: "2", zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { dc: "3", zone: "5", rack: "5", host: "34" }
      raftstore.raft-min-election-timeout-ticks: 1000
      raftstore.raft-max-election-timeout-ticks: 1200

monitoring_servers:
  - host: 10.63.10.60

grafana_servers:
  - host: 10.63.10.60

alertmanager_servers:
  - host: 10.63.10.60
```

### Labels design

In the deployment model of three DCs in two cities, the design of labels should have thought for availability and disaster recovery. It is recommended that you define the four levels (`dc`, `zone`, `rack`, `host`) based on the physical structure of the deployment.

![Label logical definition](/media/three-data-centers-in-two-cities-deployment-03.png)

Add level information of TiKV labels in the PD configuration:

```yaml
server_configs:
  pd:
    replication.location-labels:  ["dc","zone","rack","host"]
```

The configuration of `tikv_servers` is based on the label information of the real physical deployment location of TiKV, which makes it easier for PD to perform global management and scheduling.

```yaml
tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { dc: "1", zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { dc: "1", zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { dc: "2", zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { dc: "2", zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { dc: "3", zone: "5", rack: "5", host: "34" }
```

### Optimize parameter configuration

In the deployment model of three DCs in two cities, in addition to the regular configuration parameters, adjust the component parameters to optimize performance.

- Enable gRPC message compression in TiKV. Because data of the cluster is transmitted in the network, you can enable the gRPC message compression to lower the network traffic.

    ```yaml
    server.grpc-compression-type: gzip
    ```

- Adjust the PD balance buffer size and increase the tolerance of PD. Because PD calculates the score of each object according to the situation of the node as the basis for scheduling, when the difference between the scores of leaders (or Regions) of two stores is less than the specified multiple of the Region size, PD considers that balance is achieved.

    ```yaml
    schedule.tolerant-size-ratio: 20.0
    ```

- Optimize the network configuration of the TiKV node in another city (Xi'an). Modify the following TiKV parameters for IDC3 (alone) in Xi'an and try to prevent the replica in this TiKV node from participating in the Raft election.

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1200
    ```

- Configure scheduling. After the cluster is enabled, use the `tiup ctl pd` tool to modify the scheduling policy. Modify the number of TiKV Raft replicas. Configure this number as planned. In this example, the number of replicas is five.

    ```yaml
    config set max-replicas 5
    ```

- Forbid scheduling the Raft leader to IDC3. Scheduling the Raft leader to in another city (IDC3) causes unnecessary network overhead between IDC1/IDC2 in Beijing and IDC3 in Xi'an. The network bandwidth and latency also affect performance of the TiDB cluster.

    ```yaml
    config set label-property reject-leader dc 3
    ```

- Configure the priority of PD. To avoid the situation where the PD leader is in another city (IDC3), you can increase the priority of local PD (in Beijing) and decrease the priority of PD in another city (Xi'an). The larger the number, the higher the priority.

    ```yaml
    member leader_priority PD-10 5
    member leader_priority PD-11 5
    member leader_priority PD-12 5
    member leader_priority PD-13 5
    member leader_priority PD-14 1
    ```
