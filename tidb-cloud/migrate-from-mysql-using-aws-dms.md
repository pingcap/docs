---
title: Migrate from MySQL-Compatible Databases to TiDB Cloud Using AWS DMS
summary: Learn how to migrate data from MySQL-compatible databases to TiDB Cloud using AWS Database Migration Service (AWS DMS).
---

# AWS DMS を使用して MySQL 互換データベースからTiDB Cloudに移行する {#migrate-from-mysql-compatible-databases-to-tidb-cloud-using-aws-dms}

PostgreSQL、Oracle、SQL Server などの異種データベースをTiDB Cloudに移行する場合は、AWS Database Migration Service (AWS DMS) を使用することをお勧めします。

AWS DMS は、リレーショナル データベース、データ ウェアハウス、NoSQL データベース、その他のタイプのデータ ストアの移行を簡単にするクラウド サービスです。 AWS DMS を使用してデータをTiDB Cloudに移行できます。

このドキュメントでは、Amazon RDS を例として使用し、AWS DMS を使用してTiDB Cloudにデータを移行する方法を示します。この手順は、セルフホスト型 MySQL データベースまたは Amazon AuroraからTiDB Cloudへのデータの移行にも適用されます。

この例では、データ ソースは Amazon RDS で、データの宛先はTiDB Cloudの TiDB 専用クラスターです。アップストリーム データベースとダウンストリーム データベースは両方とも同じリージョンにあります。

## 前提条件 {#prerequisites}

移行を開始する前に、次の内容を必ず読んでください。

