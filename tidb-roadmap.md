---
title: TiDB Roadmap
summary: Learn about what's coming in the future for TiDB.
---

# TiDB Roadmap

This roadmap provides a look into the proposed future. This will be continually updated as we release long-term stable (LTS) versions. The purpose is to provide visibility into what is coming, so that you can more closely follow the progress, learn about the key milestones on the way, and give feedback as the development work goes on.

In the course of development, this roadmap is subject to change based on user needs and feedback. Please do not schedule release plans on the content of the roadmap. If you have a feature request or want to prioritize a feature, please file an issue on [GitHub](https://github.com/pingcap/tidb/issues).

## Rolling roadmap highlights

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>End of CY24 LTS release</th>
      <th>Mid of CY25 LTS release</th>
      <th>Future releases</th>
    </tr>
  </thead>
  <tbody valign="top">
    <tr>
      <td>
        <b>Scalability and Performance</b><br /><i>Enhance horsepower</i>
      </td>
      <td>
        <ul>
           <li>
             <b>TiKV in-memory data cache</b><br />
            TiKV maintains recent versions of data in memory to reduce redundant MVCC scans, thus improving performance.
          </li>
          <br />
          <li>
             <b>Global indexing for partitioned tables</b><br />
          </li>
          <br />
          <li>
             <b>Adaptive concurrency for statistics collection</b><br />
            TiDB automatically adjusts the parallelism and scan concurrency of statistics collection tasks based on the number of deployed nodes and hardware specifications, improving collection speed.
          </li>
          <br />
          <li>
             <b>Rapid database recovery</b><br />
            Reduce the time required for full database recovery and point-in-time recovery (PITR).
          </li>
          <br />
          <li>
             <b>Unlimited-size transactions</b><br />
            The volume of data processed by uncommitted transactions is no longer limited by the available memory of TiDB nodes, thus improving the success rate of transactions and batch tasks.
          </li>
          <br />
          <li>
             <b>Load-based traffic routing by TiProxy</b><br />
            TiProxy forwards traffic based on the load status of the target TiDB, maximizing hardware resource utilization.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Microservice for PD heartbeat</b><br />
            Heartbeat services in PD can be independently deployed and scaled, preventing PD from becoming a bottleneck for the cluster's resources.
          </li>
          <br />
          <li>
            <b>Less I/O consumption during statistics collection</b><br />
            Users can choose to scan only a portion of the data samples on TiKV during statistics collection, reducing time and resource consumption.
          </li>
          <br />
          <li>
            <b>Less limitations for pushing down Limit operator to TiKV</b><br />
          </li>
          <br />
          <li>
            <b>Cascades optimizer framework</b><br />
            Introduce a more mature and powerful optimizer framework to expand the capabilities of the current optimizer.
          </li>
          <br />
          <li>
            <b>Single DM task reaches 150 MiB/s during full data migration</b><br />
          </li>
          <br />
          <li>
            <b>Enhanced DDL execution framework</b><br />
            Provide a scalable parallel DDL execution framework to improve the performance and stability of DDL operations.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Table-level load balancing</b><br />
            PD determines data scheduling strategies based on the load situation of each Region on every table.
          </li>
          <li>
            <b>Improve performance of handling system tables with large data volumes</b><br />
            Enhance the performance of querying large data volumes in system tables to reduce query overhead.
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Reliability and Availability</b>
        <br /><i>Enhance dependability</i>
      </td>
      <td>
        <ul>
          <li>
            <b>Limited memory consumption for backup tasks</b><br />
          </li>
          <br />
          <li>
            <b>Limited memory consumption for statistics collection</b><br />
          </li>
          <br />
          <li>
            <b>Manage massive SQL bindings</b><br />
              Improve the user experience of SQL binding, making it convenient for users to create and manage a large number of execution plans to stabilize database performance.
          </li>
          <br />
          <li>
            <b>Enhance resource group control over complex SQL</b><br />
              Regularly assess the Request Unit (RU) consumption of complex SQL before completion of execution to prevent excessively large impacts on the entire system during execution.
          </li>
          <br />
          <li>
            <b>Automatically switch resource groups for runaway queries</b><br />
              When a query is identified as a runaway query, users can choose to adjust it to a specific resource group and set an upper limit on resource consumption.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Limited memory consumption of schema metadata</b><br />
            Enhance the stability of large-scale clusters.
          </li>
          <br />
          <li>
            <b>Distributed statistic collection</b><br />
            Statistics collection supports parallel execution across multiple TiDB nodes to improve collection efficiency.
          </li>
          <br />
          <li>
            <b>Multi-version statistics</b><br />
            After the statistics information is updated, users can view the historical versions and choose to restore them to a previous version.
          </li>
          <br />
          <li>
            <b>Reliable data backup</b><br />
            Reduce potential issues like insufficient memory during data backup and ensure the availability of backup data.
          </li>
          <br />
          <li>
            <b>Common operators support spilling to disk</b><br />
            Common operators like HashAgg, Sort, TopN, HashJoin, WindowFunction, IndexJoin, and IndexHashJoin support spilling to disk, reducing the risk of out-of-memory (OOM).
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Adaptive resource group</b><br />
            Resource groups automatically adjust their reservation unit (RU) settings based on past execution patterns.
          </li>
          <br />
          <li>
            <b>Enhanced memory protection</b><br />
            TiDB actively monitors the memory usage of all modules and prevents memory operations that might impact system stability.
          </li>
          <br />
          <li>
            <b>Instance-level execution plan cache</b><br />
            All sessions within the same TiDB instance can share the execution plan cache, improving memory utilization.
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Database Operations and Observability</b>
        <br /><i>Enhance DB manageability and its ecosystem</i>
      </td>
      <td>
        <ul>
           <li>
            <b>Reliable query termination</b><br />
            Running SQL statements can be immediately terminated, and the corresponding resources are released from TiDB and TiKV.
          </li>
          <br />
          <li>
            <b>Permission control for switching resource groups</b>
            <br />Only users granted specific permissions can switch their resource groups, preventing resource abuse.
          </li>
          <br />
          <li>
            <b>Mapping tables or SQL with hot Regions</b>
          </li>
          <br />
          <li>
            <b>Logical data import mode with <code>IMPORT INTO</code></b>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Fine-grained customization of statistics collection</b>
            <br />Users can modify the statistics collection strategy for specific tables, such as healthiness and parallelism levels.
          </li>
          <br />
          <li>
            <b>Workload Repository</b>
            <br />TiDB persists load information in memory, including cumulative and real-time statistics data, which aids in troubleshooting and analysis.
          </li>
          <br />
          <li>
            <b>Automatic index advisor</b>
            <br />TiDB automatically analyzes SQL statements that can be optimized and recommends creating or dropping indexes.
          </li>
          <br />
          <li>
            <b>Support modifying column types in partitioned tables</b>
            <br />Users can modify the data type of columns in partitioned tables, regardless of whether the column is a partitioning key.
          </li>
          <br />
          <li>
            <b>Conflict strategy for <code>IMPORT INTO</code></b>
            <br />Users can set the conflict resolution strategy when importing data, such as exiting with an error, ignoring, or replacing in case of conflicts.
          </li>
          <br />
          <li>
            <b>End-to-End monitoring</b>
            <br />Track the time consumption of individual SQL statements throughout their entire lifecycle, including TiDB, TiKV, PD, and TiFlash components.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Workload analysis</b>
            <br />Analyze historical workload data from the Workload Repository and provide optimization recommendations, such as SQL tuning and adjustments to statistics collection strategies.
          </li>
          <br />
          <li>
            <b>Revisable primary key</b>
          </li>
          <br />
          <li>
            <b>Export data as SQL statements</b>
          </li>
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Security</b>
        <br /><i>Enhance data safety and privacy</i>
      </td>
      <td>
        <ul>
          <li>
            <b>Google Cloud KMS</b>
            <br />Enhance the key management mechanism for static encryption based on Google Cloud KMS, making it generally available.
          </li>
          <br />
          <li>
            <b>Improved dynamic privilege</b>
            <br />Improve the dynamic privilege design and limit the implementation of Super privilege.
          </li>
          <br />
          <li>
            <b>Marker-based log desensitization</b>
            <br />Support marking sensitive information in the cluster log, and then you can determine whether to desensitize it according to the usage scenario.
          </li>
          <br />
          <li>
            <b>FIPS</b>
            <br />Encryption scenarios comply with FIPS.
          </li>
        </ul>
      </td>
      <td>
        <ul>
           <li>
            <b>IAM authentication for AWS</b>
            <br />TiDB as AWS third-party ARN for AWS IAM access.
          </li>
          <br />
          <li>
            <b>Kerberos</b>
            <br />Support Kerberos-based authentication.
          </li>
          <li>
            <b>MFA</b>
            <br />Support multi-factor authentication mechanism.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Label-based access control</b>
            <br />Support data access control by configuring labels.
          </li>
          <br />
          <li>
            <b>Enhanced client-side encryption</b>
            <br />Support client-side encryption of key fields to enhance data security.
          </li>
          <br />
          <li>
            <b>Dynamic desensitization of business data</b>
            <br />Data desensitization based on different data application scenarios to ensure data security in important fields.
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

> **Note:**
>
> These are non-exhaustive plans and are subject to change. Features might differ per service subscriptions.