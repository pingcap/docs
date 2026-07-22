# Tiered Storage FAQ

> **Version**: Private Preview
> **Platform**: TiDB Cloud Essential
> **Document Nature**: **This document reflects the current system state only. Some behaviors may change when the feature reaches GA.**
> **Updated**: 2026-07-22

---

**Q1: Can IA tables execute UPDATE / DELETE?**

A: Yes. An UPDATE operation first loads the corresponding data from S3 into the IA cache, performs the modification, and writes a new SST file — the same flow as a regular UPDATE. Performance is affected by cold reads.

---

**Q2: Can TiFlash replicas of IA tables be set to IA?**

A: No. TiFlash does not follow the IA attribute of the source table.

---

**Q3: What happens to IA tables when the object store (S3) experiences an outage?**

A: IA tables will be affected and become unavailable — since all data resides remotely, read requests must fetch from S3. Additionally, if S3 bandwidth is saturated, IA read/write performance will also be impacted.

---

**Q4: Can the system tell me which data is cold before I set IA?**

A: TiDB does not provide built-in cold/hot detection tools. Users need to assess data access patterns based on their own business knowledge. A general rule of thumb: for time-partitioned tables, older partitions tend to have lower access frequency.

---

**Q5: When data is stored in cold storage (IA tier), are all three replicas stored, or just one copy?**

A: All three replicas are stored in cold storage, not just one.

TiKV's Raft three-replica mechanism is identical between the IA and Standard layers — what changes is the data storage location and format:

- **Standard layer**: Three replicas are each stored on the local disks of three TiKV nodes
- **IA layer**: Three replicas are each uploaded to object storage independently in IA format

Each replica on each TiKV node runs its own independent LSM-Tree, performing independent flush and compaction operations. When a table switches to IA storage class, all subsequently generated SST files are written to S3 in IA type. The three replicas produce their own independent SST files — three separate objects in S3, not shared.

IA is a **storage format/location optimization**, not a **replica reduction mechanism**. It changes "how each node stores its own copy," not "how many copies exist." The Raft write and replication flow is identical to the Standard layer.

**Cost impact**: Since all three replicas upload independently, the total storage on S3 remains approximately 3× the data volume. However, the unit storage cost of STANDARD_IA is lower, so the overall storage expense is reduced.

---
