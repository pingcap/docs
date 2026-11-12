---
title: TiDB Cloud Filesystem Onboarding Best Practices
summary: Prepare a TiDB Cloud Filesystem workload for production by choosing a workspace-to-file-system model, region, network path, credentials, access method, and usage limits, and then running a pre-launch check.
---

# TiDB Cloud Filesystem Onboarding Best Practices

This guide describes the decisions that have the largest impact when you move an application, automation platform, or AI agent product onto TiDB Cloud Filesystem: how workspaces map to file systems, where file systems live, how clients reach them, which credentials each component holds, and how to finish writes safely. It ends with a pre-launch check that you can run before production traffic arrives.

Make these decisions during the proof of concept (PoC), with the same compute environment, network path, and file sizes that you plan to use in production. Record the results so that you can compare them with production behavior after launch.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice. No service-level agreement (SLA) is available during public preview, so keep a copy of important data outside TiDB Cloud Filesystem.

## Step 1. Choose how workspaces map to file systems

Most products have a unit of isolation, such as a website, project, end user, or customer organization. In this guide, that unit is called a *workspace*. Decide how workspaces map to file systems before you write any provisioning code, because changing the model later requires moving data.

### One file system per workspace

Create a dedicated file system for each workspace. This model is similar to giving each generated website its own database.

- **Isolation:** a workspace boundary is a file system boundary. A token issued for one file system cannot access another file system.
- **Lifecycle:** deleting a workspace means deleting its file system. Usage limits, storage, and file counts apply to that workspace only.
- **Attribution:** you can attribute usage to a workspace by file system.

Plan for the following when you choose this model:

- Without a credit card, each organization can create only one file system per region. Add a credit card to your organization before you create a file system for each workspace. For more information, see [Manage Usage Limits](/tidb-cloud-filesystem/manage-filesystem-limits.md).
- Creating a file system is a control-plane operation that requires TiDB Cloud API credentials. Run it from a trusted backend service, not from the environment where the workspace runs.
- Measure creation time during the PoC. If a workspace must be ready faster than a file system can be created, create file systems ahead of demand and assign one when a workspace is created.
- Give every file system a display name and labels that identify its owner, so that you can find and clean up file systems later:

    ```shell
    ti fs create-file-system \
      --display-name "ws-<workspace-id>" \
      --label app=<app-name> \
      --label environment=production \
      --label workspace=<workspace-id> \
      --wait
    ```

    Then find file systems by label in the selected region:

    ```shell
    ti fs list-file-systems --label workspace=<workspace-id>
    ```

    Do not put credentials, connection strings, private paths, or personal data in display names or labels.

### One directory per workspace in a shared file system

Create one file system per product environment, and give each workspace its own directory, such as `/workspaces/<workspace-id>`. Each workspace receives a [scoped token](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens) that is limited to its directory.

- **Scale:** creating a workspace only creates a directory and a token, so you do not need a file system per workspace.
- **Sharing:** workspaces can share common data, such as a read-only dataset under `/shared`, through additional scoped permissions.
- **Isolation:** the file system service enforces the path prefix and operations of each scoped token, including through mounts. A prefix matches whole path segments, so a token for `/workspaces/ws-a` cannot access `/workspaces/ws-ab`.

Plan for the following when you choose this model:

- Usage limits, such as storage and file count, apply to the whole file system, so one workspace can consume capacity that other workspaces need. Track usage per directory in your application if you need per-workspace quotas.
- Create the workspace directory before you generate its scoped token.
- Deleting a workspace means deleting its directory and revoking its tokens.

### Choose a model

| Question | If yes |
| --- | --- |
| Do your customers require that their files are stored in separate resources, or do you need per-workspace usage limits? | One file system per workspace |
| Do you create many workspaces per minute, or many short-lived workspaces? | One directory per workspace |
| Do workspaces need to share files? | One directory per workspace |
| Do you serve a small number of large customers, each with many workspaces? | One file system per customer, with one directory per workspace |

In every model, use separate file systems for development, staging, and production, and do not give the same owner token to more than one environment.

## Step 2. Choose a region

Create each file system in the [supported region](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions) that is closest to the compute that reads and writes it, such as agent sandboxes, application servers, or CI runners. The location of your developers or your office does not matter for production latency.

- A file system and its tokens belong to one region. A token works only with the endpoint of its own region.
- If your compute runs in several regions, create file systems in each region instead of sending all traffic to one region.
- If you also use a TiDB Cloud Starter instance for structured data, create it in the same region when both services are available there.

