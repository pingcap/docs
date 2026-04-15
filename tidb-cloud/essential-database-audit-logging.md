---
title: Database Audit Logging (Beta) for TiDB Cloud Essential
summary: TiDB CloudでTiDB Cloud Essentialインスタンスを監査する方法について学びましょう。
aliases: ['/ja/tidbcloud/serverless-audit-logging']
---

# TiDB Cloud Essentialのデータベース監査ログ機能 (ベータ版) {#database-audit-logging-beta-for-tidb-cloud-essential}

TiDB Cloud Essentialは、実行されたSQLステートメントなど、データベースへのユーザーアクセスアクティビティを記録する監査ログ機能を提供します。

> **注記：**
>
> 現在、データベース監査ログ機能はリクエストに応じてのみ利用可能です。この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)**？」**をクリックし、 次に**「サポートチケット」**をクリックして[ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/portals)に移動します。チケットを作成し、 **「説明」**フィールドに「 TiDB Cloud Essentialデータベース監査ログの申請」と入力して、 **「送信」を**クリックします。

組織のユーザーアクセスポリシーやその他の情報セキュリティ対策の有効性を評価するには、データベース監査ログを定期的に分析することがセキュリティ上のベストプラクティスです。

監査ログ機能は**デフォルトでは無効になっています**。TiDB TiDB Cloud Essentialインスタンスの監査を行うには、監査ログを有効にする必要があります。

## 監査ログの設定 {#audit-logging-configurations}

### データ編集 {#data-redaction}

TiDB Cloud Essentialは、デフォルトでは監査ログ内の機密データをマスキングします。以下のSQL文を例に挙げます。

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

以下のように編集されています。

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

### ログファイルのローテーション {#log-file-rotation}

TiDB Cloud Essentialは、以下のいずれかの条件が満たされた場合に新しい監査ログファイルを生成します。

-   現在のログファイルがローテーションサイズ（デフォルトでは100MiB）に達しました。
-   前回のログ生成から、ローテーション間隔（デフォルトでは1時間）が経過しました。内部スケジューリングメカニズムによっては、ログ生成が数分遅れる場合があります。

## 監査ログの場所 {#audit-logging-locations}

監査ログは以下の場所に保存できます。

