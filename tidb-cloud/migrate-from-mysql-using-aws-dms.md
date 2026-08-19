---
title: Migrate from MySQL-Compatible Databases to TiDB Cloud Using AWS DMS
summary: AWS Database Migration Service (AWS DMS) を使用して、MySQL互換データベースからTiDB Cloudへデータを移行する方法を学びましょう。
---

# AWS DMSを使用してMySQL互換データベースからTiDB Cloudに移行する {#migrate-from-mysql-compatible-databases-to-tidb-cloud-using-aws-dms}

PostgreSQL、Oracle、SQL Serverなどの異種データベースをTiDB Cloudに移行する場合は、AWS Database Migration Service（AWS DMS）の使用をお勧めします。

AWS DMSは、リレーショナルデータベース、データウェアハウス、NoSQLデータベース、その他のデータストアの移行を容易にするクラウドサービスです。AWS DMSを使用して、データをTiDB Cloudに移行できます。

このドキュメントでは、Amazon RDSを例として、AWS DMSを使用してTiDB Cloudにデータを移行する方法を示します。この手順は、セルフホスト型のMySQLデータベースまたはAmazon AuroraからTiDB Cloudへのデータ移行にも適用できます。

この例では、データソースはAmazon RDS、データ宛先はTiDB Cloud内のTiDB Cloud Dedicatedクラスタです。アップストリームデータベースとダウンストリームデータベースはどちらも同じリージョンにあります。

## 前提条件 {#prerequisites}

移行を開始する前に、以下の内容を必ずお読みください。

