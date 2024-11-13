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
          <li>
            <b>Adaptive Parallelism for Stats Collection (GA)</b>
            <br />Dynamically adjusts parallelism and concurrency based on hardware and node count, accelerating statistics collection.
          </li>
          <li>
            <b>Faster Database Restores</b>
            <br />Reduces recovery time for full database and point-in-time restores (PITR).
          </li>
          <li>
            <b>Unlimited Transaction Size</b>
            <br />Removes memory limits on uncommitted transactions, improving batch task success rates.
          </li>
          <li>
            <b>Load-Based Traffic Rebalancing in TiProxy (GA)</b>
            <br />Routes traffic based on TiDB node workloads to optimize resource utilization.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>PD Microservice Router Service</b>
            <br />Enables independent deployment, stateless (no Strong Leader) and easy scaling of Router Service (region meta query/updates) in PD, preventing PD from becoming a bottleneck for cluster resources.
          </li>
          <li>
            <b>Reduced I/O for Statistics Collection (GA)</b>
            <br />Allows users to scan only a portion of data samples on TiKV, reducing time and resource consumption for statistics collection.
          </li>
          <li>
            <b>Limit Operator Pushdown</b>
            <br />Removes limitations on pushing down the Limit operator from TiDB to TiKV, enabling more efficient query processing directly at the storage layer.
          </li>
          <li>
            <b>Cascades Optimizer Framework</b>
            <br />Introduces a mature, advanced optimizer framework, expanding the capabilities of the existing optimizer.
          </li>
          <li>
            <b>Scalable DDL Execution Framework</b>
            <br />Provides a parallel DDL execution framework to improve the performance and stability of DDL operations.
          </li>
          <li>
            <b>Increased TiCDC Scalability</b>
            <br />Updated TiCDC architecture delivers increased scalability and performance for change data capture use cases.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Table-Level Load Balancing</b>
            <br />Optimizes data scheduling in PD based on workload distribution across Regions for each table.
          </li>
          <li>
            <b>System Table Performance Optimization</b>
            <br />Enhances query speed and reduces overhead for system tables with large data volumes.
          </li>
          <li>
            <b>Enhance the Scalability of Region Meta Storage</b>
            <br />Migrate region meta storage from PD to TiKV, allowing the storage layer to scale infinitely and easily.
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Advanced SQL Features and Flexibility</b>
        <em>Cutting-edge SQL capabilities, improving compatibility, flexibility, and ease of use for complex queries and modern applications</em>
      </td>
      <td>
        <ul>
          <li>
            <b>Vector Search Support</b>
            <br />Enables vector data types, indexing, and high-performance vector search, with support for mixed queries involving vector and relational data.
          </li>
          <li>
            <b>Foreign Keys (GA)</b>
            <br />Now generally available, providing robust relational integrity.
          </li>
          <li>
            <b>Global indexing on partitioned tables (GA)</b>
            <br />Removes the unique key restriction on partition keys, boosting query performance for non-partitioned columns.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Modifiable Column Types in Partitioned Tables</b>
            <br />Allows users to change column data types in partitioned tables, even if the column is a partitioning key.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Materialized Views Support</b>
            <br />Enables materialized views to improve pre-computation, boost computational efficiency, and enhance data analysis performance.
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Unbreakable Reliability and Always-On Availability</b>
        <em>Near-zero downtime and enhanced fault tolerance to maintain uninterrupted operations and deliver a rock-solid user experience</em>
      </td>
      <td>
        <ul>
          <li>
            <b>Limit Memory for Backups</b>
          </li>
          <li>
            <b>Limit Memory for Statistics Collection (GA)</b>
          </li>
          <li>
            <b>Enhanced SQL Binding Management (GA)</b>
            <br />Simplifies creating and managing large numbers of execution plans to stabilize performance.
          </li>
          <li>
            <b>Improved Resource Group Control for Complex SQL (GA)</b>
            <br />Monitors RU usage of complex queries mid-execution to minimize system impact.
          </li>
          <li>
            <b>Automatic Resource Group Switching for Runaway Queries (GA)</b>
            <br />Detects runaway queries and redirects them to designated resource groups with set limits.
          </li>
          <li>
            <b>Limit Memory Usage for Schema Metadata (GA)</b>
            <br />Enhances stability in large-scale clusters by capping memory consumption for schema metadata.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Robust and Resilient Backup</b>
            <br />Reduces memory-related issues during backup processes, ensuring dependable data protection and availability.
          </li>
          <li>
            <b>Optimized Memory Management with Disk Spilling</b>
            <br />Allows operators like HashAgg, Sort, and Join to spill to disk, reducing memory load and preventing out-of-memory (OOM) issues.
          </li>
          <li>
            <b>Sharing Plan Cache across Sessions (GA)</b>
            <br />Shares execution plan cache across sessions in the same TiDB instance, optimizing memory usage.
          </li>
          <li>
            <b>Resource Group Quota Management (GA)</b>
            <br />Dynamically adjusts resource limits for Burstable resource groups, fully utilizing available resources without impacting other quotas.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Adaptive Resource Group</b>
            <br />Automatically adjusts Request Unit (RU) settings in resource groups based on past execution patterns.
          </li>
          <li>
            <b>Enhanced Memory Protection</b>
            <br />Monitors memory usage across all components to prevent operations that could impact system stability.
          </li>
          <li>
            <b>Automatic SQL Binding</b>
            <br />Analyzes SQL performance metrics to automatically create bindings, stabilizing execution plans for transactional processing.
          </li>
          <li>
            <b>Multi-Versioned Statistics</b>
            <br />Allows users to view and restore previous statistics versions after updates.
          </li>
          <li>
            <b>Distributed Statistics Collection</b>
            <br />Enables parallel statistics collection across multiple TiDB nodes to boost efficiency.
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Effortless Operations and Intelligent Observability</b>
        <em>Simplify management with proactive monitoring and insights to optimize performance and ensure smooth operations</em>
      </td>
      <td>
        <ul>
          <li>
            <b>Reliable Query Termination (GA)</b>
            <br />Instantly terminates running SQL statements and frees resources in TiDB and TiKV.
          </li>
          <li>
            <b>Permissioned Resource Group Switching (GA)</b>
            <br />Restricts resource group switching to authorized users, preventing resource misuse.
          </li>
          <li>
            <b>CPU Time Observation for TiDB and TiKV (GA)</b>
            <br />Adds CPU time metrics to logs, enabling quick identification of statements causing CPU spikes.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Customizable Statistics Collection (GA)</b>
            <br />Allows tailored statistics strategies for specific tables, adjusting parameters like health and parallelism.
          </li>
          <li>
            <b>Workload Repository (GA)</b>
            <br />Stores workload stats and real-time data for improved troubleshooting and analysis.
          </li>
          <li>
            <b>Automated Index Advisor (GA)</b>
            <br />Automatically analyzes SQL statements to recommend index optimizations, including suggestions for creating or dropping indexes.
          </li>
          <li>
            <b>Standardized Time Model (GA)</b>
            <br />Establishes a unified SQL execution time model to help identify database load sources through logs and cluster metrics, pinpointing problematic nodes and statements.
          </li>
          <li>
            <b>TiFlash CPU Time Monitoring (GA)</b>
            <br />Adds TiFlash CPU time metrics to logs, enabling quick identification of statements that cause CPU spikes in TiFlash.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Workload Analysis</b>
            <br />Analyzes historical data from the Workload Repository to provide optimization recommendations, including SQL tuning and statistics collection.
          </li>
          <li>
            <b>End-to-End SQL Monitoring</b>
            <br />Tracks the entire lifecycle of SQL statements, measuring time spent across TiDB, TiKV, PD, and TiFlash for detailed performance insights.
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Comprehensive Data Security and Privacy</b>
        <em>Robust security measures to safeguard sensitive data, ensuring top-tier protection, encryption, and compliance with evolving privacy regulations</em>
      </td>
      <td>
        <ul>
          <li>
            <b>Google Cloud KMS (GA)</b>
            <br />General availability for encryption-at-rest key management with Google Cloud KMS.
          </li>
          <li>
            <b>Azure Key Vault</b>
            <br />Enhanced encryption-at-rest key management with Azure Key Vault integration.
          </li>
          <li>
            <b>Marker-Based Log Desensitization</b>
            <br />Marks and selectively desensitizes sensitive data in cluster logs based on use case.
          </li>
          <li>
            <b>Column-Level Permission Management (GA)</b>
            <br />Adds MySQL-compatible permissions at the column level for fine-grained access control.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>AWS IAM Authentication</b>
            <br />Supports AWS IAM third-party ARN integration for secure access control in TiDB.
          </li>
          <li>
            <b>Kerberos Authentication (GA)</b>
            <br />Enables authentication using Kerberos for added security.
          </li>
          <li>
            <b>Multi-Factor Authentication (MFA)</b>
            <br />Adds support for multi-factor authentication to enhance user verification.
          </li>
          <li>
            <b>Enhanced TLS Security (GA)</b>
            <br />Ensures encrypted connections between all components within the TiDB cluster.
          </li>
          <li>
            <b>Refined Dynamic Privileges</b>
            <br />Improves dynamic privilege management, including limitations on Super privilege.
          </li>
          <li>
            <b>FIPS Compliance (GA)</b>
            <br />Ensures encryption methods comply with FIPS standards for secure data handling.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Label-Based Access Control</b>
            <br />Enables data access control through configurable labels.
          </li>
          <li>
            <b>Enhanced Client-Side Encryption</b>
            <br />Supports encryption of key fields on the client side to strengthen data security.
          </li>
          <li>
            <b>Dynamic Data Desensitization</b>
            <br />Allows data desensitization based on application scenarios, protecting sensitive business fields.
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>
