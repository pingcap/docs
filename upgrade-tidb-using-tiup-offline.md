---
title: Upgrade TiDB Using TiUP Offline Mirror
summary: Learn how to upgrade TiDB using the TiUP offline mirror.
category: how-to
---

# Upgrade TiDB Using TiUP Offline Mirror

This document describes how to upgrade TiDB using TiUP offline mirror.

## Update TiUP offline mirror

1. To update the local TiUP offline mirror, refer to Step 1 and Step 2 in [Deploy a TiDB Cluster Offline Using TiUP](/production-offline-deployment-using-tiup.md) to download and deploy the new version of the TiUP offline mirror.

    After you execute `local_install.sh`, TiUP completes the overwrite upgrade.

2. Redeclare the global environment variables according to the result of `local_install.sh`. Set `TIUP_MIRRORS` to `/path/to/mirror`, the location of the offline mirror package printed by `local_install.sh`.

    {{< copyable "shell-regular" >}}

    ```bash
    source .bash_profile
    export TIUP_MIRRORS=/path/to/mirror
    ```

    The offline mirror is successfully updated. After the overwrite upgrade, if an error is reported when TiUP is running, the cause might be that `manifest` is not updated. You can execute `rm -rf ~/.tiup/manifests` before using TiUP.

## Update TiDB cluster

After the local mirror is updated, refer to [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md) to upgrade the TiDB cluster.
