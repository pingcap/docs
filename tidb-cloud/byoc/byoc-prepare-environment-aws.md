---
title: Prepare Your BYOC Environment in AWS
summary: Instructions for preparing the necessary infrastructure components for TiDB Cloud BYOC deployment.
---

# Prepare Your BYOC Environment in AWS

Before initiating the BYOC deployment, prepare the required infrastructure components in your AWS environment. Complete the following steps in order.

## Step 1. Retrieve TiDB Cloud Organization ID

Unique identifier for your organization within TiDB Cloud.

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).

    If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up. You can sign up with an email and password to manage TiDB Cloud credentials, or use single sign-on (SSO) via Google, GitHub, or Microsoft accounts.

2. In the left navigation pane, click your profile icon > **Organization Settings**.

3. Under **Organization Information**, copy the **Organization ID** and save it for later use.

## Step 2. Prepare an AWS account

We strongly recommend using a **dedicated AWS account** for your BYOC environment to ensure isolation, simplified compliance, and accurate cost management.

- **Account ID:** Ensure you have the 12-digit AWS Account ID ready.
- **Permissions:** Ensure you have AdministratorAccess or equivalent privileges to configure IAM roles and Route 53.

## Step 3. Select region and availability zones (AZs)

TiDB is a distributed database that requires specific infrastructure for high availability.

1. **Region:** Select the AWS Region where the database will be deployed.
2. **Availability zones (AZs):** Depending on your deployment goal, choose one of the following configurations:

    - **Option A: Production Environment (Multi-AZ).** You **must** identify at least **3 AZs** in your selected region. For example, `us-west-2a`, `us-west-2b`, `us-west-2c`.

    - **Option B: POC / Cost Optimization (Single-AZ).** Select exactly **1 AZ**. For example, `us-west-2a`.

The availability zones prepared for the BYOC region determine where TiDB Cloud places resource pools. When creating a resource pool, you select either **Zonal** or **Regional** high availability. A zonal resource pool is placed in one availability zone. A regional resource pool requires at least three eligible availability zones in the region.

If the BYOC region is initially prepared with a single availability zone, TiDB Cloud uses that availability zone for Zonal resource pools. You can create a Regional resource pool only when two additional eligible availability zones are available. If you plan to use Regional resource pools, confirm during environment preparation that the region can provide at least three eligible availability zones.

## Step 4. Create a hosted zone for TiDB

Create one Amazon Route 53 hosted zone for TiDB service DNS. You do not need to provide a hosted zone for observability (O11Y).

Choose one of the following hosted zone types:

- **Public hosted zone:** supports public and private connections to TiDB. Follow [Creating a public hosted zone in AWS documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html).
- **Private hosted zone:** supports private connections only. If you choose a private hosted zone, public connection is not available for the BYOC environment. Follow [Working with private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html).

For the TiDB hosted zone, use a name of no more than 38 characters. For example, `byoc.cluster.example.com`.

For a public hosted zone, delegate the zone from its parent domain by adding the Route 53 name server (NS) records to the parent DNS configuration. For a private hosted zone, associate the hosted zone with the VPCs that require DNS resolution.

> **Note:**
>
> If you plan to deploy TiDB Cloud BYOC in multiple AWS regions, you can share the same TiDB hosted zone across all regions or use a dedicated hosted zone for each region. See [Multi-Region Deployment](/tidb-cloud/byoc/multi-region-deployment.md) for details.

## Step 5. Set up private certificate authority (PCA)

TiDB Cloud utilizes the AWS private certificate authority (PCA) service to issue certificates and the AWS Certificate Manager (ACM) service to manage digital certificates, ensuring secure communication between internal database cluster components via mTLS.

To meet compliance requirements, TiDB Cloud BYOC integrates with a customer-provided PCA to issue identity certificates for data nodes using your enterprise's own domain. This ensures that the Root of Trust for all encrypted communications remains strictly within your organization's control.

Therefore, you must prepare a valid subordinate CA in the deployment region. The CA ARN that you provide to TiDB Cloud must be the ARN of the subordinate CA. To create and activate the subordinate CA, you need an active root CA to sign its certificate.

The subordinate CA certificate must be valid for at least **20 years**. Make sure that the root CA used to sign the subordinate CA certificate supports this validity period.

Perform the following steps:

1. **Create a subordinate CA.** Follow [Create a private CA in AWS Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/create-CA.html).

    Configuration: select **Subordinate CA** as the CA type. Do not provide a root CA ARN to TiDB Cloud.

