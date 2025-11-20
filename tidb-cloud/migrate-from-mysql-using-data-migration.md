---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: データ移行機能を使用して、最小限のダウンタイムで、MySQL データベースを Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL、またはセルフマネージド MySQL インスタンスからTiDB Cloudにシームレスに移行する方法について説明します。
aliases: ['/tidbcloud/migrate-data-into-tidb','/tidbcloud/migrate-incremental-data-from-mysql']
---

# データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する {#migrate-mysql-compatible-databases-to-tidb-cloud-using-data-migration}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com/)のデータ移行機能を使用して、MySQL データベースを Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL、またはセルフマネージド MySQL インスタンスからTiDB Cloudに移行する方法について説明します。

この機能により、既存のMySQLデータを移行し、MySQL互換のソースデータベースからTiDB Cloudに直接、進行中の変更（ binlog ）を継続的に複製することで、同一リージョン内または異なるリージョン間でデータの一貫性を維持できます。この合理化されたプロセスにより、個別のダンプおよびロード操作が不要になり、ダウンタイムが短縮され、MySQLからよりスケーラブルなプラットフォームへの移行が簡素化されます。

MySQL 互換データベースからTiDB Cloudに進行中のbinlog の変更のみを複製する場合は、 [データ移行を使用して MySQL 互換データベースからTiDB Cloudに増分データを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)参照してください。

## 制限事項 {#limitations}

### 可用性 {#availability}

-   データ移行機能は、 **TiDB Cloud Dedicated**クラスターでのみ使用できます。

