---
title: TiDB 5.1 Release Notes
summary: TiDB 5.1では、共通テーブル式（CTE）、動的権限機能、およびステイル読み取りのサポートが導入されました。また、新しい統計タイプ、Lock ビュー機能、およびTiKV書き込みレートリミッターも含まれています。互換性に関する変更点として、新しいシステム変数と構成変数が追加されました。その他、様々な改善点やバグ修正も今回のリリースに含まれています。
---

# TiDB 5.1 リリースノート {#tidb-5-1-release-notes}

発売日：2021年6月24日

TiDB バージョン: 5.1.0

バージョン5.1における主な新機能または改善点は以下のとおりです。

-   SQL文の可読性と実行効率を向上させるため、MySQL 8.0の共通テーブル式（CTE）機能をサポートします。
-   コード開発の柔軟性を向上させるため、列の型をオンラインで変更できる機能をサポートする。
-   クエリの安定性を向上させるための新しい統計タイプを導入しました。これは実験的機能としてデフォルトで有効になっています。
-   MySQL 8.0の動的権限機能をサポートし、特定の操作に対するよりきめ細かな制御を実現します。
-   読み取りレイテンシーを削減し、クエリパフォーマンスを向上させるために、 ステイル読み取り機能を使用してローカルレプリカから直接データを読み取ることをサポートします（Experimental）。
-   データベース管理者（DBA）がトランザクションのロックイベントを監視し、デッドロックの問題をトラブルシューティングしやすくするために、ロックビュー機能を追加します（Experimental）。
-   バックグラウンドタスクにTiKV書き込みレートリミッターを追加し、読み取りおよび書き込みリクエストのレイテンシーが安定するようにします。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.1 にアップグレードする場合、中間バージョンの互換性変更点を確認したい場合は、該当バージョンの[リリースノート](/releases/_index.md)を参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                      | 種類を変更する  | 説明                                                                                                                            |
| :--------------------------------------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------- |
| [`cte_max_recursion_depth`](/system-variables.md#cte_max_recursion_depth)                | 新しく追加された | 共通テーブル式における最大再帰深度を制御します。                                                                                                      |
| [`init_connect`](/system-variables.md#init_connect)                                      | 新しく追加された | TiDBサーバーへの初期接続を制御します。                                                                                                         |
| [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)          | 新しく追加された | TiDBが統計情報を収集する方法を制御します。この変数のデフォルト値は`2`です。これは実験的機能です。                                                                          |
| [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)    | 新しく追加された | 接続先のTiDBサーバーでセキュリティ強化モード（SEM）が有効になっているかどうかを示します。この変数設定は、TiDBサーバーを再起動しないと変更できません。                                            |
| [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)                   | 新しく追加された | オプティマイザのコスト見積もりを無視し、クエリ実行に強制的に MPP モードを使用するかどうかを制御します。この変数のデータ型は`BOOL`で、デフォルト値は`false`です。                                     |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | 新しく追加された | パーティションテーブルの動的プルーニングモードを有効にするかどうかを指定します。この機能は実験的です。この変数のデフォルト値は`static`であり、これはパーティションテーブルの動的プルーニングモードがデフォルトで無効になっていることを意味します。 |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションアイテム                                                                                           | 種類を変更する  | 説明                                                                                                                                                                           |
| :------------- | :------------------------------------------------------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB設定ファイル     | [`security.enable-sem`](/tidb-configuration-file.md#enable-sem)                                          | 新しく追加された | セキュリティ強化モード（SEM）を有効にするかどうかを制御します。この設定項目のデフォルト値は`false`で、これはSEMが無効になっていることを意味します。                                                                                           |
| TiDB設定ファイル     | `performance.committer-concurrency`                                                                      | 修正済み     | 単一トランザクションのコミットフェーズにおけるコミット操作に関連するリクエストの同時実行数を制御します。デフォルト値は`16`から`128`に変更されます。                                                                                               |
| TiDB設定ファイル     | [`performance.tcp-no-delay`](/tidb-configuration-file.md#tcp-no-delay)                                   | 新しく追加された | TCPレイヤーで TCP_NODELAY を有効にするかどうかを決定します。デフォルト値は`true`で、これは TCP_NODELAY が有効になっていることを意味します。                                                                                      |
| TiDB設定ファイル     | [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)                                     | 新しく追加された | TiDB がインスタンス レベルでオプティマイザのコスト見積もりを無視し、MPP モードを強制するかどうかを制御します。デフォルト値は`false`です。この設定項目は、システム変数[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。 |
| TiDB設定ファイル     | [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity)     | 新しく追加された | 単一の TiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルに記録できるデッドロック イベントの最大数を設定します。デフォルト値は`10`です。                             |
| TiKV設定ファイル     | [`abort-on-panic`](/tikv-configuration-file.md#abort-on-panic)                                           | 新しく追加された | TiKVがパニックを起こした際に、 `abort`プロセスがコアダンプファイルの生成を許可するかどうかを設定します。デフォルト値は`false`で、これはコアダンプファイルの生成が許可されないことを意味します。                                                                    |
| TiKV設定ファイル     | [`hibernate-regions`](/tikv-configuration-file.md#hibernate-regions)                                     | 修正済み     | デフォルト値が`false`から`true`に変更されます。リージョンが長時間アイドル状態になると、自動的に休止状態に設定されます。                                                                                                           |
| TiKV設定ファイル     | [`old-value-cache-memory-quota`](/tikv-configuration-file.md#old-value-cache-memory-quota)               | 新しく追加された | TiCDCの古い値に基づいてメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                              |
| TiKV設定ファイル     | [`sink-memory-quota`](/tikv-configuration-file.md#sink-memory-quota)                                     | 新しく追加された | TiCDCデータ変更イベントによるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                           |
| TiKV設定ファイル     | [`incremental-scan-threads`](/tikv-configuration-file.md#incremental-scan-threads)                       | 新しく追加された | 履歴データを増分的にスキャンするタスクのスレッド数を設定します。デフォルト値は`4`で、これはタスクに4つのスレッドが使用されることを意味します。                                                                                                    |
| TiKV設定ファイル     | [`incremental-scan-concurrency`](/tikv-configuration-file.md#incremental-scan-concurrency)               | 新しく追加された | 履歴データの増分スキャンを行うタスクの同時実行の最大数を設定します。デフォルト値は`6`で、これは最大で 6 つのタスクを同時に実行できることを意味します。                                                                                               |
| TiKV設定ファイル     | [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 修正済み     | 保留中の圧縮バイトのソフトリミット。デフォルト値は`"64GB"`から`"192GB"`に変更されます。                                                                                                                         |
| TiKV設定ファイル     | [`storage.io-rate-limit`](/tikv-configuration-file.md#storageio-rate-limit)                              | 新しく追加された | TiKV書き込みのI/Oレートを制御します。 `storage.io-rate-limit.max-bytes-per-sec`のデフォルト値は`"0MB"`です。                                                                                           |
| TiKV設定ファイル     | [`resolved-ts.enable`](/tikv-configuration-file.md#enable)                                               | 新しく追加された | すべてのリージョンリーダーに対して`resolved-ts`を維持するかどうかを決定します。デフォルト値は`true`です。                                                                                                               |
| TiKV設定ファイル     | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                     | 新しく追加された | `resolved-ts`が転送される間隔。デフォルト値は`"1s"`です。この値は動的に変更できます。                                                                                                                         |
| TiKV設定ファイル     | [`resolved-ts.scan-lock-pool-size`](/tikv-configuration-file.md#scan-lock-pool-size)                     | 新しく追加された | `resolved-ts`を初期化する際に TiKV が MVCC (マルチバージョン同時実行制御) ロックデータをスキャンするために使用するスレッドの数。デフォルト値は`2`です。                                                                                  |

### その他 {#others}

-   アップグレード前に、TiDB構成の[`feedback-probability`](https://docs-archive.pingcap.com/tidb/v5.1/tidb-configuration-file#feedback-probability)の値を確認してください。値が0でない場合、アップグレード後に「回復可能なゴルーチンでpanicが発生しました」というエラーが発生しますが、このエラーはアップグレード自体には影響しません。
-   TiDBのパフォーマンスを向上させるため、TiDBのGoコンパイラバージョンをgo1.13.7からgo1.16.4にアップグレードしてください。TiDB開発者の方は、スムーズなコンパイルを保証するために、Goコンパイラバージョンをアップグレードすることをお勧めします。
-   TiDBローリングアップグレード中は、TiDB Binlogを使用するクラスタでクラスター化インデックスを持つテーブルを作成しないようにしてください。
-   TiDB のローリングアップグレード中は`alter table ... modify column`や`alter table ... change column`のようなステートメントを実行しないでください。
-   バージョン5.1以降、各テーブルのTiFlashレプリカを作成する際に、システムテーブルのレプリカを設定する機能はサポートされなくなりました。クラスタをアップグレードする前に、関連するシステムテーブルのレプリカをクリアする必要があります。クリアしないと、アップグレードは失敗します。
-   TiCDC の`--sort-dir`コマンドの`cdc cli changefeed`パラメータは非推奨です。代わりに、 `--sort-dir`コマンドで`cdc server` } を設定できます。 [#1795](https://github.com/pingcap/tiflow/pull/1795)
-   TiDB 5.1 にアップグレードした後、TiDB が「関数 READ ONLY には noop 実装しかありません」というエラーを返す場合、 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)の値を`ON`に設定することで、TiDB がこのエラーを無視するようにできます。これは、MySQL の`read_only`変数が TiDB ではまだ有効になっていないためです (TiDB では「noop」動作です)。したがって、この変数が TiDB で設定されていても、TiDB クラスタにデータを書き込むことができます。

## 新機能 {#new-features}

### SQL {#sql}

-   MySQL 8.0の共通テーブル式（CTE）機能をサポートします。

    この機能により、TiDBは階層型データを再帰的または非再帰的にクエリする機能を備え、人事、製造、金融市場、教育など、複数の分野におけるアプリケーションロジックの実装にツリークエリを使用するニーズを満たします。

    TiDB では、 `WITH`ステートメントを適用して共通テーブル式を使用できます。[ユーザー向けドキュメント](/sql-statements/sql-statement-with.md)、 [#17472](https://github.com/pingcap/tidb/issues/17472)

-   MySQL 8.0の動的権限機能をサポートします。

    動的権限は、 `SUPER`権限を制限し、TiDBに、よりきめ細かなアクセス制御のための柔軟な権限構成を提供するために使用されます。たとえば、動的権限を使用して、 `BACKUP`および`RESTORE`操作のみを実行できるユーザーアカウントを作成できます。

    サポートされている動的権限は以下のとおりです。

    -   `BACKUP_ADMIN`
    -   `RESTORE_ADMIN`
    -   `ROLE_ADMIN`
    -   `CONNECTION_ADMIN`
    -   `SYSTEM_VARIABLES_ADMIN`

    プラグインを使用して新しい権限を追加することもできます。サポートされているすべての権限を確認するには、 `SHOW PRIVILEGES`ステートメントを実行します。[ユーザー向けドキュメント](/privilege-management.md)

-   セキュリティ強化モード（SEM）用の新しい設定項目を追加します。これにより、TiDB管理者の権限をより細かく分割できます。

    セキュリティ強化モードはデフォルトでは無効になっています。これを有効にするには、 [ユーザー向けドキュメント](/system-variables.md#tidb_enable_enhanced_security)を参照してください。

-   列タイプのオンライン変更機能を強化します。 `ALTER TABLE`ステートメントを使用した列タイプのオンライン変更をサポートします。これには以下が含まれますが、これらに限定されません。

    -   `VARCHAR`を`BIGINT`に変更します。
    -   `DECIMAL`の精度を変更する
    -   `VARCHAR(10)`の長さを`VARCHAR(5)`に圧縮します

    [ユーザー向けドキュメント](/sql-statements/sql-statement-modify-column.md)

-   指定された時点または指定された期間の履歴データを読み取るための新しい実験的機能である「ステイル読み取り」を実行するための新しい SQL 構文`AS OF TIMESTAMP`導入します。

    [ユーザー向けドキュメント](/stale-read.md)、 [#21094](https://github.com/pingcap/tidb/issues/21094)

    `AS OF TIMESTAMP`の例は以下のとおりです。

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

-   新しい統計タイプ`tidb_analyze_version = 2` (Experimental) を導入します。

    `tidb_analyze_version`はデフォルトで`2`に設定されており、バージョン 1 でハッシュの競合によって発生する可能性のある大きなデータ量のエラーを回避し、ほとんどのシナリオで推定精度を維持します。

    [ユーザー向けドキュメント](/statistics.md)

### トランザクション {#transaction}

-   ロックビュー機能のサポート（Experimental）

    ロックビュー機能は、悲観的ロックのロック競合とロック待機に関する詳細情報を提供し、DBAがトランザクションのロック状態を監視し、デッドロックの問題をトラブルシューティングするのに役立ちます。 [#24199](https://github.com/pingcap/tidb/issues/24199)

    ユーザー向けドキュメント：

    -   クラスター内のすべての TiKV ノードで現在発生している悲観的ロックおよびその他のロックを確認する: [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDBノードで最近発生した複数のデッドロックエラーを確認する： [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDBノードで現在実行されているトランザクション情報を確認する： [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### パフォーマンス {#performance}

-   データレプリカの古い読み取り（Experimental）

    ローカルレプリカのデータを直接読み込むことで、読み取りレイテンシーを削減し、クエリパフォーマンスを向上させます。

    [ユーザー向けドキュメント](/stale-read.md)、 [#21094](https://github.com/pingcap/tidb/issues/21094)

-   Hibernateリージョン機能をデフォルトで有効にします。

    リージョンが長時間非アクティブ状態にある場合、自動的にサイレント状態に設定され、LeaderとFollower間のハートビート情報のシステムオーバーヘッドが削減されます。

    [ユーザー向けドキュメント](/tikv-configuration-file.md#hibernate-regions)、 [#10266](https://github.com/tikv/tikv/pull/10266)

### 安定性 {#stability}

-   TiCDCのレプリケーション安定性の問題を解決する

    -   以下のシナリオでメモリ不足（OOM）を回避するために、TiCDCのメモリ使用量を改善します。
    -   レプリケーションの中断中に大量のデータが蓄積され、1TBを超えると、再レプリケーションによってメモリ不足（OOM）の問題が発生します。
    -   TiCDCでは、大量のデータ書き込みによってメモリ不足（OOM）の問題が発生します。
    -   以下のシナリオでは、TiCDCレプリケーションの中断の可能性を低減してください。

        [プロジェクト#11](https://github.com/pingcap/tiflow/projects/11)

        -   ネットワークが不安定な場合のレプリケーションの中断
        -   TiKV/PD/TiCDCノードの一部がダウンした場合のレプリケーションの中断

-   TiFlashstorageメモリ制御

    リージョンスナップショット生成の速度とメモリ使用量を最適化し、メモリ不足（OOM）の可能性を低減します。

-   TiKVバックグラウンドタスク用の書き込みレート制限機能を追加する（TiKV書き込みレート制限機能）

    読み取りおよび書き込み要求の継続時間の安定性を確保するため、TiKV 書き込みレートリミッターは、GC や圧縮などの TiKV バックグラウンドタスクの書き込みトラフィックを平滑化します。TiKV バックグラウンドタスク書き込みレートリミッターのデフォルト値は「0MB」です。この値は、クラウドディスクメーカーが指定する最大 I/O 帯域幅など、ディスクの最適な I/O 帯域幅に設定することをお勧めします。

    [ユーザー向けドキュメント](/tikv-configuration-file.md#storageio-rate-limit)、 [#9156](https://github.com/tikv/tikv/issues/9156)

-   複数のスケーリングタスクが同時に実行される際のスケジューリングの安定性の問題を解決する

### テレメトリー {#telemetry}

TiDBは、実行ステータスと失敗ステータスを含む、TiDBクラスタリクエストの実行ステータスをテレメトリに追加します。

この情報の詳細と、この動作を無効にする方法については、[テレメトリー](/telemetry.md)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   組み込み関数`VITESS_HASH()`をサポートする [#23915](https://github.com/pingcap/tidb/pull/23915)
    -   `WHERE`句で列挙型を使用する際のパフォーマンス向上のため、列挙型のデータを TiKV にプッシュダウンする機能をサポートする [#23619](https://github.com/pingcap/tidb/issues/23619)
    -   `RENAME USER`構文をサポート [#23648](https://github.com/pingcap/tidb/issues/23648)
    -   ROW_NUMBER() でデータをページングする際の TiDB の OOM 問題を解決するために、ウィンドウ関数の計算を最適化します [#23807](https://github.com/pingcap/tidb/issues/23807)
    -   `UNION ALL`の計算を最適化し、 `UNION ALL`を使用して多数の`SELECT`ステートメントを結合する際に発生する TiDB OOM 問題を解決します [#21441](https://github.com/pingcap/tidb/issues/21441)
    -   パーティションテーブルの動的プルーニングモードを最適化して、パフォーマンスと安定性を向上させる [#24150](https://github.com/pingcap/tidb/issues/24150)
    -   複数のシナリオで発生する`Region is Unavailable`の問題を修正[プロジェクト#62](https://github.com/pingcap/tidb/projects/62)
    -   頻繁にスケジュール設定を行う状況で発生する可能性のある複数の`Region is Unavailable`問題を修正します。
    -   一部の高負荷書き込み状況で発生する可能性のある`Region is Unavailable`問題を修正します。
    -   キャッシュされた統計情報が最新の場合は、CPU使用率が高くなるのを避けるため、 `mysql.stats_histograms`テーブルを頻繁に読み込まないようにしてください [#24317](https://github.com/pingcap/tidb/pull/24317)

-   TiKV

    -   `zstd`を使用してリージョンスナップショットを圧縮し、負荷の高いスケジューリングやスケーリングの場合にノード間の大きなスペース差を防ぎます [#10005](https://github.com/tikv/tikv/pull/10005)

    -   複数のケースでOOM問題を解決する [#10183](https://github.com/tikv/tikv/issues/10183)

        -   各モジュールのメモリ使用量追跡機能を追加する
        -   Raftエントリキャッシュのサイズが大きすぎるために発生するOOM問題を解決します
        -   スタックされたGCタスクによって引き起こされるOOM問題を解決します
        -   Raftログから一度にメモリに読み込まれるRaftエントリが多すぎるために発生するOOM問題を解決します。

    -   ホットスポット書き込み時にリージョンサイズの増加が分割速度を超える問題を軽減するために、リージョンをより均等に分割する [#9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   `Union All` 、 `TopN` 、および`Limit`関数をサポートします。
    -   MPPモードでの左外部結合およびセミアンチ結合を含むデカルト積をサポートします。
    -   ロック操作を最適化して、実行中の DDL ステートメントと読み取り操作が互いにブロックされないようにする。
    -   TiFlashによる期限切れデータのクリーンアップを最適化
    -   TiFlashstorageレベルで`timestamp`列に対するクエリフィルタのさらなるフィルタリングをサポートします。
    -   クラスタ内に多数のテーブルが存在する場合のTiFlashの起動速度と拡張性を向上させる
    -   未知のCPU上で動作する際のTiFlashの互換性を向上させる

-   PD

    -   `scatter region`スケジューラ [#3602](https://github.com/pingcap/pd/pull/3602)を追加した後、予期しない統計情報を回避する
    -   スケーリングプロセスにおける複数のスケジューリング問題を解決する

        -   レプリカスナップショットの生成プロセスを最適化し、スケーリング時のスケジューリングの遅延問題を解決します[#3563](https://github.com/tikv/pd/issues/3563) [#10059](https://github.com/tikv/tikv/pull/10059) [#10001](https://github.com/tikv/tikv/pull/10001)
        -   トラフィックの変化によるハートビートのプレッシャーが原因で発生するスケジューリングの遅延問題を解決します[#3693](https://github.com/tikv/pd/issues/3693) [#3739](https://github.com/tikv/pd/issues/3739) [#3728](https://github.com/tikv/pd/issues/3728) [#3751](https://github.com/tikv/pd/issues/3751)
        -   スケジューリングによる大規模クラスタの空間不一致を低減し、大きな圧縮率の不一致によって引き起こされるバースト問題（異種空間クラスタと同様）を防止するためにスケジューリング式を最適化する[#3592](https://github.com/tikv/pd/issues/3592) [#10005](https://github.com/tikv/tikv/pull/10005)

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマにおけるシステムテーブルのバックアップと復元をサポートする[#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)
        -   仮想ホストアドレス指定モードに基づくS3互換ストレージをサポートする [#10243](https://github.com/tikv/tikv/pull/10243)
        -   バックアップメタデータのフォーマットを最適化してメモリ使用量を削減する [#1171](https://github.com/pingcap/br/pull/1171)

    -   TiCDC

        -   ログメッセージの説明をより明確かつ問題診断に役立つように改善する [#1759](https://github.com/pingcap/tiflow/pull/1759)
        -   TiCDCのスキャン速度が下流の処理能力を感知できるように、バックプレッシャー機能をサポートする [#10151](https://github.com/tikv/tikv/pull/10151)
        -   TiCDCが初期スキャンを実行する際のメモリ使用量を削減する [#10133](https://github.com/tikv/tikv/pull/10133)
        -   悲観的トランザクションにおける TiCDC 旧値のキャッシュヒット率を改善する [#10089](https://github.com/tikv/tikv/pull/10089)

    -   Dumpling

        -   TiDB v4.0からのデータエクスポートのロジックを改善し、TiDBがメモリ不足（OOM）になるのを回避する [#273](https://github.com/pingcap/dumpling/pull/273)

        -   バックアップ操作が失敗した際にエラーが出力されない問題を修正 [#280](https://github.com/pingcap/dumpling/pull/280)

    -   TiDB Lightning

        -   データインポート速度の向上。最適化の結果、TPC-Cデータのインポート速度が30%向上し、インデックス数が多い（5インデックス）大規模テーブル（2TB以上）のインポート速度が50%以上向上しました。 [#753](https://github.com/pingcap/br/pull/753)
        -   インポート前に、インポート対象データとターゲットクラスタの両方に対して事前チェックを追加し、インポート要件を満たしていない場合はエラーを報告してインポートプロセスを拒否する [#999](https://github.com/pingcap/br/pull/999)
        -   ローカルバックエンドでのチェックポイント更新のタイミングを最適化し、ブレークポイントからの再開パフォーマンスを向上させる [#1080](https://github.com/pingcap/br/pull/1080)

## バグ修正 {#bug-fixes}

-   TiDB

    -   投影結果が空の場合に、プロジェクト消去の実行結果が誤っている可能性がある問題を修正しました [#23887](https://github.com/pingcap/tidb/issues/23887)
    -   列に`NULL`値が含まれている場合に、クエリ結果が間違っている問題を修正しました [#23891](https://github.com/pingcap/tidb/issues/23891)
    -   スキャンに仮想列が含まれている場合、MPPプランの生成を禁止する [#23886](https://github.com/pingcap/tidb/issues/23886)
    -   プランキャッシュにおける`PointGet`と`TableDual`の誤った再利用を修正[#23187](https://github.com/pingcap/tidb/issues/23187) [#23144](https://github.com/pingcap/tidb/issues/23144) [#23304](https://github.com/pingcap/tidb/issues/23304) [#23290](https://github.com/pingcap/tidb/issues/23290)
    -   クラスター化インデックスの`IndexMerge`プランを作成する際に発生するエラーを修正します [#23906](https://github.com/pingcap/tidb/issues/23906)
    -   BIT型エラーの型推論を修正 [#23832](https://github.com/pingcap/tidb/issues/23832)
    -   `PointGet`演算子が存在する場合に、一部のオプティマイザヒントが有効にならない問題を修正しました [#23570](https://github.com/pingcap/tidb/issues/23570)
    -   エラー [#23893](https://github.com/pingcap/tidb/issues/23893)によりロールバック時にDDL操作が失敗する可能性がある問題を修正しました。
    -   バイナリリテラル定数のインデックス範囲が正しく構築されていない問題を修正しました [#23672](https://github.com/pingcap/tidb/issues/23672)
    -   `IN`句が場合によっては誤った結果をもたらす可能性がある問題を修正 [#23889](https://github.com/pingcap/tidb/issues/23889)
    -   一部の文字列関数の誤った結果を修正 [#23759](https://github.com/pingcap/tidb/issues/23759)
    -   ユーザーが`INSERT`操作を実行するには、テーブルに対する`DELETE`権限と`REPLACE`権限の両方が必要になりました [#23909](https://github.com/pingcap/tidb/issues/23909)
    -   ユーザーが`INSERT`操作を実行するには、テーブルに対する`DELETE`権限と`REPLACE`権限の両方が必要になりました [#24070](https://github.com/pingcap/tidb/pull/24070)
    -   バイナリとバイトの比較ミスによって発生した誤った`TableDual`プランを修正 [#23846](https://github.com/pingcap/tidb/issues/23846)
    -   プレフィックスインデックスとインデックス結合の使用によって発生するpanic問題を修正[#24547](https://github.com/pingcap/tidb/issues/24547) [#24716](https://github.com/pingcap/tidb/issues/24716) [#24717](https://github.com/pingcap/tidb/issues/24717)
    -   トランザクション [#24741](https://github.com/pingcap/tidb/issues/24741)において、 `point get`ステートメントが`point get`の準備済みプランキャッシュを誤って使用する問題を修正します。
    -   照合順序が`ascii_bin`または`latin1_bin`の場合に、誤ったプレフィックスインデックス値が書き込まれる問題を修正しました [#24569](https://github.com/pingcap/tidb/issues/24569)
    -   進行中のトランザクションがGCワーカーによって中断される可能性がある問題を修正しました [#24591](https://github.com/pingcap/tidb/issues/24591)
    -   `new-collation`が有効で`new-row-format`が無効になっている場合に、クラスター化インデックスでポイントクエリが正しく実行されない可能性があるバグを修正しました [#24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフルハッシュ結合のためのパーティションキーの変換をリファクタリングする [#24490](https://github.com/pingcap/tidb/pull/24490)
    -   `HAVING`句を含むクエリのプランを作成する際に発生するpanic問題を修正します [#24045](https://github.com/pingcap/tidb/issues/24045)
    -   列剪定の改善により、 `Apply`および`Join`演算子の結果が不正になる問題を修正します [#23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリロックが解決できないバグを修正 [#24384](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketch レコードの重複を引き起こす可能性のある統計情報の GC 問題を修正しました [#24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的ロックが`ErrKeyExists`エラー [#23799](https://github.com/pingcap/tidb/issues/23799)を受け取った場合、不要な悲観的ロールバックを回避する
    -   sql_modeに`ANSI_QUOTES`が含まれている場合に数値リテラルが認識されない問題を修正しました [#24429](https://github.com/pingcap/tidb/issues/24429)
    -   `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`のようなステートメントがリストにないパーティションからデータを読み取ることを禁止する [#24746](https://github.com/pingcap/tidb/issues/24746)
    -   SQL文に`index out of range`と`GROUP BY`両方が含まれている場合に発生する可能性のある`UNION`エラーを修正し [#24281](https://github.com/pingcap/tidb/issues/24281)
    -   `CONCAT`関数が照合順序を正しく処理しない問題を修正しました [#24296](https://github.com/pingcap/tidb/issues/24296)
    -   `collation_server`グローバル変数が新しいセッションで有効にならない問題を修正しました [#24156](https://github.com/pingcap/tidb/pull/24156)

-   TiKV

    -   コプロセッサが`IN`式内の符号付きまたは符号なし整数型を正しく処理できない問題を修正します [#9821](https://github.com/tikv/tikv/issues/9821)
    -   SSTファイルをバッチ処理で取り込んだ後に、多数のリージョンが空になる問題を修正しました [#964](https://github.com/pingcap/br/issues/964)
    -   ファイル辞書ファイルが破損した後にTiKVが起動できないバグを修正しました [#9886](https://github.com/tikv/tikv/issues/9886)
    -   古い値の読み取りによって発生する TiCDC の OOM 問題を修正[#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin`の場合に、クラスター化された主キー列のセカンダリ インデックスに空の値が含まれる問題を修正します [#24548](https://github.com/pingcap/tidb/issues/24548)
    -   TiKVがpanic発生時にコアダンプファイルを生成できるようにする`abort-on-panic`設定を追加します。ユーザーはコアダンプを有効にするために環境を正しく構成する必要があります [#10216](https://github.com/tikv/tikv/pull/10216)
    -   TiKVがビジー状態でない場合に発生する`point get`クエリのパフォーマンス低下問題を修正 [#10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合にPDLeaderの再選が遅くなる問題を修正しました [#3697](https://github.com/tikv/pd/issues/3697)

    -   存在しないストアから退去リーダースケジューラを削除する際に発生するpanic問題を修正 [#3660](https://github.com/tikv/pd/issues/3660)

    -   オフラインピアがマージされた後に統計情報が更新されない問題を修正 [#3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   時間型を整数型にキャストした際に、結果が正しくない問題を修正しました。
    -   `receiver`が10秒以内に対応するタスクを見つけられないバグを修正しました。
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性がある問題を修正します。
    -   `bitwise`演算子の動作がTiDBの動作と異なるバグを修正しました。
    -   `prefix key`を使用する際に範囲が重複することによって発生するアラートの問題を修正します。
    -   文字列型を整数型にキャストした際に、結果が正しくない問題を修正しました。
    -   連続して高速な書き込みを行うと、 TiFlashのメモリが不足する可能性がある問題を修正しました。
    -   テーブルGC中にヌルポインタ例外が発生する可能性がある問題を修正しました。
    -   削除されたテーブルにデータを書き込む際に発生するTiFlashpanic問題を修正します。
    -   TiFlashがBR復元中にpanic可能性がある問題を修正しました。
    -   共有デルタインデックスを同時クローンする際に結果が正しくない問題を修正しました。
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるpanicを修正します。
    -   TiFlashが非同期コミットからフォールバックしたロックを解決できない問題を修正します。
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれている場合に、誤った結果が返される問題を修正しました。
    -   セグメント分割中に発生するTiFlashpanic問題を修正します

-   ツール

    -   TiDB Lightning

        -   KVデータ生成時に発生するTiDB Lightningpanicの問題を修正 [#1127](https://github.com/pingcap/br/pull/1127)
        -   データインポート中にキーの合計サイズがラフトエントリの制限を超えたためにバッチ分割リージョンが失敗するバグを修正しました [#969](https://github.com/pingcap/br/issues/969)
        -   CSVファイルをインポートする際に、ファイルの最終行に改行文字（ `\r\n` ）が含まれていない場合にエラーが発生する問題を修正しました [#1133](https://github.com/pingcap/br/issues/1133)
        -   インポートするテーブルにdouble型のAUTO_INCREMENT列が含まれている場合、auto_incrementの値が異常になる問題を修正しました [#1178](https://github.com/pingcap/br/pull/1178)

    -   バックアップと復元 (BR)
        -   一部のTiKVノードの障害によって発生するバックアップ中断の問題を修正しました [#980](https://github.com/pingcap/br/issues/980)

    -   TiCDC

        -   Unified Sorter の同時実行性問題を修正し、役に立たないエラーメッセージをフィルタリングする [#1678](https://github.com/pingcap/tiflow/pull/1678)
        -   MinIO を使用したレプリケーションで、冗長ディレクトリの作成が中断される可能性があるバグを修正しました [#1463](https://github.com/pingcap/tiflow/issues/1463)
        -   MySQL 5.7ダウンストリームがアップストリーム TiDB と同じ動作を維持するように、 `explicit_defaults_for_timestamp`セッション変数のデフォルト値を ON に設定します [#1585](https://github.com/pingcap/tiflow/issues/1585)
        -   `io.EOF`の不適切な処理により、レプリケーションが中断される可能性がある問題を修正しました [#1633](https://github.com/pingcap/tiflow/issues/1633)
        -   TiCDCダッシュボードのTiKV CDCエンドポイントCPUメトリックを修正する [#1645](https://github.com/pingcap/tiflow/pull/1645)
        -   `defaultBufferChanSize`を増やして、場合によってはレプリケーションのブロックを回避する [#1259](https://github.com/pingcap/tiflow/issues/1259)
        -   Avro出力でタイムゾーン情報が失われる問題を修正しました [#1712](https://github.com/pingcap/tiflow/pull/1712)
        -   Unified Sorter で古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリの共有を禁止する [#1742](https://github.com/pingcap/tiflow/pull/1742)
        -   KVクライアントで、多数の古いリージョンが存在する場合に発生するデッドロックバグを修正しました [#1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグの誤ったヘルプ情報を修正 [#1697](https://github.com/pingcap/tiflow/pull/1697)
        -   MySQLへのデータ複製時にSUPER権限を必要とする`explicit_defaults_for_timestamp`の更新を元に戻す [#1750](https://github.com/pingcap/tiflow/pull/1750)
        -   メモリオーバーフローのリスクを軽減するために、シンクフロー制御をサポートする [#1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブルを移動する際にレプリケーションタスクが停止する可能性があるバグを修正しました [#1828](https://github.com/pingcap/tiflow/pull/1828)
        -   TiCDCチェンジフィードチェックポイントの停滞によりTiKV GCセーフポイントがブロックされる問題を修正しました [#1759](https://github.com/pingcap/tiflow/pull/1759)
