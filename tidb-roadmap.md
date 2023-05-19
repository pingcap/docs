---
title: TiDB Roadmap
summary: Learn about what's coming in the future for TiDB.
---

# TiDB Roadmap

This is a look into the proposed future. We will update this as we release long-term stable (LTS) releases. The purpose is to provide visibility into what is coming you can more closely follow progress, learn about key milestones as we go, and for us to get feedback as development happens. 

In the course of development, this roadmap is subject to change based on user needs and feedback. As expected, as the columns move right, the items under them are less committed. If you have a feature request or want to prioritize a feature, please file an issue on [GitHub](https://github.com/pingcap/tidb/issues).

## Rolling roadmap highlights

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>End of CY23 LTS release</th>
      <th>Mid CY24 LTS release</th>
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
            <b>GA of Partitioned-raft-kv storage engine</b><br /><i
              >PB-scale clusters, increased write velocity, faster scaling operations, and more compaction stability</i
            >
          </li>
          <br />
          <li>
            <b>Augmented replica reads</b><br /><i>
              Reduced cross-AZ data transfer costs in TiKV
            </i>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Performance optimization framework for all applicable background tasks, like DDL, TTL, and analyze cluster</b><br />
          </li>
          <br />
          <li>
            <b>GA TiFlash decoupling of compute/storage and S3 storage</b><br />
            <i>Enables more cost-effective and elastic HTAP</i>
          </li>
          <br />
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Unlimited transaction size</b>
          </li>
          <br />
          <br />
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
            <b>Resource control for background tasks</b><br />
            <i>
              Control over how background tasks can affect foreground traffic. These tasks could be imports, DDL, TTL, auto-analyze, compactions, etc.
            </i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Multi-tenancy</b>
            <br /><i
              >Resource isolation on top of resource control</i
            >
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Enhanced TiDB memory management</b>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>SQL</b>
        <br /><i>Enhance functionality and compatibility</i>
      </td>
      <td>
        <ul>
          <li>
            <b>MySQL 8.0 compatibility</b>
          </li>
          <br />
                    <li>
            <b>Unified SQL interface for import, backup/restore, and PiTR</b>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Materialized views</b>
            <br /><i>Regularly pre-computed results to boost query performance and better enable data serving use cases</i>
          </li>
          <li>
            <b>Cascades framework for optimizer</b>
            <br /><i>Improved framework for query optimization, and makes the optimizer more extensible and future-proof</i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Federated query</b>
          </li>
          <br />
          <li>
            <b>Full text search & GIS support</b>
          </li>
          <br />
          <li>
            <b>User-defined functions</b>
          </li>
          <br />
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
            <b>Distributed TiCDC single table replication</b>
            <br /><i>
              Dramatically improve TiDB-TiDB replication throughput
            </i>
          </li>
          <br />
          <li>
            <b
              >Automatic pause/resume DDL during upgrade</b
            >
            <br /><i>Ensure a smooth upgrade experience</i>
          </li>
          <br />
          <li>
            <b>TiCDC native integrations with big data systems</b>
            <br /><i
              >Snowflake, Iceburg, etc.</i
            >
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Multiple upstreams for TiCDC</b>
            <br /><i>Support N:1 TiDB to TiCDC</i>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>AI-indexing</b>
          </li>
          <br />
          <li>
            <b>Heterogeneous database migration support</b>
          </li>
          <br />
          <li>
            <b>Re-invented AI-SQL performance advisor</b>
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

These are non-exhaustive plans and are subject to change. Features might differ per service subscriptions.

### Previously delivered roadmap items

You may have been waiting on some items from the last version. Some of those are noted below. For more detail, visit the v7.1 release notes:

- Foundation of multi-tenancy framework: Resource control quotas and scheduling for resource groups
- TiCDC sink to S3 and Azure object store (GA)
- Fastest online ADD INDEX (GA)
- TiFlash late materialization (GA)
- TiFlash spill-to-disk (GA)
- SQL-based data import (GA)
- LDAP integration (GA)
- SQL audit logging enhancement (GA) (Enteprise-only)
- Partitioned raft-kv storage engine (experimental)
- General session-level plan cache (experimental)
- TiCDC distributed per table with Kafka downstream (experimental)

### Recently shipped

- [TiDB 7.1.0 Release Notes](https://docs.pingcap.com/tidb/dev/release-7.1.0)
- [TiDB 7.0.0 Release Notes](https://docs.pingcap.com/tidb/v7.0/release-7.0.0)
- [TiDB 7.0.0 Release Notes](https://docs.pingcap.com/tidb/v7.0/release-7.0.0)
- [TiDB 6.6.0 Release Notes](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)
- [TiDB 6.5.0 Release Notes](https://docs.pingcap.com/tidb/v6.5/release-6.5.0)
