---
title: URI Formats of External Storage Services
summary: Amazon S3、GCS、Azure Blob Storage などの外部storageサービスのstorageURI 形式について説明します。
---

## 外部ストレージサービスのURI形式 {#uri-formats-of-external-storage-services}

このドキュメントでは、Amazon S3、GCS、Azure Blob Storage などの外部storageサービスの URI 形式について説明します。

URI の基本的な形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

## Amazon S3 URI 形式 {#amazon-s3-uri-format}

<CustomContent platform="tidb">

-   `scheme` : `s3`
-   `host` : `bucket name`
-   `parameters` :

    -   `access-key` : アクセス キーを指定します。
    -   `secret-access-key` : 秘密アクセスキーを指定します。
    -   `session-token` : 一時セッショントークンを指定します。BRはv7.6.0以降でこのパラメータをサポートしています。
    -   `use-accelerate-endpoint` : Amazon S3 の高速エンドポイントを使用するかどうかを指定します (デフォルトは`false` )。
    -   `endpoint` : S3 互換サービスのカスタムエンドポイントの URL を指定します (例: `<https://s3.example.com/>` )。
    -   `force-path-style` : 仮想ホスト スタイルのアクセスではなく、パス スタイルのアクセスを使用します (デフォルトは`true` )。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`STANDARD_IA` )。
    -   `sse` : アップロードされたオブジェクトの暗号化に使用されるサーバー側暗号化アルゴリズムを指定します (値のオプション: 空、 `AES256` 、または`aws:kms` )。
    -   `sse-kms-key-id` : `sse` `aws:kms`に設定されている場合は KMS ID を指定します。
    -   `acl` : アップロードされたオブジェクトの既定 ACL を指定します (たとえば、 `private`または`authenticated-read` )。
    -   `role-arn` : 指定された[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)使用してサードパーティの Amazon S3 データにアクセスする必要がある場合、 `arn:aws:iam::888888888888:role/my-role`などの`role-arn` URL クエリパラメータで、対応する[Amazon リソースネーム (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) IAMロールを指定できます。IAMIAMを使用してサードパーティの Amazon S3 データにアクセスする方法の詳細については、 [AWSドキュメント](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)参照してください。BRはv7.6.0 以降でこのパラメータをサポートしています。
    -   `external-id` : サードパーティから Amazon S3 データにアクセスする場合、正しい[外部ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html)指定して[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)引き受けることが必要になる場合があります。この場合、この`external-id` URL クエリパラメータを使用して外部 ID を指定し、 IAMロールを引き受けることができることを確認できます。外部 ID は、Amazon S3 データにアクセスするためにIAMロール ARN と一緒にサードパーティによって提供される任意の文字列です。IAM ロールを引き受ける場合の外部 IDのIAMIAMに外部 ID を必要としない場合は、このパラメータを指定せずにIAMロールを引き受け、対応する Amazon S3 データにアクセスできます。

以下は、 TiDB LightningおよびBRの Amazon S3 URI の例です。この例では、特定のファイルパス`testfolder`指定する必要があります。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

以下は、 TiCDC `sink-uri`の Amazon S3 URI の例です。

```shell
tiup cdc:v7.5.0 cli changefeed create \
    --server=http://172.16.201.18:8300 \
    --sink-uri="s3://cdc?endpoint=http://10.240.0.38:9000&access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --changefeed-id="cdcTest" \
    --config=cdc_csv.toml
```

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `scheme` : `s3`
-   `host` : `bucket name`
-   `parameters` :

    -   `access-key` : アクセス キーを指定します。

    -   `secret-access-key` : 秘密アクセスキーを指定します。

    -   `session-token` : 一時セッション トークンを指定します。

    -   `use-accelerate-endpoint` : Amazon S3 の高速エンドポイントを使用するかどうかを指定します (デフォルトは`false` )。

    -   `endpoint` : S3 互換サービスのカスタムエンドポイントの URL を指定します (例: `<https://s3.example.com/>` )。

    -   `force-path-style` : 仮想ホスト スタイルのアクセスではなく、パス スタイルのアクセスを使用します (デフォルトは`true` )。

    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`STANDARD_IA` )。

    -   `sse` : アップロードされたオブジェクトの暗号化に使用されるサーバー側暗号化アルゴリズムを指定します (値のオプション: 空、 `AES256` 、または`aws:kms` )。

    -   `sse-kms-key-id` : `sse` `aws:kms`に設定されている場合は KMS ID を指定します。

    -   `acl` : アップロードされたオブジェクトの既定 ACL を指定します (たとえば、 `private`または`authenticated-read` )。

    -   `role-arn` : TiDB Cloud が特定の[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)使用して Amazon S3 データにアクセスできるようにするには、 `role-arn` URL クエリパラメータにロールの[Amazon リソースネーム (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)指定します。例: `arn:aws:iam::888888888888:role/my-role` 。

        > **注記：**
        >
        > -   IAMロールを自動的に作成するには、 [TiDB Cloudコンソール](https://tidbcloud.com/)でクラスターの**[Amazon S3 からのデータのインポート]**ページに移動し、 **[フォルダー URI]**フィールドに入力し、 **[ロール ARN]**フィールドの [**ここをクリックして AWS CloudFormation で新しく作成] を**クリックして、 **[新しいロール ARN の追加]**ダイアログの画面上の指示に従います。
        > -   AWS CloudFormation を使用してIAMロールを作成する際に問題が発生した場合は、 **「新しいロール ARN を追加」**ダイアログで**「問題が発生した場合は、ロール ARN を手動で作成する」を**クリックしてTiDB Cloudアカウント ID とTiDB Cloud外部 ID を取得し、 [ロール ARN を使用して Amazon S3 アクセスを構成する](https://docs.pingcap.com/tidbcloud/dedicated-external-storage#configure-amazon-s3-access-using-a-role-arn)の手順に従って手動でロールを作成してください。IAMIAMを設定する際は、 **「アカウント ID」**フィールドにTiDB Cloudアカウント ID を入力し、 [混乱した副官の攻撃](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)から保護するために**外部 ID を要求する」**を選択してください。
        > -   セキュリティを強化するために、**最大セッション継続時間を**短く設定することで、 IAMロールの有効期間を短縮できます。詳細については、AWSドキュメントの[ロールの最大セッション期間を更新する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_update-role-settings.html#id_roles_update-session-duration)参照してください。

    -   `external-id` : TiDB Cloud がAmazon S3 データにアクセスするために必要なTiDB Cloud外部 ID を指定します。この ID は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の**「新しいロール ARN を追加」**ダイアログから取得できます。詳細については、 [ロール ARN を使用して Amazon S3 アクセスを構成する](https://docs.pingcap.com/tidbcloud/dedicated-external-storage#configure-amazon-s3-access-using-a-role-arn)参照してください。

以下は、 [`BACKUP`](/sql-statements/sql-statement-backup.md)と[`RESTORE`](/sql-statements/sql-statement-restore.md)のAmazon S3 URIの例です。この例では、ファイルパス`testfolder`を使用しています。

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

</CustomContent>

## GCS URI形式 {#gcs-uri-format}

-   `scheme` ： `gcs`または`gs`
-   `host` : `bucket name`
-   `parameters` :

    -   `credentials-file` : 移行ツール ノード上の資格情報 JSON ファイルへのパスを指定します。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します（例： `STANDARD`または`COLDLINE` ）
    -   `predefined-acl` : アップロードされたオブジェクトの定義済みACLを指定します（たとえば、 `private`または`project-private` ）

<CustomContent platform="tidb">

以下は、 TiDB LightningとBRのGCS URIの例です。この例では、特定のファイルパス`testfolder`指定する必要があります。

```shell
gcs://external/testfolder?credentials-file=${credentials-file-path}
```

</CustomContent>

以下は[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の GCS URI の例です。この例では、特定のファイル名`test.csv`指定する必要があります。

```shell
gcs://external/test.csv?credentials-file=${credentials-file-path}
```

## Azure Blob Storage URI 形式 {#azure-blob-storage-uri-format}

-   `scheme` ： `azure`または`azblob`
-   `host` : `container name`
-   `parameters` :

    -   `account-name` :storageのアカウント名を指定します。
    -   `account-key` : アクセス キーを指定します。
    -   `sas-token` : 共有アクセス署名 (SAS) トークンを指定します。
    -   `access-tier` : アップロードされたオブジェクトのアクセス層を指定します（例： `Hot` 、 `Cool` 、 `Archive` ）。既定値は、storageアカウントのデフォルトのアクセス層です。
    -   `encryption-scope` : サーバー側の暗号化に[暗号化範囲](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)指定します。
    -   `encryption-key` : AES256 暗号化アルゴリズムを使用するサーバー側暗号化の場合は[暗号化キー](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys)指定します。

以下は、 BRのAzure Blob Storage URIの例です。この例では、特定のファイルパス`testfolder`指定する必要があります。

```shell
azure://external/testfolder?account-name=${account-name}&account-key=${account-key}
```
