---
title: TiDB Roadmap
summary: Learn about what's coming in the future for TiDB.
---

# TiDB Roadmap

This roadmap provides a look into the proposed future. This will be continually updated as we release long-term stable (LTS) versions. The purpose is to provide visibility into what is coming, so that you can more closely follow the progress, learn about the key milestones on the way, and give feedback as the development work goes on.

In the course of development, this roadmap is subject to change based on user needs and feedback. **DO NOT** schedule your release plans according to the content of the roadmap. If you have a feature request or want to prioritize a feature, please file an issue on [GitHub](https://github.com/pingcap/tidb/issues).

> **Note:**
> If not marked as GA, these features are experimental.

## Rolling roadmap highlights

<table><thead>
  <tr>
    <th>Category</th>
    <th>End of CY24 release</th>
    <th>Mid of CY25 release</th>
    <th>Future releases</th>
  </tr></thead>
<tbody>
  <tr>
    <td>Unmatched Scalability and Peak Performance<br>Deliver massive scalability and faster performance to support larger workloads, optimize resource utilization, and ensure superior responsiveness<br></td>
    <td>In-memory caching in TiKV<br>TiKV maintains recent versions of data in memory to reduce redundant MVCC scans, thus improving performance.<br>Adaptive Parallelism for Stats Collection (GA)<br>Dynamically adjusts parallelism and concurrency based on hardware and node count, accelerating statistics collection.<br>Faster Database Restores<br>Reduces recovery time for full database and point-in-time restores (PITR).<br>Unlimited Transaction Size<br>Removes memory limits on uncommitted transactions, improving batch task success rates.<br>Load-Based Traffic Rebalancing in TiProxy(GA)<br>Routes traffic based on TiDB node workloads to optimize resource utilization.<br></td>
    <td>PD Microservice Router Service<br>Enables independent deployment, stateless(no Strong Leader) and easy scaling of Router Service(region meta query/updates) in PD, preventing PD from becoming a bottleneck for cluster resources.<br>Reduced I/O for Statistics Collection  (GA)<br>Allows users to scan only a portion of data samples on TiKV, reducing time and resource consumption for statistics collection.<br>Limit Operator Pushdown<br>Removes limitations on pushing down the Limit operator from TiDB to TiKV, enabling more efficient query processing directly at the storage layer.<br>Cascades Optimizer Framework<br>Introduces a mature, advanced optimizer framework, expanding the capabilities of the existing optimizer.<br>Scalable DDL Execution Framework<br>Provides a parallel DDL execution framework to improve the performance and stability of DDL operations.<br>Increased TiCDC Scalability<br>Updated TiCDC architecture delivers increased scalability and performance for change data capture use cases.<br></td>
    <td>Table-Level Load Balancing<br>Optimizes data scheduling in PD based on workload distribution across Regions for each table.<br>System Table Performance Optimization<br>Enhances query speed and reduces overhead for system tables with large data volumes.<br>Enhance the Scability of Region Meta Storage<br>Migrate region meta storage from PD to TiKV, the storage layer can scale infinitely ans easily.<br></td>
  </tr>
  <tr>
    <td>Advanced SQL Features and Flexibility<br>Cutting-edge SQL capabilities, improving compatibility, flexibility, and ease of use for complex queries and modern applications<br></td>
    <td>Vector Search Support<br>Enables vector data types, indexing, and high-performance vector search, with support for mixed queries involving vector and relational data.<br>Foreign Keys(GA)<br>Providing robust relational integrity.<br>Global indexing on partitioned tables(GA)<br>Removes the unique key restriction on partition keys, boosting query performance for non-partitioned columns.</td>
    <td>Modifiable Column Types in Partitioned Tables<br>Allows users to change column data types in partitioned tables, even if the column is a partitioning key.<br></td>
    <td>Materialized Views Support<br>Enables materialized views to improve pre-computation, boost computational efficiency, and enhance data analysis performance.<br></td>
  </tr>
  <tr>
    <td>Unbreakable Reliability and Always-On Availability <br>Near-zero downtime and enhanced fault tolerance to maintain uninterrupted operations and deliver a rock-solid user experience<br></td>
    <td>Limit Memory for Backups<br>Limit Memory for Statistics Collection (GA)<br>Enhanced SQL Binding Management (GA)<br>Simplifies creating and managing large numbers of execution plans to stabilize performance.<br>Improved Resource Group Control for Complex SQL (GA)<br>Monitors RU usage of complex queries mid-execution to minimize system impact.<br>Automatic Resource Group Switching for Runaway Queries (GA)<br>Detects runaway queries and redirects them to designated resource groups with set limits. <br>Limit Memory Usage for Schema Metadata（GA）<br>Enhances stability in large-scale clusters by capping memory consumption for schema metadata.<br></td>
    <td>Robust and Resilient Backup <br>Reduces memory-related issues during backup processes, ensuring dependable data protection and availability.<br>Optimized Memory Management with Disk Spilling<br>Allows operators like HashAgg, Sort, and Join to spill to disk, reducing memory load and preventing out-of-memory (OOM) issues.<br>Sharing Plan Cache across Sessions (GA)<br>Shares execution plan cache across sessions in the same TiDB instance, optimizing memory usage.<br>Resource Group Quota Management (GA)<br>Dynamically adjusts resource limits for Burstable resource groups, fully utilizing available resources without impacting other quotas.<br></td>
    <td>Adaptive Resource Group<br>Automatically adjusts Request Unit (RU) settings in resource groups based on past execution patterns.<br>Enhanced Memory Protection<br>Monitors memory usage across all components to prevent operations that could impact system stability.<br>Automatic SQL Binding<br>Analyzes SQL performance metrics to automatically create bindings, stabilizing execution plans for transactional processing.<br>Multi-Versioned Statistics<br>Allows users to view and restore previous statistics versions after updates.<br>Distributed Statistics Collection<br>Enables parallel statistics collection across multiple TiDB nodes to boost efficiency.<br></td>
  </tr>
  <tr>
    <td>Effortless Operations and Intelligent Observability<br>Simplify management with proactive monitoring and insights to optimize performance and ensure smooth operations<br></td>
    <td>Reliable Query Termination（GA）<br>Instantly terminates running SQL statements and frees resources in TiDB and TiKV.<br>Permissioned Resource Group Switching (GA)<br>Restricts resource group switching to authorized users, preventing resource misuse.<br>CPU Time Observation for TiDB and TiKV (GA)<br>Adds CPU time metrics to logs, enabling quick identification of statements causing CPU spikes.<br></td>
    <td>Customizable Statistics Collection (GA)<br>Allows tailored statistics strategies for specific tables, adjusting parameters like health and parallelism.<br>Workload Repository (GA)<br>Stores workload stats and real-time data for improved troubleshooting and analysis.<br>Automated Index Advisor (GA)<br>Automatically analyzes SQL statements to recommend index optimizations, including suggestions for creating or dropping indexes.<br>Standardized Time Model (GA)<br>Establishes a unified SQL execution time model to help identify database load sources through logs and cluster metrics, pinpointing problematic nodes and statements.<br>TiFlash CPU Time Monitoring (GA)<br>Adds TiFlash CPU time metrics to logs, enabling quick identification of statements that cause CPU spikes in TiFlash.</td>
    <td>Workload Analysis<br>Analyzes historical data from the Workload Repository to provide optimization recommendations, including SQL tuning and statistics collection.<br>End-to-End SQL Monitoring<br>Tracks the entire lifecycle of SQL statements, measuring time spent across TiDB, TiKV, PD, and TiFlash for detailed performance insights.<br></td>
  </tr>
  <tr>
    <td>Comprehensive Data Security and Privacy <br>Robust security measures to safeguard sensitive data, ensuring top-tier protection, encryption, and compliance with evolving privacy regulations</td>
    <td>Google Cloud KMS(GA)<br>General availability for encryption-at-rest key management with Google Cloud KMS.<br>Azure Key Vault<br>Enhanced encryption-at-rest key management with Azure Key Vault integration.<br>Marker-Based Log Desensitization<br>Marks and selectively desensitizes sensitive data in cluster logs based on use case.<br>Column-Level Permission Management(GA)<br>Adds MySQL-compatible permissions at the column level for fine-grained access control.</td>
    <td>AWS IAM Authentication<br>Supports AWS IAM third-party ARN integration for secure access control in TiDB.<br>Kerberos Authentication(GA)<br>Enables authentication using Kerberos for added security.<br>Multi-Factor Authentication (MFA)<br>Adds support for multi-factor authentication to enhance user verification the multi-factor authentication mechanism.<br>Enhanced TLS Security(GA)<br>Ensures encrypted connections between all components within the TiDB cluster.<br>Refined Dynamic Privileges<br>Improves dynamic privilege management, including limitations on Super privilege.<br>FIPS Compliance(GA)<br>Ensures encryption methods comply with FIPS standards for secure data handling.<br></td>
    <td>Label-Based Access Control<br>Enables data access control through configurable labels.<br>Enhanced Client-Side Encryption<br>Supports encryption of key fields on the client side to strengthen data security.<br>Dynamic Data Desensitization<br>Allows data desensitization based on application scenarios, protecting sensitive business fields.<br></td>
  </tr>
</tbody></table>

> **Note:**
>
> These are non-exhaustive plans and are subject to change. Features might differ per service subscriptions.