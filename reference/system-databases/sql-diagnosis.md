---
title: SQL Diagnosis
summary: Understand SQL diagnostics.
category: reference
---

# SQL diagnosis

SQL diagnosis is a feature introduced since TiDB v4.0. You can use this feature to locate problems in TiDB with higher efficiency. Before TiDB v4.0, you need to use different tools to obtain different information.

The SQL diagnosis system integrates information from all components of the system as a whole, provides a consistent interface to the upper layer through system tables, and provides monitoring summaries and automatic diagnosis, which makes it easier for you to query cluster information.

The SQL diagnosis system consists of three major parts:

+ **Cluster information table**: The SQL diagnosis system adds cluster information tables that provide a unified way to get the discrete information of each instance and node. This system fully integrates the cluster topology, hardware information, software information, kernel parameters, monitoring, system information, slow queries, statements, and logs of the entire cluster into the table, allowing you to query these information using SQL statements.

+ **Cluster monitoring table**: The SQL diagnosis system adds cluster monitoring tables. All of these tables are in `metrics_schema`, and you can query monitoring information using SQL statements. Compared to the visualized monitoring before v4.0, you can use this SQL-based method to perform correlated queries on all the monitoring information of the entire cluster, and compare the results of different time periods to quickly identify performance bottlenecks. Because the TiDB cluster has many monitoring metrics, the SQL diagnosis system also provides monitoring summary tables, which allows you to more easily find abnormal monitoring items.

+ **Automatic diagnosis**: Although you can manually execute SQL statements to query cluster information tables, cluster monitoring tables, and summary tables, the automatic diagnosis can provide you better user experience. The SQL diagnosis system performs automatic diagnosis based on the existing cluster information tables and monitoring tables, and provides relevant diagnosis result tables and diagnosis summary tables.

## Cluster information tables

The cluster information tables bring together the information of all nodes and instances in a cluster. With these tables, you can query all cluster information using only one SQL statement. The following is a list of cluster information tables:

+ From the cluster topology table `information_schema.cluster_info`, you can get the current topology information of the cluster, the version of each node, the Git Hash corresponding to the version, the starting time of each node, and the running time of each node.
+ From the cluster configuration table `information_schema.cluster_config`, you can get the configuration of all nodes in the cluster. For versions before 4.0, you need to access the HTTP API of each node one by one to get these configuration information.
+ On the cluster hardware table `information_schema.cluster_hardware`, you can quickly query the cluster hardware information.
+ On the cluster load table `information_schema.cluster_load`, you can query the load information of different nodes and hardware types of the cluster.
+ On the kernel parameter table `information_schema.cluster_systeminfo`, you can query the kernel configuration information of different nodes in the cluster. Currently, TiDB supports querying the sysctl information.
+ On the cluster log table `information_schema.cluster_log`, you can query cluster logs. By pushing the query condition to each node, the impact of the query on cluster performance is less than that of the grep command.

On the system tables before v4.0, you can only view the current node. TiDB v4.0 adds the corresponding cluster tables and you can have a global view of the entire cluster on a single TiDB node. These tables are currently in `information_schema`, and the query method is the same as other `information_schema` system tables.

## Cluster monitoring tables

For you to dynamically observe and compare cluster conditions in different time periods, the SQL diagnosis system adds cluster monitoring system tables. All monitoring tables are in `metrics_schema`, and you can query the monitoring information SQL statements. Using this method, you can perform correlated queries on all monitoring information of the entire cluster and compare the results of different time periods to quickly identify performance bottlenecks.

+ `information_schema.metrics_tables`: Because many system tables exist now, you can query meta-information of these monitoring tables on the `information_schema.metrics_tables` table.

Because the TiDB cluster has many monitoring metrics, TiDB provides the following monitoring summary tables since v4.0:

+ The monitoring summary table `information_schema.metrics_summary` summarizes all monitoring data to for you to check each monitoring metric with higher efficiency.
+ The monitoring summary table `information_schema.metrics_summary_by_label` also summarizes all monitoring data, but this table performs differentiated statistics according to different labels.

## Automatic diagnosis

On the above cluster information tables and cluster monitoring tables, you need to manually execute SQL statements of a certain mode to troubleshoot the cluster. For you to have a better user experience, TiDB provides diagnosis-related system tables based on the existing basic information tables, so that the diagnosis is automatically executed. The following are the system tables related to the automatic diagnosis:

+ The diagnosis result table `information_schema.inspection_result` displays the diagnosis result of the system. The diagnosis is passively triggered. Executing `select * from inspection_result` triggers all diagnostic rules to diagnose the system, and the faults or risks in the system are displayed in the results.
+ The diagnosis summary table `information_schema.inspection_summary` summarizes the monitoring information of a specific link or module. You can troubleshoot and locate problems based on the context of the entire module or link.
