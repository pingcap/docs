---
title: TiDB Cloud BYOC Onboarding Overview
summary: Overview of the TiDB Cloud BYOC onboarding process, detailing the responsibilities and steps for both the customer and TiDB Cloud team.
---

# TiDB Cloud BYOC Onboarding Overview

TiDB Cloud BYOC (Bring Your Own Cloud) is an enterprise solution that lets you run the data plane in your own cloud environment while retaining the fully managed experience of TiDB Cloud.

The TiDB Cloud BYOC deployment process is a collaborative effort between your organization and the TiDB Cloud team. The process includes secure infrastructure preparation, automated provisioning, and comprehensive validation.

<!--TO confirm: might need to state that currently only AWS is supported and the word AWS is not used in title for future content scale.-->

## Deployment phases

| Phase | Responsibility | Description |
| :---- | :---- | :---- |
| [**Phase 1: Environment preparation**](/tidb-cloud/byoc/byoc-prepare-environment-aws.md) | **Customer** | Prepare the AWS foundation required for deployment. This includes creating a dedicated AWS account configuring Route 53 Hosted Zones setting up the private certificate authority (PCA). |
| [**Phase 2: IAM bootstrapping**](/tidb-cloud/byoc/byoc-iam-configuration.md) | **Customer** | Execute the provided bootstrapping scripts to install the necessary IAM roles and policies. This authorizes the TiDB Cloud Control Plane to securely manage resources within your AWS account. |
| [**Phase 3: Automated deployment**](/tidb-cloud/byoc/byoc-automated-deployment.md) | **TiDB Cloud** | Once IAM permissions are verified, TiDB Cloud automatically provisions the VPC, EKS clusters, and control plane resources. Note: This process is **fully automated** and requires no customer intervention. |
| [**Phase 4: Service initialization**](/tidb-cloud/byoc/instance-creation-access-setup.md) | **Customer** | Create your TiDB instance via the console. Subsequently, deploy the Bastion Host and authentication scripts to establish secure maintenance channels (Tailscale) and observability pipelines. Note: You may also choose to establish maintenance channels using your own custom methods. |
| [**Phase 5: Validation**](/tidb-cloud/byoc/joint-validation.md) | **Joint** | Both teams collaborate to validate connectivity, verify metric collection, and confirm system health to ensure the BYOC environment is ready for use. |

> **Note:**
>
> Each phase requires timely coordination between teams. We recommend assigning dedicated resources from both organizations to ensure smooth progression through all stages.

## Architecture overview

TiDB Cloud BYOC employs a strict separation between the Control Plane and the Data Plane. Your data remains entirely within your AWS account. The Control Plane connects to your VPC exclusively via AWS PrivateLink. No public internet exposure is required for database nodes.

> **Note:**
>
> This architecture defaults to a Multi-AZ deployment for production high availability, but also supports a Single-AZ deployment for Proof of Concept (POC) or cost optimization scenarios.

![TiDB Cloud BYOC Architecture](/media/tidb-cloud/byoc-architecture.png)
