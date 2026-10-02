---
title: SDKs
summary: Learn how TiDB Cloud Filesystem relates to the Drive9 workspace engine and find client SDK documentation for six programming languages.
---

# SDKs

TiDB Cloud Filesystem uses the Drive9 workspace engine to run file system operations. TiDB Cloud Filesystem is PingCAP's official hosted Drive9 service on TiDB Cloud. Drive9 is an open-source, community-based project owned by PingCAP, and TiDB Cloud Filesystem is its managed cloud service. At the API and SDK layers, you directly invoke the drive9 endpoints exposed by TiDB Cloud Filesystem service. 

Drive9 is an open-source project (Apache 2.0) maintained in the [mem9-ai/drive9 repository](https://github.com/mem9-ai/drive9). Besides the workspace engine, that repository publishes client SDKs for several programming languages. The SDKs and their documentation are maintained there, so the guides listed on this page are the source of truth for SDK installation, configuration, and API details.

The SDK guides describe how a client connects to a Drive9 server, including how to provide the server URL and an API key.

The API Keys mentioned in Drive9 SDK/API documentations.

|TiDB Cloud Filesystem Object|Drive9 SDK/API Usage|
|:--|:--|
|TiDB Cloud API Key|File system control plane actions|
|File System Token|File system data plane actions|

Available server URL for Drive9 SDK/API server URL to TiDB Cloud Filesystem regions.

| TiDB Cloud Filesystem Region| Server URL for Drive9 SDK/API | API Key|
|:--|:--|:--|
|`aws-us-east-1`|`https://aws-us-east-1.drive9.ai`| FS token|
|`aws-us-west-2`|`https://aws-us-west-2.drive9.ai`| FS token|
|`aws-ap-southeast-1`|`https://aws-ap-southeast-1.drive9.ai`| FS token|
|`gcp-us-east1`|`https://gcp-us-east-1.drive9.ai`| FS token|
|`azure-centralus`|`https://azure-centralus.drive9.ai`|FS token|
|`alicloud-ap-southeast-1`|`https://alicloud-ap-southeast-1.drive9.ai`|FS token|

## Available SDKs

| Language | Repository location | Documentation |
| --- | --- | --- |
| TypeScript | `clients/drive9-js` | [TypeScript SDK integration guide](https://github.com/mem9-ai/drive9/blob/main/docs/guides/typescript-sdk-integration.md) |
| Go | `pkg/client` | [Go SDK integration guide](https://github.com/mem9-ai/drive9/blob/main/docs/guides/go-sdk-integration.md) |
| Python | `clients/drive9-py` | [drive9-py README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-py/README.md) |
| Rust | `clients/drive9-rs` | [drive9-rs README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-rs/README.md) |
| Kotlin | `clients/drive9-kotlin` | [drive9-kotlin README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-kotlin/README.md) |
| Swift | `clients/drive9-swift` | [drive9-swift README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-swift/README.md) |

The SDKs are developed and released with the Drive9 project, so they can move ahead of the TiDB Cloud Filesystem service. Before you adopt an SDK for a TiDB Cloud Filesystem workload, check its documentation for the current server endpoint, credentials, and supported operations.

## What's next

- [TiDB Cloud CLI (`ti`)](/ai/ti/ti-quick-start.md) to install, configure, and update the CLI.
- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) to manage file system data from the command line.
- [Automation and AI Agent Workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md) to use a file system in automated workflows.
