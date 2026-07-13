---
title: TiDB Cloud BYOC Multi-Region Deployment (Optional)
summary: This document outlines the process for deploying TiDB Cloud BYOC across multiple AWS regions.
---

# TiDB Cloud BYOC Multi-Region Deployment (Optional)

TiDB Cloud BYOC supports deployments across **multiple AWS Regions**. The same IAM roles can be reused across regions, so you do not need to recreate the BYOC IAM roles when enabling an additional region.

There are two different multi-region scenarios:

| Scenario | Description | Script |
| ----- | ----- | ----- |
| New multi-region deployment | No BYOC region has been deployed yet, and multiple regions are planned from the beginning. | `tidbcloud-byoc-setup.sh` |
| Add a region to an existing deployment | One or more BYOC regions have already been deployed, and an additional region will be enabled later. | `tidbcloud-byoc-update.sh` |

Select the section that matches your current deployment status:

* For a new deployment with multiple planned regions, follow **Section 7.2**.  
* To add a region to an existing BYOC deployment, follow **Section 7.3**.

## Resource Planning: Shared and Dedicated Resources**

Before configuring multiple regions, determine whether the following foundational resources will be shared across regions or dedicated to each region:

* AWS Private Certificate Authority (PCA)  
* Route 53 Hosted Zone for TiDB  
* Route 53 Hosted Zone for O11Y

### Shared Resources**

The same PCA, TiDB Hosted Zone, and O11Y Hosted Zone can be shared across all enabled regions.

In this configuration, provide the primary PCA and Hosted Zones through the standard parameters and omit the corresponding \--additional-\* parameters.

### Dedicated Resources**

You can prepare a separate PCA, TiDB Hosted Zone, and O11Y Hosted Zone for each additional region.

The primary region resources are provided through the standard parameters:

* \--pca-arn  
* \--tidb-hz-id  
* \--o11y-hz-id

Resources for additional regions are provided through:

* \--additional-pca-arns  
* \--additional-tidb-hz-ids  
* \--additional-o11y-hz-ids

For two or more additional regions, provide the values as comma-separated lists in the same regional order.

### Mixed Resources**

Shared and dedicated resources can be combined. 

For example, all regions can share the same PCA while using separate Hosted Zones.

Each additional resource parameter is independent. Omit a parameter when the corresponding resource will remain shared with the primary region.

## Scenario 1: New Multi-Region Deployment**

Use this section when no BYOC region has been deployed yet and you are planning multiple regions from the beginning.

Run `tidbcloud-byoc-setup.sh` to initialize the BYOC environment and configure the required resources.

### All Regions Share the Same Resources**

When all regions share the same PCA and Hosted Zones, run the standard setup command:

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <SharedTidbHostedZoneId> \
  --o11y-hz-id <SharedO11yHostedZoneId> \
  --pca-arn <SharedPCAArn>
```

No \--additional-\* parameters are required.

### Additional Regions Use Dedicated Resources**

Provide the primary region resources through the standard parameters and the additional region resources through the \--additional-\* parameters:

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <Region1TidbHostedZoneId> \
  --o11y-hz-id <Region1O11yHostedZoneId> \
  --pca-arn <Region1PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \
  --additional-o11y-hz-ids <Region2O11yHostedZoneId>,<Region3O11yHostedZoneId> \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn>
```

The values in all comma-separated lists must follow the same regional order.

For example:

* The first value represents Region 2\.  
* The second value represents Region 3\.

### Mixed Shared and Dedicated Resources**

The following example shares one PCA across all regions while using dedicated Hosted Zones:

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <Region1TidbHostedZoneId> \
  --o11y-hz-id <Region1O11yHostedZoneId> \
  --pca-arn <SharedPCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \
  --additional-o11y-hz-ids <Region2O11yHostedZoneId>,<Region3O11yHostedZoneId>
```

Because the PCA is shared, `--additional-pca-arns` is omitted.

## Scenario 2: Add a Region to an Existing BYOC Deployment**

Use this section when one or more BYOC Regions have already been deployed and you want to add one or more new Regions.

Do not run `tidbcloud-byoc-setup.sh` again.

Use `tidbcloud-byoc-update.s`h to update the existing CloudFormation stacks.The existing IAM roles and previously configured stack parameters will be reused.

### Before Adding the Region

Before running the update script:

1. Confirm the AWS Regions to be added.  
2. Select the Availability Zones for the new regions.  
3. Plan the TiDB Cluster CIDR and O11Y CIDR for each new region.  
4. Confirm whether each new region will:  
   * share the existing PCA and Hosted Zones, or  
   * use dedicated PCA and Hosted Zones.  
5. Review and increase AWS service quotas in each new region.  
6. Share the information for the new regions with your TiDB Cloud representative.

The CIDR ranges for the new Regions must not overlap with:

* the TiDB Cluster CIDR and O11Y CIDR within the same Region;  
* existing application VPCs, on-premises networks, or VPN networks that will be connected through VPC Peering or VPN; or  
* other TiDB clusters that will participate in cross-region replication.

### Share Existing PCA and Hosted Zones

Use this option when all new Regions will share the PCA and Hosted Zones already used by the existing deployment.

No additional resource parameters are required:

```shell
bash tidbcloud-byoc-update.sh \
  --stack all
```

The existing resources will continue to be used by all enabled regions.

A plain \--stack all update is safe when no new multi-region resource values are required.

### Use Dedicated Resources for the New Regions

Use this option when the new Regions require dedicated PCAs, TiDB Hosted Zones, or O11Y Hosted Zones.

Provide the resources for the new Regions through the corresponding `--additional-*` parameters:

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \
  --additional-o11y-hz-ids <Region2O11yHostedZoneId>,<Region3O11yHostedZoneId>

```

Each parameter is independent. Omit a parameter when the corresponding resource will remain shared with the existing Regions.

The values in all comma-separated lists must follow the same regional order. For example:

* The first value in each list represents Region 2\.  
* The second value in each list represents Region 3\.

### Use a Mix of Shared and Dedicated Resources

The new Regions can share some existing resources while using dedicated resources for others.

For example, to share the existing PCA while using dedicated Hosted Zones for the new Regions:

```shell
bash tidbcloud-byoc-update.sh \ 
--stack all \
--additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \ --additional-o11y-hz-ids <Region2O11yHostedZoneId>,<Region3O11yHostedZoneId>
```

Because the existing PCA is shared, `--additional-pca-arns` is omitted.

The resource strategy can also differ between the new Regions. However, the values supplied for each `--additional-*` parameter must remain aligned with the same regional order.

### Add Regions When Multiple Regions Already Exist

When the existing deployment already includes multiple Regions, use the same update process to add further Regions.

The multi-region resource values are stored in the CloudFormation stacks and reused during future updates. When running the update command, provide any new or changed resource values required by the Regions being added.

For example, if Region 1 is the primary Region, Region 2 is already configured, and Region 3 is being added with dedicated resources:

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \
  --additional-o11y-hz-ids <Region2O11yHostedZoneId>,<Region3O11yHostedZoneId>
```

Ensure that previously configured and newly added resource values remain in the correct regional order.

### Complete the Regional Deployment

Updating the CloudFormation stacks prepares the account-level permissions and resource configuration required by the new Regions. It does not by itself complete the regional infrastructure deployment.

After the update succeeds:

1. Share the script execution result with your TiDB Cloud representative.  
2. TiDB Cloud verifies the updated IAM and regional resource configuration.  
3. TiDB Cloud initiates automated infrastructure provisioning for the new Regions.  
4. After provisioning completes, perform the joint validation described in Section 5 for each new Region.
