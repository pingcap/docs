---
title: Database Audit Logging (Beta) for TiDB Cloud Essential
summary: TiDB CloudでTiDB Cloud Essential クラスターを監査する方法について説明します。
aliases: ['/tidbcloud/serverless-audit-logging']
---

# TiDB Cloud Essential のデータベース監査ログ (ベータ版) {#database-audit-logging-beta-for-tidb-cloud-essential}

TiDB Cloud Essential は、実行された SQL ステートメントなど、データベースのユーザー アクセス アクティビティを記録する監査ログ機能を提供します。

> **注記：**
>
> 現在、データベース監査ログ機能はリクエストに応じてのみご利用いただけます。この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポートチケット」**をクリックして[ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/portals)に進みます。チケットを作成し、 **「説明」**欄に「 TiDB Cloud Essential データベース監査ログの申請」と入力して、 **「送信」を**クリックしてください。

組織のユーザー アクセス ポリシーやその他の情報セキュリティ対策の有効性を評価するには、データベース監査ログを定期的に分析することがセキュリティのベスト プラクティスです。

監査ログ機能は**デフォルトで無効になっています**。TiDB クラスターを監査するには、監査ログを有効にする必要があります。

## 監査ログの構成 {#audit-logging-configurations}

### データ編集 {#data-redaction}

TiDB Cloud Essentialはデフォルトで監査ログ内の機密データを削除します。次のSQL文を例に挙げましょう。

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

以下のように編集されています。

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

### ログファイルのローテーション {#log-file-rotation}

TiDB Cloud Essential は、次のいずれかの条件が満たされると、新しい監査ログ ファイルを生成します。

-   現在のログ ファイルがローテーション サイズ (デフォルトでは 100 MiB) に達しました。
-   前回のログ生成からローテーション間隔（デフォルトでは1時間）が経過しました。内部のスケジュール設定によっては、ログ生成が数分遅れる場合があります。

## 監査ログの場所 {#audit-logging-locations}

監査ログは次の場所に保存できます。