Measure latency from the production compute environment, not from a laptop. For example, run the following command several times and compare the `total` values:

```shell
curl -s -o /dev/null \
  -w 'dns=%{time_namelookup} tls=%{time_appconnect} total=%{time_total}\n' \
  https://<region-code>.drive9.ai/healthz
```

If your environment routes traffic through a proxy, connection timings can appear close to zero because they measure the connection to the proxy. Use the `total` value in this case.

## Step 3. Prepare the network path

TiDB Cloud Filesystem is accessed through public HTTPS endpoints. Clients connect to the regional endpoint `https://<region-code>.drive9.ai`. Large files are transferred directly between the client and the cloud object storage of the file system region by using presigned HTTPS URLs. For example, in AWS regions, these transfers go to Amazon S3 endpoints such as `*.s3.<aws-region>.amazonaws.com`.

If the compute environment restricts outbound traffic, configure the following before the PoC:

- Allow HTTPS to the regional endpoint and to the object storage endpoints of the same region. If you allow only the regional endpoint, small files work but large file uploads and downloads fail.
- If a proxy inspects TLS traffic, make sure that it trusts and forwards both endpoints without rewriting request bodies or headers.
- Mounts keep long-lived HTTPS connections open to receive change notifications. Make sure that proxies and load balancers do not buffer these responses or close idle connections after less than 60 seconds.

TiDB Cloud Filesystem does not provide private endpoints. If the same application also uses a TiDB Cloud Starter instance, you can connect to that instance through a [private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) while file system traffic continues to use HTTPS.

Verify the network path with a round trip of a file that is larger than a few MiB, such as 64 MiB, from the production compute environment:

```shell
head -c 67108864 /dev/urandom > roundtrip.bin
ti fs copy-file --from-local roundtrip.bin --to-remote /onboarding-check/roundtrip.bin --overwrite
ti fs copy-file --from-remote /onboarding-check/roundtrip.bin --to-local roundtrip.out
shasum -a 256 roundtrip.bin roundtrip.out
ti fs delete-file --path /onboarding-check/roundtrip.bin
```

The two checksums must match.

## Step 4. Give each component the least privilege it needs

TiDB Cloud Filesystem uses [three credential types](/tidb-cloud-filesystem/filesystem-authorization.md). Assign them as follows:

| Component | Credential | Where to keep it |
| --- | --- | --- |
| Provisioning service that creates and deletes file systems | TiDB Cloud API key | A secret manager used only by that service |
| Backend service that issues workspace access | Owner token | A secret manager used only by that service |
| Workspace runtime, such as an agent sandbox or a CI job | Scoped token with a time to live (TTL) | Environment variables injected at startup |

Generate a scoped token for each workspace or session on the backend, and grant only the operations that the workspace needs. Use `--subject` to record which workspace or session the token belongs to:

```shell
ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --subject "ws-<workspace-id>" \
  --ttl 8h \
  --allow /workspaces/<workspace-id>:read,list,search,write,delete \
  --query fs_token --output text
```

In the workspace runtime, provide only the scoped token and the region, and run commands against the allowed path:

```shell
export TI_FS_TOKEN="<scoped-token>"
export TI_REGION_CODE="<region-code>"
ti fs list-files --path /workspaces/<workspace-id>
```

Follow these practices:

- Do not copy the `~/.ti/` directory, an owner token, or TiDB Cloud API keys into a workspace runtime.
- Choose a TTL that matches the expected session length, and issue a new token when a session continues. A scoped token can be refreshed with [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md), but refreshing does not broaden its permissions.
- Revoke the tokens of a workspace when it ends with [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md). Revoking an owner token does not revoke the scoped tokens that it created.
- `ti fs check-file-system` checks the root of the file system, so it reports a failure for a token that is limited to a directory even when the token works. To check a scoped token, list its allowed path instead.

During the PoC, verify isolation with a scoped token. Writing to another workspace and listing the parent directory must both fail:

```shell
ti fs copy-file --from-local test.txt --to-remote /workspaces/<other-workspace-id>/test.txt
ti fs list-files --path /workspaces
```

## Step 5. Choose an access method

Choose the access method based on how the workspace uses files:

