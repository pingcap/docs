---
title: The Prerequisites of TiDB in Kubernetes
summary: Learn the prerequisites of TiDB in Kubernetes
category: how-to
---

# The Prerequisites of TiDB in Kubernetes

This document introduces the hardware and software prerequisites for deploying a TiDB cluster in Kubernetes.

## Software version

| Software Name | Version |
| :--- | :--- |
| Docker | Docker CE 18.09.6 |
| Kubernetes |  v1.12.5+ |
| CentOS |  7.6 and kernel 3.10.0-957 or later |

## The configuration of kernel parameter

| Configuration Item | Value |
| :--- | :--- |
| net.core.somaxconn | 32768 |
| vm.swappiness | 0 |
| net.ipv4.tcp_syncookies | 1 |
| net.ipv4.ip_forward | 1 |
| fs.file-max | 1000000 |
| fs.inotify.max_user_watches | 1048576 |
| fs.inotify.max_user_instances | 1024 |
| net.ipv4.neigh.default.gc_thresh1 | 80000 |
| net.ipv4.neigh.default.gc_thresh2 | 90000 |
| net.ipv4.neigh.default.gc_thresh3 | 100000 |
| net.bridge.bridge-nf-call-iptables | 1 |
| net.bridge.bridge-nf-call-arptables | 1 |
| net.bridge.bridge-nf-call-ip6tables | 1 |

If no error is found in the report option when you are setting the `net.bridge.bridge-nf-call-*` parameters, check whether this module has been loaded by running the following command:

{{< copyable "shell-regular" >}}

```shell
lsmod|grep br_netfilter
```

If this module is not loaded, run the following command to load the module:

{{< copyable "shell-regular" >}}

```shell
modprobe br_netfilter
```

You also need to disable the swap of each deployed Kubernetes node and run the following command:

{{< copyable "shell-regular" >}}

```shell
swapoff -a
```

Run the following command to check if the swaps are disabled:

{{< copyable "shell-regular" >}}

```shell
## If the swap column is all `0` in the result of the above command, this indicates that swaps are disabled.
free -m
```

In addition, to permanently disable swaps, remove all the swap-related entries in `/etc/fstab`.

## Kubernetes requirements for hardware and deployment

+ A 64-bit general hardware server with Intel x86-64 architecture and a 10 Gigabit NIC, which is the same as the server requirements for deploying a TiDB binary cluster. For more detail, check [here](/dev/how-to/deploy/hardware-recommendations.md).

+ The server's disk, memory and CPU depends on the capacity planning of the cluster and the deployment topology.

  > **Note:**
  >
  > It is recommended to deploy three master nodes, three etcd nodes, and several worker nodes to ensure high availability of the online deployment in Kubernetes. At the same time, the master node often acts as a worker node (that is, load can also be scheduled to the master node) to make full use of machine resources. The [reserved resources](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/) is set by kubelet to ensures that the system processes on the machine and the core processes of Kubernetes still have sufficient resources to operate under high workload, thus ensuring the stability of the entire system.

The following introduction is based on the plan of three Kubernetes masters, three etcd and several worker nodes. To deploy multi-master and highly available nodes in Kubernetes, check the [Kubernetes official documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/).

## Kubernetes requirements for system resources

- Each machine requires a relatively large SAS disk (at least 1T) to store the data directories of Docker and kubelet.

  > **Note:**
  >
  > The data from Docker mainly includes image and container logs. The data from kubelet are mainly data used in [emptyDir](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir).

- To deploy a monitoring system for the Kubernetes cluster whose data is to be stored on disk, prepare a large SAS disk for Prometheus and the log monitoring system. It is recommended to prepare two large SAS machines for each machine.

  > **Note:**
  >
  > In a production environment, it is recommended to use RAID 5 for these disks for the above two usages.

- It is recommended that the number of etcd be consistent with the Kubernetes master nodes. The etcd data is recommended to be stored on the SSD disk.

## TiDB cluster's requirements for resources

The TiDB cluster consists of three components: PD, TiKV and TiDB. The following recommendations on capacity planning is based on the standard TiDB cluster, namely three PDs, three TiKVs and two TiDBs:

- PD component: 2C 4GB. PD occupies relatively less resources and only a small portion of local disks are used.

  > **Note:**
  >
  > For easier management, you can put the PDs of all clusters on the master node. For example, to support 5 TiDB clusters, you can plan to deploy 5 PD instances on each of the 3 master nodes. These PD instances use the same SSD disk (disk of 200 or 300 GigaBytes) on which you can create 5 directories as a mount points by means of bind mount. For detailed operation, check [documentation](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs) for reference.
  >
  > If more machines are added to support more TiDB clusters, you can continue to add PD instances in this way on the master. If the resources on the master are exhausted, you can find other worker nodes to add PDs in the same way. This method is convenient for the planning and management of PD instances. However, if two machines go down, all TiDB clusters will be unavailable due to the concentration of PD instances.
  >
  > Therefore, it is recommended to take out an SSD disk from each machines in the cluster to provide PD instances like the master node. If you need to enlarge capacity by adding machines in some clusters, you only need to create PD instances on the newly added machines.

- TiKV components: An NVMe disk of 8C 32GB for each TiKV instance. To deploy multiple TiKV instances on one machine, you must reserve enough buffers when planning capacity.

- TiDB component: 8C 32 GB. Because TiDB component does not occupy the disk, you only need to consider the CPU and memory resources for it in your plan. The following example assumes that the capacity is 8C 32 GB.

## A case of planning TiDB clusters

This is an example of deploying 5 clusters (3 PDs + 3 TiKVs + 2 TiDBs), where PD is configured as 2C 4GB, TiDB as 8C 32GB, and TiKV as 8C 32GB. There are seven Kubernetes nodes, three of which are both master and worker nodes, and the other three are purely worker nodes. The distribution of each component is as follows:

+ single master node:

    - 1 etcd (2C 4GB) + 2 PD (2 \* 2C 2 \* 4GB) + 3 TiKV (3 \* 8C 3 \* 32GB) + 1 TiDB (8C 32GB), totalling 38C 140GB
    - Two SSD disks, one for etcd and one for two PD instances
    - The RAID5-applied SAS disk used for Docker and kubelet
    - Three NVMe disks for TiKV instances

+ single worker node:

    - 3 PD (3 \* 2C 3 \* 4GB) + 2 TiKV (2 \* 8C 2 \* 32GB) + 2 TiDB (2 \* 8C 2 \* 32GB), totalling 38C 140GB
    - One SSD disk for three PD instances
    - The RAID5-applied SAS disk used for Docker and kubelet
    - Two NVMe disks for TiKV instances

From the above analysis, a total of seven physical machines are required to support five sets of TiDB cluster. Three of the machines are master and worker nodes, and the remaining four are worker nodes. The requirements of machine configuration are as follows:

- master and worker node: 48C 192GB, 2 block SSD disks, one RAID5-applied SAS disk, three NVMe disks
- worker node: 48C 192GB, one block SSD disk, one RAID5-applied SAS disk, two NVMe disks

The recommended configuration above leaves plenty of available resources in addition to those taken by the components. To add monitoring and log components, use the same method to plan the type of machine you need to purchase and its configuration. Moreover, in a production environment, avoid deploying TiDB instances on the master node as much as possible due to the NIC bandwidth. If the NIC of the master nodes works at full capacity, the heartbeat report between the worker node and the master node will be affected and might leads to more serious problems.
