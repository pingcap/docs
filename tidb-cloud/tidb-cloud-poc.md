---
title: Perform a Proof of Concept (PoC) with TiDB Cloud
summary: TiDB Cloudを使用して概念実証 (PoC) を実行する方法について説明します。
---

# TiDB Cloudで概念実証 (PoC) を実行する {#perform-a-proof-of-concept-poc-with-tidb-cloud}

TiDB Cloudは、TiDBの優れた機能をすべて備えたフルマネージドクラウドデータベースを提供するDatabase-as-a-Service（DBaaS）製品です。データベースの複雑な管理に煩わされることなく、アプリケーション開発に集中できます。<customcontent language="en,zh"> TiDB Cloudは現在、Amazon Web Services (AWS)、Google Cloud、Microsoft Azure、Alibaba Cloud で利用できます。</customcontent><customcontent language="ja"> TiDB Cloudは現在、Amazon Web Services (AWS)、Google Cloud、Microsoft Azure で利用できます。</customcontent>

TiDB Cloudがお客様のビジネスニーズに最適かどうかを判断するには、概念実証（PoC）を開始することが最善の方法です。また、短期間でTiDB Cloudの主要な機能に慣れることができます。パフォーマンステストを実行することで、ワークロードがTiDB Cloud上で効率的に実行できるかどうかを確認できます。さらに、データの移行や構成の調整に必要な労力を評価することもできます。

このドキュメントでは、一般的なPoC手順を説明し、 TiDB Cloud PoCを迅速に完了できるように支援します。これは、TiDBの専門家と大規模な顧客ベースによって検証されたベストプラクティスです。

PoCにご興味をお持ちでしたら、開始前に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>までお気軽にお問い合わせください。サポートチームがテストプランの作成をお手伝いし、PoCの手順をスムーズに進めていきます。

あるいは、 [TiDB Cloudスターターを作成する](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster) TiDB Cloudに慣れて、すぐに評価することもできます。TiDB TiDB Cloud Starter には[特別な利用規約](/tidb-cloud/serverless-limitations.md)含まれています。

## PoC手順の概要 {#overview-of-the-poc-procedures}

PoCの目的は、 TiDB Cloudがお客様のビジネス要件を満たしているかどうかをテストすることです。典型的なPoCは通常14日間続き、その間、お客様はPoCの完了に集中していただくことになります。

一般的なTiDB Cloud PoC は次の手順で構成されます。

1.  成功基準を定義し、テスト計画を作成する
2.  ワークロードの特性を特定する
3.  PoC 用にTiDB Cloud専用クラスターをサインアップして作成します
4.  スキーマとSQLを適応させる
5.  データのインポート
6.  ワークロードを実行して結果を評価する
7.  その他の機能を見る
8.  環境をクリーンアップしてPoCを完了する

## ステップ1. 成功基準を定義し、テスト計画を作成する {#step-1-define-success-criteria-and-create-a-test-plan}

TiDB CloudをPoCで評価する際には、ビジネスニーズに基づいて評価ポイントとそれに対応する技術評価基準を決定し、PoCにおける期待と目標を明確にすることをお勧めします。明確かつ測定可能な技術基準と詳細なテスト計画があれば、重要な側面に焦点を当て、ビジネスレベルの要件をカバーし、最終的にPoCプロセスを通じて回答を得ることができます。

PoC の目標を特定するには、次の質問を参考にしてください。

-   ワークロードのシナリオは何ですか?
-   あなたのビジネスのデータセットのサイズやワークロードはどれくらいですか？成長率はどれくらいですか？
-   ビジネスクリティカルなスループットやレイテンシー要件を含むパフォーマンス要件は何ですか?
-   許容可能な最小限の計画的または計画外のダウンタイムを含む、可用性と安定性の要件は何ですか?
-   業務効率化に必要な指標は何ですか？どのように測定しますか？
-   ワークロードのセキュリティとコンプライアンスの要件は何ですか?

成功基準とテスト計画の作成方法の詳細については、お気軽に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>までお問い合わせください。

## ステップ2. ワークロードの特性を特定する {#step-2-identify-characteristics-of-your-workload}

