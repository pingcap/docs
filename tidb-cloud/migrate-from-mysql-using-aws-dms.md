---
title: Migrate from MySQL-Compatible Databases to TiDB Cloud Using AWS DMS
summary: AWS Database Migration Service (AWS DMS) を使用して、MySQL 互換データベースからTiDB Cloudにデータを移行する方法を学びます。
---

# AWS DMS を使用して MySQL 互換データベースからTiDB Cloudに移行する {#migrate-from-mysql-compatible-databases-to-tidb-cloud-using-aws-dms}

PostgreSQL、Oracle、SQL Server などの異種データベースをTiDB Cloudに移行する場合は、AWS Database Migration Service (AWS DMS) を使用することをお勧めします。

AWS DMS は、リレーショナルデータベース、データウェアハウス、NoSQL データベース、その他の種類のデータストアの移行を容易にするクラウドサービスです。AWS DMS を使用して、データをTiDB Cloudに移行できます。

このドキュメントでは、Amazon RDS を例に、AWS DMS を使用してデータをTiDB Cloudに移行する方法を説明します。この手順は、セルフホスト型 MySQL データベースまたは Amazon AuroraからTiDB Cloudにデータを移行する場合にも適用されます。

この例では、データソースは Amazon RDS で、データの送信先はTiDB Cloudの TiDB Dedicated クラスターです。アップストリーム データベースとダウンストリーム データベースは両方とも同じリージョンにあります。

## 前提条件 {#prerequisites}

移行を開始する前に、必ず次の内容をお読みください。

