---
title: TiDB Cloud Release Notes in 2025
summary: Learn about the release notes of TiDB Cloud in 2025.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2025

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2025.

## June 24, 2025

**General changes**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) database audit logging (beta) is now available upon request. This feature lets you record a history of user access details (such as any SQL statements executed) in logs.

    To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for TiDB Cloud Serverless database audit logging" in the Description field and click **Submit**.

    For more information, see [TiDB Cloud Serverless Database Audit Logging](/tidb-cloud/serverless-audit-logging.md).

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) supports user-controlled log redaction.

    You can now enable or disable log redaction for your TiDB Cloud Dedicated clusters to manage the redaction status of cluster logs by yourself.

    For more information, see [User-Controlled Log Redaction](/tidb-cloud/tidb-cloud-log-redaction.md).

- Encryption at Rest with Customer-Managed Encryption Keys (CMEK) is now generally available (GA) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS.

    This feature enables you to secure your data at rest by leveraging a symmetric encryption key that you manage through Key Management Service (KMS).

    For more information, see [Encryption at Rest Using Customer-Managed Encryption Keys](/tidb-cloud/tidb-cloud-encrypt-cmek.md).

## June 17, 2025

**General changes**

- For [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters, the maximum storage size of TiKV nodes with 16 vCPU and 32 vCPU is changed from **6144 GiB** to **4096 GiB**. 

    For more information, see [TiKV node storage size](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size).

**Console changes**

- Revamp the left navigation pane to improve the overall navigation experience.
  
    - A new <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> icon is now available in the upper-left corner, letting you easily hide or show the left navigation pane whenever you need.
    - A combo box is now available in the upper-left corner, letting you quickly switch between organizations, projects, and clusters, all from one central location.
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - The entries shown on the left navigation pane now dynamically adapt to your current selection in the combo box, helping you focus on the most relevant functionalities.
    - For your quick access, **Support**, **Notification**, and your account entries are now consistently displayed at the bottom of the left navigation pane on all console pages.

## June 4, 2025

**General changes**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) on Microsoft Azure is now available in public preview. 
  
    With this launch, TiDB Cloud now supports all three major public cloud platforms — AWS, Google Cloud, and Azure, which enables you to deploy TiDB Cloud Dedicated clusters wherever best fits your business needs and cloud strategy.
  
    - All core features available on AWS and Google Cloud are fully supported on Azure.
    - Azure support is currently available in three regions: East US 2, Japan East, and Southeast Asia, with more regions coming soon.
    - TiDB Cloud Dedicated clusters on Azure require TiDB version v7.5.3 or later.
  
  To quickly get started with TiDB Cloud Dedicated on Azure, see the following documentation:
  
    - [Create a TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/create-tidb-cluster.md)
    - [Connect a TiDB Cloud Dedicated Cluster via Azure Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md) 
    - [Import Data into TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/import-csv-files.md)

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.4](https://docs.pingcap.com/tidb/stable/release-8.5.4/) to [v8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/).
