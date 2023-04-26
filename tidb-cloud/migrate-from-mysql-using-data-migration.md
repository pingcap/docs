---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Learn how to migrate data from MySQL-compatible databases hosted in Amazon Aurora MySQL, Amazon Relational Database Service (RDS), Google Cloud SQL for MySQL, or a local MySQL instance to TiDB Cloud using Data Migration.
---

# データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する {#migrate-mysql-compatible-databases-to-tidb-cloud-using-data-migration}

このドキュメントでは、クラウド プロバイダー (Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、または Google Cloud SQL for MySQL) またはオンプレミスの MySQL 互換データベースから、 TiDB Cloudのデータ移行機能を使用してデータを移行する方法について説明します。 TiDB Cloudコンソール。

この機能は、ソース データベースの既存のデータと進行中の変更をTiDB Cloudに直接移行するのに役立ちます (同じリージョンまたはクロス リージョン内のいずれか)。

## 制限事項 {#limitations}

-   データ移行機能は、 **Dedicated Tier**クラスターでのみ使用できます。

-   データ移行機能は、2022 年 11 月 9 日以降に次のリージョンで作成されたプロジェクトのクラスターでのみ使用できます。**プロジェクトが**その日付より前に作成された場合、またはクラスターが別のリージョンにある場合、この機能はクラスターで使用できません。<strong>データ移行</strong>タブは、 TiDB Cloudコンソールのクラスター概要ページに表示されません。

    -   AWS オレゴン (us-west-2)
    -   AWS 北バージニア (us-east-1)
    -   AWS シンガポール (ap-southeast-1)
    -   AWS 東京 (ap-northeast-1)
    -   AWS フランクフルト (eu-central-1)
    -   AWS ソウル (ap-northeast-2)
    -   GCP オレゴン (us-west1)
    -   GCP シンガポール (asia-southeast1)
    -   GCP 東京 (asia-northeast1)

-   Amazon Aurora MySQL ライター インスタンスは、既存のデータと増分データの移行の両方をサポートしています。 Amazon Aurora MySQL リーダー インスタンスは、既存のデータの移行のみをサポートし、増分データの移行はサポートしていません。

-   組織ごとに最大 200 の移行ジョブを作成できます。さらに移行ジョブを作成するには、 [サポート チケットを提出する](/tidb-cloud/tidb-cloud-support.md)を行う必要があります。

-   移行するすべてのデータベースを選択した場合でも、システム データベースは除外され、 TiDB Cloudに移行されません。つまり、 `mysql` 、 `information_schema` 、 `information_schema` 、および`sys`は、この機能を使用して移行されません。

-   既存のデータの移行中に、移行対象のテーブルが重複キーを持つターゲット データベースに既に存在する場合、重複キーは置き換えられます。

-   増分データ移行中に、移行対象のテーブルが重複したキーを持つターゲット データベースに既に存在する場合、エラーが報告され、移行が中断されます。この状況では、アップストリーム データが正確かどうかを確認する必要があります。はいの場合は、移行ジョブの [再起動] ボタンをクリックすると、移行ジョブによって、競合するダウンストリーム レコードがアップストリーム レコードに置き換えられます。

-   TiDB Cloudでクラスターを削除すると、そのクラスター内のすべての移行ジョブが自動的に削除され、回復できなくなります。

-   増分レプリケーション (進行中の変更をクラスターに移行する) 中に、移行ジョブが突然のエラーから回復した場合、セーフ モードが 60 秒間開くことがあります。セーフ モードでは、 `INSERT`ステートメントは`REPLACE`として複製され、 `UPDATE`ステートメントは`DELETE`および`REPLACE`として複製されます。その後、これらのトランザクションがダウンストリーム クラスターに複製され、突然のエラー中のすべてのデータがダウンストリーム クラスターにスムーズに移行されたことを確認します。このシナリオでは、主キーまたは null 以外の一意のインデックスを持たないアップストリーム テーブルの場合、データがダウンストリームに繰り返し挿入される可能性があるため、一部のデータがダウンストリーム クラスターで複製される可能性があります。

-   データ移行を使用する場合は、データセットのサイズを 1 TiB 未満に保つことをお勧めします。データセットのサイズが 1 TiB を超える場合、既存のデータの移行は仕様の制限により時間がかかります。

-   次のシナリオでは、移行ジョブに 24 時間以上かかる場合は、ソース データベースのバイナリ ログを削除しないでください。これにより、Data Migration が増分レプリケーション用の連続したバイナリ ログを取得できるようになります。

    -   既存のデータの移行中。
    -   既存のデータの移行が完了した後、増分データの移行が初めて開始されるとき、レイテンシーは0 ミリ秒ではありません。