-   ソースデータベースが Amazon RDS または Amazon Auroraの場合、 `binlog_format`パラメータを`ROW`に設定する必要があります。データベースがデフォルトのパラメータグループを使用する場合、 `binlog_format`パラメータはデフォルトで`MIXED`なり、変更できません。この場合、 [新しいパラメータグループを作成する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params) 、たとえば`newset`設定し、その`binlog_format`を`ROW`に設定する必要があります。次に、 [デフォルトのパラメータグループを変更する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#USER_WorkingWithParamGroups.Modifying)を`newset`に設定します。パラメータグループを変更すると、データベースが再起動されることに注意してください。
-   ソースデータベースが TiDB と互換性のある照合順序を使用していることを確認してください。TiDB の utf8mb4 文字セットのデフォルトの照合順序は`utf8mb4_bin`です。ただし、MySQL 8.0 では、デフォルトの照合順序は`utf8mb4_0900_ai_ci`です。アップストリーム MySQL がデフォルトの照合順序を使用している場合、TiDB は`utf8mb4_0900_ai_ci`と互換性がないため、AWS DMS は TiDB にターゲットテーブルを作成できず、データを移行できません。この問題を解決するには、移行前にソースデータベースの照合順序を`utf8mb4_bin`に変更する必要があります。TiDB でサポートされている文字セットと照合順序の完全なリストについては、 [文字セットと照合順序](https://docs.pingcap.com/tidb/stable/character-set-and-collation)を参照してください。
-   TiDB `PERFORMANCE_SCHEMA` `INFORMATION_SCHEMA` `mysql` `sys` `test`移行タスクを作成するときは、デフォルトの`%`を使用して移行オブジェクトを選択するのではなく、これらのシステムデータベースを除外する必要があります。そうしないと、AWS DMS はこれらのシステムデータベースをソースデータベースからターゲット TiDB に移行しようとし、タスクが失敗します。この問題を回避するには、特定のデータベース名とテーブル名を入力することをお勧めします。
-   AWS DMS のパブリックおよびプライベート ネットワーク IP アドレスを、ソース データベースとターゲット データベースの両方の IP アクセス リストに追加します。そうしないと、シナリオによってはネットワーク接続が失敗する可能性があります。
-   [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-on-aws)または[プライベートエンドポイント接続](/tidb-cloud/set-up-private-endpoint-connections.md)を使用して、AWS DMS と TiDB クラスターを接続します。
-   より優れたデータ書き込みパフォーマンスを得るには、AWS DMS と TiDB クラスターに同じリージョンを使用することをお勧めします。
-   AWS DMS `dms.t3.large` (2 vCPU および 8 GiBメモリ) 以上のインスタンスクラスを使用することをお勧めします。インスタンスクラスが小さいと、メモリ不足 (OOM) エラーが発生する可能性があります。
-   AWS DMS はターゲットデータベースに`awsdms_control`データベースを自動的に作成します。

## 制限 {#limitation}

-   AWS DMS は`DROP TABLE`レプリケーションをサポートしていません。
-   AWS DMS は、テーブルとプライマリキーの作成を含む基本的なスキーマ移行をサポートしています。ただし、AWS DMS はTiDB Cloudにセカンダリインデックス、外部キー、またはユーザーアカウントを自動的に作成しません。必要に応じて、セカンダリインデックスを含むテーブルを含むこれらのオブジェクトを TiDB に手動で作成する必要があります。詳細については、 [AWS Database Migration Service の移行計画](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html#CHAP_SettingUp.MigrationPlanning)参照してください。

## ステップ1. AWS DMSレプリケーションインスタンスを作成する {#step-1-create-an-aws-dms-replication-instance}

1.  AWS DMS コンソールの[レプリケーションインスタンス](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。AWS DMS にはTiDB Cloudと同じリージョンを使用することをお勧めします。このドキュメントでは、アップストリームおよびダウンストリームデータベースと DMS インスタンスはすべて**us-west-2**リージョンにあります。

2.  **レプリケーションインスタンスの作成を**クリックします。

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3.  インスタンス名、ARN、説明を入力します。

4.  インスタンス構成を入力します。
    -   **インスタンス クラス**: 適切なインスタンス クラスを選択します。パフォーマンスを向上させるには、 `dms.t3.large`以上のインスタンス クラスを使用することをお勧めします。
    -   **エンジン バージョン**: デフォルト構成を使用します。
    -   **マルチ AZ** : ビジネス ニーズに応じて、**シングル AZ**または**マルチ AZ**を選択します。

5.  **割り当てられたstorage(GiB)**フィールドでstorageを構成します。デフォルトの構成を使用します。

6.  接続とセキュリティを構成します。
    -   **ネットワークタイプ - 新規**: **IPv4**を選択します。
    -   **IPv4 用の仮想プライベート クラウド (VPC)** : 必要な VPC を選択します。ネットワーク構成を簡素化するために、アップストリーム データベースと同じ VPC を使用することをお勧めします。
    -   **レプリケーション サブネット グループ**: レプリケーション インスタンスのサブネット グループを選択します。
    -   **パブリックアクセス可能**: デフォルトの設定を使用します。

7.  必要に応じて、**詳細設定**、**メンテナンス**、**タグを**構成します。 **「レプリケーション インスタンスの作成」を**クリックして、インスタンスの作成を完了します。

## ステップ2. ソースデータベースエンドポイントを作成する {#step-2-create-the-source-database-endpoint}

1.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、先ほど作成したレプリケーション インスタンスをクリックします。次のスクリーンショットに示すように、パブリック ネットワークとプライベート ネットワークの IP アドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  Amazon RDS のセキュリティグループルールを設定します。この例では、AWS DMS インスタンスのパブリック IP アドレスとプライベート IP アドレスをセキュリティグループに追加します。

    ![Configure the security group rules](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3.  **[エンドポイントの作成] を**クリックして、ソース データベース エンドポイントを作成します。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4.  この例では、 **「RDS DB インスタンスの選択」**をクリックし、ソース RDS インスタンスを選択します。ソース データベースがセルフホスト型 MySQL の場合は、この手順をスキップして、次の手順で情報を入力できます。

    ![Select RDS DB instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5.  次の情報を設定します。

    -   **エンドポイント識別子**: 後続のタスク構成で識別できるように、ソース エンドポイントのラベルを作成します。
    -   **記述的な Amazon リソース名 (ARN) - オプション**: デフォルトの DMS ARN のわかりやすい名前を作成します。
    -   **ソースエンジン**: **MySQL**を選択します。
    -   **エンドポイント データベースへのアクセス**:**アクセス情報を手動で提供するを**選択します。
    -   **サーバー名**: データプロバイダーのデータサーバーの名前を入力します。データベースコンソールからコピーできます。アップストリームが Amazon RDS または Amazon Auroraの場合は、名前が自動的に入力されます。ドメイン名のないセルフホスト MySQL の場合は、IP アドレスを入力できます。
    -   ソース データベースの**ポート**、**ユーザー名**、および**パスワード**を入力します。
    -   **セキュリティ Socket Layer (SSL) モード**: 必要に応じて SSL モードを有効にすることができます。

    ![Fill in the endpoint configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6.  **エンドポイント設定**、 **KMS キー**、**タグに**はデフォルト値を使用します。**エンドポイント接続のテスト (オプション)**セクションでは、ネットワーク構成を簡素化するために、ソース データベースと同じ VPC を選択することをお勧めします。対応するレプリケーション インスタンスを選択し、**テストの実行を**クリックします。ステータスは**成功**である必要があります。

7.  **[エンドポイントの作成]を**クリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)

## ステップ3. ターゲットデータベースエンドポイントを作成する {#step-3-create-the-target-database-endpoint}

1.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、先ほど作成したレプリケーション インスタンスをクリックします。次のスクリーンショットに示すように、パブリック ネットワークとプライベート ネットワークの IP アドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  TiDB Cloudコンソールで、 [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、右上隅の**[接続] を**クリックし、 TiDB Cloudデータベース接続情報を取得します。

3.  ダイアログの**「ステップ 1: トラフィックフィルターの作成」**で、 **「編集」**をクリックし、AWS DMS コンソールからコピーしたパブリックおよびプライベートネットワークの IP アドレスを入力して、 **「フィルターの更新」**をクリックします。AWS DMS レプリケーションインスタンスのパブリック IP アドレスとプライベート IP アドレスを TiDB クラスターのトラフィックフィルターに同時に追加することをお勧めします。そうしないと、一部のシナリオで AWS DMS が TiDB クラスターに接続できない可能性があります。

4.  CA 証明書をダウンロードするには、「CA 証明書**のダウンロード」**をクリックします。ダイアログの**「手順 3: SQL クライアントを使用して接続する**」で、接続文字列の`-u` 、および`-P` `-h`を後で使用するためにメモします。

5.  ダイアログの**「VPC ピアリング**」タブをクリックし、 **「ステップ 1: VPC のセットアップ**」の下にある**「追加」**をクリックして、TiDB クラスターと AWS DMS の VPC ピアリング接続を作成します。

6.  対応する情報を設定します。1 [VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)参照してください。

7.  TiDB クラスターのターゲット エンドポイントを構成します。

    -   **エンドポイント タイプ**:**ターゲット エンドポイント**を選択します。
    -   **エンドポイント識別子**: エンドポイントの名前を入力します。
    -   **記述的な Amazon リソース名 (ARN) - オプション**: デフォルトの DMS ARN のわかりやすい名前を作成します。
    -   **ターゲットエンジン**: **MySQL**を選択します。

    ![Configure the target endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、 **[エンドポイントの作成]**をクリックしてターゲット データベース エンドポイントを作成し、次の情報を構成します。

    -   **サーバー名**: 記録した`-h`の情報である TiDB クラスターのホスト名を入力します。
    -   **ポート**: 記録した`-P`の情報である TiDB クラスターのポートを入力します。TiDB クラスターのデフォルト ポートは 4000 です。
    -   **ユーザー名**: 記録した`-u`の情報である TiDB クラスターのユーザー名を入力します。
    -   **パスワード**: TiDB クラスターのパスワードを入力します。
    -   **セキュリティ Socket Layer (SSL) モード**: **Verify-ca**を選択します。
    -   **「新しい CA 証明書の追加」**をクリックして、前の手順でTiDB Cloudコンソールからダウンロードした CA ファイルをインポートします。

    ![Fill in the target endpoint information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9.  CA ファイルをインポートします。

    ![Upload CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. **エンドポイント設定**、 **KMS キー**、**タグに**はデフォルト値を使用します。**エンドポイント接続のテスト (オプション)**セクションで、ソース データベースと同じ VPC を選択します。対応するレプリケーション インスタンスを選択し、**テストの実行**をクリックします。ステータスは**成功**である必要があります。

11. **[エンドポイントの作成]を**クリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## ステップ4. データベース移行タスクを作成する {#step-4-create-a-database-migration-task}

1.  AWS DMS コンソールで、 [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに移動します。リージョンに切り替えます。次に、ウィンドウの右上隅にある**[タスクの作成] を**クリックします。

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2.  次の情報を設定します。

    -   **タスク識別子**: タスクの名前を入力します。覚えやすい名前を使用することをお勧めします。
    -   **記述的な Amazon リソース名 (ARN) - オプション**: デフォルトの DMS ARN のわかりやすい名前を作成します。
    -   **レプリケーションインスタンス**: 先ほど作成した AWS DMS インスタンスを選択します。
    -   **ソース データベース エンドポイント**: 先ほど作成したソース データベース エンドポイントを選択します。
    -   **ターゲット データベース エンドポイント**: 作成したターゲット データベース エンドポイントを選択します。
    -   **移行タイプ**: 必要に応じて移行タイプを選択します。この例では、「**既存のデータを移行し、進行中の変更を複製する」を**選択します。

    ![Task configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3.  次の情報を設定します。

    -   **編集モード**:**ウィザード**を選択します。
    -   **ソース トランザクションのカスタム CDC 停止モード**: デフォルト設定を使用します。
    -   **ターゲット テーブル準備モード**: 必要に応じて、 **[何もしない]**またはその他のオプションを選択します。この例では、 **[何もしない]**を選択します。
    -   **フルロードが完了したらタスクを停止します**。デフォルト設定を使用します。
    -   **レプリケーションに LOB 列を含める**:**制限付き LOB モード**を選択します。
    -   **最大 LOB サイズ (KB)** : デフォルト値**32**を使用します。
    -   **検証をオンにします**。必要に応じて選択します。
    -   **タスク ログ**: 今後のトラブルシューティングのために**CloudWatch ログをオンにする**を選択します。関連する構成にはデフォルト設定を使用します。

    ![Task settings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4.  **テーブル マッピング**セクションで、移行するデータベースを指定します。

    スキーマ名は、Amazon RDS インスタンス内のデータベース名です。**ソース名**のデフォルト値は「%」で、これは Amazon RDS 内のすべてのデータベースが TiDB に移行されることを意味します。これにより、Amazon RDS 内の`mysql`や`sys`などのシステム データベースが TiDB クラスターに移行され、タスクが失敗します。したがって、特定のデータベース名を入力するか、すべてのシステム データベースを除外することをお勧めします。たとえば、次のスクリーンショットの設定によると、 `franktest`という名前のデータベースとそのデータベース内のすべてのテーブルのみが移行されます。

    ![Table mappings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5.  右下隅の**「タスクの作成」を**クリックします。

6.  [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに戻ります。地域に切り替えます。タスクのステータスと進行状況を確認できます。

    ![Tasks status](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

移行中に問題や障害が発生した場合は、 [クラウドウォッチ](https://console.aws.amazon.com/cloudwatch/home)のログ情報を確認して問題のトラブルシューティングを行うことができます。

![Troubleshooting](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 参照 {#see-also}

-   AWS DMS を TiDB Serverless または TiDB Dedicated に接続する方法の詳細については、 [AWS DMS をTiDB Cloudクラスターに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)参照してください。

-   Aurora MySQL や Amazon Relational Database Service (RDS) などの MySQL 互換データベースからTiDB Cloudに移行する場合は、 [TiDB Cloud上のデータ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)使用することをお勧めします。

-   AWS DMS を使用して Amazon RDS for Oracle から TiDB Serverless に移行する場合は、 [AWS DMS を使用して Amazon RDS for Oracle から TiDB Serverless に移行する](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)参照してください。
