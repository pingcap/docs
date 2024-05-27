---
title: Perform a Proof of Concept (PoC) with TiDB Cloud
summary: TiDB Cloudを使用して概念実証 (PoC) を実行する方法について説明します。
---

# TiDB Cloudで概念実証（PoC）を実行する {#perform-a-proof-of-concept-poc-with-tidb-cloud}

TiDB Cloud は、TiDB の優れた機能をすべて完全に管理されたクラウド データベースで提供する Database-as-a-Service (DBaaS) 製品です。データベースの複雑さに煩わされることなく、アプリケーションに集中できます。TiDB TiDB Cloudは現在、Amazon Web Services (AWS) と Google Cloud の両方で利用できます。

概念実証 (PoC) を開始することは、 TiDB Cloud がビジネス ニーズに最適かどうかを判断するための最良の方法です。また、短時間でTiDB Cloudの主要な機能に慣れることができます。パフォーマンス テストを実行することで、ワークロードがTiDB Cloudで効率的に実行できるかどうかを確認できます。また、データの移行や構成の調整に必要な労力を評価することもできます。

このドキュメントでは、一般的な PoC 手順について説明し、 TiDB Cloud PoC を迅速に完了できるように支援することを目的としています。これは、TiDB の専門家と大規模な顧客ベースによって検証されたベスト プラクティスです。

PoC に興味がある場合は、開始する前に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP に</a>お気軽にお問い合わせください。サポート チームがテスト プランの作成をお手伝いし、PoC 手順をスムーズに進めていきます。

