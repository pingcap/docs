---
title: Perform a Proof of Concept (PoC) with TiDB Cloud
summary: Learn about how to perform a Proof of Concept (PoC) with TiDB Cloud.
---

# TiDB Cloudで概念実証（PoC）を実行する {#perform-a-proof-of-concept-poc-with-tidb-cloud}

TiDB Cloudは、フルマネージドクラウドデータベースでTiDBの優れた機能をすべて提供するサービスとしてのデータベース（DBaaS）製品です。これは、データベースの複雑さではなく、アプリケーションに集中するのに役立ちます。 TiDB Cloudは現在、Amazon Web Services（AWS）とGoogle Cloud Platform（GCP）の両方で利用できます。

概念実証（PoC）を開始することは、 TiDB Cloudがビジネスニーズに最適であるかどうかを判断するための最良の方法です。また、 TiDB Cloudの主要な機能を短時間で理解できるようになります。パフォーマンステストを実行することで、ワークロードがTiDB Cloudで効率的に実行できるかどうかを確認できます。また、データを移行して構成を適応させるために必要な作業を評価することもできます。

このドキュメントでは、一般的なPoC手順について説明し、 TiDB CloudPoCをすばやく完了するのに役立つことを目的としています。これは、TiDBの専門家と大規模な顧客ベースによって検証されたベストプラクティスです。

PoCの実行に興味がある場合は、開始する前に<a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>に連絡してください。サポートチームは、テストプランの作成を支援し、PoC手順をスムーズにガイドします。

