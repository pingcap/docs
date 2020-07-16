---
title: TiDB Scheduling
summary: Introduces the PD scheduling component in a TiDB cluster.
---

# TiDB Scheduling

PD works as the manager in a TiDB cluster, and it also schedules Regions in the
cluster. This article introduces the design and core concepts of the PD scheduling component.

## Use scenarios

TiKV is the distributed K/V storage engine used by TiDB. In TiKV, data is
organized as Regions, which are replicated on serveral stores. In all replicas,
Leader is responsible for reading and writing, Followers are responsible for
replicating Raft logs from the leader.

So there are some situations need to be considered:

* Regions need to be distributed fine in the cluster to utilize storage space
  high-efficient;
* For multiple datacenter topologies, one datacenter failure should only cause
  one replica fail for all Regions;
* When a new TiKV store is added, data can be rebalanced to it;
* When a TiKV store fails, PD needs to consider
    * recovery time of the failure store.
        * If it's short (e.g. the service is restarted), scheduling is necessary
          or not.
        * If it's long (e.g. disk fault, data is lost), how to do scheduling.
    * replicas of all regions.
        * If replicas are not enouth for some regions, needs to complete them.
        * If replicas are more than expected (e.g. failed store re-joins into the
          cluster after recovery), needs to delete them.
* Read/Write operations are performed on leaders, which shouldn't be distributed
  only on invividual stores;
* Not all regions are hot, load of all TiKV stores needs to be balanced.
* When regions are in balancing, data transferring utilizes much network/disk
  traffic and CPU time, which can influence online services.

These situations can occur at the same time, which makes it harder to resolve.
And, the whole system is changing dynamically, so a single point is necessary
to collect all informations about the cluster, and then adjust the cluster. So,
PD is introduced into TiDB cluster.

## Scheduling Requirements

The above situations can be classified into 2 classes:

** The First: must be satisfied to reach high availability, includes **

* Count of replicas can't be more or less;
* Replicas needs to be distributed to different machines;
* The cluster can auto recovery from TiKV peers failure.

** The Second: need to be satisfied as a good distributed system, includes **

* All Region leaders are balanced;
* Storeage size of all TiKV peers are balanced;
* Hot points are balanced;
* Speed of Region balance needs to be limited to ensure online services are stable;
* It's possible to online/offline peers manually.

After the first class requirements are satisfied, the system will be failure tolerable. 
After the second class requirements are satisfied, resources will be utilized more
efficent and the system will become well expandable.

To achieve these targets, PD needs to collect informations firstly, such as state of peers,
informations about Raft groups and statistics of peers' accession. Then we can specify
some strategies on PD, so that PD can make sheculing plans from these information and
strategies. Finally, PD will distribute some operators to TiKVs to complete scheduling plans.

## Basic Schedule operators

All scheduling plan contain 3 basic operators:

* Add a new replica
* Remove a replica
* Transfer a Region leader between replicas

They are implemented by Raft command `AddReplica`, `RemoveReplica` and `TransferLeader`.

## Information collecting

Scheduling is based on information collecting. In one word, scheduling needs to know
states of all TiKV peers and all Regions. TiKV peers report those information to PD.

** Information reported by TiKV peers **

TiKV sends heartbeats to PD periodically. PD can not only check the store is active
nor not, but also collect [`StoreState`](https://github.com/pingcap/kvproto/blob/release-3.1/proto/pdpb.proto#L421)
in the message. `StoreState` includes

* Total disk space
* Available disk space
* Region count
* Data read/write speed
* Send/receive snapshot count
* It's overload or not
* Labels (See [Perception of Topology](/location-awareness.md))

** Information reported by Region leaders **

Region leader send heartbeaets to PD periodically to report [`RegionState`](https://github.com/pingcap/kvproto/blob/release-3.1/proto/pdpb.proto#L271),
includes

* Position of the leader itself
* Positions of other replicas
* Offline replicas count
* data read/write speed

PD collects cluster information by these 2 type heartbeats and then makes dicision based on it.

Beside these, PD can get more information from expanded interface. For example,
if a store's heartbeats are broken, PD can't know the peer steps down temporarily or forever.
It just waits a while (by default 30min) and then treats the store become offline if there
are still no heartbeats received. Then PD balances all regions on the store to other stores.

But sometimes stores are set offline by maintainers manually, so that we can tell PD this by
PD control interface. Then PD can balance all regions immediately.

## Scheduling stretagies

PD needs some stretagies to make scheduling plans.

** Replicas count of Regions need to be correct **

PD can know replica count of a Region is incorrect from Region leader's heartbeat. If it happens,
PD can adjust replica count by add/rmeove replica operation. The reason of incorrect replica counts
could be:

* Store failure, so some Region's replica count will be less than expected;
* Store recovery after failure, so some Region's replica count could be more than expected;
* [`max-replicas`](https://github.com/pingcap/pd/blob/v4.0.0-beta/conf/config.toml#L95) is changed.

** Replicas of a Region need to be at different positions **

Please note that 'position' is different from 'machine'. Generally PD can only ensure that
replicas of a Region won't be at a same peer to avoid the peer's failure cause more than one
replicas become lost. However in production, these requirements are possible:

* Multiple TiKV peers are on one machine;
* TiKVs are on multiple racks, and the system is expected to be available even if a rack fails;
* TiKVs are in multiple datacenters, and the system is expected to be available even if a datacenter fails;

The key of there requirements is that peers can have same 'position', which is the smallest unit
for failure-toleration. Replicas of a Region shouldn't be in one unit. So, we can configure
[labels](https://github.com/tikv/tikv/blob/v4.0.0-beta/etc/config-template.toml#L140) for TiKVs,
and set [location-labels](https://github.com/pingcap/pd/blob/v4.0.0-beta/conf/config.toml#L100) on PD
to specify which labels are used for marking positions.

** Replicas should be balanced between stores **

Size limit of a Region is fixed, so make Region count be balanced between store is helpful for data size balance.

** Leaders should be balanced between stores **

Read and write operations are performed on leaders in Raft. So PD needs to distributed leader into whole cluster
instead of serveral peers.

** Hot points should be balanced between stores **

PD can detect hot points from store heartbets and Region heartbeats. So PD can disturb hot points.

** Storage size needs to be balanced between stores **

TiKV reports `capacity` of storage when it starts up, which indicates the store's space limit. PD will consider this
when doing schedule.

** Adjust scheduling speed to stabilize online services **

Scheduling utilizes CPU, memory, network and I/O traffic. Too much resource utilization will influence
online services. So PD needs to limit concurrent scheduling count. By default the strategy is conservative,
while it can be changed if quicker scheduling is required.

## Scheduling implementation

PD collects cluster information from store heartbeats and Region heartbeats, and then makes scheduling plan
from the information and stretagies. Scheduling plans are constructed by a sequence of basic operators.
Every time when PD receives a region heartbeat from a Region leader, it checks whether there is a pending
operator on the Region or not. If PD needs to dispatch a new operator to a Region, it puts the operator into
heartbeat responses, and monitors the operator by checking follow-up Region heartbeats.

Note that operators are only suggestions, which could be skipeed by Regions. Leader of Regions can decide
whether to step a scheduling operator or not based on its current status.