あるいは、 [TiDBサーバーレスを作成する](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)実行してTiDB Cloudに慣れ、簡単に評価することもできます。TiDB Serverless には[特別利用規約](/tidb-cloud/select-cluster-tier.md#tidb-serverless-special-terms-and-conditions)という制限があることに注意してください。

## PoC手順の概要 {#overview-of-the-poc-procedures}

PoC の目的は、 TiDB Cloud がビジネス要件を満たしているかどうかをテストすることです。一般的な PoC は通常 14 日間続き、その間に PoC の完了に集中することが求められます。

典型的なTiDB Cloud PoC は次の手順で構成されます。

1.  成功基準を定義し、テスト計画を作成する
2.  作業負荷の特性を特定する
3.  PoC 用にサインアップして TiDB 専用クラスターを作成する
4.  スキーマとSQLを適応させる
5.  データをインポートする
6.  ワークロードを実行して結果を評価する
7.  その他の機能を見る
8.  環境をクリーンアップしてPoCを完了する

## ステップ1. 成功基準を定義し、テスト計画を作成する {#step-1-define-success-criteria-and-create-a-test-plan}

PoC を通じてTiDB Cloudを評価する場合は、ビジネス ニーズに基づいて関心のあるポイントと対応する技術評価基準を決定し、PoC に対する期待と目標を明確にすることをお勧めします。詳細なテスト プランを備えた明確で測定可能な技術基準により、重要な側面に焦点を当て、ビジネス レベルの要件をカバーし、最終的に PoC 手順を通じて回答を得ることができます。

PoC の目標を特定するには、次の質問を参考にしてください。

-   ワークロードのシナリオは何ですか?
-   あなたのビジネスのデータセットのサイズやワークロードはどれくらいですか? 成長率はどれくらいですか?
-   ビジネスクリティカルなスループットやレイテンシーの要件を含むパフォーマンス要件は何ですか?
-   許容可能な最小限の計画的または計画外のダウンタイムを含む、可用性と安定性の要件は何ですか?
-   運用効率に必要な指標は何ですか? それをどうやって測定しますか?
-   ワークロードのセキュリティとコンプライアンスの要件は何ですか?

成功基準とテスト計画の作成方法の詳細については、お気軽に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP まで</a>お問い合わせください。

## ステップ2. ワークロードの特性を特定する {#step-2-identify-characteristics-of-your-workload}

TiDB Cloud は、大量のデータで高可用性と強力な一貫性を必要とするさまざまなユースケースに適しています。 [TiDB の紹介](https://docs.pingcap.com/tidb/stable/overview)に主要な機能とシナリオを示します。これらがビジネス シナリオに当てはまるかどうかを確認できます。

-   水平方向のスケールアウトまたはスケールイン
-   金融グレードの高可用性
-   リアルタイムHTAP
-   MySQLプロトコルおよびMySQLエコシステムと互換性があります

分析処理の高速化に役立つ列指向storageエンジンである[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)使用にも興味があるかもしれません。PoC 中は、いつでもTiFlash機能を使用できます。

## ステップ3. PoC用のTiDB専用クラスターにサインアップして作成する {#step-3-sign-up-and-create-a-tidb-dedicated-cluster-for-the-poc}

PoC 用の[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターを作成するには、次の手順を実行します。

1.  次のいずれかの方法で PoC 申請フォームに記入します。

    -   PingCAPウェブサイトの[PoCを申請する](https://pingcap.com/apply-for-poc/)ページ目に進み、申し込みフォームに記入してください。
    -   [TiDB Cloudコンソール](https://tidbcloud.com/)で、右下隅の**[?]**をクリックし、 **[営業担当者に問い合わせ]**をクリックして、 **[PoC を申請]**を選択し、申請フォームに入力します。

    フォームを送信すると、 TiDB Cloudサポート チームが申請を確認し、お客様に連絡し、申請が承認されるとクレジットをお客様のアカウントに振り込みます。また、PingCAP サポート エンジニアに連絡して PoC 手順を支援してもらい、PoC が可能な限りスムーズに実行されるようにすることもできます。

2.  PoC 用の TiDB 専用クラスターを作成するには、 [TiDB専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

クラスターを作成する前に、クラスターのサイズを決定するための容量計画を行うことをお勧めします。TiDB、TiKV、またはTiFlashノードの推定数から始めて、後でパフォーマンス要件を満たすようにクラスターをスケールアウトすることができます。詳細については、次のドキュメントを参照するか、サポート チームにお問い合わせください。

-   推定方法の詳細については、 [TiDB のサイズ](/tidb-cloud/size-your-cluster.md)参照してください。
-   TiDB 専用クラスターの構成については、 [TiDB専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。TiDB、TiKV、 TiFlash (オプション) のクラスター サイズをそれぞれ構成します。
-   PoC クレジットの消費を効果的に計画し、最適化する方法については、このドキュメントの[FAQ](#faq)参照してください。
-   スケーリングの詳細については、 [TiDBクラスタを拡張する](/tidb-cloud/scale-tidb-cluster.md)参照してください。

専用の PoC クラスターが作成されると、データを読み込んで一連のテストを実行する準備が整います。TiDB クラスターに接続する方法については、 [TiDB専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

新しく作成されたクラスターの場合は、次の構成に注意してください。

-   デフォルトのタイムゾーン（ダッシュボードの**「作成時間」**列）は UTC です。 [ローカルタイムゾーンを設定する](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)手順に従って、ローカルタイムゾーンに変更できます。
-   新しいクラスターのデフォルトのバックアップ設定は、毎日データベース全体をバックアップすることです。希望するバックアップ時間を指定するか、データを手動でバックアップすることができます。デフォルトのバックアップ時間と詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)参照してください。

## ステップ4. スキーマとSQLを適応させる {#step-4-adapt-your-schemas-and-sql}

次に、テーブルやインデックスを含むデータベース スキーマを TiDB クラスターにロードできます。

PoC クレジットの数量には限りがあるため、クレジットの価値を最大化するために、 TiDB Cloud上で互換性テストや予備分析用の[TiDB サーバーレス クラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)を作成することをお勧めします。

TiDB Cloud はMySQL 8.0 と高い互換性があります。データが MySQL と互換性があるか、MySQL と互換性を持つように調整できる場合は、データを TiDB に直接インポートできます。

互換性の詳細については、次のドキュメントを参照してください。

-   [TiDB と MySQL の互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility) 。
-   [MySQLとは異なるTiDBの機能](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql) 。
-   [TiDB のキーワードと予約語](https://docs.pingcap.com/tidb/stable/keywords) 。
-   [TiDB の制限](https://docs.pingcap.com/tidb/stable/tidb-limitations) 。

以下にベストプラクティスをいくつか示します。

-   スキーマ設定に非効率性がないか確認します。
-   不要なインデックスを削除します。
-   効果的なパーティショニングのためにパーティショニング ポリシーを計画します。
-   タイムスタンプ上のインデックスなど、右側のインデックスの増加によって発生する[ホットスポットの問題](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)回避します。
-   [シャード行IDビット](https://docs.pingcap.com/tidb/stable/shard-row-id-bits)と[自動ランダム](https://docs.pingcap.com/tidb/stable/auto-random)を使って[ホットスポットの問題](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)回避します。

SQL ステートメントの場合、データ ソースと TiDB の互換性のレベルに応じて調整する必要がある場合があります。

ご不明な点がございましたら[ピンキャップ](/tidb-cloud/tidb-cloud-support.md)ご相談ください。

## ステップ5. データのインポート {#step-5-import-data}

小さなデータセットをインポートして実現可能性をすばやくテストすることも、大きなデータセットをインポートして TiDB データ移行ツールのスループットをテストすることもできます。TiDB はサンプル データを提供していますが、実際のビジネス ワークロードでテストを実行することを強くお勧めします。

さまざまな形式のデータをTiDB Cloudにインポートできます。

-   [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
-   [ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)
-   [SQLファイル形式でサンプルデータをインポートする](/tidb-cloud/import-sample-data.md)
-   [Amazon S3 または GCS から CSV ファイルをインポートする](/tidb-cloud/import-csv-files.md)
-   [Apache Parquet ファイルのインポート](/tidb-cloud/import-parquet-files.md)

> **注記：**
>
> **インポート**ページでのデータのインポートでは追加の請求料金は発生しません。

## ステップ6. ワークロードを実行して結果を評価する {#step-6-run-your-workload-and-evaluate-results}

これで、環境の作成、スキーマの調整、データのインポートが完了しました。次はワークロードをテストします。

ワークロードをテストする前に、必要に応じてデータベースを元の状態に復元できるように、手動バックアップを実行することを検討してください。詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)参照してください。

ワークロードを開始した後、次の方法を使用してシステムを観察できます。

-   クラスターのよく使用されるメトリクスは、クラスターの概要ページにあります。これには、合計 QPS、レイテンシ、接続、 TiFlash要求 QPS、 TiFlash要求期間、 TiFlashストレージ サイズ、TiKV ストレージ サイズ、TiDB CPU、TiKV CPU、TiKV IO 読み取り、および TiKV IO 書き込みが含まれます。 [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)参照してください。
-   **「診断」 &gt; 「ステートメント」**に移動すると、SQL 実行を観察し、システム テーブルをクエリせずにパフォーマンスの問題を簡単に見つけることができます。3 [ステートメント分析](/tidb-cloud/tune-performance.md)参照してください。
-   **「診断」 &gt; 「キー ビジュアライザー」**に移動すると、TiDB データ アクセス パターンとデータ ホットスポットを表示できます。3 [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)参照してください。
-   これらのメトリクスを独自の Datadog および Prometheus に統合することもできます。 [サードパーティの監視統合](/tidb-cloud/third-party-monitoring-integrations.md)参照してください。

次はテスト結果を評価する時です。

より正確な評価を得るには、テスト前にメトリクスのベースラインを決定し、実行ごとにテスト結果を適切に記録します。結果を分析することで、 TiDB Cloud がアプリケーションに適しているかどうかを判断できます。また、これらの結果はシステムの実行状態を示しており、メトリクスに応じてシステムを調整できます。例:

-   システム パフォーマンスが要件を満たしているかどうかを評価します。合計 QPS とレイテンシーを確認します。システム パフォーマンスが満足できるものでない場合は、次のようにパフォーマンスを調整できます。

    -   ネットワークレイテンシーを監視および最適化します。
    -   SQL パフォーマンスを調査して調整します。
    -   モニターと[ホットスポットの問題を解決する](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues) 。

-   storageサイズと CPU 使用率を評価し、それに応じて TiDB クラスターをスケール アウトまたはスケール インします。スケーリングの詳細については、セクション[FAQ](#faq)を参照してください。

パフォーマンス チューニングのヒントを次に示します。

-   書き込みパフォーマンスの向上

    -   TiDB クラスターをスケールアウトして書き込みスループットを向上させます ( [TiDBクラスタのスケール](/tidb-cloud/scale-tidb-cluster.md)を参照)。
    -   [楽観的取引モデル](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model)を使用してロックの競合を減らします。

-   クエリパフォーマンスの向上

    -   **「診断 &gt; ステートメント」**ページで SQL 実行プランを確認します。
    -   **ダッシュボード &gt; キー ビジュアライザー**ページでホットスポットの問題を確認します。
    -   **「概要 &gt; 容量メトリック」**ページで、TiDB クラスターの容量が不足していないかどうかを監視します。
    -   TiFlash機能を使用して分析処理を最適化します。 [HTAPクラスタを使用する](/tiflash/tiflash-overview.md)参照してください。

## ステップ7. その他の機能を調べる {#step-7-explore-more-features}

ワークロードのテストが完了したら、アップグレードやバックアップなどのその他の機能を調べることができます。

-   アップグレード

    TiDB Cloud は定期的に TiDB クラスターをアップグレードしますが、サポート チケットを送信してクラスターのアップグレードをリクエストすることもできます。 [TiDBクラスタのアップグレード](/tidb-cloud/upgrade-tidb-cluster.md)参照してください。

-   バックアップ

    ベンダー ロックインを回避するには、毎日のフル バックアップを使用してデータを新しいクラスターに移行し、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用してデータをエクスポートします。詳細については、 [TiDB専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)および[TiDB専用データのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md#backup)を参照してください。

## ステップ8. 環境をクリーンアップしてPoCを完了する {#step-8-clean-up-the-environment-and-finish-the-poc}

実際のワークロードを使用してTiDB Cloudをテストし、テスト結果を取得したら、PoC の完全なサイクルが完了します。これらの結果は、TiDB Cloudが期待どおりであるかどうかを判断するのに役立ちます。その間に、 TiDB Cloudの使用に関するベスト プラクティスが蓄積されました。

TiDB Cloud をより大規模に試してみたい場合、つまりTiDB Cloudが提供する他のノードstorageサイズを使用してデプロイするなど、新しい一連のデプロイとテストを行う場合は、 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターを作成してTiDB Cloudへのフル アクセスを取得してください。

クレジットがなくなり、PoC を継続したい場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してご相談ください。

PoC を終了し、テスト環境を削除することはいつでも可能です。詳細については、 [TiDBクラスタを削除する](/tidb-cloud/delete-tidb-cluster.md)参照してください。

PoC プロセス、機能リクエスト、製品の改善方法など、サポート チームへのフィードバックは、 [TiDB Cloudフィードバック フォーム](https://www.surveymonkey.com/r/L3VVW8R)にご記入いただくと大変助かります。

## FAQ {#faq}

### 1. データのバックアップと復元にはどのくらいの時間がかかりますか? {#1-how-long-does-it-take-to-back-up-and-restore-my-data}

TiDB Cloud、自動バックアップと手動バックアップの 2 種類のデータベース バックアップが提供されています。どちらの方法でも、データベース全体がバックアップされます。

データのバックアップと復元にかか​​る時間は、テーブルの数、ミラー コピーの数、CPU 使用率のレベルによって異なります。1 つの TiKV ノードでのバックアップと復元の速度は、約 50 MB/秒です。

データベースのバックアップと復元操作は通常、CPU を集中的に使用するため、常に追加の CPU リソースが必要になります。この環境の CPU 集中度に応じて、QPS とトランザクションのレイテンシーに影響 (10% ～ 50%) が及ぶ可能性があります。

### 2. スケールアウトとスケールインはいつ行う必要がありますか? {#2-when-do-i-need-to-scale-out-and-scale-in}

スケーリングに関する考慮事項は次のとおりです。

-   ピーク時間中またはデータのインポート中に、ダッシュボードの容量メトリックが上限に達したことが確認された場合 ( [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)を参照)、クラスターをスケールアウトする必要がある可能性があります。
-   リソースの使用量が持続的に低い場合 (たとえば、CPU 使用率が 10% ～ 20% のみ)、クラスターをスケールインしてリソースを節約できます。

コンソールでクラスターを自分でスケールアウトできます。クラスターをスケールインする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)連絡してサポートを受ける必要があります。スケーリングの詳細については、 [TiDBクラスタを拡張する](/tidb-cloud/scale-tidb-cluster.md)を参照してください。サポート チームと連絡を取り合って、正確な進行状況を追跡することができます。データの再バランス調整によりパフォーマンスに影響する可能性があるため、テストを開始する前にスケーリング操作が完了するまで待つ必要があります。

### 3. PoC クレジットを最大限に活用するにはどうすればよいですか? {#3-how-to-make-the-best-use-of-my-poc-credits}

PoC の申請が承認されると、アカウントにクレジットが付与されます。通常、クレジットは 14 日間の PoC に十分な量です。クレジットは、ノードの種類とノードの数に応じて、時間単位で課金されます。詳細については、 [TiDB Cloud課金](/tidb-cloud/tidb-cloud-billing.md#credits)参照してください。

PoC に残っているクレジットを確認するには、次のスクリーンショットに示すように、対象プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

![TiDB Cloud PoC Credits](/media/tidb-cloud/poc-points.png)

または、<mdsvgicon name="icon-top-organization"> TiDB Cloudコンソールの左下隅で、 **[請求] を**クリックし、 **[クレジット]**をクリックしてクレジットの詳細ページを表示します。</mdsvgicon>

クレジットを節約するには、使用していないクラスターを削除します。現在、クラスターを停止することはできません。クラスターを削除する前に、バックアップが最新であることを確認する必要があります。そうすれば、後で PoC を再開するときにクラスターを復元できます。

PoC プロセスが完了した後も未使用のクレジットが残っている場合は、そのクレジットの有効期限が切れていない限り、引き続きそのクレジットを使用して TiDB クラスターの料金を支払うことができます。

### 4. PoC を完了するのに 2 週間以上かかることはありますか? {#4-can-i-take-more-than-2-weeks-to-complete-a-poc}

PoC の試用期間を延長したい場合、またはクレジットが不足している場合は、 [PingCAPに連絡する](https://www.pingcap.com/contact-us/)にお問い合わせください。

### 5. 技術的な問題で行き詰まっています。PoC のサポートを受けるにはどうすればよいですか? {#5-i-m-stuck-with-a-technical-problem-how-do-i-get-help-for-my-poc}

いつでも[TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)を求めることができます。
