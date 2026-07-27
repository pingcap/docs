---
title: Configure Allowed Access CIDRs for AWS VPC Peering
summary: Learn how to configure allowed access CIDR rules for AWS VPC peering in TiDB Cloud BYOC.
---

# Configure Allowed Access CIDRs for AWS VPC Peering

This document describes how to configure allowed access CIDR rules for AWS VPC peering in TiDB Cloud BYOC.

AWS VPC peering creates a private connection between your VPC and TiDB Cloud, allowing your instance to be accessed privately without using the public internet. For new VPC peering requests, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

> **Note:**
>
> This document does not describe how to create an AWS VPC peering connection. VPC peering connections are created manually by you in your AWS account, or with assistance from the TiDB Cloud team. This document only describes how to configure which source CIDR ranges are allowed to access your instance through an existing VPC peering connection.

## Before you begin

Before you configure allowed access CIDRs, make sure that the following requirements are met:

- You have a TiDB Cloud BYOC instance.
- The AWS VPC peering connection for the instance has been created.
- You know the source CIDR ranges of the application subnets that need to access the instance through VPC peering.

## Configure allowed access CIDRs

To configure allowed access CIDRs for AWS VPC peering, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), go to the overview page of your TiDB Cloud BYOC instance.

2. In the left navigation pane, click **Settings** > **Networking**.

3. In the **AWS VPC Peering** area, review the peering connections for the instance.

    The table displays information such as the peering connection ID, status, your VPC region, your VPC ID, your AWS account ID, and your VPC CIDR.

4. In the **Allowed Access CIDR** area, click **Add CIDR** or **Edit CIDR**.

5. In the **Add CIDR** dialog, choose one of the following options:

    - **Allow traffic from a specific IP range through VPC peering**: allows traffic only from specific CIDR ranges. This option is recommended for production environments.
    - **Allow Global Access through VPC peering**: allows traffic from all VPCs that can reach the private NLB through VPC peering. This option applies the `0.0.0.0/0` rule and overrides existing CIDR restrictions.

6. If you choose **Allow traffic from a specific IP range through VPC peering**, enter a CIDR range in the **Access CIDR** field, and then click **Add to List**.

    You can add multiple CIDR ranges. For example, you can add the CIDR ranges of multiple application subnets.

7. Review the **Access CIDRs List**, and then click **Update**.

After the configuration is updated, the allowed CIDR ranges are displayed in the **Allowed Access CIDR** area. If global access is enabled, TiDB Cloud displays a warning message indicating that traffic from all VPCs that can reach the private NLB through VPC peering is allowed.

## Recommendations

- Use specific application subnet CIDR ranges whenever possible.
- Avoid enabling global access for long-term production use unless your security requirements explicitly allow it.
- Keep the allowed access CIDR list aligned with your application subnet changes.
- If you have multiple VPC peering connections for the same instance, make sure the CIDR list covers all application subnets that need access.

## How allowed access CIDRs work

For security reasons, all traffic from the peer VPC is denied by default, regardless of the VPC peering status. Even if a VPC peering connection is active, traffic can reach your TiDB Cloud BYOC instance only after you configure allowed access CIDR rules.

Allowed access CIDR rules are applied at the instance level and shared across all VPC peering connections for the instance. When you add or remove a CIDR rule, TiDB Cloud synchronizes the corresponding access rule to the security group of the private Network Load Balancer (NLB).

The following behavior applies:

- If no allowed access CIDRs are configured, all traffic through VPC peering is denied.
- If one or more CIDR ranges are configured, only traffic from those CIDR ranges is allowed through VPC peering.
- If global access is enabled, `0.0.0.0/0` is applied and existing CIDR restrictions are temporarily ignored.
- Existing CIDR rules are preserved when global access is enabled. After global access is disabled, the existing CIDR rules take effect again.

## Troubleshooting

If connectivity is not working as expected after configuring allowed access CIDRs, review the following common issues and their solutions.

### The VPC peering connection is active, but I cannot connect to the instance

An active VPC peering connection does not automatically allow traffic. Make sure that you have configured allowed access CIDR rules for the source application subnets.

Also check the following items in your AWS environment:

- The route tables for both VPCs are configured correctly.
- The source traffic comes from a CIDR range included in the allowed access CIDR list.
- The security groups and network ACLs in your application VPC allow outbound traffic to the TiDB Cloud BYOC endpoint.

### I added a CIDR rule, but the application still cannot connect

Check whether the CIDR range matches the actual source subnet used by your application. If your application runs behind NAT, a proxy, or another network appliance, verify the source CIDR that reaches the peering connection.

If the issue persists, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
