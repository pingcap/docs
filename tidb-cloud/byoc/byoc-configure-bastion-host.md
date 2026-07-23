---
title: Configure a Bastion Host for {{{ .byoc }}}
summary: Learn how to deploy and manage bastion hosts for secure maintenance access in a {{{ .byoc }}} environment.
---

# Configure a Bastion Host for {{{ .byoc }}}

This document describes how to deploy and manage bastion hosts for a {{{ .byoc }}} environment. Bastion hosts provide controlled access paths for secure interaction with the TiDB and observability EKS clusters in your AWS account.

TiDB Cloud uses bastion hosts only for authorized troubleshooting and maintenance scenarios. The bastion hosts connect to TiDB Cloud through secure Tailscale tunnels. You can revoke or restore this access when needed.

> **Note:**
>
> Configuring bastion hosts is optional. You can also provide your own secure access method for maintenance and troubleshooting.

## Before you begin

Before you deploy bastion hosts, make sure that the following requirements are met:

- Terraform is installed locally.
- AWS CLI is configured with credentials for your AWS account.
- You have permissions to manage the required AWS resources, including EC2, IAM, and EKS resources.
- Your {{{ .byoc }}} environment has been deployed.
- You have obtained the following information from TiDB Cloud Support:
    - Your TiDB Cloud tenant ID.
    - The AWS region ID where your {{{ .byoc }}} environment is deployed.
    - The EKS cluster names for TiDB and observability.
    - Tailscale authentication keys for the bastion hosts that you want to deploy.
    - For Single-AZ deployments, the subnet IDs for the TiDB and observability EKS clusters.

## Deploy bastion hosts

To deploy bastion hosts, take the following steps:

1. Download the bastion host deployment script from the [PingCAP GitHub repository](https://github.com/tidbcloud/byoc-account-setup/tree/main/bastion).

2. Configure the Terraform backend.

    The default backend is Amazon S3. In `terraform.tf`, update the S3 backend configuration with your bucket, state file path, and region:

    ```hcl
    terraform {
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 5.0"
        }
      }

      backend "s3" {
        bucket = "YOUR_S3_BUCKET"
        key    = "TF_STATE_FILE_PATH"
        region = "us-west-2"
      }
    }
    ```

    If you use a different [Terraform backend](https://developer.hashicorp.com/terraform/language/backend), update `terraform.tf` accordingly.

3. Initialize Terraform:

    ```shell
    terraform init
    ```

4. Prepare the Terraform variables file:

    ```shell
    cp examples/terraform.tfvars.example ./terraform.tfvars
    vim ./terraform.tfvars
    ```

5. In `terraform.tfvars`, configure the required fields:

    - `aws_region`: the AWS region where your {{{ .byoc }}} environment is deployed, such as `us-west-2`.
    - `tidbcloud_tenant_id`: your TiDB Cloud tenant ID.
    - `bastions`: the bastion host configurations. You can configure bastions for `tidb` and `o11y`.
    - `<bastion_type>.eks_cluster_name`: the EKS cluster name for the bastion type, such as `tidb.eks_cluster_name` or `o11y.eks_cluster_name`.
    - `<bastion_type>.auth_key`: the Tailscale authentication key provided by TiDB Cloud.
    - `<bastion_type>.subnet_id`: for Single-AZ deployments only, the subnet ID for the corresponding EKS cluster.

    The following example configures bastion hosts for both TiDB and observability:

    ```hcl
    aws_region = "us-west-2"

    tidbcloud_tenant_id = "your_tidbcloud_tenant_id"

    bastions = {
      tidb = {
        eks_cluster_name = "your-tidb-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
      o11y = {
        eks_cluster_name = "your-o11y-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
    }
    ```

    If you only need a TiDB bastion host, configure only the `tidb` entry:

    ```hcl
    aws_region = "us-west-2"

    tidbcloud_tenant_id = "your_tidbcloud_tenant_id"

    bastions = {
      tidb = {
        eks_cluster_name = "your-tidb-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
    }
    ```

6. Apply the Terraform configuration:

    ```shell
    terraform apply
    ```

    Review the Terraform plan carefully. To confirm and proceed with the deployment, enter `yes`.

## Validate the deployment

After the deployment is complete, retrieve the Terraform output:

```shell
terraform output
```

The output is similar to the following:

```hcl
bastion_attributes = tomap({
  "bastion_name" = {
    "o11y" = "<bastion_o11y_name>"
    "tidb" = "<bastion_tidb_name>"
  }
  "instance_id" = {
    "o11y" = "<instance_o11y_id>"
    "tidb" = "<instance_tidb_id>"
  }
})
```

Provide the output to TiDB Cloud Support. TiDB Cloud Support uses the output to verify connectivity and complete any required network configuration.

## Manage bastion hosts

After a bastion host is deployed, you can manage it through AWS Systems Manager (SSM):

```shell
aws ssm start-session --region <region> --target <instance_id> --reason <reason>
```

To temporarily revoke TiDB Cloud access to the bastion host, run the following command on the bastion host:

```shell
tailscale down
```

To restore TiDB Cloud access to the bastion host, run the following command on the bastion host:

```shell
tailscale up
```

## Manage authentication keys

Tailscale authentication keys provided by TiDB Cloud are single-use and ephemeral. They typically expire after 3 days.

Key expiration does not affect bastion hosts that have already been deployed and configured with valid keys. However, if you need to run `terraform apply` again after the keys expire, such as to create a new bastion host or recreate an existing one, request new authentication keys from TiDB Cloud Support and update the `auth_key` values in `terraform.tfvars` before applying the configuration.

## Audit logs

For security and compliance, each bastion host is configured to collect a detailed audit trail of executed commands through the [auditd service](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/chap-system_auditing).

Audit logs are stored locally at `/var/log/audit/audit.log` and are automatically forwarded to the following AWS CloudWatch Log Group:

```text
/aws/eks/${eks_cluster_name}/byoc-bastion/audit
```

By default, logs are retained in CloudWatch for 90 days.

To disable CloudWatch audit log forwarding, set `cloudwatch_audit_enable` to `false`.

## Clean up bastion hosts

To remove the bastion hosts and associated resources created by the Terraform configuration, run the following command:

```shell
terraform destroy
```
