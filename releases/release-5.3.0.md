---
title: TiDB 5.3 Release Notes
---

# TiDB 5.3 リリースノート {#tidb-5-3-release-notes}

発売日：2021年11月30日

TiDB バージョン: 5.3.0

v5.3 の主な新機能または改善点は次のとおりです。

-   一時テーブルを導入してアプリケーション ロジックを簡素化し、パフォーマンスを向上させる
-   テーブルとパーティションの属性設定をサポート
-   システムのセキュリティを強化するために、TiDB ダッシュボードで最小限の権限を持つユーザーの作成をサポート
-   TiDB のタイムスタンプ処理フローを最適化して、全体的なパフォーマンスを向上させます
-   TiDB データ移行 (DM) のパフォーマンスを強化して、データが MySQL から TiDB に低レイテンシーで移行されるようにします。
-   複数のTiDB Lightningインスタンスを使用した並列インポートをサポートして、完全なデータ移行の効率を向上させます
-   単一の SQL ステートメントでクラスターのオンサイト情報の保存と復元をサポートし、実行計画に関連する問題のトラブルシューティングの効率を向上させます。
-   データベース パフォーマンスの可観測性を向上させるために、継続的なプロファイリングの実験的機能をサポートします。
-   システムのパフォーマンスと安定性を向上させるために、storageとコンピューティング エンジンの最適化を継続する
-   Raftstoreスレッド プールから I/O 操作を分離することにより、TiKV の書き込みレイテンシーを削減します (デフォルトでは無効)

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v5.3.0 にアップグレードする場合、すべての中間バージョンの互換性の変更点を知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                               | タイプを変更 | 説明                                                                                                                                                                                                                                                                                    |
| :---------------------------------------------------------------------------------------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)                        | 修正済み   | 一時テーブルが TiDB でサポートされるようになったため、 `CREATE TEMPORARY TABLE`と`DROP TEMPORARY TABLE` `tidb_enable_noop_functions`を有効にする必要がなくなりました。                                                                                                                                                          |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) | 新規追加   | テーブルの統計が期限切れになったときのオプティマイザの動作を制御します。デフォルト値は`ON`です。テーブル内の変更された行の数が合計行の 80% を超える場合 (この比率は構成によって調整できます[`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) )、オプティマイザーは行の合計数以外の統計が信頼できなくなったと見なし、疑似を使用します。代わりに統計。値を`OFF`に設定すると、統計の有効期限が切れても、オプティマイザーは統計を引き続き使用します。 |
| [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)               | 新規追加   | TSO Follower Proxy 機能を有効にするか無効にするかを決定します。デフォルト値は`OFF`で、TSO Follower Proxy 機能が無効になっていることを意味します。現時点では、TiDB は PD リーダーからのみ TSO を取得します。この機能を有効にすると、TiDB は TSO の取得時にすべての PD ノードにリクエストを均等に送信します。その後、PD フォロワーは TSO 要求を転送して、PD リーダーの CPU 負荷を軽減します。                                             |
| [`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)     | 新規追加   | TiDB が PD から TSO を要求するときのバッチ保存操作の最大待機時間を設定します。デフォルト値は`0`です。これは、追加の待機がないことを意味します。                                                                                                                                                                                                      |
| [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)                             | 新規追加   | 1 つの[一時テーブル](/temporary-tables.md)の最大サイズを制限します。一時テーブルがこのサイズを超えると、エラーが発生します。                                                                                                                                                                                                           |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                       | タイプを変更 | 説明                                                                                                                                                                                                   |
| :------------- | :------------------------------------------------------------------------------------------------- | :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`prepared-plan-cache.capacity`](/tidb-configuration-file.md#capacity)                             | 修正済み   | キャッシュされたステートメントの数を制御します。デフォルト値が`100`から`1000`に変更されました。                                                                                                                                                |
| TiKV           | [`storage.reserve-space`](/tikv-configuration-file.md#reserve-space)                               | 修正済み   | TiKV の起動時にディスク保護用に確保される領域を制御します。 v5.3.0から、予約容量の80%は、ディスク容量が不足した場合の運用や保守に必要な追加のディスク容量として使用され、残りの20%は一時ファイルの保存に使用されます。                                                                                 |
| TiKV           | `memory-usage-limit`                                                                               | 修正済み   | この構成項目は TiDB v5.3.0 の新機能で、その値はstorage.block-cache.capacity に基づいて計算されます。                                                                                                                              |
| TiKV           | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)       | 新規追加   | Raft I/O タスクを処理するスレッドの許容数。これは StoreWriter スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。 |
| TiKV           | [`raftstore.raft-write-size-limit`](/tikv-configuration-file.md#raft-write-size-limit-new-in-v530) | 新規追加   | Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの構成項目の値より大きい場合、データはディスクに書き込まれます。 `raftstore.store-io-pool-size`の値が`0`の場合、この構成アイテムは有効になりません。                                                                    |
| TiKV           | `raftstore.raft-msg-flush-interval`                                                                | 新規追加   | Raftメッセージがバッチで送信される間隔を決定します。バッチ内のRaftメッセージは、この構成項目で指定された間隔ごとに送信されます。 `raftstore.store-io-pool-size`の値が`0`の場合、この構成アイテムは有効になりません。                                                                      |
| TiKV           | `raftstore.raft-reject-transfer-leader-duration`                                                   | 削除しました | Leaderが新しく追加されたノードに転送される最小期間を決定します。                                                                                                                                                                  |
| PD             | [`log.file.max-days`](/pd-configuration-file.md#max-days)                                          | 修正済み   | ログが保持される最大日数を制御します。デフォルト値が`1`から`0`に変更されました。                                                                                                                                                          |
| PD             | [`log.file.max-backups`](/pd-configuration-file.md#max-backups)                                    | 修正済み   | 保持されるログの最大数を制御します。デフォルト値が`7`から`0`に変更されました。                                                                                                                                                           |
| PD             | [`patrol-region-interval`](/pd-configuration-file.md#patrol-region-interval)                       | 修正済み   | replicaChecker がリージョンのヘルス状態をチェックする実行頻度を制御します。この値が小さいほど、replicaChecker の実行速度は速くなります。通常、このパラメータを調整する必要はありません。デフォルト値が`100ms`から`10ms`に変更されました。                                                           |
| PD             | [`max-snapshot-count`](/pd-configuration-file.md#max-snapshot-count)                               | 修正済み   | 1 つのストアが同時に受信または送信するスナップショットの最大数を制御します。 PD スケジューラは、この構成に依存して、通常のトラフィックに使用されるリソースが横取りされるのを防ぎます。デフォルト値が`3`から`64`に変更されました。                                                                              |
| PD             | [`max-pending-peer-count`](/pd-configuration-file.md#max-pending-peer-count)                       | 修正済み   | 1 つのストアで保留中のピアの最大数を制御します。 PD スケジューラーは、この構成に依存して、一部のノードで古いログを持つリージョンが生成されるのを防ぎます。デフォルト値が`16`から`64`に変更されました。                                                                                           |
| TiDライトニング      | `meta-schema-name`                                                                                 | 新規追加   | 各TiDB Lightningインスタンスのメタ情報がターゲット クラスタに格納されるスキーマ名。デフォルト値は「lightning_metadata」です。                                                                                                                      |

### その他 {#others}

-   一時テーブル:

    -   v5.3.0 より前の TiDB クラスターでローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスターが v5.3.0 以降のバージョンにアップグレードされた後は通常のテーブルとして扱われます。 v5.3.0 以降のバージョンの TiDB クラスターでグローバル一時テーブルを作成した場合、v5.3.0 より前のバージョンにクラスターをダウングレードすると、これらのテーブルは通常のテーブルとして扱われ、データ エラーが発生します。
    -   v5.3.0 以降、TiCDC とBR は[グローバル一時テーブル](/temporary-tables.md#global-temporary-tables)をサポートしています。 v5.3.0 より前のバージョンの TiCDC およびBR を使用して、グローバル一時テーブルを下流に複製すると、テーブル定義エラーが発生します。
    -   次のクラスターは、v5.3.0 以降であると予想されます。そうしないと、グローバル一時テーブルを作成するときにデータ エラーが報告されます。

        -   TiDB 移行ツールを使用してインポートされるクラスター
        -   TiDB 移行ツールを使用して復元されたクラスター
        -   TiDB 移行ツールを使用したレプリケーション タスクのダウンストリーム クラスター
    -   一時テーブルの互換性情報については、 [MySQL 一時テーブルとの互換性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)および[他の TiDB 機能との互換性の制限](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)を参照してください。

-   v5.3.0 より前のリリースでは、システム変数が不正な値に設定されていると、TiDB がエラーを報告します。 v5.3.0 以降のリリースでは、システム変数が不正な値に設定されている場合、TiDB は &quot;|Warning | 1292 | Truncated illegal xxx: &#39;xx&#39;&quot; などの警告で成功を返します。

-   `SHOW CREATE VIEW`の実行に`SHOW VIEW`権限が必要ない問題を修正します。これで、 `SHOW CREATE VIEW`ステートメントを実行するための`SHOW VIEW`パーミッションが必要になります。

-   システム変数`sql_auto_is_null`が noop関数に追加されます。 `tidb_enable_noop_functions = 0/OFF`の場合、この変数値を変更するとエラーが発生します。

-   `GRANT ALL ON performance_schema.*`構文は許可されなくなりました。このステートメントを TiDB で実行すると、エラーが発生します。

-   v5.3.0 より前に新しいインデックスが追加された場合、指定された期間外に自動分析が予期せずトリガーされる問題を修正します。 v5.3.0 では、変数`tidb_auto_analyze_start_time`と変数`tidb_auto_analyze_end_time`で期間を設定すると、この期間中にのみ自動分析がトリガーされます。

-   プラグインのデフォルトのstorageディレクトリが`""`から`/data/deploy/plugin`に変更されました。

-   DM コードは[TiCDCコードリポジトリのフォルダ「dm」](https://github.com/pingcap/tiflow/tree/master/dm)に移行されます。現在、DM はバージョン番号で TiDB に従います。 v2.0.x に続く新しい DM バージョンは v5.3.0 で、リスクなしで v2.0.x から v5.3.0 にアップグレードできます。

-   デフォルトでデプロイされた Prometheus のバージョンは v2.8.1 から[v2.27.1](https://github.com/prometheus/prometheus/releases/tag/v2.27.1)にアップグレードされ、2021 年 5 月にリリースされます。このバージョンでは、より多くの機能が提供され、セキュリティの問題が修正されています。 Prometheus v2.8.1 と比較すると、v2.27.1 のアラート時間の表現は Unix タイムスタンプから UTC に変更されています。詳細については、 [プロメテウスコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)を参照してください。

## 新機能 {#new-features}

### SQL {#sql}

-   **SQL インターフェースを使用してデータの配置ルールを設定する (実験的機能)**

    データの配置規則を設定するための SQL インターフェイスを提供する`[CREATE | ALTER] PLACEMENT POLICY`構文をサポートします。この機能を使用すると、特定のリージョン、データ センター、ラック、ホスト、またはレプリカ カウント ルールに合わせてテーブルとパーティションをスケジュールするように指定できます。これにより、低コストと高い柔軟性を求めるアプリケーションの要求が満たされます。一般的なユーザー シナリオは次のとおりです。

    -   異なるアプリケーションの複数のデータベースをマージして、データベース メンテナンスのコストを削減し、ルール構成によってアプリケーション リソースの分離を実現します。
    -   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます
    -   新しいデータを SSD に保存し、古いデータを HHD に保存して、データのアーカイブとstorageのコストを削減
    -   ホットスポット データのリーダーを高性能 TiKV インスタンスにスケジュールする
    -   コールド データを低コストのstorageメディアに分離して、コスト効率を向上させる

    [ユーザー文書](/placement-rules-in-sql.md) 、 [#18030](https://github.com/pingcap/tidb/issues/18030)

-   **一時テーブル**

    一時テーブルを作成する`CREATE [GLOBAL] TEMPORARY TABLE`ステートメントをサポートします。この機能を使用すると、アプリケーションの計算プロセスで生成される一時データを簡単に管理できます。一時データはメモリに格納され、 `tidb_tmp_table_max_size`変数を使用して一時テーブルのサイズを制限できます。 TiDB は、次のタイプの一時テーブルをサポートしています。

    -   グローバル一時テーブル
        -   クラスタ内のすべてのセッションに表示され、テーブル スキーマは永続的です。
        -   トランザクション レベルのデータ分離を提供します。一時データはトランザクション内でのみ有効です。トランザクションが終了すると、データは自動的に削除されます。
    -   ローカル一時テーブル

        -   現在のセッションにのみ表示され、テーブル スキーマは永続的ではありません。
        -   重複したテーブル名をサポートします。アプリケーションの複雑な命名規則を設計する必要はありません。
        -   セッション レベルのデータ分離を提供し、より単純なアプリケーション ロジックを設計できるようにします。トランザクションが終了すると、一時テーブルは削除されます。

        [ユーザー文書](/temporary-tables.md) 、 [#24169](https://github.com/pingcap/tidb/issues/24169)

-   **`FOR UPDATE OF TABLES`構文のサポート**

    複数のテーブルを結合する SQL ステートメントの場合、TiDB は`OF TABLES`に含まれるテーブルに関連付けられた行に対する悲観的ロックの取得をサポートします。

    [ユーザー文書](/sql-statements/sql-statement-select.md) 、 [#28689](https://github.com/pingcap/tidb/issues/28689)

-   **テーブル属性**

    テーブルまたはパーティションの属性を設定できる`ALTER TABLE [PARTITION] ATTRIBUTES`ステートメントをサポートします。現在、TiDB は`merge_option`属性の設定のみをサポートしています。このアトリビュートを追加することで、リージョンマージの動作を明示的に制御できます。

    ユーザー シナリオ: `SPLIT TABLE`操作を実行すると、(PD パラメーター[`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)によって制御される) 一定期間後にデータが挿入されない場合、空のリージョンがデフォルトで自動的にマージされます。この場合、テーブル属性を`merge_option=deny`に設定して、リージョンの自動マージを回避できます。

    [ユーザー文書](/table-attributes.md) 、 [#3839](https://github.com/tikv/pd/issues/3839)

### Security {#security}

-   **TiDB ダッシュボードで最小限の権限を持つユーザーの作成をサポート**

    TiDB ダッシュボードのアカウント システムは、 TiDB SQLのアカウント システムと一致しています。 TiDB ダッシュボードにアクセスするユーザーは、 TiDB SQLユーザーの権限に基づいて認証および承認されます。したがって、TiDB ダッシュボードには限定された権限、または単に読み取り専用権限が必要です。最小権限の原則に基づいて TiDB ダッシュボードにアクセスするようにユーザーを構成できるため、高い権限を持つユーザーのアクセスを回避できます。

    TiDB ダッシュボードにアクセスしてサインインするには、最小限の特権を持つ SQL ユーザーを作成することをお勧めします。これにより、権限の高いユーザーのアクセスが回避され、セキュリティが向上します。

    [ユーザー文書](/dashboard/dashboard-user.md)

### パフォーマンス {#performance}

-   **PD のタイムスタンプ処理フローを最適化する**

    TiDB は、PDFollowerプロキシを有効にし、PD クライアントが TSO をバッチで要求するときに必要なバッチ待機時間を変更することで、タイムスタンプ処理フローを最適化し、PD のタイムスタンプ処理負荷を軽減します。これにより、システム全体のスケーラビリティが向上します。

    -   システム変数[`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)による PD Follower Proxy の有効化または無効化をサポートします。 TSO 要求の PD の負荷が高すぎるとします。この場合、PD フォロワー プロキシを有効にすると、フォロワーの要求サイクル中に収集された TSO 要求をリーダー ノードにバッチ転送できます。このソリューションは、クライアントとリーダー間の直接的なやり取りの数を効果的に減らし、リーダーへの負荷のプレッシャーを軽減し、TiDB の全体的なパフォーマンスを向上させることができます。

    > **ノート：**
    >
    > クライアントの数が少なく、PD リーダーの CPU 負荷がフルでない場合、PDFollowerプロキシを有効にすることはお勧めしません。

    -   システム変数[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)を使用して、PD クライアントが要求 TSO をバッチ処理するために必要な最大待機時間を設定できるようになりました。この時間の単位はミリ秒です。 PD の TSO 要求の負荷が高い場合は、待機時間を増やしてバッチ サイズを大きくすることで、負荷を減らしてスループットを向上させることができます。

    > **ノート：**
    >
    > TSO 要求の負荷が高くない場合、この変数の値を変更することはお勧めできません。

    [ユーザー文書](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530) 、 [#3149](https://github.com/tikv/pd/issues/3149)

### 安定性 {#stability}

-   **一部のストアが完全に破損した後、オンラインの安全でない回復をサポートします (実験的機能)。**

    オンライン データ アンセーフ リカバリを実行する`pd-ctl unsafe remove-failed-stores`コマンドをサポートします。大多数のデータ レプリカで永続的な損傷 (ディスクの損傷など) などの問題が発生し、これらの問題によってアプリケーションのデータ範囲が読み取り不能または書き込み不能になったとします。この場合、PD に実装されている Online Unsafe Recovery 機能を使用してデータを回復し、データを再び読み取りまたは書き込み可能にすることができます。

    TiDB チームのサポートを受けて機能関連の操作を実行することをお勧めします。

    [ユーザー文書](/online-unsafe-recovery.md) 、 [#10483](https://github.com/tikv/tikv/issues/10483)

### データ移行 {#data-migration}

-   **DM レプリケーションのパフォーマンスが強化されました**

    MySQL から TiDB への低レイテンシーのデータ レプリケーションを保証するために、次の機能をサポートします。

    -   1 つの行に対する複数の更新を 1 つのステートメントに圧縮する
    -   複数の行のバッチ更新を 1 つのステートメントにマージする

-   **DM OpenAPI を追加して、DM クラスターをより適切に維持します (実験的機能)。**

    DM は、DM クラスターを照会および操作するための OpenAPI 機能を提供します。 [dmctl ツール](/dm/dmctl-introduction.md)の特徴に似ています。

    現在、DM OpenAPI は実験的機能であり、デフォルトで無効になっています。本番環境で使用することはお勧めしません。

    [ユーザー文書](/dm/dm-open-api.md)

-   **TiDB Lightning並行インポート**

    TiDB Lightning は、元の機能を拡張するための並列インポート機能を提供します。複数の Lightning インスタンスを同時にデプロイして、単一のテーブルまたは複数のテーブルを下流の TiDB に並行してインポートできます。顧客の使用方法を変えることなく、データ移行機能が大幅に向上し、よりリアルタイムな方法でデータを移行して、さらに処理、統合、分析できるようになります。これにより、企業のデータ管理の効率が向上します。

    私たちのテストでは、10 個のTiDB Lightningインスタンスを使用して、合計 20 個の TiB MySQL データを 8 時間以内に TiDB にインポートできました。複数テーブルのインポートのパフォーマンスも向上しています。単一のTiDB Lightningインスタンスは 250 GiB/h でインポートをサポートでき、全体的な移行は元のパフォーマンスの 8 倍高速です。

    [ユーザー文書](/tidb-lightning/tidb-lightning-distributed-import.md)

-   **TiDB Lightning事前チェック**

    TiDB Lightning は、移行タスクを実行する前に構成を確認する機能を提供します。デフォルトで有効になっています。この機能は、ディスク容量と実行構成の定期的なチェックを自動的に実行します。主な目的は、後続のインポート プロセス全体がスムーズに進むようにすることです。

    [ユーザー文書](/tidb-lightning/tidb-lightning-prechecks.md)

-   **TiDB Lightning がGBK 文字セットのファイルのインポートをサポート**

    ソース データ ファイルの文字セットを指定できます。 TiDB Lightning は、インポート プロセス中にソース ファイルを指定された文字セットから UTF-8 エンコーディングに変換します。

    [ユーザー文書](/tidb-lightning/tidb-lightning-configuration.md)

-   **同期差分インスペクターの改善**

    -   比較速度を 375 MB/s から 700 MB/s に改善
    -   比較時に TiDB ノードのメモリ消費量をほぼ半分に削減
    -   ユーザー インターフェイスを最適化し、比較中にプログレス バーを表示する

    [ユーザー文書](/sync-diff-inspector/sync-diff-inspector-overview.md)

### 診断効率 {#diagnostic-efficiency}

-   **クラスターのオンサイト情報の保存と復元**

    TiDB クラスターの問題を特定してトラブルシューティングを行う場合、多くの場合、システムとクエリ プランに関する情報を提供する必要があります。より便利で効率的な方法で情報を取得し、クラスターの問題をトラブルシューティングするのに役立つように、TiDB v5.3.0 で`PLAN REPLAYER`コマンドが導入されました。このコマンドを使用すると、クラスタのオンサイト情報を簡単に保存および復元でき、トラブルシューティングの効率が向上し、管理の問題をより簡単にアーカイブできます。

    `PLAN REPLAYER`の特徴は以下の通りです。

    -   オンサイト トラブルシューティングでの TiDB クラスターの情報をstorage用の ZIP 形式のファイルにエクスポートします。
    -   別の TiDB クラスターからエクスポートされた ZIP 形式のファイルをクラスターにインポートします。このファイルには、オンサイト トラブルシューティングでの後者の TiDB クラスターの情報が含まれています。

    [ユーザー文書](/sql-plan-replayer.md) 、 [#26325](https://github.com/pingcap/tidb/issues/26325)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   **TiCDC 最終整合性レプリケーション**

    TiCDC は、災害シナリオで最終的に一貫性のあるレプリケーション機能を提供します。プライマリ TiDB クラスターで災害が発生し、短期間でサービスを再開できない場合、TiCDC はセカンダリ クラスター内のデータの一貫性を確保する機能を提供する必要があります。一方、TiCDC は、ビジネスがトラフィックをセカンダリ クラスターにすばやく切り替えて、データベースが長時間使用できなくなり、ビジネスに影響を与えないようにする必要があります。

    この機能は、TiCDC をサポートして、TiDB クラスターからセカンダリ リレーショナル データベース TiDB/ Aurora/MySQL/MariaDB に増分データをレプリケートします。プライマリ クラスタがクラッシュした場合、災害前の TiCDC のレプリケーション ステータスが正常でレプリケーション ラグが小さいという条件を考えると、TiCDC はセカンダリ クラスタをプライマリ クラスタ内の特定のスナップショットに 5 分以内に復元できます。これにより、30 分未満のデータ損失が許容されます。つまり、RTO &lt;= 5 分、RPO &lt;= 30 分です。

    [ユーザー文書](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)

-   **TiCDC は、TiCDC タスクを管理するための HTTP プロトコル OpenAPI をサポートしています。**

    TiDB v5.3.0 以降、TiCDC OpenAPI は一般提供 (GA) 機能になります。本番環境で OpenAPI を使用して、TiCDC クラスターのクエリと操作を行うことができます。

### 展開とメンテナンス {#deployment-and-maintenance}

-   **継続的なプロファイリング (実験的機能)**

    TiDB ダッシュボードは、TiDB クラスターの実行中にインスタンスのパフォーマンス分析結果をリアルタイムで自動的に保存する継続的なプロファイリング機能をサポートしています。パフォーマンス分析結果をフレーム グラフで確認できるため、より見やすく、トラブルシューティングの時間が短縮されます。

    この機能はデフォルトで無効になっており、TiDB ダッシュボードの**継続的プロファイル**ページで有効にする必要があります。

    この機能は、 TiUP v1.7.0 以降を使用してアップグレードまたはインストールされたクラスターでのみ使用できます。

    [ユーザー文書](/dashboard/continuous-profiling.md)

## テレメトリー {#telemetry}

TiDB は、TEMPORARY TABLE 機能が使用されているかどうかに関する情報をテレメトリ レポートに追加します。これには、テーブル名やテーブル データは含まれません。

テレメトリの詳細と、この動作を無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。

## 削除された機能 {#removed-feature}

TiCDC v5.3.0 から、TiDB クラスター間の循環レプリケーション機能 (v5.0.0 の実験的機能) が削除されました。 TiCDC をアップグレードする前にこの機能を使用してデータをレプリケートしている場合、関連するデータはアップグレード後に影響を受けません。

## 改良点 {#improvements}

-   TiDB

    -   コプロセッサーがロックを検出したときに、影響を受ける SQL ステートメントをデバッグ・ログに表示します。これは、問題の診断に役立ちます[#27718](https://github.com/pingcap/tidb/issues/27718)
    -   SQL 論理レイヤー[#27247](https://github.com/pingcap/tidb/issues/27247)でデータをバックアップおよび復元する場合のバックアップおよび復元データのサイズの表示のサポート
    -   `tidb_analyze_version`が`2`の場合の ANALYZE のデフォルトの収集ロジックを改善して、収集を高速化し、リソースのオーバーヘッドを削減します。
    -   `ANALYZE TABLE table_name COLUMNS col_1, col_2, ... , col_n`構文を導入します。この構文では、幅の広いテーブルの列の一部についてのみ統計を収集できるため、統計収集の速度が向上します。

-   TiKV

    -   ディスク容量の保護を強化して、storageの安定性を向上させます

        ディスクの完全書き込みエラーが発生した場合に TiKV がパニックにpanic可能性があるという問題を解決するために、TiKV は 2 レベルのしきい値防御メカニズムを導入して、ディスクの残りのスペースが過剰なトラフィックによって使い果たされるのを防ぎます。さらに、このメカニズムは、しきい値がトリガーされたときにスペースを再利用する機能を提供します。残りのスペースのしきい値がトリガーされると、一部の書き込み操作が失敗し、TiKV はディスク フル エラーとディスク フル ノードのリストを返します。この場合、スペースを回復してサービスを復元するには、 `Drop/Truncate Table`実行するか、ノードをスケールアウトします。

    -   L0 フロー制御[#10879](https://github.com/tikv/tikv/issues/10879)のアルゴリズムを簡素化する

    -   raft クライアント モジュール[#10944](https://github.com/tikv/tikv/pull/10944)のエラー ログ レポートを改善します。

    -   ログ スレッドを改善して、パフォーマンスのボトルネックにならないようにする[#10841](https://github.com/tikv/tikv/issues/10841)

    -   書き込みクエリの統計タイプを追加する[#10507](https://github.com/tikv/tikv/issues/10507)

    -   Raftstoreスレッド プールから I/O 操作を分離することにより、書き込みレイテンシーを削減します (デフォルトでは無効)。チューニングの詳細については、 [TiKV スレッド プールのパフォーマンスを調整する](/tune-tikv-thread-performance.md) [#10540](https://github.com/tikv/tikv/issues/10540)を参照してください。

-   PD

    -   ホットスポット スケジューラ[#3869](https://github.com/tikv/pd/issues/3869)の QPS ディメンションに書き込みクエリのタイプを追加する
    -   スケジューラーのパフォーマンスを向上させるために、バランスリージョンスケジューラーの再試行制限を動的に調整するサポート[#3744](https://github.com/tikv/pd/issues/3744)
    -   TiDB ダッシュボードを v2021.10.08.1 に更新する[#4070](https://github.com/tikv/pd/pull/4070)
    -   エビクト リーダー スケジューラが異常なピアを持つリージョンをスケジュールできるようにサポートします[#4093](https://github.com/tikv/pd/issues/4093)
    -   スケジューラーの終了プロセスを高速化する[#4146](https://github.com/tikv/pd/issues/4146)

-   TiFlash

    -   TableScanオペレーターの実行効率を大幅に改善

    -   Exchangeオペレーターの実行効率を向上させる

    -   storageエンジンの GC 中の書き込み増幅とメモリ使用量を削減します (実験的機能)。

    -   TiFlashの再起動時のTiFlashの安定性と可用性を向上させ、再起動後のクエリ エラーの可能性を減らします。

    -   複数の新しい String および Time関数のMPP エンジンへのプッシュ ダウンをサポート

        -   文字列関数: LIKE パターン、FORMAT()、LOWER()、LTRIM()、RTRIM()、SUBSTRING_INDEX()、TRIM()、UCASE()、UPPER()
        -   数学関数: ROUND (decimal, int)
        -   日時関数: HOUR()、MICROSECOND()、MINUTE()、SECOND()、SYSDATE()
        -   型変換関数：CAST(time, real)
        -   集計関数: GROUP_CONCAT()、SUM(enum)

    -   512 ビット SIMD をサポート

    -   古いデータのクリーンアップ アルゴリズムを強化して、ディスク使用量を削減し、ファイルをより効率的に読み取る

    -   一部の Linux 以外のシステムで、ダッシュボードにメモリまたは CPU の情報が表示されない問題を修正します。

    -   TiFlashログ ファイルの命名スタイルを統一し (命名スタイルを TiKV の命名スタイルと一致させます)、logger.count および logger.size の動的変更をサポートします。

    -   列ベースのファイルのデータ検証機能を改善 (チェックサム、実験的機能)

-   ツール

    -   TiCDC

        -   Kafka シンク構成項目`MaxMessageBytes`のデフォルト値を 64 MB から 1 MB に減らして、大きなメッセージが Kafka Broker [#3104](https://github.com/pingcap/tiflow/pull/3104)によって拒否される問題を修正します。
        -   レプリケーション パイプラインのメモリ使用量を減らす[#2553](https://github.com/pingcap/tiflow/issues/2553) [#3037](https://github.com/pingcap/tiflow/pull/3037) [#2726](https://github.com/pingcap/tiflow/pull/2726)
        -   監視項目とアラートルールを最適化し、同期リンク、メモリGC、および株式データのスキャンプロセスの可観測性を向上させる[#2735](https://github.com/pingcap/tiflow/pull/2735) [#1606](https://github.com/pingcap/tiflow/issues/1606) [#3000](https://github.com/pingcap/tiflow/pull/3000) [#2985](https://github.com/pingcap/tiflow/issues/2985) [#2156](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが通常の場合、ユーザーの誤解を招くことを避けるために、過去のエラー メッセージは表示されません[#2242](https://github.com/pingcap/tiflow/issues/2242)

## バグの修正 {#bug-fixes}

-   TiDB

    -   間違った実行計画が原因で実行中に発生するエラーを修正します。パーティション化されたテーブルで集計演算子をプッシュダウンするときにスキーマ列の浅いコピーが原因で、間違った実行計画が発生する[#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)
    -   `plan cache` unsigned フラグの変更を検出できない問題を修正[#28254](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲[#28233](https://github.com/pingcap/tidb/issues/28233)の外にある場合の間違ったパーティションのプルーニングを修正します。
    -   Planner が`join`の無効なプランをキャッシュする場合がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   ハッシュ列の型が`enum` [#27893](https://github.com/pingcap/tidb/issues/27893)のときの間違った`IndexLookUpJoin`を修正
    -   アイドル状態の接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるというバッチ クライアントのバグを修正します[#27688](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲット クラスタでチェックサムの実行に失敗した場合のTiDB Lightningpanicの問題を修正します[#27686](https://github.com/pingcap/tidb/pull/27686)
    -   場合によっては`date_add`と`date_sub`関数の誤った結果を修正します[#27232](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式[#28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の間違った結果を修正
    -   MySQL 5.1 またはそれ以前のクライアント バージョン[#27855](https://github.com/pingcap/tidb/issues/27855)に接続する際の認証の問題を修正します。
    -   新しいインデックスが追加されたときに、指定された時間外にauto analyzeがトリガーされる可能性がある問題を修正します[#28698](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると無効になるバグを修正`tidb_snapshot` [#28683](https://github.com/pingcap/tidb/pull/28683)
    -   不足しているピア リージョンが多数あるクラスタでBRが機能しないというバグを修正します[#27534](https://github.com/pingcap/tidb/issues/27534)
    -   サポートされていない`cast` TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)に押し下げると`tidb_cast to Int32 is not supported`のような予期しないエラーが発生する問題を修正
    -   `%s value is out of range in '%s'`エラー メッセージ[#27964](https://github.com/pingcap/tidb/issues/27964)で`DECIMAL overflow`が欠落している問題を修正します。
    -   一部のまれなケースで MPP ノードの可用性検出が機能しないバグを修正します[#3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)を割り当てる際の`DATA RACE`問題を修正
    -   空`dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)を削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正
    -   MPP クエリ[#1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   MPP クエリ[#28149](https://github.com/pingcap/tidb/pull/28149)のエラー ログ`cannot found column in Schema column`の問題を修正します。
    -   TiFlashのシャットダウン時に TiDB がpanicになる問題を修正[#28096](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない 3DES (Triple Data Encryption Algorithm) ベースの TLS 暗号スイートのサポートを削除します[#27859](https://github.com/pingcap/tidb/pull/27859)
    -   事前チェック中に Lightning がオフラインの TiKV ノードに接続し、インポートの失敗を引き起こす問題を修正します[#27826](https://github.com/pingcap/tidb/pull/27826)
    -   テーブルに多数のファイルをインポートする場合、事前チェックに時間がかかりすぎる問題を修正します[#27605](https://github.com/pingcap/tidb/issues/27605)
    -   式を書き換えると`between`間違った照合順序を推論する問題を修正[#27146](https://github.com/pingcap/tidb/issues/27146)
    -   `group_concat`関数が照合順序[#27429](https://github.com/pingcap/tidb/issues/27429)を考慮していなかった問題を修正
    -   `extract`関数の引数が負の期間[#27236](https://github.com/pingcap/tidb/issues/27236)の場合に発生する結果の誤りを修正します。
    -   `NO_UNSIGNED_SUBTRACTION`を[#26765](https://github.com/pingcap/tidb/issues/26765)に設定するとパーティションの作成に失敗する問題を修正
    -   列の刈り込みと集計のプッシュダウンで副作用のある式を避ける[#27106](https://github.com/pingcap/tidb/issues/27106)
    -   無駄な gRPC ログを削除する[#24190](https://github.com/pingcap/tidb/issues/24190)
    -   有効な 10 進数の長さを制限して、精度関連の問題を修正する[#3091](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式[#26977](https://github.com/pingcap/tidb/issues/26977)のオーバーフローのチェック方法が間違っている問題を修正
    -   `new collation`データ[#27024](https://github.com/pingcap/tidb/issues/27024)のテーブルから統計をダンプするときに`data too long`エラーが発生する問題を修正
    -   リトライしたトランザクションの明細が`TIDB_TRX` [#28670](https://github.com/pingcap/tidb/pull/28670)に含まれない問題を修正
    -   `plugin_dir`構成[#28084](https://github.com/pingcap/tidb/issues/28084)の間違ったデフォルト値を修正
    -   名前付きタイムゾーンと UTC オフセット[#8311](https://github.com/pingcap/tidb/issues/8311)を指定すると、 `CONVERT_TZ`関数が`NULL`返す問題を修正します。
    -   ステートメント[#27214](https://github.com/pingcap/tidb/issues/27214)の一部として何も指定されていない場合、 `CREATE SCHEMA` `character_set_server`および`collation_server`で指定された文字セットを新しいスキーマに使用しないという問題を修正します。

-   TiKV

    -   リージョンの移行時にRaftstore のデッドロックが原因で TiKV が使用できない問題を修正します。回避策は、スケジューリングを無効にして、利用できない TiKV [#10909](https://github.com/tikv/tikv/issues/10909)を再起動することです。
    -   Congest エラー[#11082](https://github.com/tikv/tikv/issues/11082)により、CDC が頻繁にスキャンの再試行を追加する問題を修正します。
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正します[#11047](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアント実装[#9714](https://github.com/tikv/tikv/issues/9714)でバッチ メッセージが大きすぎる問題を修正
    -   `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   応答のサイズが 4 GiB を超えるとコプロセッサーに発生するpanicの問題を修正します[#9012](https://github.com/tikv/tikv/issues/9012)
    -   スナップショット ファイルをガベージ コレクションできない場合に、スナップショット ガベージ コレクション (GC) で GC スナップショット ファイルが失われる問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサー要求を処理する際のタイムアウトによって引き起こされるpanicの問題を修正します[#10852](https://github.com/tikv/tikv/issues/10852)
    -   統計スレッド[#11195](https://github.com/tikv/tikv/issues/11195)のデータを監視することによって引き起こされるメモリリークを修正します。
    -   一部のプラットフォームから cgroup 情報を取得することによって引き起こされるpanicの問題を修正します[#10980](https://github.com/tikv/tikv/pull/10980)
    -   MVCC 削除バージョンが圧縮フィルター GC [#11248](https://github.com/tikv/tikv/pull/11248)によってドロップされないため、スキャン パフォーマンスが低下する問題を修正します。

-   PD

    -   ピアの数が構成済みのピアの数を超えているため、PD がデータを含むピアと保留中の状態のピアを誤って削除する問題を修正します[#4045](https://github.com/tikv/pd/issues/4045)
    -   PD が時間内にダウンしたピアを修正しない問題を修正します[#4077](https://github.com/tikv/pd/issues/4077)
    -   分散範囲スケジューラーが空のリージョン[#4118](https://github.com/tikv/pd/pull/4118)をスケジュールできないという問題を修正します
    -   キー マネージャーが CPU [#4071](https://github.com/tikv/pd/issues/4071)のコストが高すぎる問題を修正します。
    -   ホットリージョンスケジューラ[#4159](https://github.com/tikv/pd/issues/4159)の構成を設定するときに発生する可能性があるデータ競合の問題を修正します。
    -   リージョン syncer [#3936](https://github.com/tikv/pd/issues/3936)のスタックによるリーダー選出の遅さを修正

-   TiFlash

    -   不正確なTiFlash Store Size 統計の問題を修正
    -   ライブラリ`nsl`が存在しないため、一部のプラットフォームでTiFlash が起動しない問題を修正
    -   書き込み負荷が高い場合は、 `wait index`の無限TiFlashをブロックします (5 分のデフォルト タイムアウトが追加されます)。
    -   ログ ボリュームが大きい場合にログ検索が遅くなり、結果が得られない問題を修正します。
    -   古い履歴ログを検索すると、最新のログしか検索できない問題を修正
    -   新しい照合順序が有効になっているときに発生する可能性のある誤った結果を修正します
    -   SQL ステートメントに非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正します。
    -   Exchangeオペレーターの可能性のある`Block schema mismatch`エラーを修正します
    -   Decimal 型を比較するときに発生する可能性のある`Can't compare`エラーを修正します。
    -   `left/substring`機能の`3rd arguments of function substringUTF8 must be constants`エラーを修正

-   ツール

    -   TiCDC

        -   アップストリームの TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正します。
        -   ダウンストリームの TiDB/MySQL の可用性を検証する際の不要な CPU 消費を修正します[#3073](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDC によって生成される Kafka メッセージの量が`max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)によって制限されないという問題を修正します
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性があるという問題を修正します[#2834](https://github.com/pingcap/tiflow/issues/2834)
        -   株式データのスキャンに時間がかかりすぎると、TiKV が GC を実行するために株式データのスキャンが失敗する可能性がある問題を修正します[#2470](https://github.com/pingcap/tiflow/issues/2470)
        -   一部のタイプの列を Open Protocol フォーマット[#2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードする際に発生する可能性があったpanicの問題を修正
        -   一部のタイプの列を Avro フォーマット[#2648](https://github.com/pingcap/tiflow/issues/2648)にエンコードする際に発生する可能性があったpanicの問題を修正

    -   TiDBBinlog

        -   ほとんどのテーブルが除外されている場合、特定の負荷がかかるとチェックポイントを更新できないという問題を修正します[#1075](https://github.com/pingcap/tidb-binlog/pull/1075)