-   TiDB Cloud
-   [アマゾンS3](https://aws.amazon.com/s3/)
-   [Googleクラウドストレージ](https://cloud.google.com/storage)
-   [Azure BLOB ストレージ](https://azure.microsoft.com/en-us/services/storage/blobs/)
-   [Alibaba Cloud オブジェクト ストレージ サービス (OSS)](https://www.alibabacloud.com/product/oss)

### TiDB Cloud {#tidb-cloud}

監査ログはTiDB Cloudに保存し、ローカルマシンにダウンロードできます。監査ログは365日後に有効期限が切れ、削除されます。保存期間の延長をご希望の場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)ご連絡ください。

### アマゾンS3 {#amazon-s3}

監査ログを Amazon S3 に保存するには、次の情報を提供する必要があります。

-   URI: `s3://<bucket-name>/<folder-path>/`
-   アクセス資格情報: 次のいずれかを選択します。
    -   `s3:PutObject`許可を持つ[アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) 。
    -   権限`s3:PutObject`を持つ[役割ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)でホストされているクラスターのみがロールARNの使用をサポートします。

詳細については[Amazon S3 アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)参照してください。

### Googleクラウドストレージ {#google-cloud-storage}

監査ログを Google Cloud Storage に保存するには、次の情報を提供する必要があります。

-   URI: `gs://<bucket-name>/<folder-path>/`
-   アクセス資格情報: `storage.objects.create`および`storage.objects.delete`権限を持つ[サービスアカウントキー](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) 。

詳細については[GCS アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)参照してください。

### Azure BLOB ストレージ {#azure-blob-storage}

監査ログを Azure Blob Storage に保存するには、次の情報を提供する必要があります。

-   URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`または`https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
-   アクセス資格情報: `Container`および`Object`リソースに対する`Read`および`Write`権限を持つ[共有アクセス署名（SAS）トークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) 。

詳細については[Azure Blob Storage アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)参照してください。

### アリババクラウドOSS {#alibaba-cloud-oss}

Alibaba Cloud OSS に監査ログを保存するには、次の情報を提供する必要があります。

-   URI: `oss://<bucket-name>/<folder-path>/`
-   アクセス資格情報: OSS バケットへのデータのエクスポートを許可する`oss:PutObject`および`oss:GetBucketInfo`権限を持つ[アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) 。

詳細については[Alibaba Cloud Object Storage Service (OSS) アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)参照してください。

## 監査ログフィルタルール {#audit-logging-filter-rules}

監査ログをフィルタリングするには、ログに記録するイベントを指定するフィルタ ルールを作成する必要があります。

フィルター ルールには次のフィールドが含まれます。

-   `users` : 監査イベントをフィルタリングするユーザー名のリスト。ワイルドカード`%`を使用すると、任意のユーザー名に一致します。
-   `filters` : フィルターオブジェクトのリスト。各フィルターオブジェクトには以下のフィールドが含まれます。

    -   `classes` : 監査イベントをフィルタリングするイベントクラスのリスト。例： `["QUERY", "EXECUTE"]` 。
    -   `tables` : テーブルフィルターのリスト。詳細については、 [テーブルフィルター](https://docs.pingcap.com/tidb/stable/table-filter/)参照してください。
    -   `statusCodes` : 監査イベントをフィルター処理するためのステータス コードのリスト。2 `1`成功、 `0`失敗を意味します。

次の表は、データベース監査ログのすべてのイベント クラスを示しています。

| イベントクラス             | 説明                                                             | 親クラス         |
| ------------------- | -------------------------------------------------------------- | ------------ |
| `CONNECTION`        | ハンドシェイク、接続、切断、接続のリセット、ユーザーの変更など、接続に関連するすべての操作を記録します。           | <li></li>    |
| `CONNECT`           | 接続時のハンドシェイクのすべての操作を記録する                                        | `CONNECTION` |
| `DISCONNECT`        | 切断のすべての操作を記録する                                                 | `CONNECTION` |
| `CHANGE_USER`       | ユーザーの変更に関するすべての操作を記録します                                        | `CONNECTION` |
| `QUERY`             | データのクエリと変更に関するすべてのエラーを含む、SQL ステートメントのすべての操作を記録します。             | <li></li>    |
| `TRANSACTION`       | `BEGIN`などのトランザクションに関連するすべての操作を記録し`ROLLBACK` `COMMIT`           | `QUERY`      |
| `EXECUTE`           | `EXECUTE`ステートメントのすべての操作を記録します                                  | `QUERY`      |
| `QUERY_DML`         | `INSERT` `UPDATE`含むDML文`DELETE`すべての操作を記録し`LOAD DATA` `REPLACE` | `QUERY`      |
| `INSERT`            | `INSERT`ステートメントのすべての操作を記録します                                   | `QUERY_DML`  |
| `REPLACE`           | `REPLACE`ステートメントのすべての操作を記録します                                  | `QUERY_DML`  |
| `UPDATE`            | `UPDATE`ステートメントのすべての操作を記録します                                   | `QUERY_DML`  |
| `DELETE`            | `DELETE`ステートメントのすべての操作を記録します                                   | `QUERY_DML`  |
| `LOAD DATA`         | `LOAD DATA`ステートメントのすべての操作を記録します                                | `QUERY_DML`  |
| `SELECT`            | `SELECT`ステートメントのすべての操作を記録します                                   | `QUERY`      |
| `QUERY_DDL`         | DDL文のすべての操作を記録する                                               | `QUERY`      |
| `AUDIT`             | システム変数の設定やシステム関数の呼び出しなど、TiDB データベース監査の設定に関連するすべての操作を記録します。     | <li></li>    |
| `AUDIT_FUNC_CALL`   | TiDB Cloudデータベース監査に関連するシステム関数の呼び出し操作をすべて記録します。                 | `AUDIT`      |
| `AUDIT_SET_SYS_VAR` | システム変数の設定操作をすべて記録します                                           | `AUDIT`      |

> **注記：**
>
> `AUDIT`イベント クラスとそのサブクラスは常に監査ログに記録され、フィルター処理することはできません。

## 監査ログを構成する {#configure-audit-logging}

監査ログを有効化、編集、無効化できます。

### 監査ログを有効にする {#enable-audit-logging}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、 TiDB Cloud Essential クラスターの監査ログを有効にできます。

> **注記：**
>
> 監査ログを有効にするだけでは監査ログは生成されません。ログに記録するイベントを指定するには、フィルターも設定する必要があります。詳細については、 [監査ログフィルタルールを管理する](#manage-audit-logging-filter-rules)参照してください。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページで、 **[有効化]**をクリックします。

4.  監査ログのstorage場所を選択し、必要な情報を入力してください。 **「接続テスト」をクリックし、「次へ」**または**「次へ」を**クリックします。利用可能なstorage場所の詳細については、 [監査ログの場所](#audit-logging-locations)参照してください。

5.  **[データベース監査ログ設定]**ダイアログで、ログ ファイルのローテーションとログ編集の設定を入力し、 **[保存]**をクリックします。

</div>

<div label="CLI">

Amazon S3storageを例に挙げましょう。監査ログを有効にし、Amazon S3に監査ログを保存するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-url> --s3.access-key-id <s3-access-key-id> --s3.secret-access-key <s3-secret-access-key> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```

`--rotation-size-mib` 、 `--rotation-interval-minutes` 、 `--unredacted`パラメータはオプションです。指定しない場合は、デフォルト値が使用されます。

</div>
</SimpleTab>

### 監査ログの編集 {#edit-audit-logging}

TiDB Cloud Essential クラスターの監査ログは、有効化した後に編集できます。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページで、 **[設定]**をクリックします。

4.  **[データベース監査ログ設定]**ダイアログで、ログ ファイルのローテーションまたはログ編集設定を更新し、 **[保存]**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用して監査ログ設定を更新するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```

</div>
</SimpleTab>

### 監査ログを無効にする {#disable-audit-logging}

TiDB Cloud Essential クラスターの監査ログを無効にすることができます。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページで、右上隅の**[...]**をクリックし、 **[無効]**をクリックします。

4.  **DB 監査ログの無効化**ダイアログで、 **「無効化」**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用して監査ログを無効にするには、次のコマンドを実行します。

```shell
ticloud serverless audit-log config update -c <cluster-id> --disabled=true
```

</div>
</SimpleTab>

## 監査ログフィルタルールを管理する {#manage-audit-logging-filter-rules}

監査ログ フィルタ ルールを作成、編集、無効化、および削除できます。

### フィルタールールを作成する {#create-a-filter-rule}

フィルタールールを作成するには、監査ログに記録するユーザーとイベントを定義します。ユーザー、イベントクラス、テーブル、ステータスコードを指定して、ニーズに合わせてログをカスタマイズできます。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページで、**フィルター ルールの追加を**クリックします。

4.  **「フィルタルールの追加」**ダイアログで、 **「フィルタ名」** 、 **「SQLユーザー」** 、 **「フィルタルール**」の各フィールドに入力し、 **「確認」**をクリックします。これらのフィールドの詳細については、 [監査ログフィルタルール](#audit-logging-filter-rules)参照してください。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してフィルター ルールを作成するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

</div>
</SimpleTab>

### フィルタールールを編集する {#edit-a-filter-rule}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページで、編集するフィルター ルールを見つけて、その行の**[...** ] をクリックし、 **[編集]**をクリックします。

4.  **[フィルター ルールの編集]**ダイアログで、 **[フィルター名]**または**[フィルター ルール]**フィールドを更新し、 **[確認]**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してフィルター ルールを編集するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

</div>
</SimpleTab>

### フィルタルールを無効にする {#disable-a-filter-rule}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページで、無効にするフィルター ルールを見つけて、トグルをオフにしてフィルター ルールを無効にします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してフィルター ルールを無効にするには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```

</div>
</SimpleTab>

### フィルタールールを削除する {#delete-a-filter-rule}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページで、削除するフィルター ルールを見つけて、 **...**をクリックします。

4.  **「削除」**をクリックし、 **「理解しました」をクリックします。削除を**確定してください。

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --filter-rule-id <rule-id>
```

</div>
</SimpleTab>

## TiDB Cloudストレージによるアクセス監査ログ {#access-audit-logging-with-tidb-cloud-storage}

TiDB Cloudに監査ログを保存すると、 TiDB Cloud Essential はそれらを`YYYY-MM-DD-<index>.log`という名前の読み取り可能なテキストファイルとして保存します。これらのファイルは、TiDB CloudコンソールまたはTiDB Cloud CLI を使用して表示およびダウンロードできます。

> **注記：**
>
> -   TiDB Cloud Essential は、監査ログが必ずしも順番に保存されることを保証しません。ログファイル`YYYY-MM-DD-<index>.log`には、以前の日付のエントリが含まれている可能性があります。
> -   特定の日付（例えば2025年1月1日）のすべてのログを取得するには、 `--start-date 2025-01-01`と`--end-date 2025-01-02`を設定します。場合によっては、すべてのログファイルをダウンロードし、 `TIME`フィールドで並べ替える必要があるかもしれません。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[DB 監査ログ]**をクリックします。

3.  **DB 監査ログ**ページでは、 **TiDB Cloud Storage**の監査ログのリストを表示できます。

4.  監査ログをダウンロードするには、リストから 1 つ以上のログを選択し、 **[ダウンロード]**をクリックします。

</div>

<div label="CLI">

TiDB Cloud CLI を使用して監査ログをダウンロードするには、次のコマンドを実行します。

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

-   `start-date` : ダウンロードする監査ログの開始日。形式は`YYYY-MM-DD`です (例: `2025-01-01` )。
-   `end-date` : ダウンロードする監査ログの終了日。形式は`YYYY-MM-DD`です (例: `2025-01-01` )。

</div>
</SimpleTab>

## 監査ログフィールド {#audit-logging-fields}

監査ログ内の各データベース イベント レコードに対して、 TiDB Cloud は次のフィールドを提供します。

### 一般情報 {#general-information}

すべてのクラスの監査ログには、次の情報が含まれます。

| 分野                      | 説明                                           |
| ----------------------- | -------------------------------------------- |
| `ID`                    | 操作の監査レコードを識別する一意の識別子。                        |
| `TIME`                  | 監査レコードのタイムスタンプ。                              |
| `EVENT`                 | 監査レコードのイベントクラス。複数のイベントタイプはカンマ（ `,` ）で区切られます。 |
| `USER`                  | 監査レコードのユーザー名。                                |
| `ROLES`                 | 操作時のユーザーの役割。                                 |
| `CONNECTION_ID`         | ユーザーの接続の識別子。                                 |
| `TABLES`                | この監査レコードに関連するアクセスされたテーブル。                    |
| `STATUS_CODE`           | 監査レコードのステータス コード。1 `1`成功、 `0`失敗を意味します。       |
| `KEYSPACE_NAME`         | 監査レコードのキースペース名。                              |
| `SERVERLESS_TENANT_ID`  | クラスターが属するサーバーレス テナントの ID。                    |
| `SERVERLESS_PROJECT_ID` | クラスターが属するサーバーレス プロジェクトの ID。                  |
| `SERVERLESS_CLUSTER_ID` | 監査レコードが属するサーバーレス クラスターの ID。                  |
| `REASON`                | 監査レコードのエラーメッセージ。操作中にエラーが発生した場合にのみ記録されます。     |

### SQL文の情報 {#sql-statement-information}

イベント クラスが`QUERY`または`QUERY`のサブクラスの場合、監査ログには次の情報が含まれます。

| 分野               | 説明                                                                  |
| ---------------- | ------------------------------------------------------------------- |
| `CURRENT_DB`     | 現在のデータベースの名前。                                                       |
| `SQL_TEXT`       | 実行されたSQL文。監査ログの編集が有効になっている場合は、編集されたSQL文が記録されます。                     |
| `EXECUTE_PARAMS` | `EXECUTE`ステートメントのパラメータ。イベントクラスに`EXECUTE`含まれ、編集が無効になっている場合にのみ記録されます。 |
| `AFFECTED_ROWS`  | SQL文の影響を受けた行数。イベントクラスに`QUERY_DML`含まれる場合にのみ記録されます。                   |

### 接続情報 {#connection-information}

イベント クラスが`CONNECTION`または`CONNECTION`のサブクラスの場合、監査ログには次の情報が含まれます。

| 分野                | 説明                                                   |
| ----------------- | ---------------------------------------------------- |
| `CURRENT_DB`      | 現在のデータベースの名前。イベントクラスにDISCONNECTが含まれる場合、この情報は記録されません。 |
| `CONNECTION_TYPE` | 接続の種類 (ソケット、UnixSocket、SSL/TLS など)。                  |
| `PID`             | 現在の接続のプロセス ID。                                       |
| `SERVER_VERSION`  | 接続されている TiDBサーバーの現在のバージョン。                           |
| `SSL_VERSION`     | 現在使用されている SSL のバージョン。                                |
| `HOST_IP`         | 接続されている TiDBサーバーの現在の IP アドレス。                        |
| `HOST_PORT`       | 接続されている TiDBサーバーの現在のポート。                             |
| `CLIENT_IP`       | クライアントの現在の IP アドレス。                                  |
| `CLIENT_PORT`     | クライアントの現在のポート。                                       |

> **注記：**
>
> トラフィックの可視性を向上させるため、AWS PrivateLink 経由の接続において、ロードバランサー (LB) IP ではなく、実際のクライアント IP アドレスが表示されるようになり`CLIENT_IP`た。現在、この機能はベータ版であり、AWS リージョン`Frankfurt (eu-central-1)`でのみ利用可能です。

### 監査操作情報 {#audit-operation-information}

イベント クラスが`AUDIT`または`AUDIT`のサブクラスの場合、監査ログには次の情報が含まれます。

| 分野                | 説明                            |
| ----------------- | ----------------------------- |
| `AUDIT_OP_TARGET` | TiDB Cloudデータベース監査に関連する設定の対象。 |
| `AUDIT_OP_ARGS`   | TiDB Cloudデータベース監査に関連する設定の引数。 |

## 監査ログの制限 {#audit-logging-limitations}

TiDB Cloud Essentialは監査ログの順序を保証しません。そのため、最新のイベントを見つけるには、すべてのログファイルを確認する必要がある場合があります。ログを時系列で並べ替えるには、監査ログの`TIME`フィールドを使用します。
