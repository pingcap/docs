---
title: Project Migration FAQ for TiDB X Instances
summary: Learn why TiDB Cloud prompts you to move or convert your {{{ .starter }}} and Essential resources, what changes during project migration, and what follow-up actions might be required.
---

# Project Migration FAQ for TiDB X Instances

TiDB X instances are service-oriented TiDB Cloud offerings built on the [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md), including {{{ .starter }}}, {{{ .essential }}}, and {{{ .premium }}} instances.

This FAQ explains why the [TiDB Cloud console](https://tidbcloud.com/) prompts you to move your {{{ .starter }}} and Essential instances to TiDB X projects, and what changes occur during the migration process, and what follow-up actions you need to take.

## Why does the TiDB Cloud console prompt you to move your {{{ .starter }}} and Essential instances?

Before April 15, 2026, TiDB Cloud used a single **TiDB dedicated project** type to manage all TiDB Cloud resources. Such a project could contain a mix of {{{ .dedicated }}} clusters and TiDB X instances. However, mixing different resource types in one project increased management complexity because:

- TiDB dedicated projects were originally designed for {{{ .dedicated }}} clusters.
- TiDB X instances and {{{ .dedicated }}} clusters have different behaviors and management models.

Starting from April 15, 2026, TiDB Cloud introduces separate project types to provide clear separation between different resource types. Each project type now exclusively hosts its own resource type:

- **TiDB X project**: for TiDB X instances
- **TiDB dedicated project**: for {{{ .dedicated }}} clusters
- **TiDB X virtual project**: for TiDB X instances not grouped in any TiDB X project

TiDB X projects are lightweight and optional for TiDB X instances, while dedicated projects are mandatory for {{{ .dedicated }}} clusters. Separating these resources ensures a more consistent user experience and eliminates confusion over which project capabilities apply.

As a result of this separation, dedicated projects can no longer contain TiDB X instances. If your organization has existing {{{ .starter }}} or Essential resources in dedicated projects, TiDB Cloud prompts you to move them to TiDB X projects to align with the new resource model.

## What project types are available in TiDB Cloud?

TiDB Cloud provides three project types for different resource types and use cases.

- **TiDB dedicated project**: this project type is used only for {{{ .dedicated }}} clusters.

    - It helps you manage settings for {{{ .dedicated }}} clusters separately by project, such as RBAC, networks, maintenance, alert subscriptions, and encryption access.
    - Each {{{ .dedicated }}} cluster must belong to a dedicated project.
    - {{{ .dedicated }}} clusters cannot be moved between projects because of their infrastructure bindings.

- **TiDB X project**: this project type is used only for TiDB X instances.

    - It helps you manage RBAC for TiDB X instances by project.
    - TiDB X projects are lightweight and optional, so you can create TiDB X instances without assigning them to a project.
    - Projects are useful when you want to organize and group TiDB X instances, but they are not required.
    - You can move TiDB X instances between TiDB X projects or back to the organization level.

- **TiDB X virtual project**: this project is virtual and does not provide any management capabilities.

    - It acts as a logical container for TiDB X instances that do not belong to any project, so these instances can be accessed through the TiDB Cloud API by using a project ID.
    - Each organization has a unique virtual project ID.
    - You can get this ID from the project view on the **[My TiDB](https://tidbcloud.com/tidbs)** page.

The following table lists the differences between these project types:

| Feature | TiDB dedicated project | TiDB X project | TiDB X virtual project |
|---|---|---|---|
| Project icon in the TiDB Cloud console | <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="0.7" class="tiui-icon DProject " style="width: calc(1rem * var(--mantine-scale)); height: calc(1rem * var(--mantine-scale));"><path d="M11.8845 4.76892L11.2136 5.10433L11.2136 5.10433L11.8845 4.76892ZM10.4161 3.10931L10.6606 2.4003L10.6606 2.4003L10.4161 3.10931ZM11.1634 3.57116L11.6882 3.03535V3.03535L11.1634 3.57116ZM3.09202 3.21799L2.75153 2.54973L2.75153 2.54973L3.09202 3.21799ZM2.21799 4.09202L1.54973 3.75153L1.54973 3.75153L2.21799 4.09202ZM3.63803 20.673L3.29754 21.3413L3.63803 20.673ZM2.32698 19.362L1.65873 19.7025L2.32698 19.362ZM21.673 19.362L22.3413 19.7025L21.673 19.362ZM20.362 20.673L20.7025 21.3413L20.362 20.673ZM20.362 7.32698L20.7025 6.65873L20.362 7.32698ZM21.673 8.63803L22.3413 8.29754L21.673 8.63803ZM8.92285 10.5134V9.76343C8.50864 9.76343 8.17285 10.0992 8.17285 10.5134H8.92285ZM8.92285 17.5796H8.17285C8.17285 17.9938 8.50864 18.3296 8.92285 18.3296V17.5796ZM5.2 3V3.75H9.02229V3V2.25H5.2V3ZM11.8845 4.76892L11.2136 5.10433L12.3292 7.33541L13 7L13.6708 6.66459L12.5553 4.43351L11.8845 4.76892ZM2 7H2.75V6.2H2H1.25V7H2ZM9.02229 3V3.75C9.79458 3.75 10.0018 3.75979 10.1715 3.81832L10.4161 3.10931L10.6606 2.4003C10.1965 2.24021 9.68584 2.25 9.02229 2.25V3ZM11.8845 4.76892L12.5553 4.43351C12.2585 3.84002 12.0389 3.37888 11.6882 3.03535L11.1634 3.57116L10.6386 4.10698C10.7668 4.23258 10.8683 4.41358 11.2136 5.10433L11.8845 4.76892ZM10.4161 3.10931L10.1715 3.81832C10.3467 3.87873 10.5062 3.97733 10.6386 4.10698L11.1634 3.57116L11.6882 3.03535C11.3969 2.75013 11.046 2.53321 10.6606 2.4003L10.4161 3.10931ZM5.2 3V2.25C4.65232 2.25 4.19646 2.24942 3.82533 2.27974C3.44545 2.31078 3.08879 2.37789 2.75153 2.54973L3.09202 3.21799L3.43251 3.88624C3.52307 3.8401 3.66035 3.79822 3.94748 3.77476C4.24336 3.75058 4.62757 3.75 5.2 3.75V3ZM2 6.2H2.75C2.75 5.62757 2.75058 5.24336 2.77476 4.94748C2.79822 4.66035 2.8401 4.52307 2.88624 4.43251L2.21799 4.09202L1.54973 3.75153C1.37789 4.08879 1.31078 4.44545 1.27974 4.82533C1.24942 5.19646 1.25 5.65232 1.25 6.2H2ZM3.09202 3.21799L2.75153 2.54973C2.23408 2.81338 1.81338 3.23408 1.54973 3.75153L2.21799 4.09202L2.88624 4.43251C3.00608 4.19731 3.19731 4.00608 3.43251 3.88624L3.09202 3.21799ZM2 7V7.75H17.2V7V6.25H2V7ZM22 11.8H21.25V16.2H22H22.75V11.8H22ZM17.2 21V20.25H6.8V21V21.75H17.2V21ZM2 16.2H2.75V7H2H1.25V16.2H2ZM6.8 21V20.25C5.94755 20.25 5.35331 20.2494 4.89068 20.2116C4.4368 20.1745 4.17604 20.1054 3.97852 20.0048L3.63803 20.673L3.29754 21.3413C3.74175 21.5676 4.22189 21.662 4.76853 21.7066C5.30641 21.7506 5.9723 21.75 6.8 21.75V21ZM2 16.2H1.25C1.25 17.0277 1.24942 17.6936 1.29336 18.2315C1.33803 18.7781 1.43238 19.2582 1.65873 19.7025L2.32698 19.362L2.99524 19.0215C2.8946 18.824 2.82546 18.5632 2.78838 18.1093C2.75058 17.6467 2.75 17.0525 2.75 16.2H2ZM3.63803 20.673L3.97852 20.0048C3.55516 19.789 3.21095 19.4448 2.99524 19.0215L2.32698 19.362L1.65873 19.7025C2.01825 20.4081 2.59193 20.9817 3.29754 21.3413L3.63803 20.673ZM22 16.2H21.25C21.25 17.0525 21.2494 17.6467 21.2116 18.1093C21.1745 18.5632 21.1054 18.824 21.0048 19.0215L21.673 19.362L22.3413 19.7025C22.5676 19.2582 22.662 18.7781 22.7066 18.2315C22.7506 17.6936 22.75 17.0277 22.75 16.2H22ZM17.2 21V21.75C18.0277 21.75 18.6936 21.7506 19.2315 21.7066C19.7781 21.662 20.2582 21.5676 20.7025 21.3413L20.362 20.673L20.0215 20.0048C19.824 20.1054 19.5632 20.1745 19.1093 20.2116C18.6467 20.2494 18.0525 20.25 17.2 20.25V21ZM21.673 19.362L21.0048 19.0215C20.789 19.4448 20.4448 19.789 20.0215 20.0048L20.362 20.673L20.7025 21.3413C21.4081 20.9817 21.9817 20.4081 22.3413 19.7025L21.673 19.362ZM17.2 7V7.75C18.0525 7.75 18.6467 7.75058 19.1093 7.78838C19.5632 7.82546 19.824 7.8946 20.0215 7.99524L20.362 7.32698L20.7025 6.65873C20.2582 6.43238 19.7781 6.33803 19.2315 6.29336C18.6936 6.24942 18.0277 6.25 17.2 6.25V7ZM22 11.8H22.75C22.75 10.9723 22.7506 10.3064 22.7066 9.76853C22.662 9.2219 22.5676 8.74175 22.3413 8.29754L21.673 8.63803L21.0048 8.97852C21.1054 9.17604 21.1745 9.4368 21.2116 9.89068C21.2494 10.3533 21.25 10.9475 21.25 11.8H22ZM20.362 7.32698L20.0215 7.99524C20.4448 8.21095 20.789 8.55516 21.0048 8.97852L21.673 8.63803L22.3413 8.29754C21.9817 7.59193 21.4081 7.01825 20.7025 6.65873L20.362 7.32698ZM8.92285 10.5134H8.17285V17.5796H8.92285H9.67285V10.5134H8.92285ZM8.92285 10.5134V11.2634C10.7257 11.2634 12.1155 11.585 13.0271 12.1187C13.9047 12.6326 14.3271 13.3261 14.3271 14.1978H15.0771H15.8271C15.8271 12.7118 15.0471 11.5632 13.785 10.8243C12.5568 10.1052 10.8695 9.76343 8.92285 9.76343V10.5134ZM15.0771 14.1978H14.3271C14.3271 14.7061 14.2418 15.086 14.0918 15.3783C13.946 15.6622 13.7158 15.9097 13.3447 16.1211C12.5598 16.5683 11.1931 16.8296 8.92285 16.8296V17.5796V18.3296C11.2286 18.3296 12.939 18.0787 14.0873 17.4244C14.6827 17.0851 15.1331 16.6344 15.4263 16.0633C15.7152 15.5004 15.8271 14.8682 15.8271 14.1978H15.0771Z" fill="#383E40" stroke-width="inherit" stroke="currentColor"></path></svg> | <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Folder " style="width: calc(1.125rem * var(--mantine-scale)); height: calc(1.125rem * var(--mantine-scale));"><path d="M8.66671 4.66667L7.92301 3.17928C7.70898 2.7512 7.60195 2.53715 7.44229 2.38078C7.30109 2.24249 7.13092 2.13732 6.94409 2.07287C6.73282 2 6.49351 2 6.0149 2H3.46671C2.71997 2 2.3466 2 2.06139 2.14532C1.8105 2.27316 1.60653 2.47713 1.4787 2.72801C1.33337 3.01323 1.33337 3.3866 1.33337 4.13333V4.66667M1.33337 4.66667H11.4667C12.5868 4.66667 13.1469 4.66667 13.5747 4.88465C13.951 5.0764 14.257 5.38236 14.4487 5.75869C14.6667 6.18651 14.6667 6.74656 14.6667 7.86667V10.8C14.6667 11.9201 14.6667 12.4802 14.4487 12.908C14.257 13.2843 13.951 13.5903 13.5747 13.782C13.1469 14 12.5868 14 11.4667 14H4.53337C3.41327 14 2.85322 14 2.42539 13.782C2.04907 13.5903 1.74311 13.2843 1.55136 12.908C1.33337 12.4802 1.33337 11.9201 1.33337 10.8V4.66667Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> <br/> | N/A |
| Resource type | {{{ .dedicated}}} clusters only | TiDB X instances only | TiDB X instances only |
| Project is optional | ❌ <br/>(Each {{{ .dedicated }}} cluster must belong to a dedicated project) | ✅ <br/> (You can either group a TiDB X instance in a TiDB X project or keep it at the organization level) | N/A <br/>(TiDB X instances not grouped in any TiDB X project are automatically grouped in the TiDB X virtual project) |
| Project settings | ✅ | ❌ | ❌ |
| Infrastructure binding | ✅ <br/>(Strong binding) | ❌ | ❌ |
| RBAC model | Organization -> Project | Organization -> Project -> Instance | Organization -> Project -> Instance |
| Project-level RBAC | ✅ | ✅ | ❌ |
| Project-level billing | ✅ | ✅ | ❌ |
| Instance movement between projects | ❌ | ✅ <br/>(You can move a TiDB X instance to a specific TiDB X project or out of any project) | ✅ <br/>(You can move a TiDB X instance out of any TiDB X project to a specific TiDB X project) |

## Do I need to move my {{{ .starter }}} and Essential instances?

It depends on how your current project is structured:

- If your project contains only {{{ .starter }}} and Essential instances, TiDB Cloud converts the project to a TiDB X project automatically on April 15, 2026. No further action is required.
- If your project contains both {{{ .dedicated }}} clusters and {{{ .starter }}} or Essential instances, the TiDB Cloud console prompts you to move the {{{ .starter }}} and Essential instances to a new TiDB X project by clicking **Move & Unlock** in the top banner.

## Who can perform the migration?

Only users with the `Organization Owner` role can start and complete the migration.

## What happens if my project contains only {{{ .starter }}} and Essential instances?

Projects that contain only {{{ .starter }}} and Essential instances are converted to a TiDB X project automatically on April 15, 2026.

What changes after the migration:

- The project becomes a TiDB X project.
- The new TiDB X project does not include dedicated project settings, such as network settings, CMEK settings, and maintenance configurations.

What does not change after the migration:

- Your existing instances and their data, availability, and performance.
- Your billing and usage.
- The project name and project ID.

## What happens if my project contains both {{{ .dedicated }}} clusters and {{{ .starter }}} or Essential instances?

With the introduction of separate project types for different TiDB Cloud resources, a dedicated project can no longer host TiDB X instances.

If a project contains both {{{ .dedicated }}} clusters and {{{ .starter }}} or Essential instances, TiDB Cloud prompts you in the top banner to move the {{{ .starter }}} and Essential instances in the project to a new **TiDB X project**.

> **Note:**
>
> {{{ .dedicated }}} clusters remain in the original project after the migration. Therefore, the migration does not affect {{{ .dedicated }}} clusters.

If you are the `Organization Owner`, you can click **Move & Unlock** in the top banner and follow the migration wizard to complete the migration.

The migration wizard displays a list of {{{ .starter }}} and Essential instances to be moved and lets you specify a new name for the new TiDB X project.

What changes after the migration:

- The {{{ .starter }}} and Essential instances are moved to a newly created TiDB X project.
- The moved instances belong to a new project ID after the migration.
- Project-level RBAC permissions are copied to the new project.

What does not change after the migration:

- Your instance data.
- Your instance availability.
- Your instance performance.
- Your billing and usage.
- The underlying infrastructure of your instances.
- {{{ .dedicated }}} clusters remain in their current projects and are not moved.

There is no additional cost for this migration.

After the migration, you can manage your TiDB X instances through TiDB X projects (or at the organization level), and continue to manage your {{{ .dedicated }}} clusters through dedicated projects.

## What actions are required after migration?

If your {{{ .starter }}} or Essential instances are moved to a new TiDB X project, review anything that depends on the original project ID or original project-level setup, such as the following:

- Automation or scripts
- Integrations
- Project-based operational workflows
- User access and RBAC assignments
- Data Service setup
- Data Apps
- Data Service API keys

Project-level RBAC permissions are copied to the new project, but you should still review access after migration to make sure users and workflows still work as expected.

## Do I need to undeploy my Data Service endpoints before migration?

For projects deployed with [TiDB Cloud Data Service](/tidb-cloud/data-service-overview.md) endpoints, whether you need to undeploy Data Service endpoints before migration depends on how your current project is structured:

- If your project contains only {{{ .starter }}} and Essential instances, because the project ID does not change after the migration, the Data Service endpoints still work after the migration, so no further action is required.
- If your project contains both {{{ .dedicated }}} clusters and {{{ .starter }}} or Essential instances, because these {{{ .starter }}} or Essential instances are moved to new TiDB X projects after the migration, note the following:

    - Those {{{ .starter }}} and Essential instances cannot be moved until their associated endpoints are undeployed.
    - After the migration is complete, you need to redeploy the required endpoints in the new TiDB X project and update your application configuration accordingly.
    - If you use Data Apps or Data Service API keys, review and reconfigure them in the new project as needed. For more information, see [Manage Data Service endpoints](/tidb-cloud/data-service-manage-endpoint.md) and [API Keys in Data Service](/tidb-cloud/data-service-api-key.md).

## Where can I get help?

If you are unsure whether your automation, integrations, or Data Service setup depends on the original project ID, contact TiDB Cloud support at [support@pingcap.com](mailto:support@pingcap.com) before you start the migration.