---
title: Customize a Secret Key for DM Encryption and Decryption
summary: Learn how to customize a secret key to encrypt and decrypt passwords used in the DM（Data Migration）data source and migration task configurations.
---

# Customize a Secret Key for DM Encryption and Decryption

Before v8.0.0, [DM](/dm/dm-overview.md) uses a [fixed AES-256 secret key](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27) to encrypt and decrypt passwords in the data source and migration task configurations. However, using a fixed secret key might pose security risks, especially in environments where security is crucial. To enhance security, starting from v8.0.0, DM removes the fixed secret key and enables you to customize a secret key.

## Usage

1. Create a custom key file, which must contain a 64-character hexadecimal AES-256 secret key.
2. In the DM-master [command-line flags](/dm/dm-command-line-flags.md) or [configuration file](/dm/dm-master-configuration-file.md), specify `secret-key-path` as the path of your custom key file.

## Upgrade from a version earlier than v8.0.0

Because DM no longer uses the fixed secret key starting from v8.0.0, pay attention to the following when upgrading DM from versions earlier than v8.0.0:

- If plaintext passwords are used in both [data source configurations](/dm/dm-source-configuration-file.md) and [migration task configurations](/dm/task-configuration-file-full.md), no additional steps are required for the upgrade.
- If encrypted passwords are used in [data source configurations](/dm/dm-source-configuration-file.md) and [migration task configurations](/dm/task-configuration-file-full.md) or if you want to use encrypted passwords in the future, you need to do the following:
    1. Add the `secret-key-path` parameter to the [DM-master configuration file](/dm/dm-master-configuration-file.md) and specify it as the path of your custom key file. The file must contain a 64-character hexadecimal AES-256 key. If the [fixed AES-256 secret key](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27) was used for encryption before upgrading, you can copy this secret key to your key file. Make sure all DM-master nodes use the same secret key configuration.
    2. Perform a rolling upgrade of DM-master first, followed by a rolling upgrade of DM-worker. For more information, see [Rolling upgrade](/dm/maintain-dm-using-tiup.md#rolling-upgrade).

## Update the secret key for encryption and decryption

To update the secret key used for encryption and decryption, take the following steps:

1. Update `secret-key-path` in the [DM-master configuration file](/dm/dm-master-configuration-file.md).

    > **Note:**
    >
    > - Make sure all DM-master nodes are updated to the same secret key configuration.
    > - During the secret key update, do not create new [data source configuration files](/dm/dm-source-configuration-file.md) or [migration task configuration files](/dm/task-configuration-file-full.md).

2. Perform a rolling restart of DM-master.
3. Use the passwords encrypted with `tiup dmctl encrypt` (dmctl version >= v8.0.0) when you create new [data source configuration files](/dm/dm-source-configuration-file.md) and [migration task configuration files](/dm/task-configuration-file-full.md).