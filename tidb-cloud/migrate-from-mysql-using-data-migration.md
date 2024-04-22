---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
aliases: ['/tidbcloud/migrate-data-into-tidb','/tidbcloud/migrate-incremental-data-from-mysql']
summary: データ移行を使用して、TiDB CloudにMySQL互換データベースを移行する方法について説明します。この機能は、ソースデータベースの既存のデータと進行中の変更を一度に直接移行するのに役立ちます。移行ジョブの最大数は組織ごとに最大200個で、さらに移行ジョブを作成するにはサポートチケットを提出する必要があります。データ移行はMySQL 5.6、5.7、および8.0のローカルインスタンスまたはパブリッククラウドプロバイダー上でサポートされています。また、AWSやGoogle Cloudなどのクラウドプロバイダー上でのデータ移行もサポートされています。
---

# データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する {#migrate-mysql-compatible-databases-to-tidb-cloud-using-data-migration}

このドキュメントでは、データ移行を使用して、クラウドプロバイダー上の MySQL 互換データベース (Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、または Google Cloud SQL for MySQL) またはセルフホストのソース データベースからTiDB Cloudにデータを移行する方法について説明します。 TiDB Cloudコンソールの機能。

この機能は、ソース データベースの既存のデータと進行中の変更を (同じリージョン内またはリージョン間で) TiDB Cloudに一度に直接移行するのに役立ちます。

