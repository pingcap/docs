---
title: TiDB Cloud BYOC Automated Deployment
summary: This document outlines the automated deployment process for TiDB Cloud BYOC on AWS.
---

# TiDB Cloud BYOC Automated Deployment

With the AWS environment prepared and IAM permissions established, the TiDB Cloud team will initiate the automated provisioning process.

**Note:** This phase is fully managed by TiDB Cloud. No customer action is required until you receive the completion notification.

## **3.1 Deployment Timeline**

The deployment consists of two automated stages:

**Stage A: Image Synchronization (Approx. 1-2 Hours)**

* **Customer action:** Select the AWS Region where the BYOC deployment will be created and provide the Region information to your TiDB Cloud representative.  
* **What happens:** Database container images are synchronized from the TiDB Cloud central repository to your AWS account's region.  
* **Note:** This step is time-intensive only for the **first BYOC deployment** in a new region. Subsequent deployments in the same region will reuse the existing images and complete significantly faster.

**Stage B: Infrastructure Provisioning (Approx. 3 Hours)**

**Action**: The system automatically provisions dedicated resources within your AWS account, including:

*  **Network Environment (VPC & Networking):** Creates an isolated VPC to provide a secure network foundation for the database cluster.

* **Control Plane Initialization:** Deploys essential management components responsible for the database's full lifecycle management. This includes automated resource provisioning, service scheduling, elastic scaling, and failure recovery—all executed automatically with no manual intervention required.

* **Compute Resource Provisioning:** Creates two EKS clusters serving the following purposes:

  * Deploy Observability Services: Hosts components such as Prometheus and Grafana to collect monitoring metrics and logs.

  * Deploy Data Plane Management Nodes: Hosts components (such as the TiDB Operator) to provide the runtime environment for the subsequent creation of TiDB compute and storage nodes.

## **3.2 Deployment completion**

Once the automation completes:

1. **Notification: You will be notified by the TiDB Cloud Team that the BYOC Region is ready.**

2. **Billing Activation:**

* **AWS Invoice:** You will begin seeing charges from AWS for the underlying resources (EC2, NAT Gateways, EKS).

**Status:** Your BYOC region is now fully operational. You may proceed to **Phase 4** to create your first TiDB instance.
