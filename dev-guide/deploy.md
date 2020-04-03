---
title: Build for Deployment
draft: true
---

# Build for Deployment

The easiest way to deploy TiDB is to use Docker Compose, see [TiDB Docker Compose Deployment](https://pingcap.com/docs/dev/how-to/get-started/deploy-tidb-from-docker-compose/). For more deployment methods, see [TiDB deployment methods](/_index.md).

## Before you begin

You need to check the [supported platforms](/dev-guide/requirements.md#supported-platforms) and [prerequisites](/dev-guide/requirements.md#prerequisites) first.

## Build and install TiDB components

You can use the [build script](/scripts/build.sh) to build and install TiDB components in the `bin` directory.

You can use the [update script](/scripts/update.sh) to update all the TiDB components to the latest version.
