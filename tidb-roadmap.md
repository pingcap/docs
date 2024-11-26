---
title: TiDB Roadmap
summary: Learn about what's coming in the future for TiDB.
---

# TiDB Roadmap

This roadmap provides a look into the proposed future. This will be continually updated as we release long-term stable (LTS) versions. The purpose is to provide visibility into what is coming, so that you can more closely follow the progress, learn about the key milestones on the way, and give feedback as the development work goes on.

In the course of development, this roadmap is subject to change based on user needs and feedback. **DO NOT** schedule your release plans according to the content of the roadmap. If you have a feature request or want to prioritize a feature, please file an issue on [GitHub](https://github.com/pingcap/tidb/issues).

> **Note:**
> 
> - If not marked as GA, these features are experimental.
> - These are non-exhaustive plans and are subject to change. 
> - Features might differ per service subscriptions.

## Rolling roadmap highlights

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>End of CY24 release</th>
      <th>Mid of CY25 release</th>
      <th>Future releases</th>
    </tr>
  </thead>
  <tbody valign="top">
    <tr>
      <td>
        <b>Unmatched Scalability and Peak Performance</b>
        <br />Deliver massive scalability and faster performance to support larger workloads, optimize resource utilization, and ensure superior responsiveness.
      </td>
      <td>
        <ul>
          <li>
            <b>In-memory caching in TiKV</b>
            <br />TiKV maintains recent versions of data in memory to reduce redundant MVCC scans, thus improving performance.
          </li>
          <br />
          <li>
            <b>Adaptive Parallelism for Statistics Collection (GA)</b>
            <br />Dynamically adjusts parallelism and concurrency based on hardware and node count, accelerating statistics collection.
          </li>
          <br />
          <li>
            <b>Faster Database Restores</b>
            <br />Reduces recovery time for full database and Point in Time Recovery (PITR).
          </li>
          <br />
          <li>
            <b>Unlimited Transaction Size</b>
            <br />Removes memory limits on uncommitted transactions, improving success rates of transactions and batch tasks.
          </li>
          <br />
          <li>
            <b>Load-Based Traffic Rebalancing in TiProxy (GA)</b>
            <br />Routes traffic based on TiDB node workloads to optimize resource utilization.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>PD Microservice Router Service</b>
            <br />Enables independent deployment, stateless operation (without a strong leader), and easy scaling of the PD router service (region metadata queries and updates), preventing PD from becoming a bottleneck for cluster resources.
          </li>
          <br />
          <li>
            <b>Reduced I/O for Statistics Collection (GA)</b>
            <br />Allows you to scan only a portion of data samples on TiKV, reducing time and resource consumption for statistics collection.
          </li>
          <br />
          <li>
            <b><code>Limit</code> Operator Pushdown</b>
            <br />Removes limitations on pushing down the <code>Limit</code> operator from TiDB to TiKV, enabling more efficient query processing directly at the storage layer.
          </li>
          <br />
          <li>
            <b>Cascades Optimizer Framework</b>
            <br />Introduces a mature, advanced optimizer framework, expanding the capabilities of the existing optimizer.
          </li>
          <br />
          <li>
            <b>Scalable DDL Execution Framework</b>
            <br />Provides a scalable and parallel DDL execution framework to improve the performance and stability of DDL operations.
          </li>
          <br />
          <li>
            <b>Increased TiCDC Scalability</b>
            <br />Introduces a new TiCDC architecture that enhances scalability and performance for change data capture scenarios.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Table-Level Load Balancing</b>
            <br />Optimizes data scheduling in PD based on workload distribution across Regions for each table.
          </li>
          <br />
          <li>
            <b>System Table Performance Optimization</b>
            <br />Enhances query speed and reduces overhead for system tables with large data volumes.
          </li>
          <br />
          <li>
            <b>Enhance the Scalability of Region Metadata Storage</b>
            <br />Splits a dedicated stateless router service (read/write of region metadata) and migrates region metadata storage from PD to TiKV. The metadata storage layer will scale limitlessly and easily.
          </li>
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Advanced SQL Features and Flexibility</b>
        <br />Cutting-edge SQL capabilities, improving compatibility, flexibility, and ease of use for complex queries and modern applications
      </td>
      <td>
        <ul>
          <li>
            <b>Vector Search</b>
            <br />Enables vector data types, indexing, and high-performance vector search, supporting mixed queries involving vector and relational data.
          </li>
          <br />
          <li>
            <b>Foreign Keys is generally available (GA)</b>
          </li>
          <br />
          <li>
            <b>Global indexing on partitioned tables (GA)</b>
            <br />Removes the unique key restriction on partition keys, boosting query performance for non-partitioned columns.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Modifiable Column Types in Partitioned Tables</b>
            <br />Allows you to change column data types in partitioned tables, even if the column is a partitioning key.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Materialized Views</b>
            <br />Enables materialized views to improve pre-computation, boost computational efficiency, and enhance data analysis performance.
          </li>
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Unbreakable Reliability and Always-On Availability</b>
        <br />Near-zero downtime and enhanced fault tolerance to maintain uninterrupted operations and deliver a rock-solid user experience
      </td>
      <td>
        <ul>
          <li>
            <b>Limit Memory Usage for Backups</b>
          </li>
          <br />
          <li>
            <b>Limit Memory Usage for Statistics Collection (GA)</b>
          </li>
          <br />
          <li>
            <b>Enhanced SQL Binding Management (GA)</b>
            <br />Simplifies creating and managing large numbers of execution plans to stabilize performance.
          </li>
          <br />
          <li>
            <b>Improved Resource Group Control for Complex SQL (GA)</b>
            <br />Monitors RU usage during complex query execution to minimize system impact.
          </li>
          <br />
          <li>
            <b>Automatic Resource Group Switching for Runaway Queries (GA)</b>
            <br />Detects runaway queries and redirects them to designated resource groups with predefined limits.
          </li>
          <br />
          <li>
            <b>Limit Memory Usage for Schema Metadata (GA)</b>
            <br />Enhances stability in large-scale clusters by reducing memory consumption for schema metadata.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Robust and Resilient Backup</b>
            <br />Reduces memory-related issues during backup processes, ensuring dependable data protection and availability.
          </li>
          <br />
          <li>
            <b>Optimized Memory Management with Disk Spilling</b>
            <br />Allows operators such as HashAgg, Sort, and Join to spill to disk, reducing memory load and preventing out-of-memory (OOM) issues.
          </li>
          <br />
          <li>
            <b>Sharing Plan Cache across Sessions (GA)</b>
            <br />Shares execution plan cache across sessions in the same TiDB instance, optimizing memory usage.
          </li>
          <br />
          <li>
            <b>Resource Group Quota Management (GA)</b>
            <br />Dynamically adjusts resource limits for Burstable resource groups, fully utilizing available resources without impacting other quotas.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Adaptive Resource Group</b>
            <br />Automatically adjusts Request Unit (RU) settings in resource groups based on past execution patterns.
          </li>
          <br />
          <li>
            <b>Enhanced Memory Protection</b>
            <br />Monitors memory usage across all components to prevent operations that might affect system stability.
          </li>
          <br />
          <li>
            <b>Automatic SQL Binding</b>
            <br />Analyzes SQL performance metrics to automatically create bindings, stabilizing execution plans for transactional processing.
          </li>
          <br />
          <li>
            <b>Multi-Versioned Statistics</b>
            <br />Allows you to view and restore previous statistics versions after updates.
          </li>
          <br />
          <li>
            <b>Distributed Statistics Collection</b>
            <br />Enables parallel statistics collection across multiple TiDB nodes to boost efficiency.
          </li>
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Effortless Operations and Intelligent Observability</b>
        <br />Simplify management with proactive monitoring and insights to optimize performance and ensure smooth operations
      </td>
      <td>
        <ul>
          <li>
            <b>Reliable Query Termination (GA)</b>
            <br />Instantly terminates running SQL statements and frees resources in TiDB and TiKV.
          </li>
          <br />
          <li>
            <b>Access Control for Resource Group Switching (GA)</b>
            <br />Restricts resource group switching to authorized users, preventing resource misuse.
          </li>
          <br />
          <li>
            <b>CPU Time Observation for TiDB and TiKV (GA)</b>
            <br />Adds TiDB and TiKV CPU time metrics to statements and slow logs, enabling quick identification of statements causing TiDB or TiKV CPU spikes.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Customizable Statistics Collection (GA)</b>
            <br />Allows tailored statistics strategies for specific tables, adjusting parameters such as health and concurrency.
          </li>
          <br />
          <li>
            <b>Workload Repository (GA)</b>
            <br />Stores workload stats and real-time data for improved troubleshooting and analysis.
          </li>
          <br />
          <li>
            <b>Automated Index Advisor (GA)</b>
            <br />Automatically analyzes SQL statements to recommend index optimizations, including suggestions for creating or dropping indexes.
          </li>
          <br />
          <li>
            <b>Standardized Time Model (GA)</b>
            <br />Establishes a unified SQL execution time model to help identify database load sources through statement summary tables, logs, and cluster metrics, pinpointing problematic nodes and statements.
          </li>
          <br />
          <li>
            <b>TiFlash CPU Time Monitoring (GA)</b>
            <br />Adds TiFlash CPU time metrics to statement summary tables and slow logs, enabling quick identification of statements that cause CPU spikes in TiFlash.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Workload Analysis</b>
            <br />Analyzes historical data from the Workload Repository to provide optimization recommendations, including SQL tuning and statistics collection.
          </li>
          <br />
          <li>
            <b>End-to-End SQL Monitoring</b>
            <br />Tracks the entire lifecycle of SQL statements, measuring time spent across TiDB, TiKV, PD, and TiFlash for detailed performance insights.
          </li>
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Comprehensive Data Security and Privacy</b>
        <br />Robust security measures to safeguard sensitive data, ensuring top-tier protection, encryption, and compliance with evolving privacy regulations
      </td>
      <td>
        <ul>
          <li>
            <b>Google Cloud KMS (GA)</b>
            <br />General availability for encryption-at-rest key management with Google Cloud KMS.
          </li>
          <br />
          <li>
            <b>Azure Key Vault</b>
            <br />Enhanced encryption-at-rest key management with Azure Key Vault integration.
          </li>
          <br />
          <li>
            <b>Marker-Based Log Desensitization</b>
            <br />Marks and selectively desensitizes sensitive data in cluster logs based on use case.
          </li>
          <br />
          <li>
            <b>Column-Level Permission Management (GA)</b>
            <br />Adds MySQL-compatible permissions at the column level for fine-grained access control.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>AWS IAM Authentication</b>
            <br />Supports AWS IAM third-party ARN integration for secure access control in TiDB.
          </li>
          <br />
          <li>
            <b>Kerberos Authentication (GA)</b>
            <br />Enables authentication using Kerberos for enhanced security.
          </li>
          <br />
          <li>
            <b>Multi-Factor Authentication (MFA)</b>
            <br />Supports multi-factor authentication to enhance user verification.
          </li>
          <br />
          <li>
            <b>Enhanced TLS Security (GA)</b>
            <br />Ensures encrypted connections between all components within the TiDB cluster.
          </li>
          <br />
          <li>
            <b>Refined Dynamic Privileges</b>
            <br />Improves dynamic privilege management, including limitations on Super privilege.
          </li>
          <br />
          <li>
            <b>FIPS Compliance (GA)</b>
            <br />Ensures encryption methods comply with FIPS standards for secure data handling.
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Label-Based Access Control</b>
            <br />Enables data access control through configurable labels.
          </li>
          <br />
          <li>
            <b>Enhanced Client-Side Encryption</b>
            <br />Supports encryption of key fields on the client side to strengthen data security.
          </li>
          <br />
          <li>
            <b>Dynamic Data Desensitization</b>
            <br />Allows data desensitization based on application scenarios, protecting sensitive business fields.
          </li>
          <br />
        </ul>
      </td>
    </tr>
  </tbody>
</table>
