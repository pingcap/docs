---
title: Backup Storages
summary: Describes the storage URL format used in TiDB backup and restore.
aliases: ['/tidb/stable/backup-storage-S3/','/tidb/stable/backup-storage-azblob/','/tidb/stable/backup-storage-gcs/','/tidb/stable/external-storage/']
---

# バックアップ ストレージ {#backup-storages}

TiDB は、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS へのバックアップ データの保存をサポートしています。具体的には、 `br`のコマンドの`--storage`または`-s`パラメーターでバックアップstorageの URL を指定できます。このドキュメントでは、さまざまな外部storageサービスの[URL 形式](#url-format)と[認証](#authentication) 、および[サーバー側の暗号化](#server-side-encryption)を紹介します。

## 認証情報を TiKV に送信する {#send-credentials-to-tikv}

| CLI パラメータ                    | 説明                                     | デフォルト値 |
| :--------------------------- | :------------------------------------- | :----- |
| `--send-credentials-to-tikv` | BRによって取得された資格情報を TiKV に送信するかどうかを制御します。 | `true` |

デフォルトでは、storageシステムとして Amazon S3、GCS、または Azure Blob Storage を使用する場合、 BR は各 TiKV ノードに認証情報を送信します。この動作は構成を簡素化し、パラメーター`--send-credentials-to-tikv` (または略して`-c` ) によって制御されます。

この操作は、クラウド環境には適用されないことに注意してください。 IAMロール認証を使用する場合、各ノードには独自のロールと権限があります。この場合、資格情報の送信を無効にするには、 `--send-credentials-to-tikv=false` (または略して`-c=0` ) を構成する必要があります。

```bash
./br backup full -c=0 -u pd-service:2379 --storage 's3://bucket-name/prefix'
```

[`BACKUP`](/sql-statements/sql-statement-backup.md)ステートメントと[`RESTORE`](/sql-statements/sql-statement-restore.md)ステートメントを使用してデータをバックアップまたは復元する場合は、 `SEND_CREDENTIALS_TO_TIKV = FALSE`オプションを追加できます。

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

## URL 形式 {#url-format}

### URL 形式の説明 {#url-format-description}

このセクションでは、storageサービスの URL 形式について説明します。

```shell
[scheme]://[host]/[path]?[parameters]
```

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

-   `scheme` : `s3`
-   `host` : `bucket name`
-   `parameters` :

    -   `access-key` : アクセスキーを指定します。
    -   `secret-access-key` : シークレット アクセス キーを指定します。
    -   `use-accelerate-endpoint` : Amazon S3 で加速エンドポイントを使用するかどうかを指定します (デフォルトは`false` )。
    -   `endpoint` : S3 互換サービスのカスタム エンドポイントの URL を指定します (たとえば、 `<https://s3.example.com/>` )。
    -   `force-path-style` : 仮想ホスト スタイル アクセスではなく、パス スタイル アクセスを使用します (デフォルトは`true` )。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`STANDARD_IA` )。
    -   `sse` : アップロードされたオブジェクトの暗号化に使用されるサーバー側の暗号化アルゴリズムを指定します (値のオプション: ``、 `AES256` 、または`aws:kms` )。
    -   `sse-kms-key-id` : `sse`が`aws:kms`に設定されている場合、KMS ID を指定します。
    -   `acl` : アップロードされたオブジェクトの既定の ACL を指定します (たとえば、 `private`または`authenticated-read` )。

</div>
<div label="GCS" value="gcs">

-   `scheme` : `gcs`または`gs`
-   `host` : `bucket name`
-   `parameters` :

    -   `credentials-file` : 移行ツール ノードの資格情報 JSON ファイルへのパスを指定します。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`COLDLINE` )
    -   `predefined-acl` : アップロードされたオブジェクトの事前定義された ACL を指定します (たとえば、 `private`または`project-private` )

</div>
<div label="Azure Blob Storage" value="azure">

-   `scheme` : `azure`または`azblob`
-   `host` : `container name`
-   `parameters` :

    -   `account-name` :storageのアカウント名を指定します。
    -   `account-key` : アクセスキーを指定します。
    -   `access-tier` : アップロードされたオブジェクトのアクセス層を指定します (例: `Hot` 、 `Cool` 、または`Archive` )。デフォルトの値は`Hot`です。

</div>
</SimpleTab>

### URL の例 {#url-examples}

このセクションでは、 `external` `host`パラメーター (前のセクションでは`bucket name`または`container name` ) として使用して、いくつかの URL の例を示します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

**スナップショット データを Amazon S3 にバックアップする**

```shell
./br restore full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

**Amazon S3 からスナップショット データを復元する**

```shell
./br restore full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

</div>
<div label="GCS" value="gcs">

**スナップショット データを GCS にバックアップする**

```shell
./br backup full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

**GCS からスナップショット データを復元する**

```shell
./br restore full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

</div>
<div label="Azure Blob Storage" value="azure">

**スナップショット データを Azure Blob Storage にバックアップする**

```shell
./br backup full -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915?account-name=${account-name}&account-key=${account-key}"
```

**Azure Blob Storage のスナップショット バックアップ データから`test`データベースを復元する**

```shell
./br restore db --db test -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915account-name=${account-name}&account-key=${account-key}"
```

</div>
</SimpleTab>

## 認証 {#authentication}

バックアップ データをクラウドstorageシステムに保存する場合、特定のクラウド サービス プロバイダーに応じて認証パラメーターを構成する必要があります。このセクションでは、Amazon S3、GCS、および Azure Blob Storage で使用される認証方法と、対応するstorageサービスへのアクセスに使用されるアカウントを構成する方法について説明します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