-   TiDB Cloud
-   [Amazon S3](https://aws.amazon.com/s3/)
-   [Google Cloud Storage](https://cloud.google.com/storage)
-   [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
-   [Alibaba Cloudオブジェクトストレージサービス（OSS）](https://www.alibabacloud.com/product/oss)

### TiDB Cloud {#tidb-cloud}

TiDB Cloudに監査ログを保存し、ローカルマシンにダウンロードできます。監査ログは365日後に期限切れとなり、削除されます。保存期間の延長をご希望の場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)までお問い合わせください。

### Amazon S3 {#amazon-s3}

監査ログをAmazon S3に保存するには、以下の情報を提供する必要があります。

-   URI: `s3://<bucket-name>/<folder-path>/`
-   アクセス認証情報：以下のいずれかを選択してください。
    -   `s3:PutObject`権限を持つ[アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)。
    -   `s3:PutObject`権限を持つ[ロールARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) 。ロールARNの使用は、AWSでホストされているクラスターのみでサポートされています。

詳細については、 [Amazon S3へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)参照してください。

### Google Cloud Storage {#google-cloud-storage}

監査ログをGoogle Cloud Storageに保存するには、以下の情報を提供する必要があります。

-   URI: `gs://<bucket-name>/<folder-path>/`
-   アクセス資格情報: `storage.objects.create`および`storage.objects.delete`権限を持つサービス[サービスアカウントキー](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)。

詳細については、 [GCSへのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)参照してください。

### Azure Blob Storage {#azure-blob-storage}

Azure Blob Storage に監査ログを保存するには、以下の情報を提供する必要があります。

-   URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`または`https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
-   [共有アクセス署名（SAS）トークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)資格情報: `Read`および`Write`および { `Container` `Object`権限を持つ共有アクセス宣言（SAS） ブラウザ。

詳細については、 [Azure Blob Storageへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)参照してください。

### アリババクラウドOSS {#alibaba-cloud-oss}

Alibaba Cloud OSSに監査ログを保存するには、以下の情報を提供する必要があります。

-   URI: `oss://<bucket-name>/<folder-path>/`
-   アクセス資格情報: OSS バケットへのデータのエクスポートを許可する`oss:PutObject`および`oss:GetBucketInfo`権限を持つ[アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)キーペア。

詳細については、 [Alibaba Cloudオブジェクトストレージサービス（OSS）へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)参照してください。

## 監査ログフィルタルール {#audit-logging-filter-rules}

監査ログをフィルタリングするには、ログに記録するイベントを指定するフィルタルールを作成する必要があります。

フィルタルールには以下のフィールドが含まれます。

-   `users` : 監査イベントをフィルタリングするためのユーザー名のリスト。ワイルドカード`%`を使用すると、任意のユーザー名に一致させることができます。
-   `filters` : フィルタオブジェクトのリスト。各フィルタオブジェクトには、次のフィールドが含まれます。

    -   `classes` : 監査イベントをフィルタリングするためのイベントクラスのリスト。例: `["QUERY", "EXECUTE"]` 。
    -   `tables` : テーブル フィルターのリスト。詳細については、 [テーブルフィルター](https://docs.pingcap.com/tidb/stable/table-filter/)参照してください。
    -   `statusCodes` : 監査イベントをフィルタリングするためのステータスコードのリスト。 `1`は成功、 `0`は失敗を意味します。

以下の表は、データベース監査ログにおけるすべてのイベントクラスを示しています。

| イベントクラス             | 説明                                                           | 親クラス         |
| ------------------- | ------------------------------------------------------------ | ------------ |
| `CONNECTION`        | ハンドシェイク、接続、切断、接続リセット、ユーザー変更など、接続に関連するすべての操作を記録します。           | -            |
| `CONNECT`           | 接続におけるハンドシェイクのすべての操作を記録します                                   | `CONNECTION` |
| `DISCONNECT`        | 切断操作の全記録                                                     | `CONNECTION` |
| `CHANGE_USER`       | 変更されたユーザーのすべての操作を記録します                                       | `CONNECTION` |
| `QUERY`             | SQLステートメントのすべての操作を記録します。これには、データのクエリと変更に関するすべてのエラーが含まれます。    | -            |
| `TRANSACTION`       | `BEGIN` 、 `COMMIT` 、 `ROLLBACK`などのトランザクションに関連するすべての操作を記録します。 | `QUERY`      |
| `EXECUTE`           | `EXECUTE`ステートメントのすべての操作を記録します。                               | `QUERY`      |
| `QUERY_DML`         | `INSERT` 、 `REPLACE` 、 `UPDATE` 、および`DELETE` `LOAD DATA`     | `QUERY`      |
| `INSERT`            | `INSERT`ステートメントのすべての操作を記録します。                                | `QUERY_DML`  |
| `REPLACE`           | `REPLACE`ステートメントのすべての操作を記録します。                               | `QUERY_DML`  |
| `UPDATE`            | `UPDATE`ステートメントのすべての操作を記録します。                                | `QUERY_DML`  |
| `DELETE`            | `DELETE`ステートメントのすべての操作を記録します。                                | `QUERY_DML`  |
| `LOAD DATA`         | `LOAD DATA`ステートメントのすべての操作を記録します。                             | `QUERY_DML`  |
| `SELECT`            | `SELECT`ステートメントのすべての操作を記録します。                                | `QUERY`      |
| `QUERY_DDL`         | DDLステートメントのすべての操作を記録します                                      | `QUERY`      |
| `AUDIT`             | TiDBデータベース監査の設定に関連するすべての操作（システム変数の設定やシステム関数の呼び出しなど）を記録します。   | -            |
| `AUDIT_FUNC_CALL`   | TiDB Cloudデータベース監査に関連する呼び出しシステム関数のすべての操作を記録します。              | `AUDIT`      |
| `AUDIT_SET_SYS_VAR` | システム変数の設定操作をすべて記録します                                         | `AUDIT`      |

> **注記：**
>
> `AUDIT`イベント クラスとそのサブクラスは常に監査ログに記録され、フィルタリングすることはできません。

## 監査ログの設定 {#configure-audit-logging}

監査ログの有効化、編集、無効化が可能です。

### 監査ログを有効にする {#enable-audit-logging}

TiDB CloudコンソールまたはTiDB Cloud CLIを使用して、 TiDB Cloud Essentialインスタンスの監査ログを有効にすることができます。

> **注記：**
>
> 監査ログを有効にするだけでは監査ログは生成されません。また、ログに記録するイベントを指定するフィルターを構成する必要があります。詳細については、[監査ログフィルタルールの管理](#manage-audit-logging-filter-rules)参照してください。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログの**ページで、 **[有効にする]**をクリックします。

4.  監査ログのstorage場所を選択し、必要な情報を入力します。次に、 **「接続をテスト」をクリックし、「次へ」**または**「次へ」を**クリックします。利用可能なstorage場所の詳細については、[監査ログの場所](#audit-logging-locations)を参照してください。

5.  **データベース監査ログ設定**ダイアログで、ログファイルのローテーションとログのマスキング設定を入力し、 **[保存]**をクリックします。

</div>

<div label="CLI">

Amazon S3storageを例にとってみましょう。監査ログを有効にして監査ログをAmazon S3に保存するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-url> --s3.access-key-id <s3-access-key-id> --s3.secret-access-key <s3-secret-access-key> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```

`--rotation-size-mib` 、 `--rotation-interval-minutes` 、および`--unredacted`パラメータはオプションです。これらを指定しない場合、デフォルト値が使用されます。

</div>
</SimpleTab>

### 監査ログの編集 {#edit-audit-logging}

TiDB Cloud Essentialインスタンスの監査ログは、有効化後に編集できます。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログの**ページで、 **[設定]**をクリックします。

4.  **データベース監査ログ設定**ダイアログで、ログファイルのローテーションまたはログのマスキング設定を更新し、 **[保存]**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用して監査ログ設定を更新するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```

</div>
</SimpleTab>

### 監査ログを無効にする {#disable-audit-logging}

TiDB Cloud Essentialインスタンスの監査ログを無効にすることができます。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログの**ページで、右上隅の**...**をクリックし、次に**無効に**します。

4.  **「DB監査ログを無効にする」**ダイアログで、 **「無効にする」**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用して監査ログを無効にするには、次のコマンドを実行します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --disabled=true
```

</div>
</SimpleTab>

## 監査ログフィルタルールの管理 {#manage-audit-logging-filter-rules}

監査ログフィルタルールを作成、編集、無効化、削除できます。

### フィルタルールを作成する {#create-a-filter-rule}

フィルタルールを作成するには、監査ログに記録するユーザーとイベントを定義します。ユーザー、イベントクラス、テーブル、ステータスコードを指定することで、ログ記録をニーズに合わせてカスタマイズできます。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログの**ページで、 **[フィルタルールの追加]**をクリックします。

4.  **[フィルター ルールの追加]**ダイアログで、 **[フィルター名]** 、 **[SQL ユーザー]** 、および**[フィルター ルール]**フィールドに入力し、 **[確認]**をクリックします。これらのフィールドの詳細については、[監査ログフィルタルール](#audit-logging-filter-rules)を参照してください。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してフィルタルールを作成するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

</div>
</SimpleTab>

### フィルタールールを編集する {#edit-a-filter-rule}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログ**ページで、編集するフィルタルールを見つけ、その行の**...**をクリックしてから、 **[編集]**をクリックします。

4.  **「フィルタールールの編集」**ダイアログで、 **「フィルター名」**または**「フィルタールール」**フィールドを更新し、 **「確認」**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してフィルタルールを編集するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

</div>
</SimpleTab>

### フィルタルールを無効にする {#disable-a-filter-rule}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログの**ページで、無効にしたいフィルタルールを見つけ、トグルをオフにしてフィルタルールを無効にします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してフィルタルールを無効にするには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```

</div>
</SimpleTab>

### フィルタルールを削除する {#delete-a-filter-rule}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログ**ページで、削除するフィルタルールを見つけて、 **...**をクリックします。

4.  **「削除」**をクリックし、次に**「了解しました。削除して確定します」を**クリックしてください。

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --filter-rule-id <rule-id>
```

</div>
</SimpleTab>

## TiDB Cloud Storage を使用した監査ログへのアクセス {#access-audit-logging-with-tidb-cloud-storage}

TiDB Cloudに監査ログを保存すると、 TiDB Cloud Essentialはそれらを`YYYY-MM-DD-<index>.log`という名前の読み取り可能なテキストファイルとして保存します。これらのファイルは、 TiDB CloudコンソールまたはTiDB Cloud CLIを使用して表示およびダウンロードできます。

> **注記：**
>
> -   TiDB Cloud Essentialは、監査ログが時系列順に保存されることを保証しません。 `YYYY-MM-DD-<index>.log`という名前のログファイルには、それ以前の日付のエントリが含まれている可能性があります。
> -   特定の日付（例：2025年1月1日）のすべてのログを取得するには、 `--start-date 2025-01-01`と`--end-date 2025-01-02` 。場合によっては、すべてのログファイルをダウンロードし、 `TIME`フィールドでソートする必要があるかもしれません。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「DB監査ログ」**をクリックします。

3.  **DB監査ログ**ページでは、 **TiDB Cloud Storageの**下にある監査ログの一覧を表示できます。

4.  監査ログをダウンロードするには、リストから1つ以上のログを選択し、 **「ダウンロード」**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLIを使用して監査ログをダウンロードするには、次のコマンドを実行します。

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

-   `start-date` : ダウンロードする監査ログの開始日。形式は`YYYY-MM-DD`です。例: `2025-01-01` 。
-   `end-date` : ダウンロードする監査ログの終了日。形式は`YYYY-MM-DD`です。例: `2025-01-01` 。

</div>
</SimpleTab>

## 監査ログフィールド {#audit-logging-fields}

TiDB Cloudは、監査ログ内の各データベースイベントレコードに対して、以下のフィールドを提供します。

### 一般情報 {#general-information}

すべての監査ログの種類には、以下の情報が含まれています。

| 分野                      | 説明                                             |
| ----------------------- | ---------------------------------------------- |
| `ID`                    | 業務の監査記録を識別する固有の識別子。                            |
| `TIME`                  | 監査記録のタイムスタンプ。                                  |
| `EVENT`                 | 監査記録のイベントクラス。複数のイベントタイプはカンマで区切られます（ `,` ）。     |
| `USER`                  | 監査記録のユーザー名。                                    |
| `ROLES`                 | 操作時のユーザーの役割。                                   |
| `CONNECTION_ID`         | ユーザーの接続を識別する識別子。                               |
| `TABLES`                | この監査記録に関連するアクセスされたテーブル。                        |
| `STATUS_CODE`           | 監査記録のステータスコード。 `1`は成功、 `0`は失敗を意味します。           |
| `KEYSPACE_NAME`         | 監査レコードのキースペース名。                                |
| `SERVERLESS_TENANT_ID`  | TiDB Cloud Essentialインスタンスが属するサーバーレステナントのID。   |
| `SERVERLESS_PROJECT_ID` | TiDB Cloud Essentialインスタンスが属するサーバーレスプロジェクトのID。 |
| `SERVERLESS_CLUSTER_ID` | 監査レコードが属するサーバーレスTiDB Cloud EssentialインスタンスのID。 |
| `REASON`                | 監査記録のエラーメッセージ。操作中にエラーが発生した場合にのみ記録されます。         |

### SQLステートメント情報 {#sql-statement-information}

イベントクラスが`QUERY`または`QUERY`のサブクラスである場合、監査ログには次の情報が含まれます。

| 分野               | 説明                                                                     |
| ---------------- | ---------------------------------------------------------------------- |
| `CURRENT_DB`     | 現在使用しているデータベースの名前。                                                     |
| `SQL_TEXT`       | 実行されたSQLステートメント。監査ログのマスキングが有効になっている場合は、マスキングされたSQLステートメントが記録されます。      |
| `EXECUTE_PARAMS` | `EXECUTE`ステートメントのパラメータ。イベントクラスに`EXECUTE`が含まれ、かつ編集が無効になっている場合にのみ記録されます。 |
| `AFFECTED_ROWS`  | SQL ステートメントの影響を受ける行数。イベント クラスに`QUERY_DML`が含まれている場合にのみ記録されます。           |

### 接続情報 {#connection-information}

イベントクラスが`CONNECTION`または`CONNECTION`のサブクラスである場合、監査ログには次の情報が含まれます。

| 分野                | 説明                                                     |
| ----------------- | ------------------------------------------------------ |
| `CURRENT_DB`      | 現在のデータベースの名前。イベントクラスにDISCONNECTが含まれている場合、この情報は記録されません。 |
| `CONNECTION_TYPE` | 接続の種類（ソケット、UnixSocket、SSL/TLSなど）。                      |
| `PID`             | 現在の接続のプロセスID。                                          |
| `SERVER_VERSION`  | 接続されているTiDBサーバーの現在のバージョン。                              |
| `SSL_VERSION`     | 現在使用されているSSLのバージョン。                                    |
| `HOST_IP`         | 接続されているTiDBサーバーの現在のIPアドレス。                             |
| `HOST_PORT`       | 接続されているTiDBサーバーの現在のポート番号。                              |
| `CLIENT_IP`       | クライアントの現在のIPアドレス。                                      |
| `CLIENT_PORT`     | クライアントの現在のポート番号。                                       |

> **注記：**
>
> トラフィックの可視性を向上させるため、 `CLIENT_IP`では、ロードバランサー (LB) IP の代わりに、AWS PrivateLink 経由の接続の実際のクライアント IP アドレスが表示されるようになりました。現在、この機能はベータ版であり、AWS リージョン`Frankfurt (eu-central-1)`でのみ利用可能です。

### 監査操作情報 {#audit-operation-information}

イベントクラスが`AUDIT`または`AUDIT`のサブクラスである場合、監査ログには次の情報が含まれます。

| 分野                | 説明                            |
| ----------------- | ----------------------------- |
| `AUDIT_OP_TARGET` | TiDB Cloudデータベース監査に関連する設定対象。  |
| `AUDIT_OP_ARGS`   | TiDB Cloudデータベース監査に関連する設定の引数。 |

## 監査ログの制限 {#audit-logging-limitations}

TiDB Cloud Essential は監査ログの順序を保証しないため、最新のイベントを見つけるにはすべてのログファイルを確認する必要がある場合があります。ログを時系列順に並べ替えるには、監査ログの`TIME`フィールドを使用できます。
