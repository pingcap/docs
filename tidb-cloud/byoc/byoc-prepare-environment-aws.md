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

        > **Note:**
        >
        > Multi-AZ deployment functionality is disabled for this configuration.

## Step 4. Create hosted zones for TiDB and observability (O11Y)

You need to create two separate **public hosted zones** in Amazon Route 53.

1. **Create the Zones.**

    Follow the [Creating a public hosted zone in AWS documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html) to create the following:

    - **TiDB Cluster Zone:** Manages DNS for the TiDB Service.

        * Naming Constraint: Max 38 characters.
        * Example: `byoc.cluster.example.com`.

    - **Observability (O11y) Zone:** Manages DNS for monitoring tools (Grafana/Prometheus).

        * Naming Constraint: Max 34 characters.
        * Example: `o11y.cluster.example.com`.

2. **Delegate DNS.**

    > **Important:**
    >
    > **DNS Delegation Required.** After creating the hosted zones, you **must** add Route 53 Name Servers (NS records) to your parent domain's DNS configuration (for example, in your corporate DNS or parent AWS zone).

    - **Action:** Copy the 4 NS records from your new Route 53 zones and add them to the parent domain.
    - **Result:** Without this, internal service discovery will fail.

3. **Verify the DNS delegation.**

    Verify the DNS delegation by running `nslookup` or `dig` from any internet-connected command-line environment. The domain must resolve correctly.

    ```bash
    nslookup -type=ns {hosted_zone_name}
    nslookup -type=ns byoc-tidb.cluster.example.com
    nslookup -type=ns o11y.cluster.example.com
    ```

    <!--To confirm: whether to add image-->

    > **Note:**
    >
    > If you plan to deploy TiDB Cloud BYOC in **multiple AWS regions**, the same hosted zones can be shared across all regions, or you can choose to create dedicated hosted zones per region. See [Multi-Region Deployment](/tidb-cloud/byoc/multi-region-deployment.md) for detailed multi-region architecture configurations.

## Step 5. Set up private certificate authority (PCA)

TiDB Cloud utilizes the AWS private certificate authority (PCA) service to issue certificates and the AWS Certificate Manager (ACM) service to manage digital certificates, ensuring secure communication between internal database cluster components via mTLS.

To meet compliance requirements, TiDB Cloud BYOC integrates with a customer-provided PCA to issue identity certificates for data nodes using your enterprise's own domain. This ensures that the Root of Trust for all encrypted communications remains strictly within your organization's control.

Therefore, you must prepare a valid Subordinate CA in the deployment region. Please follow the steps below:

1. **Create a CA.** Follow [Create a private CA in AWS Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/create-CA.html).

    Configuration: Ensure the validity period is set to at least **20 years**.

