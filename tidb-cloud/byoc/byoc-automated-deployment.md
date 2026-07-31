---
title: TiDB Cloud BYOC Automated Deployment
summary: This document outlines the automated deployment process for TiDB Cloud BYOC on AWS.
---

# TiDB Cloud BYOC Automated Region Deployment

With the AWS environment prepared and IAM permissions established, the TiDB Cloud team will initiate the automated provisioning process.

> **Note:**
>
> > This phase is managed by TiDB Cloud and normally requires no customer action. If the deployment is blocked by customer-managed policies, AWS service quotas, or network restrictions, the TiDB Cloud team will contact you for assistance.


## Deployment overview

The automated deployment consists of the following stages:

1. Synchronize container images to your AWS account.
2. Deploy the regional management plane.
3. Deploy customer-side observability and supporting infrastructure.
4. Register and validate the new BYOC region.

The deployment creates resources in both a TiDB Cloud-managed AWS account and your AWS account.
This phase prepares the BYOC region for Resource Pool and Instance creation. It does not create a TiDB Resource Pool or Instance.


## Step 1: Image synchronization (approx. 1-2 hours)

### Customer action

Select the AWS Region for the BYOC deployment and provide the Region information to your TiDB Cloud representative.

### What happens

TiDB Cloud synchronizes the required container images from its central image repository to an Amazon ECR registry in your AWS account.

The first deployment in a new AWS Region can take longer because all required images must be synchronized. Subsequent deployments in the same Region reuse the synchronized images and usually complete faster.

## Step 2: Deploy the regional management plane

TiDB Cloud deploys a regional management plane in a TiDB Cloud-managed AWS account.

The regional management plane includes infrastructure and services used to manage the lifecycle of your BYOC environment, such as:

- A dedicated VPC and Amazon EKS cluster.
- Regional management and API services.
- Configuration and metadata services.
- Components for instance provisioning, scheduling, scaling, and recovery.
- Integration with the TiDB Cloud global control plane.

The regional management plane does not store your TiDB application data.


## Step 3: Deploy customer-side supporting infrastructure

TiDB Cloud assumes the IAM roles created during account bootstrapping and deploys the required supporting resources in your AWS account.

These resources include:

- An isolated VPC for the observability environment.
- A dedicated Amazon EKS cluster for observability services.
- Metrics, logging, and alerting components.
- Supporting storage, load balancers, API endpoints, DNS records, and certificates.
- Audit-log and service-level indicator resources.
- Secure connectivity between the customer-side environment and the regional management plane.

> **Important**
>
> The Amazon EKS cluster created in this step hosts observability and supporting services. It is not the TiDB data plane for a TiDB instance.
>
> The TiDB data plane is initialized when you create your first BYOC instance in the TiDB Cloud console.

## Step 4: Register and validate the BYOC region

After the infrastructure and services are deployed, TiDB Cloud:

- Registers the BYOC region with the TiDB Cloud global control plane.
- Verifies that regional management services are healthy.
- Verifies connectivity to the customer-side observability environment.
- Confirms that metrics and logs can flow through the expected paths.
- Confirms that the region is ready for TiDB instance creation.


## Deployment completion

After the automated deployment completes:

- The TiDB Cloud team notifies you that the BYOC region is ready.
- The new BYOC region becomes available for instance creation.
- AWS starts charging your account for the customer-owned resources created during deployment, such as Amazon EKS, EC2, NAT Gateway, load balancers, and storage.

## What's next

After your {{{ .byoc }}} region is fully operational, continue with [Create Your First TiDB Cloud BYOC Instance](/tidb-cloud/byoc/byoc-initialize-service.md) to create your first TiDB instance and configure secure administrative access.
