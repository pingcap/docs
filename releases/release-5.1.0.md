---
title: TiDB 5.1 Release Notes
---

# TiDB 5.1 リリースノート {#tidb-5-1-release-notes}

発売日：2021年6月24日

TiDB バージョン: 5.1.0

v5.1 の主な新機能または改善点は次のとおりです。

-   MySQL 8.0 の共通テーブル式 (CTE) 機能をサポートして、SQL ステートメントの読みやすさと実行効率を向上させます。
-   コード開発の柔軟性を向上させるために、オンラインでの列の型の変更をサポートします。
-   デフォルトで実験的機能として有効になっている、クエリの安定性を向上させる新しい統計タイプを導入します。
-   MySQL 8.0 の動的特権機能をサポートして、特定の操作をよりきめ細かく制御できるようにします。
-   ステイル読み取り機能を使用してローカル レプリカから直接データを読み取ることをサポートし、読み取りのレイテンシーを短縮し、クエリのパフォーマンスを向上させます (Experimental)。
-   ロックビュー機能を追加して、データベース管理者 (DBA) がトランザクション ロック イベントを監視し、デッドロックの問題をトラブルシューティングできるようにします (Experimental)。
-   バックグラウンド タスクに TiKV 書き込みレート リミッターを追加して、読み取りおよび書き込み要求のレイテンシーを安定させます。

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v5.1 にアップグレードする場合、すべての中間バージョンの互換性の変更点を知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                      | タイプを変更 | 説明                                                                                                                          |
| :--------------------------------------------------------------------------------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------- |
| [`cte_max_recursion_depth`](/system-variables.md#cte_max_recursion_depth)                | 新規追加   | 共通テーブル式の最大再帰深度を制御します。                                                                                                       |
| [`init_connect`](/system-variables.md#init_connect)                                      | 新規追加   | TiDBサーバーへの初期接続を制御します。                                                                                                       |
| [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)          | 新規追加   | TiDB が統計を収集する方法を制御します。この変数のデフォルト値は`2`です。これは実験的機能です。                                                                         |
| [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)    | 新規追加   | 接続している TiDBサーバーでSecurity強化モード (SEM) が有効になっているかどうかを示します。この変数の設定は、TiDBサーバーを再起動しないと変更できません。                                    |
| [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)                   | 新規追加   | オプティマイザーのコスト見積もりを無視し、クエリの実行に MPP モードを強制的に使用するかどうかを制御します。この変数のデータ型は`BOOL`で、デフォルト値は`false`です。                                 |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | 新規追加   | 分割されたテーブルの動的プルーニング モードを有効にするかどうかを指定します。この機能は実験的です。この変数のデフォルト値は`static`です。これは、分割されたテーブルの動的プルーニング モードがデフォルトで無効になっていることを意味します。 |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                             | タイプを変更 | 説明                                                                                                                                                                            |
| :------------- | :------------------------------------------------------------------------------------------------------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB 構成ファイル    | [`security.enable-sem`](/tidb-configuration-file.md#enable-sem)                                          | 新規追加   | Security拡張モード (SEM) を有効にするかどうかを制御します。この構成項目のデフォルト値は`false`で、これは SEM が無効であることを意味します。                                                                                           |
| TiDB 構成ファイル    | `performance.committer-concurrency`                                                                      | 修正済み   | 単一トランザクションのコミット フェーズでのコミット操作に関連する要求の同時実行数を制御します。デフォルト値が`16`から`128`に変更されました。                                                                                                   |
| TiDB 構成ファイル    | [`performance.tcp-no-delay`](/tidb-configuration-file.md#tcp-no-delay)                                   | 新規追加   | TCPレイヤーで TCP_NODELAY を有効にするかどうかを決定します。デフォルト値は`true`で、これは TCP_NODELAY が有効であることを意味します。                                                                                          |
| TiDB 構成ファイル    | [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)                                     | 新規追加   | TiDB がインスタンス レベルでオプティマイザーのコスト見積もりを無視し、MPP モードを適用するかどうかを制御します。デフォルト値は`false`です。この構成項目は、システム変数[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。 |
| TiDB 構成ファイル    | [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity)     | 新規追加   | 1 つの TiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルに記録できるデッドロック イベントの最大数を設定します。デフォルト値は`10`です。                             |
| TiKV 構成ファイル    | [`abort-on-panic`](/tikv-configuration-file.md#abort-on-panic)                                           | 新規追加   | TiKV がパニックしたときに、 `abort`プロセスがシステムにコア ダンプ ファイルの生成を許可するかどうかを設定します。デフォルト値は`false`です。これは、コア ダンプ ファイルの生成が許可されていないことを意味します。                                                         |
| TiKV 構成ファイル    | [`hibernate-regions`](/tikv-configuration-file.md#hibernate-regions)                                     | 修正済み   | デフォルト値が`false`から`true`に変更されました。リージョンが長時間アイドル状態の場合、自動的に休止状態に設定されます。                                                                                                            |
| TiKV 構成ファイル    | [`old-value-cache-memory-quota`](/tikv-configuration-file.md#old-value-cache-memory-quota)               | 新規追加   | TiCDC の古い値によるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                                |
| TiKV 構成ファイル    | [`sink-memory-quota`](/tikv-configuration-file.md#sink-memory-quota)                                     | 新規追加   | TiCDC データ変更イベントによるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                           |
| TiKV 構成ファイル    | [`incremental-scan-threads`](/tikv-configuration-file.md#incremental-scan-threads)                       | 新規追加   | 履歴データを増分スキャンするタスクのスレッド数を設定します。デフォルト値は`4`です。これは、タスクに 4 つのスレッドがあることを意味します。                                                                                                      |
| TiKV 構成ファイル    | [`incremental-scan-concurrency`](/tikv-configuration-file.md#incremental-scan-concurrency)               | 新規追加   | 履歴データを増分スキャンするタスクの同時実行の最大数を設定します。デフォルト値は`6`です。これは、最大で 6 つのタスクを同時に実行できることを意味します。                                                                                               |
| TiKV 構成ファイル    | [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 修正済み   | 保留中の圧縮バイトのソフト制限。デフォルト値が`"64GB"`から`"192GB"`に変更されました。                                                                                                                           |
| TiKV 構成ファイル    | [`storage.io-rate-limit`](/tikv-configuration-file.md#storageio-rate-limit)                              | 新規追加   | TiKV 書き込みの I/O レートを制御します。 `storage.io-rate-limit.max-bytes-per-sec`のデフォルト値は`"0MB"`です。                                                                                         |
| TiKV 構成ファイル    | [`resolved-ts.enable`](/tikv-configuration-file.md#enable)                                               | 新規追加   | すべてのリージョンリーダーの`resolved-ts`を維持するかどうかを決定します。デフォルト値は`true`です。                                                                                                                   |
| TiKV 構成ファイル    | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                     | 新規追加   | `resolved-ts`が転送される間隔。デフォルト値は`"1s"`です。値は動的に変更できます。                                                                                                                            |
| TiKV 構成ファイル    | [`resolved-ts.scan-lock-pool-size`](/tikv-configuration-file.md#scan-lock-pool-size)                     | 新規追加   | `resolved-ts` .デフォルト値は`2`です。                                                                                                                                                  |

### その他 {#others}

-   アップグレードの前に、TiDB 構成の値を確認してください[`feedback-probability`](https://docs.pingcap.com/tidb/v5.1/tidb-configuration-file#feedback-probability) 。値が 0 でない場合、アップグレード後に「回復可能なゴルーチンでpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDB の Go コンパイラ バージョンを go1.13.7 から go1.16.4 にアップグレードすると、TiDB のパフォーマンスが向上します。あなたが TiDB 開発者である場合は、Go コンパイラのバージョンをアップグレードして、コンパイルがスムーズに行われるようにしてください。
-   TiDB のローリング アップグレード中に、TiDB Binlogを使用するクラスター内にクラスター化されたインデックスを含むテーブルを作成しないようにします。
-   TiDB のローリング アップグレード中は、 `alter table ... modify column`や`alter table ... change column`のようなステートメントを実行しないでください。
-   v5.1 以降、各テーブルのTiFlashレプリカを構築するときに、システム テーブルのレプリカを設定することはサポートされなくなりました。クラスターをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、アップグレードは失敗します。
-   TiCDC の`cdc cli changefeed`コマンドの`--sort-dir`パラメータを非推奨にします。代わりに、 `cdc server`コマンドで`--sort-dir`を設定できます。 [#1795](https://github.com/pingcap/tiflow/pull/1795)
-   TiDB 5.1 にアップグレードした後、TiDB が「function READ ONLY has only noop implementation」というエラーを返した場合、値[`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)を`ON`に設定することで、TiDB にこのエラーを無視させることができます。これは、MySQL の`read_only`変数がまだ TiDB で有効になっていないためです (これは TiDB の「ヌープ」動作です)。したがって、この変数が TiDB で設定されていても、TiDB クラスターにデータを書き込むことができます。

## 新機能 {#new-features}

### SQL {#sql}

-   MySQL 8.0 の Common Table Expression (CTE) 機能をサポートします。

    この機能は、階層データを再帰的または非再帰的にクエリする機能を TiDB に提供し、ツリー クエリを使用して、人事、製造、金融市場、教育などの複数のセクターでアプリケーション ロジックを実装するニーズを満たします。

    TiDB では、 `WITH`ステートメントを適用して Common Table Expressions を使用できます。 [ユーザー文書](/sql-statements/sql-statement-with.md) , [#17472](https://github.com/pingcap/tidb/issues/17472)

-   MySQL 8.0 の動的特権機能をサポートします。

    動的権限を使用して`SUPER`特権を制限し、TiDB により柔軟な特権構成を提供して、よりきめ細かいアクセス制御を実現します。たとえば、動的権限を使用して、 `BACKUP`つと`RESTORE`の操作しか実行できないユーザー アカウントを作成できます。

    サポートされている動的権限は次のとおりです。

    -   `BACKUP_ADMIN`
    -   `RESTORE_ADMIN`
    -   `ROLE_ADMIN`
    -   `CONNECTION_ADMIN`
    -   `SYSTEM_VARIABLES_ADMIN`

    プラグインを使用して新しい権限を追加することもできます。サポートされているすべての権限を確認するには、 `SHOW PRIVILEGES`ステートメントを実行します。 [ユーザー文書](/privilege-management.md)

-   TiDB 管理者権限をよりきめ細かく分割するSecurity Enhanced Mode (SEM) 用の新しい構成項目を追加します。

    Security拡張モードはデフォルトで無効になっています。有効にするには、 [ユーザー文書](/system-variables.md#tidb_enable_enhanced_security)を参照してください。

-   列の種類をオンラインで変更する機能を強化します。 `ALTER TABLE`ステートメントを使用して列の型をオンラインで変更できるようになりました。

    -   `VARCHAR`から`BIGINT`への変更
    -   `DECIMAL`精度の変更
    -   `VARCHAR(10)` ～ `VARCHAR(5)`の長さの圧縮

    [ユーザー文書](/sql-statements/sql-statement-modify-column.md)

-   指定された時点または指定された時間範囲から履歴データを読み取るために使用される新しい実験的機能であるステイル読み取りを実行するために、新しい SQL 構文`AS OF TIMESTAMP`を導入します。

    [ユーザー文書](/stale-read.md) 、 [#21094](https://github.com/pingcap/tidb/issues/21094)

    `AS OF TIMESTAMP`の例は次のとおりです。

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

-   新しい統計タイプ`tidb_analyze_version = 2` (Experimental) を導入します。

    `tidb_analyze_version`は既定で`2`に設定されています。これにより、バージョン 1 のハッシュ競合によって大量のデータ ボリュームで発生する可能性のある大きなエラーが回避され、ほとんどのシナリオで推定精度が維持されます。

    [ユーザー文書](/statistics.md)

### トランザクション {#transaction}

-   Lock ビュー機能をサポート (Experimental)

    ロックビュー機能は、悲観的ロックのロック競合とロック待機に関する詳細情報を提供します。これは、DBA がトランザクションのロック状態を観察し、デッドロックの問題をトラブルシューティングするのに役立ちます。 [#24199](https://github.com/pingcap/tidb/issues/24199)

    ユーザー文書:

    -   クラスター内のすべての TiKV ノードで現在発生している悲観的ロックとその他のロックをビュー[`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDB ノードで最近発生したいくつかのデッドロック エラーをビュー[`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDB ノードで現在実行されているトランザクション情報をビュー。 [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### パフォーマンス {#performance}

-   データ レプリカの古い読み取り (Experimental)

    ローカル レプリカ データを直接読み取り、読み取りレイテンシーを短縮し、クエリ パフォーマンスを向上させる

    [ユーザー文書](/stale-read.md) 、 [#21094](https://github.com/pingcap/tidb/issues/21094)

-   デフォルトで Hibernate リージョン機能を有効にします。

    リージョンが長時間非アクティブ状態にある場合、自動的にサイレント状態に設定され、LeaderとFollower間のハートビート情報のシステム オーバーヘッドが削減されます。

    [ユーザー文書](/tikv-configuration-file.md#hibernate-regions) 、 [#10266](https://github.com/tikv/tikv/pull/10266)

### 安定性 {#stability}

-   TiCDC の複製安定性の問題を解決する

    -   次のシナリオで OOM を回避するために、TiCDCメモリ使用量を改善します。
    -   レプリケーションの中断中に 1 TB を超える大量のデータが蓄積されると、再レプリケーションによって OOM の問題が発生します。
    -   大量のデータ書き込みは、TiCDC で OOM の問題を引き起こします。
    -   次のシナリオで TiCDC レプリケーションが中断される可能性を減らします。

        [プロジェクト#11](https://github.com/pingcap/tiflow/projects/11)

        -   ネットワークが不安定な場合のレプリケーションの中断
        -   一部の TiKV/PD/TiCDC ノードがダウンした場合のレプリケーションの中断

-   TiFlashstorageメモリ制御

    リージョンスナップショット生成の速度とメモリ使用量を最適化し、OOM の可能性を減らします

-   TiKV バックグラウンド タスクの書き込みレート リミッターを追加します (TiKV 書き込みレート リミッター)

    読み取りおよび書き込み要求の期間の安定性を確保するために、TiKV 書き込みレート リミッターは、GC や圧縮などの TiKV バックグラウンド タスクの書き込みトラフィックを平滑化します。 TiKV バックグラウンドタスク書き込みレートリミッターのデフォルト値は「0MB」です。この値を、クラウド ディスクの製造元によって指定された最大 I/O 帯域幅など、ディスクの最適な I/O 帯域幅に設定することをお勧めします。

    [ユーザー文書](/tikv-configuration-file.md#storageio-rate-limit) 、 [#9156](https://github.com/tikv/tikv/issues/9156)

-   複数のスケーリング タスクが同時に実行されるときのスケジューリングの安定性の問題を解決する

### テレメトリー {#telemetry}

TiDB は、実行ステータスと失敗ステータスを含む、TiDB クラスター要求の実行ステータスをテレメトリに追加します。

情報とこの動作を無効にする方法について詳しくは、 [テレメトリー](/telemetry.md)を参照してください。

## 改良点 {#improvements}

-   TiDB

    -   内蔵機能をサポート`VITESS_HASH()` [#23915](https://github.com/pingcap/tidb/pull/23915)
    -   列挙型のデータの TiKV へのプッシュ ダウンをサポートして、 `WHERE`句で列挙型を使用する場合のパフォーマンスを向上させます[#23619](https://github.com/pingcap/tidb/issues/23619)
    -   `RENAME USER`構文[#23648](https://github.com/pingcap/tidb/issues/23648)をサポート
    -   ウィンドウ関数の計算を最適化して、ROW_NUMBER() でデータをページングする際の TiDB OOM の問題を解決します[#23807](https://github.com/pingcap/tidb/issues/23807)
    -   `UNION ALL`を使用して多数の`SELECT`ステートメントを結合する場合の TiDB OOM 問題を解決するために`UNION ALL`の計算を最適化します[#21441](https://github.com/pingcap/tidb/issues/21441)
    -   パーティション化されたテーブルの動的プルーニング モードを最適化して、パフォーマンスと安定性を向上させる[#24150](https://github.com/pingcap/tidb/issues/24150)
    -   複数のシナリオで発生する`Region is Unavailable`問題を修正する[プロジェクト#62](https://github.com/pingcap/tidb/projects/62)
    -   頻繁なスケジューリング状況で発生する可能性のある`Region is Unavailable`問題を修正します
    -   高負荷の書き込み状況で発生する可能性のある問題を`Region is Unavailable`修正
    -   CPU 使用率が高くならないように、キャッシュされた統計が最新の場合は`mysql.stats_histograms`テーブルを頻繁に読み取らないようにしてください[#24317](https://github.com/pingcap/tidb/pull/24317)

-   TiKV

    -   `zstd`を使用してリージョンのスナップショットを圧縮し、重いスケジューリングまたはスケーリングの場合にノード間の大きなスペースの違いを防ぎます[#10005](https://github.com/tikv/tikv/pull/10005)

    -   複数のケースで OOM の問題を解決する[#10183](https://github.com/tikv/tikv/issues/10183)

        -   各モジュールのメモリ使用量の追跡を追加
        -   Raftエントリ キャッシュが大きすぎるために発生する OOM の問題を解決する
        -   積み重ねられた GC タスクによって引き起こされる OOM の問題を解決する
        -   一度にRaftログからメモリにフェッチするRaftエントリが多すぎることによって発生する OOM の問題を解決する

    -   リージョンをより均等に分割して、ホットスポット書き込みがある場合にリージョンサイズの増加が分割速度を超えるという問題を軽減します[#9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   `Union All` 、 `TopN` 、および`Limit`関数をサポート
    -   MPP モードでの左外部結合と半逆結合を含むデカルト積をサポート
    -   ロック操作を最適化して、実行中の DDL ステートメントと読み取り操作が相互にブロックされないようにします。
    -   TiFlashによる期限切れデータのクリーンアップを最適化
    -   TiFlashstorageレベルで`timestamp`列のクエリ フィルタのさらなるフィルタリングをサポート
    -   クラスター内に多数のテーブルがある場合のTiFlashの起動とスケーラビリティの速度を向上させます
    -   不明な CPU で実行する場合のTiFlash の互換性を改善

-   PD

    -   `scatter region`スケジューラー[#3602](https://github.com/pingcap/pd/pull/3602)を追加した後の予期しない統計の回避
    -   スケーリング プロセスにおける複数のスケジューリングの問題を解決する

        -   レプリカ スナップショットの生成プロセスを最適化して、スケーリング中の遅いスケジューリングの問題を解決する[#3563](https://github.com/tikv/pd/issues/3563) [#10059](https://github.com/tikv/tikv/pull/10059) [#10001](https://github.com/tikv/tikv/pull/10001)
        -   トラフィックの変化によるハートビートのプレッシャーによって発生する遅いスケジューリングの問題を解決する[#3693](https://github.com/tikv/pd/issues/3693) [#3739](https://github.com/tikv/pd/issues/3739) [#3728](https://github.com/tikv/pd/issues/3728) [#3751](https://github.com/tikv/pd/issues/3751)
        -   スケジューリングによる大規模なクラスターのスペースの不一致を減らし、スケジューリング式を最適化して、圧縮率の大きな不一致によって引き起こされるバーストの問題 (異種のスペース クラスターに似ています) を防止します[#3592](https://github.com/tikv/pd/issues/3592) [#10005](https://github.com/tikv/tikv/pull/10005)

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマでのシステム テーブルのバックアップと復元のサポート[#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)
        -   仮想ホスト アドレッシング モード[#10243](https://github.com/tikv/tikv/pull/10243)に基づく S3 互換storageをサポートします。
        -   backupmeta のフォーマットを最適化してメモリ使用量を削減する[#1171](https://github.com/pingcap/br/pull/1171)

    -   TiCDC

        -   一部のログ メッセージの説明をより明確にし、問題の診断に役立つように改善しました[#1759](https://github.com/pingcap/tiflow/pull/1759)
        -   バック プレッシャー機能をサポートして、TiCDC スキャン速度がダウンストリーム処理能力を感知できるようにします[#10151](https://github.com/tikv/tikv/pull/10151)
        -   TiCDC が初期スキャンを実行するときのメモリ使用量を減らします[#10133](https://github.com/tikv/tikv/pull/10133)
        -   悲観的トランザクションにおける TiCDC Old Value のキャッシュ ヒット率を改善する[#10089](https://github.com/tikv/tikv/pull/10089)

    -   Dumpling

        -   TiDB v4.0 からデータをエクスポートするロジックを改善して、TiDB がメモリ不足 (OOM) になるのを回避します[#273](https://github.com/pingcap/dumpling/pull/273)

        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正[#280](https://github.com/pingcap/dumpling/pull/280)

    -   TiDB Lightning

        -   データのインポート速度を向上させます。最適化の結果は、TPC-C データのインポート速度が 30% 向上し、より多くのインデックス (5 つのインデックス) を持つ大きなテーブル (2 TB 以上) のインポート速度が 50% 以上向上したことを示しています。 [#753](https://github.com/pingcap/br/pull/753)
        -   インポートするデータとターゲット クラスタの事前チェックをインポート前に追加し、インポート要件を満たしていない場合はエラーを報告してインポート プロセスを拒否します[#999](https://github.com/pingcap/br/pull/999)
        -   ローカル バックエンドでのチェックポイント更新のタイミングを最適化して、ブレークポイントからの再起動のパフォーマンスを向上させます[#1080](https://github.com/pingcap/br/pull/1080)

## バグの修正 {#bug-fixes}

-   TiDB

    -   射影結果が空の場合、プロジェクト消去の実行結果がおかしくなることがある問題を修正[#23887](https://github.com/pingcap/tidb/issues/23887)
    -   場合によっては列に`NULL`値が含まれている場合に、間違ったクエリ結果が返される問題を修正します[#23891](https://github.com/pingcap/tidb/issues/23891)
    -   スキャンに仮想列が含まれている場合、MPP プランの生成を禁止する[#23886](https://github.com/pingcap/tidb/issues/23886)
    -   Plan Cache [#23187](https://github.com/pingcap/tidb/issues/23187) [#23144](https://github.com/pingcap/tidb/issues/23144) [#23304](https://github.com/pingcap/tidb/issues/23304) [#23290](https://github.com/pingcap/tidb/issues/23290)での`PointGet`と`TableDual`の間違った再利用を修正
    -   オプティマイザーがクラスター化インデックス[#23906](https://github.com/pingcap/tidb/issues/23906)の`IndexMerge`プランを構築するときに発生するエラーを修正します。
    -   BIT 型エラーの型推論を修正します[#23832](https://github.com/pingcap/tidb/issues/23832)
    -   `PointGet`演算子が存在する場合、一部のオプティマイザー ヒントが有効にならない問題を修正します[#23570](https://github.com/pingcap/tidb/issues/23570)
    -   エラーが原因でロールバックすると DDL 操作が失敗する可能性がある問題を修正します[#23893](https://github.com/pingcap/tidb/issues/23893)
    -   バイナリ リテラル定数のインデックス範囲が正しく構築されていない問題を修正します[#23672](https://github.com/pingcap/tidb/issues/23672)
    -   場合によっては`IN`句の潜在的な間違った結果を修正します[#23889](https://github.com/pingcap/tidb/issues/23889)
    -   一部の文字列関数の間違った結果を修正します[#23759](https://github.com/pingcap/tidb/issues/23759)
    -   ユーザーが`REPLACE`操作を実行するには、テーブルに対して`INSERT`と`DELETE`両方の権限が必要です[#23909](https://github.com/pingcap/tidb/issues/23909)
    -   ユーザーが`REPLACE`操作を実行するには、テーブルに対して`INSERT`と`DELETE`両方の権限が必要です[#24070](https://github.com/pingcap/tidb/pull/24070)
    -   間違った`TableDual`バイナリとバイトの比較によって引き起こされた計画を修正します[#23846](https://github.com/pingcap/tidb/issues/23846)
    -   場合によっては、プレフィックス インデックスとインデックス結合を使用することによって引き起こさpanicの問題を修正します。 [#24547](https://github.com/pingcap/tidb/issues/24547) [#24716](https://github.com/pingcap/tidb/issues/24716) [#24717](https://github.com/pingcap/tidb/issues/24717)
    -   トランザクション[#24741](https://github.com/pingcap/tidb/issues/24741)の`point get`ステートメントで、 `point get`の準備済みプラン キャッシュが誤って使用される問題を修正します。
    -   照合順序が`ascii_bin`または`latin1_bin` [#24569](https://github.com/pingcap/tidb/issues/24569)の場合に間違ったプレフィックス インデックス値を書き込む問題を修正します。
    -   進行中のトランザクションが GC ワーカーによって中断される可能性がある問題を修正します[#24591](https://github.com/pingcap/tidb/issues/24591)
    -   `new-collation`が有効で`new-row-format`が無効の場合、クラスタ化インデックスでポイントクエリが間違っている可能性があるバグを修正[#24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフル ハッシュ結合[#24490](https://github.com/pingcap/tidb/pull/24490)のパーティション キーの変換をリファクタリングする
    -   `HAVING`句[#24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプランを作成するときに発生するpanicの問題を修正します。
    -   列のプルーニングの改善により、 `Apply`と`Join`演算子の結果が正しくない問題を修正します[#23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリ ロックが解決できないバグを修正[#24384](https://github.com/pingcap/tidb/issues/24384)
    -   重複した fm-sketch レコードを引き起こす可能性のある統計の GC の問題を修正します[#24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観悲観的ロックが`ErrKeyExists`エラー[#23799](https://github.com/pingcap/tidb/issues/23799)を受け取った場合、不要な悲観悲観的ロールバックを回避します。
    -   sql_mode に`ANSI_QUOTES` [#24429](https://github.com/pingcap/tidb/issues/24429)含まれている場合、数値リテラルが認識されない問題を修正します。
    -   リストされていないパーティションからデータを読み取る`INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`などのステートメントを禁止します[#24746](https://github.com/pingcap/tidb/issues/24746)
    -   SQL ステートメントに`GROUP BY`と`UNION` [#24281](https://github.com/pingcap/tidb/issues/24281)の両方が含まれている場合に発生する可能性のある`index out of range`エラーを修正します。
    -   `CONCAT`関数が照合順序[#24296](https://github.com/pingcap/tidb/issues/24296)を正しく処理しない問題を修正
    -   `collation_server`グローバル変数が新しいセッションで有効にならない問題を修正[#24156](https://github.com/pingcap/tidb/pull/24156)

-   TiKV

    -   コプロセッサが`IN`式の符号付きまたは符号なし整数型を適切に処理できない問題を修正します[#9821](https://github.com/tikv/tikv/issues/9821)
    -   SST ファイルのバッチ取り込み後に空のリージョンが多数発生する問題を修正します[#964](https://github.com/pingcap/br/issues/964)
    -   ファイル辞書ファイルが破損した後、TiKV が起動できなくなるバグを修正[#9886](https://github.com/tikv/tikv/issues/9886)
    -   古い値を読み取ることによって発生する TiCDC OOM の問題を修正します[#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin` [#24548](https://github.com/pingcap/tidb/issues/24548)の場合にクラスター化された主キー列のセカンダリ インデックスに空の値が表示される問題を修正します。
    -   panicが発生したときに TiKV がコア ダンプ ファイルを生成できるようにする`abort-on-panic`構成を追加します。コア ダンプ[#10216](https://github.com/tikv/tikv/pull/10216)を有効にするには、ユーザーが環境を正しく構成する必要があります。
    -   TiKV がビジーでないときに発生する`point get`クエリのパフォーマンス低下の問題を修正します[#10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合、PDLeaderの再選が遅い問題を修正[#3697](https://github.com/tikv/pd/issues/3697)

    -   存在しないストアから evict リーダー スケジューラを削除するときに発生するpanicの問題を修正します[#3660](https://github.com/tikv/pd/issues/3660)

    -   オフライン ピアがマージされた後、統計が更新されない問題を修正します[#3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   時刻型を整数型にキャストすると、結果が正しくなくなる問題を修正
    -   `receiver`が 10 秒以内に対応するタスクを見つけられないバグを修正
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性がある問題を修正
    -   `bitwise`オペレータの挙動がTiDBと異なる不具合を修正
    -   `prefix key`を使用するときに範囲が重複することによって引き起こされるアラートの問題を修正します。
    -   文字列型を整数型にキャストしたときに誤った結果が返される問題を修正
    -   連続した高速書き込みによってTiFlash がメモリ不足になる問題を修正
    -   テーブル GC 中に null ポインターの例外が発生する可能性がある潜在的な問題を修正します。
    -   削除されたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正します
    -   BR復元中にTiFlash がpanicすることがある問題を修正
    -   共有デルタ インデックスを同時に複製するときの誤った結果の問題を修正します。
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるpanicを修正します
    -   TiFlash が非同期コミットからフォールバックしたロックを解決できない問題を修正
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれている場合に誤った結果が返される問題を修正
    -   セグメント分割中に発生するTiFlashpanicの問題を修正

-   ツール

    -   TiDB Lightning

        -   KVデータ生成時にTiDB Lightningpanicが発生する問題を修正[#1127](https://github.com/pingcap/br/pull/1127)
        -   データのインポート時にキーの合計サイズが raft エントリの制限を超えたために、リージョンのバッチ分割が失敗するバグを修正します[#969](https://github.com/pingcap/br/issues/969)
        -   CSV ファイルのインポート時に、ファイルの最終行に改行文字 ( `\r\n` ) が含まれていない場合、エラーが報告される問題を修正します[#1133](https://github.com/pingcap/br/issues/1133)
        -   インポートするテーブルに double 型の auto-increment カラムが含まれている場合、auto_increment の値が異常な[#1178](https://github.com/pingcap/br/pull/1178)になる問題を修正

    -   バックアップと復元 (BR)
        -   いくつかの TiKV ノードの障害によって引き起こされるバックアップの中断の問題を修正します[#980](https://github.com/pingcap/br/issues/980)

    -   TiCDC

        -   Unified Sorter の同時実行の問題を修正し、役に立たないエラー メッセージをフィルター処理する[#1678](https://github.com/pingcap/tiflow/pull/1678)
        -   MinIO [#1463](https://github.com/pingcap/tiflow/issues/1463)で冗長ディレクトリを作成するとレプリケーションが中断することがある不具合を修正
        -   `explicit_defaults_for_timestamp`セッション変数のデフォルト値を ON に設定して、 MySQL 5.7ダウンストリームがアップストリーム TiDB [#1585](https://github.com/pingcap/tiflow/issues/1585)と同じ動作を維持するようにします。
        -   `io.EOF`の扱いを誤るとレプリケーションが中断することがある問題を修正[#1633](https://github.com/pingcap/tiflow/issues/1633)
        -   TiCDC ダッシュボードで TiKV CDC エンドポイントの CPU メトリックを修正する[#1645](https://github.com/pingcap/tiflow/pull/1645)
        -   `defaultBufferChanSize`を増やして、場合によってはレプリケーションのブロックを回避します[#1259](https://github.com/pingcap/tiflow/issues/1259)
        -   Avro 出力[#1712](https://github.com/pingcap/tiflow/pull/1712)でタイム ゾーン情報が失われる問題を修正します。
        -   Unified Sorter の古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリの共有を禁止します[#1742](https://github.com/pingcap/tiflow/pull/1742)
        -   多くの古いリージョンが存在する場合に発生する KV クライアントのデッドロック バグを修正します[#1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[#1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正
        -   MySQL [#1750](https://github.com/pingcap/tiflow/pull/1750)にデータをレプリケートするときに SUPER 権限を必要とする`explicit_defaults_for_timestamp`の更新を元に戻します
        -   シンク フロー制御をサポートして、メモリオーバーフローのリスクを軽減します[#1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブル移動時にレプリケーションタスクが停止することがある不具合を修正[#1828](https://github.com/pingcap/tiflow/pull/1828)
        -   TiCDC changefeed チェックポイント[#1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により、TiKV GC セーフポイントがブロックされる問題を修正
