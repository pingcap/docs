---
title: Backup Storages
summary: TiDBは、Amazon S3、Google Cloud Storage、Azure Blob Storage、NFSへのバックアップstorageをサポートしています。各storageサービスのURIと認証を指定できます。S3、GCS、またはAzure Blob Storageを使用する場合、 BRはBRでTiKVに認証情報を送信します。クラウド環境では、この機能を無効にすることができます。各storageサービスのURI形式と認証方法を指定します。Amazon S3とAzure Blob Storageでは、サーバー側暗号化がサポートされています。BR v6.3.0はAWS S3オブジェクトロックもサポートしています。
---

# バックアップストレージ {#backup-storages}

TiDBは、Amazon S3、Google Cloud Storage（GCS）、Azure Blob Storage、NFSへのバックアップデータの保存をサポートしています。具体的には、 `br`コマンドの`--storage`または`-s`パラメータでバックアップstorageのURIを指定できます。このドキュメントでは、 [URI形式](#uri-format)と[認証](#authentication)の外部ストレージサービスと、 [サーバー側の暗号化](#server-side-encryption)外部storageサービスを紹介します。

## TiKVに資格情報を送信する {#send-credentials-to-tikv}

| CLIパラメータ                     | 説明                                     | デフォルト値 |
| :--------------------------- | :------------------------------------- | :----- |
| `--send-credentials-to-tikv` | BRによって取得された資格情報を TiKV に送信するかどうかを制御します。 | `true` |

デフォルトでは、storageシステムとしてAmazon S3、GCS、またはAzure Blob Storageを使用する場合、 BRは各TiKVノードに認証情報を送信します。この動作は設定を簡素化し、パラメータ`--send-credentials-to-tikv` （または短縮形`-c` ）によって制御されます。

この操作はクラウド環境には適用されないことに注意してください。IAMロール認証を使用する場合、各ノードには独自のロールと権限が付与されます。この場合、認証情報の送信を無効にするには、 `--send-credentials-to-tikv=false` （または`-c=0` ）を設定する必要があります。

```bash
tiup br backup full -c=0 -u pd-service:2379 --storage 's3://bucket-name/prefix'
```

[`BACKUP`](/sql-statements/sql-statement-backup.md)および[`RESTORE`](/sql-statements/sql-statement-restore.md)ステートメントを使用してデータをバックアップまたは復元する場合は、 `SEND_CREDENTIALS_TO_TIKV = FALSE`オプションを追加できます。

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

## URI形式 {#uri-format}

### URI形式の説明 {#uri-format-description}

外部storageサービスの URI 形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

URI 形式の詳細については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

### URIの例 {#uri-examples}

このセクションでは、 `host`パラメータとして`external` (前のセクションでは`bucket name`または`container name` ) を使用した URI の例をいくつか示します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

**スナップショットデータをAmazon S3にバックアップする**

```shell
tiup br backup full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

**Amazon S3からスナップショットデータを復元する**

```shell
tiup br restore full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

</div>
<div label="GCS" value="gcs">

**スナップショットデータをGCSにバックアップする**

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

**GCSからスナップショットデータを復元する**

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

</div>
<div label="Azure Blob Storage" value="azure">

**スナップショットデータをAzure Blob Storageにバックアップする**

```shell
tiup br backup full -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915?account-name=${account-name}&account-key=${account-key}"
```

**Azure Blob Storage のスナップショット バックアップ データから`test`データベースを復元する**

```shell
tiup br restore db --db test -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915account-name=${account-name}&account-key=${account-key}"
```

</div>
</SimpleTab>

## 認証 {#authentication}

クラウドstorageシステムにバックアップデータを保存する場合、クラウドサービスプロバイダーに応じて認証パラメータを設定する必要があります。このセクションでは、Amazon S3、GCS、Azure Blob Storageで使用される認証方法と、それぞれのストレージstorageにアクセスするために使用するアカウントの設定方法について説明します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

バックアップの前に、S3 上のバックアップ ディレクトリにアクセスするための次の権限を設定します。

-   バックアップ中にバックアップディレクトリにアクセスするための TiKV および Backup &amp; Restore ( BR ) の最小権限: `s3:ListBucket` 、 `s3:GetObject` 、 `s3:DeleteObject` 、 `s3:PutObject` 、および`s3:AbortMultipartUpload`
-   リストア中にTiKVとBRがバックアップディレクトリにアクセスするための最小権限： `s3:ListBucket` 、 `s3:GetObject` 、 `s3:DeleteObject` 、および`s3:PutObject` 。BRはチェックポイント情報をバックアップディレクトリのサブディレクトリ`./checkpoints`に書き込みます。ログバックアップデータをリストアする際、 BRはリストアされたクラスターのテーブルIDマッピング関係をバックアップディレクトリのサブディレクトリ`./pitr_id_maps`に書き込みます。

バックアップディレクトリをまだ作成していない場合は、 [バケットを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照して指定のリージョンに S3 バケットを作成してください。必要に応じて、 [フォルダを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してバケット内にフォルダを作成することもできます。

次のいずれかの方法で S3 へのアクセスを構成することをお勧めします。

-   方法1: アクセスキーを指定する

    URIにアクセスキーとシークレットアクセスキーを指定した場合、指定されたアクセスキーとシークレットアクセスキーを使用して認証が行われます。URIでキーを指定する以外にも、以下の方法がサポートされています。

    -   BRは環境変数`$AWS_ACCESS_KEY_ID`と`$AWS_SECRET_ACCESS_KEY`読み取ります。
    -   BRは環境変数`$AWS_ACCESS_KEY`と`$AWS_SECRET_KEY`読み取ります。
    -   BR は、環境変数`$AWS_SHARED_CREDENTIALS_FILE`で指定されたパスにある共有資格情報ファイルを読み取ります。
    -   BR は`~/.aws/credentials`パスにある共有資格情報ファイルを読み取ります。

-   方法2: IAMロールに基づくアクセス

    S3にアクセスできるIAMロールを、TiKVノードとBRノードが稼働するEC2インスタンスに関連付けます。関連付け後、 BRは追加設定なしでS3内のバックアップディレクトリに直接アクセスできるようになります。

    ```shell
    tiup br backup full --pd "${PD_IP}:2379" \
    --storage "s3://${host}/${path}"
    ```

</div>
<div label="GCS" value="gcs">

GCSへのアクセスに使用するアカウントは、アクセスキーを指定することで設定できます。1 `credentials-file`を指定した場合、指定された`credentials-file`使用して認証が行われます。URIでキーを指定する以外にも、以下の方法がサポートされています。

-   BRは環境変数`$GOOGLE_APPLICATION_CREDENTIALS`で指定されたパスのファイルを読み取ります。
-   BR はファイル`~/.config/gcloud/application_default_credentials.json`を読み取ります。
-   BR は、クラスターが GCE または GAE で実行されているときに、メタデータサーバーから資格情報を取得します。

</div>
<div label="Azure Blob Storage" value="azure">

-   方法1: 共有アクセス署名を指定する

    URIに`account-name`と`sas-token`指定した場合、指定されたアカウント名と共有アクセス署名（SAS）トークンを使用して認証が行われます。SASトークンには`&`文字が含まれていることに注意してください。これをURIに追加する前に、 `%26`としてエンコードする必要があります。パーセントエンコードを使用して、 `sas-token`全体を直接エンコードすることもできます。

-   方法2: アクセスキーを指定する

    URIに`account-name`と`account-key`指定すると、指定されたアカウント名とアカウントキーを用いて認証が行われます。URIでキーを指定する方法に加え、 BRは環境変数`$AZURE_STORAGE_KEY`からキーを読み取ることもできます。

-   方法3: バックアップと復元にAzure ADを使用する

    BRが実行されているノードで環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_CLIENT_SECRET` `$AZURE_TENANT_ID`します。

    -   TiUPを使用してクラスターを起動すると、TiKV は systemd サービスを使用します。次の例は、TiKV の上記の 3 つの環境変数を設定する方法を示しています。

        > **注記：**
        >
        > この方法を使用する場合は、手順 3 で TiKV を再起動する必要があります。クラスターを再起動できない場合は、 **「方法 1: バックアップと復元のアクセス キーを指定する」**を使用します。

        1.  このノードの TiKV ポートが`24000` 、つまり systemd サービスの名前が`tikv-24000`であるとします。

            ```shell
            systemctl edit tikv-24000
            ```

        2.  TiKV 構成ファイルを編集して、次の 3 つの環境変数を構成します。

                [Service]
                Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        3.  設定を再ロードし、TiKV を再起動します。

            ```shell
            systemctl daemon-reload
            systemctl restart tikv-24000
            ```

    -   コマンドラインで起動した TiKV およびBRの Azure AD 情報を構成するには、次のコマンドを実行して、オペレーティング環境で環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_CLIENT_SECRET` `$AZURE_TENANT_ID`されているかどうかを確認するだけです。

        ```shell
        echo $AZURE_CLIENT_ID
        echo $AZURE_TENANT_ID
        echo $AZURE_CLIENT_SECRET
        ```

    -   BRを使用してデータを Azure Blob Storage にバックアップします。

        ```shell
        tiup br backup full -u "${PD_IP}:2379" \
        --storage "azure://external/backup-20220915?account-name=${account-name}"
        ```

</div>
</SimpleTab>

## サーバー側の暗号化 {#server-side-encryption}

### Amazon S3 サーバー側暗号化 {#amazon-s3-server-side-encryption}

BR は、Amazon S3 へのデータのバックアップ時にサーバー側暗号化をサポートします。また、 BRを使用して S3 のサーバー側暗号化用に作成した AWS KMS キーを使用することもできます。詳細については、 [BR S3 サーバー側暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)参照してください。

### Azure Blob Storage のサーバー側暗号化 {#azure-blob-storage-server-side-encryption}

BRは、Azure Blob Storageへのデータのバックアップ時に、Azureサーバー側暗号化のスコープを指定したり、暗号化キーを提供したりすることをサポートしています。この機能により、同じstorageアカウントの異なるバックアップデータに対してセキュリティ境界を設定できます。詳細については、 [BR Azure Blob Storage サーバー側暗号化](/encryption-at-rest.md#br-azure-blob-storage-server-side-encryption)ご覧ください。

## storageサービスでサポートされているその他の機能 {#other-features-supported-by-the-storage-service}

Amazon [S3 オブジェクトロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) 、指定された保持期間中のバックアップデータの偶発的または意図的な削除を防ぎ、データのセキュリティと整合性を強化します。バージョン6.3.0以降、 BRはスナップショットバックアップでAmazon S3オブジェクトロックをサポートし、フルバックアップのセキュリティをさらに強化します。バージョン8.0.0以降、PITRもAmazon S3オブジェクトロックをサポートします。フルバックアップでもログデータバックアップでも、オブジェクトロック機能はより信頼性の高いデータ保護を実現し、データのバックアップとリカバリのセキュリティをさらに強化し、規制要件を満たします。

BRとPITRは、Amazon S3オブジェクトロック機能の有効/無効を自動的に検出します。追加の操作は必要ありません。

> **警告：**
>
> スナップショットバックアップまたはPITRログバックアッププロセス中にオブジェクトロック機能が有効になっている場合、スナップショットバックアップまたはログバックアップが失敗する可能性があります。バックアップを続行するには、スナップショットバックアップまたはPITRログバックアップタスクを再起動する必要があります。
