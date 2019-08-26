---
title: TiDB Lightning
summary: Learn how to restore data into TiDB cluster in Kubernetes fastly with TiDB Lightning.
category: how-to
---

# TiDB Lightning

This document describes how to restore data into TiDB cluster in Kubernetes using [TiDB Lightning](https://github.com/pingcap/tidb-lightning).

TiDB Lightning contains two components: tidb-lightning and tikv-importer. In Kubernetes, the tikv-importer is inside tidb-cluster Helm chart, it's deployed as a `StatefulSet` with `replicas=1` while tidb-lightning is in a separate Helm chart and deployed as a `Job`.

So to restore data with TiDB Lighting, both the tikv-importer and tidb-lightning need to be deployed.

## Deploy tikv-importer

The tikv-importer can be enabled for an existing tidb cluster or by creating a new one.

* Create a new TiDB cluster with tikv importer enabled

    1. Set `importer.create` to `true` in tidb-cluster `values.yaml`

    2. Deploy the cluster

        {{< copyable "shell-regular" >}}

        ```shell
        helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> -f values.yaml --version=<chart-version>
        ```

* Configure an existing TiDB cluster to enable tikv importer

    1. Set `importer.create` to `true` in tidb-cluster `values.yaml`

    2. Upgrade the existing TiDB cluster

        {{< copyable "shell-regular" >}}

        ```shell
        helm upgrade <release-name> pingcap/tidb-cluster -f values.yaml --version=<chart-version>
        ```

## Deploy tidb-lightning

1. Configure TiDB Lightning

    Use the following command to get the default configuration of TiDB Lightning.

    {{< copyable "shell-regular" >}}

    ```shell
    helm inspect values pingcap/tidb-lightning --version=<chart-version> > tidb-lightning-values.yaml
    ```

    TiDB Lightning Helm chart supports both local and remote data source.

    * Local

        Local mode requires the mydumper backup data to be on one of the k8s node. This mode can be enabled by setting `dataSource.local.nodeName` to the node name and `dataSource.local.hostPath` to the mydumper backup data directory path which contains a file named `metadata`.

    * Remote

        Unlike local mode, remote mode needs to use [rclone](https://rclone.org) to download mydumper backup tarball file from a network storage like [Google Cloud Storage (GCS)](https://cloud.google.com/storage/), [AWS S3](https://aws.amazon.com/s3/), [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) etc to a PV. And then extract the tarball file to the PV. Currently, only these three cloud storages are tested. Other cloud storages that are supported by rclone should also work but not tested.

        i. Ensure `dataSource.local.nodeName` and `dataSource.local.hostPath` are commented out.

        ii. Create a `Secret` containing the rclone configuration. A sample configuration is listed below, only one cloud storage configuration is required. For other cloud storage, please refer to rclone [documentation](https://rclone.org/).

        {{< copyable "" >}}

        ```yaml
        apiVersion: v1
        kind: Secret
        metadata:
          name: cloud-storage-secret
        type: Opaque
        stringData:
          rclone.conf: |
          [s3]
          type = s3
          provider = AWS
          env_auth = false
          access_key_id = <my-access-key>
          secret_access_key = <my-secret-key>
          region = us-east-1

          [ceph]
          type = s3
          provider = Ceph
          env_auth = false
          access_key_id = <my-access-key>
          secret_access_key = <my-secret-key>
          endpoint = <ceph-object-store-endpoint>
          region = :default-placement

          [gcs]
          type = google cloud storage
          # The service account must include Storage Object Viewer role
          # The content can be retrieved by `cat <service-account-file.json> | jq -c .`
          service_account_credentials = <service-account-json-file-content>
        ```

        Fill in the placeholders with your configurations and save it as `secret.yaml`, and then create the secret via `kubectl apply -f secret.yaml -n <namespace>`.

        iii. Configure the `dataSource.remote.storageClassName` to an existing storage class in the Kubernetes cluster.

2. Deploy TiDB Lightning

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-lightning --name=<release-name> --namespace=<namespace> -f values.yaml --version=<chart-version>
    ```

When TiDB Lightning fails, it cannot simply be restarted, manual intervention is required. TiDB Lightning chart has hack script which avoids pod exiting and restarting when it fails. This makes it handy to do manual intervention, however users have to check the pod's log instead of simply checking the pod's status to determine if the restore job failed or not. This behavior can be disabled by setting `failFast` to `true` in `values.yaml`.

> **Note:**
>
> Currently, TiDB Lightning will [exit with non-zero error code even when data is successfully restored](https://github.com/pingcap/tidb-lightning/pull/230), this will trigger the job failure. So the success status needs to be determined by viewing tidb-lightning pod's log too.
