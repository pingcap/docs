---
title: Enable TLS Between TiDB Components
summary: Learn how to enable TLS authentication between TiDB components.
aliases: ['/docs/dev/enable-tls-between-components/','/docs/dev/how-to/secure/enable-tls-between-components/']
---

# Enable TLS Between TiDB Components

This document describes how to enable encrypted data transmission between components within a TiDB cluster. Once enabled, encrypted transmission is used between the following components:

- Communication between TiDB, TiKV, PD, and TiFlash
- TiDB Control and TiDB; TiKV Control and TiKV; PD Control and PD
- Internal communication within each TiDB, TiKV, PD, and TiFlash cluster

Currently, it is not supported to only enable encrypted transmission of some specific components.

## Configure and enable encrypted data transmission

1. Prepare certificates.

    It is recommended to prepare a server certificate for TiDB, TiKV, and PD separately. Make sure that these components can authenticate each other. The Control tools of TiDB, TiKV, and PD can choose to share one client certificate.

    You can use tools like `openssl`, `easy-rsa` and `cfssl` to generate self-signed certificates.

    <CustomContent platform="tidb">

    If you choose `openssl`, you can refer to [generating self-signed certificates](/generate-self-signed-certificates.md).

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    If you choose `openssl`, you can refer to [generating self-signed certificates](https://docs.pingcap.com/tidb/stable/generate-self-signed-certificates).

    </CustomContent>

2. Configure certificates.

    To enable mutual authentication among TiDB components, configure the certificates of TiDB, TiKV, and PD as follows.

    - TiDB

        Configure in the configuration file or command-line arguments:

        ```toml
        [security]
        # Path of the file that contains list of trusted SSL CAs for connection with cluster components.
        cluster-ssl-ca = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format for connection with cluster components.
        cluster-ssl-cert = "/path/to/tidb-server.pem"
        # Path of the file that contains X509 key in PEM format for connection with cluster components.
        cluster-ssl-key = "/path/to/tidb-server-key.pem"
        ```

    - TiKV

        Configure in the configuration file or command-line arguments, and set the corresponding URL to `https`:

        ```toml
        [security]
        ## The path for certificates. An empty string means that secure connections are disabled.
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        ca-path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert-path = "/path/to/tikv-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key-path = "/path/to/tikv-server-key.pem"
        ```

    - PD

        Configure in the configuration file or command-line arguments, and set the corresponding URL to `https`:

        ```toml
        [security]
        ## The path for certificates. An empty string means that secure connections are disabled.
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        cacert-path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert-path = "/path/to/pd-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key-path = "/path/to/pd-server-key.pem"
        ```

    - TiFlash (New in v4.0.5)

        Configure in the `tiflash.toml` file:

        ```toml
        [security]
        ## The path for certificates. An empty string means that secure connections are disabled.
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        ca_path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert_path = "/path/to/tiflash-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key_path = "/path/to/tiflash-server-key.pem"
        ```

        Configure in the `tiflash-learner.toml` file:

        ```toml
        [security]
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        ca-path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert-path = "/path/to/tiflash-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key-path = "/path/to/tiflash-server-key.pem"
        ```

    - TiCDC

        Configure in the configuration file:

        ```toml
        [security]
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/cdc-server.pem"
        key-path = "/path/to/cdc-server-key.pem"
        ```

        Alternatively, configure in the command-line arguments and set the corresponding URL to `https`:

        {{< copyable "shell-regular" >}}

        ```bash
        cdc server --pd=https://127.0.0.1:2379 --log-file=ticdc.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301 --ca=/path/to/ca.pem --cert=/path/to/ticdc-cert.pem --key=/path/to/ticdc-key.pem
        ```

    - TiProxy

        Configure in the configuration file, and set the corresponding URL to `https`:

        ```toml
        [security]
            [server-http-tls]
            ca = "/path/to/ca.pem"
            cert = "/path/to/tiproxy-server.pem"
            key = "/path/to/tiproxy-server-key.pem"
        ```

        Now, encrypted transmission among TiDB components is enabled.

    > **Note:**
    >
    > After enabling encrypted transmission in a TiDB cluster, if you need to connect to the cluster using tidb-ctl, tikv-ctl, pd-ctl, or tiproxyctl, specify the client certificate. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-ctl -u https://127.0.0.1:10080 --ca /path/to/ca.pem --ssl-cert /path/to/client.pem --ssl-key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    ./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
    ```

### Verify component caller's identity

In general, the callee needs to verify the caller's identity using `Common Name`, in addition to verifying the key, the certificates, and the CA provided by the caller. For example, TiKV can only be accessed by TiDB, and other visitors are blocked even though they have legitimate certificates.

To verify the caller's identity for a component, you need to mark the certificate user identity using `Common Name` when generating the certificate, and check the caller's identity by configuring `cluster-verify-cn` (in TiDB) or `cert-allowed-cn` (in other components) for the callee.

> **Note:**
>
> - Starting from v8.4.0, the PD configuration item `cert-allowed-cn` supports multiple values. You can configure multiple `Common Name` in the `cluster-verify-cn` configuration item for TiDB and in the `cert-allowed-cn` configuration item for other components as needed. Note that TiUP uses a separate identifier when querying component status. For example, if the cluster name is `test`, TiUP uses `test-client` as the `Common Name`.
> - For v8.3.0 and earlier versions, the PD configuration item `cert-allowed-cn` can only be set to a single value. Therefore, the `Common Name` of all authentication objects must be set to the same value. For related configuration examples, see [v8.3.0 documentation](https://docs-archive.pingcap.com/tidb/v8.3/enable-tls-between-components/).

- TiDB

    Configure in the configuration file or command-line arguments:

    ```toml
    [security]
    cluster-verify-cn = ["tidb", "tiproxy", "test-client", "prometheus"]
    ```

- TiKV

    Configure in the configuration file or command-line arguments:

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "pd", "tikv", "tiflash", "prometheus"]
    ```

- PD

    Configure in the configuration file or command-line arguments:

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "pd", "tikv", "tiflash", "tiproxy", "test-client", "prometheus"]
    ```

- TiFlash (New in v4.0.5)

    Configure in the `tiflash.toml` file or command-line arguments:

    ```toml
    [security]
    cert_allowed_cn = ["tidb", "tikv", "prometheus"]
    ```

    Configure in the `tiflash-learner.toml` file:

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "tikv", "tiflash", "prometheus"]
    ```

