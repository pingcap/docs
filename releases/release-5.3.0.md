---
title: TiDB 5.3 Release Notes
---

# TiDB 5.3 リリースノート {#tidb-5-3-release-notes}

発売日：2021年11月30日

TiDB バージョン: 5.3.0

v5.3 の主な新機能または改善点は次のとおりです。

-   一時テーブルを導入してアプリケーション ロジックを簡素化し、パフォーマンスを向上させます。
-   テーブルとパーティションの属性設定のサポート
-   システムのセキュリティを強化するために、TiDB ダッシュボードで最小限の権限を持つユーザーの作成をサポートします。
-   TiDB のタイムスタンプ処理フローを最適化し、全体的なパフォーマンスを向上させます。
-   TiDB データ移行 (DM) のパフォーマンスを強化し、より低いレイテンシーでデータを MySQL から TiDB に移行できるようにします。
-   複数のTiDB Lightningインスタンスを使用した並行インポートをサポートし、完全なデータ移行の効率を向上させます。
-   単一の SQL ステートメントによるクラスターのオンサイト情報の保存と復元をサポートします。これにより、実行計画に関連する問題のトラブルシューティングの効率が向上します。
-   データベースパフォーマンスの可観測性を向上させるための継続的プロファイリング実験的機能をサポートします。
-   storageとコンピューティング エンジンの最適化を継続して、システムのパフォーマンスと安定性を向上させます。
-   I/O 操作をRaftstoreスレッド プールから分離することで、TiKV の書き込みレイテンシーを短縮します (デフォルトでは無効)

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v5.3.0 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、対応するバージョンの[<a href="/releases/release-notes.md">リリースノート</a>](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                                    | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [<a href="/system-variables.md#tidb_enable_noop_functions-new-in-v40">`tidb_enable_noop_functions`</a>](/system-variables.md#tidb_enable_noop_functions-new-in-v40)                                    | 修正済み     | 一時テーブルが TiDB でサポートされるようになったので、 `CREATE TEMPORARY TABLE`と`DROP TEMPORARY TABLE` `tidb_enable_noop_functions`を有効にする必要がなくなりました。                                                                                                                                                                                                                      |
| [<a href="/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530">`tidb_enable_pseudo_for_outdated_stats`</a>](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) | 新しく追加された | テーブルの統計の有効期限が切れたときのオプティマイザの動作を制御します。デフォルト値は`ON`です。テーブル内の変更された行の数が合計行の 80% を超える場合 (この比率は構成[<a href="/tidb-configuration-file.md#pseudo-estimate-ratio">`pseudo-estimate-ratio`</a>](/tidb-configuration-file.md#pseudo-estimate-ratio)で調整できます)、オプティマイザは行の合計数以外の統計は信頼できなくなったとみなし、疑似統計を使用します。代わりに統計。値を`OFF`に設定すると、統計の有効期限が切れても、オプティマイザは統計を引き続き使用します。 |
| [<a href="/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530">`tidb_enable_tso_follower_proxy`</a>](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)                      | 新しく追加された | TSOFollowerプロキシ機能を有効にするか無効にするかを決定します。デフォルト値は`OFF`で、TSO Follower Proxy 機能が無効であることを意味します。現時点では、TiDB は PD リーダーからのみ TSO を取得します。この機能が有効になっている場合、TiDB は TSO を取得するときにすべての PD ノードにリクエストを均等に送信します。次に、PD フォロワーは TSO 要求を転送して、PD リーダーの CPU 負荷を軽減します。                                                                                                          |
| [<a href="/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530">`tidb_tso_client_batch_max_wait_time`</a>](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)       | 新しく追加された | TiDB が PD から TSO を要求するときのバッチ保存操作の最大待ち時間を設定します。デフォルト値は`0`で、追加の待機がないことを意味します。                                                                                                                                                                                                                                                                       |
| [<a href="/system-variables.md#tidb_tmp_table_max_size-new-in-v530">`tidb_tmp_table_max_size`</a>](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)                                           | 新しく追加された | 単一の[<a href="/temporary-tables.md">一時テーブル</a>](/temporary-tables.md)の最大サイズを制限します。一時テーブルがこのサイズを超えるとエラーが発生します。                                                                                                                                                                                                                                      |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                                                                                                   | 種類の変更    | 説明                                                                                                                                                                                                                                                                                           |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [<a href="/tidb-configuration-file.md#capacity">`prepared-plan-cache.capacity`</a>](/tidb-configuration-file.md#capacity)                                                      | 修正済み     | キャッシュされたステートメントの数を制御します。デフォルト値が`100`から`1000`に変更されました。                                                                                                                                                                                                                                        |
| TiKV           | [<a href="/tikv-configuration-file.md#reserve-space">`storage.reserve-space`</a>](/tikv-configuration-file.md#reserve-space)                                                   | 修正済み     | TiKV の起動時にディスク保護のために予約されるスペースを制御します。 v5.3.0 以降、予約領域の 80% は、ディスク領域が不足した場合の運用および保守に必要な追加ディスク領域として使用され、残りの 20% は一時ファイルの保存に使用されます。                                                                                                                                                               |
| TiKV           | `memory-usage-limit`                                                                                                                                                           | 修正済み     | この構成項目は TiDB v5.3.0 の新機能であり、その値はstorage.block-cache.capacity に基づいて計算されます。                                                                                                                                                                                                                    |
| TiKV           | [<a href="/tikv-configuration-file.md#store-io-pool-size-new-in-v530">`raftstore.store-io-pool-size`</a>](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)          | 新しく追加された | Raft I/O タスクを処理するスレッドの許容数。これは StoreWriter スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [<a href="/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools">TiKV スレッド プールのパフォーマンス チューニング</a>](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。 |
| TiKV           | [<a href="/tikv-configuration-file.md#raft-write-size-limit-new-in-v530">`raftstore.raft-write-size-limit`</a>](/tikv-configuration-file.md#raft-write-size-limit-new-in-v530) | 新しく追加された | Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの設定項目の値より大きい場合、データはディスクに書き込まれます。 `raftstore.store-io-pool-size`の値が`0`の場合、この構成項目は有効になりません。                                                                                                                                                              |
| TiKV           | `raftstore.raft-msg-flush-interval`                                                                                                                                            | 新しく追加された | Raftメッセージがバッチで送信される間隔を決定します。バッチ内のRaftメッセージは、この設定項目で指定された間隔ごとに送信されます。 `raftstore.store-io-pool-size`の値が`0`の場合、この構成項目は有効になりません。                                                                                                                                                                |
| TiKV           | `raftstore.raft-reject-transfer-leader-duration`                                                                                                                               | 削除されました  | Leaderが新しく追加されたノードに転送される最小時間を決定します。                                                                                                                                                                                                                                                          |
| PD             | [<a href="/pd-configuration-file.md#max-days">`log.file.max-days`</a>](/pd-configuration-file.md#max-days)                                                                     | 修正済み     | ログが保持される最大日数を制御します。デフォルト値が`1`から`0`に変更されました。                                                                                                                                                                                                                                                  |
| PD             | [<a href="/pd-configuration-file.md#max-backups">`log.file.max-backups`</a>](/pd-configuration-file.md#max-backups)                                                            | 修正済み     | 保持されるログの最大数を制御します。デフォルト値が`7`から`0`に変更されました。                                                                                                                                                                                                                                                   |
| PD             | [<a href="/pd-configuration-file.md#patrol-region-interval">`patrol-region-interval`</a>](/pd-configuration-file.md#patrol-region-interval)                                    | 修正済み     | レプリカチェッカーがリージョンの正常性状態をチェックする実行頻度を制御します。この値が小さいほど、replicaChecker の実行が速くなります。通常、このパラメータを調整する必要はありません。デフォルト値が`100ms`から`10ms`に変更されました。                                                                                                                                                           |
| PD             | [<a href="/pd-configuration-file.md#max-snapshot-count">`max-snapshot-count`</a>](/pd-configuration-file.md#max-snapshot-count)                                                | 修正済み     | 単一ストアが同時に受信または送信するスナップショットの最大数を制御します。 PD スケジューラは、この設定に依存して、通常のトラフィックに使用されるリソースがプリエンプトされるのを防ぎます。デフォルト値が`3`から`64`に変更されました。                                                                                                                                                                     |
| PD             | [<a href="/pd-configuration-file.md#max-pending-peer-count">`max-pending-peer-count`</a>](/pd-configuration-file.md#max-pending-peer-count)                                    | 修正済み     | 単一ストア内の保留中のピアの最大数を制御します。 PD スケジューラーはこの構成に依存して、一部のノードで古いログを持つリージョンが多数生成されるのを防ぎます。デフォルト値が`16`から`64`に変更されました。                                                                                                                                                                                   |
| TiD ライトニング     | `meta-schema-name`                                                                                                                                                             | 新しく追加された | 各TiDB Lightningインスタンスのメタ情報がターゲット クラスターに保存されているスキーマ名。デフォルト値は「lightning_metadata」です。                                                                                                                                                                                                           |

### その他 {#others}

-   一時テーブル:

    -   v5.3.0 より前の TiDB クラスターでローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスターが v5.3.0 以降のバージョンにアップグレードされた後は通常のテーブルとして処理されます。 v5.3.0 以降のバージョンの TiDB クラスターでグローバル一時テーブルを作成した場合、クラスターを v5.3.0 より前のバージョンにダウングレードすると、これらのテーブルは通常のテーブルとして処理され、データ エラーが発生します。
    -   v5.3.0 以降、TiCDC およびBR は[<a href="/temporary-tables.md#global-temporary-tables">グローバル一時テーブル</a>](/temporary-tables.md#global-temporary-tables)をサポートします。 v5.3.0 より前のバージョンの TiCDC およびBR を使用してグローバル一時テーブルをダウンストリームにレプリケートすると、テーブル定義エラーが発生します。
    -   次のクラスターは v5.3.0 以降であることが予想されます。そうしないと、グローバル一時テーブルを作成するときにデータ エラーが報告されます。

        -   TiDB 移行ツールを使用してインポートされるクラスター
        -   TiDB 移行ツールを使用して復元されたクラスター
        -   TiDB 移行ツールを使用したレプリケーション タスクのダウンストリーム クラスター
    -   一時テーブルの互換性情報については、 [<a href="/temporary-tables.md#compatibility-with-mysql-temporary-tables">MySQL 一時テーブルとの互換性</a>](/temporary-tables.md#compatibility-with-mysql-temporary-tables)および[<a href="/temporary-tables.md#compatibility-restrictions-with-other-tidb-features">他の TiDB 機能との互換性制限</a>](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)を参照してください。

-   v5.3.0 より前のリリースでは、システム変数が不正な値に設定されている場合、TiDB はエラーを報告します。 v5.3.0 以降のリリースでは、システム変数が不正な値に設定されている場合、TiDB は「|警告 | 1292 | 切り捨てられた不正な xxx: &#39;xx&#39;」などの警告とともに成功を返します。

-   `SHOW CREATE VIEW`の実行に`SHOW VIEW`権限が必要ない問題を修正します。ここで、 `SHOW CREATE VIEW`ステートメントを実行するための`SHOW VIEW`権限が必要になります。

-   システム変数`sql_auto_is_null`が noop関数に追加されます。 `tidb_enable_noop_functions = 0/OFF`の場合、この変数値を変更するとエラーが発生します。

-   `GRANT ALL ON performance_schema.*`構文は許可されなくなりました。 TiDB でこのステートメントを実行すると、エラーが発生します。

-   v5.3.0 より前に新しいインデックスが追加された場合、指定された期間外に自動分析が予期せずトリガーされる問題を修正しました。 v5.3.0 では、 `tidb_auto_analyze_start_time`変数と`tidb_auto_analyze_end_time`変数で期間を設定すると、この期間中にのみ自動分析がトリガーされます。

-   プラグインのデフォルトのstorageディレクトリが`""`から`/data/deploy/plugin`に変更されました。

-   DM コードは[<a href="https://github.com/pingcap/tiflow/tree/master/dm">TiCDC コード リポジトリ内のフォルダー「dm」</a>](https://github.com/pingcap/tiflow/tree/master/dm)に移行されます。現在、DM は TiDB のバージョン番号に従うようになりました。 v2.0.x の次の新しい DM バージョンは v5.3.0 で、リスクなしで v2.0.x から v5.3.0 にアップグレードできます。

-   Prometheus のデフォルトのデプロイ バージョンは v2.8.1 から[<a href="https://github.com/prometheus/prometheus/releases/tag/v2.27.1">v2.27.1</a>](https://github.com/prometheus/prometheus/releases/tag/v2.27.1)にアップグレードされ、2021 年 5 月にリリースされます。このバージョンでは、より多くの機能が提供され、セキュリティ問題が修正されています。 Prometheus v2.8.1 と比較すると、v2.27.1 のアラート時刻表現は Unix タイムスタンプから UTC に変更されています。詳細は[<a href="https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06">プロメテウスのコミット</a>](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)を参照してください。

## 新機能 {#new-features}

### SQL {#sql}

-   **SQL インターフェースを使用してデータの配置ルールを設定する (実験的機能)**

    データの配置ルールを設定するための SQL インターフェイスを提供する`[CREATE | ALTER] PLACEMENT POLICY`構文をサポートします。この機能を使用すると、特定の領域、データセンター、ラック、ホスト、またはレプリカ数ルールにスケジュールされるテーブルとパーティションを指定できます。これにより、低コストと高い柔軟性を求めるアプリケーションの要求が満たされます。典型的なユーザー シナリオは次のとおりです。

    -   異なるアプリケーションの複数のデータベースを結合してデータベースの保守コストを削減し、ルール構成を通じてアプリケーション リソースの分離を実現します。
    -   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます。
    -   新しいデータを SSD に保存し、古いデータを HHD に保存して、データのアーカイブとstorageのコストを削減します。
    -   ホットスポット データのリーダーを高性能 TiKV インスタンスにスケジュールする
    -   コールド データを低コストのstorageメディアに分離して、コスト効率を向上させます。

    [<a href="/placement-rules-in-sql.md">ユーザードキュメント</a>](/placement-rules-in-sql.md) [<a href="https://github.com/pingcap/tidb/issues/18030">#18030</a>](https://github.com/pingcap/tidb/issues/18030)

-   **一時テーブル**

    一時テーブルを作成する`CREATE [GLOBAL] TEMPORARY TABLE`ステートメントをサポートします。この機能を使用すると、アプリケーションの計算過程で生成される一時データを簡単に管理できます。一時データはメモリに保存され、 `tidb_tmp_table_max_size`変数を使用して一時テーブルのサイズを制限できます。 TiDB は、次のタイプの一時テーブルをサポートします。

    -   グローバル一時テーブル
        -   クラスター内のすべてのセッションに表示され、テーブル スキーマは永続的です。
        -   トランザクションレベルのデータ分離を提供します。一時データはトランザクション内でのみ有効です。トランザクションが完了すると、データは自動的に削除されます。
    -   ローカル一時テーブル

        -   現在のセッションに対してのみ表示され、テーブル スキーマは永続的ではありません。
        -   重複したテーブル名をサポートします。アプリケーション用に複雑な命名規則を設計する必要はありません。
        -   セッション レベルのデータ分離を提供し、よりシンプルなアプリケーション ロジックを設計できるようにします。トランザクションが完了すると、一時テーブルは削除されます。

        [<a href="/temporary-tables.md">ユーザードキュメント</a>](/temporary-tables.md) [<a href="https://github.com/pingcap/tidb/issues/24169">#24169</a>](https://github.com/pingcap/tidb/issues/24169)

-   **`FOR UPDATE OF TABLES`構文のサポート**

    複数のテーブルを結合する SQL ステートメントの場合、TiDB は、 `OF TABLES`に含まれるテーブルに関連付けられた行に対する悲観的ロックの取得をサポートします。

    [<a href="/sql-statements/sql-statement-select.md">ユーザードキュメント</a>](/sql-statements/sql-statement-select.md) [<a href="https://github.com/pingcap/tidb/issues/28689">#28689</a>](https://github.com/pingcap/tidb/issues/28689)

-   **テーブルの属性**

    テーブルまたはパーティションの属性を設定できる`ALTER TABLE [PARTITION] ATTRIBUTES`ステートメントをサポートします。現在、TiDB は`merge_option`属性の設定のみをサポートしています。この属性を追加すると、リージョンのマージ動作を明示的に制御できます。

    ユーザー シナリオ: `SPLIT TABLE`操作を実行するときに、一定期間 (PD パラメーター[<a href="/pd-configuration-file.md#split-merge-interval">`split-merge-interval`</a>](/pd-configuration-file.md#split-merge-interval)で制御) が経過してもデータが挿入されない場合、空のリージョンはデフォルトで自動的にマージされます。この場合、テーブル属性を`merge_option=deny`に設定して、リージョンの自動マージを回避できます。

    [<a href="/table-attributes.md">ユーザードキュメント</a>](/table-attributes.md) [<a href="https://github.com/tikv/pd/issues/3839">#3839</a>](https://github.com/tikv/pd/issues/3839)

### Security {#security}

-   **TiDB ダッシュボードで最小限の権限を持つユーザーの作成をサポート**

    TiDB Dashboard のアカウント システムは、 TiDB SQLのアカウント システムと一致しています。 TiDB ダッシュボードにアクセスするユーザーは、 TiDB SQLユーザーの権限に基づいて認証および許可されます。したがって、TiDB ダッシュボードには制限された権限、または読み取り専用権限が必要です。最小特権の原則に基づいて TiDB ダッシュボードにアクセスするようにユーザーを構成できるため、高い特権を持つユーザーのアクセスを回避できます。

    TiDB ダッシュボードにアクセスしてサインインするには、最小権限の SQL ユーザーを作成することをお勧めします。これにより、高い権限を持つユーザーのアクセスが回避され、セキュリティが向上します。

    [<a href="/dashboard/dashboard-user.md">ユーザードキュメント</a>](/dashboard/dashboard-user.md)

### パフォーマンス {#performance}

-   **PDのタイムスタンプ処理フローを最適化する**

    TiDB は、PDFollowerプロキシを有効にし、PD クライアントがバッチで TSO を要求するときに必要なバッチ待機時間を変更することにより、タイムスタンプ処理フローを最適化し、PD のタイムスタンプ処理負荷を軽減します。これは、システム全体のスケーラビリティの向上に役立ちます。

    -   システム変数[<a href="/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530">`tidb_enable_tso_follower_proxy`</a>](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)による PD Follower Proxy の有効化または無効化をサポートします。 TSO 要求の PD の負荷が高すぎるとします。この場合、PD フォロワー プロキシを有効にすると、フォロワー上の要求サイクル中に収集された TSO 要求をリーダー ノードにバッチ転送できます。このソリューションは、クライアントとリーダー間の直接対話の数を効果的に減らし、リーダーへの負荷のプレッシャーを軽減し、TiDB の全体的なパフォーマンスを向上させることができます。

    > **ノート：**
    >
    > クライアントの数が少なく、PD リーダーの CPU 負荷がフルではない場合、PDFollowerプロキシを有効にすることはお勧めできません。

    -   システム変数[<a href="/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530">`tidb_tso_client_batch_max_wait_time`</a>](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)を使用して、PD クライアントが TSO をバッチ要求するために必要な最大待機時間を設定することをサポートします。この時間の単位はミリ秒です。 PD の TSO リクエストの負荷が高い場合は、待機時間を増やしてバッチ サイズを大きくすることで負荷を軽減し、スループットを向上させることができます。

    > **ノート：**
    >
    > TSO 要求の負荷が高くない場合、この変数値を変更することはお勧めできません。

    [<a href="/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530">ユーザードキュメント</a>](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530) [<a href="https://github.com/tikv/pd/issues/3149">#3149</a>](https://github.com/tikv/pd/issues/3149)

### 安定性 {#stability}

-   **一部のストアが永久に損傷した後のオンラインの安全でないリカバリのサポート (実験的機能)**

    オンラインデータの安全でないリカバリを実行する`pd-ctl unsafe remove-failed-stores`コマンドをサポートします。大部分のデータ レプリカで永久的な損傷 (ディスク損傷など) のような問題が発生し、これらの問題によりアプリケーション内のデータ範囲が読み取り不能または書き込み不能になったとします。この場合、PD に実装されているオンライン安全でない回復機能を使用してデータを回復し、データを再び読み取りまたは書き込みできるようにすることができます。

    TiDB チームのサポートを受けて機能関連の操作を実行することをお勧めします。

    [<a href="/online-unsafe-recovery.md">ユーザードキュメント</a>](/online-unsafe-recovery.md) [<a href="https://github.com/tikv/tikv/issues/10483">#10483</a>](https://github.com/tikv/tikv/issues/10483)

### データ移行 {#data-migration}

-   **DM レプリケーションのパフォーマンスが強化されました**

    MySQL から TiDB へのデータ レプリケーションを低レイテンシーで確実に行うために、次の機能をサポートします。

    -   単一行の複数の更新を 1 つのステートメントに圧縮します。
    -   複数行のバッチ更新を 1 つのステートメントにマージする

-   **DM OpenAPI を追加して DM クラスターをより適切に維持します (実験的機能)**

    DM は、DM クラスターのクエリと操作のための OpenAPI 機能を提供します。 [<a href="/dm/dmctl-introduction.md">dmctl ツール</a>](/dm/dmctl-introduction.md)の特徴と似ています。

    現在、DM OpenAPI は実験的機能であり、デフォルトでは無効になっています。本番環境での使用はお勧めできません。

    [<a href="/dm/dm-open-api.md">ユーザードキュメント</a>](/dm/dm-open-api.md)

-   **TiDB Lightning並行輸入品**

    TiDB Lightning は、元の機能を拡張するための並行インポート機能を提供します。これにより、複数の Lightning インスタンスを同時にデプロイして、単一のテーブルまたは複数のテーブルをダウンストリーム TiDB に並行してインポートできます。顧客の使用方法を変えることなく、データ移行機能が大幅に向上し、よりリアルタイムの方法でデータを移行して、データをさらに処理、統合、分析できるようになります。企業のデータ管理の効率が向上します。

    私たちのテストでは、10 個のTiDB Lightningインスタンスを使用して、合計 20 TiB MySQL データを 8 時間以内に TiDB にインポートできます。複数テーブルのインポートのパフォーマンスも向上しました。単一のTiDB Lightningインスタンスは 250 GiB/h でのインポートをサポートでき、全体的な移行は元のパフォーマンスの 8 倍高速になります。

    [<a href="/tidb-lightning/tidb-lightning-distributed-import.md">ユーザードキュメント</a>](/tidb-lightning/tidb-lightning-distributed-import.md)

-   **TiDB Lightning事前チェック**

    TiDB Lightning は、移行タスクを実行する前に構成をチェックする機能を提供します。デフォルトでは有効になっています。この機能は、ディスク容量と実行構成に関するいくつかの日常的なチェックを自動的に実行します。主な目的は、その後のインポート プロセス全体がスムーズに進むようにすることです。

    [<a href="/tidb-lightning/tidb-lightning-prechecks.md">ユーザードキュメント</a>](/tidb-lightning/tidb-lightning-prechecks.md)

-   **TiDB Lightning はGBK 文字セットのファイルのインポートをサポートします**

    ソースデータファイルの文字セットを指定できます。 TiDB Lightning は、インポート プロセス中にソース ファイルを指定された文字セットから UTF-8 エンコーディングに変換します。

    [<a href="/tidb-lightning/tidb-lightning-configuration.md">ユーザードキュメント</a>](/tidb-lightning/tidb-lightning-configuration.md)

-   **同期差分インスペクターの改善**

    -   比較速度が 375 MB/s から 700 MB/s に向上しました。
    -   比較中に TiDB ノードのメモリ消費量をほぼ半分に削減
    -   ユーザーインターフェイスを最適化し、比較中にプログレスバーを表示します。

    [<a href="/sync-diff-inspector/sync-diff-inspector-overview.md">ユーザードキュメント</a>](/sync-diff-inspector/sync-diff-inspector-overview.md)

### 診断効率 {#diagnostic-efficiency}

-   **クラスターのオンサイト情報の保存と復元**

    TiDB クラスターの問題を特定してトラブルシューティングする場合、多くの場合、システムとクエリ プランに関する情報を提供する必要があります。より便利かつ効率的な方法で情報を取得し、クラスターの問題をトラブルシューティングできるように、TiDB v5.3.0 では`PLAN REPLAYER`コマンドが導入されました。このコマンドを使用すると、クラスターのオンサイト情報を簡単に保存および復元できるようになり、トラブルシューティングの効率が向上し、管理のために問題をより簡単にアーカイブできるようになります。

    `PLAN REPLAYER`の特徴は以下の通りです。

    -   オンサイトのトラブルシューティングで TiDB クラスターの情報を ZIP 形式のファイルにエクスポートしてstorage。
    -   別の TiDB クラスターからエクスポートされた ZIP 形式のファイルをクラスターにインポートします。このファイルには、オンサイトのトラブルシューティングにおける後者の TiDB クラスターの情報が含まれています。

    [<a href="/sql-plan-replayer.md">ユーザードキュメント</a>](/sql-plan-replayer.md) [<a href="https://github.com/pingcap/tidb/issues/26325">#26325</a>](https://github.com/pingcap/tidb/issues/26325)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   **TiCDC 結果的に整合性のあるレプリケーション**

    TiCDC は、災害シナリオにおいて結果的に整合性のあるレプリケーション機能を提供します。プライマリ TiDB クラスターで災害が発生し、サービスを短時間で再開できない場合、TiCDC はセカンダリ クラスター内のデータの一貫性を確保する機能を提供する必要があります。一方、TiCDC では、データベースが長期間利用できなくなりビジネスに影響が出るのを避けるために、ビジネスがトラフィックをセカンダリ クラスターに迅速に切り替えることができるようにする必要があります。

    この機能は、TiCDC をサポートし、TiDB クラスターからセカンダリ リレーショナル データベース TiDB/ Aurora/MySQL/MariaDB に増分データをレプリケートします。プライマリ クラスターがクラッシュした場合、障害発生前に TiCDC のレプリケーション ステータスが正常でレプリケーション ラグが小さいという条件であれば、TiCDC は 5 分以内にセカンダリ クラスターをプライマリ クラスター内の特定のスナップショットにリカバリできます。データ損失は 30 分未満、つまり RTO &lt;= 5 分、RPO &lt;= 30 分が許容されます。

    [<a href="/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios">ユーザードキュメント</a>](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)

-   **TiCDC は、TiCDC タスクを管理するための HTTP プロトコル OpenAPI をサポートしています**

    TiDB v5.3.0 以降、TiCDC OpenAPI は一般提供 (GA) 機能になりました。本番環境では、OpenAPI を使用して TiCDC クラスターのクエリと操作を行うことができます。

### 導入とメンテナンス {#deployment-and-maintenance}

-   **継続的プロファイリング (実験的機能)**

    TiDB ダッシュボードは、TiDB クラスターの実行中にインスタンスのパフォーマンス分析結果をリアルタイムで自動的に保存する継続的プロファイリング機能をサポートしています。性能解析結果をフレームグラフで確認できるため、視認性が高くトラブルシューティングの時間を短縮できます。

    この機能はデフォルトでは無効になっており、TiDB ダッシュボードの**継続プロファイル**ページで有効にする必要があります。

    この機能は、 TiUP v1.7.0 以降を使用してアップグレードまたはインストールされたクラスターでのみ使用できます。

    [<a href="/dashboard/continuous-profiling.md">ユーザードキュメント</a>](/dashboard/continuous-profiling.md)

## テレメトリー {#telemetry}

TiDB は、TEMPORARY TABLE 機能が使用されているかどうかに関する情報をテレメトリ レポートに追加します。これには、テーブル名やテーブル データは含まれません。

テレメトリとこの動作を無効にする方法の詳細については、 [<a href="/telemetry.md">テレメトリー</a>](/telemetry.md)を参照してください。

## 削除された機能 {#removed-feature}

TiCDC v5.3.0 以降、TiDB クラスター間の循環レプリケーション機能 (v5.0.0 の実験的機能) は削除されました。 TiCDC をアップグレードする前にこの機能を使用してデータを複製していた場合、関連データはアップグレード後に影響を受けません。

## 改善点 {#improvements}

-   TiDB

    -   コプロセッサーがロックを検出したときに、影響を受ける SQL ステートメントをデバッグ ログに表示します。これは、問題の診断に役立ちます[<a href="https://github.com/pingcap/tidb/issues/27718">#27718</a>](https://github.com/pingcap/tidb/issues/27718)
    -   SQL 論理レイヤー[<a href="https://github.com/pingcap/tidb/issues/27247">#27247</a>](https://github.com/pingcap/tidb/issues/27247)でデータをバックアップおよび復元する際のバックアップおよび復元データのサイズの表示のサポート
    -   `tidb_analyze_version`が`2`の場合の ANALYZE のデフォルトの収集ロジックを改善します。これにより、収集が高速化され、リソースのオーバーヘッドが削減されます。
    -   `ANALYZE TABLE table_name COLUMNS col_1, col_2, ... , col_n`構文を紹介します。この構文では、幅の広いテーブルの一部の列についてのみ統計を収集できるため、統計収集の速度が向上します。

-   TiKV

    -   ディスク領域の保護を強化してstorageの安定性を向上

        ディスクの完全書き込みエラーが発生した場合に TiKV がパニックにpanic可能性がある問題を解決するために、TiKV は 2 レベルのしきい値防御メカニズムを導入し、ディスクの残りのスペースが過剰なトラフィックによって枯渇するのを防ぎます。さらに、このメカニズムは、しきい値がトリガーされたときにスペースを再利用する機能を提供します。残りのスペースのしきい値がトリガーされると、一部の書き込み操作が失敗し、TiKV はディスク フル エラーとディスク フル ノードのリストを返します。この場合、スペースを回復してサービスを復元するには、 `Drop/Truncate Table`実行するか、ノードをスケールアウトします。

    -   L0フロー制御のアルゴリズムを簡略化[<a href="https://github.com/tikv/tikv/issues/10879">#10879</a>](https://github.com/tikv/tikv/issues/10879)

    -   raft クライアント モジュール[<a href="https://github.com/tikv/tikv/pull/10944">#10944</a>](https://github.com/tikv/tikv/pull/10944)のエラー ログ レポートを改善しました。

    -   ロギング スレッドがパフォーマンスのボトルネックになるのを回避するために、スレッドを改善します[<a href="https://github.com/tikv/tikv/issues/10841">#10841</a>](https://github.com/tikv/tikv/issues/10841)

    -   書き込みクエリの統計タイプをさらに追加[<a href="https://github.com/tikv/tikv/issues/10507">#10507</a>](https://github.com/tikv/tikv/issues/10507)

    -   I/O 操作をRaftstoreスレッド プールから分離することで書き込みレイテンシーを短縮します (デフォルトでは無効)。チューニングの詳細については、 [<a href="/tune-tikv-thread-performance.md">TiKV スレッド プールのパフォーマンスを調整する</a>](/tune-tikv-thread-performance.md) [<a href="https://github.com/tikv/tikv/issues/10540">#10540</a>](https://github.com/tikv/tikv/issues/10540)を参照してください。

-   PD

    -   ホットスポット スケジューラ[<a href="https://github.com/tikv/pd/issues/3869">#3869</a>](https://github.com/tikv/pd/issues/3869)の QPS ディメンションにさらに多くの種類の書き込みクエリを追加します。
    -   スケジューラのパフォーマンスを向上させるために、バランスリージョンスケジューラの再試行制限を動的に調整するサポート[<a href="https://github.com/tikv/pd/issues/3744">#3744</a>](https://github.com/tikv/pd/issues/3744)
    -   TiDB ダッシュボードを v2021.10.08.1 に更新します[<a href="https://github.com/tikv/pd/pull/4070">#4070</a>](https://github.com/tikv/pd/pull/4070)
    -   エビクト リーダー スケジューラが異常なピアのあるリージョンをスケジュールできることのサポート[<a href="https://github.com/tikv/pd/issues/4093">#4093</a>](https://github.com/tikv/pd/issues/4093)
    -   スケジューラの終了プロセスを高速化[<a href="https://github.com/tikv/pd/issues/4146">#4146</a>](https://github.com/tikv/pd/issues/4146)

-   TiFlash

    -   TableScan オペレーターの実行効率を大幅に向上

    -   Exchangeオペレータの実行効率を向上させる

    -   storageエンジンの GC 中の書き込み増幅とメモリ使用量を削減します (実験的機能)

    -   TiFlashの再起動時の安定性と可用性が向上し、再起動後に発生する可能性のあるクエリエラーが減少します。

    -   複数の新しい文字列関数と時刻関数を MPP エンジンにプッシュダウンするサポート

        -   文字列関数：LIKEパターン、FORMAT()、LOWER()、LTRIM()、RTRIM()、SUBSTRING_INDEX()、TRIM()、UCASE()、UPPER()
        -   数学関数: ROUND (10 進数、整数)
        -   日付と時刻の関数: HOUR()、MICROSECOND()、MINUTE()、SECOND()、SYSDATE()
        -   型変換関数：CAST(time, real)
        -   集計関数: GROUP_CONCAT()、SUM(enum)

    -   512ビットSIMDをサポート

    -   古いデータのクリーンアップ アルゴリズムを強化して、ディスク使用量を削減し、ファイルをより効率的に読み取ることができます。

    -   一部の非 Linux システムでダッシュボードにメモリまたは CPU 情報が表示されない問題を修正

    -   TiFlashログ ファイルの命名スタイルを統一し (TiKV の命名スタイルと一貫した命名スタイルを維持)、logger.count と logger.size の動的変更をサポートします。

    -   列ベースのファイルのデータ検証機能を改善します (チェックサム、実験的機能)

-   ツール

    -   TiCDC

        -   Kafka シンク構成項目`MaxMessageBytes`のデフォルト値を 64 MB から 1 MB に減らし、大きなメッセージが Kafka ブローカーによって拒否される問題を修正します[<a href="https://github.com/pingcap/tiflow/pull/3104">#3104</a>](https://github.com/pingcap/tiflow/pull/3104)
        -   レプリケーション パイプラインのメモリ使用量を削減する[<a href="https://github.com/pingcap/tiflow/issues/2553">#2553</a>](https://github.com/pingcap/tiflow/issues/2553) [<a href="https://github.com/pingcap/tiflow/pull/3037">#3037</a>](https://github.com/pingcap/tiflow/pull/3037) [<a href="https://github.com/pingcap/tiflow/pull/2726">#2726</a>](https://github.com/pingcap/tiflow/pull/2726)
        -   監視項目とアラートルールを最適化し、同期リンク、メモリGC、ストックデータスキャン処理の可観測性を向上[<a href="https://github.com/pingcap/tiflow/pull/2735">#2735</a>](https://github.com/pingcap/tiflow/pull/2735) [<a href="https://github.com/pingcap/tiflow/issues/1606">#1606</a>](https://github.com/pingcap/tiflow/issues/1606) [<a href="https://github.com/pingcap/tiflow/pull/3000">#3000</a>](https://github.com/pingcap/tiflow/pull/3000) [<a href="https://github.com/pingcap/tiflow/issues/2985">#2985</a>](https://github.com/pingcap/tiflow/issues/2985) [<a href="https://github.com/pingcap/tiflow/issues/2156">#2156</a>](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが正常な場合、ユーザーの誤解を避けるために、履歴エラー メッセージは表示されません[<a href="https://github.com/pingcap/tiflow/issues/2242">#2242</a>](https://github.com/pingcap/tiflow/issues/2242)

## バグの修正 {#bug-fixes}

-   TiDB

    -   間違った実行計画が原因で実行中に発生するエラーを修正します。間違った実行プランは、パーティション化されたテーブルで集計演算子をプッシュダウンするときにスキーマ列の浅いコピーが原因で発生します[<a href="https://github.com/pingcap/tidb/issues/27797">#27797</a>](https://github.com/pingcap/tidb/issues/27797) [<a href="https://github.com/pingcap/tidb/issues/26554">#26554</a>](https://github.com/pingcap/tidb/issues/26554)
    -   `plan cache`符号なしフラグの変更を検出できない問題を修正[<a href="https://github.com/pingcap/tidb/issues/28254">#28254</a>](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲[<a href="https://github.com/pingcap/tidb/issues/28233">#28233</a>](https://github.com/pingcap/tidb/issues/28233)の外にある場合の間違ったパーティション プルーニングを修正しました。
    -   場合によってはプランナーが`join`の無効なプランをキャッシュする可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/28087">#28087</a>](https://github.com/pingcap/tidb/issues/28087)
    -   ハッシュカラムタイプが`enum` [<a href="https://github.com/pingcap/tidb/issues/27893">#27893</a>](https://github.com/pingcap/tidb/issues/27893)の場合の間違った`IndexLookUpJoin`を修正
    -   アイドル状態の接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるというバッチ クライアントのバグを修正しました[<a href="https://github.com/pingcap/tidb/pull/27688">#27688</a>](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲット クラスターでのチェックサムの実行に失敗した場合のTiDB Lightningpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/27686">#27686</a>](https://github.com/pingcap/tidb/pull/27686)
    -   場合によっては`date_add`と`date_sub`関数の間違った結果を修正する[<a href="https://github.com/pingcap/tidb/issues/27232">#27232</a>](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式[<a href="https://github.com/pingcap/tidb/issues/28643">#28643</a>](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正しました。
    -   MySQL 5.1 または古いクライアント バージョン[<a href="https://github.com/pingcap/tidb/issues/27855">#27855</a>](https://github.com/pingcap/tidb/issues/27855)に接続するときの認証の問題を修正
    -   新しいインデックスが追加されると、auto analyzeが指定された時間外にトリガーされる場合がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/28698">#28698</a>](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると`tidb_snapshot` [<a href="https://github.com/pingcap/tidb/pull/28683">#28683</a>](https://github.com/pingcap/tidb/pull/28683)が無効になるバグを修正
    -   多くのピアが欠落しているリージョン[<a href="https://github.com/pingcap/tidb/issues/27534">#27534</a>](https://github.com/pingcap/tidb/issues/27534)を持つクラスターでBRが機能しないバグを修正
    -   サポートされていない`cast` TiFlash [<a href="https://github.com/pingcap/tidb/issues/23907">#23907</a>](https://github.com/pingcap/tidb/issues/23907)にプッシュダウンされた場合の`tidb_cast to Int32 is not supported`のような予期しないエラーを修正
    -   `%s value is out of range in '%s'`エラーメッセージ[<a href="https://github.com/pingcap/tidb/issues/27964">#27964</a>](https://github.com/pingcap/tidb/issues/27964)に`DECIMAL overflow`が欠落している問題を修正
    -   MPP ノードの可用性検出が一部の特殊なケースで機能しないバグを修正[<a href="https://github.com/pingcap/tics/issues/3118">#3118</a>](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [<a href="https://github.com/pingcap/tidb/issues/27952">#27952</a>](https://github.com/pingcap/tidb/issues/27952)を割り当てるときの`DATA RACE`問題を修正
    -   空`dual table` [<a href="https://github.com/pingcap/tidb/issues/28250">#28250</a>](https://github.com/pingcap/tidb/issues/28250)を削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正
    -   MPP クエリ[<a href="https://github.com/pingcap/tics/issues/1791">#1791</a>](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   MPP クエリ[<a href="https://github.com/pingcap/tidb/pull/28149">#28149</a>](https://github.com/pingcap/tidb/pull/28149)のエラー ログ`cannot found column in Schema column`の問題を修正
    -   TiFlashのシャットダウン時に TiDB がpanicになる問題を修正[<a href="https://github.com/pingcap/tidb/issues/28096">#28096</a>](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない 3DES (トリプル データ暗号化アルゴリズム) ベースの TLS 暗号スイートのサポートを削除します[<a href="https://github.com/pingcap/tidb/pull/27859">#27859</a>](https://github.com/pingcap/tidb/pull/27859)
    -   Lightning が事前チェック中にオフライン TiKV ノードに接続し、インポート失敗が発生する問題を修正します[<a href="https://github.com/pingcap/tidb/pull/27826">#27826</a>](https://github.com/pingcap/tidb/pull/27826)
    -   多数のファイルをテーブル[<a href="https://github.com/pingcap/tidb/issues/27605">#27605</a>](https://github.com/pingcap/tidb/issues/27605)にインポートする場合、事前チェックに時間がかかりすぎる問題を修正
    -   式を書き換えると`between`間違った照合順序が推測される[<a href="https://github.com/pingcap/tidb/issues/27146">#27146</a>](https://github.com/pingcap/tidb/issues/27146)という問題を修正します。
    -   `group_concat`関数が照合順序を考慮していない問題を修正[<a href="https://github.com/pingcap/tidb/issues/27429">#27429</a>](https://github.com/pingcap/tidb/issues/27429)
    -   `extract`関数の引数が負の持続時間の場合に発生する結果が間違っていたのを修正[<a href="https://github.com/pingcap/tidb/issues/27236">#27236</a>](https://github.com/pingcap/tidb/issues/27236)
    -   `NO_UNSIGNED_SUBTRACTION`を[<a href="https://github.com/pingcap/tidb/issues/26765">#26765</a>](https://github.com/pingcap/tidb/issues/26765)に設定するとパーティションの作成に失敗する問題を修正
    -   列のプルーニングと集計プッシュダウンで副作用のある式を回避する[<a href="https://github.com/pingcap/tidb/issues/27106">#27106</a>](https://github.com/pingcap/tidb/issues/27106)
    -   不要な gRPC ログを削除する[<a href="https://github.com/pingcap/tidb/issues/24190">#24190</a>](https://github.com/pingcap/tidb/issues/24190)
    -   有効な 10 進数の長さを制限して、精度関連の問題を修正します[<a href="https://github.com/pingcap/tics/issues/3091">#3091</a>](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式[<a href="https://github.com/pingcap/tidb/issues/26977">#26977</a>](https://github.com/pingcap/tidb/issues/26977)のオーバーフローをチェックする間違った方法の問題を修正
    -   `new collation`データ[<a href="https://github.com/pingcap/tidb/issues/27024">#27024</a>](https://github.com/pingcap/tidb/issues/27024)を持つテーブルから統計をダンプするときに`data too long`エラーが発生する問題を修正
    -   リトライしたトランザクションのステートメントが`TIDB_TRX` [<a href="https://github.com/pingcap/tidb/pull/28670">#28670</a>](https://github.com/pingcap/tidb/pull/28670)に含まれない問題を修正
    -   `plugin_dir`構成[<a href="https://github.com/pingcap/tidb/issues/28084">#28084</a>](https://github.com/pingcap/tidb/issues/28084)の間違ったデフォルト値を修正します。
    -   名前付きタイムゾーンと UTC オフセット[<a href="https://github.com/pingcap/tidb/issues/8311">#8311</a>](https://github.com/pingcap/tidb/issues/8311)が指定されている場合、 `CONVERT_TZ`関数が`NULL`返す問題を修正します。
    -   ステートメントの一部として何も指定されていない場合、 `CREATE SCHEMA`新しいスキーマに対して`character_set_server`と`collation_server`で指定された文字セットを使用しないという問題を修正します[<a href="https://github.com/pingcap/tidb/issues/27214">#27214</a>](https://github.com/pingcap/tidb/issues/27214)

-   TiKV

    -   リージョンの移行時にRaftstore のデッドロックが原因で TiKV が利用できなくなる問題を修正します。回避策は、スケジュールを無効にして、利用できない TiKV [<a href="https://github.com/tikv/tikv/issues/10909">#10909</a>](https://github.com/tikv/tikv/issues/10909)を再起動することです。
    -   輻輳エラー[<a href="https://github.com/tikv/tikv/issues/11082">#11082</a>](https://github.com/tikv/tikv/issues/11082)が原因で CDC がスキャンの再試行を頻繁に追加する問題を修正します。
    -   チャンネルがいっぱいの場合、 Raft接続が切断される問題を修正[<a href="https://github.com/tikv/tikv/issues/11047">#11047</a>](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアント実装[<a href="https://github.com/tikv/tikv/issues/9714">#9714</a>](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   `resolved_ts` [<a href="https://github.com/tikv/tikv/issues/10965">#10965</a>](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   応答のサイズが 4 GiB を超えるとコプロセッサに発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/9012">#9012</a>](https://github.com/tikv/tikv/issues/9012)
    -   スナップショット ファイルをガベージ コレクションできない場合、スナップショット ガベージ コレクション (GC) で GC スナップショット ファイルが失われる問題を修正します[<a href="https://github.com/tikv/tikv/issues/10813">#10813</a>](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサーリクエストの処理時にタイムアウトが原因で発生するpanicの問題を修正[<a href="https://github.com/tikv/tikv/issues/10852">#10852</a>](https://github.com/tikv/tikv/issues/10852)
    -   統計スレッド[<a href="https://github.com/tikv/tikv/issues/11195">#11195</a>](https://github.com/tikv/tikv/issues/11195)のデータ監視によって発生するメモリリークを修正しました。
    -   一部のプラットフォームから cgroup 情報を取得することによって引き起こされるpanicの問題を修正します[<a href="https://github.com/tikv/tikv/pull/10980">#10980</a>](https://github.com/tikv/tikv/pull/10980)
    -   MVCC 削除バージョンが圧縮フィルター GC [<a href="https://github.com/tikv/tikv/pull/11248">#11248</a>](https://github.com/tikv/tikv/pull/11248)によってドロップされないため、スキャン パフォーマンスが低下する問題を修正

-   PD

    -   ピアの数が設定されたピアの数を超えているため、PD がデータを持ち保留ステータスのピアを誤って削除する問題を修正します[<a href="https://github.com/tikv/pd/issues/4045">#4045</a>](https://github.com/tikv/pd/issues/4045)
    -   PD がダウンしたピアを時間内に修正しない問題を修正します[<a href="https://github.com/tikv/pd/issues/4077">#4077</a>](https://github.com/tikv/pd/issues/4077)
    -   スキャッター範囲スケジューラーが空のリージョン[<a href="https://github.com/tikv/pd/pull/4118">#4118</a>](https://github.com/tikv/pd/pull/4118)をスケジュールできない問題を修正します。
    -   キーマネージャーのCPU消費量が多すぎる問題を修正[<a href="https://github.com/tikv/pd/issues/4071">#4071</a>](https://github.com/tikv/pd/issues/4071)
    -   ホットリージョンスケジューラ[<a href="https://github.com/tikv/pd/issues/4159">#4159</a>](https://github.com/tikv/pd/issues/4159)の構成を設定するときに発生する可能性があるデータ競合の問題を修正します。
    -   リージョン装置[<a href="https://github.com/tikv/pd/issues/3936">#3936</a>](https://github.com/tikv/pd/issues/3936)のスタックによって引き起こされるリーダー選出の遅さを修正

-   TiFlash

    -   不正確なTiFlashストア サイズ統計の問題を修正
    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlash が起動できない問題を修正
    -   筆圧が高い場合の無限待機`wait index`ブロックします (デフォルトのタイムアウト 5 分が追加されます)。これにより、 TiFlashがサービスを提供するためにデータ レプリケーションを長時間待機することがなくなります。
    -   ログのボリュームが大きい場合にログ検索が遅くなり、結果が得られない問題を修正
    -   古い履歴ログを検索すると最新のログしか検索できない問題を修正
    -   新しい照合順序が有効になっている場合に発生する可能性のある間違った結果を修正
    -   SQL ステートメントに非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正しました。
    -   Exchange オペレーターで発生する可能性のある`Block schema mismatch`エラーを修正
    -   Decimal 型を比較するときに発生する可能性のある`Can't compare`エラーを修正
    -   `left/substring`機能の`3rd arguments of function substringUTF8 must be constants`エラーを修正

-   ツール

    -   TiCDC

        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3061">#3061</a>](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[<a href="https://github.com/pingcap/tiflow/issues/2386">#2386</a>](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正
        -   ダウンストリーム TiDB/MySQL の可用性を確認する際の不要な CPU 消費を修正[<a href="https://github.com/pingcap/tiflow/issues/3073">#3073</a>](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDC によって生成される Kafka メッセージの量が`max-message-size` [<a href="https://github.com/pingcap/tiflow/issues/2962">#2962</a>](https://github.com/pingcap/tiflow/issues/2962)の制限を受けない問題を修正
        -   Kafka メッセージの書き込み中にエラーが発生したときに TiCDC 同期タスクが一時停止することがある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2978">#2978</a>](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2834">#2834</a>](https://github.com/pingcap/tiflow/issues/2834)
        -   ストック データのスキャンに時間がかかりすぎる場合、TiKV が GC を実行するためにストック データのスキャンが失敗する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2470">#2470</a>](https://github.com/pingcap/tiflow/issues/2470)
        -   一部の種類の列をオープン プロトコル形式[<a href="https://github.com/pingcap/tiflow/issues/2758">#2758</a>](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生する可能性のpanicの問題を修正しました。
        -   一部の種類の列を Avro 形式[<a href="https://github.com/pingcap/tiflow/issues/2648">#2648</a>](https://github.com/pingcap/tiflow/issues/2648)にエンコードするときに発生する可能性のpanicの問題を修正

    -   TiDBBinlog

        -   ほとんどのテーブルがフィルターで除外されると、特別な負荷がかかるとチェックポイントを更新できない問題を修正します[<a href="https://github.com/pingcap/tidb-binlog/pull/1075">#1075</a>](https://github.com/pingcap/tidb-binlog/pull/1075)