- **CLI commands:** use `ti fs` commands such as `copy-file` and `read-file` in CI jobs and scripts that move whole files. They do not require a mount. For more information, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md).
- **SDKs:** use an SDK when your application reads and writes files in code. Set the server URL to the regional endpoint and pass a file system token as the API key. Pin the SDK version that you validated in the PoC. For more information, see [SDKs](/tidb-cloud-filesystem/filesystem-sdks.md).
- **Mounts:** mount the file system when tools need local file paths, for example, a coding agent that runs compilers and test commands. For more information, see [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md).

If you mount file systems, follow these practices:

- On Linux, provide `/dev/fuse` and the `fuse3` package to the container or virtual machine. On macOS, mounts use WebDAV by default. Specify `--driver fuse` when you need FUSE-only features, such as layers, checkpoints, and `drain-file-system`.
- For a coding agent, use `--mount-profile coding-agent` so that dependency trees, build output, caches, and Git internals stay on the local disk.
- Mount only the workspace directory with `--remote-path`, and use `--read-only` for reviewers and other readers.
- Verify each mount before an application uses it. For more information, see [Verify a mount before using it](/tidb-cloud-filesystem/filesystem-mount.md#verify-a-mount-before-using-it).

To let an agent try changes without modifying the shared files, create a [layer](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) for each attempt, and commit or abandon the layer when the attempt ends.

## Step 6. Finish writes before you remove a machine

FUSE mounts can buffer writes locally before sending them to the file system. If you delete a sandbox, container, or virtual machine while writes are still buffered, those writes are lost.

- Before you remove a machine, stop writers and run `ti fs unmount-file-system`. A normal FUSE unmount drains pending writes. Remove the machine only after the unmount succeeds.
- To make updates visible to another environment while the mount keeps running, run `ti fs drain-file-system`. WebDAV mounts do not support `drain-file-system`.
- If a drain or unmount fails, keep the machine available until you resolve the error and verify that required files have reached the file system.
- Data that the `coding-agent` mount profile keeps on the local disk disappears with that disk. Rebuild it in the next environment, or pack it before you remove the machine.

For more information, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

## Step 7. Plan usage limits and cleanup

Without a credit card, each organization can create one file system per region, and each file system can store up to 2,000 files and 2 GiB of data, with a maximum single file size of 500 MiB. When a file system reaches its storage or file count limit, existing files remain readable, but new writes are rejected.

- Before launch, estimate peak storage, file count, and maximum file size for each file system, and set its usage limits with headroom. For more information, see [Manage Usage Limits](/tidb-cloud-filesystem/manage-filesystem-limits.md).
- Review [TiDB Cloud Filesystem pricing](https://www.pingcap.com/tidb-cloud-filesystem-pricing-details/) for reads, writes, storage, and internet egress.
- Run a periodic job that compares file systems or workspace directories with the workspaces in your application, and removes those that no longer have an owner. Deleting a file system permanently removes its data, so unmount clients and confirm ownership first.

## Step 8. Run a pre-launch check

Before production traffic arrives, run the following checks from the production environment and record the results.

| Area | Check | How to verify |
| --- | --- | --- |
| Resource model | The workspace-to-file-system model is chosen and documented. | Review the decision from Step 1. |
| Resource model | Development, staging, and production use separate file systems. | Run `ti fs list-file-systems` in each region. |
| Resource model | Every file system has owner labels. | Run `ti fs list-file-systems --label app=<app-name>`. |
| Region | File systems are in the same region as their compute. | Compare the file system region with the compute region. |
| Network | Large files reach object storage. | A 64 MiB round trip from Step 3 has matching checksums. |
| Network | Latency is measured from production compute. | Record `total` values from Step 2. |
| Credentials | Workspace runtimes hold only scoped tokens with a TTL. | Inspect the environment of a running workspace. |
| Credentials | A scoped token cannot access another workspace. | The isolation checks from Step 4 fail as expected. |
| Credentials | Token revocation works. | Revoke a test token and confirm that the next request is rejected. |
| Durability | Teardown waits for a successful unmount. | Write a file, unmount, remove the machine, and read the file from another environment. |
| Usage limits | Limits cover expected peak usage with headroom. | Compare the configured limits with your estimate. |
| Cleanup | Orphaned file systems, directories, and tokens are removed. | Run the cleanup job against a test workspace. |
| Support | You can identify the failing resource quickly. | Record the file system ID, region, `ti --version`, and time of each test. |

When you contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md), include the file system ID, region, CLI or SDK version, the command or API call, the time of the failure, and the error message. Do not include tokens or API keys.

## What's next

- [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md)
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md)
- [Automation and AI Agent Workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)
