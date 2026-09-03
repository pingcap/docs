---
title: Export Data from TiDB Cloud Premium
summary: TiDB Cloud Premiumインスタンスからデータをエクスポートする方法を学びましょう。
---

# TiDB Cloud Premium からデータをエクスポート {#export-data-from-tidb-cloud-premium}

TiDB Cloudを使用すると、{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスから外部ストレージサービスにデータをエクスポートできます。エクスポートしたデータは、バックアップ、移行、データ分析、その他の目的に使用できます。

[mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)やTiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)などのツールを使用してデータをエクスポートすることもできますが、TiDB Cloudが提供するエクスポート機能は、{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスからデータをエクスポートするための、より便利で効率的な方法です。この機能には、次のような利点があります。

- 利便性: エクスポートサービスを利用することで、{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスからデータをエクスポートするためのシンプルで使いやすい方法が提供され、追加のツールやリソースが不要になります。
- 分離性: エクスポートサービスは独立したコンピューティングリソースを使用するため、オンラインサービスで使用されるリソースから確実に分離されます。
- 一貫性: エクスポートサービスは、ロックを発生させることなくエクスポートされたデータの一貫性を保証するため、オンラインサービスに影響を与えません。

> **Note:**
>
> - 現在、この機能はリクエストに応じてのみ利用可能です。この機能をリクエストするには、[TiDB Cloud console](https://tidbcloud.com)の右下隅にある**?**をクリックし、次に**Support Tickets**をクリックして[Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals)に移動します。チケットを作成し、**Description**フィールドに "Apply for data export for {{{ .premium }}}<CustomContent plan="byoc"> or {{{ .byoc }}}</CustomContent> instance" と入力して、**Submit**をクリックします。
> - エクスポートの最大サイズは 1 TiB です。この制限を超えるエクスポートは失敗する可能性があります。より多くのデータをエクスポートする場合、またはより高いエクスポート速度をリクエストする場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## エクスポート先 {#export-locations}

データを以下の外部ストレージの場所にエクスポートできます。

- [Amazon S3](https://aws.amazon.com/s3/)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
- [Alibaba Cloudオブジェクトストレージサービス（OSS）](https://www.alibabacloud.com/product/oss)

### Amazon S3 {#amazon-s3}

データをAmazon S3にエクスポートするには、以下の情報を提供する必要があります。

- URI: `s3://<bucket-name>/<folder-path>/`
- 以下のいずれかのアクセス認証情報：
    - [アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): アクセスキーに `s3:PutObject` 権限があることを確認してください。
    - [ロールARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html): ロールARN（Amazon Resource Name）に `s3:PutObject` 権限があることを確認してください。なお、ロールARNをサポートしているのは、AWS 上でホストされている {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスのみです。

詳細については、 [外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)を参照してください。

### Azure Blob Storage {#azure-blob-storage}

Azure Blob Storage にデータをエクスポートするには、以下の情報を提供する必要があります。

- URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`または`https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- アクセス資格情報: Azure Blob Storage コンテナーの[共有アクセス署名（SAS）トークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。 SAS トークンに、 `Read`および`Write`リソースに対する`Container`および`Object`権限があることを確認してください。

詳細については、 [外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)を参照してください。

### アリババクラウドOSS {#alibaba-cloud-oss}

Alibaba Cloud OSSにデータをエクスポートするには、以下の情報を提供する必要があります。

- URI: `oss://<bucket-name>/<folder-path>/`
- アクセス資格情報: Alibaba Cloud アカウントの[アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)。 AccessKey ペアに`oss:PutObject`および`oss:GetBucketInfo`権限があることを確認してください。

詳細については、 [外部ストレージへのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)を参照してください。

## エクスポートオプション {#export-options}

### データフィルタリング {#data-filtering}

TiDB Cloudコンソールは、選択したデータベースとテーブルを含むデータのエクスポートをサポートしています。

### データ形式 {#data-formats}

データを以下の形式でエクスポートできます。

- `SQL` : データを SQL 形式でエクスポートします。
- `CSV` : データをCSV形式でエクスポートします。以下のオプションを指定できます。
    - `delimiter` : エクスポートされたデータで使用される区切り文字を指定します。デフォルトの区切り文字は`"`です。
    - `separator` : エクスポートされたデータ内のフィールドを区切るために使用される文字を指定します。デフォルトの区切り文字は`,`です。
    - `header` : エクスポートされたデータにヘッダー行を含めるかどうかを指定します。デフォルト値は`true`です。
    - `null-value` : エクスポートされたデータ内の NULL 値を表す文字列を指定します。デフォルト値は`\N`です。

スキーマとデータは、以下の命名規則に従ってエクスポートされます。

| アイテム             | 圧縮されていない              | 圧縮されている                                   |
| -------------------- | ----------------------------- | ------------------------------------------------ |
| データベーススキーマ | {database}-schema-create.sql  | {database}-schema-create.sql.{compression-type}  |
| テーブルスキーマ     | {database}.{table}-schema.sql | {database}.{table}-schema.sql.{compression-type} |
| データ               | {database}.{table}.{0001}.csv | {database}.{table}.{0001}.csv.{compression-type} |
| データ               | {database}.{table}.{0001}.sql | {database}.{table}.{0001}.sql.{compression-type} |

### データ圧縮 {#data-compression}

エクスポートされたCSVデータとSQLデータは、以下のアルゴリズムを使用して圧縮できます。

- `gzip` (デフォルト): `gzip`を使用してエクスポートされたデータを圧縮します。
- `snappy` : `snappy`を使用してエクスポートされたデータを圧縮します。
- `zstd` : `zstd`を使用してエクスポートされたデータを圧縮します。
- `none` : エクスポートされたデータを圧縮しません。

## 例 {#examples}

### データをAmazon S3にエクスポートする {#export-data-to-amazon-s3}

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDB Instances**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 対象の{{{ .premium }}}<CustomContent plan="byoc">または{{{ .byoc }}}</CustomContent>インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Data** > **Export**をクリックします。

3. **Export**ページで、右上隅にある**Export Data**をクリックします。次に、以下の設定を行います。

    - **Task Name**：エクスポートタスクの名前を入力してください。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    - **Source Connection**：{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの**Username**と**Password**を入力し、**Test Connection**をクリックして認証情報を確認します。
    - **Target Connection**：
        - **Storage Provider**：Amazon S3を選択してください。
        - **Folder URI**：`s3://<bucket-name>/<folder-path>/`形式でAmazon S3のURIを入力してください。
        - **Bucket Access**：以下のアクセス認証情報から1つを選択し、認証情報を入力してください。
            - **AWS Role ARN**：バケットにアクセスする権限を持つロール ARN を入力します。AWS CloudFormation を使用してロール ARN を作成することをお勧めします。詳細については、[外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)を参照してください。
            - **AWS Access Key**：バケットへのアクセス権限を持つアクセスキーIDとアクセスキーシークレットを入力してください。
    - **Exported Data**：エクスポートするデータベースまたはテーブルを選択してください。
    - **Data Format**：**SQL**または**CSV**を選択してください。
    - **Compression**：**Gzip**、**Snappy**、**Zstd**、または**None**を選択してください。

4. **Export**をクリックします。

### データをAzure Blob Storageにエクスポートする {#export-data-to-azure-blob-storage}

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDB Instances**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで **Data** > **Export** をクリックします。

3. **Export**ページで、右上隅にある**Export Data**をクリックします。次に、以下の設定を行います。

    - **Task Name**：エクスポートタスクの名前を入力してください。デフォルト値は `SNAPSHOT_{snapshot_time}` です。
    - **Source Connection**：{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの **Username** と **Password** を入力し、**Test Connection** をクリックして認証情報を確認します。
    - **Target Connection**：
        - **Storage Provider**：Azure Blob Storage を選択してください。
        - **Folder URI**：`azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` の形式で Azure Blob Storage の URI を入力してください。
        - **SAS Token**：コンテナーへのアクセス権限を持つ SAS トークンを入力します。[Azure ARM template](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/) を使用して SAS トークンを作成することを推奨します。詳細については、[外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access) を参照してください。
    - **Exported Data**：エクスポートするデータベースまたはテーブルを選択してください。
    - **Data Format**：**SQL** または **CSV** を選択してください。
    - **Compression**：**Gzip**、**Snappy**、**Zstd**、または **None** を選択してください。

4. **Export**をクリックします。

### データをAlibaba Cloud OSSにエクスポート {#export-data-to-alibaba-cloud-oss}

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDB Instances**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 対象の{{{ .premium }}}<CustomContent plan="byoc">または{{{ .byoc }}}</CustomContent>インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Data** > **Export**をクリックします。

3. **Export**ページで、右上隅にある**Export Data**をクリックします。

    - **Task Name**：エクスポートタスクの名前を入力してください。デフォルト値は `SNAPSHOT_{snapshot_time}` です。
    - **Source Connection**：{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの **Username** と **Password** を入力し、**Test Connection** をクリックして認証情報を確認します。
    - **Target Connection**：
        - **Storage Provider**：Alibaba Cloud OSS を選択してください。
        - **Folder URI**：データをエクスポートする Alibaba Cloud OSS URI を `oss://<bucket-name>/<folder-path>/` 形式で入力します。
        - **AccessKey ID** と **AccessKey Secret**：バケットへのアクセス権限を持つ AccessKey ID と AccessKey Secret を入力してください。
    - **Exported Data**：エクスポートするデータベースまたはテーブルを選択してください。
    - **Data Format**：**SQL** または **CSV** を選択してください。
    - **Compression**：**Gzip**、**Snappy**、**Zstd**、または **None** を選択してください。

4. **Export**をクリックします。

### エクスポートタスクをキャンセルする {#cancel-an-export-task}

進行中のエクスポートタスクをキャンセルするには、以下の手順に従ってください。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDB Instances**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで **Data** > **Export** をクリックします。

3. **Export**ページで、エクスポートタスク一覧を表示します。

4. キャンセルしたいエクスポートタスクを選択し、 **Action**をクリックします。

5. ドロップダウンリストから**Cancel**を選択してください。なお、キャンセルできるのは**Running**ステータスのエクスポートタスクのみです。
