---
title: TiDB 5.1 Release Notes
---

# TiDB 5.1 リリースノート {#tidb-5-1-release-notes}

発売日：2021年6月24日

TiDB バージョン: 5.1.0

v5.1 の主な新機能または改善点は次のとおりです。

-   MySQL 8.0 の Common Table Expression (CTE) 機能をサポートし、SQL ステートメントの読みやすさと実行効率を向上させます。
-   コード開発の柔軟性を向上させるために、オンラインでの列タイプの変更をサポートします。
-   クエリの安定性を向上させるために新しい統計タイプを導入します。これは実験的機能としてデフォルトで有効になっています。
-   MySQL 8.0 の動的特権機能をサポートして、特定の操作に対するよりきめ細かい制御を実装します。
-   ステイル読み取り機能を使用したローカル レプリカからのデータの直接読み取りをサポートし、読み取りレイテンシーを削減し、クエリのパフォーマンスを向上させます (Experimental)。
-   ロックビュー機能を追加して、データベース管理者 (DBA) がトランザクション ロック イベントを監視し、デッドロックの問題をトラブルシューティングできるようにします (Experimental)。
-   バックグラウンド タスクに TiKV 書き込みレート リミッターを追加して、読み取りおよび書き込みリクエストのレイテンシーが安定していることを確認します。

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v5.1 にアップグレードする場合、すべての中間バージョンの互換性変更メモを知りたい場合は、対応するバージョンの[<a href="/releases/release-notes.md">リリースノート</a>](/releases/release-notes.md)を確認してください。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                              | 種類の変更    | 説明                                                                                                                              |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------ |
| [<a href="/system-variables.md#cte_max_recursion_depth">`cte_max_recursion_depth`</a>](/system-variables.md#cte_max_recursion_depth)                             | 新しく追加された | 共通テーブル式の最大再帰の深さを制御します。                                                                                                          |
| [<a href="/system-variables.md#init_connect">`init_connect`</a>](/system-variables.md#init_connect)                                                              | 新しく追加された | TiDBサーバーへの最初の接続を制御します。                                                                                                          |
| [<a href="/system-variables.md#tidb_analyze_version-new-in-v510">`tidb_analyze_version`</a>](/system-variables.md#tidb_analyze_version-new-in-v510)              | 新しく追加された | TiDB が統計を収集する方法を制御します。この変数のデフォルト値は`2`です。これは実験的機能です。                                                                             |
| [<a href="/system-variables.md#tidb_enable_enhanced_security">`tidb_enable_enhanced_security`</a>](/system-variables.md#tidb_enable_enhanced_security)           | 新しく追加された | 接続している TiDBサーバーでSecurity強化モード (SEM) が有効になっているかどうかを示します。この変数設定は、TiDBサーバーを再起動しないと変更できません。                                         |
| [<a href="/system-variables.md#tidb_enforce_mpp-new-in-v51">`tidb_enforce_mpp`</a>](/system-variables.md#tidb_enforce_mpp-new-in-v51)                            | 新しく追加された | オプティマイザーのコスト見積もりを無視し、クエリ実行に MPP モードを強制的に使用するかどうかを制御します。この変数のデータ型は`BOOL`で、デフォルト値は`false`です。                                      |
| [<a href="/system-variables.md#tidb_partition_prune_mode-new-in-v51">`tidb_partition_prune_mode`</a>](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | 新しく追加された | パーティションテーブルの動的プルーニングモードを有効にするかどうかを指定します。この機能は実験的です。この変数のデフォルト値は`static`です。これは、パーティション化されたテーブルの動的プルーニング モードがデフォルトで無効であることを意味します。 |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                                                                                                           | 種類の変更    | 説明                                                                                                                                                                                                                                           |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB 設定ファイル    | [<a href="/tidb-configuration-file.md#enable-sem">`security.enable-sem`</a>](/tidb-configuration-file.md#enable-sem)                                                                   | 新しく追加された | Security強化モード (SEM) を有効にするかどうかを制御します。この構成項目のデフォルト値は`false`で、SEM が無効であることを意味します。                                                                                                                                                              |
| TiDB 設定ファイル    | `performance.committer-concurrency`                                                                                                                                                    | 修正済み     | 単一トランザクションのコミットフェーズでのコミット操作に関連するリクエストの同時実行数を制御します。デフォルト値が`16`から`128`に変更されました。                                                                                                                                                                |
| TiDB 設定ファイル    | [<a href="/tidb-configuration-file.md#tcp-no-delay">`performance.tcp-no-delay`</a>](/tidb-configuration-file.md#tcp-no-delay)                                                          | 新しく追加された | TCPレイヤーで TCP_NODELAY を有効にするかどうかを決定します。デフォルト値は`true`で、TCP_NODELAY が有効であることを意味します。                                                                                                                                                             |
| TiDB 設定ファイル    | [<a href="/tidb-configuration-file.md#enforce-mpp">`performance.enforce-mpp`</a>](/tidb-configuration-file.md#enforce-mpp)                                                             | 新しく追加された | TiDB がインスタンス レベルでオプティマイザーのコスト見積もりを無視し、MPP モードを強制するかどうかを制御します。デフォルト値は`false`です。この構成項目は、システム変数[<a href="/system-variables.md#tidb_enforce_mpp-new-in-v51">`tidb_enforce_mpp`</a>](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。 |
| TiDB 設定ファイル    | [<a href="/tidb-configuration-file.md#deadlock-history-capacity">`pessimistic-txn.deadlock-history-capacity`</a>](/tidb-configuration-file.md#deadlock-history-capacity)               | 新しく追加された | 単一の TiDBサーバーの[<a href="/information-schema/information-schema-deadlocks.md">`INFORMATION_SCHEMA.DEADLOCKS`</a>](/information-schema/information-schema-deadlocks.md)テーブルに記録できるデッドロック イベントの最大数を設定します。デフォルト値は`10`です。                           |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#abort-on-panic">`abort-on-panic`</a>](/tikv-configuration-file.md#abort-on-panic)                                                                | 新しく追加された | TiKV がパニックになったときに、 `abort`プロセスでシステムがコア ダンプ ファイルを生成できるようにするかどうかを設定します。デフォルト値は`false`で、コア ダンプ ファイルの生成が許可されていないことを意味します。                                                                                                                        |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#hibernate-regions">`hibernate-regions`</a>](/tikv-configuration-file.md#hibernate-regions)                                                       | 修正済み     | デフォルト値が`false`から`true`に変更されました。リージョンが長時間アイドル状態である場合、リージョンは自動的に休止状態に設定されます。                                                                                                                                                                   |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#old-value-cache-memory-quota">`old-value-cache-memory-quota`</a>](/tikv-configuration-file.md#old-value-cache-memory-quota)                      | 新しく追加された | TiCDC の古い値でメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                                                                                                 |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#sink-memory-quota">`sink-memory-quota`</a>](/tikv-configuration-file.md#sink-memory-quota)                                                       | 新しく追加された | TiCDC データ変更イベントによるメモリ使用量の上限を設定します。デフォルト値は`512MB`です。                                                                                                                                                                                          |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#incremental-scan-threads">`incremental-scan-threads`</a>](/tikv-configuration-file.md#incremental-scan-threads)                                  | 新しく追加された | 履歴データを増分スキャンするタスクのスレッド数を設定します。デフォルト値は`4`で、タスクに 4 つのスレッドがあることを意味します。                                                                                                                                                                          |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#incremental-scan-concurrency">`incremental-scan-concurrency`</a>](/tikv-configuration-file.md#incremental-scan-concurrency)                      | 新しく追加された | 履歴データを段階的にスキャンするタスクの同時実行の最大数を設定します。デフォルト値は`6`で、最大 6 つのタスクを同時に実行できることを意味します。                                                                                                                                                                  |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#soft-pending-compaction-bytes-limit">`soft-pending-compaction-bytes-limit`</a>](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 修正済み     | 保留中の圧縮バイトのソフト制限。デフォルト値が`"64GB"`から`"192GB"`に変更されました。                                                                                                                                                                                          |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#storageio-rate-limit">`storage.io-rate-limit`</a>](/tikv-configuration-file.md#storageio-rate-limit)                                             | 新しく追加された | TiKV 書き込みの I/O 速度を制御します。デフォルト値の`storage.io-rate-limit.max-bytes-per-sec`は`"0MB"`です。                                                                                                                                                          |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#enable">`resolved-ts.enable`</a>](/tikv-configuration-file.md#enable)                                                                            | 新しく追加された | すべてのリージョンリーダーの`resolved-ts`を維持するかどうかを決定します。デフォルト値は`true`です。                                                                                                                                                                                  |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#advance-ts-interval">`resolved-ts.advance-ts-interval`</a>](/tikv-configuration-file.md#advance-ts-interval)                                     | 新しく追加された | `resolved-ts`が転送される間隔。デフォルト値は`"1s"`です。値を動的に変更できます。                                                                                                                                                                                           |
| TiKV設定ファイル     | [<a href="/tikv-configuration-file.md#scan-lock-pool-size">`resolved-ts.scan-lock-pool-size`</a>](/tikv-configuration-file.md#scan-lock-pool-size)                                     | 新しく追加された | TiKV が`resolved-ts`の初期化時に MVCC (マルチバージョン同時実行制御) ロック データをスキャンするために使用するスレッドの数。デフォルト値は`2`です。                                                                                                                                                    |

### その他 {#others}

-   アップグレードの前に、TiDB 構成の値を確認してください[<a href="https://docs.pingcap.com/tidb/v5.1/tidb-configuration-file#feedback-probability">`feedback-probability`</a>](https://docs.pingcap.com/tidb/v5.1/tidb-configuration-file#feedback-probability) 。値が 0 でない場合、アップグレード後に「回復可能な goroutine のpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDB の Go コンパイラー バージョンを go1.13.7 から go1.16.4 にアップグレードすると、TiDB のパフォーマンスが向上します。 TiDB 開発者の場合は、スムーズにコンパイルできるように Go コンパイラーのバージョンをアップグレードしてください。
-   TiDB ローリング アップグレード中に、TiDB Binlogを使用するクラスター内にクラスター化インデックスを含むテーブルを作成しないでください。
-   TiDB ローリング アップグレード中に`alter table ... modify column`や`alter table ... change column`のようなステートメントを実行しないでください。
-   v5.1 以降、テーブルごとにTiFlashレプリカを構築する場合のシステム テーブルのレプリカの設定はサポートされなくなりました。クラスターをアップグレードする前に、関連するシステム テーブルのレプリカをクリアする必要があります。そうしないと、アップグレードは失敗します。
-   TiCDC の`cdc cli changefeed`コマンドの`--sort-dir`パラメータを非推奨にします。代わりに、 `cdc server`コマンドで`--sort-dir`を設定できます。 [<a href="https://github.com/pingcap/tiflow/pull/1795">#1795</a>](https://github.com/pingcap/tiflow/pull/1795)
-   TiDB 5.1 にアップグレードした後、TiDB が「関数 READ ONLY には noop 実装しかありません」エラーを返した場合、値[<a href="/system-variables.md#tidb_enable_noop_functions-new-in-v40">`tidb_enable_noop_functions`</a>](/system-variables.md#tidb_enable_noop_functions-new-in-v40)から`ON`を設定することで TiDB にこのエラーを無視させることができます。これは、MySQL の`read_only`変数が TiDB ではまだ有効になっていないためです (これは TiDB では「noop」動作です)。したがって、この変数が TiDB に設定されている場合でも、TiDB クラスターにデータを書き込むことができます。

## 新機能 {#new-features}

### SQL {#sql}

-   MySQL 8.0 の Common Table Expression (CTE) 機能をサポートします。

    この機能により、TiDB は階層データを再帰的または非再帰的にクエリできるようになり、人事、製造、金融市場、教育などの複数のセクターでツリー クエリを使用してアプリケーション ロジックを実装するニーズを満たします。

    TiDB では、 `WITH`ステートメントを適用して共通テーブル式を使用できます。 [<a href="/sql-statements/sql-statement-with.md">ユーザードキュメント</a>](/sql-statements/sql-statement-with.md) [<a href="https://github.com/pingcap/tidb/issues/17472">#17472</a>](https://github.com/pingcap/tidb/issues/17472)

-   MySQL 8.0 の動的権限機能をサポートします。

    動的権限は、 `SUPER`特権を制限し、よりきめ細かいアクセス制御のためのより柔軟な特権構成を TiDB に提供するために使用されます。たとえば、動的権限を使用して、 `BACKUP`と`RESTORE`操作のみを実行できるユーザー アカウントを作成できます。

    サポートされている動的権限は次のとおりです。

    -   `BACKUP_ADMIN`
    -   `RESTORE_ADMIN`
    -   `ROLE_ADMIN`
    -   `CONNECTION_ADMIN`
    -   `SYSTEM_VARIABLES_ADMIN`

    プラグインを使用して新しい権限を追加することもできます。サポートされているすべての権限を確認するには、 `SHOW PRIVILEGES`ステートメントを実行します。 [<a href="/privilege-management.md">ユーザードキュメント</a>](/privilege-management.md)

-   Security強化モード (SEM) の新しい構成項目を追加します。これにより、TiDB 管理者権限がよりきめ細かい方法で分割されます。

    Security強化モードはデフォルトでは無効になっています。これを有効にするには、 [<a href="/system-variables.md#tidb_enable_enhanced_security">ユーザードキュメント</a>](/system-variables.md#tidb_enable_enhanced_security)を参照してください。

-   オンラインで列タイプを変更する機能を強化します。 `ALTER TABLE`ステートメントを使用したオンラインでの列タイプの変更をサポートします。これには次のものが含まれますが、これらに限定されません。

    -   `VARCHAR`を`BIGINT`に変更する
    -   `DECIMAL`精度を変更する
    -   `VARCHAR(10)` ～ `VARCHAR(5)`の長さを圧縮する

    [<a href="/sql-statements/sql-statement-modify-column.md">ユーザードキュメント</a>](/sql-statements/sql-statement-modify-column.md)

-   新しい SQL 構文`AS OF TIMESTAMP`を導入して、指定された時点または指定された時間範囲から履歴データを読み取るために使用される新しい実験的機能であるステイル読み取りを実行します。

    [<a href="/stale-read.md">ユーザードキュメント</a>](/stale-read.md) [<a href="https://github.com/pingcap/tidb/issues/21094">#21094</a>](https://github.com/pingcap/tidb/issues/21094)

    `AS OF TIMESTAMP`の例は以下の通りです。

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

-   新しい統計タイプ`tidb_analyze_version = 2` (Experimental) を導入します。

    デフォルトでは`tidb_analyze_version`が`2`に設定されており、これにより、バージョン 1 のハッシュ競合によって大量のデータで発生する可能性のある大きなエラーが回避され、ほとんどのシナリオで推定精度が維持されます。

    [<a href="/statistics.md">ユーザードキュメント</a>](/statistics.md)

### トランザクション {#transaction}

-   ビューのロック機能をサポート (Experimental)

    ロックビュー機能は、ロックの競合と悲観的ロックのロック待機に関する詳細情報を提供します。これは、DBA がトランザクション ロック状態を観察し、デッドロックの問題をトラブルシューティングするのに役立ちます。 [<a href="https://github.com/pingcap/tidb/issues/24199">#24199</a>](https://github.com/pingcap/tidb/issues/24199)

    ユーザー文書:

    -   クラスター内のすべての TiKV ノードで現在発生している悲観的ロックとその他のロックをビュー[<a href="/information-schema/information-schema-data-lock-waits.md">`DATA_LOCK_WAITS`</a>](/information-schema/information-schema-data-lock-waits.md)
    -   TiDB ノードで最近発生したいくつかのデッドロック エラーをビュー: [<a href="/information-schema/information-schema-deadlocks.md">`DEADLOCKS`</a>](/information-schema/information-schema-deadlocks.md)
    -   TiDB ノード上で現在実行されているトランザクション情報をビュー: [<a href="/information-schema/information-schema-tidb-trx.md">`TIDB_TRX`</a>](/information-schema/information-schema-tidb-trx.md)

### パフォーマンス {#performance}

-   データ レプリカの古い読み取り (Experimental)

    ローカル レプリカ データを直接読み取ることで、読み取りレイテンシーを短縮し、クエリのパフォーマンスを向上させます。

    [<a href="/stale-read.md">ユーザードキュメント</a>](/stale-read.md) [<a href="https://github.com/pingcap/tidb/issues/21094">#21094</a>](https://github.com/pingcap/tidb/issues/21094)

-   デフォルトで休止状態リージョン機能を有効にします。

    リージョンが長期間非アクティブな状態にある場合、リージョンは自動的にサイレント状態に設定され、LeaderとFollowerの間のハートビート情報のシステム オーバーヘッドが削減されます。

    [<a href="/tikv-configuration-file.md#hibernate-regions">ユーザードキュメント</a>](/tikv-configuration-file.md#hibernate-regions) [<a href="https://github.com/tikv/tikv/pull/10266">#10266</a>](https://github.com/tikv/tikv/pull/10266)

### 安定性 {#stability}

-   TiCDC のレプリケーションの安定性の問題を解決する

    -   TiCDCメモリ使用量を改善して、次のシナリオで OOM を回避します。
    -   レプリケーションの中断中に 1TB を超える大量のデータが蓄積されると、再レプリケーションによって OOM の問題が発生します。
    -   大量のデータ書き込みにより、TiCDC で OOM 問題が発生します。
    -   次のシナリオで TiCDC レプリケーションが中断される可能性を減らします。

        [<a href="https://github.com/pingcap/tiflow/projects/11">プロジェクト#11</a>](https://github.com/pingcap/tiflow/projects/11)

        -   ネットワークが不安定な場合のレプリケーションの中断
        -   一部の TiKV/PD/TiCDC ノードがダウンした場合のレプリケーションの中断

-   TiFlashstorageメモリ制御

    リージョンスナップショット生成の速度とメモリ使用量を最適化し、OOM の可能性を低減します。

-   TiKV バックグラウンド タスクの書き込みレート リミッターを追加します (TiKV 書き込みレート リミッター)

    読み取りおよび書き込みリクエストの期間の安定性を確保するために、TiKV 書き込みレート リミッターは、GC やコンパクションなどの TiKV バックグラウンド タスクの書き込みトラフィックを平滑化します。 TiKV バックグラウンド タスクの書き込みレート リミッターのデフォルト値は「0MB」です。この値を、クラウド ディスクの製造元が指定する最大 I/O 帯域幅など、ディスクの最適な I/O 帯域幅に設定することをお勧めします。

    [<a href="/tikv-configuration-file.md#storageio-rate-limit">ユーザードキュメント</a>](/tikv-configuration-file.md#storageio-rate-limit) [<a href="https://github.com/tikv/tikv/issues/9156">#9156</a>](https://github.com/tikv/tikv/issues/9156)

-   複数のスケーリング タスクが同時に実行される場合のスケジュールの安定性の問題を解決する

### テレメトリー {#telemetry}

TiDB は、実行ステータスや失敗ステータスなど、TiDB クラスター リクエストの実行ステータスをテレメトリに追加します。

情報の詳細とこの動作を無効にする方法については、 [<a href="/telemetry.md">テレメトリー</a>](/telemetry.md)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   組み込み関数のサポート`VITESS_HASH()` [<a href="https://github.com/pingcap/tidb/pull/23915">#23915</a>](https://github.com/pingcap/tidb/pull/23915)
    -   `WHERE`節[<a href="https://github.com/pingcap/tidb/issues/23619">#23619</a>](https://github.com/pingcap/tidb/issues/23619)で列挙型を使用する場合のパフォーマンスを向上させるために、列挙型のデータを TiKV にプッシュダウンするサポート
    -   `RENAME USER`構文[<a href="https://github.com/pingcap/tidb/issues/23648">#23648</a>](https://github.com/pingcap/tidb/issues/23648)をサポートします。
    -   ROW_NUMBER() [<a href="https://github.com/pingcap/tidb/issues/23807">#23807</a>](https://github.com/pingcap/tidb/issues/23807)でデータをページングする際の TiDB OOM 問題を解決するために、ウィンドウ関数の計算を最適化します。
    -   `UNION ALL`を使用して多数の`SELECT`ステートメントを結合する場合の TiDB OOM 問題を解決するために`UNION ALL`の計算を最適化する[<a href="https://github.com/pingcap/tidb/issues/21441">#21441</a>](https://github.com/pingcap/tidb/issues/21441)
    -   パーティションテーブルの動的プルーニングモードを最適化して、パフォーマンスと安定性を向上させます[<a href="https://github.com/pingcap/tidb/issues/24150">#24150</a>](https://github.com/pingcap/tidb/issues/24150)
    -   複数のシナリオで発生する`Region is Unavailable`問題を修正します[<a href="https://github.com/pingcap/tidb/projects/62">プロジェクト#62</a>](https://github.com/pingcap/tidb/projects/62)
    -   頻繁なスケジュール状況で発生する可能性のある複数の`Region is Unavailable`問題を修正します
    -   一部の高ストレス書き込み状況で発生する可能性がある問題`Region is Unavailable`を修正
    -   `mysql.stats_histograms`キャッシュされた統計が最新の場合は、CPU 使用率が高くなるのを避けるためにテーブルを頻繁に読み取らないようにします[<a href="https://github.com/pingcap/tidb/pull/24317">#24317</a>](https://github.com/pingcap/tidb/pull/24317)

-   TiKV

    -   `zstd`を使用してリージョンスナップショットを圧縮し、大量のスケジュールまたはスケーリングの場合にノード間で大きなスペースの差が生じるのを防ぎます[<a href="https://github.com/tikv/tikv/pull/10005">#10005</a>](https://github.com/tikv/tikv/pull/10005)

    -   複数のケースで OOM の問題を解決する[<a href="https://github.com/tikv/tikv/issues/10183">#10183</a>](https://github.com/tikv/tikv/issues/10183)

        -   各モジュールのメモリ使用量追跡を追加する
        -   サイズ超過のRaftエントリ キャッシュによって引き起こされる OOM 問題を解決する
        -   スタックされた GC タスクによって引き起こされる OOM 問題を解決する
        -   Raftログからメモリに一度に多すぎるRaftエントリをフェッチすることによって引き起こされる OOM 問題を解決する

    -   ホットスポット書き込みがある場合にリージョンサイズの増加が分割速度を超える問題を軽減するために、リージョンをより均等に分割します[<a href="https://github.com/tikv/tikv/issues/9785">#9785</a>](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   `Union All` 、 `TopN` 、および`Limit`関数をサポート
    -   MPP モードで左外部結合およびセミアンチ結合を含むデカルト積をサポートする
    -   ロック操作を最適化して、実行中の DDL ステートメントと読み取り操作が相互にブロックされないようにする
    -   TiFlashによる期限切れデータのクリーンアップを最適化する
    -   TiFlashstorageレベルで`timestamp`列に対するクエリ フィルタのさらなるフィルタリングをサポートします。
    -   クラスター内に多数のテーブルがある場合のTiFlashの起動速度とスケーラビリティ速度を向上させます。
    -   不明な CPU で実行する場合のTiFlash の互換性を向上させる

-   PD

    -   `scatter region`スケジューラ[<a href="https://github.com/pingcap/pd/pull/3602">#3602</a>](https://github.com/pingcap/pd/pull/3602)を追加した後の予期しない統計を回避します
    -   スケーリングプロセスにおける複数のスケジュールの問題を解決する

        -   スケーリング中のスケジュールの遅さの問題を解決するために、レプリカ スナップショットの生成プロセスを最適化する[<a href="https://github.com/tikv/pd/issues/3563">#3563</a>](https://github.com/tikv/pd/issues/3563) [<a href="https://github.com/tikv/tikv/pull/10059">#10059</a>](https://github.com/tikv/tikv/pull/10059) [<a href="https://github.com/tikv/tikv/pull/10001">#10001</a>](https://github.com/tikv/tikv/pull/10001)
        -   トラフィックの変化によるハートビートの圧力によって引き起こされるスケジュールの遅さの問題を解決する[<a href="https://github.com/tikv/pd/issues/3693">#3693</a>](https://github.com/tikv/pd/issues/3693) [<a href="https://github.com/tikv/pd/issues/3739">#3739</a>](https://github.com/tikv/pd/issues/3739) [<a href="https://github.com/tikv/pd/issues/3728">#3728</a>](https://github.com/tikv/pd/issues/3728) [<a href="https://github.com/tikv/pd/issues/3751">#3751</a>](https://github.com/tikv/pd/issues/3751)
        -   スケジューリングによる大規模クラスターのスペースの不一致を削減し、スケジューリング式を最適化して、大きな圧縮率の不一致によって引き起こされるバーストの問題 (異種スペース クラスターと同様) を防止します[<a href="https://github.com/tikv/pd/issues/3592">#3592</a>](https://github.com/tikv/pd/issues/3592) [<a href="https://github.com/tikv/tikv/pull/10005">#10005</a>](https://github.com/tikv/tikv/pull/10005)

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマ[<a href="https://github.com/pingcap/br/pull/1143">#1143</a>](https://github.com/pingcap/br/pull/1143) [<a href="https://github.com/pingcap/br/pull/1078">#1078</a>](https://github.com/pingcap/br/pull/1078)でのシステム テーブルのバックアップと復元のサポート
        -   仮想ホスト アドレッシング モード[<a href="https://github.com/tikv/tikv/pull/10243">#10243</a>](https://github.com/tikv/tikv/pull/10243)に基づく S3 互換storageをサポートします。
        -   メモリ使用量を削減するためにバックアップメタの形式を最適化します[<a href="https://github.com/pingcap/br/pull/1171">#1171</a>](https://github.com/pingcap/br/pull/1171)

    -   TiCDC

        -   一部のログ メッセージの説明を改善して、より明確になり、問題の診断にさらに役立つようにしました[<a href="https://github.com/pingcap/tiflow/pull/1759">#1759</a>](https://github.com/pingcap/tiflow/pull/1759)
        -   バック プレッシャー機能をサポートして、TiCDC スキャン速度がダウンストリームの処理能力を感知できるようにします[<a href="https://github.com/tikv/tikv/pull/10151">#10151</a>](https://github.com/tikv/tikv/pull/10151)
        -   TiCDC が初期スキャンを実行するときのメモリ使用量を削減します[<a href="https://github.com/tikv/tikv/pull/10133">#10133</a>](https://github.com/tikv/tikv/pull/10133)
        -   悲観的トランザクション[<a href="https://github.com/tikv/tikv/pull/10089">#10089</a>](https://github.com/tikv/tikv/pull/10089)における TiCDC Old Value のキャッシュ ヒット率を改善します。

    -   Dumpling

        -   TiDB のメモリ不足 (OOM) を回避するために、TiDB v4.0 からデータをエクスポートするロジックを改善しました[<a href="https://github.com/pingcap/dumpling/pull/273">#273</a>](https://github.com/pingcap/dumpling/pull/273)

        -   バックアップ失敗時にエラーが出力されない問題を修正[<a href="https://github.com/pingcap/dumpling/pull/280">#280</a>](https://github.com/pingcap/dumpling/pull/280)

    -   TiDB Lightning

        -   データのインポート速度を向上させます。最適化の結果は、TPC-C データのインポート速度が 30% 向上し、より多くのインデックス (5 つのインデックス) を持つ大きなテーブル (2TB 以上) のインポート速度が 50% 以上向上したことを示しています。 [<a href="https://github.com/pingcap/br/pull/753">#753</a>](https://github.com/pingcap/br/pull/753)
        -   インポートするデータとインポート前にターゲット クラスターに事前チェックを追加し、インポート要件を満たさない場合はインポート プロセスを拒否するエラーを報告します[<a href="https://github.com/pingcap/br/pull/999">#999</a>](https://github.com/pingcap/br/pull/999)
        -   ローカル バックエンドでのチェックポイント更新のタイミングを最適化し、ブレークポイント[<a href="https://github.com/pingcap/br/pull/1080">#1080</a>](https://github.com/pingcap/br/pull/1080)からの再起動のパフォーマンスを向上させます。

## バグの修正 {#bug-fixes}

-   TiDB

    -   投影結果が空の場合、プロジェクトの削除の実行結果が正しくない場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/23887">#23887</a>](https://github.com/pingcap/tidb/issues/23887)
    -   列に`NULL`値が含まれる場合に、場合によっては間違ったクエリ結果が表示される問題を修正します[<a href="https://github.com/pingcap/tidb/issues/23891">#23891</a>](https://github.com/pingcap/tidb/issues/23891)
    -   スキャンに仮想列が含まれる場合、MPP プランの生成を禁止する[<a href="https://github.com/pingcap/tidb/issues/23886">#23886</a>](https://github.com/pingcap/tidb/issues/23886)
    -   プラン キャッシュ[<a href="https://github.com/pingcap/tidb/issues/23187">#23187</a>](https://github.com/pingcap/tidb/issues/23187) [<a href="https://github.com/pingcap/tidb/issues/23144">#23144</a>](https://github.com/pingcap/tidb/issues/23144) [<a href="https://github.com/pingcap/tidb/issues/23304">#23304</a>](https://github.com/pingcap/tidb/issues/23304) [<a href="https://github.com/pingcap/tidb/issues/23290">#23290</a>](https://github.com/pingcap/tidb/issues/23290)の`PointGet`と`TableDual`の誤った再利用を修正
    -   オプティマイザーがクラスター化インデックス`IndexMerge`のプランを構築するときに発生するエラーを修正します[<a href="https://github.com/pingcap/tidb/issues/23906">#23906</a>](https://github.com/pingcap/tidb/issues/23906)
    -   BIT 型エラーの型推論を修正[<a href="https://github.com/pingcap/tidb/issues/23832">#23832</a>](https://github.com/pingcap/tidb/issues/23832)
    -   `PointGet`演算子が存在する場合、一部のオプティマイザ ヒントが有効にならない問題を修正[<a href="https://github.com/pingcap/tidb/issues/23570">#23570</a>](https://github.com/pingcap/tidb/issues/23570)
    -   ロールバック時にエラー[<a href="https://github.com/pingcap/tidb/issues/23893">#23893</a>](https://github.com/pingcap/tidb/issues/23893)が原因で DDL 操作が失敗する可能性がある問題を修正します。
    -   バイナリリテラル定数のインデックス範囲が正しく構築されない問題を修正[<a href="https://github.com/pingcap/tidb/issues/23672">#23672</a>](https://github.com/pingcap/tidb/issues/23672)
    -   場合によっては`IN`節の誤った結果が生じる可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/23889">#23889</a>](https://github.com/pingcap/tidb/issues/23889)
    -   一部の文字列関数の間違った結果を修正[<a href="https://github.com/pingcap/tidb/issues/23759">#23759</a>](https://github.com/pingcap/tidb/issues/23759)
    -   ユーザーが`REPLACE`操作を実行するには、テーブルに対する`INSERT`と`DELETE`両方の権限が必要になる[<a href="https://github.com/pingcap/tidb/issues/23909">#23909</a>](https://github.com/pingcap/tidb/issues/23909)
    -   ユーザーが`REPLACE`操作を実行するには、テーブルに対する`INSERT`と`DELETE`両方の権限が必要になる[<a href="https://github.com/pingcap/tidb/pull/24070">#24070</a>](https://github.com/pingcap/tidb/pull/24070)
    -   バイナリとバイト[<a href="https://github.com/pingcap/tidb/issues/23846">#23846</a>](https://github.com/pingcap/tidb/issues/23846)の誤った比較によって引き起こされる間違った`TableDual`プランを修正します。
    -   場合によってはプレフィックスインデックスとインデックスジョインの使用によって引き起こされるpanicの問題を修正[<a href="https://github.com/pingcap/tidb/issues/24547">#24547</a>](https://github.com/pingcap/tidb/issues/24547) [<a href="https://github.com/pingcap/tidb/issues/24716">#24716</a>](https://github.com/pingcap/tidb/issues/24716) [<a href="https://github.com/pingcap/tidb/issues/24717">#24717</a>](https://github.com/pingcap/tidb/issues/24717)
    -   準備されたプラン キャッシュ`point get`がトランザクション[<a href="https://github.com/pingcap/tidb/issues/24741">#24741</a>](https://github.com/pingcap/tidb/issues/24741)の`point get`ステートメントによって誤って使用される問題を修正します。
    -   照合順序が`ascii_bin`または`latin1_bin` [<a href="https://github.com/pingcap/tidb/issues/24569">#24569</a>](https://github.com/pingcap/tidb/issues/24569)場合に、間違ったプレフィックス インデックス値が書き込まれる問題を修正します。
    -   進行中のトランザクションが GC ワーカーによって中断される可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/24591">#24591</a>](https://github.com/pingcap/tidb/issues/24591)
    -   `new-collation`が有効で`new-row-format`が無効な場合、クラスター化インデックスでポイント クエリが誤る可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/24541">#24541</a>](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフル ハッシュ結合[<a href="https://github.com/pingcap/tidb/pull/24490">#24490</a>](https://github.com/pingcap/tidb/pull/24490)パーティション キーの変換をリファクタリングします。
    -   `HAVING`節[<a href="https://github.com/pingcap/tidb/issues/24045">#24045</a>](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプランを構築するときに発生するpanicの問題を修正します。
    -   列枝刈りの改善により`Apply`と`Join`演算子の結果がおかしくなる問題を修正[<a href="https://github.com/pingcap/tidb/issues/23887">#23887</a>](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリロックが解決できないバグを修正[<a href="https://github.com/pingcap/tidb/issues/24384">#24384</a>](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketch レコードの重複を引き起こす可能性がある統計の GC 問題を修正[<a href="https://github.com/pingcap/tidb/pull/24357">#24357</a>](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的的ロックが`ErrKeyExists`エラー[<a href="https://github.com/pingcap/tidb/issues/23799">#23799</a>](https://github.com/pingcap/tidb/issues/23799)を受け取った場合、不必要な悲観的的ロールバックを回避します。
    -   sql_mode に`ANSI_QUOTES` [<a href="https://github.com/pingcap/tidb/issues/24429">#24429</a>](https://github.com/pingcap/tidb/issues/24429)が含まれる場合、数値リテラルが認識されない問題を修正
    -   `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`のようなステートメントによる、リストされていないパーティションからのデータの読み取りを禁止します[<a href="https://github.com/pingcap/tidb/issues/24746">#24746</a>](https://github.com/pingcap/tidb/issues/24746)
    -   SQL ステートメントに`GROUP BY`と`UNION`両方が含まれる場合に発生する可能性のある`index out of range`エラーを修正[<a href="https://github.com/pingcap/tidb/issues/24281">#24281</a>](https://github.com/pingcap/tidb/issues/24281)
    -   `CONCAT`関数が照合順序[<a href="https://github.com/pingcap/tidb/issues/24296">#24296</a>](https://github.com/pingcap/tidb/issues/24296)を正しく処理しない問題を修正します。
    -   `collation_server`グローバル変数が新しいセッション[<a href="https://github.com/pingcap/tidb/pull/24156">#24156</a>](https://github.com/pingcap/tidb/pull/24156)で有効にならない問題を修正します。

-   TiKV

    -   コプロセッサが`IN`式[<a href="https://github.com/tikv/tikv/issues/9821">#9821</a>](https://github.com/tikv/tikv/issues/9821)の符号付き整数型または符号なし整数型を適切に処理できない問題を修正します。
    -   SST ファイルのバッチ取り込み後に多数の空のリージョンが発生する問題を修正[<a href="https://github.com/pingcap/br/issues/964">#964</a>](https://github.com/pingcap/br/issues/964)
    -   ファイル辞書ファイルが破損するとTiKVが起動できなくなるバグを修正[<a href="https://github.com/tikv/tikv/issues/9886">#9886</a>](https://github.com/tikv/tikv/issues/9886)
    -   古い値の読み取りによって発生する TiCDC OOM 問題を修正[<a href="https://github.com/tikv/tikv/issues/9996">#9996</a>](https://github.com/tikv/tikv/issues/9996) [<a href="https://github.com/tikv/tikv/issues/9981">#9981</a>](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin` [<a href="https://github.com/pingcap/tidb/issues/24548">#24548</a>](https://github.com/pingcap/tidb/issues/24548)の場合に、クラスター化された主キー列のセカンダリ インデックスに空の値が表示される問題を修正します。
    -   `abort-on-panic`構成を追加します。これにより、panic発生時に TiKV がコア ダンプ ファイルを生成できるようになります。ユーザーは、コア ダンプ[<a href="https://github.com/tikv/tikv/pull/10216">#10216</a>](https://github.com/tikv/tikv/pull/10216)を有効にするために環境を正しく構成する必要があります。
    -   TiKV がビジーでないときに発生する`point get`クエリのパフォーマンス低下の問題を修正します[<a href="https://github.com/tikv/tikv/issues/10046">#10046</a>](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合、PDLeaderの再選出が遅い問題を修正[<a href="https://github.com/tikv/pd/issues/3697">#3697</a>](https://github.com/tikv/pd/issues/3697)

    -   存在しないストア[<a href="https://github.com/tikv/pd/issues/3660">#3660</a>](https://github.com/tikv/pd/issues/3660)からエビクト リーダー スケジューラを削除するときに発生するpanicの問題を修正します。

    -   オフラインピアのマージ後に統計が更新されない問題を修正[<a href="https://github.com/tikv/pd/issues/3611">#3611</a>](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   時間型を整数型にキャストするときに誤った結果が表示される問題を修正
    -   `receiver`が10秒以内に対応するタスクを見つけられないバグを修正
    -   `cancelMPPQuery`に無効な反復子が存在する可能性がある問題を修正
    -   `bitwise`オペレーターの挙動がTiDBと異なるバグを修正
    -   `prefix key`を使用するときに範囲が重複することによって引き起こされるアラートの問題を修正します。
    -   文字列型を整数型にキャストするときに誤った結果が発生する問題を修正
    -   連続した高速書き込みによりTiFlash がメモリ不足になる可能性がある問題を修正
    -   テーブル GC 中に null ポインターの例外が発生する可能性がある潜在的な問題を修正
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanic問題を修正
    -   BR復元中にTiFlash がpanicになる可能性がある問題を修正
    -   共有デルタインデックスを同時にクローン作成するときに誤った結果が発生する問題を修正
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるpanicを修正しました。
    -   TiFlash が非同期コミットからフォールバックしたロックを解決できない問題を修正
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれる場合に誤った結果が返される問題を修正
    -   セグメント分割中に発生するTiFlashpanic問題を修正

-   ツール

    -   TiDB Lightning

        -   KV データ[<a href="https://github.com/pingcap/br/pull/1127">#1127</a>](https://github.com/pingcap/br/pull/1127)の生成時に発生するTiDB Lightningpanicの問題を修正
        -   データインポート時に合計キーサイズがraftエントリ制限を超えたためバッチ分割リージョンが失敗するバグを修正[<a href="https://github.com/pingcap/br/issues/969">#969</a>](https://github.com/pingcap/br/issues/969)
        -   CSV ファイルをインポートするときに、ファイルの最終行に改行文字 ( `\r\n` ) が含まれていない場合、エラーが報告される問題を修正します[<a href="https://github.com/pingcap/br/issues/1133">#1133</a>](https://github.com/pingcap/br/issues/1133)
        -   インポートするテーブルにdouble型のオートインクリメントカラムが含まれる場合、auto_incrementの値が異常[<a href="https://github.com/pingcap/br/pull/1178">#1178</a>](https://github.com/pingcap/br/pull/1178)になる問題を修正

    -   バックアップと復元 (BR)
        -   いくつかの TiKV ノードの障害によって引き起こされるバックアップ中断の問題を修正します[<a href="https://github.com/pingcap/br/issues/980">#980</a>](https://github.com/pingcap/br/issues/980)

    -   TiCDC

        -   統合ソーターの同時実行の問題を修正し、役に立たないエラー メッセージをフィルタリングします[<a href="https://github.com/pingcap/tiflow/pull/1678">#1678</a>](https://github.com/pingcap/tiflow/pull/1678)
        -   冗長ディレクトリの作成により MinIO [<a href="https://github.com/pingcap/tiflow/issues/1463">#1463</a>](https://github.com/pingcap/tiflow/issues/1463)でのレプリケーションが中断される可能性があるバグを修正
        -   `explicit_defaults_for_timestamp`セッション変数のデフォルト値を ON に設定して、 MySQL 5.7ダウンストリームがアップストリームの TiDB [<a href="https://github.com/pingcap/tiflow/issues/1585">#1585</a>](https://github.com/pingcap/tiflow/issues/1585)と同じ動作を維持できるようにします。
        -   `io.EOF`の処理を誤るとレプリケーションが中断される可能性がある問題を修正[<a href="https://github.com/pingcap/tiflow/issues/1633">#1633</a>](https://github.com/pingcap/tiflow/issues/1633)
        -   TiCDC ダッシュボード[<a href="https://github.com/pingcap/tiflow/pull/1645">#1645</a>](https://github.com/pingcap/tiflow/pull/1645)で TiKV CDC エンドポイントの CPU メトリックを修正します。
        -   場合によってはレプリケーションのブロックを避けるために`defaultBufferChanSize`を増やします[<a href="https://github.com/pingcap/tiflow/issues/1259">#1259</a>](https://github.com/pingcap/tiflow/issues/1259)
        -   Avro 出力[<a href="https://github.com/pingcap/tiflow/pull/1712">#1712</a>](https://github.com/pingcap/tiflow/pull/1712)でタイムゾーン情報が失われる問題を修正
        -   統合ソーターでの古い一時ファイルのクリーンアップをサポートし、ディレクトリ`sort-dir`の共有を禁止します[<a href="https://github.com/pingcap/tiflow/pull/1742">#1742</a>](https://github.com/pingcap/tiflow/pull/1742)
        -   古いリージョンが多数存在する場合に発生する KV クライアントのデッドロック バグを修正[<a href="https://github.com/pingcap/tiflow/issues/1599">#1599</a>](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[<a href="https://github.com/pingcap/tiflow/pull/1697">#1697</a>](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正
        -   データを MySQL [<a href="https://github.com/pingcap/tiflow/pull/1750">#1750</a>](https://github.com/pingcap/tiflow/pull/1750)にレプリケートするときに SUPER 権限が必要となる`explicit_defaults_for_timestamp`の更新を元に戻します。
        -   シンク フロー制御をサポートしてメモリオーバーフローのリスクを軽減します[<a href="https://github.com/pingcap/tiflow/pull/1840">#1840</a>](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブル[<a href="https://github.com/pingcap/tiflow/pull/1828">#1828</a>](https://github.com/pingcap/tiflow/pull/1828)の移動時にレプリケーションタスクが停止する場合があるバグを修正
        -   TiCDC チェンジフィード チェックポイント[<a href="https://github.com/pingcap/tiflow/pull/1759">#1759</a>](https://github.com/pingcap/tiflow/pull/1759)の停滞により TiKV GC セーフ ポイントがブロックされる問題を修正