## 前提条件 {#prerequisites}

移行を実行する前に、データ ソースを確認し、アップストリーム データベースとダウンストリーム データベースの権限を準備し、ネットワーク接続を設定する必要があります。

### データソースとバージョンがサポートされていることを確認してください {#make-sure-your-data-source-and-version-are-supported}

データ移行では、次のデータ ソースとバージョンがサポートされています。

-   MySQL 5.6、5.7、および 8.0 ローカル インスタンスまたはパブリック クラウド プロバイダー。 MySQL 8.0 はTiDB Cloudではまだ実験的であり、非互換性の問題がある可能性があることに注意してください。
-   アマゾンAurora(MySQL 5.6 および 5.7)
-   アマゾン RDS (MySQL 5.7)
-   Google Cloud SQL for MySQL 5.6 および 5.7

### アップストリーム データベースに必要な権限を付与する {#grant-required-privileges-to-the-upstream-database}

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

### 下流のTiDB Cloudクラスターに必要な権限を付与する {#grant-required-privileges-to-the-downstream-tidb-cloud-cluster}

ダウンストリームのTiDB Cloudクラスターに使用するユーザー名には、次の権限が必要です。

| 特権         | 範囲          |
| :--------- | :---------- |
| `CREATE`   | データベース、テーブル |
| `SELECT`   | テーブル        |
| `INSERT`   | テーブル        |
| `UPDATE`   | テーブル        |
| `DELETE`   | テーブル        |
| `ALTER`    | テーブル        |
| `DROP`     | データベース、テーブル |
| `INDEX`    | テーブル        |
| `TRUNCATE` | テーブル        |

たとえば、次の`GRANT`ステートメントを実行して、対応する権限を付与できます。

```sql
GRANT CREATE,SELECT,INSERT,UPDATE,DELETE,ALTER,TRUNCATE,DROP,INDEX ON *.* TO 'your_user'@'your_IP_address_of_host'
```

移行ジョブをすばやくテストするには、 TiDB Cloudクラスターの`root`アカウントを使用できます。

### ネットワーク接続のセットアップ {#set-up-network-connection}

