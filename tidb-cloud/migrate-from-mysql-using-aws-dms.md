---
title: Migrate from MySQL-Compatible Databases to TiDB Cloud Using AWS DMS
summary: Learn how to migrate data from MySQL-compatible databases to TiDB Cloud using AWS Database Migration Service (AWS DMS).
---

# AWS DMS を使用して MySQL 互換データベースからTiDB Cloudに移行する {#migrate-from-mysql-compatible-databases-to-tidb-cloud-using-aws-dms}

PostgreSQL、Oracle、SQL Server などの異種データベースをTiDB Cloudに移行する場合は、AWS Database Migration Service (AWS DMS) を使用することをお勧めします。

AWS DMS は、リレーショナル データベース、データ ウェアハウス、NoSQL データベース、およびその他のタイプのデータ ストアを簡単に移行できるクラウド サービスです。 AWS DMS を使用して、データをTiDB Cloudに移行できます。

このドキュメントでは、Amazon RDS を例として使用し、AWS DMS を使用してデータをTiDB Cloudに移行する方法を示します。この手順は、自己ホスト型の MySQL データベースまたは Amazon AuroraからTiDB Cloudへのデータの移行にも適用されます。

この例では、データ ソースは Amazon RDS であり、データ送信先はTiDB CloudのDedicated Tierクラスターです。アップストリーム データベースとダウンストリーム データベースの両方が同じリージョンにあります。

## 前提条件 {#prerequisites}

移行を開始する前に、次の内容を必ずお読みください。