TiDB Cloudは、高可用性と大容量データの強力な一貫性が求められる様々なユースケースに適しています。1 [TiDBの紹介](https://docs.pingcap.com/tidb/stable/overview)主要な機能とシナリオをリストアップしました。ご自身のビジネスシナリオに当てはまるかどうか、以下からご確認ください。

-   水平方向のスケールアウトまたはスケールイン
-   金融グレードの高可用性
-   リアルタイムHTAP
-   MySQLプロトコルおよびMySQLエコシステムと互換性があります

分析処理の高速化に役立つ列指向storageエンジンである[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)ご利用もご検討いただけるかもしれません。PoC期間中は、 TiFlash機能をいつでもご利用いただけます。

## ステップ3. PoC用のTiDB Cloud専用クラスターにサインアップして作成する {#step-3-sign-up-and-create-a-tidb-cloud-dedicated-cluster-for-the-poc}

PoC 用の[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを作成するには、次の手順を実行します。

1.  次のいずれかの方法で PoC 申請フォームに記入します。

    -   PingCAPウェブサイトの[PoCに申し込む](https://pingcap.com/apply-for-poc/)ページ目に進み、申込書にご記入ください。
    -   [TiDB Cloudコンソール](https://tidbcloud.com/)で、右下隅の**[?]**をクリックし、 **[営業担当者に問い合わせ**] をクリックして、 **[PoC の申請]**を選択し、申請フォームに入力します。

    フォームを送信すると、 TiDB Cloudサポートチームが申請内容を確認し、ご連絡いたします。申請が承認され次第、アカウントにクレジットが付与されます。また、PingCAP サポートエンジニアにご連絡いただければ、PoC の手順をサポートし、PoC がスムーズに実行されるようサポートいたします。

2.  PoC 用のTiDB Cloud Dedicated クラスターを作成するには、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

    > **注記：**
    >
    > TiDB Cloud Dedicated クラスターを作成する前に、次のいずれかの支払い方法を追加する必要があります。
    >
    > -   クラスター作成ページの画面上の指示に従って、クレジットカードを追加します。
    > -   電信送金で支払うには、 TiDB Cloudサポート チームにお問い合わせください。
    > -   クラウド マーケットプレイス (AWS、Azure、または Google Cloud) を通じてTiDB Cloudにサインアップし、クラウド プロバイダー アカウントを使用して支払います。
    >
    > PoC クレジットは、PoC 期間中に発生した対象費用を相殺するために自動的に使用されます。

クラスタを作成する前に、クラスタのサイズを決定するためのキャパシティプランニングを行うことをお勧めします。TiDB、TiKV、またはTiFlashノードの数を概算し、パフォーマンス要件に合わせてクラスタをスケールアウトすることも可能です。詳細については、以下のドキュメントをご覧いただくか、サポートチームにお問い合わせください。

-   見積りの実践の詳細については、 [TiDBのサイズ](/tidb-cloud/size-your-cluster.md)参照してください。
-   TiDB Cloud Dedicated クラスターの構成については、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。TiDB、TiKV、 TiFlash (オプション) のクラスター サイズをそれぞれ構成します。
-   PoC クレジットの消費を効果的に計画し最適化する方法については、このドキュメントの[FAQ](#faq)参照してください。
-   スケーリングの詳細については、 [TiDBクラスタのスケール](/tidb-cloud/scale-tidb-cluster.md)参照してください。

専用のPoCクラスターを作成したら、データをロードして一連のテストを実行する準備が整います。TiDBクラスターへの接続方法については、 [TiDB Cloud専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)ご覧ください。

新しく作成されたクラスターの場合は、次の構成に注意してください。

-   デフォルトのタイムゾーン（ダッシュボードの**「作成時間」**列）はUTCです。以下の手順[ローカルタイムゾーンを設定する](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)で、ローカルタイムゾーンに変更できます。
-   新しいクラスタのデフォルトのバックアップ設定は、毎日データベース全体のバックアップです。希望するバックアップ時間を指定するか、手動でデータをバックアップすることもできます。デフォルトのバックアップ時間および詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)参照してください。

## ステップ4. スキーマとSQLを適応させる {#step-4-adapt-your-schemas-and-sql}

次に、テーブルやインデックスを含むデータベース スキーマを TiDB クラスターにロードできます。

PoC クレジットの数量には限りがあるため、クレジットの価値を最大化するために、 TiDB Cloud上で互換性テストや予備分析用の[TiDB Cloudスターター クラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)作成することをお勧めします。

TiDB CloudはMySQL 8.0との互換性が非常に高くなっています。MySQLと互換性がある、またはMySQLと互換性を持たせることができる場合は、データをTiDBに直接インポートできます。

互換性の詳細については、次のドキュメントを参照してください。

-   [TiDBとMySQLの互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility) 。
-   [MySQLとは異なるTiDBの機能](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql) 。
-   [TiDBのキーワードと予約語](https://docs.pingcap.com/tidb/stable/keywords) 。
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

小規模なデータセットをインポートして実現可能性を迅速にテストすることも、大規模なデータセットをインポートしてTiDBデータ移行ツールのスループットをテストすることもできます。TiDBはサンプルデータを提供していますが、実際の業務ワークロードでテストを実施することを強くお勧めします。

TiDB Cloudにはさまざまな形式のデータをインポートできます。

-   [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
-   [ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)
-   [SQL ファイル形式でサンプルデータをインポートする](/tidb-cloud/import-sample-data.md)
-   [クラウドストレージからCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)
-   [Apache Parquet ファイルのインポート](/tidb-cloud/import-parquet-files.md)

> **注記：**
>
> **「インポート」**ページでのデータのインポートでは追加の請求料金は発生しません。

## ステップ6. ワークロードを実行して結果を評価する {#step-6-run-your-workload-and-evaluate-results}

これで環境の作成、スキーマの調整、データのインポートが完了しました。次はワークロードをテストしましょう。

ワークロードをテストする前に、必要に応じてデータベースを元の状態に復元できるように、手動バックアップを実行することを検討してください。詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)参照してください。

ワークロードを開始した後、次の方法を使用してシステムを観察できます。

-   クラスターのよく使用されるメトリクスは、クラスター概要ページで確認できます。これには、合計QPS、レイテンシ、接続数、 TiFlashリクエストQPS、 TiFlashリクエスト期間、 TiFlashストレージサイズ、TiKVストレージサイズ、TiDB CPU、TiKV CPU、TiKV IO読み取り、TiKV IO書き込みが含まれます[TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)参照してください。
-   クラスターの[**診断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)ページに移動し、 **「SQLステートメント」**タブを確認してください。ここでは、システムテーブルをクエリすることなくSQL実行を監視し、パフォーマンスの問題を簡単に特定できます[ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)参照してください。
-   クラスターの[**診断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)ページに移動し、 **「Key Visualizer」**タブを確認します。ここで、TiDBのデータアクセスパターンとデータホットスポットを確認できます。5 [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)参照してください。
-   これらのメトリクスを、お客様独自のDatadogおよびPrometheusに統合することも可能です。1 [サードパーティの監視統合](/tidb-cloud/third-party-monitoring-integrations.md)ご覧ください。

次はテスト結果を評価する時です。

より正確な評価を行うには、テスト前にメトリクスのベースラインを決定し、各実行のテスト結果を適切に記録してください。結果を分析することで、 TiDB Cloudがアプリケーションに適しているかどうかを判断できます。また、これらの結果はシステムの実行状態を示しており、メトリクスに応じてシステムを調整できます。例えば、

-   システムパフォーマンスが要件を満たしているかどうかを評価します。合計QPSとレイテンシーを確認します。システムパフォーマンスが満足できるものでない場合は、以下の手順でパフォーマンスを調整できます。

    -   ネットワークレイテンシーを監視し、最適化します。
    -   SQL パフォーマンスを調査して調整します。
    -   モニターと[ホットスポットの問題を解決する](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues) 。

-   storageサイズとCPU使用率を評価し、それに応じてTiDBクラスターをスケールアウトまたはスケールインしてください。スケーリングの詳細については、セクション[FAQ](#faq)を参照してください。

パフォーマンス チューニングのヒントを次に示します。

-   書き込みパフォーマンスの向上

    -   TiDB クラスターをスケールアウトして書き込みスループットを向上させます ( [TiDBクラスタのスケール](/tidb-cloud/scale-tidb-cluster.md)参照)。
    -   [楽観的取引モデル](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model)使用してロックの競合を減らします。

-   クエリパフォーマンスの向上

    -   [**診断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)ページの[**SQL文**](/tidb-cloud/tune-performance.md#statement-analysis)タブで SQL 実行プランを確認します。
    -   [**診断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)ページの[**キービジュアライザー**](/tidb-cloud/tune-performance.md#key-visualizer)タブでホットスポットの問題を確認します。
    -   [**メトリクス**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページで TiDB クラスターの容量が不足していないかどうかを監視します。
    -   TiFlash機能を使用して分析処理を最適化します。1 [HTAPクラスタを使用する](/tiflash/tiflash-overview.md)参照してください。

## ステップ7. その他の機能を調べる {#step-7-explore-more-features}

ワークロードのテストが完了したら、アップグレードやバックアップなどのその他の機能を調べることができます。

-   アップグレード

    TiDB CloudはTiDBクラスタを定期的にアップグレードします。また、サポートチケットを送信してクラスタのアップグレードをリクエストすることもできます。1 [TiDBクラスタのアップグレード](/tidb-cloud/upgrade-tidb-cluster.md)ご覧ください。

-   バックアップ

    ベンダーロックインを回避するには、毎日フルバックアップを使用してデータを新しいクラスタに移行し、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用してデータをエクスポートします。詳細については、 [TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)と[TiDB Cloud StarterまたはEssentialでデータをバックアップおよび復元する](/tidb-cloud/backup-and-restore-serverless.md)参照してください。

## ステップ8. 環境をクリーンアップしてPoCを完了する {#step-8-clean-up-the-environment-and-finish-the-poc}

実際のワークロードを使用してTiDB Cloudをテストし、テスト結果を取得することで、PoCサイクル全体が完了しました。これらの結果は、 TiDB Cloudが期待どおりに機能しているかどうかを判断するのに役立ちます。同時に、 TiDB Cloudの活用に関するベストプラクティスも蓄積されました。

TiDB Cloud をより大規模に試してみたい場合、つまりTiDB Cloudが提供する他のノードstorageサイズを使用してデプロイするなど、新しい一連のデプロイとテストを行う場合は、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを作成してTiDB Cloudへのフル アクセスを取得してください。

クレジットがなくなり、PoC を継続したい場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)連絡してご相談ください。

PoCはいつでも終了し、テスト環境を削除できます。詳細については、 [TiDBクラスタを削除する](/tidb-cloud/delete-tidb-cluster.md)ご覧ください。

PoC プロセス、機能のリクエスト、製品の改善方法など、サポート チームへのフィードバックは、 [TiDB Cloudフィードバックフォーム](https://www.surveymonkey.com/r/L3VVW8R)にご記入いただくと大変助かります。

## FAQ {#faq}

### 1. データのバックアップと復元にはどのくらいの時間がかかりますか? {#1-how-long-does-it-take-to-back-up-and-restore-my-data}

TiDB Cloud は、自動バックアップと手動バックアップの 2 種類のデータベースバックアップを提供しています。どちらの方法でも、データベース全体がバックアップされます。

データのバックアップとリストアにかかる時間は、テーブル数、ミラーコピー数、CPU負荷レベルによって異なります。単一のTiKVノードにおけるバックアップとリストアの速度は約50MB/秒です。

データベースのバックアップとリストア操作は通常、CPUを大量に消費するため、常に追加のCPUリソースを必要とします。環境のCPU負荷に応じて、QPSとトランザクションレイテンシーに10%～50%の影響を与える可能性があります。

### 2. スケールアウトとスケールインはいつ行う必要がありますか? {#2-when-do-i-need-to-scale-out-and-scale-in}

スケーリングに関する考慮事項は次のとおりです。

-   ピーク時間中またはデータのインポート中に、ダッシュボードの容量メトリックが上限に達したことが確認された場合 ( [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)参照)、クラスターをスケールアウトする必要がある可能性があります。
-   リソースの使用量が持続的に低い場合（たとえば、CPU 使用率が 10% ～ 20% のみ）は、クラスターをスケールインしてリソースを節約できます。

コンソール上でクラスターをスケールアウトできます。クラスターをスケールインする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。スケーリングの詳細については、 [TiDBクラスタのスケール](/tidb-cloud/scale-tidb-cluster.md)ご覧ください。サポートチームに連絡して、正確な進捗状況を追跡することができます。スケーリング操作はデータの再バランス調整によってパフォーマンスに影響を与える可能性があるため、テストを開始する前に完了するまでお待ちください。

### 3. PoC クレジットを最大限に活用するにはどうすればよいですか? {#3-how-to-make-the-best-use-of-my-poc-credits}

PoCの申請が承認されると、アカウントにクレジットが付与されます。通常、このクレジットは14日間のPoCに十分な量です。クレジットは、ノードの種類と数に応じて、時間単位で課金されます。詳細については、 [TiDB Cloud課金](/tidb-cloud/tidb-cloud-billing.md#credits)ご覧ください。

PoC の合計クレジット数、利用可能なクレジット数、現在のクレジット使用量を確認するには、 TiDB Cloudコンソールの左上隅にあるコンボ ボックスを使用して対象組織に切り替え、左側のナビゲーション ペインで**[請求]**をクリックし、 **[クレジット]**タブをクリックします。

クレジットを節約するには、使用していないクラスターを削除してください。現在、クラスターを停止することはできません。クラスターを削除する前に、バックアップが最新であることを確認してください。そうすれば、後でPoCを再開する際にクラスターを復元できます。

PoC プロセスが完了した後も未使用のクレジットが残っている場合は、そのクレジットの有効期限が切れない限り、引き続きそのクレジットを使用して TiDB クラスターの料金を支払うことができます。

### 4. PoC を完了するのに 2 週間以上かかることはありますか? {#4-can-i-take-more-than-2-weeks-to-complete-a-poc}

PoC の試用期間を延長したい場合、またはクレジットが不足している場合は、 [PingCAPに連絡する](https://www.pingcap.com/contact-us/)お問い合わせください。

### 5. 技術的な問題で行き詰まっています。PoCのサポートを受けるにはどうすればいいですか？ {#5-i-m-stuck-with-a-technical-problem-how-do-i-get-help-for-my-poc}

[TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)でも助けを求めることができます。
