---
title: Back Up and Restore Data on Google Cloud Storage Using BR
summary: Learn how to use BR to back up and restore data on Google Cloud Storage.
---

# BRを使用してGoogleCloudStorageのデータをバックアップおよび復元する {#back-up-and-restore-data-on-google-cloud-storage-using-br}

Backup＆Restore（BR）ツールは、データをバックアップおよび復元するための外部ストレージとしてGoogle Cloud Storage（GCS）を使用することをサポートしています。

## ユーザーシナリオ {#user-scenario}

Google Compute Engine（GCE）にデプロイされたTiDBクラスタのデータをGCSにすばやくバックアップしたり、GCSのバックアップデータからTiDBクラスタをすばやく復元したりできます。

## データをGCSにバックアップする {#back-up-data-to-gcs}

{{< copyable "" >}}

```shell
br backup full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

データをGCSにバックアップするときは、BRが実行されているノードにクレデンシャルファイルを配置する必要があります。クレデンシャルファイルには、GCSにアクセスするためのアカウントクレデンシャルが含まれています。 `--send-credentials-to-tikv`が表示されている場合は、GCSのアカウントアクセスクレデンシャルがTiKVノードに渡されることを意味します。

クレデンシャルファイルを取得するには、 [GCSクレデンシャルファイルを作成してダウンロードする](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/google_cloud_backup_guide/creds)を参照してください。

## GCSからデータを復元する {#restore-data-from-gcs}

{{< copyable "" >}}

```shell
br restore full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

## も参照してください {#see-also}

BRでサポートされている他の外部ストレージについては、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。
