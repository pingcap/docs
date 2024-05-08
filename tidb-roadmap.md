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
             <b>TiKV In-Memory Cache </b><br />
            TiKV maintains the recent copies of hot rows to reduce repeated MVCC scans. 
          </li>
          <br />
          <li>
             <b>Global Indexing on partitioned tables</b><br />
          </li>
          <br />
          <li>
             <b>Adaptive concurrency for stats collections</b><br />
            TiDB decides the degree of parallelism  based on the deployment and hardware specifications, that increases the performance with default options.
          </li>
          <br />
          <li>
             <b>Rapid Database Restoration</b><br />
            Accelerate the processing of full restore and PiTR.
          </li>
          <br />
          <li>
             <b>Unlimited Size of Transactions</b><br />
            The size of transactions no longer rely on the available memory in TiDB instances, that reduces the chance of transaction failure.
          </li>
          <br />
          <li>
             <b>Load-based Rebalance in TiProxy</b><br />
            TiProxy decides the target instances based on the recent load of each TiDB instance, in order to make full use of resources.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>PD microservice - heartbeat</b><br />
            Heartbeat services in PD can be deployed independently. It reduces the chance that PD becomes the bottleneck of the cluster.
          </li>
          <br />
          <li>
            <b>Less I/O made by stats collections</b><br />
            TiKV makes partial scanning and returns only necessary data sets when stats collection decides to sample the tables, which reduces the time and resource spent.
          </li>
          <br />
          <li>
            <b>Less limitations for pushing Limit to TiKV</b><br />
          </li>
          <br />
          <li>
            <b>Cascades Optimizer </b><br />
            A sophisticated framework that extends the capabilities of optimizer.
          </li>
          <br />
          <li>
            <b>Single DM task reaches 150 MiB/s for full data migration</b><br />
          </li>
          <br />
          <li>
            <b>Enhanced  DDL framework</b><br />
            Providing scalable and parallel DDL task execution capability, enhancing scalability and performance.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Load-based table rebalance</b><br />
            PD measures the load of each table and decides the rebalance.
          </li>
          <br />
          <li>
            <b>Dealing with massive records in system tables</b><br />
            Boost the performance of querying system tables with massive records.
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
            <b>Limited memory for backup tasks</b><br />
          </li>
          <br />
          <li>
            <b>Limited memory for stats collections</b><br />
          </li>
          <br />
          <li>
            <b>Managing massive SQL bindings</b><br />
              Improve the user experience of importing and managing a large number of SQL bindings. 
          </li>
          <br />
          <li>
            <b>Charging RU intermittently for an expensive SQL</b><br />
              Measure the RU produced before one large query completes, which mitigates the impacted by expensives SQL in resource groups.
          </li>
          <br />
          <li>
            <b>Switching resource groups of runaway queries</b><br />
              When a query is identified as runaway queries, users can put it to a particular resource group, in order to limit its resource. 
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Limited memory for schema meta</b><br />
          </li>
          <br />
          <li>
            <b>Distributed statistic collection</b><br />
            Collecting statistics in parallel across multiple TiDB instances.
          </li>
          <br />
          <li>
            <b>Multi-versioned statistics</b><br />
            When the statistics are updated, users can manage to review the past copies or rollback.
          </li>
          <br />
          <li>
            <b>Reliable backup </b><br />
            Reduce the chance of OOM and secure the availability of backups.
          </li>
          <br />
          <li>
            <b>The popular operators spill to disk</b><br />
            To minimize the change of OOM. The target operators: HashAgg / Sort / TopN / HashJoin / WindowFunction / IndexJoin / IndexHashJoin
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Adaptive Resource Group</b><br />
            TiDB automatically decides reasonable RU for resource groups according to past metrics.
          </li>
          <br />
          <li>
            <b>Enforced memory assurance</b><br />
            TiDB actively manages memory usage across all modules, and prevents excessive memory that  potentially causes system instability. 
          </li>
          <br />
          <li>
            <b>Plan cache at instance level</b><br />
            All sessions from the same TiDB instance share plan cache.
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
            <b>Guaranteed query termination</b><br />
            The running statements can be killed instantly with resources released from TiDB and TiKV.
          </li>
          <br />
          <li>
            <b>Enforced permission on switching groups</b>
            <br />Switching resource groups needs privileges to be granted.
          </li>
          <br />
          <li>
            <b>Mapping tables / SQL with hot regions</b>
          </li>
          <br />
          <li>
            <b>Logical data import mode with "IMPORT INTO"</b>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Customized preference for stats collections</b>
            <br />Users are able to set certain options such as staleness ratio at table level.
          </li>
          <br />
          <li>
            <b>Workload Repository</b>
            <br />TiDB manages to persist volatile tables which include both cumulative metrics and active metrics. This helps greatly during troubleshooting.
          </li>
          <br />
          <li>
            <b>Automatic index advisor</b>
            <br />TiDB finds candidate queries and recommend new indexes or unused indexes to users. 
          </li>
          <br />
          <li>
            <b>The columns can be altered on partitioned tables</b>
            <br />Users are able to alter the column type no matter if it's partitioning key or not.
          </li>
          <br />
          <li>
            <b>Confliction Strategy for IMPORT INTO</b>
            <br />Users set the strategy for the conficition found during data ingestion, such "error", "ignore" and "replace".
          </li>
          <br />
          <li>
            <b>End-to-End Observation</b>
            <br />Introduce a way to breakdown the duration produced by one SQL statement during its lifetime, including the time spent in TiDB, PD, TiKV and TiFlash.
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Workload Analysis</b>
            <br />Mine Workload Repository and make necessary recommendations, such SQL tuning, Stats collections, etc.
          </li>
          <br />
          <li>
            <b>Revisable Primary Key </b>
          </li>
          <br />
          <li>
            <b>Export Data as SQL statements</b>
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
            <b>GCP KMS</b>
            <br />Encryption at rest supports GCP KMS key management.
          </li>
          <br />
          <li>
            <b>Dynamic privilege design</b>
            <br />Improve the dynamic privilege design and restrict the use of "Super".
          </li>
          <br />
          <li>
            <b>Marker-based log desensitization</b>
            <br />Supports the ability to optionally desensitize cluster logs based on usage scenarios.
          </li>
          <br />
          <li>
            <b>FIPS</b>
            <br />Encryption scenarios comply with FIPS standards.
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
            <br />Supports Kerberos-based authentication.
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
            <br />Access permissions granted by configured labels.
          </li>
          <br />
          <li>
            <b>Enhanced client-side encryption</b>
            <br />Supports client-side encryption of key fields to enhance data security.
          </li>
          <br />
          <li>
            <b>Dynamic desensitization of business data</b>
            <br />Data desensitization based on different data application scenarios to protect the data security of important fields.
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

These are non-exhaustive plans and are subject to change. Features might differ per service subscriptions.
