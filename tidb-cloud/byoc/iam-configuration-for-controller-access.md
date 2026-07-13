---
title: TiDB Cloud BYOC IAM Configuration for Controller Access
summary: This document outlines the IAM configuration required for TiDB Cloud BYOC controller access.
---

# TiDB Cloud BYOC IAM Configuration for Controller Access

Once the AWS environment is prepared, you must authorize the TiDB Cloud Control Plane to manage resources within your account. This is achieved by executing a bootstrapping script that establishes the necessary IAM Roles based on the Principle of Least Privilege.

## Preparation

Before executing the script, ensure you have the following:

1. **AWS CLI Installed:** The CLI must be configured with an Access Key that has permissions to create IAM roles and policies.
2. **TiDB Cloud Account Info:** Contact your TiDB Cloud support representative to obtain the **Control Plane Account ID** and **Clinic Account ID**.

## Gather Parameters

Use the table below to map the required parameters for the script:

| Parameter | Source | Description |
| :---- | :---- | :---- |
| \<ControlPlaneAccountId\> | **TiDB Support** | The AWS Account ID of the TiDB Control Plane. |
| \<ClinicAccountId\> | **TiDB Support** | The AWS Account ID for the TiDB Clinic service. |
| \<TidbHostedZoneId\> | Table 1-1 | The ID of the TiDB Cluster Hosted Zone you created. |
| \<O11yHostedZoneId\> | Table 1-1 | The ID of the Observability Hosted Zone you created. |
| \<TidbPCAArn\> | Table 1-1 | The ARN of the Private CA you created. |

## Execute Bootstrapping Script

1. **Download:** Download the script from the [PingCAP GitHub Repository](https://github.com/tidbcloud/byoc-account-setup/tree/main).

2. **Execute:** Run the command below in your terminal, replacing the placeholders with your actual values.

| \# Syntax
`sh tidbcloud-byoc-setup.sh \ --control-plane-id <ControlPlaneAccountId> \ --clinic-id <ClinicAccountId> \ --tidb-hz-id <TidbHostedZoneId> \ --o11y-hz-id <O11yHostedZoneId> \ --pca-arn <TidbPCAArn>` |
| :---- |

3. **Process Monitoring:** Upon execution, the script initiates AWS CloudFormation to provision and update resources. You will observe a log stream in the terminal displaying status messages such as `waiting for changeset to be created` and `successfully created/updated stack`.

![][image6]

## Verification

After execution, the script will output the ARNs of the created IAM roles.

* **Action Required:** Please share the **execution result/log** with your TiDB Cloud Representative.

* **Next Step:** Once TiDB Cloud verifies the roles, the automated deployment (Phase 3\) will be triggered.
