---
title: URI Formats of External Storage Services
summary: Learn about the storage URI formats of external storage services, including Amazon S3, GCS, and Azure Blob Storage.
---

## 外部ストレージ サービスの URI 形式 {#uri-formats-of-external-storage-services}

このドキュメントでは、Amazon S3、GCS、Azure Blob Storage などの外部storageサービスの URI 形式について説明します。

URI の基本的な形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

## Amazon S3 URI 形式 {#amazon-s3-uri-format}

-   `scheme` ： `s3`
-   `host` ： `bucket name`
-   `parameters` :

    -   `access-key` : アクセスキーを指定します。
    -   `secret-access-key` : シークレットアクセスキーを指定します。
    -   `session-token` : 一時セッショントークンを指定します。 BR はまだこのパラメータをサポートしていません。
    -   `use-accelerate-endpoint` : Amazon S3 で加速エンドポイントを使用するかどうかを指定します (デフォルトは`false` )。
    -   `endpoint` : S3 互換サービスのカスタム エンドポイントの URL を指定します (例: `<https://s3.example.com/>` )。
    -   `force-path-style` : 仮想ホスト型アクセスではなく、パス型アクセスを使用します (デフォルトは`true` )。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`STANDARD_IA` )。
    -   `sse` : アップロードされたオブジェクトの暗号化に使用されるサーバー側の暗号化アルゴリズムを指定します (値のオプション: ``、 `AES256` 、または`aws:kms` )。
    -   `sse-kms-key-id` : `sse`が`aws:kms`に設定されている場合、KMS ID を指定します。
    -   `acl` : アップロードされたオブジェクトの既定の ACL を指定します (たとえば、 `private`または`authenticated-read` )。
    -   `role-arn` : 指定された[IAMの役割](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)使用してサードパーティの Amazon S3 データにアクセスする必要がある場合、 `role-arn` URL クエリ パラメーター ( `arn:aws:iam::888888888888:role/my-role`など) を使用してIAMロールの対応する[Amazon リソースネーム (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)指定できます。 IAMロールを使用してサードパーティから Amazon S3 データにアクセスする方法の詳細については、 [AWS ドキュメント](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)を参照してください。
    -   `external-id` : サードパーティから Amazon S3 データにアクセスする場合、 [IAMの役割](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)想定するには正しい[外部ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html)を指定する必要がある場合があります。この場合、この`external-id` URL クエリ パラメーターを使用して外部 ID を指定し、 IAMロールを確実に引き受けることができます。外部 ID は、Amazon S3 データにアクセスするためにIAMロール ARN とともにサードパーティによって提供される任意の文字列です。 IAMロールを引き受ける場合、外部 ID の指定はオプションです。つまり、サードパーティがIAMロールに外部 ID を必要としない場合は、このパラメータを指定せずにIAMロールを引き受けて、対応する Amazon S3 データにアクセスできます。

以下は、 TiDB LightningおよびBRの Amazon S3 URI の例です。この例では、特定のファイル パス`testfolder`を指定する必要があります。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

以下は、 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の Amazon S3 URI の例です。この例では、特定のファイル名`test.csv`を指定する必要があります。

```shell
s3://external/test.csv?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

## GCS URI 形式 {#gcs-uri-format}

-   `scheme` ： `gcs`または`gs`
-   `host` ： `bucket name`
-   `parameters` :

    -   `credentials-file` : 移行ツール ノード上の認証情報 JSON ファイルへのパスを指定します。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`COLDLINE` )
    -   `predefined-acl` : アップロードされたオブジェクトの事前定義された ACL を指定します (たとえば、 `private`または`project-private` )

以下は、 TiDB LightningおよびBRの GCS URI の例です。この例では、特定のファイル パス`testfolder`を指定する必要があります。

```shell
gcs://external/testfolder?credentials-file=${credentials-file-path}
```

以下は[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の GCS URI の例です。この例では、特定のファイル名`test.csv`を指定する必要があります。

```shell
gcs://external/test.csv?credentials-file=${credentials-file-path}
```

## Azure Blob Storage URI 形式 {#azure-blob-storage-uri-format}

-   `scheme` ： `azure`または`azblob`
-   `host` ： `container name`
-   `parameters` :

    -   `account-name` :storageのアカウント名を指定します。
    -   `account-key` : アクセスキーを指定します。
    -   `sas-token` : Shared Access Signature (SAS) トークンを指定します。
    -   `access-tier` : アップロードされたオブジェクトのアクセス層を指定します (たとえば、 `Hot` 、 `Cool` 、または`Archive` )。デフォルト値は、storageアカウントのデフォルトのアクセス層です。
    -   `encryption-scope` : サーバー側の暗号化に[暗号化スコープ](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)を指定します。
    -   `encryption-key` : AES256 暗号化アルゴリズムを使用するサーバー側暗号化に[暗号化キー](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys)指定します。

以下は、 TiDB LightningおよびBRの Azure Blob Storage URI の例です。この例では、特定のファイル パス`testfolder`を指定する必要があります。

```shell
azure://external/testfolder?account-name=${account-name}&account-key=${account-key}
```

以下は、 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の Azure Blob Storage URI の例です。この例では、特定のファイル名`test.csv`を指定する必要があります。

```shell
azure://external/test.csv?account-name=${account-name}&account-key=${account-key}
```
