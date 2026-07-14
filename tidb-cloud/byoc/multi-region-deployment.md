---
title: TiDB Cloud BYOC Multi-Region Deployment
summary: This document outlines the process for deploying TiDB Cloud BYOC across multiple AWS regions.
---

# TiDB Cloud BYOC Multi-Region Deployment

TiDB Cloud BYOC supports deployments across **multiple AWS Regions**. The same IAM roles can be reused across regions, so you do not need to recreate the BYOC IAM roles when enabling an additional region.

The following two scenarios apply to multi-region deployments:

| Scenario | Description | Script |
| ----- | ----- | ----- |
| New multi-region deployment | No BYOC region has been deployed yet, and multiple regions are planned from the beginning. | `tidbcloud-byoc-setup.sh` |
| Add a region to an existing deployment | One or more BYOC regions have already been deployed, and an additional region will be enabled later. | `tidbcloud-byoc-update.sh` |

* For a new deployment with multiple planned regions, see [Scenario 1: New multi-region deployment](#scenario-1-new-multi-region-deployment).
* To add a region to an existing BYOC deployment, see [Scenario 2: Add a region to an existing deployment](#scenario-2-add-a-region-to-an-existing-byoc-deployment).

## Resource planning: shared and dedicated resources

Before configuring multiple regions, determine whether the following foundational resources will be shared across regions or dedicated to each region:

* AWS private certificate authority (PCA)
* Route 53 hosted zone for TiDB
* Route 53 hosted zone for O11Y

### Shared resources

The same PCA, TiDB hosted zone, and O11Y hosted zone can be shared across all enabled regions.

In this configuration, provide the primary PCA and Hosted Zones through the standard parameters and omit the corresponding \--additional-\* parameters.

### Dedicated resources

You can prepare a separate PCA, TiDB hosted zone, and O11Y hosted zone for each additional region.

The primary region resources are provided through the standard parameters:

* `--pca-arn`
* `--tidb-hz-id`
* `--o11y-hz-id`

Resources for additional regions are provided through:

* `--additional-pca-arns`
* `--additional-tidb-hz-ids`
* `--additional-o11y-hz-ids`

For two or more additional regions, provide the values as comma-separated lists in the same regional order.

### Mixed resources

Shared and dedicated resources can be combined.

For example, all regions can share the same PCA while using separate Hosted Zones.

Each additional resource parameter is independent. Omit a parameter when the corresponding resource will remain shared with the primary region.

## Scenario 1: New multi-region deployment

Use this section if you have not deployed any BYOC regions yet and plan to deploy multiple regions from the start.

Run `tidbcloud-byoc-setup.sh` to initialize the BYOC environment and configure the required resources.

### All regions share the same resources

When all regions share the same PCA and hosted zones, run the standard setup command:

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <SharedTidbHostedZoneId> \
  --o11y-hz-id <SharedO11yHostedZoneId> \
  --pca-arn <SharedPCAArn>
```

No `--additional-*` parameters are required.

### Additional regions use dedicated resources

Provide the primary region resources through the standard parameters and the additional region resources through the `--additional-*` parameters:

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

The values in all comma-separated lists must follow the same regional order. For example:

* The first value represents Region 2.
* The second value represents Region 3.

### Mixed shared and dedicated resources

The following example shares one PCA across all regions while using dedicated hosted zones:

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

## Scenario 2: Add a region to an existing BYOC deployment

Use this section if one or more BYOC regions have already been deployed and you want to add one or more new regions.

Do not run `tidbcloud-byoc-setup.sh` again.

Use `tidbcloud-byoc-update.sh` to update the existing CloudFormation stacks. The existing IAM roles and previously configured stack parameters will be reused.

### Before adding the region

Before running the update script:

1. Confirm the AWS Regions to be added.
2. Select the Availability Zones for the new regions.
3. Plan the TiDB Cluster CIDR and O11Y CIDR for each new region.
4. Confirm whether each new region will:
    * share the existing PCA and hosted zones, or
    * use dedicated PCA and hosted zones.
5. Review and increase AWS service quotas in each new region.
6. Share the information for the new regions with your TiDB Cloud representative.

The CIDR ranges for the new regions must not overlap with:

* the TiDB Cluster CIDR and O11Y CIDR within the same region;
* existing application VPCs, on-premises networks, or VPN networks that will be connected through VPC Peering or VPN; or
* other TiDB clusters that will participate in cross-region replication.

### Share existing PCA and hosted zones

Use this option if all new regions will share the PCA and hosted zones already used by the existing deployment.

No additional resource parameters are required:

```shell
bash tidbcloud-byoc-update.sh \
  --stack all
```

The existing resources will continue to be used by all enabled regions.

A plain \--stack all update is safe when no new multi-region resource values are required.

### Use dedicated resources for the new regions

Use this option if the new regions require dedicated PCAs, TiDB hosted zones, or O11Y hosted zones.

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

* The first value in each list represents Region 2.
* The second value in each list represents Region 3.

### Use a mix of shared and dedicated resources

The new regions can share some existing resources while using dedicated resources for others.

For example, to share the existing PCA while using dedicated hosted zones for the new regions:

```shell
bash tidbcloud-byoc-update.sh \
--stack all \
--additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \ --additional-o11y-hz-ids <Region2O11yHostedZoneId>,<Region3O11yHostedZoneId>
```

Because the existing PCA is shared, `--additional-pca-arns` is omitted.

The resource strategy can also differ between the new regions. However, the values supplied for each `--additional-*` parameter must remain aligned with the same regional order.

### Add Regions When Multiple Regions Already Exist

When the existing deployment already includes multiple regions, use the same update process to add further regions.

The multi-region resource values are stored in the CloudFormation stacks and reused during future updates. When running the update command, provide any new or changed resource values required by the Regions being added.

For example, if Region 1 is the primary region, Region 2 is already configured, and Region 3 is being added with dedicated resources:

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \
  --additional-o11y-hz-ids <Region2O11yHostedZoneId>,<Region3O11yHostedZoneId>
```

Ensure that previously configured and newly added resource values remain in the correct regional order.

### Complete the Regional Deployment

Updating the CloudFormation stacks prepares the account-level permissions and resource configuration required by the new regions. It does not by itself complete the regional infrastructure deployment.

After the update succeeds:

1. Share the script execution result with your TiDB Cloud representative.
2. TiDB Cloud verifies the updated IAM and regional resource configuration.
3. TiDB Cloud initiates automated infrastructure provisioning for the new regions.
4. After provisioning completes, perform the joint validation described in Section 5 for each new region.
