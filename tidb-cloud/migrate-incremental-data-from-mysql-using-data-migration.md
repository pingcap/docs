---
title: Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Data Migration を使用して、Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、Azure Database for MySQL、またはローカル MySQL インスタンスでホストされている MySQL 互換データベースから増分データをTiDB Cloudに移行する方法について説明します。
---

# データ移行を使用して、MySQL 互換データベースからTiDB Cloudに増分データのみを移行する {#migrate-only-incremental-data-from-mysql-compatible-databases-to-tidb-cloud-using-data-migration}

このドキュメントでは、TiDB Cloud コンソールのデータ移行機能を使用して、クラウドプロバイダー (Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、または Azure Database for MySQL) 上の MySQL 互換データベースまたはセルフホスト型ソースデータベースからTiDB Cloud TiDB Cloudに増分データを移行する方法について説明します。

既存のデータ、または既存のデータと増分データの両方を移行する方法については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

## 制限事項 {#limitations}

> **注記**：
>
> このセクションでは、増分データ移行に関する制限事項のみを説明します。一般的な制限事項も併せてご確認いただくことをお勧めします。1 [制限事項](/tidb-cloud/migrate-from-mysql-using-data-migration.md#limitations)参照してください。

-   ターゲットデータベースにターゲットテーブルがまだ作成されていない場合、移行ジョブは次のようなエラーを報告し、失敗します。この場合、ターゲットテーブルを手動で作成してから、移行ジョブを再試行する必要があります。

    ```sql
    startLocation: [position: (mysql_bin.000016, 5122), gtid-set:
    00000000-0000-0000-0000-00000000000000000], endLocation:
    [position: (mysql_bin.000016, 5162), gtid-set: 0000000-0000-0000
    0000-0000000000000:0]: cannot fetch downstream table schema of
    zm`.'table1' to initialize upstream schema 'zm'.'table1' in sschema
    tracker Raw Cause: Error 1146: Table 'zm.table1' doesn't exist
    ```

-   アップストリームで一部の行が削除または更新され、ダウンストリームに対応する行がない場合、移行ジョブは、アップストリームから`DELETE`と`UPDATE` DML 操作を複製するときに、削除または更新できる行がないことを検出します。

増分データを移行するための開始位置として GTID を指定する場合は、次の制限に注意してください。

-   ソース データベースで GTID モードが有効になっていることを確認します。
-   ソース データベースが MySQL の場合、MySQL バージョンは 5.6 以降であり、storageエンジンは InnoDB である必要があります。
-   移行ジョブが上流のセカンダリデータベースに接続する場合、 `REPLICATE CREATE TABLE ... SELECT`のイベントは移行できません。これは、ステートメントが同じGTIDを持つ2つのトランザクション（ `CREATE TABLE`と`INSERT` ）に分割されるためです。その結果、 `INSERT`ステートメントはセカンダリデータベースによって無視されます。

## 前提条件 {#prerequisites}

> **注記**：
>
> このセクションでは、増分データ移行に関する前提条件のみを説明します。1 [一般的な前提条件](/tidb-cloud/migrate-from-mysql-using-data-migration.md#prerequisites)併せてお読みいただくことをお勧めします。

GTID を使用して開始位置を指定する場合は、ソースデータベースで GTID が有効になっていることを確認してください。操作はデータベースの種類によって異なります。

### Amazon RDS および Amazon Aurora MySQL の場合 {#for-amazon-rds-and-amazon-aurora-mysql}

Amazon RDS および Amazon Aurora MySQL の場合、新しい変更可能なパラメータグループ (つまり、デフォルトのパラメータグループではないもの) を作成し、パラメータグループ内の次のパラメータを変更して、インスタンスアプリケーションを再起動する必要があります。

-   `gtid_mode`
-   `enforce_gtid_consistency`

次の SQL ステートメントを実行すると、GTID モードが正常に有効化されたかどうかを確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`場合、 GTID モードは正常に有効化されています。

詳細については[GTIDベースのレプリケーションのパラメータ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-replication-gtid.html#mysql-replication-gtid.parameters)参照してください。

### Google Cloud SQL for MySQLの場合 {#for-google-cloud-sql-for-mysql}

Google Cloud SQL for MySQL では、GTID モードがデフォルトで有効になっています。次の SQL 文を実行することで、GTID モードが正常に有効になっているかどうかを確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`場合、 GTID モードは正常に有効化されています。

### Azure Database for MySQLの場合 {#for-azure-database-for-mysql}

Azure Database for MySQL（バージョン 5.7 以降）では、GTID モードがデフォルトで有効になっています。次の SQL ステートメントを実行することで、GTID モードが正常に有効になっているかどうかを確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`場合、 GTID モードは正常に有効化されています。

さらに、 `binlog_row_image`サーバーパラメータが`FULL`に設定されていることを確認してください。これは、次のSQL文を実行することで確認できます。

```sql
SHOW VARIABLES LIKE 'binlog_row_image';
```

結果が`FULL`以外の場合は、 [Azureポータル](https://portal.azure.com/)または[Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)使用して、Azure Database for MySQL インスタンスに対してこのパラメーターを構成する必要があります。

### セルフホスト型MySQLインスタンスの場合 {#for-a-self-hosted-mysql-instance}

> **注記**：
>
> 具体的な手順とコマンドは、MySQLのバージョンと設定によって異なる場合があります。GTIDを有効化した場合の影響を理解し、本番環境以外で適切なテストと検証を行った上で、この操作を実行してください。

セルフホスト MySQL インスタンスで GTID モードを有効にするには、次の手順に従います。

1.  適切な権限を持つ MySQL クライアントを使用して MySQLサーバーに接続します。

2.  GTID モードを有効にするには、次の SQL ステートメントを実行します。

    ```sql
    -- Enable the GTID mode
    SET GLOBAL gtid_mode = ON;

    -- Enable `enforce_gtid_consistency`
    SET GLOBAL enforce_gtid_consistency = ON;

    -- Reload the GTID configuration
    RESET MASTER;
    ```

3.  設定の変更を有効にするには、MySQLサーバーを再起動します。

4.  次の SQL ステートメントを実行して、GTID モードが正常に有効化されているかどうかを確認します。

    ```sql
    SHOW VARIABLES LIKE 'gtid_mode';
    ```

    結果が`ON`または`ON_PERMISSIVE`場合、 GTID モードは正常に有効化されています。

## ステップ1:<strong>データ移行</strong>ページに移動します {#step-1-go-to-the-strong-data-migration-strong-page}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ移行]**をクリックします。

3.  **「データ移行」**ページで、右上隅の**「移行ジョブの作成」を**クリックします。 **「移行ジョブの作成」**ページが表示されます。

## ステップ2: ソースとターゲットの接続を構成する {#step-2-configure-the-source-and-target-connection}

**「移行ジョブの作成」**ページで、ソース接続とターゲット接続を構成します。

1.  ジョブ名を入力してください。ジョブ名は文字で始まり、60文字未満である必要があります。文字（AZ、az）、数字（0-9）、アンダースコア（_）、ハイフン（-）が使用できます。

2.  ソース接続プロファイルを入力します。

    -   **データ ソース**: データ ソースの種類。
    -   **リージョン**: データ ソースのリージョン。クラウド データベースにのみ必要です。
    -   **接続方法**：データソースへの接続方法。現在、接続方法に応じて、パブリックIP、VPCピアリング、またはプライベートリンクを選択できます。
    -   **ホスト名または IP アドレス**(パブリック IP および VPC ピアリングの場合): データ ソースのホスト名または IP アドレス。
    -   **サービス名**(Private Link の場合): エンドポイント サービス名。
    -   **ポート**: データ ソースのポート。
    -   **ユーザー名**: データ ソースのユーザー名。
    -   **パスワード**: ユーザー名のパスワード。
    -   **SSL/TLS** : SSL/TLS を有効にする場合は、次のいずれかを含むデータ ソースの証明書をアップロードする必要があります。
        -   CA証明書のみ
        -   クライアント証明書とクライアントキー
        -   CA証明書、クライアント証明書、クライアントキー

3.  ターゲット接続プロファイルを入力します。

    -   **ユーザー名**: TiDB Cloudのターゲット クラスターのユーザー名を入力します。
    -   **パスワード**: TiDB Cloudユーザー名のパスワードを入力します。

4.  入力した情報を検証するには、 **「接続の検証」と「次へ」**をクリックします。

5.  表示されるメッセージに従ってアクションを実行します。

    -   パブリック IP または VPC ピアリングを使用する場合は、データ移行サービスの IP アドレスをソース データベースとファイアウォール (存在する場合) の IP アクセス リストに追加する必要があります。
    -   AWS Private Link を使用する場合は、エンドポイントリクエストを承認するように求められます。1 [AWS VPCコンソール](https://us-west-2.console.aws.amazon.com/vpc/home)移動し、 **「エンドポイントサービス」**をクリックしてエンドポイントリクエストを承認してください。

## ステップ3: 移行ジョブの種類を選択する {#step-3-choose-migration-job-type}

ソースデータベースの増分データのみをTiDB Cloudに移行するには、 **「増分データ移行」**を選択し、 **「既存データ移行」**は選択しないでください。これにより、移行ジョブはソースデータベースの進行中の変更のみをTiDB Cloudに移行します。

**[開始位置]**領域では、増分データ移行の開始位置として次のいずれかのタイプを指定できます。

-   増分移行ジョブが開始される時刻
-   GTID
-   Binlogファイル名と位置

移行ジョブが開始されると、開始位置を変更することはできません。

### 増分移行ジョブが開始される時刻 {#the-time-when-the-incremental-migration-job-starts}

このオプションを選択すると、移行ジョブは移行ジョブの開始後にソース データベースで生成された増分データのみを移行します。

### GTIDを指定する {#specify-gtid}

ソースデータベースのGTID（例： `3E11FA47-71CA-11E1-9E33-C80AA9429562:1-23` ）を指定するには、このオプションを選択します。移行ジョブは、指定されたGTIDセットを除くトランザクションを複製し、ソースデータベースの進行中の変更をTiDB Cloudに移行します。

次のコマンドを実行して、ソース データベースの GTID を確認できます。

```sql
SHOW MASTER STATUS;
```

GTID を有効にする方法については、 [前提条件](#prerequisites)参照してください。

### binlogファイルの名前と位置を指定する {#specify-binlog-file-name-and-position}

このオプションを選択すると、ソースデータベースのbinlogファイル名（例： `binlog.000001` ）とbinlog位置（例： `1307` ）を指定できます。移行ジョブは指定されたbinlogファイル名と位置から開始され、ソースデータベースの進行中の変更をTiDB Cloudに移行します。

次のコマンドを実行して、ソース データベースのbinlogファイル名と位置を確認できます。

```sql
SHOW MASTER STATUS;
```

ターゲットデータベースにデータが存在する場合は、binlogの位置が正しいことを確認してください。そうでない場合、既存データと増分データの間に競合が発生する可能性があります。競合が発生した場合、移行ジョブは失敗します。競合したレコードをソースデータベースのデータに置き換えたい場合は、移行ジョブを再開できます。

## ステップ4: 移行するオブジェクトを選択する {#step-4-choose-the-objects-to-be-migrated}

1.  **「移行するオブジェクトの選択」**ページで、移行するオブジェクトを選択します。 **「すべて」**をクリックしてすべてのオブジェクトを選択するか、 **「カスタマイズ」**をクリックしてオブジェクト名の横にあるチェックボックスをクリックしてオブジェクトを選択します。

2.  **「次へ」**をクリックします。

## ステップ5: 事前チェック {#step-5-precheck}

**「事前チェック」**ページでは、事前チェックの結果を確認できます。事前チェックに失敗した場合は、 **「失敗」**または**「警告」の**詳細に従って操作し、「再チェック」をクリックして**再**チェックしてください。

一部のチェック項目にのみ警告がある場合は、リスクを評価し、警告を無視するかどうかを検討できます。すべての警告を無視した場合、移行ジョブは自動的に次のステップに進みます。

エラーと解決策の詳細については、 [エラーと解決策を事前に確認する](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)参照してください。

事前チェック項目の詳細については、 [移行タスクの事前チェック](https://docs.pingcap.com/tidb/stable/dm-precheck)参照してください。

すべてのチェック項目が**合格と**表示されたら、 **「次へ」**をクリックします。

## ステップ6: 仕様を選択して移行を開始する {#step-6-choose-a-spec-and-start-migration}

**「仕様の選択と移行の開始」**ページで、パフォーマンス要件に応じて適切な移行仕様を選択します。仕様の詳細については、 [データ移行の仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)参照してください。

仕様を選択したら、 **「ジョブの作成」と「開始」**をクリックして移行を開始します。

## ステップ7: 移行の進行状況をビュー {#step-7-view-the-migration-progress}

移行ジョブが作成されると、 **「移行ジョブの詳細」**ページで移行の進行状況を確認できます。移行の進行状況は**「ステージとステータス」**領域に表示されます。

移行ジョブは実行中に一時停止または削除できます。

移行ジョブが失敗した場合は、問題を解決してから再開できます。

移行ジョブはどのステータスでも削除できます。

移行中に問題が発生した場合は、 [移行エラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)参照してください。