-   [TiDB Cloudコンソール](https://tidbcloud.com/)にTiDB Cloud Dedicated クラスターの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md#step-1-go-to-the-data-migration-page)エントリが表示されない場合、この機能はお客様のリージョンではご利用いただけない可能性があります。お客様のリージョンでのサポートをご希望の場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

-   Amazon Aurora MySQL ライターインスタンスは、既存データと増分データの両方の移行をサポートします。Amazon Aurora MySQL リーダーインスタンスは、既存データのみの移行をサポートし、増分データ移行はサポートしません。

### 移行ジョブの最大数 {#maximum-number-of-migration-jobs}

組織ごとに最大200件の移行ジョブを作成できます。それ以上の移行ジョブを作成するには、 [サポートチケットを提出する](/tidb-cloud/tidb-cloud-support.md) .

### フィルタリングされ削除されたデータベース {#filtered-out-and-deleted-databases}

-   移行対象データベースをすべて選択した場合でも、システムデータベースは除外され、 TiDB Cloudに移行されません。つまり、 `mysql` 、 `information_schema` 、 `performance_schema` 、 `sys`はこの機能では移行されません。

-   TiDB Cloudでクラスターを削除すると、そのクラスター内のすべての移行ジョブが自動的に削除され、回復できなくなります。

### 既存のデータ移行の制限 {#limitations-of-existing-data-migration}

-   既存のデータの移行中に、ターゲット データベースに移行対象のテーブルがすでに含まれていて、重複キーがある場合は、重複キーを持つ行が置き換えられます。

-   データセットのサイズが1 TiB未満の場合は、論理モード（デフォルトモード）の使用をお勧めします。データセットのサイズが1 TiBを超える場合、または既存のデータをより速く移行したい場合は、物理モードを使用できます。詳細については、 [既存データと増分データを移行する](#migrate-existing-data-and-incremental-data)ご覧ください。

### 増分データ移行の制限 {#limitations-of-incremental-data-migration}

-   増分データ移行中に、移行対象のテーブルがターゲットデータベースに重複キーで既に存在する場合、エラーが報告され、移行は中断されます。このような状況では、MySQLソースデータが正確かどうかを確認する必要があります。正しい場合は、移行ジョブの「再開」ボタンをクリックしてください。移行ジョブは、ターゲットTiDB Cloudクラスタの競合するレコードをMySQLソースレコードに置き換えます。

-   増分レプリケーション（進行中の変更をクラスタに移行する）中に、移行ジョブが突発的なエラーから回復した場合、60秒間のセーフモードが起動することがあります。セーフモード中は、 `INSERT`文が`REPLACE`として、 `UPDATE`文が`DELETE`および`REPLACE`として移行され、その後、これらのトランザクションがターゲットTiDB Cloudクラスタに移行されます。これにより、突発的なエラー発生時のすべてのデータがターゲットTiDB Cloudクラスタにスムーズに移行されたことが確認されます。このシナリオでは、主キーや非NULLの一意のインデックスを持たないMySQLソーステーブルの場合、データがターゲットTiDB Cloudクラスタに繰り返し挿入される可能性があるため、一部のデータがターゲットTiDB Cloudクラスタで重複する可能性があります。

-   次のシナリオでは、移行ジョブに 24 時間以上かかる場合は、ソース データベースのバイナリ ログを消去せず、データ移行が増分レプリケーション用に連続したバイナリ ログを取得できるようにします。

    -   既存のデータの移行中。
    -   既存のデータ移行が完了し、増分データ移行が初めて開始されたとき、レイテンシーは0 ミリ秒ではありません。

## 前提条件 {#prerequisites}

移行する前に、データ ソースがサポートされているかどうかを確認し、MySQL 互換データベースでバイナリ ログを有効にし、ネットワーク接続を確認し、ソース データベースとターゲットTiDB Cloudクラスター データベースの両方に必要な権限を付与します。

### データソースとバージョンがサポートされていることを確認してください {#make-sure-your-data-source-and-version-are-supported}

データ移行では、次のデータ ソースとバージョンがサポートされます。

| データソース                                 | サポートされているバージョン |
| :------------------------------------- | :------------- |
| セルフマネージド MySQL (オンプレミスまたはパブリック クラウド)   | 8.0、5.7、5.6    |
| Amazon Aurora MySQL                    | 8.0、5.7、5.6    |
| Amazon RDS MySQL                       | 8.0、5.7        |
| Azure Database for MySQL - フレキシブル サーバー | 8.0、5.7        |
| MySQL 用 Google Cloud SQL               | 8.0、5.7、5.6    |

### レプリケーション用のソースMySQL互換データベースでバイナリログを有効にする {#enable-binary-logs-in-the-source-mysql-compatible-database-for-replication}

DM を使用してソースの MySQL 互換データベースからTiDB Cloudターゲット クラスターに増分変更を継続的にレプリケートするには、ソース データベースでバイナリ ログを有効にするために次の構成が必要です。

| コンフィグレーション                   | 必要な値                             | なぜ                                         |
| :--------------------------- | :------------------------------- | :----------------------------------------- |
| `log_bin`                    | `ON`                             | バイナリログを有効にします。DM はこれを使用して TiDB への変更を複製します。 |
| `binlog_format`              | `ROW`                            | すべてのデータの変更を正確にキャプチャします（他の形式ではエッジケースが失われます） |
| `binlog_row_image`           | `FULL`                           | 安全な競合解決のためにイベントにすべての列値を含める                 |
| `binlog_expire_logs_seconds` | ≥ `86400` （1日）、 `604800` （7日、推奨） | 移行中に DM が連続したログにアクセスできるようにします              |

#### 現在の値を確認し、ソースMySQLインスタンスを構成する {#check-current-values-and-configure-the-source-mysql-instance}

現在の構成を確認するには、ソース MySQL インスタンスに接続し、次のステートメントを実行します。

```sql
SHOW VARIABLES WHERE Variable_name IN
('log_bin','server_id','binlog_format','binlog_row_image',
'binlog_expire_logs_seconds','expire_logs_days');
```

必要に応じて、必要な値に合わせてソース MySQL インスタンスの構成を変更します。

<details><summary>セルフマネージドMySQLインスタンスを構成する</summary>

1.  `/etc/my.cnf`を開いて以下を追加します。

        [mysqld]
        log_bin = mysql-bin
        binlog_format = ROW
        binlog_row_image = FULL
        binlog_expire_logs_seconds = 604800   # 7 days retention

2.  変更を適用するには、MySQL サービスを再起動します。

        sudo systemctl restart mysqld

3.  設定が有効になっていることを確認するために、 `SHOW VARIABLES`ステートメントを再度実行します。

詳細な手順については、MySQL ドキュメントの[MySQLサーバーのシステム変数](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html)と[バイナリログ](https://dev.mysql.com/doc/refman/8.0/en/binary-log.html)参照してください。

</details>

<details><summary>AWS RDS またはAurora MySQL を構成する</summary>

1.  AWS マネジメントコンソールで、 [Amazon RDS コンソール](https://console.aws.amazon.com/rds/)を開き、左側のナビゲーションペインで**[パラメータグループ]**をクリックして、カスタムパラメータグループを作成または編集します。
2.  上記の 4 つのパラメータを必要な値に設定します。
3.  パラメータ グループをインスタンスまたはクラスターにアタッチし、再起動して変更を適用します。
4.  再起動後、インスタンスに接続し、 `SHOW VARIABLES`ステートメントを実行して構成を確認します。

詳細な手順については、AWS ドキュメントの[DBパラメータグループの操作](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html)と[MySQLバイナリログの設定](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)参照してください。

</details>

<details><summary>Azure Database for MySQL を構成する - フレキシブル サーバー</summary>

1.  [Azureポータル](https://portal.azure.com/)で、 **Azure Database for MySQL サーバーを**検索して選択し、インスタンス名をクリックして、左側のナビゲーション ウィンドウで**[設定]** &gt; **[サーバー パラメーター]**をクリックします。

2.  各パラメータを検索し、その値を更新します。

    ほとんどの変更は再起動なしで有効になります。再起動が必要な場合は、ポータルからプロンプトが表示されます。

3.  `SHOW VARIABLES`ステートメントを実行して構成を確認します。

詳細な手順については、Microsoft Azure ドキュメントの[Azure Portal を使用して Azure Database for MySQL - フレキシブル サーバーのサーバーパラメーターを構成する](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-configure-server-parameters-portal)参照してください。

</details>

<details><summary>Google Cloud SQL for MySQL を構成する</summary>

1.  [Google Cloud コンソール](https://console.cloud.google.com/project/_/sql/instances)で、インスタンスを含むプロジェクトを選択し、インスタンス名をクリックして、 **[編集]**をクリックします。
2.  必要なフラグ（ `log_bin` 、 `binlog_format` 、 `binlog_row_image` 、 `binlog_expire_logs_seconds` ）を追加または変更します。
3.  **「保存」**をクリックします。再起動が必要な場合は、コンソールからプロンプトが表示されます。
4.  再起動後、 `SHOW VARIABLES`ステートメントを実行して変更を確認します。

詳細な手順については、Google Cloud ドキュメントの[データベースフラグを構成する](https://cloud.google.com/sql/docs/mysql/flags)と[ポイントインタイムリカバリを使用する](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr)ご覧ください。

</details>

### ネットワーク接続を確保する {#ensure-network-connectivity}

移行ジョブを作成する前に、ソース MySQL インスタンス、 TiDB Cloud Data Migration (DM) サービス、およびターゲットTiDB Cloudクラスター間の適切なネットワーク接続を計画して設定する必要があります。

利用可能な接続方法は次のとおりです。

| 接続方法                      | 可用性                                | おすすめ                                                   |
| :------------------------ | :--------------------------------- | :----------------------------------------------------- |
| パブリックエンドポイントまたはIPアドレス     | TiDB Cloudでサポートされているすべてのクラウドプロバイダー | 迅速な概念実証の移行、テスト、またはプライベート接続が利用できない場合                    |
| プライベートリンクまたはプライベートエンドポイント | AWSとAzureのみ                        | パブリックインターネットにデータを公開せずに本番環境のワークロードを実行                   |
| VPCピアリング                  | AWSとGoogle Cloudのみ                 | 低レイテンシのリージョン内接続を必要とし、重複しない VPC/VNet CIDR を持つ本番環境ワークロード |

クラウド プロバイダー、ネットワーク トポロジ、セキュリティ要件に最適な接続方法を選択し、その方法のセットアップ手順に従います。

#### TLS/SSL によるエンドツーエンドの暗号化 {#end-to-end-encryption-over-tls-ssl}

接続方法に関わらず、エンドツーエンドの暗号化にはTLS/SSLの使用を強くお勧めします。プライベートエンドポイントとVPCピアリングはネットワークパスを保護しますが、TLS/SSLはデータ自体を保護し、コンプライアンス要件の遵守に役立ちます。

<details><summary>TLS/SSL暗号化接続用のクラウドプロバイダーの証明書をダウンロードして保存します</summary>

-   Amazon Aurora MySQL または Amazon RDS MySQL: [SSL/TLS を使用して DB インスタンスまたはクラスターへの接続を暗号化する](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html)
-   Azure Database for MySQL - フレキシブル サーバー: [暗号化された接続で接続する](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl)
-   MySQL 用 Google Cloud SQL: [SSL/TLS証明書を管理する](https://cloud.google.com/sql/docs/mysql/manage-ssl-instance)

</details>

#### パブリックエンドポイントまたはIPアドレス {#public-endpoints-or-ip-addresses}

パブリックエンドポイントを使用する場合、ネットワーク接続とアクセスを、DMジョブ作成プロセス中にも、すぐにでも確認できます。その際、 TiDB Cloud具体的な出力IPアドレスと指示が表示されます。

> **注記**：
>
> ファイアウォールの出力IP範囲は、データ移行タスクの作成時にのみ利用可能です。このIP範囲を事前に取得することはできません。開始する前に、以下の点をご確認ください。
>
> -   ファイアウォール ルールを変更する権限を持ちます。
> -   セットアップ プロセス中にクラウド プロバイダーのコンソールにアクセスできます。
> -   ファイアウォールを構成するために、タスク作成ワークフローを一時停止できます。

1.  ソース MySQL インスタンスのエンドポイント ホスト名 (FQDN) またはパブリック IP アドレスを識別して記録します。

2.  データベースのファイアウォールまたはセキュリティグループのルールを変更するために必要な権限があることを確認してください。以下の手順については、クラウドプロバイダーのドキュメントを参照してください。

    -   Amazon Aurora MySQL または Amazon RDS MySQL: [セキュリティグループによるアクセス制御](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Overview.RDSSecurityGroups.html) .
    -   Azure Database for MySQL - フレキシブル サーバー: [パブリックネットワークアクセス](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-networking-public)
    -   MySQL 用 Google Cloud SQL: [承認されたネットワーク](https://cloud.google.com/sql/docs/mysql/configure-ip#authorized-networks) 。

3.  オプション: 転送中の暗号化に適切な証明書を使用して、パブリック インターネットにアクセスできるマシンからソース データベースへの接続を確認します。

    ```shell
    mysql -h <public-host> -P <port> -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4.  後ほど、データ移行ジョブのセットアップ中に、 TiDB Cloud出力 IP 範囲が提供されます。その際に、上記と同じ手順に従って、この IP 範囲をデータベースのファイアウォールまたはセキュリティグループのルールに追加する必要があります。

#### プライベートリンクまたはプライベートエンドポイント {#private-link-or-private-endpoint}

プロバイダーネイティブのプライベート リンクまたはプライベート エンドポイントを使用する場合は、ソース MySQL インスタンス (RDS、 Aurora、または Azure Database for MySQL) のプライベート エンドポイントを作成します。

<details><summary>MySQLソースデータベース用のAWS PrivateLinkとプライベートエンドポイントを設定する</summary>

AWS は RDS またはAuroraへの直接の PrivateLink アクセスをサポートしていません。そのため、ネットワークロードバランサー (NLB) を作成し、ソース MySQL インスタンスに関連付けられたエンドポイントサービスとして公開する必要があります。

1.  [Amazon EC2 コンソール](https://console.aws.amazon.com/ec2/)で、RDS またはAuroraライターと同じサブネットに NLB を作成します。ポート`3306`に TCP リスナーを設定し、データベースエンドポイントにトラフィックを転送します。

    詳細な手順については、AWS ドキュメントの[ネットワークロードバランサーを作成する](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)参照してください。

2.  [Amazon VPCコンソール](https://console.aws.amazon.com/vpc/)で、左側のナビゲーションペインにある**「エンドポイントサービス」**をクリックし、エンドポイントサービスを作成します。セットアップ中に、前の手順で作成したNLBをバックエンドロードバランサーとして選択し、 **「エンドポイントの承認が必要」**オプションを有効にします。エンドポイントサービスを作成したら、後で使用するためにサービス名（ `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`形式）をコピーしておきます。

    詳細な手順については、AWS ドキュメントの[エンドポイントサービスを作成する](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)参照してください。

3.  オプション: 移行を開始する前に、同じ VPC または VNet 内の要塞またはクライアントからの接続をテストします。

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4.  後で、 TiDB Cloud DM を PrivateLink 経由で接続するように構成するときに、AWS コンソールに戻り、 TiDB Cloudからこのプライベートエンドポイントへの保留中の接続要求を承認する必要があります。

</details>

<details><summary>MySQL ソース データベース用の Azure PrivateLink とプライベート エンドポイントを設定する</summary>

Azure Database for MySQL - フレキシブル サーバーは、ネイティブのプライベート エンドポイントをサポートします。MySQL インスタンスの作成時にプライベート アクセス (VNet 統合) を有効にするか、後でプライベート エンドポイントを追加することができます。

新しいプライベート エンドポイントを追加するには、次の手順を実行します。

1.  [Azureポータル](https://portal.azure.com/)で、 **Azure Database for MySQL サーバー**を検索して選択し、インスタンス名をクリックして、左側のナビゲーション ウィンドウで**[設定]** &gt; **[ネットワーク]**をクリックします。

2.  **[ネットワーク]**ページで、 **[プライベート エンドポイント]**セクションまで下にスクロールし、 **[+ プライベート エンドポイントの作成**] をクリックして、画面の指示に従ってプライベート エンドポイントを設定します。

    セットアップ中は、「仮想**ネットワーク」**タブでTiDB Cloudがアクセスできる仮想ネットワークとサブネットを選択し、 **「DNS」**タブで**プライベートDNS統合を**有効のままにしておきます。プライベートエンドポイントが作成され、デプロイされたら、 **「リソースに移動」**をクリックし、左側のナビゲーションペインで**「設定」** &gt; **「DNS構成」**の順にクリックし、 **「顧客が参照できるFQDN」**セクションでインスタンスへの接続に使用するホスト名を見つけます。通常、ホスト名は`<your-instance-name>.mysql.database.azure.com`形式です。

    詳細な手順については、Azure ドキュメントの[プライベート リンク センター経由でプライベート エンドポイントを作成する](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-networking-private-link-portal#create-a-private-endpoint-via-private-link-center)参照してください。

3.  オプション: 移行を開始する前に、同じ VPC または VNet 内の要塞またはクライアントからの接続をテストします。

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4.  [Azureポータル](https://portal.azure.com/)で、MySQL Flexible Server インスタンス（プライベートエンドポイントオブジェクトではありません）の概要ページに戻り、 **「Essentials」**セクションの**「JSON ビュー」**をクリックして、後で使用するためにリソースIDをコピーします。リソースIDは`/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`形式です。このリソースID（プライベートエンドポイントIDではありません）を使用して、 TiDB Cloud DMを構成します。

5.  後で、PrivateLink 経由で接続するようにTiDB Cloud DM を構成するときに、Azure ポータルに戻り、 TiDB Cloudからこのプライベート エンドポイントへの保留中の接続要求を承認する必要があります。

</details>

#### VPCピアリング {#vpc-peering}

AWS VPC ピアリングまたは Google Cloud VPC ネットワーク ピアリングを使用する場合は、次の手順を参照してネットワークを構成してください。

<details><summary>AWS VPCピアリングを設定する</summary>

MySQL サービスが AWS VPC 内にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスター間の[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    受信ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)追加する必要があります。これにより、トラフィックがTiDBクラスタからMySQLインスタンスに流れるようになります。

3.  MySQL URL に DNS ホスト名が含まれている場合は、 TiDB Cloud がMySQL サービスのホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

</details>

<details><summary>Google Cloud VPC ネットワーク ピアリングを設定する</summary>

MySQL サービスが Google Cloud VPC 内にある場合は、次の手順を実行します。

1.  セルフホスト型MySQLの場合は、この手順をスキップして次のステップに進んでください。MySQLサービスがGoogle Cloud SQLの場合は、Google Cloud SQLインスタンスに関連付けられたVPCでMySQLエンドポイントを公開する必要があります。Googleが開発した[Cloud SQL 認証プロキシ](https://cloud.google.com/sql/docs/mysql/sql-proxy)を使用する必要があるかもしれません。

2.  MySQL サービスの VPC と TiDB クラスター間の[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

3.  MySQL が配置されている VPC の受信ファイアウォール ルールを変更します。

    入口ファイアウォールルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)追加する必要があります。これにより、TiDBクラスターからMySQLエンドポイントへのトラフィックが許可されます。

</details>

### 移行に必要な権限を付与する {#grant-required-privileges-for-migration}

移行を開始する前に、ソースデータベースとターゲットデータベースの両方で必要な権限を持つ適切なデータベースユーザーを設定する必要があります。これらの権限により、TiDB Cloud DMはMySQLからデータを読み取り、変更を複製し、 TiDB Cloudクラスタに安全に書き込むことができます。移行には、既存データの完全なデータダンプと増分変更のbinlogレプリケーションの両方が含まれるため、移行ユーザーには基本的な読み取りアクセスに加えて、特定の権限が必要です。

#### ソースMySQLデータベースの移行ユーザーに必要な権限を付与します {#grant-required-privileges-to-the-migration-user-in-the-source-mysql-database}

テスト目的で、ソース MySQL データベースで管理ユーザー ( `root`など) を使用できます。

本番ワークロードの場合、ソース MySQL データベースでのデータ ダンプとレプリケーション専用のユーザーを用意し、必要な権限のみを付与することをお勧めします。

| 特権                   | 範囲    | 目的                                |
| :------------------- | :---- | :-------------------------------- |
| `SELECT`             | テーブル  | すべてのテーブルからデータを読み取ることができます         |
| `RELOAD`             | グローバル | フルダンプ中に一貫したスナップショットを確保            |
| `REPLICATION SLAVE`  | グローバル | 増分レプリケーションのためのbinlogストリーミングを有効にする |
| `REPLICATION CLIENT` | グローバル | binlogの位置とサーバーのステータスへのアクセスを提供します  |

たとえば、ソース MySQL インスタンスで次の`GRANT`ステートメントを使用して、対応する権限を付与できます。

```sql
GRANT SELECT, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'dm_source_user'@'%';
```

#### ターゲットTiDB Cloudクラスタに必要な権限を付与する {#grant-required-privileges-in-the-target-tidb-cloud-cluster}

テスト目的で、 TiDB Cloudクラスターの`root`アカウントを使用できます。

本番ワークロードの場合、ターゲットTiDB Cloudクラスターにレプリケーション専用のユーザーを用意し、必要な権限のみを付与することをお勧めします。

| 特権            | 範囲          | 目的                        |
| :------------ | :---------- | :------------------------ |
| `CREATE`      | データベース、テーブル | ターゲットにスキーマオブジェクトを作成します    |
| `SELECT`      | テーブル        | 移行中にデータを検証する              |
| `INSERT`      | テーブル        | 移行されたデータを書き込む             |
| `UPDATE`      | テーブル        | 増分レプリケーション中に既存の行を変更します    |
| `DELETE`      | テーブル        | レプリケーションまたは更新中に行を削除します    |
| `ALTER`       | テーブル        | スキーマが変更されたときにテーブル定義を変更します |
| `DROP`        | データベース、テーブル | スキーマ同期中にオブジェクトを削除します      |
| `INDEX`       | テーブル        | インデックスを作成および変更する          |
| `CREATE VIEW` | ビュー         | 移行で使用するビューを作成する           |

たとえば、ターゲットのTiDB Cloudクラスターで次の`GRANT`ステートメントを実行して、対応する権限を付与できます。

```sql
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER, DROP, INDEX ON *.* TO 'dm_target_user'@'%';
```

## ステップ1: データ移行ページに移動します {#step-1-go-to-the-data-migration-page}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[移行]**をクリックします。

3.  **「データ移行」**ページで、右上隅の**「移行ジョブの作成」**をクリックします。 **「移行ジョブの作成」**ページが表示されます。

## ステップ2: ソース接続とターゲット接続を構成する {#step-2-configure-the-source-and-target-connections}

**「移行ジョブの作成」**ページで、ソース接続とターゲット接続を構成します。

1.  ジョブ名を入力してください。ジョブ名は文字で始まり、60文字未満である必要があります。文字（AZ、az）、数字（0-9）、アンダースコア（_）、ハイフン（-）が使用できます。

2.  ソース接続プロファイルを入力します。

    -   **データ ソース**: データ ソースの種類。
    -   **接続方法**: セキュリティ要件とクラウド プロバイダーに基づいて、データ ソースの接続方法を選択します。
        -   **パブリック IP** : すべてのクラウド プロバイダーで利用可能 (テストおよび概念実証の移行に推奨)。
        -   **プライベート リンク**: AWS および Azure でのみ使用可能 (プライベート接続を必要とする本番のワークロードに推奨)。
        -   **VPC ピアリング**: AWS と Google Cloud でのみ利用可能 (重複しない VPC/VNet CIDR を使用した低レイテンシのリージョン内接続を必要とする本番ワークロードに推奨)。
    -   選択した**接続方法**に基づいて、次の操作を実行します。
        -   **パブリック IP**または**VPC ピアリングを**選択した場合は、**ホスト名または IP アドレス**フィールドにデータ ソースのホスト名または IP アドレスを入力します。
        -   **プライベートリンク**を選択した場合は、次の情報を入力します。
            -   **エンドポイント サービス名**(**データ ソースが**AWS からのものである場合に使用可能): RDS またはAuroraインスタンス用に作成した VPC エンドポイント サービス名 (形式: `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx` ) を入力します。
            -   **プライベート エンドポイント リソース ID** (**データ ソース**が Azure からのものである場合に使用可能): MySQL フレキシブル サーバー インスタンスのリソース ID を入力します (形式: `/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>` )。
    -   **ポート**: データ ソースのポート。
    -   **ユーザー名**: データ ソースのユーザー名。
    -   **パスワード**: ユーザー名のパスワード。
    -   **SSL/TLS** : エンドツーエンドのデータ暗号化のために SSL/TLS を有効にします（すべての移行ジョブで強く推奨）。MySQL サーバーの SSL 設定に基づいて適切な証明書をアップロードしてください。

        SSL/TLS 構成オプション:

        -   オプション1: サーバー認証のみ

            -   MySQLサーバーがサーバー認証のみに構成されている場合は、 **CA 証明書**のみをアップロードします。
            -   このオプションでは、MySQLサーバーは自身の ID を証明するために証明書を提示し、 TiDB Cloud はCA に対してサーバー証明書を検証します。
            -   CA 証明書は中間者攻撃から保護するもので、MySQLサーバーが`require_secure_transport = ON`で起動されている場合に必要です。

        -   オプション2: クライアント証明書認証

            -   MySQLサーバーがクライアント証明書認証用に構成されている場合は、**クライアント証明書**と**クライアント秘密キー**をアップロードします。
            -   このオプションでは、 TiDB Cloud は認証のために MySQLサーバーに証明書を提示しますが、 TiDB Cloud はMySQL サーバーの証明書を検証しません。
            -   このオプションは通常、MySQLサーバーが`REQUIRE X509`なしで`REQUIRE SUBJECT '...'`や`REQUIRE ISSUER '...'`などのオプションで構成されている場合に使用されるため、クライアント証明書の完全な CA 検証を行わずにクライアント証明書の特定の属性をチェックできます。
            -   このオプションは、MySQLサーバーが自己署名またはカスタムPKI環境でクライアント証明書を受け入れる場合によく使用されます。この設定は中間者攻撃に対して脆弱であるため、他のネットワークレベルの制御によってサーバーの信頼性が保証されない限り、本番環境では推奨されません。

        -   オプション3: 相互TLS (mTLS) - 最高のセキュリティ

            -   MySQLサーバーが相互 TLS (mTLS) 認証用に構成されている場合は、 **CA 証明書**、**クライアント証明書**、および**クライアント秘密キー**をアップロードします。
            -   このオプションでは、MySQLサーバーはクライアント証明書を使用して TiDB Cloud の ID を検証し、 TiDB Cloud はCA 証明書を使用して MySQL サーバーの ID を検証します。
            -   このオプションは、MySQLサーバーに移行ユーザーに対して`REQUIRE X509`または`REQUIRE SSL`構成されている場合に必要です。
            -   このオプションは、MySQLサーバーが認証にクライアント証明書を必要とする場合に使用されます。
            -   証明書は次のソースから取得できます。
                -   クラウド プロバイダーからダウンロードします ( [TLS証明書リンク](#end-to-end-encryption-over-tlsssl)参照)。
                -   組織の内部 CA 証明書を使用します。
                -   自己署名証明書 (開発/テスト専用)。

3.  ターゲット接続プロファイルを入力します。

    -   **ユーザー名**: TiDB Cloudのターゲット クラスターのユーザー名を入力します。
    -   **パスワード**: TiDB Cloudユーザー名のパスワードを入力します。

4.  入力した情報を検証するには、 **「接続の検証」と「次へ」**をクリックします。

5.  表示されるメッセージに従ってアクションを実行します。

    -   接続方法として**パブリック IP**または**VPC ピアリングを**使用する場合は、データ移行サービスの IP アドレスをソース データベースとファイアウォール (存在する場合) の IP アクセス リストに追加する必要があります。
    -   接続方法として**Private Link**を使用する場合は、エンドポイント要求を受け入れるように求められます。
        -   AWS の場合: [AWS VPCコンソール](https://us-west-2.console.aws.amazon.com/vpc/home)に移動し、 **[エンドポイント サービス]**をクリックして、 TiDB Cloudからのエンドポイント要求を承認します。
        -   Azure の場合: [Azureポータル](https://portal.azure.com)に移動し、MySQL フレキシブル サーバーを名前で検索し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク] を**クリックし、右側の**[プライベート エンドポイント]**セクションを見つけて、 TiDB Cloudからの保留中の接続要求を承認します。

## ステップ3: 移行ジョブの種類を選択する {#step-3-choose-migration-job-type}

**移行するオブジェクトの選択**手順では、既存のデータの移行、増分データの移行、またはその両方を選択できます。

### 既存データと増分データを移行する {#migrate-existing-data-and-incremental-data}

データをTiDB Cloudに一度に移行するには、**既存のデータ移行**と**増分データ移行の**両方を選択します。これにより、ソース データベースとターゲット データベース間のデータの一貫性が確保されます。

**既存のデータ**と**増分データ**を移行するには、**物理モード**または**論理モード**を使用できます。

-   デフォルトモードは**論理モード**です。このモードでは、MySQLソースデータベースからデータをSQL文としてエクスポートし、TiDBで実行します。このモードでは、移行前のターゲットテーブルは空でも空でなくても構いません。ただし、パフォーマンスは物理モードよりも低くなります。

-   大規模なデータセットの場合は、**物理モード**の使用をお勧めします。このモードでは、MySQLソースデータベースからデータをエクスポートし、KVペアとしてエンコードしてTiKVに直接書き込むことで、パフォーマンスが向上します。このモードでは、移行前にターゲットテーブルが空である必要があります。16 RCU（レプリケーション容量ユニット）の仕様では、論理モードと比較して約2.5倍のパフォーマンスが得られます。その他の仕様では、論理モードと比較して20%から50%のパフォーマンス向上が期待できます。なお、パフォーマンスデータは参考値であり、シナリオによって異なる場合があります。

> **注記：**
>
> -   物理モードを使用する場合、既存のデータ移行が完了する前に、TiDB クラスターに対して 2 番目の移行ジョブまたはインポート タスクを作成することはできません。
> -   物理モードを使用し、移行ジョブが開始された場合は、PITR（ポイントインタイムリカバリ）を有効にしたり、クラスターで変更フィードを実行したり**しないで**ください。有効にすると、移行ジョブが停止します。PITRを有効にしたり、変更フィードを実行したりする必要がある場合は、論理モードを使用してデータを移行してください。

物理モードでは、MySQLソースデータを可能な限り高速にエクスポートするため、データエクスポート中にMySQLソースデータベースのQPSとTPSに[異なる仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)パフォーマンス影響が生じます。次の表は、各仕様におけるパフォーマンスの低下を示しています。

| 移行仕様   | 最大エクスポート速度  | MySQLソースデータベースのパフォーマンス低下 |
| ------ | ----------- | ------------------------ |
| 2台のRCU | 80.84 MiB/秒 | 15.6%                    |
| 4つのRCU | 214.2 MiB/秒 | 20.0%                    |
| 8 RCU  | 365.5 MiB/秒 | 28.9%                    |
| 16 RCU | 424.6 MiB/秒 | 46.7%                    |

### 既存のデータのみを移行する {#migrate-only-existing-data}

ソース データベースの既存のデータのみをTiDB Cloudに移行するには、**既存データの移行を**選択します。

既存のデータの移行には論理モードのみを使用できます。詳細については、 [既存データと増分データを移行する](#migrate-existing-data-and-incremental-data)参照してください。

### 増分データのみを移行する {#migrate-only-incremental-data}

ソースデータベースの増分データのみをTiDB Cloudに移行するには、 **「増分データ移行」**を選択します。この場合、移行ジョブはソースデータベースの既存データをTiDB Cloudに移行せず、移行ジョブで明示的に指定されたソースデータベースの進行中の変更のみを移行します。

増分データ移行の詳細な手順については、 [データ移行を使用して、MySQL 互換データベースからTiDB Cloudに増分データのみを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)参照してください。

## ステップ4: 移行するオブジェクトを選択する {#step-4-choose-the-objects-to-be-migrated}

1.  **「移行するオブジェクトの選択」**ページで、移行するオブジェクトを選択します。 **「すべて」**をクリックしてすべてのオブジェクトを選択するか、 **「カスタマイズ」**をクリックしてオブジェクト名の横にあるチェックボックスをクリックしてオブジェクトを選択します。

    -   **「すべて」**をクリックすると、移行ジョブはソースデータベースインスタンス全体から既存のデータをTiDB Cloudに移行し、移行完了後に進行中の変更も移行します。これは、前の手順で「**既存データの移行」**と**「増分データの移行」**のチェックボックスを選択した場合にのみ実行されることに注意してください。
    -   **「カスタマイズ」**をクリックしてデータベースを選択すると、移行ジョブは既存のデータと、選択したデータベースの進行中の変更をTiDB Cloudに移行します。これは、前の手順で「**既存データの移行」**と**「増分データの移行」**のチェックボックスを選択した場合にのみ実行されることに注意してください。
    -   **「カスタマイズ」**をクリックし、データセット名の下にあるテーブルをいくつか選択すると、移行ジョブは既存のデータと、選択したテーブルの進行中の変更のみを移行します。同じデータベース内に後から作成されたテーブルは移行されません。

2.  **「次へ」**をクリックします。

## ステップ5: 事前チェック {#step-5-precheck}

**「事前チェック」**ページでは、事前チェックの結果を確認できます。事前チェックに失敗した場合は、 **「失敗」**または**「警告」の**詳細に従って操作し、「再チェック」をクリックして**再チェック**してください。

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

## 移行ジョブ仕様のスケーリング {#scale-a-migration-job-specification}

TiDB Cloud は、さまざまなシナリオでのパフォーマンスとコストの要件を満たすために、移行ジョブ仕様のスケールアップまたはスケールダウンをサポートしています。

移行仕様によってパフォーマンスは異なります。また、移行段階によってパフォーマンス要件も変化する可能性があります。例えば、既存データの移行中は、パフォーマンスを可能な限り高速化したいため、8 RCUなど、より大きな仕様の移行ジョブを選択します。既存データの移行が完了すると、増分移行ではそれほど高いパフォーマンスは必要ないため、ジョブ仕様をスケールダウン（例えば、8 RCUから2 RCUへ）してコストを削減できます。

移行ジョブの仕様をスケーリングする場合は、次の点に注意してください。

-   移行ジョブ仕様のスケーリングには約 5 ～ 10 分かかります。
-   スケーリングが失敗した場合、ジョブ仕様はスケーリング前と同じままになります。

### 制限事項 {#limitations}

-   移行ジョブの仕様をスケーリングできるのは、ジョブが**実行**中または**一時停止中の**ステータスにある場合のみです。
-   TiDB Cloud は、既存のデータ エクスポート ステージでの移行ジョブ仕様のスケーリングをサポートしていません。
-   移行ジョブ仕様をスケーリングすると、ジョブが再起動されます。ジョブのソーステーブルに主キーがない場合、重複データが挿入される可能性があります。
-   スケーリング中は、ソースデータベースのバイナリログをパージしたり、MySQLソースデータベースの値を一時的に`expire_logs_days`増やしたりしないでください。そうしないと、連続したバイナリログの位置を取得できず、ジョブが失敗する可能性があります。

### スケーリング手順 {#scaling-procedure}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[移行]**をクリックします。

3.  **「データ移行」**ページで、スケールする移行ジョブを見つけます。 **「アクション」**列で、 **「...」** &gt; **「スケールアップ/ダウン」を**クリックします。

4.  **「スケールアップ/ダウン」**ウィンドウで、使用する新しい仕様を選択し、 **「送信」**をクリックします。ウィンドウの下部に、その仕様の新しい価格が表示されます。
