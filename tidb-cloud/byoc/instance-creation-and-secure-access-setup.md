---
title: TiDB Cloud BYOC Instance Creation & Secure Access Setup
summary: This document outlines the process for creating a TiDB Cloud BYOC instance and setting up secure access.
---

# TiDB Cloud BYOC Instance Creation & Secure Access Setup

Following the successful deployment of the BYOC infrastructure, the next phase involves creating your first database instance and establishing secure administrative access channels.

## Create TiDB Instance

### Create a new TiDB Instance

You can now provision TiDB instances directly via the TiDB Cloud Console.

1. **Initiate Creation:** Log in to the [TiDB Cloud Console](https://tidbcloud.com/) and follow the standard workflow to create a new instance.

![][image8]

2. **Configuration:** Select the region and specifications that match your workload requirements.

* *Initial Setup Time:* The creation of the **first instance** typically takes approximately **1 hour** as the system initializes the Kubernetes environment.

* *Subsequentinstances:* Creating additional instances in the same region will only take a few minutes.

3. **Capacity Configuration: Please consult with your TiDB Cloud representative** to determine the appropriate Request Unit (RU) settings for your initial connectivity and functional tests. They will recommend a configuration based on your specific testing requirements.

### Restore a new instance from S3

After successfully preparing your backup file in Amazon S3, you can proceed to restore the data into your newly created TiDB Cloud BYOC instance.

**Step 1: Configure Amazon S3 Access (AK/SK)** To allow TiDB Cloud to read your S3 backup, you must configure external storage access by generating an AWS Access Key ID and Secret Access Key (AK/SK) with the appropriate S3 read permissions.

* Please follow the detailed instructions here: [Configure Amazon S3 access using an AWS Access Key](https://docs-preview.pingcap.com/tidbcloud/configure-external-storage-access/#configure-amazon-s3-access-using-an-aws-access-key).

**Step 2: Execute the Restore Process** Once the access keys are configured, you can initiate the restore job from the TiDB Cloud Console.

* **Documentation:** For step-by-step restoration procedures, please refer to: [Restore backups from cloud storage](https://docs-preview.pingcap.com/tidbcloud/backup-and-restore-premium/#restore-backups-from-cloud-storage).

## (Optional) Deploy Secure Access Solution (Bastion Host)

To enable TiDB Support to assist with troubleshooting and observability, a secure access channel must be established. This is achieved by deploying a hardened Bastion Host within your VPC that connects via **Tailscale** (a secure VPN protocol).

**Note:**

1. This step is **optional**. You may choose to provide your own secure login method for maintenance.

2. The Bastion Host is used only for troubleshooting and does not need to maintain a persistent connection. You may terminate this channel at any time.

3. The Bastion Host deployment instruction for Single-AZ will be provided in the separated tab.

**A. Execute Deployment Script**

1. **Download:** Get the Bastion Host deployment script from the [PingCAP GitHub Repository](https://github.com/tidbcloud/byoc-account-setup/tree/main/bastion).
2. **Execute Terraform Deployment**

* *What this deployment does:*

* Provisions a hardened EC2 Bastion Host in your VPC.

* Creates an EKS Access Entry to allow the Bastion limited access to the Kubernetes cluster for management tasks.

* Establishes a secure Tailscale tunnel upon startup.

**B. Verify Access**

After the script completes:

1. **Check AWS Console:** verify that the Bastion Host EC2 instance is running.
2. **Confirm with TiDB:** Notify your TiDB Cloud Representative. They will verify that the PingCAP engineering team can successfully connect via the internal secure tunnel.

