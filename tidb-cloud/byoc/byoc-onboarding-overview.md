---
title: TiDB Cloud BYOC Onboarding Overview
summary: Overview of the TiDB Cloud BYOC onboarding process, detailing the responsibilities and steps for both the customer and TiDB Cloud team.
---

# TiDB Cloud BYOC Onboarding Overview

TiDB Cloud BYOC (Bring Your Own Cloud) is an enterprise solution that lets you run the data plane in your own cloud environment while retaining the fully managed experience of TiDB Cloud.

The TiDB Cloud BYOC deployment is a collaborative process between your organization and the TiDB Cloud team. The timeline allows for secure infrastructure preparation, automated provisioning, and rigorous validation.

## Deployment phases

| Phase | Responsibility | Description |
| :---- | :---- | :---- |
| **Phase 1: AWS Prerequisites** | **Customer** | **Environment Preparation** Prepare the AWS foundation required for deployment. This includes creating a dedicated AWS account configuring Route 53 Hosted Zones setting up the Private Certificate Authority (PCA) |
| **Phase 2: IAM Bootstrapping** | **Customer** | **Permissions Setup** Execute the provided bootstrapping scripts to install the necessary IAM roles and policies. This authorizes the TiDB Cloud Control Plane to securely manage resources within your AWS account. |
| **Phase 3: Infrastructure Provisioning** | **TiDB Cloud** | **Automated Deployment** Once IAM permissions are verified, TiDB Cloud automatically provisions the VPC, EKS clusters, and control plane resources. *(Note: This process is fully automated and requires no customer intervention.)* |
| **Phase 4: Service Initialization** | **Customer** | **Instance Creation & Access Setup** Create your TiDB instance via the console. Subsequently, deploy the Bastion Host and authentication scripts to establish secure maintenance channels (Tailscale) and observability pipelines. *(Note: You may also choose to establish maintenance channels using your own custom methods.)* |
| **Phase 5: Validation** | **Joint** | **End-to-End Verification** Both teams collaborate to validate connectivity, verify metric collection, and confirm system health to ensure the BYOC environment is ready for use. |

| Note: Each phase requires timely coordination between teams. We recommend assigning dedicated resources from both organizations to ensure smooth progression through all stages. |
| :---- |

## **Architecture Overview**

TiDB Cloud BYOC employs a strict separation between the Control Plane and the Data Plane. Your data remains entirely within your AWS account. The Control Plane connects to your VPC exclusively via AWS PrivateLink. No public internet exposure is required for database nodes.

> **Note:**
>
> This architecture defaults to a Multi-AZ deployment for production high availability, but also supports a Single-AZ deployment for Proof of Concept (POC) or cost optimization scenarios.

![TiDB Cloud BYOC Architecture](/media/tidb-cloud/byoc-architecture.png)