-   ソースデータベースが Amazon RDS または Amazon Auroraの場合は、 `binlog_format`パラメータを`ROW`に設定する必要があります。データベースがデフォルトのパラメータ グループを使用する場合、 `binlog_format`パラメータはデフォルトで`MIXED`になり、変更できません。この場合、 [新しいパラメータグループを作成する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params) (たとえば`newset`を指定し、その`binlog_format`を`ROW`に設定する必要があります。次に、 [デフォルトのパラメータグループを変更する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#USER_WorkingWithParamGroups.Modifying) ～ `newset` 。パラメータグループを変更するとデータベースが再起動されることに注意してください。
-   ソース データベースが TiDB と互換性のある照合順序を使用していることを確認してください。 TiDB の utf8mb4 文字セットのデフォルトの照合順序は`utf8mb4_bin`です。ただし、MySQL 8.0 では、デフォルトの照合順序は`utf8mb4_0900_ai_ci`です。アップストリームの MySQL がデフォルトの照合順序を使用する場合、TiDB は`utf8mb4_0900_ai_ci`と互換性がないため、AWS DMS は TiDB にターゲットテーブルを作成できず、データを移行できません。この問題を解決するには、移行前にソース データベースの照合順序を`utf8mb4_bin`に変更する必要があります。 TiDB でサポートされる文字セットと照合順序の完全なリストについては、 [文字セットと照合順序](https://docs.pingcap.com/tidb/stable/character-set-and-collation)を参照してください。
-   TiDB には、デフォルトでシステム データベース`INFORMATION_SCHEMA` 、 `PERFORMANCE_SCHEMA` 、 `mysql` 、 `sys` 、および`test`が含まれています。 AWS DMS 移行タスクを作成するときは、デフォルトの`%`使用して移行オブジェクトを選択するのではなく、これらのシステム データベースをフィルタリングして除外する必要があります。そうしないと、AWS DMS はこれらのシステム データベースをソース データベースからターゲット TiDB に移行しようとし、タスクが失敗します。この問題を回避するには、特定のデータベース名とテーブル名を入力することをお勧めします。
-   AWS DMS のパブリックおよびプライベートネットワーク IP アドレスを、ソースデータベースとターゲットデータベースの両方の IP アクセスリストに追加します。そうしないと、一部のシナリオでネットワーク接続が失敗する可能性があります。
-   [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-on-aws)または[プライベートエンドポイント接続](/tidb-cloud/set-up-private-endpoint-connections.md)を使用して、AWS DMS と TiDB クラスターを接続します。
-   データ書き込みパフォーマンスを向上させるために、AWS DMS と TiDB クラスターに同じリージョンを使用することをお勧めします。
-   AWS DMS `dms.t3.large` (2 vCPU と 8 GiBメモリ) 以降のインスタンス クラスを使用することをお勧めします。小さなインスタンス クラスでは、メモリ不足 (OOM) エラーが発生する可能性があります。
-   AWS DMS は、ターゲット データベースに`awsdms_control`データベースを自動的に作成します。

## 制限 {#limitation}

AWS DMS はレプリケーションをサポートしていません`DROP TABLE` 。

## ステップ 1. AWS DMS レプリケーションインスタンスを作成する {#step-1-create-an-aws-dms-replication-instance}

1.  AWS DMS コンソールの[レプリケーションインスタンス](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。 AWS DMS にはTiDB Cloudと同じリージョンを使用することをお勧めします。このドキュメントでは、アップストリームおよびダウンストリームのデータベースと DMS インスタンスはすべて**us-west-2**リージョンにあります。

2.  **[レプリケーション インスタンスの作成]**をクリックします。

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3.  インスタンス名、ARN、説明を入力します。

4.  インスタンス構成を入力します。
    -   **インスタンス クラス**: 適切なインスタンス クラスを選択します。パフォーマンスを向上させるには、 `dms.t3.large`つ以上のインスタンス クラスを使用することをお勧めします。
    -   **エンジンのバージョン**: デフォルトの構成を使用します。
    -   **マルチ AZ** : ビジネス ニーズに基づいて**シングル AZ**または**マルチ AZ**を選択します。

5.  **[割り当てられたstorage(GiB)]**フィールドでstorageを構成します。デフォルトの構成を使用します。

6.  接続とセキュリティを構成します。
    -   **ネットワーク タイプ - 新規**: **IPv4**を選択します。
    -   **IPv4 用の仮想プライベート クラウド (VPC)** : 必要な VPC を選択します。ネットワーク構成を簡素化するために、上流データベースと同じ VPC を使用することをお勧めします。
    -   **レプリケーション サブネット グループ**: レプリケーション インスタンスのサブネット グループを選択します。
    -   **パブリックにアクセス可能**: デフォルト設定を使用します。

7.  必要に応じて、 **[詳細設定]** 、 **[メンテナンス]** 、および**[タグ]**を構成します。 **「レプリケーション・インスタンスの作成」**をクリックしてインスタンスの作成を完了します。

## ステップ 2. ソース データベース エンドポイントを作成する {#step-2-create-the-source-database-endpoint}

1.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、作成したばかりのレプリケーション インスタンスをクリックします。次のスクリーンショットに示すように、パブリック ネットワーク IP アドレスとプライベート ネットワーク IP アドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  Amazon RDS のセキュリティ グループ ルールを設定します。この例では、AWS DMS インスタンスのパブリック IP アドレスとプライベート IP アドレスをセキュリティ グループに追加します。

    ![Configure the security group rules](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3.  **[エンドポイントの作成]**をクリックして、ソース データベース エンドポイントを作成します。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4.  この例では、 **[RDS DB インスタンスの選択]**をクリックして、ソース RDS インスタンスを選択します。ソース データベースがセルフホスト型 MySQL である場合は、この手順をスキップして、次の手順で情報を入力できます。

    ![Select RDS DB instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5.  次の情報を設定します。

    -   **エンドポイント識別子**: ソース エンドポイントのラベルを作成して、後続のタスク構成で識別しやすくします。
    -   **説明的な Amazon リソースネーム (ARN) - オプション**: デフォルトの DMS ARN のフレンドリ名を作成します。
    -   **ソース エンジン**: **MySQL**を選択します。
    -   **エンドポイント データベースへのアクセス**: **[アクセス情報を手動で提供する]**を選択します。
    -   **サーバー名**: データプロバイダーのデータサーバーの名前を入力します。データベース コンソールからコピーできます。アップストリームが Amazon RDS または Amazon Auroraの場合、名前は自動的に入力されます。ドメイン名のないセルフホスト MySQL の場合は、IP アドレスを入力できます。
    -   ソース データベースの [**ポート]** 、 **[ユーザー名**] 、および**[パスワード]**を入力します。
    -   **セキュリティ Socket Layer (SSL) モード**: 必要に応じて SSL モードを有効にできます。

    ![Fill in the endpoint configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6.  **エンドポイント設定**、 **KMS キー**、**タグに**はデフォルト値を使用します。 **[エンドポイント接続のテスト (オプション)]**セクションでは、ネットワーク構成を簡素化するために、ソース データベースと同じ VPC を選択することをお勧めします。対応するレプリケーション インスタンスを選択し、 **[テストの実行]**をクリックします。ステータスは**成功で**ある必要があります。

7.  **「エンドポイントの作成」**をクリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)

## ステップ 3. ターゲット データベース エンドポイントを作成する {#step-3-create-the-target-database-endpoint}

1.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、作成したばかりのレプリケーション インスタンスをクリックします。次のスクリーンショットに示すように、パブリック ネットワーク IP アドレスとプライベート ネットワーク IP アドレスをコピーします。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2.  TiDB Cloudコンソールで、 [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックし、右上隅にある**[接続]**をクリックして、 TiDB Cloudデータベース接続情報を取得します。

3.  **[ステップ 1: ダイアログのトラフィック フィルターを作成する]**で、 **[編集]**をクリックし、AWS DMS コンソールからコピーしたパブリック ネットワークおよびプライベート ネットワークの IP アドレスを入力し、 **[フィルターの更新]**をクリックします。 AWS DMS レプリケーション インスタンスのパブリック IP アドレスとプライベート IP アドレスを同時に TiDB クラスター トラフィック フィルターに追加することをお勧めします。そうしないと、一部のシナリオでは AWS DMS が TiDB クラスターに接続できない可能性があります。

4.  **[TiDB クラスター CA のダウンロード]**をクリックして CA 証明書をダウンロードします。ダイアログの**「ステップ 3: SQL クライアントに接続する」で**、後で使用できるように接続文字列の`-u` 、 `-h` 、および`-P`の情報をメモします。

5.  ダイアログの**[VPC ピアリング]**タブをクリックし、 **[ステップ 1: VPC をセットアップする]**で**[追加**] をクリックして、TiDB クラスターと AWS DMS の VPC ピアリング接続を作成します。

6.  対応する情報を設定します。 [VPC ピア接続のセットアップ](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。

7.  TiDB クラスターのターゲット エンドポイントを構成します。

    -   **エンドポイント タイプ**: **[ターゲット エンドポイント]**を選択します。
    -   **エンドポイント識別子**: エンドポイントの名前を入力します。
    -   **説明的な Amazon リソースネーム (ARN) - オプション**: デフォルトの DMS ARN のフレンドリ名を作成します。
    -   **ターゲット エンジン**: **MySQL**を選択します。

    ![Configure the target endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8.  [AWS DMS コンソール](https://console.aws.amazon.com/dms/v2/home)で、 **[エンドポイントの作成]**をクリックしてターゲット データベース エンドポイントを作成し、次の情報を構成します。

    -   **サーバー名**: TiDB クラスターのホスト名を入力します。これは、記録した`-h`情報です。
    -   **Port** : TiDB クラスターのポートを入力します。これは、記録した`-P`の情報です。 TiDB クラスターのデフォルトのポートは 4000 です。
    -   **ユーザー名**: TiDB クラスターのユーザー名を入力します。これは、記録した`-u`情報です。
    -   **パスワード**: TiDB クラスターのパスワードを入力します。
    -   **セキュリティ Socket Layer (SSL) モード**: **Verify-ca**を選択します。
    -   **[新しい CA 証明書の追加]**をクリックして、前の手順でTiDB Cloudコンソールからダウンロードした CA ファイルをインポートします。

    ![Fill in the target endpoint information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9.  CA ファイルをインポートします。

    ![Upload CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. **エンドポイント設定**、 **KMS キー**、および**タグ**にはデフォルト値を使用します。 **[エンドポイント接続のテスト (オプション)]**セクションで、ソース データベースと同じ VPC を選択します。対応するレプリケーション インスタンスを選択し、 **[テストの実行]**をクリックします。ステータスは**成功で**ある必要があります。

11. **「エンドポイントの作成」**をクリックします。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## ステップ 4. データベース移行タスクを作成する {#step-4-create-a-database-migration-task}

1.  AWS DMS コンソールで、 [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに移動します。お住まいの地域に切り替えてください。次に、ウィンドウの右上隅にある**「タスクの作成」**をクリックします。

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2.  次の情報を設定します。

    -   **タスク識別子**: タスクの名前を入力します。覚えやすい名前を使用することをお勧めします。
    -   **説明的な Amazon リソースネーム (ARN) - オプション**: デフォルトの DMS ARN のフレンドリ名を作成します。
    -   **レプリケーションインスタンス**: 作成したばかりの AWS DMS インスタンスを選択します。
    -   **ソース データベース エンドポイント**: 作成したばかりのソース データベース エンドポイントを選択します。
    -   **ターゲット データベース エンドポイント**: 作成したばかりのターゲット データベース エンドポイントを選択します。
    -   **移行タイプ**: 必要に応じて移行タイプを選択します。この例では、 **[既存のデータを移行し、進行中の変更をレプリケートする]**を選択します。

    ![Task configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3.  次の情報を設定します。

    -   **編集モード**:**ウィザード**を選択します。
    -   **ソース トランザクションのカスタム CDC 停止モード**: デフォルト設定を使用します。
    -   **ターゲットテーブル準備モード**: 必要に応じて、 **[何もしない]**または他のオプションを選択します。この例では、 **[何もしない]**を選択します。
    -   **全ロード完了後にタスクを停止**: デフォルト設定を使用します。
    -   **レプリケーションに LOB 列を含める**:**制限付き LOB モード**を選択します。
    -   **最大 LOB サイズ (KB)** : デフォルト値**32**を使用します。
    -   **検証をオンにする**: ニーズに応じて選択します。
    -   **タスク ログ**: 今後のトラブルシューティングのために**CloudWatch ログをオンにする**を選択します。関連する構成にはデフォルト設定を使用します。

    ![Task settings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4.  **[テーブル マッピング]**セクションで、移行するデータベースを指定します。

    スキーマ名は、Amazon RDS インスタンスのデータベース名です。**ソース名**のデフォルト値は「%」です。これは、Amazon RDS 内のすべてのデータベースが TiDB に移行されることを意味します。これにより、Amazon RDS の`mysql`や`sys`などのシステム データベースが TiDB クラスターに移行され、タスクが失敗します。したがって、特定のデータベース名を入力するか、すべてのシステム データベースをフィルターで除外することをお勧めします。たとえば、次のスクリーンショットの設定によれば、 `franktest`という名前のデータベースとそのデータベース内のすべてのテーブルのみが移行されます。

    ![Table mappings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5.  右下隅にある**「タスクの作成」**をクリックします。

6.  [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに戻ります。お住まいの地域に切り替えてください。タスクのステータスと進捗状況を確認できます。

    ![Tasks status](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

移行中に問題や障害が発生した場合は、 [クラウドウォッチ](https://console.aws.amazon.com/cloudwatch/home)のログ情報を確認して問題のトラブルシューティングを行うことができます。

![Troubleshooting](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## こちらも参照 {#see-also}

-   Aurora MySQL や Amazon Relational Database Service (RDS) などの MySQL 互換データベースからTiDB Cloudに移行する場合は、 [TiDB Cloudでのデータ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を使用することをお勧めします。

-   AWS DMS を使用して Amazon RDS for Oracle から TiDB サーバーレスに移行する場合は、 [AWS DMS を使用して Amazon RDS for Oracle から TiDB サーバーレスに移行する](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)を参照してください。