増分データのみを移行する場合は、 [データ移行を使用して、MySQL 互換データベースからTiDB Cloudに増分データを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照してください。

## 制限事項 {#limitations}

### 可用性 {#availability}

-   データ移行機能は、 **TiDB 専用**クラスターでのみ使用できます。

-   データ移行機能は、2022 年 11 月 9 日以降に[特定の地域](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost)で作成されたクラスターでのみ使用できます。**プロジェクト**がその日より前に作成された場合、またはクラスターが別のリージョンにある場合、この機能はクラスターと**[データ移行]**タブでは使用できません。 TiDB Cloudコンソールのクラスター概要ページには表示されません。

-   Amazon Aurora MySQL ライター インスタンスは、既存のデータと増分データ移行の両方をサポートします。 Amazon Aurora MySQL リーダー インスタンスは、既存のデータ移行のみをサポートし、増分データ移行はサポートしません。

### 移行ジョブの最大数 {#maximum-number-of-migration-jobs}

組織ごとに最大 200 個の移行ジョブを作成できます。さらに移行ジョブを作成するには、 [サポートチケットを提出する](/tidb-cloud/tidb-cloud-support.md)を実行する必要があります。

### フィルタリングされて削除されたデータベース {#filtered-out-and-deleted-databases}

-   移行するデータベースをすべて選択した場合でも、システム データベースはフィルターで除外され、 TiDB Cloudには移行されません。つまり、 `mysql` 、 `information_schema` 、 `information_schema` 、および`sys`は、この機能を使用して移行されません。

-   TiDB Cloudでクラスターを削除すると、そのクラスター内のすべての移行ジョブが自動的に削除され、回復できなくなります。

### 既存のデータ移行の制限 {#limitations-of-existing-data-migration}

-   既存のデータの移行中に、移行対象のテーブルが重複キーを持つターゲット データベースにすでに存在する場合、重複キーは置き換えられます。

-   データセットのサイズが 1 TiB より小さい場合は、論理モード (デフォルト モード) を使用することをお勧めします。データセットのサイズが 1 TiB より大きい場合、または既存のデータをより速く移行したい場合は、物理モードを使用できます。詳細については、 [既存のデータと増分データを移行する](#migrate-existing-data-and-incremental-data)を参照してください。

### 増分データ移行の制限 {#limitations-of-incremental-data-migration}

-   増分データ移行中に、移行対象のテーブルが重複したキーを持つターゲット データベースにすでに存在する場合、エラーが報告され、移行は中断されます。この状況では、アップストリーム データが正確かどうかを確認する必要があります。 「はい」の場合、移行ジョブの「再開」ボタンをクリックすると、移行ジョブは競合する下流のレコードを上流のレコードに置き換えます。

-   増分レプリケーション (進行中の変更をクラスターに移行する) 中に、移行ジョブが突然のエラーから回復すると、セーフ モードが 60 秒間開くことがあります。セーフ モードでは、 `INSERT`ステートメントは`REPLACE`として、 `UPDATE`ステートメントは`DELETE`および`REPLACE`として移行され、その後、これらのトランザクションはダウンストリーム クラスターに移行され、突然のエラー中のすべてのデータがダウンストリーム クラスターにスムーズに移行されたことを確認します。このシナリオでは、主キーや非 null の一意のインデックスがないアップストリーム テーブルの場合、データがダウンストリームに繰り返し挿入される可能性があるため、一部のデータがダウンストリーム クラスターで重複する可能性があります。

-   次のシナリオでは、移行ジョブに 24 時間以上かかる場合は、データ移行が増分レプリケーション用に連続したバイナリ ログを確実に取得できるように、ソース データベース内のバイナリ ログをパージしないでください。

    -   既存のデータの移行中。
    -   既存のデータ移行が完了した後、初めて増分データ移行を開始するとき、レイテンシーは0 ミリ秒ではありません。

## 前提条件 {#prerequisites}

移行を実行する前に、データ ソースを確認し、上流および下流のデータベースに対する権限を準備し、ネットワーク接続を設定する必要があります。

### データ ソースとバージョンがサポートされていることを確認してください {#make-sure-your-data-source-and-version-are-supported}

データ移行は、次のデータ ソースとバージョンをサポートします。

-   MySQL 5.6、5.7、および 8.0 のローカル インスタンスまたはパブリック クラウド プロバイダー上。 MySQL 8.0 はTiDB Cloud上でまだ実験的にあるため、非互換性の問題が発生する可能性があることに注意してください。
-   Amazon Aurora (MySQL 5.6 および 5.7)
-   Amazon RDS (MySQL 5.7)
-   MySQL 5.6 および 5.7 用の Google Cloud SQL

### 上流データベースに必要な権限を付与します。 {#grant-required-privileges-to-the-upstream-database}

アップストリーム データベースに使用するユーザー名には、次のすべての権限が必要です。

| 特権                   | 範囲    |
| :------------------- | :---- |
| `SELECT`             | テーブル  |
| `LOCK`               | テーブル  |
| `REPLICATION SLAVE`  | グローバル |
| `REPLICATION CLIENT` | グローバル |

たとえば、次の`GRANT`ステートメントを使用して、対応する権限を付与できます。

```sql
GRANT SELECT,LOCK TABLES,REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'your_user'@'your_IP_address_of_host'
```

### ダウンストリームTiDB Cloudクラスターに必要な権限を付与します。 {#grant-required-privileges-to-the-downstream-tidb-cloud-cluster}

ダウンストリームTiDB Cloudクラスターに使用するユーザー名には、次の権限が必要です。

| 特権       | 範囲          |
| :------- | :---------- |
| `CREATE` | データベース、テーブル |
| `SELECT` | テーブル        |
| `INSERT` | テーブル        |
| `UPDATE` | テーブル        |
| `DELETE` | テーブル        |
| `ALTER`  | テーブル        |
| `DROP`   | データベース、テーブル |
| `INDEX`  | テーブル        |

たとえば、次の`GRANT`ステートメントを実行して、対応する権限を付与できます。

```sql
GRANT CREATE,SELECT,INSERT,UPDATE,DELETE,ALTER,DROP,INDEX ON *.* TO 'your_user'@'your_IP_address_of_host'
```

移行ジョブを迅速にテストするには、 TiDB Cloudクラスターの`root`アカウントを使用できます。

### ネットワーク接続をセットアップする {#set-up-network-connection}

移行ジョブを作成する前に、接続方法に従ってネットワーク接続を設定します。 [TiDB 専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

-   ネットワーク接続にパブリック IP (標準接続) を使用する場合は、上流のデータベースがパブリック ネットワーク経由で接続できることを確認してください。

-   AWS VPC ピアリングまたは Google Cloud VPC ネットワーク ピアリングを使用する場合は、次の手順を参照してネットワークを構成してください。

<details><summary>AWS VPC ピアリングを設定する</summary>

MySQL サービスが AWS VPC 内にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスターの間は[VPC ピアリング接続をセットアップする](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    受信ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)を追加する必要があります。これにより、トラフィックが TiDB クラスターから MySQL インスタンスに流れるようになります。

3.  MySQL URL に DNS ホスト名が含まれている場合は、 TiDB Cloud がMySQL サービスのホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **アクセプター DNS 解決**オプションを有効にします。

</details>

<details><summary>Google Cloud VPC ネットワーク ピアリングを設定する</summary>

MySQL サービスが Google Cloud VPC 内にある場合は、次の手順を実行します。

1.  セルフホスト型 MySQL の場合は、この手順をスキップして次の手順に進むことができます。 MySQL サービスが Google Cloud SQL の場合は、Google Cloud SQL インスタンスの関連する VPC で MySQL エンドポイントを公開する必要があります。 Google が開発した[Cloud SQL 認証プロキシ](https://cloud.google.com/sql/docs/mysql/sql-proxy)使用する必要がある場合があります。

2.  MySQL サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続をセットアップする](/tidb-cloud/set-up-vpc-peering-connections.md) 。

3.  MySQL が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    受信ファイアウォール ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)を追加する必要があります。これにより、トラフィックが TiDB クラスターから MySQL エンドポイントに流れることが可能になります。

</details>

### バイナリログを有効にする {#enable-binary-logs}

増分データ移行を実行するには、アップストリーム データベースのバイナリ ログが有効になっていること、およびバイナリ ログが 24 時間以上保存されていることを確認してください。

## ステップ 1:<strong>データ移行</strong>ページに移動する {#step-1-go-to-the-strong-data-migration-strong-page}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅の をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ移行]**をクリックします。

3.  **[データ移行]**ページで、右上隅にある**[移行ジョブの作成]**をクリックします。 **「移行ジョブの作成」**ページが表示されます。

## ステップ 2: ソース接続とターゲット接続を構成する {#step-2-configure-the-source-and-target-connection}

**[移行ジョブの作成]**ページで、ソース接続とターゲット接続を構成します。

1.  ジョブ名を入力します。ジョブ名は文字で始まり、60 文字未満である必要があります。文字 (A ～ Z、az)、数字 (0 ～ 9)、アンダースコア (_)、およびハイフン (-) を使用できます。

2.  ソース接続プロファイルを入力します。

    -   **データ ソース**: データ ソースの種類。
    -   **リージョン**: データ ソースのリージョン。クラウド データベースにのみ必要です。
    -   **接続方法**: データ ソースの接続方法。現在、接続方法に応じてパブリック IP、VPC ピアリング、またはプライベート リンクを選択できます。
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

    -   **ユーザー名**: TiDB Cloudのターゲットクラスターのユーザー名を入力します。
    -   **パスワード**: TiDB Cloudユーザー名のパスワードを入力します。

4.  **「接続を検証して次へ」**をクリックして、入力した情報を検証します。

5.  表示されるメッセージに従ってアクションを実行します。

    -   パブリック IP または VPC ピアリングを使用する場合は、ソース データベースとファイアウォール (存在する場合) の IP アクセス リストにデータ移行サービスの IP アドレスを追加する必要があります。
    -   AWS Private Link を使用する場合は、エンドポイント リクエストを受け入れるように求められます。 [AWS VPC コンソール](https://us-west-2.console.aws.amazon.com/vpc/home)に移動し、 **「エンドポイント サービス」**をクリックしてエンドポイント要求を受け入れます。

## ステップ 3: 移行ジョブの種類を選択する {#step-3-choose-migration-job-type}

**「移行するオブジェクトの選択」**ステップでは、既存のデータ移行、増分データ移行、またはその両方を選択できます。

### 既存のデータと増分データを移行する {#migrate-existing-data-and-incremental-data}

TiDB Cloudにデータを一度に移行するには、 **[既存のデータ移行]**と**[増分データ移行]**の両方を選択します。これにより、ソース データベースとターゲット データベース間のデータの一貫性が確保されます。

**物理モード**または**論理モード**を使用して、**既存のデータ**を移行できます。

-   デフォルトのモードは**論理モード**です。このモードでは、上流のデータベースからデータを SQL ステートメントとしてエクスポートし、TiDB 上で実行します。このモードでは、移行前のターゲット テーブルは空でも空でなくても構いません。ただし、パフォーマンスは物理モードよりも遅くなります。

-   大規模なデータセットの場合は、**物理モード**を使用することをお勧めします。このモードでは、上流のデータベースからデータをエクスポートして KV ペアとしてエンコードし、TiKV に直接書き込むことでより高速なパフォーマンスを実現します。このモードでは、移行前にターゲット テーブルが空である必要があります。 16 RCU (Replication Capacity Unit) の仕様では、論理モードと比較して約 2.5 倍のパフォーマンスが向上します。他の仕様のパフォーマンスは、論理モードと比較して 20% ～ 50% 向上する可能性があります。パフォーマンス データは参考用であり、シナリオによって異なる場合があることに注意してください。

物理モードは、AWS および Google Cloud にデプロイされた TiDB クラスターで使用できます。

> **注記：**
>
> -   物理モードを使用する場合、既存のデータ移行が完了するまで、TiDB クラスターの 2 番目の移行ジョブまたはインポート タスクを作成することはできません。
> -   物理モードを使用しており、移行ジョブが開始されている場合は、PITR (ポイントインタイム リカバリ) を有効にしたり、クラスター上で変更フィードを設定したりし**ないで**ください。そうしないと、移行ジョブが停止します。 PITR を有効にする必要がある場合、または変更フィードがある場合は、代わりに論理モードを使用してデータを移行します。

物理モードでは、アップストリーム データが可能な限り高速にエクスポートされるため、データ エクスポート中にアップストリーム データベースの QPS および TPS に対してパフォーマンスに[異なる仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)影響があります。次の表は、各仕様のパフォーマンス回帰を示しています。

| 移行仕様   | 最大エクスポート速度  | 上流データベースのパフォーマンス低下 |
| ------ | ----------- | ------------------ |
| 2 RCU  | 80.84 MiB/秒 | 15.6%              |
| 4 RCU  | 214.2 MiB/秒 | 20.0%              |
| 8 RCU  | 365.5 MiB/秒 | 28.9%              |
| 16 RCU | 424.6 MiB/秒 | 46.7%              |

### 既存のデータのみを移行する {#migrate-only-existing-data}

ソース データベースの既存データのみをTiDB Cloudに移行するには、 **[既存のデータの移行]**を選択します。

既存のデータを移行するために物理モードまたは論理モードの使用を選択できます。詳細については、 [既存のデータと増分データを移行する](#migrate-existing-data-and-incremental-data)を参照してください。

### 増分データのみを移行する {#migrate-only-incremental-data}

ソース データベースの増分データのみをTiDB Cloudに移行するには、 **[増分データ移行]**を選択します。この場合、移行ジョブはソース データベースの既存のデータをTiDB Cloudに移行せず、移行ジョブによって明示的に指定されたソース データベースの進行中の変更のみを移行します。

増分データ移行の詳細な手順については、 [データ移行を使用して、MySQL 互換データベースからTiDB Cloudに増分データのみを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照してください。

## ステップ 4: 移行するオブジェクトを選択する {#step-4-choose-the-objects-to-be-migrated}

1.  **「移行するオブジェクトの選択」**ページで、移行するオブジェクトを選択します。 **「すべて」**をクリックしてすべてのオブジェクトを選択するか、 **「カスタマイズ」**をクリックしてオブジェクト名の横にあるチェックボックスをクリックしてオブジェクトを選択します。

    -   **「すべて」**をクリックすると、移行ジョブはソース・データベース・インスタンス全体から既存のデータをTiDB Cloudに移行し、完全な移行後に進行中の変更を移行します。これは、前の手順で**[既存のデータ移行]**チェックボックスと**[増分データ移行]**チェックボックスを選択した場合にのみ発生することに注意してください。

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-all.png" width="60%" />

    -   **「カスタマイズ」**をクリックしてデータベースを選択すると、移行ジョブによって既存のデータが移行され、選択したデータベースの進行中の変更がTiDB Cloudに移行されます。これは、前の手順で**[既存のデータ移行]**チェックボックスと**[増分データ移行]**チェックボックスを選択した場合にのみ発生することに注意してください。

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-db.png" width="60%" />

    -   **[カスタマイズ]**をクリックし、データセット名の下でいくつかのテーブルを選択すると、移行ジョブは既存のデータのみを移行し、選択したテーブルの進行中の変更を移行します。同じデータベース内に後で作成されたテーブルは移行されません。

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-tables.png" width="60%" />

    <!--
     - If you click **Customize** and select some databases, and then select some tables in the **Selected Objects** area to move them back to the **Source Database** area, (for example the `username` table in the following screenshots), then the tables will be treated as in a blocklist. The migration job will migrate the existing data but filter out the excluded tables (such as the `username` table in the screenshots), and will migrate ongoing changes of the selected databases to TiDB Cloud except the filtered-out tables.
         ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist1.png)
         ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist2.png)
     -->

2.  **「次へ」**をクリックします。

## ステップ 5: 事前チェック {#step-5-precheck}

**[事前チェック]**ページでは、事前チェックの結果を表示できます。事前チェックが失敗した場合は、「**失敗」**または**「警告」の**詳細に従って操作し、 **「再度チェック」を**クリックして再チェックする必要があります。

一部のチェック項目に警告のみがある場合は、リスクを評価し、警告を無視するかどうかを検討できます。すべての警告が無視された場合、移行ジョブは自動的に次のステップに進みます。

エラーと解決策の詳細については、 [事前チェックエラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)を参照してください。

事前チェック項目の詳細については、 [移行タスクの事前チェック](https://docs.pingcap.com/tidb/stable/dm-precheck)を参照してください。

すべてのチェック項目に**「合格」**と表示されている場合は、 **「次へ」**をクリックします。

## ステップ 6: 仕様を選択して移行を開始する {#step-6-choose-a-spec-and-start-migration}

**「仕様を選択して移行を開始」**ページで、パフォーマンス要件に応じて適切な移行仕様を選択します。仕様の詳細については、 [データ移行の仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)を参照してください。

仕様を選択した後、 **「ジョブを作成して開始」**をクリックして移行を開始します。

## ステップ 7: 移行の進行状況をビュー {#step-7-view-the-migration-progress}

移行ジョブの作成後、 **[移行ジョブの詳細]**ページで移行の進行状況を確認できます。移行の進行状況が**「ステージとステータス」**領域に表示されます。

実行中の移行ジョブを一時停止または削除できます。

移行ジョブが失敗した場合は、問題を解決した後に再開できます。

移行ジョブはどのステータスでも削除できます。

移行中に問題が発生した場合は、 [移行エラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)を参照してください。

## 移行ジョブの仕様を拡張する {#scale-a-migration-job-specification}

TiDB Cloudは、さまざまなシナリオでのパフォーマンスとコストの要件を満たすために、移行ジョブ仕様のスケールアップまたはスケールダウンをサポートしています。

移行仕様が異なればパフォーマンスも異なります。パフォーマンス要件もさまざまな段階で異なる場合があります。たとえば、既存のデータの移行中に、パフォーマンスをできるだけ高速にする必要があるため、8 RCU などの大きな仕様の移行ジョブを選択します。既存のデータ移行が完了すると、増分移行にはそれほど高いパフォーマンスは必要ないため、コストを節約するためにジョブ仕様をたとえば 8 RCU から 2 RUC にスケールダウンできます。

移行ジョブの仕様を拡張する場合は、次の点に注意してください。

-   移行ジョブの仕様を拡張するには、約 5 ～ 10 分かかります。
-   スケーリングが失敗した場合、ジョブ仕様はスケーリング前と同じままになります。

### 制限事項 {#limitations}

-   移行ジョブ仕様をスケールできるのは、ジョブが**実行中**または**一時停止**ステータスにある場合のみです。
-   TiDB Cloudは、既存のデータ エクスポート段階での移行ジョブ仕様のスケーリングをサポートしていません。
-   移行ジョブ仕様をスケーリングすると、ジョブが再開されます。ジョブのソーステーブルに主キーがない場合、重複データが挿入される可能性があります。
-   スケーリング中は、ソース データベースのバイナリ ログをパージしたり、上流データベースの`expire_logs_days`を一時的に増やしたりしないでください。そうしないと、連続バイナリ ログの位置を取得できないため、ジョブが失敗する可能性があります。

### スケーリング手順 {#scaling-procedure}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ移行]**をクリックします。

3.  **[データ移行]**ページで、スケールする移行ジョブを見つけます。 **[アクション]**列で、 **[...]** &gt; **[スケールアップ/ダウン]**をクリックします。

4.  **[スケールアップ/スケールダウン]**ウィンドウで、使用する新しい仕様を選択し、 **[送信]**をクリックします。ウィンドウの下部に仕様の新しい価格が表示されます。
