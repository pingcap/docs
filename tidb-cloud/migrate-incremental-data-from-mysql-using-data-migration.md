---
title: Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Data Migration を使用して、Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、またはローカル MySQL インスタンスでホストされている MySQL 互換データベースから増分データをTiDB Cloudに移行する方法を学習します。
---

# データ移行を使用して、MySQL 互換データベースから増分データのみをTiDB Cloudに移行する {#migrate-only-incremental-data-from-mysql-compatible-databases-to-tidb-cloud-using-data-migration}

このドキュメントでは、 TiDB Cloudのデータ移行機能を使用して、クラウドプロバイダー (Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、または Google Cloud SQL for MySQL) 上の MySQL 互換データベースまたはセルフホスト型ソースデータベースからTiDB Cloud Cloud に増分データを移行する方法について説明します。

既存のデータ、または既存のデータと増分データの両方を移行する方法については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

## 制限事項 {#limitations}

> **注記**：
>
> このセクションには、増分データ移行に関する制限事項のみが記載されています。一般的な制限事項も読むことをお勧めします[制限事項](/tidb-cloud/migrate-from-mysql-using-data-migration.md#limitations)参照してください。

-   ターゲット データベースにターゲット テーブルがまだ作成されていない場合、移行ジョブは次のようにエラーを報告し、失敗します。この場合、ターゲット テーブルを手動で作成してから、移行ジョブを再試行する必要があります。

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
-   移行ジョブがアップストリームのセカンダリ データベースに接続する場合、 `REPLICATE CREATE TABLE ... SELECT`イベントは移行できません。これは、ステートメントが同じ GTID が割り当てられている 2 つのトランザクション ( `CREATE TABLE`と`INSERT` ) に分割されるためです。その結果、 `INSERT`ステートメントはセカンダリ データベースによって無視されます。

## 前提条件 {#prerequisites}

> **注記**：
>
> このセクションには、増分データ移行に関する前提条件のみが記載されています。 [一般的な前提条件](/tidb-cloud/migrate-from-mysql-using-data-migration.md#prerequisites)も読むことをお勧めします。

GTID を使用して開始位置を指定する場合は、ソース データベースで GTID が有効になっていることを確認してください。操作はデータベースの種類によって異なります。

### Amazon RDS および Amazon Aurora MySQL の場合 {#for-amazon-rds-and-amazon-aurora-mysql}

Amazon RDS および Amazon Aurora MySQL の場合、新しい変更可能なパラメータグループ (つまり、デフォルトのパラメータグループではない) を作成し、パラメータグループ内の次のパラメータを変更して、インスタンスアプリケーションを再起動する必要があります。

-   `gtid_mode`
-   `enforce_gtid_consistency`

次の SQL ステートメントを実行すると、GTID モードが正常に有効化されたかどうかを確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`の場合、 GTID モードは正常に有効化されています。

詳細については[GTIDベースのレプリケーションのパラメータ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-replication-gtid.html#mysql-replication-gtid.parameters)参照してください。

### Google Cloud SQL for MySQLの場合 {#for-google-cloud-sql-for-mysql}

Google Cloud SQL for MySQL では、GTID モードがデフォルトで有効になっています。次の SQL ステートメントを実行すると、GTID モードが正常に有効になっているかどうかを確認できます。

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

結果が`ON`または`ON_PERMISSIVE`の場合、 GTID モードは正常に有効化されています。

### セルフホスト型MySQLインスタンスの場合 {#for-a-self-hosted-mysql-instance}

> **注記**：
>
> 正確な手順とコマンドは、MySQL のバージョンと構成によって異なる場合があります。このアクションを実行する前に、GTID を有効にした場合の影響を理解し、非本番環境で適切にテストおよび検証したことを確認してください。

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

3.  設定の変更を有効にするために、MySQLサーバーを再起動します。

4.  次の SQL ステートメントを実行して、GTID モードが正常に有効化されているかどうかを確認します。

    ```sql
    SHOW VARIABLES LIKE 'gtid_mode';
    ```

    結果が`ON`または`ON_PERMISSIVE`の場合、 GTID モードは正常に有効化されています。

## ステップ1:<strong>データ移行</strong>ページに移動します {#step-1-go-to-the-strong-data-migration-strong-page}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ移行]**をクリックします。

3.  「**データ移行」**ページで、右上隅の**「移行ジョブの作成」**をクリックします。 **「移行ジョブの作成」**ページが表示されます。

## ステップ2: ソースとターゲットの接続を構成する {#step-2-configure-the-source-and-target-connection}

**「移行ジョブの作成」**ページで、ソース接続とターゲット接続を構成します。

1.  ジョブ名を入力します。ジョブ名は文字で始まり、60 文字未満である必要があります。文字 (AZ、az)、数字 (0-9)、アンダースコア (_)、ハイフン (-) が使用できます。

2.  ソース接続プロファイルを入力します。

    -   **データ ソース**: データ ソースの種類。
    -   **リージョン**: データ ソースのリージョン。クラウド データベースにのみ必要です。
    -   **接続方法**: データ ソースの接続方法。現在、接続方法に応じて、パブリック IP、VPC ピアリング、またはプライベート リンクを選択できます。
    -   **ホスト名または IP アドレス**(パブリック IP および VPC ピアリングの場合): データ ソースのホスト名または IP アドレス。
    -   **サービス名**(プライベート リンクの場合): エンドポイント サービス名。
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
    -   AWS Private Link を使用する場合は、エンドポイント要求を受け入れるように求められます。 [AWS VPC コンソール](https://us-west-2.console.aws.amazon.com/vpc/home)に移動し、 **[エンドポイント サービス] を**クリックしてエンドポイント要求を受け入れます。

## ステップ3: 移行ジョブの種類を選択する {#step-3-choose-migration-job-type}

ソース データベースの増分データのみをTiDB Cloudに移行するには、 **[増分データ移行]**を選択し、 **[既存データ移行]**は選択しないでください。この方法では、移行ジョブはソース データベースの進行中の変更のみをTiDB Cloudに移行します。

**[開始位置]**領域では、増分データ移行の開始位置として次のいずれかのタイプを指定できます。

-   増分移行ジョブが開始される時間
-   GTID
-   Binlogファイル名と位置

移行ジョブが開始されると、開始位置を変更することはできません。

### 増分移行ジョブが開始される時間 {#the-time-when-the-incremental-migration-job-starts}

このオプションを選択すると、移行ジョブは移行ジョブの開始後にソース データベースで生成された増分データのみを移行します。

### GTIDを指定する {#specify-gtid}

ソース データベースの GTID (例: `3E11FA47-71CA-11E1-9E33-C80AA9429562:1-23` ) を指定するには、このオプションを選択します。移行ジョブは、指定された GTID セットを除くトランザクションを複製し、ソース データベースの進行中の変更をTiDB Cloudに移行します。

次のコマンドを実行して、ソース データベースの GTID を確認できます。

```sql
SHOW MASTER STATUS;
```

GTID を有効にする方法については、 [前提条件](#prerequisites)参照してください。

### binlogファイル名と位置を指定する {#specify-binlog-file-name-and-position}

このオプションを選択して、ソース データベースのbinlogファイル名 (例: `binlog.000001` ) とbinlog位置 (例: `1307` ) を指定します。移行ジョブは、指定されたbinlogファイル名と位置から開始され、ソース データベースの進行中の変更がTiDB Cloudに移行されます。

次のコマンドを実行して、ソース データベースのbinlogファイル名と位置を確認できます。

```sql
SHOW MASTER STATUS;
```

ターゲット データベースにデータがある場合は、binlogの位置が正しいことを確認してください。そうでない場合、既存のデータと増分データの間に競合が発生する可能性があります。競合が発生した場合、移行ジョブは失敗します。競合したレコードをソース データベースのデータに置き換える場合は、移行ジョブを再開できます。

## ステップ4: 移行するオブジェクトを選択する {#step-4-choose-the-objects-to-be-migrated}

1.  **[移行するオブジェクトの選択]**ページで、移行するオブジェクトを選択します。 **[すべて**] をクリックしてすべてのオブジェクトを選択するか、 **[カスタマイズ]**をクリックしてオブジェクト名の横にあるチェックボックスをクリックしてオブジェクトを選択します。

2.  **「次へ」**をクリックします。

## ステップ5: 事前チェック {#step-5-precheck}

「**事前チェック」**ページでは、事前チェックの結果を確認できます。事前チェックが失敗した場合は、 **「失敗」**または**「警告」の**詳細に従って操作し、「再度**チェック」をクリックして再チェックする**必要があります。

一部のチェック項目にのみ警告がある場合は、リスクを評価して警告を無視するかどうかを検討できます。すべての警告を無視すると、移行ジョブは自動的に次のステップに進みます。

エラーと解決策の詳細については、 [事前チェックのエラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)参照してください。

事前チェック項目の詳細については、 [移行タスクの事前チェック](https://docs.pingcap.com/tidb/stable/dm-precheck)参照してください。

すべてのチェック項目が**合格**と表示されたら、 **「次へ」**をクリックします。

## ステップ6: 仕様を選択して移行を開始する {#step-6-choose-a-spec-and-start-migration}

**「仕様の選択と移行の開始」**ページで、パフォーマンス要件に応じて適切な移行仕様を選択します。仕様の詳細については、 [データ移行の仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)参照してください。

仕様を選択したら、 **「ジョブの作成」と「開始」**をクリックして移行を開始します。

## ステップ7: 移行の進行状況をビュー {#step-7-view-the-migration-progress}

移行ジョブが作成されると、**移行ジョブの詳細**ページで移行の進行状況を確認できます。移行の進行状況は、**ステージとステータス**領域に表示されます。

移行ジョブは実行中に一時停止または削除できます。

移行ジョブが失敗した場合は、問題を解決した後に再開できます。

移行ジョブはどのステータスでも削除できます。

移行中に問題が発生した場合は、 [移行エラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)参照してください。
