---
title: TiDB Cloud BYOC Security Hardening (Optional)
summary: This document outlines the security hardening steps for TiDB Cloud BYOC deployments.
---

# TiDB Cloud BYOC Security Hardening (Optional)

After the BYOC environment has been fully delivered and is in production, you may choose to remove the bootstrap permissions used only during the installation phase to follow the **Principle of Least Privilege** recommended in cloud security best practices.

These permissions involve two IAM roles:

* **auto-deploy-cli**: The highest-privilege role used for creating infrastructure such as VPCs and EKS clusters.

* **auto-deploy-sync-image**: The role used to pull and synchronize images from TiDB Cloud.

| ⚠️ IMPORTANT NOTE FOR MULTI-REGION & MULTIPLE RESOURCE POOLS: The `auto-deploy-cli` and `auto-deploy-sync-image` IAM roles are Global (Account-level) resources. If you plan to deploy TiDB Cloud BYOC in multiple AWS regions (Section 7\) or provision multiple physically isolated Resource Pools within your account, we recommend delaying this security hardening step until ALL environments are fully deployed. |
| :---- |

Depending on your requirements for **automatic upgrades**, you can choose one of the following options:

### **Option A: Retain automatic upgrades, remove infrastructure deployment permissions**

**Goal:** Remove the `auto-deploy-cli` role while keeping the `auto-deploy-sync-image` role.

**Impact:**

* **Security:** The control plane can no longer create new infrastructure resources (e.g., VPCs) in your account.

* **Maintainability:** The cluster can still perform automatic upgrades, as image synchronization permissions are retained.

**Steps:**

1. Locate the CloudFormation template used during deployment: `tidbcloud-byoc-setup-deploy.yaml`.

2. Edit the file: find the `TiDBCloudAutoDeployRole` field and delete that line along with all its subordinate content, while keeping the `TiDBCloudAutoDeploySyncImageRole` section intact.

3. Apply the updated script in your terminal:

| `bash tidbcloud-byoc-update.sh --stack deploy` |
| :---- |

### **Option B: Remove all bootstrap permissions (automatic upgrades disabled)**

**Goal:** Remove both the `auto-deploy-cli` and `auto-deploy-sync-image` roles.

**Impact:**

* **Maximum security:** All IAM roles used during the bootstrap phase are removed.  
* **Feature limitation:** Automatic upgrades will no longer be available. To upgrade database components in the future, you must redeploy the sync-image role.

**Steps:**

Delete the corresponding CloudFormation stack via AWS CLI:

| `aws cloudformation delete-stack --stack-name tidbcloud-byoc-setup-deploy` |
| :---- |

---

⚠️ **Important:** Regardless of the option you choose, **do not delete stacks with** `dataplane` **or** `o11y` **suffixes** (e.g., `tidbcloud-byoc-setup-dataplane`), as these provide runtime permissions required for cluster operation, monitoring, and backups.
