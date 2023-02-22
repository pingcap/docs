---
title: Console Audit Logging
summary: Learn about the audit logging feature for the TiDB Cloud console.
---

# Console Audit Logging

TiDB Cloud provides the console audit logging feature to help you track various behaviors and operations of users on the [TiDB Cloud console](https://tidbcloud.com). For example, you can track operations, such as inviting a user to join your organization and creating a cluster.

## Prerequisites

- You must be in the Owner or Audit Admin role of your organization in TiDB Cloud. Otherwise, you cannot see the console audit logging-related options in the TiDB Cloud console. For more information, see [Manage role access](/tidb-cloud/manage-user-access.md#manage-role-access).
- You can only enable and disable the console audit logging for your organization. You can only track the actions of users in your organization.
- After the console audit logging is enabled, all event types of the TiDB Cloud console will be audited, and you cannot specify only auditing some of them.

## Enable console audit logging

The console audit logging feature is disabled by default. To enable it, take the following steps:

1. In the upper-right corner of the [TiDB Cloud console](https://tidbcloud.com/), click <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging**.
2. Click **Enable Console Audit Logging**. Or click **Setting** in the upper-right corner to enable console audit logging.

## Disable console audit logging

To disable console audit logging, take the following steps:

1. In the upper-right corner of the [TiDB Cloud console](https://tidbcloud.com/), click <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging**.
2. Click **Setting** in the upper-right corner, and then disable console audit logging.

## View console audit logs

You can only view the console audit logs of your organization. 

1. In the upper-right corner of the [TiDB Cloud console](https://tidbcloud.com/), click <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging**.
2. To get a specific part of audit logs, you can filter the event type, operation status, and time range. 
3. (Optional) To filter more fields, click **Advanced filter**, add more filters, and then click **Apply**. 
4. Click the row of a log to view its detailed information in the right pane.

## Export console audit logs

To export the console audit logs of your organization, take the following step:

1. In the upper-right corner of the [TiDB Cloud console](https://tidbcloud.com/), click <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging**.
3. If you need to export a specific part of console audit logs, you can filter through various conditions. Otherwise, skip this step.
4. Click **Export** and select the desired export format in JSON or CSV. 

## Console audit log storage policy

The storage time of console audit logs is 90 days, after which the logs will be automatically cleaned up.

> **Note:**
>
> - You cannot specify the storage location of console audit logs in TiDB Cloud.
> - You cannot manually delete audit logs.

## Console audit event types

The console audit logs can record various user activities on the TiDB Cloud console through the following event types:

| Console audit event type | Description |
|---|---|
| CreateOrganization | Create an organization |
| LoginOrganization | Log in to an organization |
| SwitchOrganization | Switch from the current organization to another organization |
| LogoutOrganization | Log out from an organization |
| InviteUserToOrganization | Invite a user to join the organization |
| DeleteInvitationToOrganization | Delete a user's invitation to join the organization |
| ResendInvitationToOrganization | Resend an invitation for a user to join the organization  |
| ConfirmJoinOrganization | The invited user confirms joining the organization |
| DeleteUserFromOrganization | Delete a joined user from the organization |
| UpdateUserRoleInOrganization | Update the role of a user in the organization |
| CreateAPIKey | Create an API Key |
| EditAPIKey | Edit an API Key |
| DeleteAPIKey | Delete an API Key |
| UpdateTimezone | Update the time zone of your organization |
| ShowBill | Show organization bill  |
| DownloadBill | Download organization bill |
| ShowCredits | Show organization credits |
| AddPaymentCard | Add a payment card |
| UpdatePaymentCard | Update a payment card |
| DeletePaymentCard | Delete a payment card |
| SetDefaultPaymentCard | Set a default payment card |
| EditBillingProfile | Edit billing profile information |
| ContractAction | Organize contract-related activities |
| EnableConsoleAuditLog | Enable console audit logging |
| ShowConsoleAuditLog | Show console audit logs |
| InviteUserToProject | Invite a user to join a project  |
| DeleteInvitationToProject | Delete a user's invitation to join the project |
| ResendInvitationToProject | Resend an invitation for a user to join the project |
| ConfirmJoinProject | The invited user confirms joining the project |
| DeleteUserFromProject | Delete a joined user from the project |
| CreateProject | Create a project |
| CreateProjectCIDR | Create a new project CIDR |
| CreateAWSVPCPeering | Create an AWS VPC Peering |
| DeleteAWSVPCPeering | Delete an AWS VPC Peering |
| CreateGCPVPCPeering | Create a GCP VPC Peering |
| DeleteGCPVPCPeering | Delete a GCP VPC Peering |
| CreatePrivateEndpointService | Create private endpoint service |
| DeletePrivateEndpointService | Delete private endpoint service |
| CreateAWSPrivateEndPoint | Create an AWS private endpoint |
| DeleteAWSPrivateEndPoint | Delete AWS private endpoint |
| SubscribeAlerts | Subscribe alerts |
| UnsubscribeAlerts | Unsubscribe alerts |
| CreateDatadogIntegration | Create datadog integration |
| DeleteDatadogIntegration | Delete datadog integration |
| CreateVercelIntegration | Create vercel integration |
| DeleteVercelIntegration | Delete vercel integration |
| CreatePrometheusIntegration | Create Prometheus integration |
| DeletePrometheusIntegration | Delete Prometheus integration |
| CreateCluster | Create a cluster |
| DeleteCluster | Delete a cluster |
| PauseCluster | Pause a cluster |
| ResumeCluster | Resume a cluster |
| ScaleCluster | Scale a cluster |
| DownloadTiDBClusterCA | Download TiDB cluster CA certificate |
| OpenWebSQLConsole | Connect to a TiDB cluster through Web SQL |
| SetRootPassword | Set the root password of a TiDB cluster |
| UpdateIPAccessList | Update the IP access list of a TiDB cluster |
| SetAutoBackup | Set the automatic backup mechanism of a TiDB cluster |
| DoManualBackup | Perform a manual backup of TiDB cluster |
| DeleteBackupTask | Delete a backup task |
| DeleteBackup | Delete a backup file |
| RestoreFromBackup | Restore to a TiDB cluster based on the backup files |
| RestoreFromTrash | Restore to a TiDB cluster based on the backup files in the trash |
| ImportDataFromAWS | Import data from AWS |
| ImportDataFromGCP | Import data from GCP |
| CreateMigrationJob | Create a migration job |
| SuspendMigrationJob | Suspend a migration job |
| ResumeMigrationJob | Resume a migration job |
| DeleteMigrationJob | Delete a migration job |
| ShowDiagnose | Show diagnosis information |
| DBAuditLogAction | Set the activity of database audit logging |
| AddDBAuditFilter | Add a database audit log filter |
| DeleteDBAuditFilter | Delete a database audit log filter |
| EditProject | Edit the information of a project |
| DeleteProject | Delete a project |
| BindSupportPlan | Bind a support plan |
| CancelSupportPlan | Cancel a support plan |
| UpdateOrganizationName | Update the organization name |

> **Note:**
>
> The main event types have been covered, but a small number of event types have not been covered for the time being and are being improved.

## Console audit log fields

To help you track user activities, TiDB Cloud provides the following fields for each console audit log:

| Field name | Data type | Description |
|---|---|---|
| type | string | Event type |
| ends_at | timestamp | Event time |
| operator_type | enum | Operator type: `user` or `api_key` |
| operator_id | uint64 | Operator ID |
| operator_name | string | Operator name |
| operator_ip | string | Operator's IP address |
| operator_login_method | enum | Operator's login method: `google`, `github`, `microsoft`, `email`, or `api_key` |
| org_id | uint64 | Organization ID to which the event belongs |
| org_name | string | Organization name to which the event belongs |
| project_id | uint64 | Project ID to which the event belongs |
| project_name | string | Project name to which the event belongs |
| cluster_id | uint64 | Cluster ID to which the event belongs |
| cluster_name | string | Cluster name to which the event belongs |
| trace_id | string | Trace ID of the request initiated by the operator |
| result | enum | Event result: `success` or `failure` |
| details | json | Detailed description of the event |

> **Note:**
>
> The trace_id field is temporarily unavailable