2. **Install the subordinate CA certificate.** Follow [Installing the CA certificate](https://docs.aws.amazon.com/privateca/latest/userguide/PCACertInstall.html).

3. **Record ARN.** Copy the **Subordinate CA ARN**.

    Example: `arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234...`

4. **Verify PCA information** from your AWS console.

<!--To confirm: image screenshot-->

> **Note:**
>
> - **For POC or cost optimization**: If you are in the Proof of Concept (POC) phase, you may choose to use Self-Signed Certificates instead of AWS Private CA to reduce costs. Contact your TiDB Cloud Support Representative directly for specific configuration instructions regarding this option.
> - **For multi-region deployment**: Similar to hosted zones, the same private certificate authority (PCA) can be shared across all regions for multi-region deployments. Alternatively, you can create a dedicated PCA for each new region. See [Multi-Region Deployment](/tidb-cloud/byoc/multi-region-deployment.md) for details.

## Step 6. Plan network CIDR ranges

Before starting the BYOC deployment, plan dedicated private CIDR ranges for observability (O11Y) infrastructure and resource pools. Use a prefix length between `/16` and `/22`.

Each BYOC deployment region has one O11Y CIDR. Resource pool CIDR is configured for each resource pool when you create it. Plan these CIDR ranges before deployment so that the BYOC environment and future resource pools can be provisioned without network conflicts.

Prepare the following information:

| Item | Description | Example |
| ----- | ----- | ----- |
| O11Y CIDR | CIDR range reserved for observability infrastructure and related services in the deployment region. | `10.1.0.0/22` |
| Resource pool CIDR | CIDR range reserved for a resource pool. Each resource pool has its own CIDR, which cannot be modified after the resource pool is created. | `10.10.0.0/16` |

**CIDR planning rules & constraints**

When planning CIDR ranges, make sure to comply with the following connectivity rules:

- **Internal isolation:** In the same region, resource pool CIDRs must not overlap with the O11Y CIDR or with one another.

- **VPC peering rule:**

    * **Cannot overlap:** The O11Y CIDR and any resource pool CIDR must not overlap with your existing application VPCs, on-premises networks, or VPN networks.
    * **Customer responsibility:** TiDB Cloud cannot detect conflicts with customer-managed networks. You are responsible for planning and verifying these CIDR ranges before deployment or before creating a resource pool.

- **Cross-region CIDR planning:** Resource pool CIDRs in different regions can overlap. However, use non-overlapping CIDRs for resource pools that require cross-region connectivity or replication.

- **Cross-resource pool replication (critical):** If you plan to deploy multiple resource pools and might need to **replicate data between instances in different resource pools** (for example, using TiCDC for disaster recovery or data consolidation), their respective resource pool CIDR ranges **must not overlap**.

Provide the planned CIDR ranges to your TiDB Cloud representative before the automated region deployment starts.

## Summary: required information

Fill out the table below with the information gathered in steps above and share it with your TiDB Cloud representative to initiate the deployment.

**Required information:**

| Category | Details to provide | Example | Comments |
| :---- | :---- | :---- | :---- |
| **TiDB Cloud Organization ID** | Unique identifier for your TiDB Cloud org | `1372813089209270552` | Step 1 |
| **AWS Account ID** | 12-digit AWS account number | `123456789012` | Step 2 |
| **AWS Region** | Region selected for deployment | `us-west-2`, `us-east-1`, `us-east-2` | Step 3. For multi-region deployment, list all regions. |
| **Availability Zones** | 3 AZs or single AZ per region (specify names and ID) | **Us-east-1:** `us-east-1a`, `use1-az1`, `us-east-1b`, `use1-az2`, `us-east-1c`, `use1-az4`; **Us-east-2:** `us-east-2a`, `use2-az1`, `us-east-2b`, `use2-az2`, `us-east-2c`, `use2-az3`; **Us-west-2:** `us-west-2a`, `usw2-az1` | Step 3. Note to meet the AZ quantity requirement for **each** selected region. |
| **Subordinate CA ARN** | AWS ACM Private CA ARN | `arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234` | Step 5. The ARN can be shared across multiple regions. |
| **Hosted Zone Name & Hosted Zone ID** | TiDB hosted zone. You can provide either a public or private hosted zone. | **Hosted TiDB zone name:** `clusters.byoc-0929.pingcap.net`; **Hosted TiDB zone ID:** `Z1039122VAY4T8UNWR8E`. | Step 4. The hosted zone can be shared across multiple regions. |
| **CIDR** | Customer-planned CIDR ranges for O11Y infrastructure and resource pools | **O11Y CIDR:** `10.1.0.0/22`; **Resource pool CIDR:** `10.10.0.0/16` | Step 6 |
| **Image Sync Region** | Region ID chosen for image synchronization | `us-west-2` | Refer to [image synchronization](/tidb-cloud/byoc/byoc-automated-deployment.md#step-1-image-synchronization) for details. |

## Review and increase AWS service quotas

AWS service quota requirements vary by customer environment. The required quota values depend on factors such as your workload size, target capacity, selected AWS region, availability mode, and expected scaling range.

During environment preparation, work with TiDB Cloud Support or your TiDB Cloud representative to calculate the required quota values for your deployment. If your current AWS service quotas are lower than the calculated requirements, request quota increases before the automated region deployment starts.

### Quota categories to review

Review the following quota categories in each target AWS region:

- **Amazon EC2 quotas**: quota values related to vCPU-based instance usage and instance families required by the deployment.
- **Amazon EBS quotas**: quota values related to the storage types and volume capacity required by the deployment.
- **Amazon EKS and scaling-related quotas**: quota values that affect EKS clusters and node scaling capacity, including EC2 capacity, Auto Scaling Group limits, and EKS managed node group limits.

### How to request a quota increase

1. Log in to the AWS Management Console.
2. Navigate to Service Quotas.
3. Search for the relevant services: Amazon EC2, Amazon EBS, and Amazon EKS.
4. Select the required quota.
5. Click **Request quota increase**.
6. Enter the target values and submit the request.

## What's next

After you have prepared the AWS environment and shared the required information with your TiDB Cloud representative, continue with [TiDB Cloud BYOC IAM Configuration](/tidb-cloud/byoc/byoc-configure-iam-permissions.md) to configure the IAM permissions required for automated region deployment.
