---
title: Select a Plan
summary: Learn how to select a plan on TiDB Cloud.
aliases: ['/tidbcloud/developer-tier-cluster']
---

# Select Your Plan

The plan determines the throughput and performance of your TiDB resource.

TiDB Cloud provides the following options of plans. Whether you are just getting started or scaling to meet the increasing application demands, these service plans provide the flexibility and capability you need. Before creating a TiDB resource, you need to consider which option suits your need better.

- [TiDB Cloud Starter](#starter)
- [{{{ .essential }}}](#essential)
- [TiDB Cloud Dedicated](#tidb-cloud-dedicated)
- [ {{{ .premium }}}](#premium)

> **Note:**
>
> Some of TiDB Cloud features are partially supported or not supported on {{{ .starter }}} and {{{ .essential }}}. See [{{{ .starter }}} and Essential Limitations](/tidb-cloud/serverless-limitations.md) for details.

## {{{ .starter }}} {#starter}

TiDB Cloud Starter is a fully managed, multi-tenant TiDB offering. It delivers an instant, autoscaling MySQL-compatible database and offers a generous free quota and consumption based billing once free limits are exceeded.

The free plan is ideal for those who are getting started with {{{ .starter }}}. It provides developers and small teams with the following essential features:

- **No cost**: This plan is completely free, with no credit card required to get started.
- **Storage**: Provides an initial 5 GiB of row-based storage and 5 GiB of columnar storage.
- **Request Units**: Includes 50 million [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) for database operations.

### Usage quota

For each organization in TiDB Cloud, you can create a maximum of five free {{{ .starter }}} instances by default. To create more {{{ .starter }}} instances, you need to add a credit card and specify a spending limit.

For the first five {{{ .starter }}} instances in your organization, whether they are free or scalable, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- Columnar storage: 5 GiB
- Request Units (RUs): 50 million RUs per month

A Request Unit (RU) is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified.

Once a {{{ .starter }}} instance reaches its usage quota, it immediately denies any new connection attempts until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) or the usage is reset upon the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling. For example, when the row-based storage of a {{{ .starter }}} instance exceeds 5 GiB for a free {{{ .starter }}} instance, the instance automatically restricts any new connection attempts.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/).

## {{{ .essential }}} {#essential}

For applications experiencing growing workloads and needing scalability in real time, the Essential plan provides the flexibility and performance to keep pace with your business growth with the following features:

- **Enhanced capabilities**: includes all capabilities of the Starter plan, along with the capacity to handle larger and more complex workloads, as well as advanced security features.
- **Automatic scaling**: automatically adjusts storage and computing resources to efficiently meet changing workload demands.
- **High availability**: built-in fault tolerance and redundancy ensure your applications remain available and resilient, even during infrastructure failures.
- **Predictable pricing**: billed based on storage and Request Capacity Units (RCUs) of the compute resources, offering transparent, usage-based pricing that scales with your needs, so you only pay for what you use without surprises.

## User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

For each {{{ .starter }}} or {{{ .essential }}} instance, TiDB Cloud generates a unique prefix to distinguish it from other instances.

Whenever you use or set a database user name, you must include the prefix in the user name. For example, assume that the prefix of your {{{ .starter }}} or {{{ .essential }}} instance is `3pTAoNNegb47Uc8`.

- To connect to your {{{ .starter }}} or {{{ .essential }}} instance:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **Note:**
    >
    > {{{ .starter }}} and {{{ .essential }}} require TLS connection. To find the CA root path on your system, see [Root certificate default path](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path).

- To create a database user:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

To get the prefix for your {{{ .starter }}} or {{{ .essential }}} instance, take the following steps:

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.
2. Click the name of your target {{{ .starter }}} or Essential instance to go to its overview page, and then click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the dialog, get the prefix from the connection string.

## {{{ .premium }}} {#premium}

For mission-critical enterprise workloads requiring hyper-scale and the highest levels of performance, the Premium plan delivers a true cloud-native experience with the following features:

- **Instant elasticity**: handles massive and unpredictable traffic spikes by scaling computing resources automatically, ensuring zero performance bottlenecks during peak demands.
- **Unlimited growth**: architected for virtually unlimited expansion in both storage and throughput, allowing your database to scale seamlessly alongside your business without physical infrastructure constraints.
- **Zero-infrastructure management**: provides a fully managed, "zero-touch" operational experience, eliminating the complexity of manual scaling, patching, or capacity planning.
- **Predictable pricing**: billed based on storage and Request Capacity Units (RCUs), offering transparent, usage-based pricing that scales with your needs, so you only pay for what you use without surprises.
- **Advanced security and compliance**: incorporates our most stringent security standards, including advanced encryption, CMEK, private networking options, and comprehensive compliance certifications to protect your most sensitive data.

## TiDB Cloud Dedicated

TiDB Cloud Dedicated is for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For TiDB Cloud Dedicated clusters, you can customize the cluster size of TiDB, TiKV, and TiFlash easily according to your business need. For each TiKV node and TiFlash node, the data on the node is replicated and distributed in different availability zones for [high availability](/tidb-cloud/high-availability-with-multi-az.md).

To create a TiDB Cloud Dedicated cluster, you need to [add a payment method](/tidb-cloud/tidb-cloud-billing.md#payment-method) or [apply for a Proof of Concept (PoC) trial](/tidb-cloud/tidb-cloud-poc.md).

> **Note:**
>
> You cannot decrease the node storage after your TiDB Cloud Dedicated cluster is created.
