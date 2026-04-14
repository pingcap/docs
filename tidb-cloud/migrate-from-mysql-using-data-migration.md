---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: データ移行機能を使用して、Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL、またはセルフマネージドのMySQLインスタンスから、ダウンタイムを最小限に抑えながらMySQLデータベースをTiDB Cloudにシームレスに移行する方法を学びましょう。
aliases: ['/ja/tidbcloud/migrate-data-into-tidb','/ja/tidbcloud/migrate-incremental-data-from-mysql']
---

# データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する {#migrate-mysql-compatible-databases-to-tidb-cloud-using-data-migration}

このドキュメントでは、TiDB Cloud のデータ移行機能を使用して、Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL、またはセルフマネージド MySQL インスタンスから<CustomContent plan="dedicated">TiDB Cloud Dedicated</CustomContent> <CustomContent plan="essential">TiDB Cloud Essential</CustomContent>へ MySQL [TiDB Cloudコンソール](https://tidbcloud.com/)を移行する手順を説明します。

<CustomContent plan="essential">

> **注記：**
>
> 現在、 TiDB Cloud Essentialのデータ移行機能はベータ版です。

</CustomContent>

この機能により、既存のMySQLデータを移行し、MySQL互換のソースデータベースからTiDB Cloudへ進行中の変更（binlog）を継続的にレプリケートできます。これにより、同一リージョン内または異なるリージョン間でデータの一貫性が維持されます。合理化されたプロセスにより、個別のダンプおよびロード操作が不要になり、ダウンタイムが短縮され、MySQLからよりスケーラブルなプラットフォームへの移行が簡素化されます。

進行中のbinlogの変更を MySQL 互換データベースからTiDB Cloudにレプリケートするだけの場合は、 [データ移行を使用して、MySQL互換データベースからTiDB Cloudへ増分データを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)参照してください。

## 制限事項 {#limitations}

### 可用性 {#availability}

-   現在、 TiDB Cloud Starterではデータ移行機能は利用できません。

<CustomContent plan="dedicated">

-   [TiDB Cloudコンソール](https://tidbcloud.com/)にTiDB Cloud Dedicatedクラスターの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md#step-1-go-to-the-data-migration-page)エントリーが表示されない場合、その機能はお住まいの地域で利用できない可能性があります。お住まいの地域のサポートをリクエストするには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

-   Amazon Aurora MySQL ライターインスタンスは、既存データ移行と増分データ移行の両方をサポートします。Amazon Aurora MySQL リーダーインスタンスは、既存データ移行のみをサポートし、増分データ移行はサポートしません。

### 移行ジョブの最大数 {#maximum-number-of-migration-jobs}

<CustomContent plan="dedicated">

TiDB Cloud Dedicatedクラスターでは、組織ごとに最大 200 個の移行ジョブを作成できます。さらに移行ジョブを作成するには、[サポートチケットを提出する](/tidb-cloud/tidb-cloud-support.md)必要があります。

</CustomContent>
<CustomContent plan="essential">

TiDB Cloud Essentialインスタンスでは、組織ごとに最大 100 個の移行ジョブを作成できます。さらに移行ジョブを作成するには、[サポートチケットを提出する](/tidb-cloud/tidb-cloud-support.md)必要があります。

</CustomContent>

### フィルタリングおよび削除されたデータベース {#filtered-out-and-deleted-databases}

-   システムデータベースは、移行するデータベースをすべて選択した場合でも、フィルタリングされてTiDB Cloudに移行されません。つまり、 `mysql` 、 `information_schema` 、 `performance_schema` 、および`sys`は、この機能を使用して移行されません。

<CustomContent plan="dedicated">

-   TiDB CloudでTiDB Cloud Dedicatedクラスタを削除すると、そのクラスタ内のすべての移行ジョブが自動的に削除され、復元できなくなります。

</CustomContent>

<CustomContent plan="essential">

### Alibaba Cloud RDSの制限事項 {#limitations-of-alibaba-cloud-rds}

Alibaba Cloud RDSをデータソースとして使用する場合、すべてのテーブルに明示的な主キーが必要です。主キーのないテーブルの場合、RDSはbinlogに非表示の主キーを追加しますが、これによりソーステーブルとのスキーマの不一致が発生し、移行が失敗します。

### Alibaba Cloud PolarDB-Xの制限事項 {#limitations-of-alibaba-cloud-polardb-x}

完全なデータ移行中に、PolarDB-Xのスキーマに下流のデータベースと互換性のないキーワードが含まれている場合、インポートが失敗する可能性があります。

これを防ぐには、移行プロセスを開始する前に、下流データベースにターゲットテーブルを作成してください。

</CustomContent>

### 既存のデータ移行の限界 {#limitations-of-existing-data-migration}

-   既存データの移行中に、移行対象のテーブルが移行先のデータベースに既に存在し、かつ重複するキーがある場合、重複するキーを持つ行は置き換えられます。

<CustomContent plan="dedicated">

-   TiDB Cloud Dedicatedの場合、データセット サイズが 1 TiB より小さい場合は、論理モード (デフォルト モード) を使用することをお勧めします。データセットのサイズが 1 TiB より大きい場合、または既存のデータをより速く移行したい場合は、物理モードを使用できます。詳細については、[既存データと増分データを移行する](#migrate-existing-data-and-incremental-data)参照してください。

</CustomContent>
<CustomContent plan="essential">

-   TiDB Cloud Essentialでは、現在、データ移行には論理モードのみがサポートされています。このモードでは、MySQLソースデータベースからSQLステートメントとしてデータをエクスポートし、TiDB上で実行します。このモードでは、移行前のターゲットテーブルは空でも空でなくても構いません。

</CustomContent>

### 増分データ移行の限界 {#limitations-of-incremental-data-migration}

-   増分データ移行中に、移行対象のテーブルが既にターゲットデータベースに重複キーで存在する場合、エラーが報告され、移行が中断されます。この場合、MySQLソースデータが正確であることを確認する必要があります。正確であれば、移行ジョブの**「再開」**ボタンをクリックすると、移行ジョブはターゲット<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>で競合するレコードをMySQLソースレコードに置き換えます。

<CustomContent plan="essential">

-   増分データ移行 (進行中の変更をTiDB Cloud Essentialインスタンスに移行する) 中に、移行ジョブが突然のエラーから回復した場合、60 秒間セーフ モードが開くことがあります。セーフ モード中は、 `INSERT`ステートメントが`REPLACE`として、 `UPDATE`ステートメントが`DELETE`および`REPLACE`として移行され、その後、これらのトランザクションがターゲットのTiDB Cloud Essentialインスタンスに移行され、突然のエラー中に発生したすべてのデータがターゲットのTiDB Cloud Essentialインスタンスにスムーズに移行されたことが保証されます。このシナリオでは、プライマリキーまたはNULL以外の一意インデックスを持たないMySQLソーステーブルの場合、データがターゲットのTiDB Cloud Essentialインスタンスに繰り返し挿入される可能性があるため、一部のデータがターゲットのTiDB Cloud Essentialインスタンスで重複する可能性があります。

</CustomContent>
<CustomContent plan="dedicated">

-   増分データ移行 (進行中の変更をTiDB Cloud Dedicatedクラスターに移行する) 中に、移行ジョブが突然のエラーから回復した場合、60 秒間セーフ モードが開くことがあります。セーフ モード中は、 `INSERT`ステートメントが`REPLACE`として、 `UPDATE`ステートメントが`DELETE`および`REPLACE`として移行され、その後、これらのトランザクションがターゲットのTiDB Cloud Dedicatedクラスターに移行され、突然のエラー中に発生したすべてのデータがターゲットのTiDB Cloud Dedicatedクラスターにスムーズに移行されたことが保証されます。このシナリオでは、プライマリキーやNULL値を含まない一意インデックスを持たないMySQLソーステーブルの場合、データがターゲットのTiDB Cloud Dedicatedクラスタに繰り返し挿入される可能性があるため、一部のデータがターゲットのTiDB Cloud Dedicatedクラスタで重複する可能性があります。

-   以下のシナリオでは、移行ジョブに24時間以上かかる場合、ソースデータベースのバイナリログを削除しないでください。これにより、データ移行ツールは増分データ移行のために連続したバイナリログを取得できます。

    -   既存のデータ移行中に。
    -   既存のデータ移行が完了し、増分データ移行が初めて開始された後、レイテンシーは0msになりません。

</CustomContent>

## 前提条件 {#prerequisites}

移行する前に、データソースがサポートされているかどうかを確認し、MySQL互換データベースでバイナリログを有効にし、ネットワーク接続を確保し、ソースデータベースとターゲット<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>とTiDB Cloud Essentialの両方に必要な権限を付与してください<CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>データベース。

### データソースとバージョンがサポートされていることを確認してください。 {#make-sure-your-data-source-and-version-are-supported}

<CustomContent plan="dedicated">

TiDB Cloud Dedicated のデータ移行機能は、以下のデータソースとバージョンをサポートしています。

| データソース                             | サポートされているバージョン |
| :--------------------------------- | :------------- |
| 自己管理型MySQL（オンプレミスまたはパブリッククラウド）     | 8.0、5.7、5.6    |
| Amazon Aurora MySQL                | 8.0、5.7、5.6    |
| Amazon RDS MySQL                   | 8.0、5.7        |
| Azure Database for MySQL - 柔軟なサーバー | 8.0、5.7        |
| Google Cloud SQL for MySQL         | 8.0、5.7、5.6    |
| Alibaba Cloud RDS MySQL            | 8.0、5.7        |

</CustomContent>
<CustomContent plan="essential">

TiDB Cloud Essentialのデータ移行機能は、以下のデータソースとバージョンをサポートしています。

| データソース                             | サポートされているバージョン |
| :--------------------------------- | :------------- |
| 自己管理型MySQL（オンプレミスまたはパブリッククラウド）     | 8.0、5.7        |
| Amazon Aurora MySQL                | 8.0、5.7        |
| Amazon RDS MySQL                   | 8.0、5.7        |
| Alibaba Cloud RDS MySQL            | 8.0、5.7        |
| Azure Database for MySQL - 柔軟なサーバー | 8.0、5.7        |
| Google Cloud SQL for MySQL         | 8.0、5.7        |

</CustomContent>

### レプリケーションのために、ソースのMySQL互換データベースでバイナリログを有効にする {#enable-binary-logs-in-the-source-mysql-compatible-database-for-replication}

DM を使用して、ソースの MySQL 互換データベースからターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>に増分変更を継続的にレプリケートするには、ソース データベースでバイナリ ログを有効にするために次の構成が必要です。

| コンフィグレーション                       | 必要値                              | なぜ                                        |
| :------------------------------- | :------------------------------- | :---------------------------------------- |
| `log_bin`                        | `ON`                             | DMがTiDBへの変更を複製するために使用するバイナリログを有効にします。     |
| `binlog_format`                  | `ROW`                            | すべてのデータ変更を正確に記録します（他の形式では例外的なケースを見落とします）。 |
| `binlog_row_image`               | `FULL`                           | 安全な紛争解決のために、イベントにすべての列値が含まれます。            |
| `binlog_expire_logs_seconds`     | ≥ `86400` （1日）、 `604800` （7日、推奨） | 移行中にDMが連続ログにアクセスできるようにします                 |
| `binlog_transaction_compression` | `OFF`                            | DMはトランザクション圧縮をサポートしていません                  |

#### 現在の値を確認し、ソースのMySQLインスタンスを設定します。 {#check-current-values-and-configure-the-source-mysql-instance}

現在の設定を確認するには、ソースのMySQLインスタンスに接続し、次のステートメントを実行します。

```sql
SHOW VARIABLES WHERE Variable_name IN
('log_bin','server_id','binlog_format','binlog_row_image',
'binlog_expire_logs_seconds','expire_logs_days','binlog_transaction_compression');
```

必要に応じて、ソースのMySQLインスタンスの設定を変更して、必要な値と一致するようにしてください。

<details><summary>自己管理型MySQLインスタンスを構成する</summary>

1.  `/etc/my.cnf`を開いて、以下を追加します。

        [mysqld]
        log_bin = mysql-bin
        binlog_format = ROW
        binlog_row_image = FULL
        binlog_expire_logs_seconds = 604800   # 7 days retention
        binlog_transaction_compression = OFF

2.  変更を適用するには、MySQLサービスを再起動してください。

        sudo systemctl restart mysqld

3.  設定が有効になっていることを確認するには、 `SHOW VARIABLES`ステートメントを再度実行してください。

詳細な手順については、MySQL ドキュメントの[MySQLサーバーのシステム変数](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html)および[バイナリログ](https://dev.mysql.com/doc/refman/8.0/en/binary-log.html)を参照してください。

</details>

<details><summary>AWS RDSまたはAurora MySQLの設定</summary>

1.  AWS マネジメント コンソールで、 [Amazon RDS コンソール](https://console.aws.amazon.com/rds/)を開き、左側のナビゲーション ペインで**[パラメータ グループ]**をクリックし、カスタム パラメータ グループを作成または編集します。
2.  上記の4つのパラメータを必要な値に設定してください。
3.  パラメータグループをインスタンスまたはクラスターにアタッチし、再起動して変更を適用してください。
4.  再起動後、インスタンスに接続し、 `SHOW VARIABLES`ステートメントを実行して構成を確認します。

詳細な手順については、AWS ドキュメントの[DBパラメータグループの操作](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html)と[MySQLバイナリログの設定](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)参照してください。

</details>

<details><summary>Azure Database for MySQL の構成 - Flexible Server</summary>

1.  [Azureポータル](https://portal.azure.com/)で、 **Azure Database for MySQL サーバー**を検索して選択し、インスタンス名をクリックしてから、左側のナビゲーション ペインで**[設定]** &gt; **[サーバー パラメーター]**をクリックします。

2.  各パラメータを検索し、その値を更新します。

    ほとんどの変更は再起動なしで反映されます。再起動が必要な場合は、ポータルから通知が表示されます。

3.  `SHOW VARIABLES`ステートメントを実行して、設定を確認します。

詳細な手順については、Microsoft Azure ドキュメントの[Azure ポータルを使用して、Azure Database for MySQL - Flexible Server でサーバーパラメーターを構成する](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-configure-server-parameters-portal)参照してください。

</details>

<details><summary>Google Cloud SQL for MySQL の設定</summary>

1.  [Google Cloud Console](https://console.cloud.google.com/project/_/sql/instances)で、インスタンスを含むプロジェクトを選択し、インスタンス名をクリックして、 **[編集]**をクリックします。
2.  必要なフラグ ( `log_bin` 、 `binlog_format` 、 `binlog_row_image` 、 `binlog_expire_logs_seconds` ) を追加または変更します。
3.  **「保存」**をクリックしてください。再起動が必要な場合は、コンソールからメッセージが表示されます。
4.  再起動後、 `SHOW VARIABLES`ステートメントを実行して変更を確認します。

詳細な手順については、Google Cloud ドキュメントの[データベースフラグを設定する](https://cloud.google.com/sql/docs/mysql/flags)と[特定時点へのリカバリを使用する](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr)ご覧ください。

</details>

<details><summary>Alibaba Cloud RDS MySQL の設定</summary>

1.  [ApsaraDB RDSコンソール](https://rds.console.aliyun.com/)で、インスタンスのリージョンを選択し、RDS for MySQL インスタンスの ID をクリックします。

2.  左側のナビゲーションペインで**「パラメーター」**をクリックし、各パラメーターを検索して、次の値を設定します。

    -   `binlog_row_image` : `FULL`

3.  左側のナビゲーション ペインで、 **[バックアップと復元]**をクリックし、 **[バックアップ戦略]**を選択します。移行中に DM が連続するbinlogファイルにアクセスできるようにするには、バックアップ戦略を次の制約で構成します。

    -   保存期間：最低3日間（推奨7日間）に設定してください。

    -   保持ファイル: 古いログが時期尚早に上書きされないように、「最大ファイル数」が十分であることを確認してください。

    -   ストレージ保護：ストレージの使用状況を綿密に監視してください。ディスク容量の使用量がシステムしきい値に達すると、保持期間の設定に関わらず、RDSは最も古いバイナリログを自動的に削除しますのでご注意ください。

4.  変更を適用した後（必要に応じて再起動した後）、インスタンスに接続し、このセクションの`SHOW VARIABLES`ステートメントを実行して構成を確認します。

詳細については、 [インスタンスパラメータを設定します](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/modify-the-parameters-of-an-apsaradb-rds-for-mysql-instance)参照してください。

</details>

### ネットワーク接続を確保する {#ensure-network-connectivity}

移行ジョブを作成する前に、ソース MySQL インスタンス、 TiDB Cloudデータ マイグレーション (DM) サービス、およびターゲット<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>の間の適切なネットワーク接続を計画し、設定する必要があります。

<CustomContent plan="dedicated">

TiDB Cloud Dedicatedで利用可能な接続方法は以下のとおりです。

| 接続方法                      | 可用性                             | 推奨対象                                           |
| :------------------------ | :------------------------------ | :--------------------------------------------- |
| 公開エンドポイントまたはIPアドレス        | TiDB Cloudがサポートするすべてのクラウドプロバイダー | 迅速な概念実証移行、テスト、またはプライベート接続が利用できない場合             |
| プライベートリンクまたはプライベートエンドポイント | AWSとAzureのみ                     | データをパブリックインターネットに公開することなく、本番環境のワークロードを実行する     |
| VPCピアリング                  | AWSとGoogle Cloudのみ              | 低遅延でリージョン内接続が必要であり、VPC/VNet CIDRが重複しない本番ワークロード |

</CustomContent>
<CustomContent plan="essential">

TiDB Cloud Essentialで利用可能な接続方法は以下のとおりです。

| 接続方法                      | 可用性                             | 推奨対象                                       |
| :------------------------ | :------------------------------ | :----------------------------------------- |
| 公開エンドポイントまたはIPアドレス        | TiDB Cloudがサポートするすべてのクラウドプロバイダー | 迅速な概念実証移行、テスト、またはプライベート接続が利用できない場合         |
| プライベートリンクまたはプライベートエンドポイント | AWSとAlibaba Cloudのみ             | データをパブリックインターネットに公開することなく、本番環境のワークロードを実行する |

</CustomContent>

ご利用のクラウドプロバイダー、ネットワーク構成、およびセキュリティ要件に最適な接続方法を選択し、その方法の設定手順に従ってください。

#### TLS/SSLによるエンドツーエンド暗号化 {#end-to-end-encryption-over-tls-ssl}

接続方法に関わらず、エンドツーエンド暗号化にはTLS/SSLの使用を強く推奨します。プライベートエンドポイント<CustomContent plan="dedicated">およびVPCピアリング</CustomContent>ネットワークパスを保護しますが、TLS/SSLはデータ自体を保護し、コンプライアンス要件を満たすのに役立ちます。

<details><summary>TLS/SSL暗号化接続用のクラウドプロバイダーの証明書をダウンロードして保存する</summary>

-   Amazon Aurora MySQL または Amazon RDS MySQL: [SSL/TLSを使用してDBインスタンスまたはクラスタへの接続を暗号化する](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html)
-   Azure Database for MySQL - フレキシブル サーバー: [暗号化された接続で接続します](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl)
-   Google Cloud SQL for MySQL: [SSL/TLS証明書の管理](https://cloud.google.com/sql/docs/mysql/manage-ssl-instance)
-   Alibaba Cloud RDS MySQL: [SSL暗号化機能を設定する](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/configure-a-cloud-certificate-to-enable-ssl-encryption)

</details>

#### 公開エンドポイントまたはIPアドレス {#public-endpoints-or-ip-addresses}

パブリックエンドポイントを使用する場合、ネットワーク接続とアクセスは、DMジョブ作成プロセス中、現在と後の両方で確認できます。TiDB Cloudは、その時点で特定の送信IPアドレスと指示を提供します。

<CustomContent plan="dedicated">

> **注記**：
>
> ファイアウォールの送信側IPアドレス範囲は、データ移行タスクの作成時にのみ利用可能です。このIPアドレス範囲を事前に取得することはできません。開始する前に、以下の点を確認してください。
>
> -   ファイアウォールルールを変更する権限が必要です。
> -   セットアッププロセス中に、クラウドプロバイダーのコンソールにアクセスできます。
> -   タスク作成ワークフローを一時停止して、ファイアウォールを設定できます。

</CustomContent>

1.  ソースとなるMySQLインスタンスのエンドポイントホスト名（FQDN）またはパブリックIPアドレスを特定し、記録します。

2.  データベースのファイアウォールまたはセキュリティグループのルールを変更するには、必要な権限が付与されていることを確認してください。詳細については、クラウドプロバイダーのドキュメントを参照してください。

    -   Amazon Aurora MySQL または Amazon RDS MySQL: [セキュリティグループによるアクセス制御](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Overview.RDSSecurityGroups.html)。
    -   Azure Database for MySQL - フレキシブル サーバー: [公共ネットワークアクセス](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-networking-public)
    -   Google Cloud SQL for MySQL: [認証済みネットワーク](https://cloud.google.com/sql/docs/mysql/configure-ip?__hstc=86493575.39bd75fe158e3a694e276e9709c7bc82.1766498597248.1768349165136.1768351956126.50&#x26;__hssc=86493575.1.1768351956126&#x26;__hsfp=3e9153f1372737b813f3fefb5bbb2ddf#authorized-networks)。

3.  オプション：適切な証明書を使用して転送中の暗号化を行い、パブリックインターネットアクセスを備えたマシンからソースデータベースへの接続を確認します。

    ```shell
    mysql -h <public-host> -P <port> -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4.  後ほど、データ移行ジョブの設定時に、 TiDB Cloud送信元IPアドレス範囲が提供されます。その際、上記と同じ手順に従って、このIPアドレス範囲をデータベースのファイアウォールまたはセキュリティグループのルールに追加する必要があります。

#### プライベートリンクまたはプライベートエンドポイント {#private-link-or-private-endpoint}

<CustomContent plan="dedicated">

プロバイダーネイティブのプライベートリンクまたはプライベートエンドポイントを使用する場合は、ソースのMySQLインスタンス（RDS、 Aurora、またはAzure Database for MySQL）用のプライベートエンドポイントを作成します。

<details><summary>MySQLソースデータベース用にAWS PrivateLinkとプライベートエンドポイントを設定します。</summary>

AWS は RDS またはAuroraへの PrivateLink による直接アクセスをサポートしていません。そのため、ネットワークロードバランサー (NLB) を作成し、それをソース MySQL インスタンスに関連付けられたエンドポイントサービスとして公開する必要があります。

1.  [Amazon EC2 コンソール](https://console.aws.amazon.com/ec2/)で RDS またはAuroraライターと同じサブネットに NLB を作成します。NLB を、データベースエンドポイントにトラフィックを転送するポート`3306`の TCP リスナーで構成します。

    詳細な手順については、AWS ドキュメントの[ネットワークロードバランサーを作成する](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)参照してください。

2.  [Amazon VPC コンソール](https://console.aws.amazon.com/vpc/)で、左側のナビゲーション ペインの**[エンドポイント サービス]**をクリックし、エンドポイント サービスを作成します。セットアップ中に、前の手順で作成した NLB をバックエンド ロード バランサーとして選択し、[**エンドポイントの承認を必須にする]**オプションを有効にします。エンドポイント サービスが作成されたら、後で使用するためにサービス名 ( `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`形式) をコピーします。

    詳細な手順については、AWS ドキュメントの[エンドポイントサービスを作成します](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)参照してください。

3.  オプション：移行を開始する前に、同じVPCまたはVNet内の踏み台サーバーまたはクライアントから接続テストを実施してください。

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4.  後ほど、 TiDB Cloud DMをPrivateLink経由で接続するように設定する際には、AWSコンソールに戻り、 TiDB Cloudからこのプライベートエンドポイントへの保留中の接続要求を承認する必要があります。

</details>

<details><summary>Azure PrivateLink と MySQL ソース データベース用のプライベート エンドポイントを設定します。</summary>

Azure Database for MySQL - Flexible Server は、ネイティブのプライベートエンドポイントをサポートしています。MySQL インスタンスの作成時にプライベートアクセス (VNet 統合) を有効にするか、後からプライベートエンドポイントを追加することができます。

新しいプライベートエンドポイントを追加するには、以下の手順を実行してください。

1.  [Azureポータル](https://portal.azure.com/)で、 **「Azure Database for MySQL サーバー」**を検索して選択し、インスタンス名をクリックしてから、左側のナビゲーション ペインで**「設定」** &gt; **「ネットワーク」**をクリックします。

2.  **ネットワーク設定**ページで、**プライベートエンドポイントの**セクションまでスクロールダウンし、 **「+ プライベートエンドポイントの作成」**をクリックして、画面の指示に従ってプライベートエンドポイントを設定します。

    セットアップ中に、[仮想**ネットワーク]**タブでTiDB Cloud がアクセスできる仮想ネットワークとサブネットを選択し、 **[DNS]**タブで**[プライベート DNS 統合] を**有効にします。プライベートエンドポイントが作成されてデプロイされたら、 **[リソースに移動] を**クリックし、左側のナビゲーション ペインで**[設定]** &gt; **[DNS 構成] を**クリックして、[**顧客可視 FQDN]**セクションでインスタンスへの接続に使用するホスト名を見つけます。通常、ホスト名は`<your-instance-name>.mysql.database.azure.com`形式です。

    詳細な手順については、Azure ドキュメントの[プライベートリンクセンターを使用してプライベートエンドポイントを作成します。](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-networking-private-link-portal#create-a-private-endpoint-via-private-link-center)参照してください。

3.  オプション：移行を開始する前に、同じVPCまたはVNet内の踏み台サーバーまたはクライアントから接続テストを実施してください。

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4.  [Azureポータル](https://portal.azure.com/)の で、MySQL Flexible Server インスタンスの概要ページ (プライベート エンドポイント オブジェクトではありません) に戻り、 **[Essentials]**セクションで**[JSON ビュー]**をクリックして、後で使用するためにリソース ID をコピーします。リソース ID は`/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`形式です。このリソース ID (プライベート エンドポイント ID ではありません) を使用して、 TiDB Cloud DM を構成します。

5.  後ほど、 TiDB Cloud DMをPrivateLink経由で接続するように構成する際には、Azureポータルに戻り、 TiDB Cloudからこのプライベートエンドポイントへの保留中の接続要求を承認する必要があります。

</details>

</CustomContent>
<CustomContent plan="essential">

プロバイダーネイティブのプライベート リンクまたはプライベート エンドポイントを使用する場合は、ソース MySQL インスタンスに対して[プライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)作成します。

</CustomContent>

<CustomContent plan="dedicated">

#### VPCピアリング {#vpc-peering}

AWS VPCピアリングまたはGoogle Cloud VPCネットワークピアリングを使用する場合は、以下の手順に従ってネットワークを設定してください。

<details><summary>AWS VPCピアリングの設定</summary>

MySQLサービスがAWS VPC内にある場合は、以下の手順を実行してください。

1.  VPC ピアリング接続を MySQL サービスの VPC と<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>クラスター<CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>の間で[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)。

2.  MySQLサービスが関連付けられているセキュリティグループの受信ルールを変更します。

    <CustomContent plan="dedicated">

    [TiDB Cloud Dedicatedクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)受信ルールに追加する必要があります。これにより、 TiDB Cloud Dedicatedクラスターから MySQL インスタンスにトラフィックが流れるようになります。

    </CustomContent>

    <CustomContent plan="essential">

    [TiDB Cloud Essentialインスタンスが配置されているリージョンのCIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)ルールに追加する必要があります。これにより、トラフィックがTiDB Cloud Essentialインスタンスから MySQL インスタンスに流れるようになります。

    </CustomContent>

3.  MySQLのURLにDNSホスト名が含まれている場合、 TiDB CloudがMySQLサービスのホスト名を解決できるようにする必要があります。

    1.  [VPCピアリング接続のDNS解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **アクセプターDNS解決**オプションを有効にする。

</details>

<details><summary>Google Cloud VPCネットワークピアリングの設定</summary>

MySQLサービスがGoogle Cloud VPC内にある場合は、以下の手順を実行してください。

1.  セルフホスト型のMySQLの場合は、この手順をスキップして次の手順に進んでください。MySQLサービスがGoogle Cloud SQLの場合は、Google Cloud SQLインスタンスに関連付けられたVPCにMySQLエンドポイントを公開する必要があります。Googleが開発した[Cloud SQL認証プロキシ](https://cloud.google.com/sql/docs/mysql/sql-proxy)使用する必要があるかもしれません。

2.  MySQL サービスの VPC とTiDB Cloud Dedicatedクラスターの間で[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)。

3.  MySQLが配置されているVPCの受信ファイアウォールルールを変更します。

    <CustomContent plan="dedicated">

    [TiDB Cloud Dedicatedクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)イングレス ファイアウォール ルールに追加する必要があります。これにより、トラフィックがTiDB Cloud Dedicatedクラスターから MySQL エンドポイントに流れることが可能になります。

    </CustomContent>

    <CustomContent plan="essential">

    [TiDB Cloud Essentialインスタンスが配置されているリージョンのCIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)イングレス ファイアウォール ルールに追加する必要があります。これにより、トラフィックがTiDB Cloud Essentialインスタンスから MySQL エンドポイントに流れることが可能になります。

    </CustomContent>

</details>

</CustomContent>

### 移行に必要な権限を付与する {#grant-required-privileges-for-migration}

移行を開始する前に、ソースデータベースとターゲットデータベースの両方で、必要な権限を持つ適切なデータベースユーザーを設定する必要があります。これらの権限、 TiDB Cloud DM は MySQL からデータを読み取り、変更を複製し、 <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>に安全に書き込むことができます。移行には、既存データの完全なデータダンプと増分変更のbinlog複製の両方が含まれるため、移行ユーザーには基本的な読み取りアクセス以外の特定の権限が必要です。

#### ソースMySQLデータベースで、移行ユーザーに必要な権限を付与します。 {#grant-required-privileges-to-the-migration-user-in-the-source-mysql-database}

テスト目的では、ソースの MySQL データベースで管理者ユーザー ( `root`など) を使用できます。

本番のワークロードでは、ソースのMySQLデータベースにデータダンプとレプリケーション専用のユーザーを用意し、必要な権限のみを付与することをお勧めします。

| 特権                   | 範囲    | 目的                             |
| :------------------- | :---- | :----------------------------- |
| `SELECT`             | 表     | すべてのテーブルからデータを読み取ることができます      |
| `RELOAD`             | グローバル | フルダンプ中に一貫性のあるスナップショットを保証します    |
| `REPLICATION SLAVE`  | グローバル | 増分データ移行のためのbinlogストリーミングを有効にする |
| `REPLICATION CLIENT` | グローバル | binlogの位置とサーバーの状態へのアクセスを提供します  |

例えば、ソースのMySQLインスタンスで次の`GRANT`ステートメントを使用すると、対応する権限を付与できます。

```sql
GRANT SELECT, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'dm_source_user'@'%';
```

#### 対象に必要な権限を付与する<customcontent plan="dedicated">TiDB Cloud Dedicatedクラスター</customcontent><customcontent plan="essential">TiDB Cloud Essentialインスタンス</customcontent> {#grant-required-privileges-in-the-target-customcontent-plan-dedicated-tidb-cloud-dedicated-cluster-customcontent-customcontent-plan-essential-tidb-cloud-essential-instance-customcontent}

テスト目的では、 <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>インスタンスの`root`アカウントを使用できます。

本番ワークロードの場合は、ターゲット<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>でレプリケーション専用のユーザーを用意し、必要な権限のみを付与することをお勧めします。

| 特権            | 範囲          | 目的                      |
| :------------ | :---------- | :---------------------- |
| `CREATE`      | データベース、テーブル | ターゲットにスキーマオブジェクトを作成します  |
| `SELECT`      | 表           | 移行中にデータを検証する            |
| `INSERT`      | 表           | 移行されたデータを書き込む           |
| `UPDATE`      | 表           | 増分データ移行中に既存の行を変更します     |
| `DELETE`      | 表           | レプリケーションまたは更新中に行を削除します  |
| `ALTER`       | 表           | スキーマ変更時にテーブル定義を修正します    |
| `DROP`        | データベース、テーブル | スキーマ同期中にオブジェクトを削除します    |
| `INDEX`       | 表           | インデックスを作成および変更します       |
| `CREATE VIEW` | 閲覧数         | マイグレーションで使用されるビューを作成します |

たとえば、ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>インスタンスで次の`GRANT`ステートメントを実行して、対応する権限を付与できます。

```sql
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER, DROP, INDEX ON *.* TO 'dm_target_user'@'%';
```

## ステップ1：データ移行ページに移動します {#step-1-go-to-the-data-migration-page}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

2.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>の名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[データ移行]**をクリックします。

3.  **データ移行**ページで、右上隅にある**「移行ジョブの作成」**をクリックします。**移行ジョブの作成**ページが表示されます。

## ステップ2：ソース接続とターゲット接続を設定する {#step-2-configure-the-source-and-target-connections}

**「移行ジョブの作成」**ページで、ソースとターゲットの接続を設定します。

1.  職名を入力してください。職名は文字で始まり、60文字以内である必要があります。文字（AZ、az）、数字（0～9）、アンダースコア（_）、ハイフン（-）が使用可能です。

2.  ソース接続プロファイルを入力してください。

    -   **データソース**：データソースの種類。

    <CustomContent plan="dedicated">

    -   **接続方法**：セキュリティ要件とクラウドプロバイダーに基づいて、データソースの接続方法を選択してください。

        -   **パブリックIP** ：すべてのクラウドプロバイダーで利用可能（テストおよび概念実証移行に推奨）。
        -   **プライベートリンク**：AWSおよびAzureでのみ利用可能（プライベート接続を必要とする本番ワークロードに推奨）。
        -   **VPCピアリング**：AWSとGoogle Cloudでのみ利用可能です（低遅延でリージョン内接続が必要で、VPC/VNet CIDRが重複しない本番ロードに推奨されます）。

    </CustomContent>
    <CustomContent plan="essential">

    -   **接続方法**：セキュリティ要件とクラウドプロバイダーに基づいて、データソースの接続方法を選択してください。

        -   **公開**：すべてのクラウドプロバイダーで利用可能（テストおよび概念実証のための移行に推奨）。
        -   **プライベートリンク**：AWSおよびAlibaba Cloudでのみ利用可能です（プライベート接続を必要とする本番のワークロードに推奨）。

    </CustomContent>

    <CustomContent plan="dedicated">

    -   選択した**接続方法**に基づいて、以下の手順を実行してください。

        -   **パブリックIP**または**VPCピアリングを**選択した場合は、**ホスト名またはIPアドレスの**フィールドにデータソースのホスト名またはIPアドレスを入力してください。
        -   **「プライベートリンク」**を選択した場合は、以下の情報を入力してください。
            -   **エンドポイント サービス名**(**データ ソースが**AWS の場合に利用可能): RDS またはAuroraインスタンス用に作成した VPC エンドポイント サービス名 (形式: `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx` ) を入力します。
            -   **プライベートエンドポイントリソースID** （**データソース**がAzureの場合に利用可能）：MySQL Flexible ServerインスタンスのリソースIDを入力します（形式： `/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>` ）。

    </CustomContent>
    <CustomContent plan="essential">

    -   選択した**接続方法**に基づいて、以下の手順を実行してください。

        -   **「公開」**を選択した場合は、 **「ホスト名またはIPアドレス」**フィールドにデータソースのホスト名またはIPアドレスを入力してください。
        -   **[プライベート リンク]**が選択されている場合は、[プライベートリンク[プライベートリンクまたはプライベートエンドポイント](#private-link-or-private-endpoint)セクションで作成したプライベート リンク接続を選択します。

    </CustomContent>

    -   **ポート**：データソースのポート番号。
    -   **ユーザー名**：データソースのユーザー名。
    -   **パスワード**：ユーザー名のパスワード。
    -   **SSL/TLS** ：エンドツーエンドのデータ暗号化のためにSSL/TLSを有効にします（すべての移行作業で強く推奨）。MySQLサーバーのSSL構成に基づいて、適切な証明書をアップロードしてください。

        SSL/TLS設定オプション：

        -   オプション1：サーバー認証のみ

            -   MySQLサーバーがサーバー認証のみに設定されている場合は、 **CA証明書**のみをアップロードしてください。
            -   このオプションでは、MySQLサーバーが自身の証明書を提示して身元を証明し、 TiDB Cloudが認証局（CA）に対してサーバー証明書を検証します。
            -   CA証明書は中間者攻撃から保護し、MySQLサーバーを`require_secure_transport = ON`で起動する場合に必要です。

        -   オプション2：クライアント証明書認証

            -   MySQLサーバーがクライアント証明書認証用に構成されている場合は、**クライアント証明書**と**クライアント秘密鍵**をアップロードしてください。
            -   このオプションでは、 TiDB Cloudは認証のためにMySQLサーバーに証明書を提示しますが、 TiDB Cloudサーバーの証明書を検証しません。
            -   このオプションは通常、MySQLサーバーが`REQUIRE SUBJECT '...'`や`REQUIRE ISSUER '...'`などのオプションで構成されているが、 `REQUIRE X509`含まれていない場合に使用され、クライアント証明書の完全な CA 検証を行わずに、クライアント証明書の特定の属性をチェックできるようにします。
            -   このオプションは、MySQLサーバーが自己署名証明書またはカスタムPKI環境でクライアント証明書を受け入れる場合によく使用されます。ただし、この構成は中間者攻撃に対して脆弱であるため、他のネットワークレベルの制御によってサーバーの信頼性が保証されない限り、本番環境での本番は推奨されません。

        -   オプション3：相互TLS（mTLS） - 最高レベルのセキュリティ

            -   MySQLサーバーが相互TLS（mTLS）認証用に構成されている場合は、 **CA証明書**、**クライアント証明書**、および**クライアント秘密鍵**をアップロードしてください。
            -   このオプションでは、MySQLサーバーはクライアント証明書を使用してTiDB Cloudの身元を検証し、 TiDB CloudはCA証明書を使用してMySQLサーバーの身元を検証します。
            -   このオプションは、MySQLサーバーで移行ユーザーに対して`REQUIRE X509`または`REQUIRE SSL`が設定されている場合に必要です。
            -   このオプションは、MySQLサーバーが認証のためにクライアント証明書を必要とする場合に使用されます。
            -   証明書は以下の情報源から入手できます。
                -   クラウド プロバイダーからダウンロードします ( [TLS証明書リンク](#end-to-end-encryption-over-tlsssl)を参照)。
                -   組織の内部認証局証明書を使用してください。
                -   自己署名証明書（開発／テスト専用）。

3.  ターゲット接続プロファイルを入力してください。

    -   **ユーザー名**: <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>TiDB Cloud<CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>のユーザー名を入力します。
    -   **パスワード**： TiDB Cloudのユーザー名のパスワードを入力してください。

4.  入力した情報を検証するには、 **「接続を検証」をクリックし、「次へ」を**クリックしてください。

5.  表示されたメッセージに従って行動してください。

    <CustomContent plan="dedicated">

    -   接続方法として**パブリックIP**または**VPCピアリングを**使用する場合は、データ移行サービスのIPアドレスを、ソースデータベースおよびファイアウォール（存在する場合）のIPアクセスリストに追加する必要があります。
    -   接続方法として**プライベートリンク**を使用する場合、エンドポイント要求を承認するよう求められます。
        -   AWSの場合： [AWS VPCコンソール](https://us-west-2.console.aws.amazon.com/vpc/home)に移動し、**エンドポイントサービス**をクリックして、 TiDB Cloudからのエンドポイントリクエストを承認します。
        -   Azure の場合: [Azureポータル](https://portal.azure.com)に移動し、MySQL Flexible Server を名前で検索し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックし、右側の**[プライベート エンドポイント]**セクションを見つけて、 TiDB Cloudからの保留中の接続要求を承認します。

    </CustomContent>
    <CustomContent plan="essential">

    パブリックIPを使用する場合は、データ移行サービスのIPアドレスを、ソースデータベースおよびファイアウォール（存在する場合）のIPアクセスリストに追加する必要があります。

    </CustomContent>

## ステップ3：移行ジョブの種類を選択する {#step-3-choose-migration-job-type}

<CustomContent plan="dedicated">

**「移行ジョブタイプの選択」**ステップでは、既存データと増分データの両方を移行するか、既存データのみを移行するか、増分データのみを移行するかを選択できます。

</CustomContent>

<CustomContent plan="essential">

**「移行ジョブタイプの選択」**ステップでは、既存データと増分データの両方を移行するか、増分データのみを移行するかを選択できます。

</CustomContent>

### 既存データと増分データを移行する {#migrate-existing-data-and-incremental-data}

<CustomContent plan="dedicated">

TiDB Cloudへのデータ移行を一度で完了させるには、 **「既存データ移行」**と**「増分データ移行」の**両方を選択してください。これにより、ソースデータベースとターゲットデータベース間のデータの一貫性が確保されます。

**既存データ**と**増分データの**移行には**、物理​​モード**または**論理モード**を使用できます。

-   デフォルトモードは**論理モード**です。このモードでは、MySQLソースデータベースからSQLステートメントとしてデータをエクスポートし、TiDB上で実行します。このモードでは、移行前のターゲットテーブルは空でも空でなくても構いません。ただし、物理モードよりもパフォーマンスは低下します。

-   大規模なデータセットの場合は、**物理モード**の使用をお勧めします。このモードでは、MySQLソースデータベースからデータをエクスポートし、KVペアとしてエンコードしてTiKVに直接書き込むことで、パフォーマンスを向上させます。このモードでは、移行前にターゲットテーブルが空である必要があります。16 RCU（レプリケーション容量ユニット）の仕様の場合、パフォーマンスは論理モードの約2.5倍高速です。その他の仕様では、論理モードと比較してパフォーマンスが20%～50%向上する可能性があります。なお、パフォーマンスデータは参考値であり、シナリオによって異なる場合がありますのでご注意ください。

> **注記：**
>
> -   物理モードを使用する場合、既存のデータ移行が完了する前に、 <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>の 2 番目の移行ジョブまたはインポート タスクを作成することはできません。
> -   物理モードを使用し、移行ジョブが開始されたら、 <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>で PITR (ポイントインタイムリカバリ) を有効にしたり、変更フィードを設定したり**しないで**ください<CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>そうしないと、移行ジョブが停止します。PITR を有効にしたり、変更フィードを設定したりする必要がある場合は、代わりに論理モードを使用してデータを移行してください。

物理モードでは、MySQLソースデータを可能な限り高速にエクスポートするため、 [異なる仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)データエクスポート時のMySQLソースデータベースのQPSとTPSに対するパフォーマンスへの影響が異なります。以下の表は、各仕様のパフォーマンス低下を示しています。

| 移行仕様   | 最大輸出速度      | MySQLソースデータベースのパフォーマンス低下 |
| ------ | ----------- | ------------------------ |
| RCU 2台 | 80.84 MiB/秒 | 15.6%                    |
| 4つのRCU | 214.2 MiB/秒 | 20.0%                    |
| 8 RCU  | 365.5 MiB/秒 | 28.9%                    |
| 16 RCU | 424.6 MiB/秒 | 46.7%                    |

</CustomContent>
<CustomContent plan="essential">

TiDB Cloudへのデータ移行を一度で完了させるには、ソースデータベースとターゲットデータベース間のデータの一貫性を確保するため、 **「完全＋増分」**と**「増分」の両方のデータ移行を**選択してください。

現在、**既存データの**移行には**論理モード**のみを使用できます。このモードでは、MySQLソースデータベースからSQLステートメントとしてデータをエクスポートし、TiDB上で実行します。このモードでは、移行前のターゲットテーブルは空でも空でなくても構いません。

</CustomContent>

<CustomContent plan="dedicated">

### 既存データのみを移行する {#migrate-only-existing-data}

ソースデータベースの既存データのみをTiDB Cloudに移行するには、 **「既存データの移行」を**選択します。

物理モードまたは論理モードを使用して、既存のデータを移行できます。詳細については、[既存データと増分データを移行する](#migrate-existing-data-and-incremental-data)参照してください。

</CustomContent>

### 増分データのみを移行する {#migrate-only-incremental-data}

ソースデータベースの増分データのみをTiDB Cloudに移行するには、 **「増分データ移行」**を選択します。この場合、移行ジョブはソースデータベースの既存データをTiDB Cloudに移行せず、移行ジョブで明示的に指定されたソースデータベースの進行中の変更のみを移行します。

増分データ移行の詳細な手順については、 [データ移行を使用して、MySQL互換データベースからTiDB Cloudへ増分データのみを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)参照してください。

## ステップ4：移行するオブジェクトを選択する {#step-4-choose-the-objects-to-be-migrated}

1.  **「移行するオブジェクトの選択」**ページで、移行するオブジェクトを選択します。 **「すべて**」をクリックするとすべてのオブジェクトを選択できます。 **「カスタマイズ」**をクリックしてから、オブジェクト名の横にあるチェックボックスをクリックしてオブジェクトを選択することもできます。

    -   **「すべて」**をクリックすると、移行ジョブはソースデータベースインスタンス全体から既存のデータをTiDB Cloudに移行し、完全移行後に進行中の変更も移行します。ただし、これは前の手順で「**既存データの移行」**と**「増分データの移行」の**チェックボックスを選択した場合にのみ実行されます。
    -   **「カスタマイズ」**をクリックしてデータベースを選択すると、移行ジョブによって既存のデータと選択したデータベースの進行中の変更がTiDB Cloudに移行されます。ただし、これは前の手順で「**既存データの移行」**と**「増分データの移行」の**チェックボックスを選択した場合にのみ実行されます。
    -   **「カスタマイズ」**をクリックしてデータベース名の下のテーブルを選択すると、移行ジョブは既存のデータと選択したテーブルの進行中の変更のみを移行します。同じデータベースで後から作成されたテーブルは移行されません。

2.  **「次へ」**をクリックしてください。

## ステップ5：事前チェック {#step-5-precheck}

**事前チェック**ページでは、事前チェックの結果を確認できます。事前チェックが失敗した場合は、 **「失敗」**または**「警告」の**詳細に従って問題を解決し、再度**「チェック」**をクリックして再チェックしてください。

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

## 移行ジョブ仕様を拡張する {#scale-a-migration-job-specification}

TiDB Cloud Dedicatedは、さまざまなシナリオにおけるパフォーマンスとコストの要件を満たすために、移行ジョブの仕様をスケールアップまたはスケールダウンすることをサポートします。

移行仕様によってパフォーマンスは異なります。パフォーマンス要件は、移行の段階によっても変化する可能性があります。例えば、既存データの移行中は、可能な限り高速なパフォーマンスが求められるため、8 RCUといった大規模な仕様の移行ジョブを選択します。既存データの移行が完了すると、増分移行ではそれほど高いパフォーマンスは必要ないため、例えば8 RCUから2 RCUへとジョブ仕様を縮小することでコストを削減できます。

移行ジョブの仕様を拡張する際には、以下の点に注意してください。

-   移行ジョブの仕様を拡張するには、約5～10分かかります。
-   スケーリングが失敗した場合、ジョブの仕様はスケーリング前と同じままになります。

### 制限事項 {#limitations}

-   移行ジョブの仕様をスケーリングできるのは、ジョブが**「実行中」**または**「一時停止中」の**状態にある場合のみです。
-   TiDB Cloudは、既存のデータエクスポート段階における移行ジョブ仕様のスケーリングをサポートしていません。
-   移行ジョブの仕様を拡張すると、ジョブが再起動されます。ジョブのソーステーブルに主キーがない場合、重複データが挿入される可能性があります。
-   スケーリング中は、ソースデータベースのバイナリログをパージしたり、MySQLソースデータベースの`expire_logs_days`を一時的に増やしたりしないでください。そうしないと、連続したバイナリログの位置を取得できず、ジョブが失敗する可能性があります。

### スケーリング手順 {#scaling-procedure}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

2.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent>の名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[データ移行]**をクリックします。

3.  **データ移行**ページで、スケールアップする移行ジョブを探します。**アクション**列で、 **[...]** &gt; **[スケールアップ/スケールダウン]**をクリックします。

4.  **「スケールアップ／スケールダウン」**ウィンドウで、使用する新しい仕様を選択し、 **「送信」**をクリックします。ウィンドウの下部に、その仕様の新しい価格が表示されます。

</CustomContent>
