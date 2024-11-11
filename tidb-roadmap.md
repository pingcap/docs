---
title: TiDB Roadmap
summary: Learn about what's coming in the future for TiDB.
---

# TiDB Roadmap

This roadmap provides a look into the proposed future. This will be continually updated as we release long-term stable (LTS) versions. The purpose is to provide visibility into what is coming, so that you can more closely follow the progress, learn about the key milestones on the way, and give feedback as the development work goes on.

In the course of development, this roadmap is subject to change based on user needs and feedback. **DO NOT** schedule your release plans according to the content of the roadmap. If you have a feature request or want to prioritize a feature, please file an issue on [GitHub](https://github.com/pingcap/tidb/issues).

> **Note:**
> 
> If not marked as GA, these features are experimental.

## Rolling roadmap highlights

<table class="ace-table" data-ace-table-col-widths="234;324;290;261"><colgroup><col width="234" /><col width="324" /><col width="290" /><col width="261" /></colgroup>
<thead>
<tr>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcnry5fhnIDrOvdPu6RhiUlLf"><strong>Category</strong></div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcnGyF5fBBYbXOsxT4uiGtk6u"><strong>End of CY24 release</strong></div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcn8AlVCcP3ct18GfSEhHMmIh"><strong>Mid of CY25 release</strong></div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcnteOZvXCYIuCUDcisZXOppb"><strong>Future releases</strong></div>
</td>
</tr>
</thead>
<tbody>
<tr>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcnnxJDQMqle8oMXdLGe3pgDg"><strong>Unmatched Scalability and Peak Performance</strong> <em>Deliver massive scalability and faster performance to support larger workloads, optimize resource utilization, and ensure superior responsiveness</em></div>
<div class="ace-line ace-line old-record-id-doxcnLikmkzPB5Ap8A4DQTXWjRe">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnv8m9lckOD3Q9yhXL1jnHBf" data-list="bullet">
<div><strong>In</strong><strong>-memory cach</strong><strong>ing in </strong><strong>TiKV</strong></div>
<div class="ace-line ace-line old-record-id-doxcncoOUnM58BGRJYtgu1CmX7g">TiKV maintains recent versions of data in memory to reduce redundant MVCC scans, thus improving performance.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnRqaYUnfpEnthZtOVlUzECh" data-list="bullet">
<div><strong>Adaptive </strong><strong>P</strong><strong>arallelism </strong><strong>f</strong><strong>or </strong><strong>S</strong><strong>tats </strong><strong>C</strong><strong>ollection</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnuoydIn1NLQq1nBu1qijiKg">Dynamically adjusts parallelism and concurrency based on hardware and node count, accelerating statistics collection.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnMxYsum2fKYh30XDtSOO0md" data-list="bullet">
<div><strong>Faster D</strong><strong>atabase </strong><strong>Restores</strong></div>
<div class="ace-line ace-line old-record-id-doxcnEVxHqcd5kz0t0NpKJnC3ce">Reduces recovery time for full database and point-in-time restores (PITR).</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn32v4qHmU5OPr6clL2yMG6e" data-list="bullet">
<div><strong>Unlimited </strong><strong>T</strong><strong>ransaction</strong><strong> Size</strong></div>
<div class="ace-line ace-line old-record-id-doxcnjnfdR0VPcKuPdfdj0BUcbb">Removes memory limits on uncommitted transactions, improving batch task success rates.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnInSFfssxoHlcSqNdo4cn0d" data-list="bullet">
<div><strong>Load-</strong><strong>B</strong><strong>ased </strong><strong>Traffic R</strong><strong>ebalanc</strong><strong>ing</strong><strong> in TiProxy(</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnlWuuz6L0BYqqPuwvSnLvze">Routes traffic based on TiDB node workloads to optimize resource utilization</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-doxcnNFCqokzu2bCwNyyYeJCFmb">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnBiF1yF56T4c9zoQHwkoHTc" data-list="bullet">
<div><strong>PD</strong><strong> Microservice </strong><strong>Router Service</strong></div>
<div class="ace-line ace-line old-record-id-doxcnQ5rb6By8WKwPMwFM7vh1Mb">Enables independent deployment, stateless(no Strong Leader) and easy scaling of Router Service(region meta query/updates) in PD, preventing PD from becoming a bottleneck for cluster resources</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnwCdXsKUSBCInmPiRxKXqun" data-list="bullet">
<div><strong>Reduced I/O for Statistics Collection</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnbGdMsVEeHBPZEP8vQby8HK">Allows users to scan only a portion of data samples on TiKV, reducing time and resource consumption for statistics collection</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnvCP8MiX6lXqEzcHolsn5Db" data-list="bullet">
<div><strong>Limit Operator Pushdown</strong></div>
<div class="ace-line ace-line old-record-id-Q3KidmZgZoesZvxM07IcbAVXnMb">Removes limitations on pushing down the Limit operator from TiDB to TiKV, enabling more efficient query processing directly at the storage layer</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn23Bpzf7YYjIjqMiMtFOHlb" data-list="bullet">
<div><strong>Cascades Optimizer Framework</strong></div>
<div class="ace-line ace-line old-record-id-doxcnlh86JoC3xnMGCFJ3e8cuQf">Introduces a mature, advanced optimizer framework, expanding the capabilities of the existing optimizer.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn9QdtbzQ5UpkJ4qLbHvB1qg" data-list="bullet">
<div><strong>Scalable </strong><strong>DDL</strong><strong> Execution Framework</strong></div>
<div class="ace-line ace-line old-record-id-doxcnvZvO1kyMJiQCf1Or4quL1d">Provides a parallel DDL execution framework to improve the performance and stability of DDL operations</div>
</li>
<li class="ace-line ace-line old-record-id-W4JwduuhxokkAPxxGUQcBOdYnBu" data-list="bullet">
<div><strong>Increased </strong><strong>TiCDC</strong><strong> Scalability</strong></div>
<div class="ace-line ace-line old-record-id-VtP3dkoiPo9r9xx5xU7cog6BnGe">Updated TiCDC architecture delivers increased scalability and performance for change data capture use cases.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-TXNud9NeooffptxqRwWcAGBPnug">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnN8rM0rSpwDt2ANmsk79V4d" data-list="bullet">
<div><strong>Table-Level Load Balancing</strong></div>
<div class="ace-line ace-line old-record-id-doxcn2rcK01jZfYffOJZTVjni6z">Optimizes data scheduling in PD based on workload distribution across Regions for each table</div>
</li>
<li class="ace-line ace-line old-record-id-doxcntAI6Fy3vqXxmzGfzhXxOoh" data-list="bullet">
<div><strong>System Table Performance Optimization</strong></div>
<div class="ace-line ace-line old-record-id-doxcnsSyAWpvIExYESmmJhUr8hc">Enhances query speed and reduces overhead for system tables with large data volumes</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnOpF40rbfemShuoQCj9PhI8" data-list="bullet">
<div><strong>Enhance the Scability of </strong><strong>Region</strong><strong> Meta Storage</strong></div>
<div class="ace-line ace-line old-record-id-UOeLdDBhWoLnd3xtmXbcSjQ9nld">Migrate region meta storage from PD to TiKV, the storage layer can scale infinitely ans easily</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-LrW2d8ayfoZjlIxfncecyvi2nwd">&nbsp;</div>
</td>
</tr>
<tr>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcnXXzaXbwLFO77T0dVWHYIrc"><strong>Advanced </strong><strong>SQL</strong><strong> Features and Flexibility</strong></div>
<div class="ace-line ace-line old-record-id-DZDpdBB2LoucOFxLc0bcyPTGnPe"><em>Cutting-edge </em><em>SQL</em><em> capabilities, improving compatibility, flexibility, and ease of use for complex queries and modern applications</em></div>
<div class="ace-line ace-line old-record-id-N5ivdKU8eolwd0xO1Y2cLWhSnNb">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcn4riHSZhYfo9cM2yB5yBI5c" data-list="bullet">
<div><strong>Vector Search Support</strong></div>
<div class="ace-line ace-line old-record-id-doxcnS5CP8wzsDpycTdtkqj6xld">Enables vector data types, indexing, and high-performance vector search, with support for mixed queries involving vector and relational data.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnx9aM13i6tPWDKxDj0u91tt" data-list="bullet">
<div><strong>Foreign Keys(</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-UHYUdrNyLoE96vxj5JFcfUUanqH">Now generally available, providing robust relational integrity</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnnhsZSf2JqcSDIbftApTnQg" data-list="bullet">
<div><strong>Global indexing on partitioned tables(GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcn3TmvJgAGBOKtzIPwnDVm4d">Removes the unique key restriction on partition keys, boosting query performance for non-partitioned columns.</div>
</li>
</ul>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcndajTGVB9RKDZRpK7w7NzQg" data-list="bullet">
<div><strong>Modifiable Column Types in Partitioned Tables</strong></div>
<div class="ace-line ace-line old-record-id-doxcnazu2gaK6Sip3EVq1QV3zTb">Allows users to change column data types in partitioned tables, even if the column is a partitioning key.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-doxcnpYjBW661Utkk88lL5bIwrb">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnVZWNfRK4sw7yLNTXWYw6cg" data-list="bullet">
<div><strong>Materialized Views Support</strong></div>
<div class="ace-line ace-line old-record-id-doxcnkvCsN5jAtL4mRcc78IEmOf">Enables materialized views to improve pre-computation, boost computational efficiency, and enhance data analysis performance.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-doxcnyZZJEpWmjiQefKPf10vv1f">&nbsp;</div>
</td>
</tr>
<tr>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcnSFN1A7CBjCYS5B0qBYtSod"><strong>Unbreakable Reliability and Always-On Availability</strong> <em>Near-zero downtime and enhanced fault tolerance to maintain uninterrupted operations and deliver a rock-solid user experience</em></div>
<div class="ace-line ace-line old-record-id-doxcnMvvswxGatG9vuKf1kMpYXb">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnJCq7f0DYq5bQHgwxuuIMKd" data-list="bullet">
<div><strong>Limit Memory for Backups</strong></div>
</li>
<li class="ace-line ace-line old-record-id-doxcnEAvWC6g4iyGZ95M6Qla6Ad" data-list="bullet">
<div><strong>Limit Memory for Statistics Collection</strong><strong> (GA)</strong></div>
</li>
<li class="ace-line ace-line old-record-id-doxcnpVEC9xx42dfzcSeUISB8zf" data-list="bullet">
<div><strong>Enhanced </strong><strong>SQL</strong><strong> Binding Management</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnb8hOcWGs9K4iLy9BY4KhPh">Simplifies creating and managing large numbers of execution plans to stabilize performance.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn16L3YYEIgvoL1oQlbAdG6p" data-list="bullet">
<div><strong>Improved Resource Group Control for Complex </strong><strong>SQL</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcn2SImV7TasCIYXK7fXGdwoe">Monitors RU usage of complex queries mid-execution to minimize system impact.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcntJNm7evgG9UABpQ4sEEgDg" data-list="bullet">
<div><strong>Automatic Resource Group Switching for Runaway Queries</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnG5LvQRsMBVMnR3lEgSSkOh">Detects runaway queries and redirects them to designated resource groups with set limits.</div>
</li>
<li class="ace-line ace-line old-record-id-AHQAdGReDoJx0ZxZC2UcmFGqnMd" data-list="bullet">
<div><strong>Limit Memory Usage for Schema Metadata</strong><strong>（GA）</strong></div>
<div class="ace-line ace-line old-record-id-HDfEdwEsEomsUWxKytOcVfQ0nUc">Enhances stability in large-scale clusters by capping memory consumption for schema metadata.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-AYOsdnBZHoRNTmxwjKQcfLOuneh">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnj0kxqnkpsAwWDLL4C0U7Sd" data-list="bullet">
<div><strong>Robust and Resilient Backup</strong></div>
<div class="ace-line ace-line old-record-id-doxcnM0PYmfaha9fhJqYfheQ4Zc">Reduces memory-related issues during backup processes, ensuring dependable data protection and availability.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn1NxjJTYJHFQkQ48WhjB0tb" data-list="bullet">
<div><strong>Optimized Memory Management with Disk Spilling</strong></div>
<div class="ace-line ace-line old-record-id-doxcncY84pbyMlyvIESOX5tLbQb">Allows operators like HashAgg, Sort, and Join to spill to disk, reducing memory load and preventing out-of-memory (OOM) issues.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnGvHL7bl7sfyWp54SyWRXJc" data-list="bullet">
<div><strong>Sharing</strong><strong> Plan Cache</strong><strong> across Sessions (</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnkmO5e8KH3wnimnT07frR2e">Shares execution plan cache across sessions in the same TiDB instance, optimizing memory usage.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnYwRmD2GnxWytSCy1C2oIby" data-list="bullet">
<div><strong>Resource Group Quota Management</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnFf8ngoxzFaCwT9cAAI6aeh">Dynamically adjusts resource limits for Burstable resource groups, fully utilizing available resources without impacting other quotas</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-doxcnCw7mLahKHeB2tgRG6GOVZg">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnABSMRPoe1U42APUlHiz0ze" data-list="bullet">
<div><strong>Adaptive Resource Group</strong></div>
<div class="ace-line ace-line old-record-id-doxcnnifWMZ9Oft70jIZki8kObn">Automatically adjusts Request Unit (RU) settings in resource groups based on past execution patterns</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnRva3R2ej1CfjWREJ3XpQGb" data-list="bullet">
<div><strong>Enhanced Memory Protection</strong></div>
<div class="ace-line ace-line old-record-id-doxcn68xXng0eDLW9hyXco2aQPb">Monitors memory usage across all components to prevent operations that could impact system stability</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnL8ctUy6pCxbRE1sIVLys4g" data-list="bullet">
<div><strong>Automatic </strong><strong>SQL</strong><strong> Binding</strong></div>
<div class="ace-line ace-line old-record-id-doxcnWJA5hTBc90reg1n50mOc4b">Analyzes SQL performance metrics to automatically create bindings, stabilizing execution plans for transactional processing</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnvtUDD5UL6ufvxDnfyPqcah" data-list="bullet">
<div><strong>Multi-Versioned Statistics</strong></div>
<div class="ace-line ace-line old-record-id-doxcnBI3M1YQUlBAjNKuMvFYaUe">Allows users to view and restore previous statistics versions after updates</div>
</li>
<li class="ace-line ace-line old-record-id-VgROdaukPow0qWxmuMrcLyHKnBd" data-list="bullet">
<div><strong>Distributed Statistics Collection</strong></div>
<div class="ace-line ace-line old-record-id-S895dIeQCoXPCJxZodXcwkornuh">Enables parallel statistics collection across multiple TiDB nodes to boost efficiency.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-BuCAdOdoKoV7bJxXa3ucfALunsh">&nbsp;</div>
</td>
</tr>
<tr>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcnbX5vwCThHj5aHOW75i1hLe"><strong>Effortless Operations and Intelligent Observability</strong> <em>Simplify management with proactive monitoring and insights to optimize performance and ensure smooth operations</em></div>
<div class="ace-line ace-line old-record-id-P7Kzd9DkkobOiHxl891cOkCPnrg">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnhTLcyywXh1WmmDCt8sAb7e" data-list="bullet">
<div><strong>Reliable Query Termination</strong><strong>（</strong><strong>GA</strong><strong>）</strong></div>
<div class="ace-line ace-line old-record-id-doxcnFlO6Jn4Fit4sOeaCBny8Pe">Instantly terminates running SQL statements and frees resources in TiDB and TiKV.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnrpMI1o0w6nLaMVikJ9u7ue" data-list="bullet">
<div><strong>Permissioned Resource Group Switching</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcn6o9TBTV58tI5aVylumI0Oc">Restricts resource group switching to authorized users, preventing resource misuse.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnKJGScfbXiixnNQEO0uWnNh" data-list="bullet">
<div><strong>CPU Time Observation for </strong><strong>TiDB</strong><strong> and </strong><strong>TiKV</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnjgvvrp2n9GcO3cALRnKSub">Adds CPU time metrics to logs, enabling quick identification of statements causing CPU spikes</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-doxcnylZ0Xr6PGZTpxj265VNCtd">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnKNOhBf2FezS2LkS89zauCd" data-list="bullet">
<div><strong>Customizable Statistics Collection</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnk0zb89UYXcUy4RaIGkx4Vh">Allows tailored statistics strategies for specific tables, adjusting parameters like health and parallelism.</div>
</li>
<li class="ace-line ace-line old-record-id-LJqGdNWM4oDun1xs4ltcudVwnxh" data-list="bullet">
<div><strong>Workload Repository</strong><strong> (</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-RPNNdYlaqoKjtYxXAH9cM7mfnPe">Stores workload stats and real-time data for improved troubleshooting and analysis.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn09Kcp51ryh6jRRDroVyc6d" data-list="bullet">
<div><strong>Automated Index Advisor</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnS51DKN75GTUzdWMFeR1hxh">Automatically analyzes SQL statements to recommend index optimizations, including suggestions for creating or dropping indexes</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnaAMAeQ6a97NyRRDsw6KPHe" data-list="bullet">
<div><strong>Standardized Time Model</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcntxyn01xoJgDonbcFXNo5Me">Establishes a unified SQL execution time model to help identify database load sources through logs and cluster metrics, pinpointing problematic nodes and statements</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnjIpqZd3BrbLfMfrbtf0Rye" data-list="bullet">
<div><strong>TiFlash</strong><strong> CPU Time Monitoring</strong><strong> (GA)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnc6dIg8OYI1dve2rmIvyb0c">Adds TiFlash CPU time metrics to logs, enabling quick identification of statements that cause CPU spikes in TiFlash</div>
</li>
</ul>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnVRICDGKDg51UFQ8UWSGmib" data-list="bullet">
<div><strong>Workload Analysis</strong></div>
<div class="ace-line ace-line old-record-id-doxcnkg4hjrJ9SWA3z2KgJJ4pMd">Analyzes historical data from the Workload Repository to provide optimization recommendations, including SQL tuning and statistics collection</div>
</li>
<li class="ace-line ace-line old-record-id-LTo3dOzKOoTPF9x9159cyinJn1d" data-list="bullet">
<div><strong>End-to-End </strong><strong>SQL</strong><strong> Monitoring</strong></div>
<div class="ace-line ace-line old-record-id-KAGNdFYHfoj1PQxAg8LcVhHvnRc">Tracks the entire lifecycle of SQL statements, measuring time spent across TiDB, TiKV, PD, and TiFlash for detailed performance insights</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-KOT2dzKDRozUunxS24ec7dnVnEd">&nbsp;</div>
</td>
</tr>
<tr>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-doxcn8YeTibezefrKtgYkUpfV2b"><strong>Comprehensive Data Security and Privacy</strong> <em>Robust security measures to safeguard sensitive data, ensuring top-tier protection, encryption, and compliance with evolving privacy regulations</em></div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnMzvwKUNRf12uCJKYWkZEIc" data-list="bullet">
<div><strong>Google Cloud KMS(</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnR51htmqPt3ZfDsxcLeyxDf">General availability for encryption-at-rest key management with Google Cloud KMS.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnsrA69D9lmqvbcQKEnGX1b5" data-list="bullet">
<div><strong>Azure</strong><strong> Key Vault</strong></div>
<div class="ace-line ace-line old-record-id-doxcnvfRtmudzTDmSIH1Vev9AFh">Enhanced encryption-at-rest key management with Azure Key Vault integration.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcna945pOERF777XsP3ojCMFd" data-list="bullet">
<div><strong>Marker-Based Log Desensitization</strong></div>
<div class="ace-line ace-line old-record-id-doxcnuRtDDi84LVyh1ierusK8Mc">Marks and selectively desensitizes sensitive data in cluster logs based on use case.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnQ3GWriYpI7Hq4qIScmYg6b" data-list="bullet">
<div><strong>Column-Level Permission Management</strong><strong>(</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-doxcn7UEOn7MGbXwlNEVkE8WVAe">Adds MySQL-compatible permissions at the column level for fine-grained access control.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-DYCudzZPjozw3dxyoYxctvrvnib">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcn8oa7RZSbknOlM8LhVYce8c" data-list="bullet">
<div><strong>AWS</strong> <strong>IAM</strong><strong> Authentication</strong></div>
<div class="ace-line ace-line old-record-id-FeJPdXnQloJ5ioxunS8cOjClnVf">Supports AWS IAM third-party ARN integration for secure access control in TiDB</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnHkATQzEeKnm2XFzgQBUzYf" data-list="bullet">
<div><strong>Kerberos Authentication</strong><strong>(</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-OPKgdwv6AoYBOfxPS41czSbcngS">Enables authentication using Kerberos for added security.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnhKQrTvTXg0f9xa6qEpANVf" data-list="bullet">
<div><strong>Multi-Factor Authentication (MFA)</strong></div>
<div class="ace-line ace-line old-record-id-GmH4d0afwo0YY0xoMxacAjt9n4f">Adds support for multi-factor authentication to enhance user verification the multi-factor authentication mechanism.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnXD09i2C3P4dot8VIyqbDBd" data-list="bullet">
<div><strong>Enhanced </strong><strong>TLS</strong><strong> Security</strong><strong>(</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnv1qdu2EQor5BrhXFIFo3bg">Ensures encrypted connections between all components within the TiDB cluster</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnTf7r0nXImFnuqCOoFAhZvf" data-list="bullet">
<div><strong>Refined Dynamic Privileges</strong></div>
<div class="ace-line ace-line old-record-id-doxcnbMayn57z7lfrro4J7yY8wc">Improves dynamic privilege management, including limitations on Super privilege</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn69LomkHh9C7exTLEXPJ9Xd" data-list="bullet">
<div><strong>FIPS Compliance</strong><strong>(</strong><strong>GA</strong><strong>)</strong></div>
<div class="ace-line ace-line old-record-id-doxcnbpFd3sKuKZ5uRVyTpVublc">Ensures encryption methods comply with FIPS standards for secure data handling.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-doxcnX1wExSTPXM2B5SXGGf82Bh">&nbsp;</div>
</td>
<td style="vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-doxcnnOUbZabHVinM7Lq7pSzZYg" data-list="bullet">
<div><strong>Label-Based Access Control</strong></div>
<div class="ace-line ace-line old-record-id-Ep8RdlorcoW0OKxMdaQchJiOnRb">Enables data access control through configurable labels.</div>
</li>
<li class="ace-line ace-line old-record-id-doxcnMF150Vf2VL3dHEJYyjFoOe" data-list="bullet">
<div><strong>Enhanced Client-Side Encryption</strong></div>
<div class="ace-line ace-line old-record-id-EVP5dEgwRoHf04xD6CHclV7An5d">Supports encryption of key fields on the client side to strengthen data security</div>
</li>
<li class="ace-line ace-line old-record-id-doxcn1OTa1saqRHyW8pylf92a2c" data-list="bullet">
<div><strong>Dynamic Data Desensitization</strong></div>
<div class="ace-line ace-line old-record-id-L2YZdV3veoZjRoxC3KvccRQ0nAc">Allows data desensitization based on application scenarios, protecting sensitive business fields</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-GjnLdE3I4oHSUYx6lc5cSNrsnZf">&nbsp;</div>
</td>
</tr>
</tbody>
</table>

> **Note:**
>
> These are non-exhaustive plans and are subject to change. Features might differ per service subscriptions.