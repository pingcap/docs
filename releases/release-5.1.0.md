---
title: TiDB 5.1 Release Notes
summary: TiDB 5.1 では、共通テーブル式、動的権限機能、およびステイル読み取りのサポートが導入されています。また、新しい統計タイプ、Lock ビュー機能、および TiKV 書き込みレート リミッターも含まれています。互換性の変更には、新しいシステム変数と構成変数が含まれます。その他の改善とバグ修正もこのリリースに含まれています。
---

# TiDB 5.1 リリースノート {#tidb-5-1-release-notes}

発売日: 2021年6月24日

TiDB バージョン: 5.1.0

v5.1 の主な新機能または改善点は次のとおりです。

-   MySQL 8.0 の共通テーブル式 (CTE) 機能をサポートし、SQL ステートメントの読みやすさと実行効率を向上させます。
-   コード開発の柔軟性を向上させるために、オンラインでの列タイプの変更をサポートします。
-   クエリの安定性を向上させるために新しい統計タイプを導入しました。これは、実験的機能としてデフォルトで有効になっています。
-   MySQL 8.0 の動的権限機能をサポートし、特定の操作に対するよりきめ細かい制御を実装します。
-   読み取りレイテンシーを短縮し、クエリ パフォーマンスを向上させるために、 ステイル読み取り機能を使用してローカル レプリカからデータを直接読み取る機能をサポートします (Experimental)。
-   データベース管理者 (DBA) がトランザクション ロック イベントを観察し、デッドロックの問題をトラブルシューティングできるように、ロックビュー機能を追加します (Experimental)。
-   読み取りおよび書き込み要求のレイテンシーが安定するように、バックグラウンド タスクに TiKV 書き込みレート リミッターを追加します。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.1 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                      | タイプを変更   | 説明                                                                                                                                           |
| :--------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| [`cte_max_recursion_depth`](/system-variables.md#cte_max_recursion_depth)                | 新しく追加された | 共通テーブル式の最大再帰深度を制御します。                                                                                                                        |
| [`init_connect`](/system-variables.md#init_connect)                                      | 新しく追加された | TiDBサーバーへの初期接続を制御します。                                                                                                                        |
| [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)          | 新しく追加された | TiDB が統計を収集する方法を制御します。この変数のデフォルト値は`2`です。これは実験的機能です。                                                                                          |
| [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)    | 新しく追加された | 接続している TiDBサーバーでSecurity拡張モード (SEM) が有効になっているかどうかを示します。この変数設定は、TiDBサーバーを再起動しないと変更できません。                                                      |
| [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)                   | 新しく追加された | オプティマイザのコスト見積もりを無視し、クエリ実行に MPP モードを強制的に使用するかどうかを制御します。この変数のデータ型は`BOOL`で、デフォルト値は`false`です。                                                    |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | 新しく追加された | パーティション化されたテーブルに対して動的プルーニング モードを有効にするかどうかを指定します。この機能は実験的段階です。この変数のデフォルト値は`static`です。これは、パーティション化されたテーブルの動的プルーニング モードがデフォルトで無効になっていることを意味します。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                             | タイプを変更   | 説明                                                                                                                                                                             |
| :------------- | :------------------------------------------------------------------------------------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB 構成ファイル    | [`security.enable-sem`](/tidb-configuration-file.md#enable-sem)                                          | 新しく追加された | Security拡張モード (SEM) を有効にするかどうかを制御します。この構成項目のデフォルト値は`false`で、SEM が無効であることを意味します。                                                                                                |
| TiDB 構成ファイル    | `performance.committer-concurrency`                                                                      | 修正済み     | 単一トランザクションのコミット フェーズにおけるコミット操作に関連する要求の同時実行数を制御します。デフォルト値は`16`から`128`に変更されます。                                                                                                   |
| TiDB 構成ファイル    | [`performance.tcp-no-delay`](/tidb-configuration-file.md#tcp-no-delay)                                   | 新しく追加された | TCPレイヤーで TCP_NODELAY を有効にするかどうかを決定します。デフォルト値は`true`で、TCP_NODELAY が有効であることを意味します。                                                                                               |
| TiDB 構成ファイル    | [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)                                     | 新しく追加された | TiDB がインスタンス レベルで Optimizer のコスト見積を無視し、MPP モードを強制するかどうかを制御します。デフォルト値は`false`です。この構成項目は、システム変数[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。 |
| TiDB 構成ファイル    | [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity)     | 新しく追加された | 単一の TiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルに記録できるデッドロック イベントの最大数を設定します。デフォルト値は`10`です。                               |
| TiKV 設定ファイル    | [`abort-on-panic`](/tikv-configuration-file.md#abort-on-panic)                                           | 新しく追加された | `abort`プロセスが、TiKV パニック時にシステムがコア ダンプ ファイルを生成することを許可するかどうかを設定します。デフォルト値は`false`で、コア ダンプ ファイルの生成は許可されません。                                                                         |
| TiKV 設定ファイル    | [`hibernate-regions`](/tikv-configuration-file.md#hibernate-regions)                                     | 修正済み     | デフォルト値は`false`から`true`に変更されます。リージョンが長時間アイドル状態の場合、自動的に休止状態に設定されます。                                                                                                              |
| TiKV 設定ファイル    | [`old-value-cache-memory-quota`](/tikv-configuration-file.md#old-value-cache-memory-quota)               | 新しく追加された | TiCDC 古い値によるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                                  |
| TiKV 設定ファイル    | [`sink-memory-quota`](/tikv-configuration-file.md#sink-memory-quota)                                     | 新しく追加された | TiCDC データ変更イベントによるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                            |
| TiKV 設定ファイル    | [`incremental-scan-threads`](/tikv-configuration-file.md#incremental-scan-threads)                       | 新しく追加された | 履歴データを増分スキャンするタスクのスレッド数を設定します。デフォルト値は`4`で、タスクに 4 つのスレッドがあることを意味します。                                                                                                            |
| TiKV 設定ファイル    | [`incremental-scan-concurrency`](/tikv-configuration-file.md#incremental-scan-concurrency)               | 新しく追加された | 履歴データを増分スキャンするタスクの最大同時実行数を設定します。デフォルト値は`6`で、最大 6 つのタスクを同時に実行できることを意味します。                                                                                                       |
| TiKV 設定ファイル    | [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 修正済み     | 保留中の圧縮バイトのソフト制限。デフォルト値は`"64GB"`から`"192GB"`に変更されます。                                                                                                                             |
| TiKV 設定ファイル    | [`storage.io-rate-limit`](/tikv-configuration-file.md#storageio-rate-limit)                              | 新しく追加された | TiKV 書き込みの I/O レートを制御します。デフォルト値は`storage.io-rate-limit.max-bytes-per-sec`で、 `"0MB"`です。                                                                                         |
| TiKV 設定ファイル    | [`resolved-ts.enable`](/tikv-configuration-file.md#enable)                                               | 新しく追加された | すべてのリージョンリーダーに対して`resolved-ts`維持するかどうかを決定します。デフォルト値は`true`です。                                                                                                                  |
| TiKV 設定ファイル    | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                     | 新しく追加された | `resolved-ts`が転送される間隔。デフォルト値は`"1s"`です。値は動的に変更できます。                                                                                                                             |
| TiKV 設定ファイル    | [`resolved-ts.scan-lock-pool-size`](/tikv-configuration-file.md#scan-lock-pool-size)                     | 新しく追加された | `resolved-ts`初期化するときに TiKV が MVCC (マルチバージョン同時実行制御) ロック データをスキャンするために使用するスレッドの数。デフォルト値は`2`です。                                                                                   |

### その他 {#others}

-   アップグレード前に、TiDB 構成[`feedback-probability`](https://docs.pingcap.com/tidb/v5.1/tidb-configuration-file#feedback-probability)の値を確認してください。値が 0 でない場合、アップグレード後に「回復可能な goroutine でpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDB の Go コンパイラ バージョンを go1.13.7 から go1.16.4 にアップグレードすると、TiDB のパフォーマンスが向上します。TiDB 開発者の場合は、スムーズなコンパイルを確実に実行できるように Go コンパイラ バージョンをアップグレードしてください。
-   TiDB ローリング アップグレード中に、TiDB Binlog を使用するクラスター内にクラスター化インデックスを持つテーブルを作成しないようにしてください。
-   TiDB ローリング アップグレード中は、 `alter table ... modify column`または`alter table ... change column`のようなステートメントを実行しないでください。
-   v5.1 以降、各テーブルのTiFlashレプリカを構築するときに、システム テーブルのレプリカを設定することはサポートされなくなりました。クラスターをアップグレードする前に、関連するシステム テーブル レプリカをクリアする必要があります。そうしないと、アップグレードは失敗します。
-   TiCDC の`cdc cli changefeed`コマンドの`--sort-dir`パラメータは非推奨です。代わりに、 `cdc server`コマンドで`--sort-dir`設定できます[＃1795](https://github.com/pingcap/tiflow/pull/1795)
-   TiDB 5.1 にアップグレードした後、TiDB が「関数 READ ONLY には noop 実装のみがあります」というエラーを返す場合、 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)の値を`ON`に設定することで、TiDB がこのエラーを無視するようにすることができます。これは、MySQL の`read_only`変数が TiDB でまだ有効になっていないためです (TiDB では「noop」動作です)。したがって、この変数が TiDB で設定されている場合でも、TiDB クラスターにデータを書き込むことができます。

## 新機能 {#new-features}

### 構文 {#sql}

-   MySQL 8.0 の共通テーブル式 (CTE) 機能をサポートします。

    この機能により、TiDB は階層データを再帰的または非再帰的にクエリする機能を強化し、人事、製造、金融市場、教育などの複数の分野でツリー クエリを使用してアプリケーション ロジックを実装するニーズを満たします。

    TiDBでは、共通テーブル式[ユーザードキュメント](/sql-statements/sql-statement-with.md)使用するために`WITH`文を適用できます[＃17472](https://github.com/pingcap/tidb/issues/17472)

-   MySQL 8.0 の動的権限機能をサポートします。

    動的権限は、 `SUPER`権限を制限し、よりきめ細かいアクセス制御のために TiDB に柔軟な権限構成を提供するために使用されます。たとえば、動的権限を使用して、 `BACKUP`と`RESTORE`操作のみを実行できるユーザー アカウントを作成できます。

    サポートされている動的権限は次のとおりです。

    -   `BACKUP_ADMIN`
    -   `RESTORE_ADMIN`
    -   `ROLE_ADMIN`
    -   `CONNECTION_ADMIN`
    -   `SYSTEM_VARIABLES_ADMIN`

    プラグインを使用して新しい権限を追加することもできます。サポートされているすべての権限を確認するには、 `SHOW PRIVILEGES`ステートメントを実行します[ユーザードキュメント](/privilege-management.md)

-   Security強化モード (SEM) の新しい構成項目を追加します。これにより、TiDB 管理者権限がより細かく分割されます。

    Security強化モードはデフォルトで無効になっています。有効にするには、 [ユーザードキュメント](/system-variables.md#tidb_enable_enhanced_security)を参照してください。

-   オンラインでの列タイプ変更機能を強化します`ALTER TABLE`ステートメントを使用したオンラインでの列タイプ変更をサポートします。これには以下が含まれますが、これらに限定されません。

    -   `VARCHAR` `BIGINT`に変更
    -   `DECIMAL`精度の変更
    -   `VARCHAR(10)`の長さを`VARCHAR(5)`に圧縮する

    [ユーザードキュメント](/sql-statements/sql-statement-modify-column.md)

-   指定された時点または指定された時間範囲から履歴データを読み取るために使用される新しい実験的機能であるステイル読み取り を実行するための新しい SQL 構文`AS OF TIMESTAMP`を導入します。

    [ユーザードキュメント](/stale-read.md) , [＃21094](https://github.com/pingcap/tidb/issues/21094)

    `AS OF TIMESTAMP`の例は以下のとおりです。

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

-   新しい統計タイプ`tidb_analyze_version = 2` (Experimental) を導入します。

    デフォルトでは`tidb_analyze_version`は`2`に設定されており、これにより、バージョン 1 でのハッシュ競合によって大量のデータで発生する可能性のある大きなエラーが回避され、ほとんどのシナリオで推定精度が維持されます。

    [ユーザードキュメント](/statistics.md)

### トランザクション {#transaction}

-   ロックビュー機能のサポート（Experimental）

    ロックビュー機能は、ロック競合や悲観的ロックのロック待機に関する詳細情報を提供し、DBA がトランザクションのロック状態を観察し、デッドロックの問題をトラブルシューティングするのに役立ちます[＃24199](https://github.com/pingcap/tidb/issues/24199)

    ユーザードキュメント:

    -   クラスター内のすべての TiKV ノードで現在発生している悲観的ロックとその他のロックをビュー[`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDBノードで最近発生したいくつかのデッドロックエラーをビュー: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDBノードで現在実行されているトランザクション情報をビュー: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### パフォーマンス {#performance}

-   データレプリカの古い読み取り (Experimental)

    ローカルレプリカデータを直接読み取り、読み取りレイテンシーを削減し、クエリパフォーマンスを向上させます。

    [ユーザードキュメント](/stale-read.md) , [＃21094](https://github.com/pingcap/tidb/issues/21094)

-   デフォルトで Hibernate リージョン機能を有効にします。

    リージョンが長時間非アクティブ状態にある場合、自動的にサイレント状態に設定され、LeaderとFollower間のハートビート情報のシステム オーバーヘッドが削減されます。

    [ユーザードキュメント](/tikv-configuration-file.md#hibernate-regions) , [＃10266](https://github.com/tikv/tikv/pull/10266)

### 安定性 {#stability}

-   TiCDCのレプリケーション安定性の問題を解決する

    -   以下のシナリオで OOM を回避するために TiCDC のメモリ使用量を改善します。
    -   レプリケーション中断中に 1TB を超える大量のデータが蓄積されると、再レプリケーションによって OOM 問題が発生します。
    -   大量のデータ書き込みは TiCDC で OOM の問題を引き起こします。
    -   次のシナリオで TiCDC レプリケーションが中断される可能性を減らします。

        [プロジェクト#11](https://github.com/pingcap/tiflow/projects/11)

        -   ネットワークが不安定な場合のレプリケーションの中断
        -   一部の TiKV/PD/TiCDC ノードがダウンした場合のレプリケーションの中断

-   TiFlashstorageメモリ制御

    リージョンスナップショット生成の速度とメモリ使用量を最適化し、OOMの可能性を減らします。

-   TiKV バックグラウンド タスクの書き込みレート リミッターを追加します (TiKV 書き込みレート リミッター)

    読み取りおよび書き込み要求の持続時間の安定性を確保するために、TiKV 書き込みレート リミッターは、GC や圧縮などの TiKV バックグラウンド タスクの書き込みトラフィックを平滑化します。TiKV バックグラウンド タスク書き込みレート リミッターの既定値は「0MB」です。この値は、クラウド ディスクの製造元によって指定された最大 I/O 帯域幅など、ディスクの最適な I/O 帯域幅に設定することをお勧めします。

    [ユーザードキュメント](/tikv-configuration-file.md#storageio-rate-limit) , [＃9156](https://github.com/tikv/tikv/issues/9156)

-   複数のスケーリングタスクが同時に実行される場合のスケジュールの安定性の問題を解決します

### テレメトリー {#telemetry}

TiDB は、実行ステータスや失敗ステータスなど、テレメトリに TiDB クラスター要求の実行ステータスを追加します。

この情報の詳細と、この動作を無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。

## 改善点 {#improvements}

-   ティビ

    -   組み込み関数`VITESS_HASH()` [＃23915](https://github.com/pingcap/tidb/pull/23915)をサポート
    -   `WHERE`節[＃23619](https://github.com/pingcap/tidb/issues/23619)で列挙型を使用する場合のパフォーマンスを向上させるために、列挙型のデータを TiKV にプッシュダウンすることをサポートします。
    -   `RENAME USER`構文[＃23648](https://github.com/pingcap/tidb/issues/23648)サポートする
    -   ROW_NUMBER() [＃23807](https://github.com/pingcap/tidb/issues/23807)を使用してデータをページングする際の TiDB OOM 問題を解決するためにウィンドウ関数の計算を最適化します。
    -   `UNION ALL`使用して多数の`SELECT`文を結合する場合のTiDB OOM問題を解決するために`UNION ALL`の計算を最適化します[＃21441](https://github.com/pingcap/tidb/issues/21441)
    -   パーティションテーブルの動的プルーニングモードを最適化してパフォーマンスと安定性を向上[＃24150](https://github.com/pingcap/tidb/issues/24150)
    -   複数のシナリオで発生する`Region is Unavailable`問題を修正する[プロジェクト#62](https://github.com/pingcap/tidb/projects/62)
    -   頻繁なスケジュール設定で発生する可能性のある複数の`Region is Unavailable`問題を修正
    -   一部の高負荷書き込み状況で発生する可能性のある`Region is Unavailable`問題を修正
    -   キャッシュされた統計が最新である場合は、CPU使用率の上昇を避けるために、 `mysql.stats_histograms`テーブルを頻繁に読み取らないようにします[＃24317](https://github.com/pingcap/tidb/pull/24317)

-   ティクヴ

    -   `zstd`使用してリージョンスナップショットを圧縮し、大量のスケジュールやスケーリングが発生した場合にノード間で大きなスペースの違いが発生するのを防ぎます[＃10005](https://github.com/tikv/tikv/pull/10005)

    -   複数のケースでOOM問題を解決する[＃10183](https://github.com/tikv/tikv/issues/10183)

        -   各モジュールのメモリ使用量追跡を追加する
        -   Raftエントリキャッシュが大きすぎるために発生するOOM問題を解決する
        -   GCタスクのスタックによって発生するOOM問題を解決する
        -   一度にRaftログからメモリに取得するRaftエントリが多すぎるために発生する OOM の問題を解決します。

    -   ホットスポット書き込みがあるときに、リージョンサイズの増加が分割速度を超えるという問題を軽減するために、リージョンをより均等に分割します[＃9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   `Union All` `TopN` `Limit`をサポート
    -   MPP モードで左外部結合と半反結合を含むカルテシアン積をサポート
    -   実行中のDDL文と読み取り操作が相互にブロックされないようにロック操作を最適化します。
    -   TiFlashによる期限切れデータのクリーンアップを最適化
    -   TiFlashstorageレベルで`timestamp`列のクエリフィルターのさらなるフィルタリングをサポート
    -   クラスター内に多数のテーブルがある場合のTiFlashの起動とスケーラビリティの速度を向上
    -   不明なCPUで実行する場合のTiFlashの互換性を向上

-   PD

    -   `scatter region`スケジューラ[＃3602](https://github.com/pingcap/pd/pull/3602)を追加した後の予期しない統計を回避する
    -   スケーリングプロセスにおける複数のスケジュール問題を解決する

        -   レプリカスナップショットの生成プロセスを最適化して、スケーリング中の低速スケジュールの問題を解決します[＃3563](https://github.com/tikv/pd/issues/3563) [＃10059](https://github.com/tikv/tikv/pull/10059) [＃10001](https://github.com/tikv/tikv/pull/10001)
        -   トラフィックの変化によるハートビートの圧力によって発生する低速スケジューリングの問題を解決する[＃3693](https://github.com/tikv/pd/issues/3693) [＃3739](https://github.com/tikv/pd/issues/3739) [＃3728](https://github.com/tikv/pd/issues/3728) [＃3751](https://github.com/tikv/pd/issues/3751)
        -   スケジューリングによる大規模クラスタのスペースの不一致を減らし、大きな圧縮率の不一致によって引き起こされるバースト問題（異種スペースクラスタに類似）を防ぐためにスケジューリング式を最適化する[＃3592](https://github.com/tikv/pd/issues/3592) [＃10005](https://github.com/tikv/tikv/pull/10005)

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマ[＃1143](https://github.com/pingcap/br/pull/1143) [＃1078](https://github.com/pingcap/br/pull/1078)のシステムテーブルのバックアップと復元をサポート
        -   仮想ホストアドレスモード[＃10243](https://github.com/tikv/tikv/pull/10243)に基づくS3互換storageをサポート
        -   メモリ使用量を削減するためにバックアップメタのフォーマットを最適化します[＃1171](https://github.com/pingcap/br/pull/1171)

    -   ティCDC

        -   いくつかのログメッセージの説明をより明確かつ問題の診断に役立つように改善しました[＃1759](https://github.com/pingcap/tiflow/pull/1759)
        -   バックプレッシャー機能をサポートし、TiCDCスキャン速度が下流の処理能力を感知できるようにします[＃10151](https://github.com/tikv/tikv/pull/10151)
        -   TiCDCが初期スキャンを実行する際のメモリ使用量を削減する[＃10133](https://github.com/tikv/tikv/pull/10133)
        -   悲観的トランザクションにおける TiCDC の古い値のキャッシュヒット率を向上させる[＃10089](https://github.com/tikv/tikv/pull/10089)

    -   Dumpling

        -   TiDB v4.0 からデータをエクスポートするロジックを改善し、TiDB がメモリ不足 (OOM) になるのを回避します[＃273](https://github.com/pingcap/dumpling/pull/273)

        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正[＃280](https://github.com/pingcap/dumpling/pull/280)

    -   TiDB Lightning

        -   データのインポート速度を向上します。最適化の結果、TPC-C データのインポート速度が 30% 向上し、インデックス数が多い (5 個) 大規模なテーブル (2TB 以上) のインポート速度が 50% 以上向上しました[＃753](https://github.com/pingcap/br/pull/753)
        -   インポートするデータとインポート前にターゲット クラスターの事前チェックを追加し、インポート要件を満たしていない場合はエラーを報告してインポート プロセスを拒否します[＃999](https://github.com/pingcap/br/pull/999)
        -   ローカルバックエンドでのチェックポイント更新のタイミングを最適化し、ブレークポイント[＃1080](https://github.com/pingcap/br/pull/1080)からの再開のパフォーマンスを向上

## バグ修正 {#bug-fixes}

-   ティビ

    -   投影結果が空の場合にプロジェクト除去の実行結果が間違っている可能性がある問題を修正[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   列に`NULL`値が含まれている場合に間違ったクエリ結果が表示される問題を修正しました[＃23891](https://github.com/pingcap/tidb/issues/23891)
    -   スキャンに仮想列[＃23886](https://github.com/pingcap/tidb/issues/23886)が含まれている場合、MPP プランの生成を禁止します。
    -   プラン キャッシュ[＃23187](https://github.com/pingcap/tidb/issues/23187) [＃23144](https://github.com/pingcap/tidb/issues/23144) [＃23304](https://github.com/pingcap/tidb/issues/23304) [＃23290](https://github.com/pingcap/tidb/issues/23290)での`PointGet`と`TableDual`の誤った再利用を修正
    -   オプティマイザがクラスター化インデックス[＃23906](https://github.com/pingcap/tidb/issues/23906)の`IndexMerge`プランを構築するときに発生するエラーを修正します。
    -   BIT型エラーの型推論を修正[＃23832](https://github.com/pingcap/tidb/issues/23832)
    -   `PointGet`演算子が存在する場合に一部のオプティマイザヒントが有効にならない問題を修正[＃23570](https://github.com/pingcap/tidb/issues/23570)
    -   エラー[＃23893](https://github.com/pingcap/tidb/issues/23893)によりロールバック時にDDL操作が失敗する可能性がある問題を修正
    -   バイナリリテラル定数のインデックス範囲が正しく構築されない問題を修正[＃23672](https://github.com/pingcap/tidb/issues/23672)
    -   いくつかのケースで`IN`節の潜在的な誤った結果を修正[＃23889](https://github.com/pingcap/tidb/issues/23889)
    -   いくつかの文字列関数の誤った結果を修正[＃23759](https://github.com/pingcap/tidb/issues/23759)
    -   ユーザーは、テーブルに対して`REPLACE`操作を実行するために`INSERT`と`DELETE`両方の権限が必要になります[＃23909](https://github.com/pingcap/tidb/issues/23909)
    -   ユーザーは、テーブルに対して`REPLACE`操作を実行するために`INSERT`と`DELETE`両方の権限が必要になります[＃24070](https://github.com/pingcap/tidb/pull/24070)
    -   バイナリとバイトを誤って比較することで発生した間違った`TableDual`プランを修正[＃23846](https://github.com/pingcap/tidb/issues/23846)
    -   一部のケースでプレフィックスインデックスとインデックス結合を使用することで発生するpanic問題を修正[＃24547](https://github.com/pingcap/tidb/issues/24547) [＃24716](https://github.com/pingcap/tidb/issues/24716) [＃24717](https://github.com/pingcap/tidb/issues/24717)
    -   `point get`の準備されたプラン キャッシュがトランザクション[＃24741](https://github.com/pingcap/tidb/issues/24741)の`point get`ステートメントによって誤って使用される問題を修正しました。
    -   照合順序が`ascii_bin`または`latin1_bin`場合に間違ったプレフィックスインデックス値を書き込む問題を修正しました[＃24569](https://github.com/pingcap/tidb/issues/24569)
    -   進行中のトランザクションがGCワーカー[＃24591](https://github.com/pingcap/tidb/issues/24591)によって中断される可能性がある問題を修正
    -   `new-collation`が有効で`new-row-format`が無効の場合、クラスター化インデックスでポイントクエリが間違って実行される可能性があるバグを修正[＃24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフルハッシュ結合[＃24490](https://github.com/pingcap/tidb/pull/24490)のパーティションキーの変換をリファクタリングする
    -   `HAVING`節[＃24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプラン構築時に発生するpanic問題を修正
    -   列プルーニングの改善により、 `Apply`および`Join`演算子の結果が間違ってしまう問題を修正しました[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリロックが解決できないバグを修正[＃24384](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketch レコードの重複を引き起こす可能性のある統計の GC 問題を修正[＃24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的ロックが`ErrKeyExists`エラー[＃23799](https://github.com/pingcap/tidb/issues/23799)を受け取ったときに不必要な悲観的ロールバックを避ける
    -   sql_modeに`ANSI_QUOTES` [＃24429](https://github.com/pingcap/tidb/issues/24429)含まれている場合に数値リテラルが認識されない問題を修正
    -   `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`のようなステートメントは、リストされていないパーティション[＃24746](https://github.com/pingcap/tidb/issues/24746)からデータを読み取ることを禁止します。
    -   SQL文に`GROUP BY`と`UNION`両方が含まれている場合に発生する可能性のある`index out of range`エラーを修正します[＃24281](https://github.com/pingcap/tidb/issues/24281)
    -   `CONCAT`関数が照合順序[＃24296](https://github.com/pingcap/tidb/issues/24296)誤って処理する問題を修正
    -   `collation_server`グローバル変数が新しいセッション[＃24156](https://github.com/pingcap/tidb/pull/24156)で有効にならない問題を修正

-   ティクヴ

    -   コプロセッサが`IN`式[＃9821](https://github.com/tikv/tikv/issues/9821)の符号付きまたは符号なし整数型を適切に処理できない問題を修正
    -   SST ファイルをバッチで取り込んだ後に多くの空の領域が発生する問題を修正[＃964](https://github.com/pingcap/br/issues/964)
    -   ファイル辞書ファイルが破損した後にTiKVが起動できなくなるバグを修正[＃9886](https://github.com/tikv/tikv/issues/9886)
    -   古い値の読み取りによって引き起こされる TiCDC OOM 問題を修正[＃9996](https://github.com/tikv/tikv/issues/9996) [＃9981](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin` [＃24548](https://github.com/pingcap/tidb/issues/24548)場合にクラスター化された主キー列のセカンダリ インデックスに空の値が含まれる問題を修正しました。
    -   `abort-on-panic`設定を追加すると、panicが発生したときに TiKV がコアダンプファイルを生成できるようになります。ユーザーは、コアダンプ[＃10216](https://github.com/tikv/tikv/pull/10216)を有効にするために環境を正しく設定する必要があります。
    -   TiKVがビジーでないときに発生する`point get`クエリのパフォーマンス低下の問題を修正しました[＃10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合にPDLeaderの再選出が遅くなる問題を修正[＃3697](https://github.com/tikv/pd/issues/3697)

    -   存在しないストア[＃3660](https://github.com/tikv/pd/issues/3660)からエビクト リーダー スケジューラを削除するときに発生するpanic問題を修正しました。

    -   オフラインピアがマージされた後に統計が更新されない問題を修正[＃3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   時間型を整数型にキャストしたときに誤った結果が返される問題を修正しました
    -   10秒以内に対応する`receiver`が見つからないバグを修正
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性がある問題を修正
    -   `bitwise`演算子の動作がTiDBと異なるバグを修正
    -   `prefix key`使用時に範囲が重複することで発生するアラート問題を修正
    -   文字列型を整数型にキャストしたときに誤った結果が返される問題を修正しました
    -   連続した高速書き込みによりTiFlash のメモリが不足する問題を修正
    -   テーブルGC中にヌルポインタの例外が発生する可能性がある問題を修正しました。
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正しました
    -   BR復元中にTiFlash がpanicになる可能性がある問題を修正
    -   共有デルタインデックスを同時に複製するときに誤った結果が返される問題を修正
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるpanicを修正
    -   TiFlash が非同期コミットからフォールバックしたロックを解決できない問題を修正
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれている場合に誤った結果が返される問題を修正しました
    -   セグメント分割中に発生するTiFlashpanic問題を修正

-   ツール

    -   TiDB Lightning

        -   KVデータ[＃1127](https://github.com/pingcap/br/pull/1127)を生成する際に発生するTiDB Lightningpanicの問題を修正
        -   データインポート中に合計キーサイズがラフトエントリ制限を超えたためにバッチ分割リージョンが失敗するバグを修正[＃969](https://github.com/pingcap/br/issues/969)
        -   CSVファイルをインポートする際に、ファイルの最後の行に改行文字が含まれていない場合（ `\r\n` ）、エラーが報告される問題を修正しました[＃1133](https://github.com/pingcap/br/issues/1133)
        -   インポートするテーブルにdouble型の自動増分列が含まれている場合、auto_increment値が異常になる問題を修正[＃1178](https://github.com/pingcap/br/pull/1178)

    -   バックアップと復元 (BR)
        -   いくつかの TiKV ノードの障害によりバックアップが中断される問題を修正[＃980](https://github.com/pingcap/br/issues/980)

    -   ティCDC

        -   Unified Sorter の同時実行の問題を修正し、役に立たないエラー メッセージをフィルタリングする[＃1678](https://github.com/pingcap/tiflow/pull/1678)
        -   冗長ディレクトリの作成により MinIO [＃1463](https://github.com/pingcap/tiflow/issues/1463)でのレプリケーションが中断される可能性があるバグを修正
        -   `explicit_defaults_for_timestamp`セッション変数のデフォルト値をONに設定して、 MySQL 5.7ダウンストリームがアップストリームTiDB [＃1585](https://github.com/pingcap/tiflow/issues/1585)と同じ動作を維持するようにします。
        -   `io.EOF`の誤った処理によりレプリケーションが中断される可能性がある問題を修正[＃1633](https://github.com/pingcap/tiflow/issues/1633)
        -   TiCDCダッシュボード[＃1645](https://github.com/pingcap/tiflow/pull/1645)のTiKV CDCエンドポイントCPUメトリックを修正する
        -   場合によってはレプリケーションのブロックを回避するために`defaultBufferChanSize`増やす[＃1259](https://github.com/pingcap/tiflow/issues/1259)
        -   Avro出力[＃1712](https://github.com/pingcap/tiflow/pull/1712)でタイムゾーン情報が失われる問題を修正
        -   Unified Sorter 内の古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリ[＃1742](https://github.com/pingcap/tiflow/pull/1742)の共有を禁止します。
        -   古いリージョンが多数存在する場合に発生する KV クライアントのデッドロック バグを修正[＃1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[＃1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正
        -   MySQL [＃1750](https://github.com/pingcap/tiflow/pull/1750)にデータを複製する際にSUPER権限を必要とする`explicit_defaults_for_timestamp`の更新を元に戻す
        -   メモリオーバーフローのリスクを軽減するためにシンクフロー制御をサポートする[＃1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブル[＃1828](https://github.com/pingcap/tiflow/pull/1828)を移動するときにレプリケーション タスクが停止する可能性があるバグを修正しました。
        -   TiCDC チェンジフィード チェックポイント[＃1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により TiKV GC セーフ ポイントがブロックされる問題を修正しました。
