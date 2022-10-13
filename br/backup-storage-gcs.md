---
title: Back Up and Restore Data on Google Cloud Storage Using BR
summary: Learn how to use BR to back up and restore data on Google Cloud Storage.
---

# BR を使用した Google Cloud Storage でのデータのバックアップと復元 {#back-up-and-restore-data-on-google-cloud-storage-using-br}

バックアップと復元 (BR) ツールは、データのバックアップと復元のための外部ストレージとして Google Cloud Storage (GCS) の使用をサポートしています。

## ユーザーシナリオ {#user-scenario}

Google Compute Engine (GCE) にデプロイされた TiDB クラスターのデータを GCS にすばやくバックアップしたり、GCS のバックアップ データから TiDB クラスターをすばやく復元したりできます。

## データを GCS にバックアップする {#back-up-data-to-gcs}

{{< copyable "" >}}

```shell
br backup full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

データを GCS にバックアップする場合、BR が実行されているノードに認証情報ファイルを配置する必要があります。認証情報ファイルには、GCS にアクセスするためのアカウント認証情報が含まれています。 `--send-credentials-to-tikv`が表示された場合、GCS のアカウント アクセス資格情報が TiKV ノードに渡されることを意味します。

認証情報ファイルを取得するには、 [GCS 認証情報ファイルを作成してダウンロードする](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/google_cloud_backup_guide/creds)を参照してください。

## GCS からデータを復元する {#restore-data-from-gcs}

{{< copyable "" >}}

```shell
br restore full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

## こちらもご覧ください {#see-also}

BR でサポートされているその他の外部ストレージについては、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。
