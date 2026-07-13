---
title: Prepare Your BYOC Environment
summary: Instructions for preparing the necessary infrastructure components for TiDB Cloud BYOC deployment.
---

# Prepare Your BYOC Environment

Before initiating the deployment, specific infrastructure components must be prepared in your AWS environment. Follow the steps below in order:

## Step 1. Retrieve TiDB Cloud Tenant ID

Unique identifier for your organization within TiDB Cloud.

1. Log in to the [TiDB Cloud Console](https://tidbcloud.com/).

    If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up.* *You may sign up with an email/password to manage TiDB Cloud credentials, or use single sign-on (SSO) via google, Github, or Microsoft accounts.

2. Navigate to **Organization Settings** (Click your profile icon > **Organization Settings**).
3. Under **Organization Overview**, copy the **Organization ID**.

    Save this for Table 2-1. (e.g. tenant ID: 1372813089209270552*).

## Step 2. Prepare an AWS Account

We strongly recommend using a **dedicated AWS account** for the BYOC environment to ensure isolation, simplified compliance, and accurate cost management.

- **Account ID:** Ensure you have the 12-digit AWS Account ID ready.
- **Permissions:** Ensure you have AdministratorAccess or equivalent privileges to configure IAM roles and Route 53\.

## Step 3. Select Region and Availability Zones (AZs)

TiDB is a distributed database that requires specific infrastructure for high availability.

1. **Region:** Select the AWS Region where the database will be deployed.
2. **Availability Zones:** Depending on your deployment goal, choose one of the following configurations:

    - **Option A: Production Environment (Multi-AZ):**  You **must** identify at least **3 Availability Zones (AZs)** in your selected region.

    *Example:* us-west-2a, us-west-2b, us-west-2c

        ![][image3]

    - **Option B: POC / Cost Optimization (Single-AZ)** : Please select exactly **1 Availability Zone (AZ)**.
      * Note: Multi-AZ deployment functionality is disabled for this configuration
      * *Example*: `us-west-2a`

## Step 4. Create Hosted Zones for TiDB and Observability (O11Y)

You are required to create two separate **Public Hosted Zones** in Amazon Route 53\.

**A. Create the Zones** Follow the [AWS Documentation: Creating a Hosted Zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html) to create the following:

1. **TiDB Cluster Zone:** Manages DNS for the TiDB Service.

* *Naming Constraint:* Max 38 characters.

* *Example:* [byoc.cluster.example.com](http://byoc.cluster.example.com)

2. **Observability (O11y) Zone:** Manages DNS for monitoring tools (Grafana/Prometheus).

* *Naming Constraint:* Max 34 characters.

* *Example:* o11y.cluster.example.com

**B. Delegate DNS (Critical Step)**

| ⚠️ IMPORTANT: DNS Delegation Required After creating the hosted zones, you must add Route 53 Name Servers (NS records) to your parent domain's DNS configuration (e.g., in your corporate DNS or parent AWS zone). Action: Copy the 4 NS records from your new Route 53 zones and add them to the parent domain. Result: Without this, internal service discovery will fail. |
| :---- |

**C. Verification** Verify the DNS delegation by running `nslookup` or `dig` from any internet-connected command-line environment. The domain must resolve correctly.

| \# nslookup \-type=ns {hosted\_zone\_name}
nslookup \-type=ns byoc-tidb.cluster.example.com
nslookup \-type=ns o11y.cluster.example.com |
| :---- |

![][image4]

| Note for Multi-Region Deployment:  If you plan to deploy TiDB Cloud BYOC in multiple AWS regions, the same hosted zones can be shared across all regions, or you can choose to create dedicated hosted zones per region. Please refer to Section 7 for detailed multi-region architecture configurations. |
| :---- |

## Step 5. Set Up Private Certificate Authority (PCA)

TiDB Cloud utilizes the **AWS Private Certificate Authority (ACM PCA)** service to issue and manage digital certificates, ensuring secure communication between internal database cluster components via mTLS.

To meet compliance requirements, TiDB BYOC integrates with a customer-provided PCA to issue identity certificates for data nodes using your enterprise's own domain. This ensures that the Root of Trust for all encrypted communications remains strictly within your organization's control.

Therefore, you must prepare a valid Subordinate CA in the deployment region. Please follow the steps below:

1. **Create a CA:** Follow [AWS Private CA: Creating a private CA](https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html).

* *Configuration:* Ensure the validity period is set to at least **20 years**.

2. **Install Certificate:** Follow [Installing the CA certificate](https://docs.aws.amazon.com/privateca/latest/userguide/PCACertInstall.html#InstallRoot).

* *Prerequisite:* You must have an active Root CA.

3. **Record ARN:** Copy the **Subordinate CA ARN**.

* *Example:* arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234...

**Verification:** PCA Information from your AWS console.

![][image5]

|  Note for POC / Cost Optimization: If you are in the Proof of Concept (POC) phase, you may choose to use Self-Signed Certificates instead of AWS Private CA to reduce costs. Please contact your TiDB Cloud Support Representative directly for specific configuration instructions regarding this option. |
| :---- |


| Note for Multi-Region Deployment: Similar to Hosted Zones, the same Private Certificate Authority (PCA) can be shared across all regions for multi-region deployments. Alternatively, you can create a dedicated PCA for each new region. See Section 7 for details. |
| :---- |

## Step 6. Plan Network CIDR Ranges

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
   * **Can Overlap:** Things that will *never* be peered can safely overlap with the TiDB BYOC environment.  
3. **Cross-Cluster Replication (Critical):** If you plan to deploy multiple TiDB clusters (whether in the same region or across different regions) and eventually want to **replicate data between them** (e.g., using TiCDC for Disaster Recovery or data consolidation), their respective TiDB Cluster CIDR ranges **must be de-conflicted**.

Please provide the planned CIDR ranges to your TiDB Cloud representative before the automated deployment starts.

## Step 7. Summary: Required Information (Table 1-1)

Please fill out the table below with the information gathered in steps 1.1–1.5 and share it with your TiDB Cloud representative to initiate Phase 3\.

Table 1-1:  **Required Information** 

| Category | Details to provide | Example  | Comments |
| :---- | :---- | :---- | :---- |
| **TiDB tenant ID** | Unique identifier for your TiDB Cloud org | 1372813089209270552 | (Section 1.1) |
| **AWS Account ID** | 12-digit AWS account number | 123456789012 | (Section 1.2) |
| **AWS Region**  | Region selected for deployment | Us-west-2 Us-east-1 Us-east-2  | (Session 1.2)
*If multi-region, please list all intended regions.* |
| **Availability Zones** | 3 AZs or single AZ per region (specify names and ID)  | **Us-east-1:** us-east-1a, use1-az1 us-east-1b, use1-az2 us-east-1c, use1-az4 **Us-east-2:** us-east-2a, use2-az1 us-east-2b, use2-az2 us-east-2c, use2-az3 **Us-west-2:**  us-west-2a, usw2-az1 | (Section 1.3) *Must meet the AZ quantity requirement for **each** selected region.* |
| **Subordinate CA ARN** | AWS ACM Private CA ARN  | arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234 | (Section 1.5) *(Can be shared across multiple regions)* |
| **Hosted Zone Names & Host Zone ID**  | TiDB Cluster Zone Observability (O11Y) Zone  | **Hosted zone name：** clusters.byoc-0929.pingcap.net **Hosted zone ID：** Z1039122VAY4T8UNWR8E **Hosted zone name：** o11y.byoc-0929.pingcap.net **Hosted zone ID：** Z10389823CTXFNM7VG79P | (Section 1.4) *(Can be shared across multiple regions)* |
| **CIDR**  | Customer-planned CIDR range for TiDB Cluster Customer-planned CIDR range for O11Y Cluster | **TiDB Cluster CIDR:** 10.10.0.0/16 **O11y CIDR** 10.20.0.0/16 | (Section 1.6)  |
| **Image Sync Region**  | Region ID chosen for image synchronization | us-west-2  | Refer to section 3.1 for details |

## Step 8. Review and Increase AWS Service Quotas

**A. Recommended Quota Limits**  
Please request quota increases for the following resources in your target AWS region:

* **Amazon EC2 (vCPU-based quotas):** Increase relevant instance family quotas (e.g., Standard instances) to support up to 1024 vCPUs.  
* **Amazon EBS (gp3 storage):** Increase General Purpose (gp3) volume storage quota to 150 TiB.  
* **Amazon EKS / Cluster Scaling Capacity:** Ensure the environment supports scaling to at least 40 worker nodes, including:  
  * EC2 capacity  
  * Auto Scaling Group limits  
  * EKS managed node group limits

**B. How to Request a Quota Increase**

1. Log in to the AWS Management Console.  
2. Navigate to Service Quotas.  
3. Search for the relevant services: Amazon EC2， Amazon EBS，Amazon EKS  
4. Select the required quota.  
5. Click Request quota increase.  
6. Enter the target values and submit the request.
