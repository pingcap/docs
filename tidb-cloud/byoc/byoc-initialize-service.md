---
title: Create Your First TiDB Cloud BYOC Instance
summary: This document outlines the process for creating a TiDB Cloud BYOC instance and setting up secure access.
---

# Create Your First TiDB Cloud BYOC Instance

After deploying your BYOC infrastructure, create a resource pool, create your first {{{ .byoc }}} instance in the resource pool, and configure secure administrative access.

## Create a BYOC instance

You can now provision resource pools and TiDB instances directly via the TiDB Cloud console.

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and then follow the instructions in [Create a Resource Pool](/tidb-cloud/byoc/create-resource-pool-byoc.md) to create a resource pool in the target cloud provider and region. 

    >**Note:**
    >
    > When creating the resource pool, select **Zonal** or **Regional** high availability based on your workload requirements. {{{ .byoc }}} instances created or restored in the resource pool inherit the high availability mode of the pool.

2. After the resource pool becomes **Active**, follow the instructions in [Create a {{{ .byoc }}} Instance](/tidb-cloud/byoc/create-tidb-instance-byoc.md) to create a new instance in the resource pool.

    * Initial setup time: creating the **first resource pool** in a region might take approximately **1 hour** as the system initializes the Kubernetes environment.
    * Subsequent instances: creating additional instances in an active resource pool usually takes only a few minutes.

3. Consult with your TiDB Cloud representative to determine the appropriate Request Unit (RU) settings for your initial connectivity and functional tests. They will recommend a configuration based on your specific testing requirements.

## Restore data from Amazon S3 to a new BYOC instance

After preparing your backup file in Amazon S3, you can restore the data to a new {{{ .byoc }}} instance in an active resource pool.

1. Configure Amazon S3 Access (AK/SK).

    To allow TiDB Cloud to read your S3 backup, you must configure external storage access by generating an AWS Access Key ID and Secret Access Key (AK/SK) with the appropriate S3 read permissions.

    For detailed instructions, see [Configure Amazon S3 access using an AWS Access Key](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access-using-an-aws-access-key).

2. Execute the restore process.

    Once the access keys are configured, you can initiate the restore job from the TiDB Cloud console.

    During restore, select an active resource pool with sufficient vCPU capacity in the target cloud provider and region. The restored instance inherits the high availability mode of the selected resource pool.

    If the selected resource pool has reached its Pool vCPU Limit, increase or turn off the limit, or select another resource pool before continuing. This is because restoring to a new {{{ .byoc }}} instance might cause the total provisioned vCPUs to exceed the Pool vCPU Limit and affect the performance of all {{{ .byoc }}} instances in the same pool.

    For step-by-step restoration procedures, see [Restore backups from cloud storage](/tidb-cloud/premium/backup-and-restore-premium.md#restore-backups-from-cloud-storage).

## Configure secure administrative access

To enable TiDB Cloud Support to assist with troubleshooting and observability, you can configure a secure access channel by deploying a hardened bastion host within your VPC.

> **Note:**
>
> - This step is **optional**. You may choose to provide your own secure login method for maintenance.
> - The Bastion Host is used only for troubleshooting and does not need to maintain a persistent connection. You may terminate this channel at any time.

For deployment and verification steps, see [Configure a Bastion Host for {{{ .byoc }}}](/tidb-cloud/byoc/byoc-configure-bastion-host.md).

## What's next

After you create your first resource pool and {{{ .byoc }}} instance and configure secure administrative access, continue with [TiDB Cloud BYOC Joint Validation](/tidb-cloud/byoc/joint-validation.md) to validate connectivity, observability, security, and alerting.