移行ジョブを作成する前に、接続方法に従ってネットワーク接続をセットアップします。 [TiDBクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

-   ネットワーク接続にパブリック IP (これは標準接続) を使用する場合は、上流のデータベースがパブリック ネットワーク経由で接続できることを確認してください。

-   AWS PrivateLink を使用する場合は、 [プライベート エンドポイント接続のセットアップ](/tidb-cloud/set-up-private-endpoint-connections.md)に従って設定します。

-   AWS VPC ピアリングまたは GCP VPC ネットワーク ピアリングを使用する場合は、次の手順を参照してネットワークを構成してください。

<details><summary>AWS VPC ピアリングをセットアップする</summary>

MySQL サービスが AWS VPC にある場合は、次の手順を実行します。

1.  MySQL サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  MySQL サービスが関連付けられているセキュリティ グループの受信ルールを変更します。

    インバウンド規則に[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)を追加する必要があります。そうすることで、トラフィックが TiDB クラスターから MySQL インスタンスに流れるようになります。

3.  MySQL URL に DNS ホスト名が含まれている場合、 TiDB Cloud がMySQL サービスのホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

</details>

<details><summary>GCP VPC ネットワーク ピアリングを設定する</summary>

MySQL サービスが GCP VPC にある場合は、次の手順を実行します。

1.  自己ホスト型の MySQL の場合は、この手順をスキップして次の手順に進むことができます。 MySQL サービスが Google Cloud SQL の場合、Google Cloud SQL インスタンスの関連付けられた VPC で MySQL エンドポイントを公開する必要があります。 Google が開発した[Cloud SQL 認証プロキシ](https://cloud.google.com/sql/docs/mysql/sql-proxy)使用する必要がある場合があります。

2.  MySQL サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

3.  MySQL が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    イングレス ファイアウォール ルールに[TiDB Cloudクラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)を追加する必要があります。これにより、トラフィックが TiDB クラスターから MySQL エンドポイントに流れるようになります。

</details>

### バイナリログを有効にする {#enable-binary-logs}

増分データ移行を実行するには、アップストリーム データベースのバイナリ ログが有効になっていて、バイナリ ログが 24 時間以上保持されていることを確認してください。

## ステップ 1:<strong>データ移行</strong>ページに移動します {#step-1-go-to-the-strong-data-migration-strong-page}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データの移行]**をクリックします。

3.  **[データ移行]**ページで、右上隅にある<strong>[移行ジョブの作成]</strong>をクリックします。<strong>移行ジョブの作成</strong>ページが表示されます。

## ステップ 2: ソースとターゲットの接続を構成する {#step-2-configure-the-source-and-target-connection}

**[移行ジョブの作成]**ページで、ソース接続とターゲット接続を構成します。

1.  ジョブ名を入力します。この名前は文字で始まり、60 文字未満である必要があります。文字 (AZ、az)、数字 (0-9)、アンダースコア (_)、およびハイフン (-) を使用できます。

2.  ソース接続プロファイルを入力します。

    -   **データ ソース**: データ ソースの種類。
    -   **リージョン** : データ ソースのリージョン。クラウド データベースにのみ必要です。
    -   **接続方法**: データ ソースの接続方法。現在、接続方法に応じて、パブリック IP、VPC ピアリング、またはプライベート リンクを選択できます。
    -   **ホスト名または IP アドレス**(パブリック IP および VPC ピアリングの場合): データ ソースのホスト名または IP アドレス。
    -   **サービス名**(Private Link 用): エンドポイント サービス名。
    -   **Port** : データ ソースのポート。
    -   **Username** : データ ソースのユーザー名。
    -   **パスワード**: ユーザー名のパスワード。
    -   **SSL/TLS** : SSL/TLS を有効にする場合は、次のいずれかを含むデータ ソースの証明書をアップロードする必要があります。
        -   CA証明書のみ
        -   クライアント証明書とクライアント キー
        -   CA 証明書、クライアント証明書、およびクライアント キー

3.  ターゲット接続プロファイルを入力します。

    -   **ユーザー名**: TiDB Cloudのターゲット クラスターのユーザー名を入力します。
    -   **パスワード**: TiDB Cloudユーザー名のパスワードを入力します。

4.  **[接続を検証して次へ]**をクリックして、入力した情報を検証します。

5.  表示されるメッセージに従って対処してください。

    -   パブリック IP または VPC ピアリングを使用する場合は、データ移行サービスの IP アドレスをソース データベースとファイアウォール (存在する場合) の IP アクセス リストに追加する必要があります。
    -   AWS Private Link を使用する場合、エンドポイント リクエストを受け入れるように求められます。 [AWS VPC コンソール](https://us-west-2.console.aws.amazon.com/vpc/home)に移動し、 **[エンドポイント サービス]**をクリックしてエンドポイント要求を受け入れます。

## ステップ 3: 移行するオブジェクトを選択する {#step-3-choose-the-objects-to-be-migrated}

1.  チェックボックスを選択して、既存のデータ移行、増分データ移行、またはその両方を選択します。

    > **ヒント：**
    >
    > -   データをTiDB Cloudに完全に移行するには、**既存のデータの移行**と<strong>増分データの移行</strong>の両方を選択します。これにより、ソース データベースとターゲット データベース間のデータの一貫性が保証されます。
    > -   ソース データベースの既存のデータのみをTiDB Cloudに移行するには、 **[既存のデータ移行]**チェックボックスのみを選択します。

2.  **[移行するオブジェクトの選択]**ページで、移行するオブジェクトを選択します。 <strong>[すべて]</strong>をクリックしてすべてのオブジェクトを選択するか、 <strong>[カスタマイズ]</strong>をクリックしてからオブジェクト名の横にあるチェックボックスをクリックしてオブジェクトを選択します。

    -   **All**をクリックすると、移行ジョブは既存のデータをソース データベース インスタンス全体からTiDB Cloudに移行し、完全な移行後に進行中の変更をレプリケートします。これは、前の手順で<strong>[既存のデータの移行]</strong>チェックボックスと<strong>[増分データの移行]</strong>チェックボックスを選択した場合にのみ発生することに注意してください。

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-all.png" width="60%" />

    -   **[カスタマイズ]**をクリックしていくつかのデータベースを選択すると、移行ジョブは既存のデータを移行し、選択したデータベースの進行中の変更をTiDB Cloudにレプリケートします。これは、前の手順で<strong>[既存のデータの移行]</strong>チェックボックスと<strong>[増分データの移行]</strong>チェックボックスを選択した場合にのみ発生することに注意してください。

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-db.png" width="60%" />

    -   **[カスタマイズ]**をクリックしてデータセット名の下にあるいくつかのテーブルを選択すると、移行ジョブは既存のデータのみを移行し、選択したテーブルの進行中の変更をレプリケートします。後で同じデータベースに作成されたテーブルは移行されません。

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-tables.png" width="60%" />

    <!--
     - If you click **Customize** and select some databases, and then select some tables in the **Selected Objects** area to move them back to the **Source Database** area, (for example the `username` table in the following screenshots), then the tables will be treated as in a blocklist. The migration job will migrate the existing data but filter out the excluded tables (such as the `username` table in the screenshots), and will replicate ongoing changes of the selected databases to TiDB Cloud except the filtered-out tables.
         ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist1.png)
         ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist2.png)
     -->

3.  **[次へ]**をクリックします。

## ステップ 4: 事前チェック {#step-4-precheck}

**[事前チェック]**ページで、事前チェックの結果を表示できます。事前チェックに失敗した場合は、<strong>失敗</strong>または<strong>警告の</strong>詳細に従って操作し、<strong>再度チェック</strong>をクリックして再チェックする必要があります。

一部のチェック項目に警告しかない場合は、リスクを評価し、警告を無視するかどうかを検討できます。すべての警告が無視された場合、移行ジョブは自動的に次のステップに進みます。

エラーと解決策の詳細については、 [事前チェックのエラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)を参照してください。

事前チェック項目の詳細については、 [移行タスクの事前チェック](https://docs.pingcap.com/tidb/stable/dm-precheck)を参照してください。

すべてのチェック項目が**Pass**と表示されたら、 <strong>[Next]</strong>をクリックします。

## ステップ 5: 仕様を選択して移行を開始する {#step-5-choose-a-spec-and-start-migration}

**[仕様を選択して移行を開始]**ページで、パフォーマンス要件に応じて適切な移行仕様を選択します。仕様の詳細については、 [データ移行の仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)を参照してください。

スペックを選択したら、 **[Create Job and Start]**をクリックして移行を開始します。

## ステップ 6: 移行の進行状況をビュー {#step-6-view-the-migration-progress}

移行ジョブが作成されたら、 **[移行ジョブの詳細]**ページで移行の進行状況を確認できます。移行の進行状況は、 <strong>[ステージとステータス]</strong>領域に表示されます。

実行中の移行ジョブを一時停止または削除できます。

移行ジョブが失敗した場合は、問題を解決した後に再開できます。

どのステータスの移行ジョブも削除できます。

移行中に問題が発生した場合は、 [移行エラーと解決策](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)を参照してください。

## 移行ジョブ仕様のスケーリング {#scale-a-migration-job-specification}

TiDB Cloud は、さまざまなシナリオでパフォーマンスとコストの要件を満たすために、移行ジョブ仕様のスケールアップまたはスケールダウンをサポートしています。

移行仕様が異なれば性能も異なります。パフォーマンス要件もステージごとに異なる場合があります。たとえば、既存のデータの移行中に、パフォーマンスをできるだけ高速にしたいので、8 RCU などの大きな仕様の移行ジョブを選択します。既存のデータの移行が完了したら、増分移行ではそれほど高いパフォーマンスは必要ないため、たとえば 8 RCU から 2 RUC にジョブ仕様を縮小してコストを節約できます。

移行ジョブの仕様をスケーリングするときは、次の点に注意してください。

-   移行ジョブの仕様をスケーリングするには、約 5 ～ 10 分かかります。
-   スケーリングが失敗した場合、ジョブの仕様はスケーリング前と同じままです。

### 制限事項 {#limitations}

-   移行ジョブの仕様をスケーリングできるのは、ジョブが [**実行中**] または<strong>[一時停止]</strong>ステータスにある場合のみです。
-   TiDB Cloud は、既存のデータ エクスポート段階での移行ジョブ仕様のスケーリングをサポートしていません。
-   移行ジョブ仕様をスケーリングすると、ジョブが再開されます。ジョブのソース テーブルに主キーがない場合、重複データが挿入される可能性があります。
-   スケーリング中は、ソース データベースのバイナリ ログを削除したり、アップストリーム データベースの`expire_logs_days`を一時的に増やしたりしないでください。そうしないと、連続バイナリ ログの位置を取得できないため、ジョブが失敗する可能性があります。

### スケーリング手順 {#scaling-procedure}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データの移行]**をクリックします。

3.  **[データ移行]**ページで、スケーリングする移行ジョブを見つけます。 <strong>[アクション]</strong>列で、 <strong>[...]</strong> &gt; <strong>[拡大/縮小]</strong>をクリックします。

4.  **[拡大/縮小]**ウィンドウで、使用する新しい仕様を選択し、 <strong>[送信]</strong>をクリックします。ウィンドウの下部に、仕様の新しい価格が表示されます。