バックアップの前に、S3 のバックアップ ディレクトリにアクセスするために次の権限を設定します。

-   バックアップ中にバックアップ ディレクトリにアクセスするための TiKV および Backup &amp; Restore ( BR ) の最小権限: `s3:ListBucket` 、 `s3:PutObject` 、および`s3:AbortMultipartUpload`
-   復元中に TiKV およびBR がバックアップ ディレクトリにアクセスするための最小権限: `s3:ListBucket`および`s3:GetObject`

バックアップ ディレクトリをまだ作成していない場合は、 [バケットを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照して、指定したリージョンに S3 バケットを作成します。必要に応じて、 [フォルダを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してバケットにフォルダーを作成することもできます。

次のいずれかの方法を使用して、S3 へのアクセスを構成することをお勧めします。

-   方法 1: アクセス キーを指定する

    URLにアクセスキーとシークレットアクセスキーを指定すると、指定したアクセスキーとシークレットアクセスキーで認証が行われます。 URL でキーを指定する以外に、次の方法もサポートされています。

    -   BR は、環境変数`$AWS_ACCESS_KEY_ID`および`$AWS_SECRET_ACCESS_KEY`を読み取ります。
    -   BR は、環境変数`$AWS_ACCESS_KEY`および`$AWS_SECRET_KEY`を読み取ります。
    -   BR は、環境変数`$AWS_SHARED_CREDENTIALS_FILE`で指定されたパスにある共有資格情報ファイルを読み取ります。
    -   BR は`~/.aws/credentials`パスの共有認証情報ファイルを読み取ります。

-   方法 2: IAMロールに基づくアクセス

    S3 にアクセスできるIAMロールを、TiKV およびBRノードが実行される EC2 インスタンスに関連付けます。関連付け後、 BR は追加設定なしで S3 のバックアップ ディレクトリに直接アクセスできます。

    ```shell
    br backup full --pd "${PD_IP}:2379" \
    --storage "s3://${host}/${path}"
    ```

</div>
<div label="GCS" value="gcs">

アクセス キーを指定することで、GCS へのアクセスに使用するアカウントを構成できます。 `credentials-file`パラメータを指定すると、指定された`credentials-file`を使用して認証が実行されます。 URL でキーを指定する以外に、次の方法もサポートされています。

-   BR は、環境変数`$GOOGLE_APPLICATION_CREDENTIALS`で指定されたパスにあるファイルを読み取ります
-   BR はファイルを読み取ります`~/.config/gcloud/application_default_credentials.json` 。
-   クラスターが GCE または GAE で実行されている場合、 BR はメタデータサーバーから資格情報を取得します。

</div>
<div label="Azure Blob Storage" value="azure">

-   方法 1: アクセス キーを指定する

    URL に`account-name`と`account-key`を指定すると、指定したアクセス キーとシークレット アクセス キーを使用して認証が行われます。 URL でキーを指定する方法の他に、 BR は環境変数`$AZURE_STORAGE_KEY`からキーを読み取ることもできます。

-   方法 2: バックアップと復元に Azure AD を使用する

    BRが実行されているノードで、環境変数`$AZURE_CLIENT_ID` 、 `$AZURE_TENANT_ID` 、および`$AZURE_CLIENT_SECRET`を構成します。

    -   TiUPを使用してクラスターを起動すると、TiKV は systemd サービスを使用します。次の例は、TiKV 用に前述の 3 つの環境変数を構成する方法を示しています。

        > **ノート：**
        >
        > この方法を使用する場合は、手順 3 で TiKV を再起動する必要があります。クラスターを再起動できない場合は、**方法 1: バックアップと復元用のアクセス キーを指定します**。

        1.  このノードの TiKV ポートが`24000` 、つまり systemd サービスの名前が`tikv-24000`であるとします。

            ```shell
            systemctl edit tikv-24000
            ```

        2.  TiKV 構成ファイルを編集して、3 つの環境変数を構成します。

            ```
            [Service]
            Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ```

        3.  構成をリロードし、TiKV を再起動します。

            ```shell
            systemctl daemon-reload
            systemctl restart tikv-24000
            ```

    -   コマンド ラインで開始された TiKV およびBRの Azure AD 情報を構成するには、次のコマンドを実行して、環境変数`$AZURE_CLIENT_ID` 、 `$AZURE_TENANT_ID` 、および`$AZURE_CLIENT_SECRET`が動作環境で構成されているかどうかを確認するだけで済みます。

        ```shell
        echo $AZURE_CLIENT_ID
        echo $AZURE_TENANT_ID
        echo $AZURE_CLIENT_SECRET
        ```

    -   BRを使用してデータを Azure Blob Storage にバックアップします。

        ```shell
        ./br backup full -u "${PD_IP}:2379" \
        --storage "azure://external/backup-20220915?account-name=${account-name}"
        ```

</div>
</SimpleTab>

## サーバー側の暗号化 {#server-side-encryption}

### Amazon S3 サーバー側の暗号化 {#amazon-s3-server-side-encryption}

BR は、データを Amazon S3 にバックアップする際のサーバー側の暗号化をサポートしています。 BRを使用して、S3 サーバー側の暗号化用に作成した AWS KMS キーを使用することもできます。詳細については、 [BR S3 サーバー側の暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)を参照してください。

## storageサービスがサポートするその他の機能 {#other-features-supported-by-the-storage-service}

BR v6.3.0 は AWS [S3 オブジェクト ロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)をサポートします。この機能を有効にすると、バックアップ データの改ざんや削除を防ぐことができます。