- TiProxy (New in v1.4.0)

    Configure in the configuration file:

    ```toml
    [security]
        [server-http-tls]
        cert-allowed-cn = ["tiproxy", "tidb", "test-client", "prometheus"]
    ```

## Validate TLS between TiDB components

After configuring TLS for communication between TiDB components, you can use the following commands to verify that TLS has been successfully enabled. These commands print the certificate and TLS handshake details for each component.

- TiDB

    ```sh
    openssl s_client -connect <tidb_host>:10080 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

- PD

    ```sh
    openssl s_client -connect <pd_host>:2379 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

- TiKV

    ```sh
    openssl s_client -connect <tikv_host>:20160 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

- TiFlash (New in v4.0.5)

    ```sh
    openssl s_client -connect <tiflash_host>:<tiflash_port> -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

- TiProxy

    ```sh
    openssl s_client -connect <tiproxy_host>:3080 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

## Reload certificates

- If your TiDB cluster is deployed in a local data center, to reload the certificates and keys, TiDB, PD, TiKV, TiFlash, TiCDC, TiProxy, and all kinds of clients reread the current certificates and key files each time a new connection is created, without restarting the TiDB cluster.

- If your TiDB cluster is deployed on your own managed cloud, make sure that the issuance of TLS certificates is integrated with the certificate management service of the cloud provider. The TLS certificates of the TiDB, PD, TiKV, TiFlash, TiCDC, and TiProxy components can be automatically rotated without restarting the TiDB cluster.

## Certificate validity

You can customize the validity period of TLS certificates for each component in a TiDB cluster. For example, when using OpenSSL to issue and generate TLS certificates, you can set the validity period via the **days** parameter. For more information, see [Generate self-signed certificates](/generate-self-signed-certificates.md).

## See also

- [Enable TLS Between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md)
