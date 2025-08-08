---
title: TiDB 5.1 Release Notes
summary: TiDB 5.1では、共通テーブル式、動的権限機能、およびステイル読み取りのサポートが導入されました。また、新しい統計タイプ、Lock ビュー機能、TiKV書き込みレートリミッターも含まれています。互換性に関する変更には、新しいシステム変数と設定変数が含まれます。その他の改善とバグ修正もこのリリースに含まれています。
---

# TiDB 5.1 リリースノート {#tidb-5-1-release-notes}

発売日：2021年6月24日

TiDB バージョン: 5.1.0

v5.1 の主な新機能または改善点は次のとおりです。

-   MySQL 8.0 の共通テーブル式 (CTE) 機能をサポートし、SQL ステートメントの読みやすさと実行効率が向上します。
-   コード開発の柔軟性を向上させるために、オンラインでの列タイプの変更をサポートします。
-   クエリの安定性を向上させるために新しい統計タイプを導入します。これは、実験的機能としてデフォルトで有効になっています。
-   MySQL 8.0 の動的権限機能をサポートし、特定の操作に対するよりきめ細かな制御を実装します。
-   読み取りレイテンシーを短縮し、クエリ パフォーマンスを向上させるために、 ステイル読み取り機能を使用してローカル レプリカからデータを直接読み取る機能をサポートします (Experimental)。
-   データベース管理者 (DBA) がトランザクション ロック イベントを観察し、デッドロックの問題をトラブルシューティングできるように、ロックビュー機能を追加します (Experimental)。
-   読み取りおよび書き込み要求のレイテンシーが安定するように、バックグラウンド タスクに TiKV 書き込みレート リミッターを追加します。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.1 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                      | タイプを変更   | 説明                                                                                                                |
| :--------------------------------------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------- |
| [`cte_max_recursion_depth`](/system-variables.md#cte_max_recursion_depth)                | 新しく追加された | 共通テーブル式の最大再帰深度を制御します。                                                                                             |
| [`init_connect`](/system-variables.md#init_connect)                                      | 新しく追加された | TiDBサーバーへの初期接続を制御します。                                                                                             |
| [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)          | 新しく追加された | TiDBが統計情報を収集する方法を制御します。この変数のデフォルト値は`2`です。これは実験的機能です。                                                              |
| [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)    | 新しく追加された | 接続しているTiDBサーバーでSecurity拡張モード（SEM）が有効になっているかどうかを示します。この変数設定は、TiDBサーバーを再起動しない限り変更できません。                             |
| [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)                   | 新しく追加された | オプティマイザのコスト推定を無視し、クエリ実行時にMPPモードを強制的に使用するかどうかを制御します。この変数のデータ型は`BOOL`で、デフォルト値は`false`です。                            |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | 新しく追加された | パーティションテーブルの動的プルーニングモードを有効にするかどうかを指定します。この機能は実験的です。この変数のデフォルト値は`static`で、パーティションテーブルの動的プルーニングモードはデフォルトで無効になっています。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                             | タイプを変更   | 説明                                                                                                                                                                         |
| :------------- | :------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB構成ファイル     | [`security.enable-sem`](/tidb-configuration-file.md#enable-sem)                                          | 新しく追加された | Security拡張モード（SEM）を有効にするかどうかを制御します。この設定項目のデフォルト値は`false`で、SEMは無効です。                                                                                                        |
| TiDB構成ファイル     | `performance.committer-concurrency`                                                                      | 修正済み     | 単一トランザクションのコミットフェーズにおけるコミット操作に関連するリクエストの同時実行数を制御します。デフォルト値は`16`から`128`に変更されます。                                                                                             |
| TiDB構成ファイル     | [`performance.tcp-no-delay`](/tidb-configuration-file.md#tcp-no-delay)                                   | 新しく追加された | TCPレイヤーでTCP_NODELAYを有効にするかどうかを決定します。デフォルト値は`true`で、TCP_NODELAYが有効であることを意味します。                                                                                              |
| TiDB構成ファイル     | [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)                                     | 新しく追加された | TiDBがインスタンスレベルでのOptimizerのコスト見積を無視し、MPPモードを強制するかどうかを制御します。デフォルト値は`false`です。この設定項目は、システム変数[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。 |
| TiDB構成ファイル     | [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity)     | 新しく追加された | 単一のTiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルに記録できるデッドロックイベントの最大数を設定します。デフォルト値は`10`です。                             |
| TiKV設定ファイル     | [`abort-on-panic`](/tikv-configuration-file.md#abort-on-panic)                                           | 新しく追加された | TiKVパニック発生時に、 `abort`プロセスがシステムにコアダンプファイルの生成を許可するかどうかを設定します。デフォルト値は`false`で、コアダンプファイルの生成は許可されません。                                                                           |
| TiKV設定ファイル     | [`hibernate-regions`](/tikv-configuration-file.md#hibernate-regions)                                     | 修正済み     | デフォルト値が`false`から`true`に変更されました。リージョンが長時間アイドル状態の場合、自動的に休止状態に設定されます。                                                                                                         |
| TiKV設定ファイル     | [`old-value-cache-memory-quota`](/tikv-configuration-file.md#old-value-cache-memory-quota)               | 新しく追加された | TiCDCの古い値によるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                              |
| TiKV設定ファイル     | [`sink-memory-quota`](/tikv-configuration-file.md#sink-memory-quota)                                     | 新しく追加された | TiCDCデータ変更イベントによるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                         |
| TiKV設定ファイル     | [`incremental-scan-threads`](/tikv-configuration-file.md#incremental-scan-threads)                       | 新しく追加された | 履歴データの増分スキャンタスクのスレッド数を設定します。デフォルト値は`4`で、タスクに4つのスレッドがあることを意味します。                                                                                                            |
| TiKV設定ファイル     | [`incremental-scan-concurrency`](/tikv-configuration-file.md#incremental-scan-concurrency)               | 新しく追加された | 履歴データの増分スキャンタスクの最大同時実行数を設定します。デフォルト値は`6`で、最大6つのタスクを同時に実行できます。                                                                                                              |
| TiKV設定ファイル     | [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 修正済み     | 保留中の圧縮バイトのソフト制限。デフォルト値は`"64GB"`から`"192GB"`に変更されます。                                                                                                                         |
| TiKV設定ファイル     | [`storage.io-rate-limit`](/tikv-configuration-file.md#storageio-rate-limit)                              | 新しく追加された | TiKV書き込みのI/Oレートを制御します。デフォルト値は`storage.io-rate-limit.max-bytes-per-sec`で、 `"0MB"`です。                                                                                        |
| TiKV設定ファイル     | [`resolved-ts.enable`](/tikv-configuration-file.md#enable)                                               | 新しく追加された | すべてのリージョンリーダーに対して`resolved-ts`維持するかどうかを決定します。デフォルト値は`true`です。                                                                                                              |
| TiKV設定ファイル     | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                     | 新しく追加された | `resolved-ts`転送する間隔。デフォルト値は`"1s"`です。この値は動的に変更できます。                                                                                                                         |
| TiKV設定ファイル     | [`resolved-ts.scan-lock-pool-size`](/tikv-configuration-file.md#scan-lock-pool-size)                     | 新しく追加された | TiKVが`resolved-ts`初期化する際にMVCC（マルチバージョン同時実行制御）ロックデータをスキャンするために使用するスレッドの数。デフォルト値は`2`です。                                                                                      |

### その他 {#others}

-   アップグレード前に、TiDB設定[`feedback-probability`](https://docs.pingcap.com/tidb/v5.1/tidb-configuration-file#feedback-probability)の値を確認してください。値が0でない場合、アップグレード後に「回復可能なゴルーチンでpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDBのGoコンパイラバージョンをgo1.13.7からgo1.16.4にアップグレードすると、TiDBのパフォーマンスが向上します。TiDB開発者の方は、スムーズなコンパイルを実現するために、Goコンパイラバージョンをアップグレードしてください。
-   TiDB ローリング アップグレード中に、TiDB Binlog を使用するクラスター内にクラスター化インデックスを持つテーブルを作成しないようにしてください。
-   TiDB ローリング アップグレード中は、 `alter table ... modify column`または`alter table ... change column`ようなステートメントを実行しないでください。
-   v5.1以降、各テーブルのTiFlashレプリカ構築時にシステムテーブルのレプリカを設定する機能はサポートされなくなりました。クラスターをアップグレードする前に、関連するシステムテーブルレプリカをクリアする必要があります。クリアしないと、アップグレードは失敗します。
-   TiCDCの`cdc cli changefeed`コマンドの`--sort-dir`パラメータは非推奨となりました。代わりに、 `cdc server`コマンドで`--sort-dir`パラメータを設定できます[＃1795](https://github.com/pingcap/tiflow/pull/1795)
-   TiDB 5.1にアップグレード後、TiDBが「関数 READ ONLY にはnoop実装のみがあります」というエラーを返す場合、 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)の値を`ON`に設定することで、このエラーを無視することができます。これは、MySQLの`read_only`変数がTiDBではまだ有効になっていないためです（これはTiDBでは「noop」動作です）。したがって、この変数がTiDBで設定されていても、TiDBクラスタにデータを書き込むことは可能です。

## 新機能 {#new-features}

### SQL {#sql}

-   MySQL 8.0 の共通テーブル式 (CTE) 機能をサポートします。

    この機能により、TiDB は階層データを再帰的または非再帰的にクエリする機能を持つようになり、人事、製造、金融市場、教育などの複数の分野でツリー クエリを使用してアプリケーション ロジックを実装するというニーズを満たします。

    TiDBでは、共通テーブル式[＃17472](https://github.com/pingcap/tidb/issues/17472)使用するために`WITH`文を適用できます[ユーザードキュメント](/sql-statements/sql-statement-with.md)

-   MySQL 8.0 の動的権限機能をサポートします。

    動的権限は、 `SUPER`権限を制限し、TiDB に柔軟な権限設定を提供して、よりきめ細かなアクセス制御を実現するために使用されます。例えば、動的権限を使用して、 `BACKUP`と`RESTORE`操作のみを実行できるユーザーアカウントを作成できます。

    サポートされている動的権限は次のとおりです。

    -   `BACKUP_ADMIN`
    -   `RESTORE_ADMIN`
    -   `ROLE_ADMIN`
    -   `CONNECTION_ADMIN`
    -   `SYSTEM_VARIABLES_ADMIN`

    プラグインを使って新しい権限を追加することもできます。サポートされているすべての権限を確認するには、 `SHOW PRIVILEGES`文を実行してください[ユーザードキュメント](/privilege-management.md)

-   Security拡張モード (SEM) の新しい構成項目を追加します。これにより、TiDB 管理者権限がより細かく分割されます。

    Security強化モードはデフォルトで無効になっています。有効にするには、 [ユーザードキュメント](/system-variables.md#tidb_enable_enhanced_security)参照してください。

-   オンラインでの列タイプの変更機能を強化しました。1 ステートメント`ALTER TABLE`使用したオンラインでの列タイプの変更をサポートします。これには以下が含まれますが、これらに限定されません。

    -   `VARCHAR`を`BIGINT`に変更
    -   `DECIMAL`精度の変更
    -   `VARCHAR(10)`の長さを`VARCHAR(5)`に圧縮する

    [ユーザードキュメント](/sql-statements/sql-statement-modify-column.md)

-   指定された時点または指定された時間範囲から履歴データを読み取るために使用される新しい実験的機能であるステイル読み取り を実行するための新しい SQL 構文`AS OF TIMESTAMP`を導入します。

    [ユーザードキュメント](/stale-read.md) [＃21094](https://github.com/pingcap/tidb/issues/21094)

    `AS OF TIMESTAMP`の例は以下のとおりです。

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

-   新しい統計タイプ`tidb_analyze_version = 2` (Experimental) を導入します。

    デフォルトでは`tidb_analyze_version`は`2`に設定されており、これによりバージョン 1 でのハッシュ競合によって大量のデータで発生する可能性のある大きなエラーが回避され、ほとんどのシナリオで推定精度が維持されます。

    [ユーザードキュメント](/statistics.md)

### トランザクション {#transaction}

-   ロックビュー機能のサポート（Experimental）

    ロックビュー機能は、悲観的ロックのロック競合とロック待機に関する詳細情報を提供し、DBA がトランザクションのロック状態を観察し、デッドロックの問題をトラブルシューティングするのに役立ちます[＃24199](https://github.com/pingcap/tidb/issues/24199)

    ユーザードキュメント:

    -   クラスター内のすべての TiKV ノードで現在発生している悲観的ロックとその他のロックをビュー[`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDBノードで最近発生したいくつかのデッドロックエラーをビュー: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDBノードで現在実行されているトランザクション情報をビュー: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### パフォーマンス {#performance}

-   データレプリカの古い読み取り（Experimental）

    ローカルレプリカデータを直接読み取り、読み取りレイテンシーを削減し、クエリパフォーマンスを向上させます。

    [ユーザードキュメント](/stale-read.md) [＃21094](https://github.com/pingcap/tidb/issues/21094)

-   Hibernate リージョン機能をデフォルトで有効にします。

    リージョンが長時間非アクティブ状態にある場合、自動的にサイレント状態に設定され、LeaderとFollower間のハートビート情報のシステム オーバーヘッドが削減されます。

    [ユーザードキュメント](/tikv-configuration-file.md#hibernate-regions) [＃10266](https://github.com/tikv/tikv/pull/10266)

### 安定性 {#stability}

-   TiCDCのレプリケーション安定性の問題を解決する

    -   以下のシナリオで OOM を回避するために TiCDC のメモリ使用量を改善します
    -   レプリケーション中断中に 1TB を超える大量のデータが蓄積されると、再レプリケーションによって OOM 問題が発生します。
    -   大量のデータ書き込みは TiCDC で OOM の問題を引き起こします。
    -   次のシナリオで TiCDC レプリケーションが中断される可能性を減らします。

        [プロジェクト#11](https://github.com/pingcap/tiflow/projects/11)

        -   ネットワークが不安定な場合のレプリケーションの中断
        -   一部の TiKV/PD/TiCDC ノードがダウンした場合のレプリケーションの中断

-   TiFlashstorageメモリ制御

    リージョンスナップショット生成の速度とメモリ使用量を最適化し、OOMの可能性を減らします。

-   TiKV バックグラウンド タスクの書き込みレート リミッターを追加します (TiKV 書き込みレート リミッター)

    読み取りおよび書き込みリクエストの持続時間の安定性を確保するため、TiKV書き込みレートリミッターは、GCやコンパクションなどのTiKVバックグラウンドタスクの書き込みトラフィックを平滑化します。TiKVバックグラウンドタスク書き込みレートリミッターのデフォルト値は「0MB」です。この値は、クラウドディスクメーカーが指定する最大I/O帯域幅など、ディスクの最適なI/O帯域幅に設定することをお勧めします。

    [ユーザードキュメント](/tikv-configuration-file.md#storageio-rate-limit) [＃9156](https://github.com/tikv/tikv/issues/9156)

-   複数のスケーリングタスクが同時に実行される場合のスケジュールの安定性の問題を解決します

### テレメトリー {#telemetry}

TiDB は、実行ステータスや失敗ステータスなど、テレメトリに TiDB クラスター要求の実行ステータスを追加します。

情報の詳細とこの動作を無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   組み込み関数`VITESS_HASH()` [＃23915](https://github.com/pingcap/tidb/pull/23915)をサポート
    -   `WHERE`節[＃23619](https://github.com/pingcap/tidb/issues/23619)で列挙型を使用するときにパフォーマンスを向上させるために列挙型のデータを TiKV にプッシュダウンすることをサポートします。
    -   `RENAME USER`構文[＃23648](https://github.com/pingcap/tidb/issues/23648)サポートする
    -   ROW_NUMBER() [＃23807](https://github.com/pingcap/tidb/issues/23807)でデータをページングする際の TiDB OOM 問題を解決するためにウィンドウ関数の計算を最適化します。
    -   `UNION ALL`の計算を最適化して、 `UNION ALL`使用して多数の`SELECT`文を結合する場合のTiDB OOM問題を解決します[＃21441](https://github.com/pingcap/tidb/issues/21441)
    -   パーティションテーブルの動的プルーニングモードを最適化してパフォーマンスと安定性を向上[＃24150](https://github.com/pingcap/tidb/issues/24150)
    -   複数のシナリオで発生する`Region is Unavailable`問題を修正する[プロジェクト#62](https://github.com/pingcap/tidb/projects/62)
    -   頻繁なスケジュール設定で発生する可能性のある複数の`Region is Unavailable`の問題を修正
    -   一部の高負荷書き込み状況で発生する可能性のある`Region is Unavailable`問題を修正しました
    -   キャッシュされた統計が最新の場合は、CPU使用率の上昇を避けるために、 `mysql.stats_histograms`テーブルを頻繁に読み取らないようにします[＃24317](https://github.com/pingcap/tidb/pull/24317)

-   TiKV

    -   `zstd`使用してリージョンスナップショットを圧縮し、高負荷のスケジュールやスケーリング[＃10005](https://github.com/tikv/tikv/pull/10005)の際にノード間の大きなスペース差を防ぐ

    -   複数のケースにおけるOOM問題の解決[＃10183](https://github.com/tikv/tikv/issues/10183)

        -   各モジュールのメモリ使用量追跡を追加する
        -   Raftエントリキャッシュが大きすぎることによって引き起こされるOOM問題を解決する
        -   GCタスクのスタックによって引き起こされるOOM問題を解決する
        -   一度にRaftログからメモリに取得するRaftエントリが多すぎるために発生する OOM 問題を解決します。

    -   ホットスポット書き込みがあるときに、リージョンサイズの増加が分割速度を超える問題を軽減するために、リージョンをより均等に分割します[＃9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   `Union All` `TopN`関数`Limit`サポート
    -   MPP モードで左外部結合と半反結合を含むカルテシアン積をサポートします。
    -   実行中のDDL文と読み取り操作が相互にブロックされることを回避するためにロック操作を最適化します。
    -   TiFlashによる期限切れデータのクリーンアップを最適化
    -   TiFlashstorageレベルで`timestamp`列のクエリ フィルターのさらなるフィルタリングをサポート
    -   多数のテーブルがクラスター内にある場合のTiFlashの起動とスケーラビリティ速度を改善
    -   不明なCPUで実行する場合のTiFlashの互換性を向上

-   PD

    -   `scatter region`スケジューラ[＃3602](https://github.com/pingcap/pd/pull/3602)追加した後の予期しない統計を回避する
    -   スケーリングプロセスにおける複数のスケジュールの問題を解決する

        -   レプリカスナップショットの生成プロセスを最適化して、スケーリング中の低速スケジュールの問題を解決します[＃3563](https://github.com/tikv/pd/issues/3563) [＃10059](https://github.com/tikv/tikv/pull/10059) [＃10001](https://github.com/tikv/tikv/pull/10001)
        -   トラフィックの変化によるハートビートの圧力によって発生する、遅いスケジューリングの問題を解決する[＃3693](https://github.com/tikv/pd/issues/3693) [＃3739](https://github.com/tikv/pd/issues/3739) [＃3728](https://github.com/tikv/pd/issues/3728) [＃3751](https://github.com/tikv/pd/issues/3751)
        -   スケジューリングによる大規模クラスタのスペースの不一致を減らし、大きな圧縮率の不一致によって引き起こされるバースト問題（異種スペースクラスタに類似）を防ぐためにスケジューリング式を最適化します[＃3592](https://github.com/tikv/pd/issues/3592) [＃10005](https://github.com/tikv/tikv/pull/10005)

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマ[＃1143](https://github.com/pingcap/br/pull/1143) [＃1078](https://github.com/pingcap/br/pull/1078)のシステムテーブルのバックアップと復元をサポート
        -   仮想ホストアドレスモード[＃10243](https://github.com/tikv/tikv/pull/10243)に基づくS3互換storageをサポート
        -   メモリ使用量を削減するためにバックアップメタのフォーマットを最適化します[＃1171](https://github.com/pingcap/br/pull/1171)

    -   TiCDC

        -   いくつかのログメッセージの説明をより明確かつ問題の診断に役立つように改善しました[＃1759](https://github.com/pingcap/tiflow/pull/1759)
        -   バックプレッシャー機能をサポートし、TiCDCスキャン速度が下流の処理能力を感知できるようにします[＃10151](https://github.com/tikv/tikv/pull/10151)
        -   TiCDCが初期スキャンを実行する際のメモリ使用量を削減する[＃10133](https://github.com/tikv/tikv/pull/10133)
        -   悲観的トランザクションにおける TiCDC の古い値のキャッシュヒット率を向上させる[＃10089](https://github.com/tikv/tikv/pull/10089)

    -   Dumpling

        -   TiDB v4.0 からデータをエクスポートするロジックを改善し、TiDB がメモリ不足 (OOM) になるのを回避します[＃273](https://github.com/pingcap/dumpling/pull/273)

        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正[＃280](https://github.com/pingcap/dumpling/pull/280)

    -   TiDB Lightning

        -   データのインポート速度を向上。最適化の結果、TPC-Cデータのインポート速度が30%向上し、インデックス数（5個）が多い大規模テーブル（2TB以上）のインポート速度が50%以上向上しました[＃753](https://github.com/pingcap/br/pull/753)
        -   インポートするデータとインポート前にターゲットクラスタの事前チェックを追加し、インポート要件を満たしていない場合はエラーを報告してインポートプロセスを拒否します[＃999](https://github.com/pingcap/br/pull/999)
        -   ローカルバックエンドでのチェックポイント更新のタイミングを最適化して、ブレークポイント[＃1080](https://github.com/pingcap/br/pull/1080)からの再開のパフォーマンスを向上します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   投影結果が空の場合にプロジェクト除去の実行結果が間違っている可能性がある問題を修正[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   列に`NULL`値が含まれている場合に間違ったクエリ結果が表示される問題を修正しました[＃23891](https://github.com/pingcap/tidb/issues/23891)
    -   スキャンに仮想列[＃23886](https://github.com/pingcap/tidb/issues/23886)が含まれている場合、MPP プランの生成を禁止します。
    -   プランキャッシュ[＃23187](https://github.com/pingcap/tidb/issues/23187) [＃23144](https://github.com/pingcap/tidb/issues/23144) [＃23304](https://github.com/pingcap/tidb/issues/23304) [＃23290](https://github.com/pingcap/tidb/issues/23290)での`PointGet`と`TableDual`の誤った再利用を修正
    -   オプティマイザがクラスタ化インデックス[＃23906](https://github.com/pingcap/tidb/issues/23906) `IndexMerge`プランを構築するときに発生するエラーを修正します
    -   BIT型エラーの型推論を修正[＃23832](https://github.com/pingcap/tidb/issues/23832)
    -   `PointGet`演算子が存在する場合に一部のオプティマイザヒントが有効にならない問題を修正[＃23570](https://github.com/pingcap/tidb/issues/23570)
    -   エラー[＃23893](https://github.com/pingcap/tidb/issues/23893)によりロールバック時にDDL操作が失敗する可能性がある問題を修正
    -   バイナリリテラル定数のインデックス範囲が正しく構築されない問題を修正[＃23672](https://github.com/pingcap/tidb/issues/23672)
    -   いくつかのケースで`IN`節の潜在的な誤った結果を修正[＃23889](https://github.com/pingcap/tidb/issues/23889)
    -   いくつかの文字列関数の誤った結果を修正[＃23759](https://github.com/pingcap/tidb/issues/23759)
    -   ユーザーは、テーブルに対して`REPLACE`操作を実行するために`INSERT`と`DELETE`両方の権限が必要になります[＃23909](https://github.com/pingcap/tidb/issues/23909)
    -   ユーザーは、テーブルに対して`REPLACE`操作を実行するために`INSERT`と`DELETE`両方の権限が必要になります[＃24070](https://github.com/pingcap/tidb/pull/24070)
    -   バイナリとバイトを誤って比較することによって発生した間違った`TableDual`計画を修正[＃23846](https://github.com/pingcap/tidb/issues/23846)
    -   一部のケースでプレフィックスインデックスとインデックス結合を使用することで発生するpanic問題を修正[＃24547](https://github.com/pingcap/tidb/issues/24547) [＃24716](https://github.com/pingcap/tidb/issues/24716) [＃24717](https://github.com/pingcap/tidb/issues/24717)
    -   `point get`の準備されたプランキャッシュがトランザクション[＃24741](https://github.com/pingcap/tidb/issues/24741)の`point get`文によって誤って使用される問題を修正しました。
    -   照合順序が`ascii_bin`または`latin1_bin`場合に間違ったプレフィックスインデックス値を書き込む問題を修正しました[＃24569](https://github.com/pingcap/tidb/issues/24569)
    -   GCワーカー[＃24591](https://github.com/pingcap/tidb/issues/24591)によって進行中のトランザクションが中断される可能性がある問題を修正
    -   `new-collation`が有効で`new-row-format`無効の場合、クラスター化インデックスでポイントクエリが間違って実行される可能性があるバグを修正しました[＃24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフルハッシュ結合[＃24490](https://github.com/pingcap/tidb/pull/24490)パーティションキーの変換をリファクタリングする
    -   `HAVING`句[＃24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプランを構築するときに発生するpanic問題を修正しました。
    -   列プルーニングの改善により、演算子`Apply`と`Join`結果が間違ってしまう問題を修正しました[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリロックが解決できないバグを修正[＃24384](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketch レコードの重複を引き起こす可能性のある統計の GC 問題を修正しました[＃24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的ロックが`ErrKeyExists`エラー[＃23799](https://github.com/pingcap/tidb/issues/23799)を受け取ったときに不要な悲観的ロールバックを回避する
    -   sql_modeに`ANSI_QUOTES` [＃24429](https://github.com/pingcap/tidb/issues/24429)が含まれている場合に数値リテラルが認識されない問題を修正しました
    -   `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`ような文は、リストされていないパーティション[＃24746](https://github.com/pingcap/tidb/issues/24746)からデータを読み取ることを禁止します。
    -   SQL文に`GROUP BY`と`UNION`両方が含まれている場合に発生する可能性のある`index out of range`エラーを修正します[＃24281](https://github.com/pingcap/tidb/issues/24281)
    -   `CONCAT`関数が照合順序[＃24296](https://github.com/pingcap/tidb/issues/24296)誤って処理する問題を修正しました
    -   `collation_server`グローバル変数が新しいセッション[＃24156](https://github.com/pingcap/tidb/pull/24156)で有効にならない問題を修正しました

-   TiKV

    -   コプロセッサが`IN`式[＃9821](https://github.com/tikv/tikv/issues/9821)の符号付きまたは符号なし整数型を適切に処理できない問題を修正しました。
    -   SST ファイルのバッチ取り込み後に多くの空の領域が発生する問題を修正[＃964](https://github.com/pingcap/br/issues/964)
    -   ファイル辞書ファイルが破損した後にTiKVが起動できなくなるバグを修正[＃9886](https://github.com/tikv/tikv/issues/9886)
    -   古い値の読み取りによって引き起こされる TiCDC OOM 問題を修正[＃9996](https://github.com/tikv/tikv/issues/9996) [＃9981](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin` [＃24548](https://github.com/pingcap/tidb/issues/24548)場合にクラスター化主キー列のセカンダリインデックスに空の値が含まれる問題を修正しました
    -   `abort-on-panic`設定を追加すると、panic発生時にTiKVがコアダンプファイルを生成できるようになります。コアダンプ[＃10216](https://github.com/tikv/tikv/pull/10216)を有効にするには、ユーザーは環境を正しく設定する必要があります。
    -   TiKVがビジーでないときに発生する`point get`クエリのパフォーマンス回帰の問題を修正しました[＃10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合にPDLeaderの再選出が遅くなる問題を修正[＃3697](https://github.com/tikv/pd/issues/3697)

    -   存在しないストア[＃3660](https://github.com/tikv/pd/issues/3660)からエビクト リーダー スケジューラを削除するときに発生するpanic問題を修正しました

    -   オフラインピアがマージされた後に統計が更新されない問題を修正[＃3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   時間型を整数型にキャストしたときに誤った結果が返される問題を修正しました
    -   `receiver`秒以内に対応するタスクが見つからないバグを修正
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性がある問題を修正
    -   `bitwise`演算子の動作がTiDBと異なるバグを修正
    -   `prefix key`使用する際に範囲が重複することで発生するアラートの問題を修正
    -   文字列型を整数型にキャストするときに誤った結果が返される問題を修正しました
    -   連続した高速書き込みによりTiFlashのメモリが不足する可能性がある問題を修正しました
    -   テーブルGC中にヌルポインタの例外が発生する可能性がある問題を修正しました
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanic問題を修正しました
    -   BRの復元中にTiFlashがpanic可能性がある問題を修正
    -   共有デルタインデックスを同時にクローン化する際に誤った結果が生成される問題を修正しました
    -   圧縮フィルタ機能が有効になっているときに発生する可能性のあるpanicを修正しました
    -   TiFlash が非同期コミットからフォールバックしたロックを解決できない問題を修正しました
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれている場合に誤った結果が返される問題を修正しました
    -   セグメント分割中に発生するTiFlashpanic問題を修正

-   ツール

    -   TiDB Lightning

        -   KVデータ生成時に発生するTiDB Lightning panicの問題を修正[＃1127](https://github.com/pingcap/br/pull/1127)
        -   データインポート中にキーの合計サイズがラフトエントリ制限を超えたためにバッチ分割リージョンが失敗するバグを修正[＃969](https://github.com/pingcap/br/issues/969)
        -   CSVファイルをインポートする際に、ファイルの最後の行に改行文字が含まれていない場合（ `\r\n` ）、エラーが報告される問題を修正しました[＃1133](https://github.com/pingcap/br/issues/1133)
        -   インポートするテーブルにdouble型の自動増分列が含まれている場合、auto_increment値が異常になる問題を修正しました[＃1178](https://github.com/pingcap/br/pull/1178)

    -   バックアップと復元 (BR)
        -   いくつかの TiKV ノードの障害によって発生するバックアップ中断の問題を修正[＃980](https://github.com/pingcap/br/issues/980)

    -   TiCDC

        -   Unified Sorter の同時実行の問題を修正し、役に立たないエラーメッセージをフィルタリングします[＃1678](https://github.com/pingcap/tiflow/pull/1678)
        -   冗長ディレクトリの作成によりMinIO [＃1463](https://github.com/pingcap/tiflow/issues/1463)でのレプリケーションが中断される可能性があるバグを修正
        -   MySQL 5.7ダウンストリームがアップストリーム TiDB [＃1585](https://github.com/pingcap/tiflow/issues/1585)と同じ動作を維持するように、 `explicit_defaults_for_timestamp`セッション変数のデフォルト値を ON に設定します。
        -   `io.EOF`の誤った処理によりレプリケーションが中断される可能性がある問題を修正[＃1633](https://github.com/pingcap/tiflow/issues/1633)
        -   TiCDCダッシュボード[＃1645](https://github.com/pingcap/tiflow/pull/1645)のTiKV CDCエンドポイントCPUメトリックを修正
        -   場合によってはレプリケーションのブロックを回避するために`defaultBufferChanSize`増やす[＃1259](https://github.com/pingcap/tiflow/issues/1259)
        -   Avro出力[＃1712](https://github.com/pingcap/tiflow/pull/1712)でタイムゾーン情報が失われる問題を修正
        -   Unified Sorter 内の古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリ[＃1742](https://github.com/pingcap/tiflow/pull/1742)共有を禁止します。
        -   多くの古いリージョンが存在する場合に発生する KV クライアントのデッドロックバグを修正[＃1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[＃1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正
        -   MySQL [＃1750](https://github.com/pingcap/tiflow/pull/1750)にデータを複製する際にSUPER権限を必要とする`explicit_defaults_for_timestamp`更新を元に戻します
        -   シンクフロー制御をサポートし、メモリオーバーフローのリスクを軽減します[＃1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブル[＃1828](https://github.com/pingcap/tiflow/pull/1828)移動する際にレプリケーションタスクが停止する可能性があるバグを修正
        -   TiCDC チェンジフィード チェックポイント[＃1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により TiKV GC セーフ ポイントがブロックされる問題を修正しました
