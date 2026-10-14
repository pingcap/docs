---
title: Platforms & Regions
summary: Learn about the supported cloud platforms and regions for TiDB Cloud Lake.
---

# Platforms & Regions

{{{ .lake }}} is a cloud-native solution that currently supports the following cloud providers and regions:

| Cloud Provider | Region Name              | Region ID      |
|----------------|--------------------------|----------------|
| AWS            | US West (Oregon)         | us-west-2      |
| AWS            | Asia Pacific (Tokyo)     | ap-northeast-1 |
| AWS            | US East (N. Virginia)    | us-east-1      |
| AWS            | Asia Pacific (Singapore) | ap-southeast-1 |
| AWS            | Asia Pacific (Mumbai)    | ap-south-1     |
| Alibaba Cloud  | Japan (Tokyo)            | ap-northeast-1 |

> **Note:**
>
> - For efficient and stable data synchronization and import, it is strongly recommended to choose a cloud provider and region that match your current environment. This configuration reduces cross-network transfers and the associated risks of network latency and data loss, ensuring security and smoothness of the data transmission process.
> - {{{ .lake }}} plans to expand support for more cloud providers and regions. If your current cloud provider or region is not supported, please click [Contact Sales](https://www.pingcap.com/contact-us/) to get in touch with the {{{ .lake }}} team.

When you sign up for a {{{ .lake }}} account, you will need to select a cloud platform and region. Once the account is successfully created, the selected cloud platform and region cannot be changed.