または、 [開発者層を作成する](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster) （1年間の無料トライアル）してTiDB Cloudに慣れ、簡単に評価することもできます。開発者層には[特別利用規約](/tidb-cloud/select-cluster-tier.md#developer-tier-special-terms-and-conditions)あることに注意してください。

## PoC手順の概要 {#overview-of-the-poc-procedures}

PoCの目的は、 TiDB Cloudがビジネス要件を満たしているかどうかをテストすることです。通常のPoCは通常14日間続き、その間、PoCの完了に集中することが期待されます。

一般的なTiDB Cloudは、次の手順で構成されています。

1.  成功基準を定義し、テスト計画を作成します
2.  ワークロードの特性を特定する
3.  サインアップして、PoC専用のクラスタを作成します
4.  スキーマとSQLを適応させる
5.  データのインポート
6.  ワークロードを実行して結果を評価する
7.  その他の機能を探す
8.  環境をクリーンアップし、PoCを終了します

## ステップ1.成功基準を定義し、テスト計画を作成します {#step-1-define-success-criteria-and-create-a-test-plan}

PoCを介してTiDB Cloudを評価する場合は、ビジネスニーズに基づいて関心のあるポイントと対応する技術評価基準を決定し、PoCに対する期待と目標を明確にすることをお勧めします。詳細なテスト計画を備えた明確で測定可能な技術基準は、主要な側面に焦点を合わせ、ビジネスレベルの要件をカバーし、最終的にPoC手順を通じて回答を得るのに役立ちます。

次の質問を使用して、PoCの目標を特定します。

-   あなたのワークロードのシナリオは何ですか？
-   あなたのビジネスのデータセットサイズまたはワークロードはどれくらいですか？成長率はどれくらいですか？
-   ビジネスクリティカルなスループットまたは遅延要件を含む、パフォーマンス要件は何ですか？
-   許容可能な最小の計画的または計画外のダウンタイムを含む、可用性と安定性の要件は何ですか？
-   運用効率に必要な指標は何ですか？それらをどのように測定しますか？
-   ワークロードのセキュリティとコンプライアンスの要件は何ですか？

成功基準とテストプランの作成方法の詳細については、 <a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>にお気軽にお問い合わせください。

## ステップ2.ワークロードの特性を特定する {#step-2-identify-characteristics-of-your-workload}

TiDB Cloudは、高可用性と大量のデータとの強力な一貫性を必要とするさまざまなユースケースに適しています。 [TiDBの紹介](https://docs.pingcap.com/tidb/stable/overview)に、主要な機能とシナリオを示します。それらがビジネスシナリオに適用されるかどうかを確認できます。

-   水平方向のスケールアウトまたはスケールイン
-   金融グレードの高可用性
-   リアルタイムHTAP
-   MySQL 5.7プロトコルおよびMySQLエコシステムと互換性があります

また、分析処理の高速化に役立つ列型ストレージエンジンである[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)の使用にも興味があるかもしれません。 PoC中は、いつでもTiFlash機能を使用できます。

## ステップ3.サインアップして、PoC専用のクラスタを作成します {#step-3-sign-up-and-create-a-dedicated-cluster-for-the-poc}

PoC専用のクラスタを作成するには、次の手順を実行します。

1.  次のいずれかを実行して、PoCアプリケーションフォームに入力します。

    -   すでに[開発者層を作成しました](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)つ（1年間の無料トライアル）をお持ちの場合は、PoCアプリケーションの送信に関するプロンプトバーがTiDB Cloudコンソールに表示されます。バーのPoCアプリケーションリンクをクリックして、PoCアプリケーションフォームに入力できます。
    -   開発者層をまだ作成していない場合は、 [PoCに申し込む](https://en.pingcap.com/apply-for-poc/)ページに移動してPoCアプリケーションフォームに記入してください。

    フォームを送信すると、 TiDB Cloudサポートチームがアプリケーションを確認して連絡し、アプリケーションが承認されるとトライアルポイントをアカウントに転送します。また、PingCAPサポートエンジニアに連絡して、PoCの手順を支援し、PoCが可能な限りスムーズに実行されるようにすることもできます。

2.  PoCの[専用層](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタを作成するには、 [クイックスタート](/tidb-cloud/tidb-cloud-quickstart.md)を参照してください。

クラスタを作成する前に、クラスタのサイズ設定に容量計画を立てることをお勧めします。 TiDB、TiKV、またはTiFlashノードの推定数から始めて、後でクラスタをスケールアウトしてパフォーマンス要件を満たすことができます。詳細については、次のドキュメントを参照するか、サポートチームにご相談ください。

-   推定方法の詳細については、 [TiDBのサイズを設定する](/tidb-cloud/size-your-cluster.md)を参照してください。
-   専用クラスタの構成については、 [TiDBクラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。 TiDB、TiKV、およびTiFlash（オプション）のクラスタサイズをそれぞれ構成します。
-   PoCトライアルポイントの消費を効果的に計画および最適化する方法については、このドキュメントの[FAQ](#faq)を参照してください。
-   スケーリングの詳細については、 [TiDBクラスターをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

専用のPoCクラスタが作成されると、データをロードして一連のテストを実行する準備が整います。 TiDBクラスタに接続する方法については、 [TiDBクラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

新しく作成されたクラスタの場合、次の構成に注意してください。

-   デフォルトのタイムゾーン（ダッシュボードの[時間の**作成**]列）はUTCです。 [ローカルタイムゾーンを設定する](/tidb-cloud/manage-user-access.md#set-the-local-time-zone)を実行すると、ローカルタイムゾーンに変更できます。
-   新しいクラスタのデフォルトのバックアップ設定は、毎日のデータベースの完全バックアップです。優先バックアップ時間を指定するか、データを手動でバックアップできます。デフォルトのバックアップ時間と詳細については、 [TiDBクラスターデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#backup)を参照してください。

## ステップ4.スキーマとSQLを適応させる {#step-4-adapt-your-schemas-and-sql}

次に、テーブルとインデックスを含むデータベーススキーマをTiDBクラスタにロードできます。

PoCトライアルポイントの数には限りがあるため、トライアルポイントの価値を最大化するには、 TiDB Cloudでの互換性テストと予備分析のために[開発者層クラスタ](/tidb-cloud/select-cluster-tier.md#developer-tier) （1年間の無料トライアル）を作成することをお勧めします。

TiDB CloudはMySQL5.7と高い互換性がありMySQL 5.7。データがMySQLと互換性がある場合、またはMySQLと互換性があるように適合できる場合は、データをTiDBに直接インポートできます。

互換性の詳細については、次のドキュメントを参照してください。

-   [TiDBとMySQLの互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility) 。
-   [MySQLとは異なるTiDB機能](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql) 。
-   [TiDBのキーワードと予約語](https://docs.pingcap.com/tidb/stable/keywords) 。
-   [TiDBの制限](https://docs.pingcap.com/tidb/stable/tidb-limitations) 。

ここにいくつかのベストプラクティスがあります：

-   スキーマのセットアップに非効率性があるかどうかを確認してください。
-   不要なインデックスを削除します。
-   効果的なパーティショニングのためのパーティショニングポリシーを計画します。
-   タイムスタンプのインデックスなど、右側のインデックスの増加によって引き起こされる[ホットスポットの問題](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)は避けてください。
-   [SHARD_ROW_ID_BITS](https://docs.pingcap.com/tidb/stable/shard-row-id-bits)と[AUTO_RANDOM](https://docs.pingcap.com/tidb/stable/auto-random)を使用して[ホットスポットの問題](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)を避けます。

SQLステートメントの場合、データソースとTiDBとの互換性のレベルに応じて、それらを適合させる必要がある場合があります。

ご不明な点がございましたら、 [PingCAP](/tidb-cloud/tidb-cloud-support.md)までお問い合わせください。

## ステップ5.データをインポートする {#step-5-import-data}

小さなデータセットをインポートして実現可能性をすばやくテストしたり、大きなデータセットをインポートしてTiDBデータ移行ツールのスループットをテストしたりできます。 TiDBはサンプルデータを提供しますが、ビジネスの実際のワークロードでテストを実行することを強くお勧めします。

さまざまな形式のデータをTiDB Cloudにインポートできます。

-   [TiDBDumpling形式でサンプルデータをインポートする](/tidb-cloud/import-sample-data.md)
-   [Auroraから移行する](/tidb-cloud/migrate-from-aurora-bulk-import.md)
-   [AmazonS3またはGCSからCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)
-   [ApacheParquetファイルをインポートする](/tidb-cloud/import-parquet-files.md)

> **ノート：**
>
> -   TiDB Cloudでサポートされている文字照合については、 [MySQL互換データベースからの移行](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。データが元々どのように保存されているかを理解することは非常に役立ちます。
> -   **[データインポートタスク]**ページでのデータインポートでは、追加の請求料金は発生しません。

## ステップ6.ワークロードを実行し、結果を評価します {#step-6-run-your-workload-and-evaluate-results}

これで、環境が作成され、スキーマが適合され、データがインポートされました。ワークロードをテストする時が来ました。

ワークロードをテストする前に、手動バックアップの実行を検討してください。これにより、必要に応じてデータベースを元の状態に復元できます。詳細については、 [TiDBクラスターデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#backup)を参照してください。

ワークロードを開始した後、次の方法を使用してシステムを監視できます。

-   クラスターの一般的に使用されるメトリックは、クラスタの概要ページにありクラスタ。これには、合計QPS、レイテンシー、接続、TiFlash要求QPS、TiFlash要求期間、TiFlashストレージサイズ、TiKVストレージサイズ、TiDB CPU、TiKV CPU、TiKV IO読み取り、およびTiKVIO書き込み。 [TiDBクラスターを監視する](/tidb-cloud/monitor-tidb-cluster.md)を参照してください。
-   **[診断]&gt;[ステートメント]**に移動します。ここで、SQLの実行を監視し、システムテーブルにクエリを実行せずにパフォーマンスの問題を簡単に見つけることができます。 [ステートメント分析](/tidb-cloud/tune-performance.md)を参照してください。
-   **[診断]&gt;[キービジュア**ライザー]に移動します。ここで、TiDBデータアクセスパターンとデータホットスポットを表示できます。 [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)を参照してください。
-   これらのメトリックを独自のDatadogおよびPrometheusに統合することもできます。 [サードパーティの統合](/tidb-cloud/monitor-tidb-cluster.md#third-party-integrations)を参照してください。

次に、テスト結果を評価します。

より正確な評価を取得するには、テストの前にメトリックベースラインを決定し、実行ごとにテスト結果を適切に記録します。結果を分析することで、 TiDB Cloudがアプリケーションに適しているかどうかを判断できます。一方、これらの結果はシステムの実行ステータスを示しており、メトリックに従ってシステムを調整できます。例えば：

-   システムパフォーマンスが要件を満たしているかどうかを評価します。合計QPSとレイテンシーを確認してください。システムパフォーマンスが不十分な場合は、次のようにパフォーマンスを調整できます。

    -   ネットワーク遅延を監視および最適化します。
    -   SQLのパフォーマンスを調査して調整します。
    -   モニターと[ホットスポットの問題を解決する](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues) 。

-   ストレージサイズとCPU使用率を評価し、それに応じてTiDBクラスタでスケールアウトまたはスケールアウトします。スケーリングの詳細については、 [FAQ](#faq)セクションを参照してください。

パフォーマンスチューニングのヒントは次のとおりです。

-   書き込みパフォーマンスを向上させる

    -   TiDBクラスターをスケールアウトして書き込みスループットを向上させます（ [TiDBクラスターをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照）。
    -   [楽観的なトランザクションモデル](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model)を使用して、ロックの競合を減らします。

-   クエリのパフォーマンスを向上させる

    -   **[診断]&gt;[ステートメント]**ページでSQL実行プランを確認します。
    -   **[ダッシュボード]&gt;[キービジュアライザー]**ページでホットスポットの問題を確認します。
    -   **[概要]&gt;[容量メトリック**]ページで、TiDBクラスタの容量が不足していないかどうかを監視します。
    -   TiFlash機能を使用して、分析処理を最適化します。 [HTAPクラスターを使用する](/tidb-cloud/use-htap-cluster.md)を参照してください。

## ステップ7.その他の機能を調べる {#step-7-explore-more-features}

これでワークロードのテストが終了しました。アップグレードやバックアップなど、より多くの機能を調べることができます。

-   アップグレード

    TiDB Cloudは定期的にTiDBクラスターをアップグレードしますが、クラスターへのアップグレードをリクエストするためのサポートチケットを送信することもできます。 [TiDBクラスターをアップグレードする](/tidb-cloud/upgrade-tidb-cluster.md)を参照してください。

-   バックアップ

    ベンダーロックインを回避するために、毎日の完全バックアップを使用してデータを新しいクラスタに移行し、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用してデータをエクスポートできます。詳細については、 [TiDBからデータをエクスポートする](/tidb-cloud/export-data-from-tidb-cloud.md)を参照してください。

## ステップ8.環境をクリーンアップし、PoCを終了します {#step-8-clean-up-the-environment-and-finish-the-poc}

実際のワークロードを使用してTiDB Cloudをテストし、テスト結果を取得した後、PoCの全サイクルを完了しました。これらの結果は、 TiDB Cloudが期待を満たしているかどうかを判断するのに役立ちます。その間、 TiDB Cloudを使用するためのベストプラクティスを蓄積しました。

TiDB Cloudをより大規模に試してみたい場合は、 TiDB Cloudが提供する他のストレージサイズでの展開など、新しいラウンドの展開とテストのために、 [専用層](/tidb-cloud/select-cluster-tier.md#dedicated-tier)を作成してTiDB Cloudへのフルアクセスを取得します。

トライアルポイントが不足していて、PoCを続行したい場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡して相談してください。

PoCを終了し、いつでもテスト環境を削除できます。詳細については、 [TiDBクラスターを削除する](/tidb-cloud/delete-tidb-cluster.md)を参照してください。

PoCプロセス、機能のリクエスト、製品の改善方法など、 [TiDB Cloudフィードバックフォーム](https://www.surveymonkey.com/r/L3VVW8R)を入力することで、サポートチームへのフィードバックを高く評価しています。

## FAQ {#faq}

### 1.データのバックアップと復元にはどのくらい時間がかかりますか？ {#1-how-long-does-it-take-to-back-up-and-restore-my-data}

TiDB Cloudは、自動バックアップと手動バックアップの2種類のデータベースバックアップを提供します。どちらの方法でも、データベース全体がバックアップされます。

データのバックアップと復元にかかる時間は、テーブルの数、ミラーコピーの数、CPUを集中的に使用するレベルなどによって異なる場合があります。 1つのTiKVノードでのバックアップと復元の速度は約50MB/秒です。

データベースのバックアップおよび復元操作は通常、CPUを集中的に使用し、常に追加のCPUリソースを必要とします。この環境のCPU負荷度によっては、QPSとトランザクション遅延に影響（10％から50％）が生じる可能性があります。

### 2.いつスケールアウトしてスケールインする必要がありますか？ {#2-when-do-i-need-to-scale-out-and-scale-in}

スケーリングに関する考慮事項は次のとおりです。

-   ピーク時またはデータのインポート中に、ダッシュボードの容量メトリックが上限に達していることを確認した場合（ [TiDBクラスターを監視する](/tidb-cloud/monitor-tidb-cluster.md)を参照）、クラスタをスケールアウトする必要がある場合があります。
-   リソース使用率が永続的に低い場合（たとえば、CPU使用率の10％〜20％のみ）、クラスタでスケーリングしてリソースを節約できます。

コンソールでクラスターを自分でスケールアウトできます。クラスタでスケーリングする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してサポートを受ける必要があります。スケーリングの詳細については、 [TiDBクラスターをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照してください。正確な進捗状況を追跡するために、サポートチームと連絡を取り合うことができます。データのリバランスによりパフォーマンスに影響を与える可能性があるため、テストを開始する前にスケーリング操作が終了するのを待つ必要があります。

### 3. PoCトライアルポイントを最大限に活用するにはどうすればよいですか？ {#3-how-to-make-the-best-use-of-my-poc-trial-points}

PoCの申請が承認されると、アカウントにトライアルポイントが付与されます。通常、14日間のPoCにはトライアルポイントで十分です。トライアルポイントは、ノードの種類とノード数に応じて1時間ごとに課金されます。詳細については、 [TiDB Cloud請求](/tidb-cloud/tidb-cloud-billing.md#trial-points)を参照してください。

PoCに残されたポイントを確認するには、次のスクリーンショットに示すように、[**アクティブクラスター]**ページに移動します。

![TiDB Cloud PoC Points](/media/tidb-cloud/poc-points.png)

ポイントを保存するには、使用していないクラスタを削除します。現在、クラスタを停止することはできません。クラスタを削除する前に、バックアップが最新であることを確認する必要があります。これにより、後でPoCを再開するときにクラスタを復元できます。

### 4. PoCを完了するのに2週間以上かかることはありますか？ {#4-can-i-take-more-than-2-weeks-to-complete-a-poc}

PoCトライアル期間を延長したい場合、またはトライアルポイントが不足している場合は、 [PingCAP](https://en.pingcap.com/contact-us/)にお問い合わせください。

### 5.技術的な問題で立ち往生しています。 PoCのヘルプを取得するにはどうすればよいですか？ {#5-i-m-stuck-with-a-technical-problem-how-do-i-get-help-for-my-poc}

いつでも[PingCAP](/tidb-cloud/tidb-cloud-support.md)に連絡して支援を求めることができます。