2. **Install the CA certificate.** Follow [Installing the CA certificate](https://docs.aws.amazon.com/privateca/latest/userguide/PCACertInstall.html).

    Prerequisite: You must have an active Root CA.

3. **Record ARN.** Copy the **Subordinate CA ARN**.

    Example: `arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234...`

4. **Verify PCA information** from your AWS console.

<!--To confirm: image screenshot-->

> **Note:**
>
> - **For POC or cost optimization**: If you are in the Proof of Concept (POC) phase, you may choose to use Self-Signed Certificates instead of AWS Private CA to reduce costs. Contact your TiDB Cloud Support Representative directly for specific configuration instructions regarding this option.
> - **For multi-region deployment**: Similar to hosted zones, the same private certificate authority (PCA) can be shared across all regions for multi-region deployments. Alternatively, you can create a dedicated PCA for each new region. See [Multi-Region Deployment](/tidb-cloud/byoc/multi-region-deployment.md) for details.

## Step 6. Plan network CIDR ranges

Before starting the BYOC deployment, plan dedicated CIDR ranges for the TiDB cluster and observability (O11Y) infrastructure. This planning must be evaluated on a **per-region** basis.

The CIDR ranges will be used by TiDB Cloud to provision the required AWS networking resources for the BYOC environment.

Prepare the following information:

| Item | Description | Example |
| ----- | ----- | ----- |
| TiDB Cluster CIDR | CIDR range reserved for TiDB cluster and dataplane resources. | `10.10.0.0/16` |
| O11Y CIDR | CIDR range reserved for observability infrastructure and related services. | `10.20.0.0/16` |

When planning the CIDR ranges, ensure that:

**CIDR Planning Rules & Constraints:** When planning the CIDR ranges, ensure you strictly follow these connectivity rules:

1. **Internal Isolation:** The TiDB Cluster CIDR and O11Y CIDR within the same environment must not overlap with each other.

2. **VPC Peering Rule:**

    * **Cannot Overlap:** Anything that will be peered *cannot* overlap. If you plan to establish VPC Peering between the TiDB Cluster VPC and your existing application VPCs, on-premises networks, or VPNs, the CIDR ranges must be strictly de-conflicted.
    * **Can Overlap:** Things that will *never* be peered can safely overlap with the TiDB Cloud BYOC environment.

3. **Cross-Cluster Replication (Critical):** If you plan to deploy multiple TiDB clusters (whether in the same region or across different regions) and eventually want to **replicate data between them** (for example, using TiCDC for Disaster Recovery or data consolidation), their respective TiDB Cluster CIDR ranges **must be de-conflicted**.

Provide the planned CIDR ranges to your TiDB Cloud representative before the automated deployment starts.

## Summary: Required information

Fill out the table below with the information gathered in steps above and share it with your TiDB Cloud representative to initiate the deployment.

**Required information:**

| Category | Details to provide | Example | Comments |
| :---- | :---- | :---- | :---- |
| **TiDB Cloud Organization ID** | Unique identifier for your TiDB Cloud org | `1372813089209270552` | Step 1 |
| **AWS Account ID** | 12-digit AWS account number | `123456789012` | Step 2 |
| **AWS Region** | Region selected for deployment | `us-west-2`, `us-east-1`, `us-east-2` | Step 3. For multi-region deployment, list all regions. |
| **Availability Zones** | 3 AZs or single AZ per region (specify names and ID) | **Us-east-1:** `us-east-1a`, `use1-az1`, `us-east-1b`, `use1-az2`, `us-east-1c`, `use1-az4`; **Us-east-2:** `us-east-2a`, `use2-az1`, `us-east-2b`, `use2-az2`, `us-east-2c`, `use2-az3`; **Us-west-2:** `us-west-2a`, `usw2-az1` | Step 3. Note to meet the AZ quantity requirement for **each** selected region. |
| **Subordinate CA ARN** | AWS ACM Private CA ARN | `arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234` | Step 5. The ARN can be shared across multiple regions. |
| **Hosted Zone Names & Host Zone ID** | TiDB Cluster Zone, Observability (O11Y) Zone | **Hosted TiDB cluster zone name:** `clusters.byoc-0929.pingcap.net`; **Hosted TiDB cluster zone ID:** `Z1039122VAY4T8UNWR8E`. **Hosted O11Y zone name:** `o11y.byoc-0929.pingcap.net`; **Hosted O11Y zone ID:** `Z10389823CTXFNM7VG79P`. | Step 4. The zone names and IDs can be shared across multiple regions. |
| **CIDR** | Customer-planned CIDR range for the TiDB cluster, Customer-planned CIDR range for the O11Y cluster | **TiDB cluster CIDR:** `10.10.0.0/16`; **O11Y cluster CIDR:** `10.20.0.0/16` | Step 6 |
| **Image Sync Region** | Region ID chosen for image synchronization | `us-west-2` | Refer to [image synchronization](/tidb-cloud/byoc/byoc-automated-deployment.md#deployment-process) for details. |

## Review and increase AWS service quotas

<!--To confirm: need to update-->

### Recommended Quota Limits

You can request quota increases for the following resources in your target AWS region:

* **Amazon EC2 (vCPU-based quotas):** Increase relevant instance family quotas (e.g., Standard instances) to support up to 1024 vCPUs.
* **Amazon EBS (gp3 storage):** Increase General Purpose (gp3) volume storage quota to 150 TiB.
* **Amazon EKS / Cluster Scaling Capacity:** Ensure the environment supports scaling to at least 40 worker nodes, including:
    * EC2 capacity
    * Auto Scaling Group limits
    * EKS managed node group limits

### How to Request a Quota Increase

1. Log in to the AWS Management Console.
2. Navigate to Service Quotas.
3. Search for the relevant services: Amazon EC2， Amazon EBS，Amazon EKS
4. Select the required quota.
5. Click Request quota increase.
6. Enter the target values and submit the request.
