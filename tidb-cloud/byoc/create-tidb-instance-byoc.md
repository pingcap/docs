---
title: Create a {{{ .byoc }}} Instance
summary: Learn how to create a {{{ .byoc }}} instance.
---

# Create a {{{ .byoc }}} Instance

This document describes how to create a {{{ .byoc }}} instance in the [TiDB Cloud console](https://tidbcloud.com/).

TiDB Cloud BYOC (Bring Your Own Cloud) keeps the control plane in TiDB Cloud while deploying the data plane in your own cloud account. Before you create a BYOC instance, your organization must complete BYOC onboarding and prepare the target cloud environment.

In TiDB Cloud BYOC, a resource pool provides the underlying physical resources, network, and capacity for BYOC instances. Before you create a BYOC instance, you must have an active resource pool in the target cloud provider and region.

> **Note:**
>
> To learn how to create a {{{ .premium }}} instance, see [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md).

## Before you begin

If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

Before you create a BYOC instance, make sure that the following requirements are met:

- You have the required organization or project role to create TiDB Cloud resources.
- Your organization has completed the prerequisite BYOC setup for the target cloud provider and region, including the required cloud account permissions. For AWS, this includes the IAM roles required by TiDB Cloud to deploy and manage BYOC resources in your AWS account.
- An active resource pool exists in the cloud provider and region where you want to deploy the BYOC instance.

If your BYOC environment is not ready, the **Bring Your Own Cloud** tab is not displayed on the **Create Resource** page. To enable BYOC for your organization, contact your TiDB Cloud account team or [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

If no suitable resource pool is available, an `Organization Owner` can create one from **BYOC Management** > **Resource Pools** or from the instance creation workflow. Other roles cannot create resource pools. For more information, see [Create a Resource Pool](/tidb-cloud/byoc/create-resource-pool-byoc.md).

## Steps

If you have the required permissions, you can create a {{{ .byoc }}} instance as follows:

1. In the [TiDB Cloud console](https://tidbcloud.com/tidbs), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click **Create Resource** in the upper-right corner.

2. On the **Create Resource** page, click the **Bring Your Own Cloud** tab.

3. Confirm that **BYOC** is selected as your plan.

    BYOC is powered by TiDB X and is designed for large-scale production workloads. It lets you run the data plane in your own cloud account while using TiDB Cloud for automated operations, elastic scalability, and enterprise-grade security.

4. In the **Basic Settings** area, enter a name for your {{{ .byoc }}} instance, and then choose a cloud provider and a region where you want to host your instance.

5. (Optional) To group this {{{ .byoc }}} instance in a project for management, select the target project for the instance.

6. In the **Resource Pool** area, select an active resource pool.

    Only resource pools that match the selected cloud provider and region and are in the **Active** status are displayed. If no suitable resource pool is available and you are an `Organization Owner`, click **Create Resource Pool** to create one. After the resource pool becomes active, it is automatically selected for the new instance.

7. In the **Capacity** area, set the maximum number of Request Capacity Units (RCUs) for your instance. RCUs represent the compute resources provisioned for your workload. TiDB Cloud automatically scales your instance within this range based on demand.

8. For {{{ .byoc }}} instances, the high availability mode is inherited from the selected resource pool. If the resource pool uses Regional high availability, the instance uses Regional high availability. If the resource pool uses Zonal high availability, the instance uses Zonal high availability. You cannot configure the high availability mode when you create a BYOC instance. For more information, see [TiDB Cloud BYOC architecture](/tidb-cloud/architecture-concepts.md#tidb-cloud-byoc).

9. Click **Create**.

    The instance creation process begins. Provisioning time can vary depending on the region, capacity, and cloud provider you select.

## What's next

After your BYOC instance is created, you can do the following:

- Set or reset the root password for the instance if it has not been configured.
- Configure network access from your application environment to the instance endpoint.
- Connect to the instance from your application or SQL client.
