---
title: TiDB 5.1 Release Notes
---

# TiDB5.1リリースノート {#tidb-5-1-release-notes}

発売日：2021年6月24日

TiDBバージョン：5.1.0

v5.1では、主な新機能または改善点は次のとおりです。

-   MySQL8.0のCommonTableExpression（CTE）機能をサポートして、SQLステートメントの可読性と実行効率を向上させます。
-   オンラインでの列タイプの変更をサポートして、コード開発の柔軟性を向上させます。
-   クエリの安定性を向上させるために新しい統計タイプを導入します。これはデフォルトで実験的機能として有効になっています。
-   MySQL 8.0の動的特権機能をサポートして、特定の操作に対してよりきめ細かい制御を実装します。
-   Stale Read機能を使用してローカルレプリカからデータを直接読み取ることをサポートして、読み取りの待ち時間を短縮し、クエリのパフォーマンスを向上させます（実験的）。
-   ロックビュー機能を追加して、データベース管理者（DBA）がトランザクションロックイベントを監視し、デッドロックの問題をトラブルシューティングできるようにします（実験的）。
-   バックグラウンドタスクにTiKV書き込みレートリミッターを追加して、読み取りおよび書き込み要求のレイテンシーが安定するようにします。

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前のTiDBバージョンからv5.1にアップグレードするときに、すべての中間バージョンの互換性の変更に関する注意事項を知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                      | タイプを変更する   | 説明                                                                                                                                |
| :--------------------------------------------------------------------------------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| [`cte_max_recursion_depth`](/system-variables.md#cte_max_recursion_depth)                | 新しく追加されました | 共通テーブル式の最大再帰深度を制御します。                                                                                                             |
| [`init_connect`](/system-variables.md#init_connect)                                      | 新しく追加されました | TiDBサーバーへの初期接続を制御します。                                                                                                             |
| [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)          | 新しく追加されました | TiDBが統計を収集する方法を制御します。この変数のデフォルト値は`2`です。これは実験的機能です。                                                                                |
| [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)    | 新しく追加されました | 接続しているTiDBサーバーでセキュリティ拡張モード（SEM）が有効になっているかどうかを示します。この変数設定は、TiDBサーバーを再起動せずに変更することはできません。                                            |
| [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)                   | 新しく追加されました | オプティマイザのコスト見積もりを無視するかどうか、およびクエリの実行にMPPモードを強制的に使用するかどうかを制御します。この変数のデータ型は`BOOL`で、デフォルト値は`false`です。                                  |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | 新しく追加されました | パーティションテーブルの動的プルーニングモードを有効にするかどうかを指定します。この機能は実験的です。この変数のデフォルト値は`static`です。これは、パーティション化されたテーブルの動的プルーニングモードがデフォルトで無効になっていることを意味します。 |

### Configuration / コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| Configuration / コンフィグレーションファイル | Configuration / コンフィグレーション項目                                                                             | タイプを変更する   | 説明                                                                                                                                                                         |
| :----------------------------- | :------------------------------------------------------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB構成ファイル                     | [`security.enable-sem`](/tidb-configuration-file.md#enable-sem)                                          | 新しく追加されました | セキュリティ拡張モード（SEM）を有効にするかどうかを制御します。この構成アイテムのデフォルト値は`false`です。これは、SEMが無効になっていることを意味します。                                                                                       |
| TiDB構成ファイル                     | `performance.committer-concurrency`                                                                      | 変更         | 単一トランザクションのコミットフェーズでのコミット操作に関連する要求の同時実行数を制御します。デフォルト値は`16`から`128`に変更されます。                                                                                                  |
| TiDB構成ファイル                     | [`performance.tcp-no-delay`](/tidb-configuration-file.md#tcp-no-delay)                                   | 新しく追加されました | TCP層でTCP_NODELAYを有効にするかどうかを決定します。デフォルト値は`true`です。これは、TCP_NODELAYが有効になっていることを意味します。                                                                                         |
| TiDB構成ファイル                     | [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)                                     | 新しく追加されました | TiDBがインスタンスレベルでオプティマイザーのコスト見積もりを無視し、MPPモードを適用するかどうかを制御します。デフォルト値は`false`です。この構成項目は、システム変数[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。 |
| TiDB構成ファイル                     | [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity)     | 新しく追加されました | 単一のTiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)つのテーブルに記録できるデッドロックイベントの最大数を設定します。デフォルト値は`10`です。                           |
| TiKV構成ファイル                     | [`abort-on-panic`](/tikv-configuration-file.md#abort-on-panic)                                           | 新しく追加されました | `abort`プロセスで、TiKVがパニックになったときにシステムがコアダンプファイルを生成できるようにするかどうかを設定します。デフォルト値は`false`です。これは、コアダンプファイルの生成が許可されていないことを意味します。                                                       |
| TiKV構成ファイル                     | [`hibernate-regions`](/tikv-configuration-file.md#hibernate-regions)                                     | 変更         | デフォルト値は`false`から`true`に変更されます。リージョンが長時間アイドル状態の場合、自動的に休止状態に設定されます。                                                                                                          |
| TiKV構成ファイル                     | [`old-value-cache-memory-quota`](/tikv-configuration-file.md#old-value-cache-memory-quota)               | 新しく追加されました | TiCDCの古い値によるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                              |
| TiKV構成ファイル                     | [`sink-memory-quota`](/tikv-configuration-file.md#sink-memory-quota)                                     | 新しく追加されました | TiCDCデータ変更イベントによるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                         |
| TiKV構成ファイル                     | [`incremental-scan-threads`](/tikv-configuration-file.md#incremental-scan-threads)                       | 新しく追加されました | 履歴データを段階的にスキャンするタスクのスレッド数を設定します。デフォルト値は`4`です。これは、タスクに4つのスレッドがあることを意味します。                                                                                                   |
| TiKV構成ファイル                     | [`incremental-scan-concurrency`](/tikv-configuration-file.md#incremental-scan-concurrency)               | 新しく追加されました | 履歴データを段階的にスキャンするタスクの同時実行の最大数を設定します。デフォルト値は`6`です。これは、最大6つのタスクを同時に実行できることを意味します。                                                                                             |
| TiKV構成ファイル                     | [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 変更         | 保留中の圧縮バイトのソフト制限。デフォルト値は`"64GB"`から`"192GB"`に変更されます。                                                                                                                         |
| TiKV構成ファイル                     | [`storage.io-rate-limit`](/tikv-configuration-file.md#storageio-rate-limit)                              | 新しく追加されました | TiKV書き込みのI/Oレートを制御します。デフォルト値の`storage.io-rate-limit.max-bytes-per-sec`は`"0MB"`です。                                                                                          |
| TiKV構成ファイル                     | [`resolved-ts.enable`](/tikv-configuration-file.md#enable)                                               | 新しく追加されました | すべてのリージョンリーダーに対して`resolved-ts`を維持するかどうかを決定します。デフォルト値は`true`です。                                                                                                             |
| TiKV構成ファイル                     | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)                     | 新しく追加されました | `resolved-ts`が転送される間隔。デフォルト値は`"1s"`です。値は動的に変更できます。                                                                                                                         |
| TiKV構成ファイル                     | [`resolved-ts.scan-lock-pool-size`](/tikv-configuration-file.md#scan-lock-pool-size)                     | 新しく追加されました | `resolved-ts`を初期化するときにTiKVがMVCC（マルチバージョン同時実行制御）ロックデータをスキャンするために使用するスレッドの数。デフォルト値は`2`です。                                                                                    |

### その他 {#others}

-   アップグレードする前に、TiDB構成[`feedback-probability`](/tidb-configuration-file.md#feedback-probability)の値を確認してください。値が0でない場合、アップグレード後に「回復可能なゴルーチンのpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDBのGoコンパイラバージョンをgo1.13.7からgo1.16.4にアップグレードします。これにより、TiDBのパフォーマンスが向上します。 TiDB開発者の場合は、Goコンパイラのバージョンをアップグレードして、スムーズにコンパイルできるようにしてください。
-   TiDBローリングアップグレード中にBinlogを使用するクラスタで、クラスター化インデックスを使用してテーブルを作成することは避けてください。
-   TiDBローリングアップグレード中に`alter table ... modify column`または`alter table ... change column`のようなステートメントを実行することは避けてください。
-   v5.1以降、各テーブルのTiFlashレプリカを構築するときに、システムテーブルのレプリカを設定することはサポートされなくなりました。クラスタをアップグレードする前に、関連するシステムテーブルのレプリカをクリアする必要があります。そうしないと、アップグレードは失敗します。
-   TiCDCの`cdc cli changefeed`コマンドの`--sort-dir`パラメータを非推奨にします。代わりに、 `cdc server`コマンドで`--sort-dir`を設定できます。 [＃1795](https://github.com/pingcap/tiflow/pull/1795)
-   TiDB 5.1にアップグレードした後、TiDBが「関数READ ONLYにはnoop実装のみがあります」エラーを返した場合、 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)から`ON`の値を設定することにより、TiDBにこのエラーを無視させることができます。これは、MySQLの`read_only`変数がTiDBではまだ有効になっていないためです（これはTiDBの「noop」動作です）。したがって、この変数がTiDBで設定されている場合でも、TiDBクラスタにデータを書き込むことができます。

## 新機能 {#new-features}

### SQL {#sql}

-   MySQL8.0のCommonTableExpression（CTE）機能をサポートします。

    この機能により、TiDBは階層データを再帰的または非再帰的にクエリすることができ、ツリークエリを使用して、人材、製造、金融市場、教育などの複数のセクターでアプリケーションロジックを実装する必要があります。

    TiDBでは、 `WITH`ステートメントを適用して共通テーブル式を使用できます。 [ユーザードキュメント](/sql-statements/sql-statement-with.md) [＃17472](https://github.com/pingcap/tidb/issues/17472)

-   MySQL8.0の動的特権機能をサポートします。

    動的特権は、 `SUPER`の特権を制限し、TiDBに、よりきめ細かいアクセス制御のためのより柔軟な特権構成を提供するために使用されます。たとえば、動的権限を使用して、 `BACKUP`および`RESTORE`の操作のみを実行できるユーザーアカウントを作成できます。

    サポートされている動的特権は次のとおりです。

    -   `BACKUP_ADMIN`
    -   `RESTORE_ADMIN`
    -   `ROLE_ADMIN`
    -   `CONNECTION_ADMIN`
    -   `SYSTEM_VARIABLES_ADMIN`

    プラグインを使用して新しい権限を追加することもできます。サポートされているすべての特権をチェックアウトするには、 `SHOW PRIVILEGES`ステートメントを実行します。 [ユーザードキュメント](/privilege-management.md)

-   セキュリティ拡張モード（SEM）の新しい構成項目を追加します。これにより、TiDB管理者権限がよりきめ細かく分割されます。

    セキュリティ強化モードはデフォルトで無効になっています。有効にするには、 [ユーザードキュメント](/system-variables.md#tidb_enable_enhanced_security)を参照してください。

-   オンラインで列タイプを変更する機能を強化します。以下を含むがこれらに限定されない、 `ALTER TABLE`ステートメントを使用したオンラインでの列タイプの変更をサポートします。

    -   `VARCHAR`から`BIGINT`に変更
    -   `DECIMAL`精度の変更
    -   `VARCHAR(10)`から`VARCHAR(5)`の長さを圧縮します

    [ユーザードキュメント](/sql-statements/sql-statement-modify-column.md)

-   新しいSQL構文`AS OF TIMESTAMP`を導入して、指定された時点または指定された時間範囲から履歴データを読み取るために使用される新しい実験的機能であるStaleReadを実行します。

    [ユーザードキュメント](/stale-read.md) [＃21094](https://github.com/pingcap/tidb/issues/21094)

    `AS OF TIMESTAMP`の例は次のとおりです。

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

-   新しい統計タイプ`tidb_analyze_version = 2` （実験的）を導入します。

    デフォルトでは`tidb_analyze_version`が`2`に設定されています。これにより、バージョン1のハッシュの競合によって発生する可能性のある大量のデータで発生する可能性のある大きなエラーが回避され、ほとんどのシナリオで推定精度が維持されます。

    [ユーザードキュメント](/statistics.md)

### 取引 {#transaction}

-   ロックビュー機能をサポートする（実験的）

    ロックビュー機能は、ペシミスティックロックのロック競合とロック待機に関する詳細情報を提供します。これは、DBAがトランザクションのロック状態を監視し、デッドロックの問題をトラブルシューティングするのに役立ちます。 [＃24199](https://github.com/pingcap/tidb/issues/24199)

    ユーザードキュメント：

    -   クラスタ内のすべてのTiKVノードで現在発生している悲観的ロックおよびその他のロックをビューします[`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDBノードで最近発生したいくつかのデッドロックエラーをビューします[`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDBノードで現在実行されているトランザクション情報をビューします[`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### パフォーマンス {#performance}

-   データレプリカの古い読み取り（実験的）

    ローカルレプリカデータを直接読み取ることで、読み取りの待ち時間を短縮し、クエリのパフォーマンスを向上させます

    [ユーザードキュメント](/stale-read.md) [＃21094](https://github.com/pingcap/tidb/issues/21094)

-   デフォルトで休止状態機能を有効にします。

    リージョンが長期間非アクティブ状態にある場合、リージョンは自動的にサイレント状態に設定されます。これにより、リーダーとフォロワーの間のハートビート情報のシステムオーバーヘッドが削減されます。

    [ユーザードキュメント](/tikv-configuration-file.md#hibernate-regions) [＃10266](https://github.com/tikv/tikv/pull/10266)

### 安定性 {#stability}

-   TiCDCの複製の安定性の問題を解決する

    -   次のシナリオでOOMを回避するために、TiCDCのメモリ使用量を改善します
    -   レプリケーションの中断中に1TBを超える大量のデータが蓄積されると、再レプリケーションによってOOMの問題が発生します。
    -   大量のデータ書き込みは、TiCDCでOOMの問題を引き起こします。
    -   次のシナリオで、TiCDCレプリケーションの中断の可能性を減らします。

        [プロジェクト＃11](https://github.com/pingcap/tiflow/projects/11)

        -   ネットワークが不安定な場合のレプリケーションの中断
        -   一部のTiKV/PD/TiCDCノードがダウンした場合のレプリケーションの中断

-   TiFlashストレージメモリ制御

    リージョンスナップショット生成の速度とメモリ使用量を最適化し、OOMの可能性を減らします

-   TiKVバックグラウンドタスクの書き込みレートリミッターを追加します（TiKV書き込みレートリミッター）

    読み取りおよび書き込み要求の継続時間の安定性を確保するために、TiKV書き込みレートリミッターは、GCや圧縮などのTiKVバックグラウンドタスクの書き込みトラフィックをスムーズにします。 TiKVバックグラウンドタスク書き込みレートリミッターのデフォルト値は「0MB」です。この値は、クラウドディスクの製造元が指定した最大I / O帯域幅など、ディスクの最適なI/O帯域幅に設定することをお勧めします。

    [ユーザードキュメント](/tikv-configuration-file.md#storageio-rate-limit) [＃9156](https://github.com/tikv/tikv/issues/9156)

-   複数のスケーリングタスクが同時に実行される場合のスケジューリングの安定性の問題を解決します

### テレメトリー {#telemetry}

TiDBは、実行ステータス、障害ステータスなどを含む、テレメトリでのTiDBクラスタ要求の実行ステータスを追加します。

情報とこの動作を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## 改善 {#improvements}

-   TiDB

    -   組み込み機能をサポートする`VITESS_HASH()` [＃23915](https://github.com/pingcap/tidb/pull/23915)
    -   `WHERE`節[＃23619](https://github.com/pingcap/tidb/issues/23619)で列挙型を使用する場合のパフォーマンスを向上させるために、列挙型のデータをTiKVにプッシュダウンすることをサポートします。
    -   ROW_NUMBER（） [＃23807](https://github.com/pingcap/tidb/issues/23807)を使用してデータをページングするときに、ウィンドウ関数の計算を最適化してTiDBOOMの問題を解決します。
    -   `UNION ALL`の計算を最適化して、 `UNION ALL`を使用して多数の`SELECT`のステートメントを結合する場合のTiDBOOMの問題を解決します[＃21441](https://github.com/pingcap/tidb/issues/21441)
    -   パーティションテーブルの動的プルーニングモードを最適化して、パフォーマンスと安定性を向上させます[＃24150](https://github.com/pingcap/tidb/issues/24150)
    -   複数のシナリオで発生する`Region is Unavailable`の問題を修正します[プロジェクト＃62](https://github.com/pingcap/tidb/projects/62)
    -   頻繁なスケジューリング状況で発生する可能性のある複数の`Region is Unavailable`の問題を修正します
    -   一部の高ストレス書き込み状況で発生する可能性のある`Region is Unavailable`の問題を修正
    -   キャッシュされた統計が最新の場合は、CPU使用率が高くなるのを避けるために、 `mysql.stats_histograms`テーブルを頻繁に[＃24317](https://github.com/pingcap/tidb/pull/24317)ことは避けてください。

-   TiKV

    -   `zstd`を使用してリージョンのスナップショットを圧縮し、大量のスケジューリングまたはスケーリングの場合にノード間の大きなスペースの違いを防ぎます[＃10005](https://github.com/tikv/tikv/pull/10005)

    -   複数のケースでOOMの問題を解決する[＃10183](https://github.com/tikv/tikv/issues/10183)

        -   各モジュールのメモリ使用量追跡を追加します
        -   特大のRaftエントリキャッシュによって引き起こされるOOMの問題を解決します
        -   スタックされたGCタスクによって引き起こされるOOMの問題を解決します
        -   一度にRaftログからメモリに取得するRaftエントリが多すぎるために発生するOOMの問題を解決します

    -   ホットスポット書き込みがある場合にリージョンサイズの増加がスプリット速度を超えるという問題を軽減するために、リージョンをより均等に分割します[＃9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   `Union All` 、および`TopN`の関数を`Limit`
    -   MPPモードでの左外部結合と半反結合を含むデカルト積をサポートします
    -   ロック操作を最適化して、実行中のDDLステートメントと読み取り操作が相互にブロックされないようにします
    -   TiFlashによる期限切れデータのクリーンアップを最適化する
    -   TiFlashストレージレベルで`timestamp`列のクエリフィルターのさらなるフィルタリングをサポート
    -   多数のテーブルがクラスタにある場合のTiFlashの起動とスケーラビリティの速度を向上させる
    -   不明なCPUで実行する場合のTiFlashの互換性を改善します

-   PD

    -   `scatter region`スケジューラーを追加した後の予期しない統計を回避する[＃3602](https://github.com/pingcap/pd/pull/3602)
    -   スケーリングプロセスで複数のスケジューリングの問題を解決する

        -   レプリカスナップショットの生成プロセスを最適化して、スケーリング中の遅いスケジューリングの問題を解決します[＃3563](https://github.com/tikv/pd/issues/3563) [＃10059](https://github.com/tikv/tikv/pull/10059) [＃10001](https://github.com/tikv/tikv/pull/10001)
        -   トラフィックの変化による[＃3751](https://github.com/tikv/pd/issues/3751)のプレッシャーによって引き起こされる遅いスケジューリングの問題を解決し[＃3693](https://github.com/tikv/pd/issues/3693) [＃3739](https://github.com/tikv/pd/issues/3739) [＃3728](https://github.com/tikv/pd/issues/3728)
        -   スケジューリングによる大規模なクラスターのスペースの不一致を減らし、大規模な圧縮率の不一致によって引き起こされるバーストの問題（異種のスペースクラスターと同様）を防ぐためにスケジューリング式を最適化します[＃3592](https://github.com/tikv/pd/issues/3592) [＃10005](https://github.com/tikv/tikv/pull/10005)

-   ツール

    -   バックアップと復元（BR）

        -   `mysql` [＃1078](https://github.com/pingcap/br/pull/1078) [＃1143](https://github.com/pingcap/br/pull/1143)でのシステムテーブルのバックアップと復元のサポート
        -   仮想ホストアドレッシングモードに基づくS3互換ストレージをサポートする[＃10243](https://github.com/tikv/tikv/pull/10243)
        -   バックアップメタのフォーマットを最適化してメモリ使用量を削減[＃1171](https://github.com/pingcap/br/pull/1171)

    -   TiCDC

        -   一部のログメッセージの説明を改善して、問題の診断に役立つようにします[＃1759](https://github.com/pingcap/tiflow/pull/1759)
        -   背圧機能をサポートして、TiCDCスキャン速度がダウンストリーム処理能力を検出できるようにします[＃10151](https://github.com/tikv/tikv/pull/10151)
        -   TiCDCが初期スキャンを実行するときのメモリ使用量を減らす[＃10133](https://github.com/tikv/tikv/pull/10133)
        -   悲観的なトランザクションでのTiCDCOldValueのキャッシュヒット率を改善する[＃10089](https://github.com/tikv/tikv/pull/10089)

    -   Dumpling

        -   TiDBがメモリ不足（OOM）になるのを防ぐために、TiDBv4.0からデータをエクスポートするロジックを改善します[＃273](https://github.com/pingcap/dumpling/pull/273)

        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正します[＃280](https://github.com/pingcap/dumpling/pull/280)

    -   TiDB Lightning

        -   データのインポート速度を向上させます。最適化の結果は、TPC-Cデータのインポート速度が30％向上し、より多くのインデックス（5インデックス）を持つ大きなテーブル（2TB +）のインポート速度が50％以上向上することを示しています。 [＃753](https://github.com/pingcap/br/pull/753)
        -   インポートするデータと、インポートする前のターゲットクラスタに事前チェックを追加し、エラーを報告して、インポート要件を満たしていない場合にインポートプロセスを拒否します[＃999](https://github.com/pingcap/br/pull/999)
        -   ローカルバックエンドでのチェックポイント更新のタイミングを最適化して、ブレークポイントからの再起動のパフォーマンスを向上させます[＃1080](https://github.com/pingcap/br/pull/1080)

## バグの修正 {#bug-fixes}

-   TiDB

    -   投影結果が空の場合、プロジェクト除去の実行結果が間違っている可能性がある問題を修正します[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   列に`NULL`の値が含まれている場合の誤ったクエリ結果の問題を修正します[＃23891](https://github.com/pingcap/tidb/issues/23891)
    -   スキャンに仮想列が含まれている場合にMPPプランの生成を禁止する[＃23886](https://github.com/pingcap/tidb/issues/23886)
    -   プラン[＃23144](https://github.com/pingcap/tidb/issues/23144) [＃23187](https://github.com/pingcap/tidb/issues/23187)での`PointGet`と`TableDual`の[＃23290](https://github.com/pingcap/tidb/issues/23290)た再利用を[＃23304](https://github.com/pingcap/tidb/issues/23304)
    -   オプティマイザーがクラスター化インデックスの`IndexMerge`プランを作成するときに発生するエラーを修正します[＃23906](https://github.com/pingcap/tidb/issues/23906)
    -   BITタイプエラーのタイプ推論を修正します[＃23832](https://github.com/pingcap/tidb/issues/23832)
    -   `PointGet`演算子が存在する場合に一部のオプティマイザヒントが有効にならない問題を修正します[＃23570](https://github.com/pingcap/tidb/issues/23570)
    -   エラー[＃23893](https://github.com/pingcap/tidb/issues/23893)が原因でロールバック時にDDL操作が失敗する可能性がある問題を修正します
    -   バイナリリテラル定数のインデックス範囲が正しく構築されない問題を修正します[＃23672](https://github.com/pingcap/tidb/issues/23672)
    -   場合によっては`IN`句の潜在的な誤った結果を修正します[＃23889](https://github.com/pingcap/tidb/issues/23889)
    -   一部の文字列関数の誤った結果を修正する[＃23759](https://github.com/pingcap/tidb/issues/23759)
    -   ユーザーは、 `REPLACE`の操作を実行するために、テーブルに対して`INSERT`と`DELETE`の両方の特権が必要になります[＃23909](https://github.com/pingcap/tidb/issues/23909)
    -   ユーザーは、 `REPLACE`の操作を実行するために、テーブルに対して`INSERT`と`DELETE`の両方の特権が必要になります[＃24070](https://github.com/pingcap/tidb/pull/24070)
    -   バイナリとバイト[＃23846](https://github.com/pingcap/tidb/issues/23846)を誤って比較することによって引き起こされた間違った`TableDual`プランを修正します
    -   場合によっては[＃24717](https://github.com/pingcap/tidb/issues/24717)インデックスとインデックス結合を使用することによって引き起こされるpanicの問題を修正し[＃24547](https://github.com/pingcap/tidb/issues/24547) [＃24716](https://github.com/pingcap/tidb/issues/24716)
    -   準備されたプランキャッシュ`point get`がトランザクション[＃24741](https://github.com/pingcap/tidb/issues/24741)の`point get`ステートメントによって誤って使用される問題を修正します。
    -   照合順序が`ascii_bin`または[＃24569](https://github.com/pingcap/tidb/issues/24569)の場合に間違ったプレフィックスインデックス値を書き込む問題を修正し`latin1_bin`
    -   進行中のトランザクションがGCワーカーによって中断される可能性があるという問題を修正します[＃24591](https://github.com/pingcap/tidb/issues/24591)
    -   `new-collation`が有効で、 `new-row-format`が無効の場合、クラスター化インデックスでポイントクエリが間違ってしまう可能性があるバグを修正します[＃24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフルハッシュ結合[＃24490](https://github.com/pingcap/tidb/pull/24490)のパーティションキーの変換をリファクタリングします
    -   `HAVING`句[＃24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプランを作成するときに発生するpanicの問題を修正します
    -   列プルーニングの改善により、 `Apply`および`Join`の演算子の結果が正しくなくなる問題を修正します[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックされたプライマリロックを解決できないバグを修正します[＃24384](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketchレコードの重複を引き起こす可能性のある統計のGCの問題を修正します[＃24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的ロックが`ErrKeyExists`エラー[＃23799](https://github.com/pingcap/tidb/issues/23799)を受け取ったときに、不必要な悲観的ロールバックを回避します。
    -   sql_modeに`ANSI_QUOTES`が含まれていると、数値リテラルが認識されない問題を修正し[＃24429](https://github.com/pingcap/tidb/issues/24429) 。
    -   リストされていないパーティションからデータを読み取るための`INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`などのステートメントの禁止[＃24746](https://github.com/pingcap/tidb/issues/24746)
    -   SQLステートメントに`GROUP BY`と[＃24281](https://github.com/pingcap/tidb/issues/24281)の両方が含まれている場合の潜在的な`index out of range`エラーを修正し`UNION` 。
    -   `CONCAT`関数が照合順序[＃24296](https://github.com/pingcap/tidb/issues/24296)を誤って処理する問題を修正します
    -   `collation_server`グローバル変数が新しいセッションで有効にならない問題を修正します[＃24156](https://github.com/pingcap/tidb/pull/24156)

-   TiKV

    -   コプロセッサーが`IN`式[＃9821](https://github.com/tikv/tikv/issues/9821)の符号付きまたは符号なし整数型を適切に処理できない問題を修正します。
    -   SSTファイルをバッチ取り込みした後の多くの空のリージョンの問題を修正します[＃964](https://github.com/pingcap/br/issues/964)
    -   ファイル辞書ファイルが破損した後にTiKVが起動できないバグを修正します[＃9886](https://github.com/tikv/tikv/issues/9886)
    -   古い値の読み取りによって引き起こされる[＃9981](https://github.com/tikv/tikv/issues/9981)の問題を修正します[＃9996](https://github.com/tikv/tikv/issues/9996)
    -   照合順序が`latin1_bin`の場合に、クラスター化された主キー列の2次インデックスの値が空になる問題を修正し[＃24548](https://github.com/pingcap/tidb/issues/24548) 。
    -   panicが発生したときにTiKVがコアダンプファイルを生成できるようにする`abort-on-panic`の構成を追加します。ユーザーは、コアダンプ[＃10216](https://github.com/tikv/tikv/pull/10216)を有効にするために環境を正しく構成する必要があります。
    -   TiKVがビジーでないときに発生する`point get`クエリのパフォーマンスリグレッションの問題を修正します[＃10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多いとPDリーダーの再選が遅くなる問題を修正[＃3697](https://github.com/tikv/pd/issues/3697)

    -   存在しないストアからエビクトリーダースケジューラを削除するときに発生するpanicの問題を修正します[＃3660](https://github.com/tikv/pd/issues/3660)

    -   オフラインピアがマージされた後に統計が更新されない問題を修正します[＃3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   時間型を整数型にキャストするときの誤った結果の問題を修正します
    -   `receiver`が10秒以内に対応するタスクを見つけることができないバグを修正します
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性があるという問題を修正します
    -   `bitwise`演算子の動作がTiDBの動作と異なるバグを修正します
    -   `prefix key`を使用するときに範囲が重複することによって発生するアラートの問題を修正します
    -   文字列型を整数型にキャストするときの誤った結果の問題を修正します
    -   連続した高速書き込みによってTiFlashのメモリが不足する可能性がある問題を修正します
    -   テーブルGC中にnullポインタの例外が発生する可能性があるという潜在的な問題を修正します
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正します
    -   BRの復元中にTiFlashがpanicになる可能性がある問題を修正します
    -   共有デルタインデックスを同時に複製した場合の誤った結果の問題を修正
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるpanicを修正します
    -   TiFlashが非同期コミットからフォールバックされたロックを解決できない問題を修正します
    -   `TIMEZONE`タイプのキャスト結果に`TIMESTAMP`タイプが含まれている場合に誤った結果が返される問題を修正しました
    -   セグメント分割中に発生するTiFlashpanicの問題を修正します

-   ツール

    -   TiDB Lightning

        -   KVデータの生成時に発生するTiDB Lightningpanicの問題を修正します[＃1127](https://github.com/pingcap/br/pull/1127)
        -   データのインポート中にキーの合計サイズがラフトエントリの制限を超えたためにバッチ分割リージョンが失敗するバグを修正します[＃969](https://github.com/pingcap/br/issues/969)
        -   CSVファイルをインポートするときに、ファイルの最後の行に改行文字（ `\r\n` ）が含まれていない場合、エラーが報告される問題を修正します[＃1133](https://github.com/pingcap/br/issues/1133)
        -   インポートするテーブルにdouble型の自動インクリメント列が含まれている場合、auto_increment値が異常になる問題を修正します[＃1178](https://github.com/pingcap/br/pull/1178)

    -   バックアップと復元（BR）
        -   いくつかのTiKVノードの障害によって引き起こされるバックアップ中断の問題を修正します[＃980](https://github.com/pingcap/br/issues/980)

    -   TiCDC

        -   Unified Sorterの同時実行の問題を修正し、役に立たないエラーメッセージをフィルタリングします[＃1678](https://github.com/pingcap/tiflow/pull/1678)
        -   冗長ディレクトリの作成がMinIO1でのレプリケーションを中断する可能性があるバグを修正し[＃1463](https://github.com/pingcap/tiflow/issues/1463)
        -   `explicit_defaults_for_timestamp`セッション変数のデフォルト値をONに設定して、 MySQL 5.7ダウンストリームがアップストリーム[＃1585](https://github.com/pingcap/tiflow/issues/1585)と同じ動作を維持するようにします。
        -   `io.EOF`を誤って処理すると、レプリケーションが中断される可能性があるという問題を修正します[＃1633](https://github.com/pingcap/tiflow/issues/1633)
        -   TiCDCダッシュボードのTiKVCDCエンドポイントCPUメトリックを修正します[＃1645](https://github.com/pingcap/tiflow/pull/1645)
        -   場合によってはレプリケーションのブロックを回避するために`defaultBufferChanSize`を増やします[＃1259](https://github.com/pingcap/tiflow/issues/1259)
        -   Avro出力[＃1712](https://github.com/pingcap/tiflow/pull/1712)でタイムゾーン情報が失われる問題を修正します
        -   Unified Sorterでの古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリの共有を禁止します[＃1742](https://github.com/pingcap/tiflow/pull/1742)
        -   多くの古いリージョンが存在する場合に発生するKVクライアントのデッドロックバグを修正します[＃1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[＃1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正します
        -   [＃1750](https://github.com/pingcap/tiflow/pull/1750)にデータを複製するときにSUPER特権を必要とする`explicit_defaults_for_timestamp`の更新を元に戻します。
        -   シンクフロー制御をサポートして、メモリオーバーフローのリスクを軽減します[＃1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブルを移動するときにレプリケーションタスクが停止する可能性があるバグを修正します[＃1828](https://github.com/pingcap/tiflow/pull/1828)
        -   TiCDCチェンジフィードチェックポイント[＃1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により、TiKVGCセーフポイントがブロックされる問題を修正します。
