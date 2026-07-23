---
title: TiDB Cloud BYOC IAM Configuration
summary: This document outlines the IAM configuration required for TiDB Cloud BYOC controller access.
---

# TiDB Cloud BYOC IAM Configuration

Once the AWS environment is prepared, you must authorize the TiDB Cloud Control Plane to manage resources within your account. This is achieved by executing a bootstrapping script that establishes the necessary IAM Roles based on the Principle of Least Privilege.

## Preparation

Before executing the script, ensure you have the following:

1. **AWS CLI installed:** The CLI must be configured with an Access Key that has permissions to create IAM roles and policies.
2. **TiDB Cloud account info:** Contact your TiDB Cloud support representative to obtain the **Control Plane Account ID** and **Clinic Account ID**.

## Gather parameters

Use the table below to map the required parameters for the script:

| Parameter | Source | Description |
| :---- | :---- | :---- |
| `<ControlPlaneAccountId>` | **TiDB Support** | The AWS Account ID of the TiDB Control Plane. |
| `<ClinicAccountId>` | **TiDB Support** | The AWS Account ID for the TiDB Clinic service. |
| `<TidbHostedZoneId>` | [Required information](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#summary-required-information) | The ID of the TiDB Cluster Hosted Zone you created. |
| `<O11yHostedZoneId>` | [Required information](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#summary-required-information) | The ID of the Observability Hosted Zone you created. |
| `<TidbPCAArn>` | [Required information](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#summary-required-information) | The ARN of the Private CA you created. |

## Execute bootstrapping script

1. Download the script from the [PingCAP GitHub repository](https://github.com/tidbcloud/byoc-account-setup/tree/main).

2. In your terminal, run the following command. Note to replace the placeholders with your actual values.

    ```bash
    sh tidbcloud-byoc-setup.sh \
        --control-plane-id <ControlPlaneAccountId> \
        --clinic-id <ClinicAccountId> \
        --tidb-hz-id <TidbHostedZoneId> \
        --o11y-hz-id <O11yHostedZoneId> \
        --pca-arn <TidbPCAArn>
    ```

3. Monitor the process. Upon execution, the script initiates AWS CloudFormation to provision and update resources. You can observe a log stream in the terminal displaying status messages such as `waiting for changeset to be created` and `successfully created/updated stack`.

<!--To confirm: whether to add image-->

## Verification

After execution, the script will output the ARNs of the created IAM roles.

- **Action required:** Share the **execution result/log** with your TiDB Cloud representative.

## What's next

After TiDB Cloud verifies the IAM roles, continue with [TiDB Cloud BYOC Automated Deployment](/tidb-cloud/byoc/byoc-automated-deployment.md). TiDB Cloud will trigger the automated deployment.
