---
title: Backup Storages
summary: Describes the storage URI format used in TiDB backup and restore.
---

# バックアップストレージ {#backup-storages}

TiDB は、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS へのバックアップ データの保存をサポートしています。具体的には、 `br`のコマンドの`--storage`または`-s`パラメータにバックアップstorageのURIを指定できます。このドキュメントでは、さまざまな外部storageサービスの[URI形式](#uri-format)と[認証](#authentication) 、および[サーバー側の暗号化](#server-side-encryption)を紹介します。

## 資格情報を TiKV に送信する {#send-credentials-to-tikv}

| CLIパラメータ                     | 説明                                     | デフォルト値 |
| :--------------------------- | :------------------------------------- | :----- |
| `--send-credentials-to-tikv` | BRによって取得された資格情報を TiKV に送信するかどうかを制御します。 | `true` |

デフォルトでは、Amazon S3、GCS、または Azure Blob Storage をstorageシステムとして使用する場合、 BR は各 TiKV ノードに認証情報を送信します。この動作により構成が簡素化され、パラメータ`--send-credentials-to-tikv` (つまり`-c` ) によって制御されます。

この操作はクラウド環境には適用されないことに注意してください。 IAMロール認証を使用する場合、各ノードは独自のロールと権限を持ちます。この場合、資格情報の送信を無効にするために`--send-credentials-to-tikv=false` (つまり`-c=0` ) を構成する必要があります。

```bash
./br backup full -c=0 -u pd-service:2379 --storage 's3://bucket-name/prefix'
```

[`BACKUP`](/sql-statements/sql-statement-backup.md)および[`RESTORE`](/sql-statements/sql-statement-restore.md)ステートメントを使用してデータをバックアップまたは復元する場合は、 `SEND_CREDENTIALS_TO_TIKV = FALSE`オプションを追加できます。

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

## URI形式 {#uri-format}

### URI形式の説明 {#uri-format-description}

このセクションでは、storageサービスの URI 形式について説明します。

```shell
[scheme]://[host]/[path]?[parameters]
```

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

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

</div>
<div label="GCS" value="gcs">

-   `scheme` ： `gcs`または`gs`
-   `host` ： `bucket name`
-   `parameters` :

    -   `credentials-file` : 移行ツール ノード上の認証情報 JSON ファイルへのパスを指定します。
    -   `storage-class` : アップロードされたオブジェクトのstorageクラスを指定します (たとえば、 `STANDARD`または`COLDLINE` )
    -   `predefined-acl` : アップロードされたオブジェクトの事前定義された ACL を指定します (たとえば、 `private`または`project-private` )

</div>
<div label="Azure Blob Storage" value="azure">

-   `scheme` ： `azure`または`azblob`
-   `host` ： `container name`
-   `parameters` :

    -   `account-name` :storageのアカウント名を指定します。
    -   `account-key` : アクセスキーを指定します。
    -   `access-tier` : アップロードされたオブジェクトのアクセス層を指定します (たとえば、 `Hot` 、 `Cool` 、または`Archive` )。デフォルトの値は`Hot`です。

</div>
</SimpleTab>

### URIの例 {#uri-examples}

このセクションでは、 `host`パラメーター (前のセクションでは`bucket name`または`container name` ) として`external`を使用した URI の例をいくつか示します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

**スナップショット データを Amazon S3 にバックアップする**

```shell
./br backup full -u "${PD_IP}:2379" \
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

バックアップ データをクラウドstorageシステムに保存する場合、特定のクラウド サービス プロバイダーに応じて認証パラメーターを構成する必要があります。このセクションでは、Amazon S3、GCS、および Azure Blob Storage で使用される認証方法と、対応するstorageサービスへのアクセスに使用されるアカウントの構成方法について説明します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

バックアップ前に、S3 上のバックアップ ディレクトリにアクセスするための次の権限を設定します。

-   バックアップ中にバックアップ ディレクトリにアクセスするための TiKV およびバックアップ &amp; リストア ( BR ) の最小権限: `s3:ListBucket` 、 `s3:PutObject` 、および`s3:AbortMultipartUpload`
-   TiKV およびBR が復元中にバックアップ ディレクトリにアクセスするための最小権限: `s3:ListBucket` 、 `s3:GetObject` 、および`s3:PutObject` 。 BR は、チェックポイント情報をバックアップ ディレクトリの下の`./checkpoints`サブディレクトリに書き込みます。ログ バックアップ データを復元するとき、 BR は復元されたクラスターのテーブル ID マッピング関係をバックアップ ディレクトリの下の`./pitr_id_maps`サブディレクトリに書き込みます。

バックアップ ディレクトリをまだ作成していない場合は、 [バケットを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照して、指定したリージョンに S3 バケットを作成します。必要に応じて、 [フォルダーを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してバケット内にフォルダーを作成することもできます。

次のいずれかの方法を使用して S3 へのアクセスを構成することをお勧めします。

-   方法 1: アクセスキーを指定する

    URIにアクセスキーとシークレットアクセスキーを指定すると、指定したアクセスキーとシークレットアクセスキーを使用して認証が行われます。 URI でキーを指定する以外に、次のメソッドもサポートされています。

    -   BR は環境変数`$AWS_ACCESS_KEY_ID`と`$AWS_SECRET_ACCESS_KEY`を読み取ります。
    -   BR は環境変数`$AWS_ACCESS_KEY`および`$AWS_SECRET_KEY`を読み取ります。
    -   BR は、環境変数`$AWS_SHARED_CREDENTIALS_FILE`で指定されたパスにある共有資格情報ファイルを読み取ります。
    -   BR は、 `~/.aws/credentials`パスの共有資格情報ファイルを読み取ります。

-   方法 2: IAMロールに基づいてアクセスする

    S3 にアクセスできるIAMロールを、TiKV ノードとBRノードが実行される EC2 インスタンスに関連付けます。関連付け後、 BR は追加の設定を行わずに S3 のバックアップ ディレクトリに直接アクセスできます。

    ```shell
    br backup full --pd "${PD_IP}:2379" \
    --storage "s3://${host}/${path}"
    ```

</div>
<div label="GCS" value="gcs">

アクセスキーを指定することで、GCS へのアクセスに使用するアカウントを設定できます。 `credentials-file`パラメータを指定した場合、認証は指定された`credentials-file`を使用して実行されます。 URI でキーを指定する以外に、次のメソッドもサポートされています。

-   BR は、環境変数`$GOOGLE_APPLICATION_CREDENTIALS`で指定されたパスにあるファイルを読み取ります。
-   BR はファイル`~/.config/gcloud/application_default_credentials.json`を読み取ります。
-   BR は、クラスターが GCE または GAE で実行されているときにメタデータサーバーから認証情報を取得します。

</div>
<div label="Azure Blob Storage" value="azure">

-   方法 1: アクセスキーを指定する

    URIに`account-name`と`account-key`を指定した場合は、指定したアクセスキーとシークレットアクセスキーを使用して認証が行われます。 BR は、URI でキーを指定する方法以外に、環境変数`$AZURE_STORAGE_KEY`からキーを読み取ることもできます。

-   方法 2: バックアップと復元に Azure AD を使用する

    BR が実行されているノードで環境変数`$AZURE_CLIENT_ID` 、 `$AZURE_TENANT_ID` 、および`$AZURE_CLIENT_SECRET`を構成します。

    -   TiUPを使用してクラスターが起動されると、TiKV は systemd サービスを使用します。次の例は、TiKV 用に前述の 3 つの環境変数を構成する方法を示しています。

        > **注記：**
        >
        > この方法を使用する場合は、手順 3 で TiKV を再起動する必要があります。クラスターを再起動できない場合は、**方法 1: バックアップと復元のアクセス キーを指定するを**使用します。

        1.  このノードの TiKV ポートが`24000` 、つまり systemd サービスの名前が`tikv-24000`であるとします。

            ```shell
            systemctl edit tikv-24000
            ```

        2.  TiKV 構成ファイルを編集して、3 つの環境変数を構成します。

                [Service]
                Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        3.  構成をリロードし、TiKV を再起動します。

            ```shell
            systemctl daemon-reload
            systemctl restart tikv-24000
            ```

    -   コマンド ラインを使用して TiKV およびBRの Azure AD 情報を構成するには、次のコマンドを実行して、環境変数`$AZURE_CLIENT_ID` 、 `$AZURE_TENANT_ID` 、および`$AZURE_CLIENT_SECRET`がオペレーティング環境で構成されているかどうかを確認するだけです。

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

BR は、 Amazon S3 にデータをバックアップする際のサーバー側の暗号化をサポートします。 BRを使用して S3 サーバー側暗号化用に作成した AWS KMS キーを使用することもできます。詳細は[BR S3 サーバー側暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)を参照してください。

## storageサービスでサポートされるその他の機能 {#other-features-supported-by-the-storage-service}

BR v6.3.0 は AWS [S3 オブジェクトロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)をサポートします。この機能を有効にすると、バックアップ データの改ざんや削除を防ぐことができます。