-   ソース データベースが Amazon RDS または Amazon Auroraの場合、 `binlog_format`パラメータを`ROW`に設定する必要があります。データベースがデフォルトのパラメーター グループを使用する場合、 `binlog_format`パラメーターはデフォルトで`MIXED`であり、変更できません。この場合、たとえば`newset`ように[新しいパラメータ グループを作成する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params)にし、その`binlog_format`を`ROW`に設定する必要があります。続いて[デフォルトのパラメータ グループを変更する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#USER_WorkingWithParamGroups.Modifying) ～ `newset` 。パラメータ グループを変更すると、データベースが再起動されることに注意してください。
-   ソース データベースが TiDB と互換性のある照合順序を使用していることを確認してください。 TiDB の utf8mb4 文字セットのデフォルトの照合順序は`utf8mb4_bin`です。しかし、MySQL 8.0 では、デフォルトの照合順序は`utf8mb4_0900_ai_ci`です。アップストリームの MySQL がデフォルトの照合順序を使用している場合、TiDB は`utf8mb4_0900_ai_ci`と互換性がないため、AWS DMS は TiDB にターゲット テーブルを作成できず、データを移行できません。この問題を解決するには、移行前にソース データベースの照合順序を`utf8mb4_bin`に変更する必要があります。 TiDB がサポートする文字セットと照合順序の完全なリストについては、 [文字セットと照合順序](https://docs.pingcap.com/tidb/stable/character-set-and-collation)を参照してください。
-   TiDB には、デフォルトで次のシステム データベースが含まれています: `INFORMATION_SCHEMA` 、 `PERFORMANCE_SCHEMA` 、 `mysql` 、 `sys` 、および`test` 。 AWS DMS 移行タスクを作成するときは、デフォルトの`%`使用して移行オブジェクトを選択するのではなく、これらのシステム データベースを除外する必要があります。そうしないと、AWS DMS はこれらのシステム データベースをソース データベースからターゲット TiDB に移行しようとするため、タスクが失敗します。この問題を回避するには、特定のデータベース名とテーブル名を入力することをお勧めします。
-   AWS DMS のパブリックおよびプライベート ネットワーク IP アドレスを、ソース データベースとターゲット データベースの両方の IP アクセス リストに追加します。そうしないと、一部のシナリオでネットワーク接続が失敗する可能性があります。
-   [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-on-aws)または[プライベート エンドポイント接続](/tidb-cloud/set-up-private-endpoint-connections.md)を使用して、AWS DMS と TiDB クラスターを接続します。
-   データ書き込みのパフォーマンスを向上させるために、AWS DMS と TiDB クラスターに同じリージョンを使用することをお勧めします。
-   AWS DMS `dms.t3.large` (2 つの vCPU と 8 GiBメモリ) 以上のインスタンス クラスを使用することをお勧めします。小さなインスタンス クラスは、メモリ不足 (OOM) エラーを引き起こす可能性があります。
-   AWS DMS は、ターゲット データベースに`awsdms_control`データベースを自動的に作成します。

## 制限 {#limitation}

AWS DMS はレプリケートをサポートしていません`DROP TABLE` 。

## ステップ 1.AWS DMS レプリケーションインスタンスを作成する {#step-1-create-an-aws-dms-replication-instance}

1.  AWS DMS コンソールの[レプリケーション インスタンス](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。 AWS DMS にはTiDB Cloudと同じリージョンを使用することをお勧めします。このドキュメントでは、アップストリーム データベースとダウンストリーム データベース、および DMS インスタンスはすべて**us-west-2**リージョンにあります。

2.  **[レプリケーション インスタンスの作成]**をクリックします。

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3.  インスタンス名、ARN、および説明を入力します。

4.  インスタンス構成を入力します。
    -   **インスタンス クラス**: 適切なインスタンス クラスを選択します。パフォーマンスを向上させるには、 `dms.t3.large`つ以上のインスタンス クラスを使用することをお勧めします。
    -   **エンジンのバージョン**: デフォルトの構成を使用します。
    -   **マルチ AZ** : ビジネス ニーズに基づいて、<strong>シングル AZ</strong>または<strong>マルチ AZ</strong>を選択します。

5.  **[割り当てられたstorage(GiB)]**フィールドでstorageを構成します。デフォルト構成を使用します。

6.  接続とセキュリティを構成します。
    -   **ネットワーク タイプ - 新規**: <strong>IPv4</strong>を選択します。
    -   **IPv4 の仮想プライベート クラウド (VPC)** : 必要な VPC を選択します。ネットワーク構成を簡素化するために、アップストリーム データベースと同じ VPC を使用することをお勧めします。
    -   **レプリケーション サブネット グループ**: レプリケーション インスタンスのサブネット グループを選択します。
    -   **一般公開**: デフォルトの構成を使用します。

7.  必要に応じて、 **[詳細設定]** 、 <strong>[メンテナンス]</strong> 、および<strong>[タグ]</strong>を構成します。 <strong>[レプリケーション インスタンスの作成]</strong>をクリックして、インスタンスの作成を終了します。

## ステップ 2. ソース データベース エンドポイントを作成する {#step-2-create-the-source-database-endpoint}

1.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、作成した複製インスタンスをクリックします。次のスクリーンショットに示すように、パブリック ネットワークとプライベート ネットワークの IP アドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  Amazon RDS のセキュリティ グループ ルールを設定します。この例では、AWS DMS インスタンスのパブリック IP アドレスとプライベート IP アドレスをセキュリティ グループに追加します。

    ![Configure the security group rules](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3.  **[エンドポイントの作成]**をクリックして、ソース データベース エンドポイントを作成します。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4.  この例では、 **[RDS DB インスタンスを選択]**をクリックし、ソース RDS インスタンスを選択します。ソース データベースが自己ホスト型の MySQL である場合は、この手順をスキップして、次の手順で情報を入力できます。

    ![Select RDS DB instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5.  次の情報を構成します。

    -   **エンドポイント識別子**: ソース エンドポイントのラベルを作成して、後続のタスク構成で識別できるようにします。
    -   **説明的な Amazon リソースネーム (ARN) - オプション**: デフォルトの DMS ARN のわかりやすい名前を作成します。
    -   **ソース エンジン**: <strong>MySQL</strong>を選択します。
    -   **エンドポイント データベースへのアクセス**: <strong>[アクセス情報を手動で提供する]</strong>を選択します。
    -   **サーバー名**: データ プロバイダーのデータサーバーの名前を入力します。データベースコンソールからコピーできます。アップストリームが Amazon RDS または Amazon Auroraの場合、名前は自動的に入力されます。ドメイン名のないセルフホスト MySQL の場合、IP アドレスを入力できます。
    -   ソース データベースの**Port** 、 <strong>Username</strong> 、および<strong>Password</strong>を入力します。
    -   **セキュリティ Socket Layer (SSL) モード**: 必要に応じて SSL モードを有効にできます。

    ![Fill in the endpoint configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6.  **エンドポイント設定**、 <strong>KMS キー</strong>、および<strong>タグ</strong>にはデフォルト値を使用します。 <strong>[エンドポイント接続のテスト (オプション)]</strong>セクションでは、ソース データベースと同じ VPC を選択して、ネットワーク構成を簡素化することをお勧めします。対応するレプリケーション インスタンスを選択し、 <strong>[テストの実行]</strong>をクリックします。ステータスは<strong>成功で</strong>ある必要があります。

7.  **[エンドポイントの作成]**をクリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)

## ステップ 3. ターゲット データベース エンドポイントを作成する {#step-3-create-the-target-database-endpoint}

1.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、作成した複製インスタンスをクリックします。次のスクリーンショットに示すように、パブリック ネットワークとプライベート ネットワークの IP アドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  TiDB Cloudコンソールで、 [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックしてから、右上隅にある**[接続]**をクリックして、 TiDB Cloudデータベース接続情報を取得します。

3.  ダイアログの**[ステップ 1: トラフィック フィルターの作成]**で、 <strong>[編集]</strong>をクリックし、AWS DMS コンソールからコピーしたパブリックおよびプライベート ネットワークの IP アドレスを入力して、 <strong>[フィルターの更新]</strong>をクリックします。 AWS DMS レプリケーション インスタンスのパブリック IP アドレスとプライベート IP アドレスを同時に TiDB クラスター トラフィック フィルターに追加することをお勧めします。そうしないと、一部のシナリオで AWS DMS が TiDB クラスターに接続できない場合があります。

4.  **[TiDB クラスター CA のダウンロード]**をクリックして、CA 証明書をダウンロードします。ダイアログの<strong>[ステップ 3: SQL クライアントに接続する] で</strong>、後で使用できるように接続文字列の`-u` 、 `-h` 、および`-P`の情報を書き留めます。

5.  ダイアログの**[VPC ピアリング]**タブをクリックし、 <strong>[ステップ 1: VPC のセットアップ]</strong>の下の<strong>[追加]</strong>をクリックして、TiDB クラスターと AWS DMS の VPC ピアリング接続を作成します。

6.  対応する情報を設定します。 [VPC ピアリング接続の設定](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。

7.  TiDB クラスターのターゲット エンドポイントを構成します。

    -   **エンドポイント タイプ**: <strong>[ターゲット エンドポイント]</strong>を選択します。
    -   **エンドポイント識別子**: エンドポイントの名前を入力します。
    -   **説明的な Amazon リソースネーム (ARN) - オプション**: デフォルトの DMS ARN のわかりやすい名前を作成します。
    -   **ターゲット エンジン**: <strong>MySQL</strong>を選択します。

    ![Configure the target endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、 **[エンドポイントの作成]**をクリックしてターゲット データベース エンドポイントを作成し、次の情報を構成します。

    -   **サーバー名**: TiDB クラスターのホスト名を入力します。これは、記録した`-h`情報です。
    -   **ポート**: TiDB クラスターのポートを入力します。これは、記録した`-P`情報です。 TiDB クラスターのデフォルトのポートは 4000 です。
    -   **ユーザー名**: TiDB クラスターのユーザー名を入力します。これは、記録した`-u`情報です。
    -   **パスワード**: TiDB クラスターのパスワードを入力します。
    -   **セキュリティ Socket Layer (SSL) モード**: <strong>Verify-ca</strong>を選択します。
    -   **Add new CA certificate**をクリックして、前の手順でTiDB Cloudコンソールからダウンロードした CA ファイルをインポートします。

    ![Fill in the target endpoint information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9.  CA ファイルをインポートします。

    ![Upload CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. **Endpoint settings** 、 <strong>KMS key</strong> 、および<strong>Tags</strong>にはデフォルト値を使用します。 <strong>[Test endpoint connection (optional)]</strong>セクションで、ソース データベースと同じ VPC を選択します。対応するレプリケーション インスタンスを選択し、 <strong>[テストの実行]</strong>をクリックします。ステータスは<strong>成功で</strong>ある必要があります。

11. **[エンドポイントの作成]**をクリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## ステップ 4. データベース移行タスクを作成する {#step-4-create-a-database-migration-task}

1.  AWS DMS コンソールで、 [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに移動します。お住まいの地域に切り替えます。次に、ウィンドウの右上隅にある**[タスクの作成]**をクリックします。

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2.  次の情報を構成します。

    -   **タスク識別子**: タスクの名前を入力します。覚えやすい名前を使用することをお勧めします。
    -   **説明的な Amazon リソースネーム (ARN) - オプション**: デフォルトの DMS ARN のわかりやすい名前を作成します。
    -   **レプリケーション インスタンス**: 作成した AWS DMS インスタンスを選択します。
    -   **ソース データベース エンドポイント**: 作成したソース データベース エンドポイントを選択します。
    -   **ターゲット データベース エンドポイント**: 作成したターゲット データベース エンドポイントを選択します。
    -   **移行タイプ**: 必要に応じて移行タイプを選択します。この例では、 <strong>[既存のデータを移行し、進行中の変更をレプリケートする]</strong>を選択します。

    ![Task configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3.  次の情報を構成します。

    -   **編集モード**:<strong>ウィザード</strong>を選択します。
    -   **ソース トランザクションのカスタム CDC 停止モード**: デフォルト設定を使用します。
    -   **ターゲット テーブル準備モード**: 必要に応じて、 <strong>[何もしない]</strong>またはその他のオプションを選択します。この例では、 <strong>[何もしない]</strong>を選択します。
    -   **全ロード完了後にタスクを停止**: デフォルト設定を使用します。
    -   **レプリケーションに LOB 列を含める**:<strong>限定 LOB モード</strong>を選択します。
    -   **LOB の最大サイズ (KB)** : デフォルト値の<strong>32</strong>を使用します。
    -   **検証を有効にする**: 必要に応じて選択します。
    -   **タスク ログ**: [今後のトラブルシューティングのために<strong>CloudWatch ログをオンにする]</strong>を選択します。関連する構成にはデフォルト設定を使用します。

    ![Task settings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4.  **[テーブル マッピング]**セクションで、移行するデータベースを指定します。

    スキーマ名は、Amazon RDS インスタンスのデータベース名です。**ソース名**のデフォルト値は「%」です。これは、Amazon RDS 内のすべてのデータベースが TiDB に移行されることを意味します。 Amazon RDS の`mysql`や`sys`などのシステム データベースが TiDB クラスターに移行され、タスクが失敗します。したがって、特定のデータベース名を入力するか、すべてのシステム データベースを除外することをお勧めします。たとえば、次のスクリーンショットの設定によれば、 `franktest`という名前のデータベースとそのデータベース内のすべてのテーブルのみが移行されます。

    ![Table mappings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5.  右下隅にある**[タスクの作成]**をクリックします。

6.  [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに戻ります。お住まいの地域に切り替えます。タスクのステータスと進行状況を確認できます。

    ![Tasks status](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

移行中に問題や障害が発生した場合は、 [クラウドウォッチ](https://console.aws.amazon.com/cloudwatch/home)のログ情報を確認して問題をトラブルシューティングできます。

![Troubleshooting](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## こちらもご覧ください {#see-also}

-   Aurora MySQL や Amazon Relational Database Service (RDS) などの MySQL 互換データベースからTiDB Cloudに移行する場合は、 [TiDB Cloudでのデータ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を使用することをお勧めします。

-   AWS DMS を使用して Amazon RDS for Oracle からTiDB Cloud Serverless Tierに移行する場合は、 [AWS DMS を使用して Amazon RDS for Oracle からTiDB CloudServerless Tierに移行する](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)を参照してください。
