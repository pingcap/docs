---
title: Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: データ移行を使用して、Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、Azure Database for MySQL、Alibaba Cloud RDS、またはローカルのMySQLインスタンスでホストされているMySQL互換データベースからTiDB Cloudへ増分データを移行する方法を学びましょう。
---

# データ移行を使用して、MySQL互換データベースからTiDB Cloudへ増分データのみを移行する {#migrate-only-incremental-data-from-mysql-compatible-databases-to-tidb-cloud-using-data-migration}

このドキュメントでは、TiDB Cloud コンソールのデータ移行機能を使用して、クラウド プロバイダー (Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、Azure Database for MySQL、または Alibaba Cloud RDS) またはセルフホストのソース データベース上の MySQL 互換データベースから、増分データをTiDB Cloud <CustomContent plan="dedicated">TiDB Cloud Dedicated</CustomContent> <CustomContent plan="essential">TiDB Cloud Essential</CustomContent>に移行する方法について説明します。

<CustomContent plan="essential">

> **注記：**
>
> 現在、 TiDB Cloud Essentialのデータ移行機能はベータ版です。

</CustomContent>

既存のデータ、または既存のデータと増分データの両方を移行する方法については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

## 制限事項 {#limitations}

> **注記**：
>
> このセクションでは、増分データ移行に関する制限事項のみを記載しています。一般的な制限事項も併せてお読みになることをお勧めします。 [制限事項](/tidb-cloud/migrate-from-mysql-using-data-migration.md#limitations)をご覧ください。

-   対象データベースにターゲットテーブルがまだ作成されていない場合、移行ジョブは以下のようなエラーを報告して失敗します。この場合、ターゲットテーブルを手動で作成してから、移行ジョブを再試行する必要があります。

    ```sql
    startLocation: [position: (mysql_bin.000016, 5122), gtid-set:
    00000000-0000-0000-0000-00000000000000000], endLocation:
    [position: (mysql_bin.000016, 5162), gtid-set: 0000000-0000-0000
    0000-0000000000000:0]: cannot fetch downstream table schema of
    zm`.'table1' to initialize upstream schema 'zm'.'table1' in schema
    tracker Raw Cause: Error 1146: Table 'zm.table1' doesn't exist
    ```

-   アップストリームで一部の行が削除または更新され、ダウンストリームに対応する行がない場合、移行ジョブは、アップストリームから`DELETE`および`UPDATE` DML 操作を複製する際に、削除または更新可能な行がないことを検知します。

増分データの移行開始位置としてGTIDを指定する場合、以下の制限事項に注意してください。

-   ソースデータベースでGTIDモードが有効になっていることを確認してください。
-   ソースデータベースがMySQLの場合、MySQLのバージョンは5.6以降である必要があり、storageエンジンはInnoDBである必要があります。
-   移行ジョブがアップストリームのセカンダリデータベースに接続する場合、 `REPLICATE CREATE TABLE ... SELECT`イベントは移行できません。これは、ステートメントが同じ GTID が割り当てられた 2 つのトランザクション ( `CREATE TABLE`と`INSERT` ) に分割されるためです。その結果、 `INSERT`ステートメントはセカンダリデータベースによって無視されます。

## 前提条件 {#prerequisites}

> **注記**：
>
> このセクションには、増分データ移行に関する前提条件のみが含まれています。 [一般的な前提条件](/tidb-cloud/migrate-from-mysql-using-data-migration.md#prerequisites)も併せて読むことをお勧めします。

開始位置を指定するためにGTIDを使用する場合は、ソースデータベースでGTIDが有効になっていることを確認してください。操作方法はデータベースの種類によって異なります。

### Amazon RDS および Amazon Aurora MySQL の場合 {#for-amazon-rds-and-amazon-aurora-mysql}

Amazon RDS および Amazon Aurora MySQL の場合、新しい変更可能なパラメータ グループ (デフォルトのパラメータ グループではない) を作成し、そのパラメータ グループ内の以下のパラメータを変更してから、インスタンスを再起動して変更を適用する必要があります。

-   `gtid_mode`
-   `enforce_gtid_consistency`

GTIDモードが正常に有効化されたかどうかは、以下のSQL文を実行することで確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`の場合、GTID モードは正常に有効化されています。

詳細については、 [GTIDベースの複製のためのパラメータ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-replication-gtid.html#mysql-replication-gtid.parameters)を参照してください。

### Google Cloud SQL for MySQL の場合 {#for-google-cloud-sql-for-mysql}

Google Cloud SQL for MySQL では、GTID モードがデフォルトで有効になっています。GTID モードが正常に有効になっているかどうかは、次の SQL ステートメントを実行することで確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`の場合、GTID モードは正常に有効化されています。

### Azure Database for MySQL の場合 {#for-azure-database-for-mysql}

Azure Database for MySQL（バージョン5.7以降）では、GTIDモードはデフォルトで有効になっており、GTIDモードを無効にすることはできません。

さらに、 `binlog_row_image`サーバーパラメーターが`FULL`に設定されていることを確認してください。これは、次の SQL ステートメントを実行することで確認できます。

```sql
SHOW VARIABLES LIKE 'binlog_row_image';
```

結果が`FULL`でない場合は、 [Azureポータル](https://portal.azure.com/)または[Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)を使用して、Azure Database for MySQL インスタンスのこのパラメーターを構成する必要があります。

### Alibaba Cloud RDS MySQL 用 {#for-alibaba-cloud-rds-mysql}

Alibaba Cloud RDS MySQLでは、GTIDモードはデフォルトで有効になっています。GTIDモードが正常に有効になっているかどうかは、次のSQL文を実行することで確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`の場合、GTID モードは正常に有効化されています。

さらに、 `binlog_row_image`サーバーパラメーターが`FULL`に設定されていることを確認してください。これは、次の SQL ステートメントを実行することで確認できます。

```sql
SHOW VARIABLES LIKE 'binlog_row_image';
```

結果が`FULL`でない場合は、 [RDSコンソール](https://rds.console.aliyun.com/)を使用して Alibaba Cloud RDS MySQL インスタンスのこのパラメータを設定する必要があります。 。

### 自己ホスト型のMySQLインスタンスの場合 {#for-a-self-hosted-mysql-instance}

> **注記**：
>
> 具体的な手順やコマンドは、MySQLのバージョンや構成によって異なる場合があります。GTIDを有効にすることによる影響を十分に理解し、本番環境以外の環境で適切にテストおよび検証してから、この操作を実行してください。

自己ホスト型のMySQLインスタンスでGTIDモードを有効にするには、以下の手順に従ってください。

1.  適切な権限を持つMySQLクライアントを使用してMySQLサーバーに接続します。

2.  GTIDモードを有効にするには、以下のSQL文を実行してください。

    ```sql
    -- Enable the GTID mode
    SET GLOBAL gtid_mode = ON;

    -- Enable `enforce_gtid_consistency`
    SET GLOBAL enforce_gtid_consistency = ON;

    -- Reload the GTID configuration
    RESET MASTER;
    ```

3.  設定変更を有効にするには、MySQLサーバーを再起動してください。

4.  次のSQL文を実行して、GTIDモードが正常に有効化されているかどうかを確認してください。

    ```sql
    SHOW VARIABLES LIKE 'gtid_mode';
    ```

    結果が`ON`または`ON_PERMISSIVE`の場合、GTID モードは正常に有効化されています。

## ステップ1：データ移行ページに移動します {#step-1-go-to-the-data-migration-page}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>の名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[データ移行]**をクリックします。

3.  **データ移行**ページで、右上隅にある**「移行ジョブの作成」**をクリックします。**移行ジョブの作成**ページが表示されます。

## ステップ2：ソース接続とターゲット接続を設定する {#step-2-configure-the-source-and-target-connection}

**「移行ジョブの作成」**ページで、ソースとターゲットの接続を設定します。

1.  職名を入力してください。職名は文字で始まり、60文字以内である必要があります。文字（AZ、az）、数字（0～9）、アンダースコア（_）、ハイフン（-）が使用可能です。

2.  ソース接続プロファイルを入力してください。

    -   **データソース**：データソースの種類。
    -   **リージョン**：データソースのリージョン。クラウドデータベースの場合のみ必要です。
    -   **接続方法**: データ ソースの接続方法。<CustomContent plan="dedicated">現在、接続方法に応じて、パブリックIP、VPCピアリング、またはプライベートリンクを選択できます。</CustomContent><CustomContent plan="essential">接続方法に応じて、パブリックIPまたはプライベートリンクを選択できます。</CustomContent>

    <CustomContent plan="dedicated">

    -   **ホスト名またはIPアドレス**（パブリックIPおよびVPCピアリングの場合）：データソースのホスト名またはIPアドレス。
    -   **サービス名**（プライベートリンクの場合）：エンドポイントのサービス名。

    </CustomContent>
    <CustomContent plan="essential">

    -   **ホスト名またはIPアドレス**（パブリックIPの場合）：データソースのホスト名またはIPアドレス。
    -   **プライベート リンク接続**(プライベート リンク用): プライベートリンク[プライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)セクションで作成したプライベート リンク接続。

    </CustomContent>

    -   **ポート**：データソースのポート番号。
    -   **ユーザー名**：データソースのユーザー名。
    -   **パスワード**：ユーザー名のパスワード。
    -   **SSL/TLS** ：SSL/TLSを有効にする場合は、以下のいずれかの証明書を含む、データソースの証明書をアップロードする必要があります。
        -   CA証明書のみ
        -   クライアント証明書とクライアントキー
        -   CA証明書、クライアント証明書、およびクライアントキー

3.  ターゲット接続プロファイルを入力してください。

    -   **ユーザー名**: ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>のユーザー名を入力します。
    -   **パスワード**： TiDB Cloudのユーザー名のパスワードを入力してください。

4.  入力した情報を検証するには、 **「接続を検証」をクリックし、「次へ」を**クリックしてください。

5.  表示されたメッセージに従って行動してください。

    <CustomContent plan="dedicated">

    -   パブリックIPまたはVPCピアリングを使用する場合は、データ移行サービスのIPアドレスを、ソースデータベースおよびファイアウォール（存在する場合）のIPアクセスリストに追加する必要があります。
    -   AWS Private Link を使用する場合、エンドポイント要求を承認するよう求められます。AWS [AWS VPCコンソール](https://us-west-2.console.aws.amazon.com/vpc/home)に移動し、**エンドポイント サービス**をクリックしてエンドポイント要求を承認してください。

    </CustomContent>
    <CustomContent plan="essential">

    パブリックIPを使用する場合は、データ移行サービスのIPアドレスを、ソースデータベースおよびファイアウォール（存在する場合）のIPアクセスリストに追加する必要があります。

    </CustomContent>

## ステップ3：移行ジョブの種類を選択する {#step-3-choose-migration-job-type}

ソースデータベースの増分データのみをTiDB Cloudに移行するには、 **「増分データ移行」**を選択し、 **「既存データ移行」**は選択しないでください。こうすることで、移行ジョブはソースデータベースの進行中の変更のみをTiDB Cloudに移行します。

**「開始位置」**領域では、増分データ移行の開始位置として、以下のいずれかのタイプを指定できます。

-   増分移行ジョブが開始される時間
-   GTID
-   Binlogファイル名と位置

移行ジョブが開始されると、開始位置を変更することはできません。

### 増分移行ジョブが開始される時間 {#the-time-when-the-incremental-migration-job-starts}

このオプションを選択すると、移行ジョブは、移行ジョブの開始後にソースデータベースで生成された増分データのみを移行します。

### GTIDを指定してください {#specify-gtid}

このオプションを選択すると、ソースデータベースの GTID を指定できます（例: `3E11FA47-71CA-11E1-9E33-C80AA9429562:1-23` 。移行ジョブは、指定された GTID セットを除いたトランザクションを複製し、ソースデータベースの進行中の変更をTiDB Cloudに移行します。

ソースデータベースのGTIDを確認するには、以下のコマンドを実行してください。

```sql
SHOW MASTER STATUS;
```

GTID を有効にする方法については、[前提条件](#prerequisites)を参照してください。

### binlogファイル名と位置を指定してください。 {#specify-binlog-file-name-and-position}

このオプションを選択すると、ソースデータベースのbinlogファイル名（例： `binlog.000001` ）とbinlogの位置（例： `1307` ）を指定できます。移行ジョブは、指定されたbinlogファイル名と位置から開始され、ソースデータベースの進行中の変更をTiDB Cloudに移行します。

以下のコマンドを実行すると、ソースデータベースのbinlogファイル名と位置を確認できます。

```sql
SHOW MASTER STATUS;
```

対象データベースにデータが存在する場合は、binlogの位置が正しいことを確認してください。そうでない場合、既存データと増分データの間で競合が発生する可能性があります。競合が発生すると、移行ジョブは失敗します。競合したレコードをソースデータベースのデータで置き換える場合は、移行ジョブを再開できます。

## ステップ4：移行するオブジェクトを選択する {#step-4-choose-the-objects-to-be-migrated}

1.  **「移行するオブジェクトの選択」**ページで、移行するオブジェクトを選択します。 **「すべて**」をクリックするとすべてのオブジェクトを選択できます。 **「カスタマイズ」**をクリックしてから、オブジェクト名の横にあるチェックボックスをクリックしてオブジェクトを選択することもできます。

2.  **「次へ」**をクリックしてください。

## ステップ5：事前チェック {#step-5-precheck}

**事前チェック**ページでは、事前チェックの結果を確認できます。事前チェックが失敗した場合は、 **「失敗」**または**「警告」の**詳細に従って操作を行い、再度**「チェック」をクリックして再**チェックしてください。

チェック項目の一部にのみ警告が表示されている場合は、リスクを評価し、警告を無視するかどうかを検討できます。すべての警告を無視した場合、移行ジョブは自動的に次のステップに進みます。

エラーと解決策の詳細については、 [事前チェックのエラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)を参照してください。

事前チェック項目の詳細については、 [移行タスクの事前チェック](https://docs.pingcap.com/tidb/stable/dm-precheck)参照してください。

すべてのチェック項目が**「合格」**と表示されたら、 **「次へ」**をクリックしてください。

<CustomContent plan="essential">

## ステップ6：移行の進捗状況をビュー {#step-6-view-the-migration-progress}

移行ジョブが作成されると、**移行ジョブの詳細**ページで移行の進行状況を確認できます。移行の進行状況は、 **「ステージ」と「ステータス」の**領域に表示されます。

移行ジョブは、実行中でも一時停止または削除できます。

移行ジョブが失敗した場合は、問題を解決した後で再開できます。

移行ジョブはどのステータスでも削除できます。

移行中に問題が発生した場合は、 [移行エラーとその解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)参照してください。

</CustomContent>

<CustomContent plan="dedicated">

## ステップ6：仕様を選択して移行を開始する {#step-6-choose-a-spec-and-start-migration}

**「仕様を選択して移行を開始」**ページで、パフォーマンス要件に応じて適切な移行仕様を選択します。仕様の詳細については、 [データ移行の仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)参照してください。

仕様を選択したら、 **「ジョブの作成」をクリックし、「開始」を**クリックして移行を開始します。

## ステップ7：移行の進捗状況をビュー {#step-7-view-the-migration-progress}

移行ジョブが作成されると、**移行ジョブの詳細**ページで移行の進行状況を確認できます。移行の進行状況は、 **「ステージ」と「ステータス」の**領域に表示されます。

移行ジョブは、実行中でも一時停止または削除できます。

移行ジョブが失敗した場合は、問題を解決した後で再開できます。

移行ジョブはどのステータスでも削除できます。

移行中に問題が発生した場合は、 [移行エラーとその解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)参照してください。

</CustomContent>
