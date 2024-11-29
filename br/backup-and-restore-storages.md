---
title: Backup Storages
summary: TiDB は、Amazon S3、Google Cloud Storage、Azure Blob Storage、NFS へのバックアップstorageをサポートしています。さまざまなstorageサービスの URI と認証を指定できます。S3、GCS、または Azure Blob Storage を使用する場合、 BR はデフォルトで TiKV に資格情報を送信します。クラウド環境ではこれを無効にすることができます。各storageサービスの URI 形式と認証方法が指定されます。Amazon S3 と Azure Blob Storage では、サーバー側の暗号化がサポートされています。BR v6.3.0 はBR S3 オブジェクト ロックもサポートしています。
---

# バックアップストレージ {#backup-storages}

TiDB は、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS へのバックアップ データの保存をサポートしています。具体的には、 `br`コマンドの`--storage`または`-s`パラメータでバックアップstorageの URI を指定できます。このドキュメントでは、さまざまな外部storageサービスの[URI 形式](#uri-format)と[認証](#authentication) 、および[サーバー側暗号化](#server-side-encryption)紹介します。

## TiKVに資格情報を送信する {#send-credentials-to-tikv}

| CLIパラメータ                     | 説明                                     | デフォルト値 |
| :--------------------------- | :------------------------------------- | :----- |
| `--send-credentials-to-tikv` | BRによって取得された資格情報を TiKV に送信するかどうかを制御します。 | `true` |

デフォルトでは、storageシステムとして Amazon S3、GCS、または Azure Blob Storage を使用する場合、 BR は各 TiKV ノードに認証情報を送信します。この動作は構成を簡素化し、パラメータ`--send-credentials-to-tikv` (または短縮して`-c` ) によって制御されます。

この操作はクラウド環境には適用できないことに注意してください。IAM ロール認証を使用する場合、各ノードには独自のロールと権限があります。この場合、認証情報の送信を無効にするには、 `--send-credentials-to-tikv=false` (または`-c=0` ) を設定する必要があります。

```bash
tiup br backup full -c=0 -u pd-service:2379 --storage 's3://bucket-name/prefix'
```

[`BACKUP`](/sql-statements/sql-statement-backup.md)および[`RESTORE`](/sql-statements/sql-statement-restore.md)ステートメントを使用してデータをバックアップまたは復元する場合は、 `SEND_CREDENTIALS_TO_TIKV = FALSE`オプションを追加できます。

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

## URI 形式 {#uri-format}

### URI 形式の説明 {#uri-format-description}

外部storageサービスの URI 形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

URI 形式の詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

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

**スナップショット データを Azure Blob Storage にバックアップする**

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

クラウドstorageシステムにバックアップ データを保存する場合、特定のクラウド サービス プロバイダーに応じて認証パラメータを構成する必要があります。このセクションでは、Amazon S3、GCS、Azure Blob Storage で使用される認証方法と、対応するstorageサービスにアクセスするために使用するアカウントを構成する方法について説明します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

バックアップの前に、S3 上のバックアップ ディレクトリにアクセスするための次の権限を設定します。

-   バックアップ`s3:PutObject`に TiKV およびバックアップ &amp; リストア ( BR ) `s3:GetObject`バックアップ ディレクトリ`s3:AbortMultipartUpload`アクセスするための最小権限: `s3:ListBucket` 、および`s3:DeleteObject`
-   復元中に TiKV とBR がバックアップ ディレクトリにアクセスするための最小権限: `s3:ListBucket` `s3:DeleteObject`および`s3:PutObject`は、チェックポイント情報をバックアップ ディレクトリの下の`./checkpoints`サブディレクトリに書き込みます。ログ バックアップ データ`s3:GetObject`復元する場合、 BR は、復元されたクラスターのテーブル ID マッピング関係をバックアップ ディレクトリの下の`./pitr_id_maps`サブディレクトリに書き込みます。

バックアップディレクトリをまだ作成していない場合は、 [バケットを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)参考にして指定のリージョンに S3 バケットを作成してください。必要に応じて[フォルダを作成する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)参考にバケット内にフォルダを作成することもできます。

次のいずれかの方法で S3 へのアクセスを構成することをお勧めします。

-   方法1: アクセスキーを指定する

    URI にアクセスキーとシークレットアクセスキーを指定すると、指定したアクセスキーとシークレットアクセスキーを使用して認証が行われます。URI でキーを指定する以外に、次の方法もサポートされています。

    -   BR は環境変数`$AWS_ACCESS_KEY_ID`と`$AWS_SECRET_ACCESS_KEY`読み取ります。
    -   BR は環境変数`$AWS_ACCESS_KEY`と`$AWS_SECRET_KEY`読み取ります。
    -   BR は、環境変数`$AWS_SHARED_CREDENTIALS_FILE`で指定されたパスにある共有資格情報ファイルを読み取ります。
    -   BR は`~/.aws/credentials`パスの共有資格情報ファイルを読み取ります。

-   方法2: IAMロールに基づくアクセス

    S3 にアクセスできるIAMロールを、TiKV ノードとBRノードが実行される EC2 インスタンスに関連付けます。関連付け後、 BR は追加設定なしで S3 内のバックアップ ディレクトリに直接アクセスできるようになります。

    ```shell
    tiup br backup full --pd "${PD_IP}:2379" \
    --storage "s3://${host}/${path}"
    ```

</div>
<div label="GCS" value="gcs">

アクセス キーを指定して、GCS へのアクセスに使用するアカウントを設定できます。 `credentials-file`パラメータを指定すると、指定された`credentials-file`使用して認証が行われます。 URI でキーを指定する以外に、次の方法もサポートされています。

-   BRは環境変数`$GOOGLE_APPLICATION_CREDENTIALS`で指定されたパスのファイルを読み取ります。
-   BR はファイル`~/.config/gcloud/application_default_credentials.json`を読み取ります。
-   BR は、クラスターが GCE または GAE で実行されているときに、メタデータサーバーから資格情報を取得します。

</div>
<div label="Azure Blob Storage" value="azure">

-   方法1: 共有アクセス署名を指定する

    URI に`account-name`と`sas-token`指定すると、指定されたアカウント名と共有アクセス署名 (SAS) トークンを使用して認証が実行されます。SAS トークンには`&`文字が含まれていることに注意してください。これを URI に追加する前に`%26`としてエンコードする必要があります。パーセントエンコードを使用して`sas-token`全体を直接エンコードすることもできます。

-   方法2: アクセスキーを指定する

    URI に`account-name`と`account-key`指定すると、指定したアカウント名とアカウントキーを使用して認証が行われます。 URI にキーを指定する方法の他に、 BR は環境変数`$AZURE_STORAGE_KEY`からキーを読み取ることもできます。

-   方法 3: バックアップと復元に Azure AD を使用する

    BRが実行されているノードで環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID` `$AZURE_CLIENT_SECRET`設定します。

    -   TiUP を使用してクラスターを起動すると、TiKV は systemd サービスを使用します。次の例は、TiKV の前述の 3 つの環境変数を構成する方法を示しています。

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

    -   コマンドラインで起動した TiKV およびBRの Azure AD 情報を構成するには、次のコマンドを実行して、オペレーティング環境で環境変数`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID` `$AZURE_CLIENT_SECRET`構成されているかどうかを確認するだけです。

        ```shell
        echo $AZURE_CLIENT_ID
        echo $AZURE_TENANT_ID
        echo $AZURE_CLIENT_SECRET
        ```

    -   BR を使用してデータを Azure Blob Storage にバックアップします。

        ```shell
        tiup br backup full -u "${PD_IP}:2379" \
        --storage "azure://external/backup-20220915?account-name=${account-name}"
        ```

</div>
</SimpleTab>

## サーバー側の暗号化 {#server-side-encryption}

### Amazon S3 サーバー側暗号化 {#amazon-s3-server-side-encryption}

BR は、Amazon S3 にデータをバックアップするときにサーバー側の暗号化をサポートします。また、 BRを使用して S3 サーバー側の暗号化用に作成した AWS KMS キーを使用することもできます。詳細については、 [BR S3 サーバー側暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)参照してください。

### Azure Blob Storage サーバー側暗号化 {#azure-blob-storage-server-side-encryption}

BR は、Azure Blob Storage にデータをバックアップするときに、Azure サーバー側暗号化スコープの指定や暗号化キーの提供をサポートしています。この機能を使用すると、同じstorageアカウントの異なるバックアップ データに対してセキュリティ境界を確立できます。詳細については、 [BR Azure Blob Storage サーバー側暗号化](/encryption-at-rest.md#br-azure-blob-storage-server-side-encryption)参照してください。

## storageサービスでサポートされているその他の機能 {#other-features-supported-by-the-storage-service}

Amazon [S3 オブジェクトロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)は、指定された保持期間中にバックアップ データが誤ってまたは意図的に削除されるのを防ぎ、データのセキュリティと整合性を強化します。v6.3.0 以降、 BR はスナップショット バックアップの Amazon S3 オブジェクト ロックをサポートし、フル バックアップのレイヤーをさらに強化します。v8.0.0 以降、PITR も Amazon S3 オブジェクト ロックをサポートします。フル バックアップでもログ データ バックアップでも、オブジェクト ロック機能により、より信頼性の高いデータ保護が保証され、データのバックアップとリカバリのセキュリティがさらに強化され、規制要件を満たすことができます。

BRと PITR は、Amazon S3 オブジェクト ロック機能が有効か無効かを自動的に検出します。追加の操作を実行する必要はありません。

> **警告：**
>
> スナップショット バックアップまたは PITR ログ バックアップ プロセス中にオブジェクト ロック機能が有効になっている場合、スナップショット バックアップまたはログ バックアップが失敗する可能性があります。バックアップを続行するには、スナップショット バックアップまたは PITR ログ バックアップ タスクを再起動する必要があります。