-   ソースデータベースが Amazon RDS または Amazon Auroraの場合、 `binlog_format`パラメータを`ROW`に設定する必要があります。データベースがデフォルトのパラメータ グループを使用する場合、 `binlog_format`パラメータはデフォルトで`MIXED`となり、変更できません。この場合、 [新しいパラメータグループを作成する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params)必要があります (例: `newset` 。その`binlog_format`を`ROW`に設定します。次に、 [デフォルトパラメータグループを変更する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#USER_WorkingWithParamGroups.Modifying)`newset`に変更します。パラメータ グループを変更するとデータベースが再起動されることに注意してください。
-   ソース データベースが TiDB と互換性のある照合順序を使用していることを確認してください。TiDB の utf8mb4 文字セットのデフォルトの照合照合順序は`utf8mb4_bin`です。しかし、MySQL 8.0 では、デフォルトの照合照合順序は`utf8mb4_0900_ai_ci`です。アップストリームの MySQL がデフォルトの照合順序を使用している場合、TiDB は`utf8mb4_0900_ai_ci`と互換性がないため、AWS DMS は TiDB にターゲット テーブルを作成できず、データを移行できません。この問題を解決するには、移行前にソース データベースの照合順序`utf8mb4_bin`に変更する必要があります。TiDB でサポートされている文字セットと照合順序の完全なリストについては、 [文字セットと照合](https://docs.pingcap.com/tidb/stable/character-set-and-collation)を参照してください。
-   TiDB には、デフォルトで`INFORMATION_SCHEMA` 、 `PERFORMANCE_SCHEMA` 、 `mysql` 、 `sys` } 、および`test`システム データベースが含まれています。AWS DMS 移行タスクを作成する際は、デフォルトの`%`を使用して移行オブジェクトを選択するのではなく、これらのシステム データベースを除外する必要があります。そうしないと、AWS DMS はこれらのシステム データベースをソース データベースからターゲット TiDB に移行しようとし、タスクが失敗します。この問題を回避するには、特定のデータベース名とテーブル名を入力することをお勧めします。
-   AWS DMSのパブリックネットワークIPアドレスとプライベートネットワークIPアドレスを、ソースデータベースとターゲットデータベースの両方のIPアクセスリストに追加してください。そうしないと、状況によってはネットワーク接続が失敗する可能性があります。
-   [VPCピアリング](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-on-aws)または[プライベートエンドポイント接続](/tidb-cloud/set-up-private-endpoint-connections.md)を使用して、AWS DMS と TiDB クラスターを接続します。
-   データ書き込みパフォーマンスを向上させるため、AWS DMSとTiDBクラスターには同じリージョンを使用することをお勧めします。
-   AWS DMS `dms.t3.large` （2 vCPU、8 GiBメモリ）以上のインスタンスクラスを使用することをお勧めします。インスタンスクラスが小さい場合、メモリ不足（OOM）エラーが発生する可能性があります。
-   AWS DMS は、ターゲット データベースに`awsdms_control`データベースを自動的に作成します。

## 制限 {#limitation}

-   AWS DMS は`DROP TABLE`のレプリケーションをサポートしていません。
-   AWS DMS は、テーブルや主キーの作成など、基本的なスキーマ移行をサポートしています。ただし、AWS DMS はTiDB Cloudにセカンダリインデックス、外部キー、ユーザーアカウントを自動的に作成しません。必要に応じて、セカンダリインデックスを持つテーブルを含め、これらのオブジェクトを TiDB に手動で作成する必要があります。詳細については、 [AWS Database Migration Service の移行計画](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html#CHAP_SettingUp.MigrationPlanning)を参照してください。

## ステップ1. AWS DMSレプリケーションインスタンスを作成する {#step-1-create-an-aws-dms-replication-instance}

1.  AWS DMS コンソールの[レプリケーションインスタンス](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。 AWS DMS にはTiDB Cloudと同じリージョンを使用することをお勧めします。このドキュメントでは、アップストリームおよびダウンストリームのデータベースと DMS インスタンスはすべて**us-west-2**リージョンにあります。

2.  **Create replication instance**をクリックします。

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3.  インスタンス名、ARN、および説明を入力してください。

4.  インスタンス構成を入力してください。
    -   **Instance class**：適切なインスタンスクラスを選択してください。パフォーマンスを向上させるには、 `dms.t3.large`またはそれより高いインスタンスクラスを使用することをお勧めします。
    -   **Engine version**：デフォルト設定を使用します。
    -   **マルチAZ** ：ビジネスニーズに応じて、**シングルAZ**または**マルチAZ**を選択してください。

5.  ストレージは**Allocated storage (GiB)**フィールドで設定します。デフォルト設定を使用してください。

6.  接続性とセキュリティを設定します。
    -   **Network type - new**: **IPv4**を選択してください。
    -   **IPv4 用仮想プライベートクラウド (VPC)** ：必要な VPC を選択してください。ネットワーク構成を簡素化するため、アップストリームデータベースと同じ VPC を使用することをお勧めします。
    -   **Replication subnet group**：レプリケーションインスタンスに使用するサブネットグループを選択してください。
    -   **Public accessible**：デフォルト設定を使用します。

7.  必要に応じて、**Advanced settings**、**メンテナンス**、および**タグ**を設定します。 **Create replication instance**をクリックして、インスタンスの作成を完了します。

## ステップ2. ソースデータベースエンドポイントを作成する {#step-2-create-the-source-database-endpoint}

1.  [AWS DMSコンソール](https://console.aws.amazon.com/dms/v2/home)で、先ほど作成したレプリケーションインスタンスをクリックします。次のスクリーンショットに示すように、パブリックネットワークIPアドレスとプライベートネットワークIPアドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  Amazon RDS のセキュリティグループルールを設定します。この例では、AWS DMS インスタンスのパブリック IP アドレスとプライベート IP アドレスをセキュリティグループに追加します。

    ![Configure the security group rules](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3.  ソースデータベースのエンドポイントを作成するには、 **Create endpoint**をクリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4.  この例では、 **Select RDS DB instance**をクリックし、ソースとなるRDSインスタンスを選択します。ソースデータベースがセルフホスト型のMySQLの場合は、この手順をスキップして、次の手順で情報を入力できます。

    ![Select RDS DB instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5.  以下の情報を設定してください。

    -   **Endpoint identifier**：後続のタスク構成で識別しやすくするために、ソースエンドポイントにラベルを作成します。
    -   **記述的な Amazon リソース名 (ARN) - オプション**: デフォルトの DMS ARN に分かりやすい名前を作成します。
    -   **Source engine**: **MySQL**を選択してください。
    -   **Access to endpoint database**:**Provide access information manually**を選択します。
    -   **Server name**：データプロバイダーのデータサーバー名を入力してください。データベースコンソールからコピーできます。アップストリームがAmazon RDSまたはAmazon Auroraの場合は、名前が自動的に入力されます。ドメイン名のないセルフホスト型MySQLの場合は、IPアドレスを入力してください。
    -   ソースデータベースの**ポート番号**、**ユーザー名**、**パスワード**を入力してください。
    -   **セキュリティソケットレイヤー（SSL）モード**：必要に応じてSSLモードを有効にできます。

    ![Fill in the endpoint configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6.  **Endpoint settings**、 **KMS key**、**タグに**はデフォルト値を使用してください。**Test endpoint connection (optional)**セクションでは、ネットワーク構成を簡素化するために、ソースデータベースと同じVPCを選択することをお勧めします。対応するレプリケーションインスタンスを選択し、 **Run test**をクリックします。ステータスが**「成功」**である必要があります。

7.  **Create endpoint**をクリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)

## ステップ3. ターゲットデータベースエンドポイントを作成する {#step-3-create-the-target-database-endpoint}

1.  [AWS DMSコンソール](https://console.aws.amazon.com/dms/v2/home)で、先ほど作成したレプリケーションインスタンスをクリックします。次のスクリーンショットに示すように、パブリックネットワークIPアドレスとプライベートネットワークIPアドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  TiDB Cloudコンソールで、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のリソース名をクリックしてから、右上隅の**[接続]**をクリックすると、 TiDB Cloudデータベースの接続情報が表示されます。

3.  ダイアログの**「ステップ 1: トラフィック フィルタの作成」**で、 **「編集」**をクリックし、AWS DMS コンソールからコピーしたパブリック IP アドレスとプライベート IP アドレスを入力して、 **Update Filter**をクリックします。AWS DMS レプリケーション インスタンスのパブリック IP アドレスとプライベート IP アドレスを TiDB クラスタのトラフィック フィルタに同時に追加することをお勧めします。そうしないと、状況によっては AWS DMS が TiDB クラスタに接続できない場合があります。

4.  **Download CA cert**をクリックします。ダイアログの**[ステップ3：SQLクライアントで接続する**]で、接続文字列内の`-u` 、 `-h` 、および`-P`情報を後で使用するためにメモしておきます。

5.  ダイアログの**VPC Peering**タブをクリックし、 **「ステップ1：VPCの設定**」の下にある**「追加」**をクリックして、TiDBクラスターとAWS DMSのVPCピアリング接続を作成します。

6.  対応する情報を設定します。 [VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。

7.  TiDBクラスタのターゲットエンドポイントを設定します。

    -   **Endpoint type**：**Target endpoint**を選択してください。
    -   **Endpoint identifier**：エンドポイントの名前を入力してください。
    -   **記述的な Amazon リソース名 (ARN) - オプション**: デフォルトの DMS ARN に分かりやすい名前を作成します。
    -   **Target engine**: **MySQL**を選択してください。

    ![Configure the target endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8.  [AWS DMSコンソール](https://console.aws.amazon.com/dms/v2/home)で、 **Create endpoint**をクリックしてターゲットデータベースエンドポイントを作成し、次の情報を設定します。

    -   **Server name**: 記録した`-h`情報である TiDB クラスターのホスト名を入力してください。
    -   **ポート**：記録した`-P`情報と同じTiDBクラスタのポート番号を入力してください。TiDBクラスタのデフォルトポートは4000です。
    -   **User name**: TiDB クラスターのユーザー名を入力してください。これは、記録した`-u`情報です。
    -   **パスワード**：TiDBクラスタのパスワードを入力してください。
    -   **セキュリティソケットレイヤー（SSL）モード**： **Verify-ca**を選択します。
    -   **Add new CA certificate**をクリックして、前の手順でTiDB CloudコンソールからダウンロードしたCAファイルをインポートします。

    ![Fill in the target endpoint information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9.  CAファイルをインポートします。

    ![Upload CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. **Endpoint settings**、 **KMS key**、**タグに**はデフォルト値を使用します。**Test endpoint connection (optional)**セクションで、ソースデータベースと同じVPCを選択します。対応するレプリケーションインスタンスを選択し、 **Run test**をクリックします。ステータスが**「成功」**である必要があります。

11. **Create endpoint**をクリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## ステップ4. データベース移行タスクを作成する {#step-4-create-a-database-migration-task}

1.  AWS DMS コンソールで、 [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに移動します。お住まいの地域に切り替えてください。次に、ウィンドウの右上隅にある**Create task**をクリックします。

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2.  以下の情報を設定してください。

    -   **Task identifier**: タスクの名前を入力してください。覚えやすい名前を使用することをお勧めします。
    -   **記述的な Amazon リソース名 (ARN) - オプション**: デフォルトの DMS ARN に分かりやすい名前を作成します。
    -   **Replication instance**：先ほど作成したAWS DMSインスタンスを選択します。
    -   **Source database endpoint**：先ほど作成したソースデータベースエンドポイントを選択してください。
    -   **Target database endpoint**：先ほど作成したターゲットデータベースエンドポイントを選択してください。
    -   **Migration type**：必要に応じて移行タイプを選択してください。この例では、 **「既存データの移行と進行中の変更の複製」**を選択します。

    ![Task configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3.  以下の情報を設定してください。

    -   **Editing mode**：**ウィザード**を選択してください。
    -   **ソーストランザクションのカスタムCDC停止モード**：デフォルト設定を使用します。
    -   **Target table preparation mode**：必要に応じて**Do nothing**またはその他のオプションを選択してください。この例では、 **Do nothing**を選択します。
    -   **フルロード完了後にタスクを停止する**：デフォルト設定を使用する。
    -   **LOB列をレプリケーションに含める**：**Limited LOB mode**を選択します。
    -   **LOBの最大サイズ（KB）** ：デフォルト値の**32**を使用します。
    -   **Turn on validation**：必要に応じて選択してください。
    -   **Task logs**: 今後のトラブルシューティングのために、 **Turn on CloudWatch logs**を選択してください。関連する設定については、デフォルト設定を使用してください。

    ![Task settings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4.  **Table mappings**のセクションで、移行するデータベースを指定します。

    スキーマ名は、Amazon RDS インスタンス内のデータベース名です。**Source name**のデフォルト値は「%」で、これは Amazon RDS 内のすべてのデータベースが TiDB に移行されることを意味します。これにより、Amazon RDS 内の`mysql`や`sys`などのシステム データベースが TiDB クラスターに移行され、タスクが失敗します。そのため、特定のデータベース名を入力するか、すべてのシステム データベースを除外することをお勧めします。たとえば、次のスクリーンショットの設定に従って、 `franktest`という名前のデータベースと、そのデータベース内のすべてのテーブルのみが移行されます。

    ![Table mappings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5.  右下隅の**Create task**をクリックしてください。

6.  [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに戻ります。お住まいの地域に切り替えてください。タスクのステータスと進捗状況を確認できます。

    ![Tasks status](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

移行中に問題や障害が発生した場合は、 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home)のログ情報を確認して問題のトラブルシューティングを行ってください。

![Troubleshooting](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 関連項目 {#see-also}

-   AWS DMS をTiDB Cloudに接続する方法の詳細については、 [AWS DMSをTiDB Cloudに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)を参照してください。

-   Aurora MySQL や Amazon Relational Database Service (RDS) などの MySQL 互換データベースからTiDB Cloudに移行する場合は、 [TiDB Cloudでのデータ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を使用することをお勧めします。

-   AWS DMS を使用して Amazon RDS for Oracle からTiDB Cloudに移行する場合は、 [AWS DMSを使用してAmazon RDS for OracleからTiDB Cloudに移行する](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)を参照してください。
