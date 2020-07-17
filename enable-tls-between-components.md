---
title: Enable TLS Between TiDB Components
summary: Learn how to enable TLS authentication between TiDB components.
aliases: ['/docs/dev/enable-tls-between-components/','/docs/dev/how-to/secure/enable-tls-between-components/']
---

# Enable TLS Between TiDB Components

This document describes how to enable encrypted data transmission between components within a TiDB cluster. Once enabled, encrypted transmission is used between the following components:

- TiDB and TiKV; TiDB and PD
- TiKV and PD
- TiDB Control and TiDB; TiKV Control and TiKV; PD Control and PD
- Internal communication within each TiKV, PD, TiDB cluster

Currently, it is not supported to only enable encrypted transmission of some specific components.

## Configure and enable encrypted data transmission

1. Prepare certificates.

    It is recommended to prepare a server certificate for TiDB, TiKV, and PD separately. Make sure that these components can authenticate each other. The Control tools of TiDB, TiKV, and PD can choose to share one client certificate.

    You can use tools like `openssl`, `easy-rsa` and `cfssl` to generate self-signed certificates.

    If you choose `openssl`, you can refer to [generating self-signed certificates](/generate-self-signed-certificates.md).

2. Configure certificates.

   To enable mutual authentication among TiDB components, configure the certificates of TiDB, TiKV, and PD as follows.

   - TiDB

        Configure in the configuration file or command line arguments:

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs for connection with cluster components.
        cluster-ssl-ca = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format for connection with cluster components.
        cluster-ssl-cert = "/path/to/tidb-server.pem"
        # Path of file that contains X509 key in PEM format for connection with cluster components.
        cluster-ssl-key = "/path/to/tidb-server-key.pem"
        ```

   - TiKV

        Configure in the configuration file or command line arguments, and set the corresponding URL to https:

        ```toml
        [security]
        # set the path for certificates. Empty string means disabling secure connections.
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/tikv-server.pem"
        key-path = "/path/to/tikv-server-key.pem"
        ```

   - PD

        Configure in the configuration file or command line arguments, and set the corresponding URL to https:

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs. If set, following four settings shouldn't be empty
        cacert-path = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format.
        cert-path = "/path/to/pd-server.pem"
        # Path of file that contains X509 key in PEM format.
        key-path = "/path/to/pd-server-key.pem"
        ```

    Now, encrypted transmission among TiDB components is enabled.

    > **Note:**
    >
    > After enabling encrypted transmission in a TiDB cluster, if you need to connect to the cluster using tidb-ctl, tikv-ctl, or pd-ctl, specify the client certificate. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-ctl -u https://127.0.0.1:10080 --ca /path/to/ca.pem --ssl-cert /path/to/client.pem --ssl-key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    ./pd-ctl -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    ./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
    ```

### Verify component caller's identity

The Common Name is used for caller verification. In general, the callee needs to verify the caller's identity, in addition to verifying the key, the certificates, and the CA provided by the caller. For example, TiKV can only be accessed by TiDB, and other visitors are blocked even though they have legitimate certificates.

To verify component caller's identity, you need to mark the certificate user identity using `Common Name` when generating the certificate, and to check the caller's identity by configuring the `Common Name` list for the callee.

- TiDB

    Configure in the configuration file or command line arguments:

    ```toml
    [security]
    cluster-verify-cn = [
        "TiDB-Server",
        "TiKV-Control",
    ]
    ```

- TiKV

    Configure in the configuration file or command line arguments:

    ```toml
    [security]
    cert-allowed-cn = [
        "TiDB-Server", "PD-Server", "TiKV-Control", "RawKvClient1",
    ]
    ```

- PD

    Configure in the configuration file or command line arguments:

    ```toml
    [security]
    cert-allowed-cn = ["TiKV-Server", "TiDB-Server", "PD-Control"]
    ```

### Reload certificates

To reload the certificates and the keys, TiDB, PD, TiKV, and all kinds of clients reread the current certificates and the key files each time a new connection is created. Currently, you cannot reload the CA certificate.

## See also

- [Enable TLS Between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md)
