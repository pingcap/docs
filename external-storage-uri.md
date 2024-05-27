---
title: URI Formats of External Storage Services
summary: Amazon S3、GCS、Azure Blob Storage などの外部storageサービスのstorageURI 形式について説明します。
---

## 外部ストレージサービスの URI 形式 {#uri-formats-of-external-storage-services}

このドキュメントでは、Amazon S3、GCS、Azure Blob Storage などの外部storageサービスの URI 形式について説明します。

URI の基本的な形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

## Amazon S3 URI 形式 {#amazon-s3-uri-format}

-   `scheme` : `s3`
-   `host` : `bucket name`
-   `parameters` :

    -   `access-key` : アクセスキーを指定します。
    -   `secret-access-key` : 秘密アクセスキーを指定します。
    -   `session-token` : 一時セッション トークンを指定します。BRはv7.6.0 以降でこのパラメータをサポートしています。
    -   `use-accelerate-endpoint` : Amazon S3 の高速エンドポイントを使用するかどうかを指定します (デフォルトは`false` )。
    -   `endpoint` : S3 互換サービスのカスタムエンドポイントの URL を指定します (例: `<https://s3.example.com/>` )。
    -   `force-path-style` : 仮想ホスト形式のアクセスではなく、パス形式のアクセスを使用します (デフォルトは`true` )。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`STANDARD_IA` )。
    -   `sse` : アップロードされたオブジェクトの暗号化に使用されるサーバー側暗号化アルゴリズムを指定します (値のオプション: ``、 `AES256` 、または`aws:kms` )。
    -   `sse-kms-key-id` : `sse`が`aws:kms`に設定されている場合は KMS ID を指定します。
    -   `acl` : アップロードされたオブジェクトの既定 ACL を指定します (たとえば、 `private`または`authenticated-read` )。
    -   `role-arn` : 指定された[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)を使用してサードパーティの Amazon S3 データにアクセスする必要がある場合は、 `arn:aws:iam::888888888888:role/my-role`などの`role-arn` URL クエリパラメータを使用して、 IAMロールの対応する[Amazon リソース名 (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)指定できます。IAM ロールを使用してサードパーティの Amazon S3 データにアクセスする方法の詳細については、 [AWS ドキュメント](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)を参照してください。BRは、 v7.6.0 以降でこのパラメータをサポートしています。
    -   `external-id` : サードパーティから Amazon S3 データにアクセスする場合、正しい[外部ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html)を指定して[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)引き受けなければならない場合があります。この場合、この`external-id` URL クエリパラメータを使用して外部 ID を指定し、 IAMロールを引き受けることができることを確認できます。外部 ID は、Amazon S3 データにアクセスするためにIAMロール ARN とともにサードパーティによって提供される任意の文字列です。IAM ロールを引き受ける場合、外部 ID の提供はオプションです。つまり、サードパーティがIAMロールの外部 ID を必要としない場合は、IAMIAMを引き受け、対応する Amazon S3 データにアクセスできます。

以下は、 TiDB LightningおよびBRの Amazon S3 URI の例です。この例では、特定のファイルパス`testfolder`を指定する必要があります。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

以下は、TiCDC `sink-uri`の Amazon S3 URI の例です。

```shell
tiup cdc:v7.5.0 cli changefeed create \
    --server=http://172.16.201.18:8300 \
    --sink-uri="s3://cdc?endpoint=http://10.240.0.38:9000&access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --changefeed-id="cdcTest" \
    --config=cdc_csv.toml
```

以下は、 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の Amazon S3 URI の例です。この例では、特定のファイル名`test.csv`を指定する必要があります。

```shell
s3://external/test.csv?access-key=${access-key}&secret-access-key=${secret-access-key}
```

## GCS URI 形式 {#gcs-uri-format}

-   `scheme` : `gcs`または`gs`
-   `host` : `bucket name`
-   `parameters` :

    -   `credentials-file` : 移行ツール ノード上の資格情報 JSON ファイルへのパスを指定します。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します（たとえば、 `STANDARD`または`COLDLINE` ）
    -   `predefined-acl` : アップロードされたオブジェクトの定義済みACLを指定します（たとえば、 `private`または`project-private` ）

以下は、 TiDB LightningおよびBRの GCS URI の例です。この例では、特定のファイル パス`testfolder`を指定する必要があります。

```shell
gcs://external/testfolder?credentials-file=${credentials-file-path}
```

以下は[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の GCS URI の例です。この例では、特定のファイル名`test.csv`を指定する必要があります。

```shell
gcs://external/test.csv?credentials-file=${credentials-file-path}
```

## Azure Blob Storage URI 形式 {#azure-blob-storage-uri-format}

-   `scheme` : `azure`または`azblob`
-   `host` : `container name`
-   `parameters` :

    -   `account-name` :storageのアカウント名を指定します。
    -   `account-key` : アクセスキーを指定します。
    -   `sas-token` : 共有アクセス署名 (SAS) トークンを指定します。
    -   `access-tier` : アップロードされたオブジェクトのアクセス層を指定します (例: `Hot` 、 `Cool` 、 `Archive` 。既定値は、storageアカウントの既定のアクセス層です。
    -   `encryption-scope` : サーバー側の暗号化に[暗号化範囲](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)を指定します。
    -   `encryption-key` : AES256 暗号化アルゴリズムを使用するサーバー側暗号化の場合は[暗号化キー](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys)指定します。

以下は、 BRの Azure Blob Storage URI の例です。この例では、特定のファイル パス`testfolder`を指定する必要があります。

```shell
azure://external/testfolder?account-name=${account-name}&account-key=${account-key}
```
