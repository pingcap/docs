---
title: TiDB 5.2 Release Notes
---

# TiDB 5.2 リリースノート {#tidb-5-2-release-notes}

発売日：2021年8月27日

TiDB バージョン: 5.2.0

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 5.2.x バージョンを使用することをお勧めします。

v5.2 の主な新機能と改善点は次のとおりです。

-   クエリのパフォーマンスを大幅に向上させるために、式インデックスで複数の関数を使用するサポート
-   オプティマイザーのカーディナリティ推定の精度を向上させて、最適な実行計画を選択できるようにします
-   トランザクション ロック イベントを監視し、デッドロックの問題をトラブルシューティングするための Lock ビュー機能の一般提供 (GA) を発表
-   TiFlash のI/O トラフィック制限機能を追加して、 TiFlashの読み取りと書き込みの安定性を向上させます
-   TiKV は、以前の RocksDB 書き込みストール メカニズムを置き換える新しいフロー制御メカニズムを導入して、TiKV フロー制御の安定性を向上させます。
-   データ移行 (DM) の運用と保守を簡素化し、管理コストを削減します。
-   TiCDC は、HTTP プロトコル OpenAPI をサポートして、TiCDC タスクを管理します。 Kubernetes とオンプレミス環境の両方で、よりユーザー フレンドリーな操作方法を提供します。 (Experimental機能)

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v5.2 にアップグレードする場合、すべての中間バージョンの互換性の変更点を知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                       | タイプを変更 | 説明                                                                         |
| :-------------------------------------------------------------------------------------------------------- | :----- | :------------------------------------------------------------------------- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                     | 新規追加   | サーバーがアドバタイズする認証方法を設定します。デフォルト値は`mysql_native_password`です。                  |
| [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) | 新規追加   | 生成された列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定します。デフォルト値は`OFF`です。    |
| [`tidb_opt_enable_correlation_adjustment`](/system-variables.md#tidb_opt_enable_correlation_adjustment)   | 新規追加   | オプティマイザーが列の順序の相関に基づいて行数を見積もるかどうかを制御します。デフォルト値は`ON`です。                      |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold)           | 新規追加   | Limit オペレーターまたは TopN オペレーターを TiKV まで下げるかどうかを決定するしきい値を設定します。デフォルト値は`100`です。 |
| [`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40)    | 修正済み   | ステートメント サマリー テーブルがメモリに格納するステートメントの最大数を設定します。デフォルト値が`200`から`3000`に変更されました。  |
| `tidb_enable_streaming`                                                                                   | 非推奨    | システム変数`enable-streaming`は非推奨であり、今後使用することはお勧めしません。                          |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                                                  | タイプを変更 | 説明                                                                                                                                |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------- |
| TiDB 構成ファイル    | [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable)        | 新規追加   | [`INFORMATION\_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロック エラー メッセージを収集するかどうかを制御します。 |
| TiDB 構成ファイル    | [`security.auto-tls`](/tidb-configuration-file.md#auto-tls)                                                                   | 新規追加   | 起動時に TLS 証明書を自動的に生成するかどうかを決定します。デフォルト値は`false`です。                                                                                 |
| TiDB 構成ファイル    | `stmt-summary.max-stmt-count`                                                                                                 | 修正済み   | ステートメント要約テーブルに保管できる SQL カテゴリーの最大数を示します。デフォルト値が`200`から`3000`に変更されました。                                                              |
| TiDB 構成ファイル    | `experimental.allow-expression-index`                                                                                         | 非推奨    | TiDB 構成ファイルの`allow-expression-index`構成は非推奨です。                                                                                     |
| TiKV 構成ファイル    | [`raftstore.cmd-batch`](/tikv-configuration-file.md#cmd-batch)                                                                | 新規追加   | リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。デフォルト値は`true`です。                                                          |
| TiKV 構成ファイル    | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                  | 新規追加   | 一定の間隔で、TiKV はRaftstoreコンポーネントのレイテンシーを検査します。この構成項目は、検査の間隔を指定します。レイテンシーがこの値を超えると、この検査はタイムアウトとしてマークされます。デフォルト値は`500ms`です。            |
| TiKV 構成ファイル    | [`raftstore.max-peer-down-duration`](/tikv-configuration-file.md#max-peer-down-duration)                                      | 修正済み   | ピアに許可される最長の非アクティブ期間を示します。タイムアウトのあるピアは`down`としてマークされ、PD は後でそれを削除しようとします。デフォルト値が`5m`から`10m`に変更されました。                                |
| TiKV 構成ファイル    | [`server.raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                                         | 新規追加   | TiKV のRaftメッセージのキュー サイズを指定します。デフォルト値は`8192`です。                                                                                    |
| TiKV 構成ファイル    | [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)                                                           | 新規追加   | フロー制御メカニズムを有効にするかどうかを決定します。デフォルト値は`true`です。                                                                                       |
| TiKV 構成ファイル    | [`storage.flow-control.memtables-threshold`](/tikv-configuration-file.md#memtables-threshold)                                 | 新規追加   | kvDB memtables の数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。デフォルト値は`5`です。                                                                    |
| TiKV 構成ファイル    | [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                   | 新規追加   | kvDB L0 ファイルの数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。デフォルト値は`9`です。                                                                       |
| TiKV 構成ファイル    | [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 新規追加   | KvDB の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始め、 `ServerIsBusy`エラーを報告します。初期値は「192GB」です。                                    |
| TiKV 構成ファイル    | [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit) | 新規追加   | KvDB の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`エラーを報告します。デフォルト値は「1024GB」です。                                 |

### その他 {#others}

-   アップグレードの前に、システム変数[`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40)の値が`ON`かどうかを確認します。値が`ON`の場合は`OFF`に設定します。そうしないと、アップグレードは失敗します。
-   v4.0 から v5.2 にアップグレードされた TiDB クラスターの場合、デフォルト値の[`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)が`WARN`から`OFF`に変更されます。
-   アップグレードの前に、TiDB 構成の値を確認してください[`feedback-probability`](https://docs.pingcap.com/tidb/v5.2/tidb-configuration-file#feedback-probability) 。値が`0`でない場合、アップグレード後に「回復可能なゴルーチンでpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDB は現在、 MySQL 5.7の noop 変数`innodb_default_row_format`と互換性があります。この変数を設定しても効果はありません。 [#23541](https://github.com/pingcap/tidb/issues/23541)
-   TiDB 5.2 以降では、システムのセキュリティを向上させるために、クライアントからの接続のトランスポートレイヤーを暗号化することが推奨されています (必須ではありません)。 TiDB は、TiDB での暗号化を自動的に構成して有効にする Auto TLS 機能を提供します。自動 TLS 機能を使用するには、TiDB をアップグレードする前に、TiDB 構成ファイルで[`security.auto-tls`](/tidb-configuration-file.md#auto-tls) `true`に設定します。
-   MySQL 8.0 からの移行を容易にし、セキュリティを向上させるために、 `caching_sha2_password`認証方法をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   **式インデックスでの複数の関数の使用をサポート**

    式インデックスは、式で作成できる特別なインデックスの一種です。式インデックスが作成されると、TiDB は式ベースのクエリをサポートするため、クエリのパフォーマンスが大幅に向上します。

    [ユーザー文書](/sql-statements/sql-statement-create-index.md) 、 [#25150](https://github.com/pingcap/tidb/issues/25150)

-   **Oracle の`translate`機能をサポート**

    `translate`関数は、文字列内のすべての文字を他の文字に置き換えます。 TiDB では、この関数は Oracle のように空の文字列を`NULL`として扱いません。

    [ユーザー文書](/functions-and-operators/string-functions.md)

-   **スピル HashAgg のサポート**

    ディスクへの HashAgg のスピルをサポートします。 HashAgg 演算子を含む SQL ステートメントによってメモリ不足 (OOM) が発生した場合、この演算子の同時実行数を`1`に設定して、ディスク スピルをトリガーすることを試みることができます。これにより、メモリストレスが軽減されます。

    [ユーザー文書](/configure-memory-usage.md#other-memory-control-behaviors-of-tidb-server) 、 [#25882](https://github.com/pingcap/tidb/issues/25882)

-   **オプティマイザーのカーディナリティ推定の精度を向上させる**

    -   TiDB の TopN/Limit の推定の精度を向上させます。たとえば、 `order by col limit x`条件を含む大きなテーブルでのページネーション クエリの場合、TiDB は適切なインデックスをより簡単に選択し、クエリの応答時間を短縮できます。
    -   範囲外推定の精度を向上させます。たとえば、1 日の統計が更新されていない場合でも、TiDB は`where date=Now()`を含むクエリの対応するインデックスを正確に選択できます。
    -   Limit/TopN を押し下げるオプティマイザーの動作を制御する`tidb_opt_limit_push_down_threshold`変数を導入します。これにより、状況によっては、誤った見積もりが原因で Limit/TopN を押し下げることができないという問題が解決されます。

    [ユーザー文書](/system-variables.md#tidb_opt_limit_push_down_threshold) 、 [#26085](https://github.com/pingcap/tidb/issues/26085)

-   **オプティマイザのインデックス選択を改善する**

    インデックス選択のプルーニング ルールを追加します。比較のために統計を使用する前に、TiDB はこれらのルールを使用して、選択可能なインデックスの範囲を絞り込みます。これにより、最適でないインデックスが選択される可能性が減少します。

    [ユーザー文書](/choose-index.md)

### トランザクション {#transaction}

-   **Lock ビューの一般提供 (GA)**

    ロックビュー機能は、悲観的ロックのロック競合とロック待機に関する詳細情報を提供します。これは、DBA がトランザクション ロック イベントを観察し、デッドロックの問題をトラブルシューティングするのに役立ちます。

    v5.2 では、Lock ビューに対して次の機能強化が行われました。

    -   ロック ビュー関連のテーブルの SQL ダイジェスト列に加えて、対応する正規化された SQL テキストを示す列をこれらのテーブルに追加します。 SQL ダイジェストに対応するステートメントを手動でクエリする必要はありません。
    -   `TIDB_DECODE_SQL_DIGESTS`関数を追加して、クラスター内の一連の SQL ダイジェストに対応する正規化された SQL ステートメント (形式と引数のないフォーム) を照会します。これにより、トランザクションによって過去に実行されたステートメントを照会する操作が簡素化されます。
    -   `DATA_LOCK_WAITS`および`DEADLOCKS`システム テーブルに列を追加して、キーから解釈されたテーブル名、行 ID、インデックス値、およびその他のキー情報を表示します。これにより、キーが属するテーブルの検索やキー情報の解釈などの操作が簡素化されます。
    -   `DEADLOCKS`のテーブルでリトライ可能なデッドロック エラーの情報を収集できるようになりました。これにより、このようなエラーによって引き起こされる問題のトラブルシューティングが容易になります。エラー収集はデフォルトで無効になっており、 `pessimistic-txn.deadlock-history-collect-retryable`構成を使用して有効にすることができます。
    -   `TIDB_TRX`システム テーブルで、クエリ実行トランザクションとアイドル トランザクションの区別をサポートします。第`Normal`状態は現在、 `Running`と`Idle`状態に分割されています。

    ユーザー ドキュメント:

    -   クラスター内のすべての TiKV ノードで発生している悲観的ロック待機イベントをビュー。 [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDB ノードで最近発生したデッドロック エラーをビュー: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDB ノードで実行中のトランザクションをビュー: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

-   `AUTO_RANDOM`または`SHARD_ROW_ID_BITS`属性を持つテーブルにインデックスを追加するユーザー シナリオを最適化します。

### 安定性 {#stability}

-   **TiFlash I/O トラフィック制限を追加**

    この新機能は、ディスク帯域幅が小さく特定のサイズのクラウドstorageに適しています。デフォルトでは無効になっています。

    TiFlash I/O Rate Limiter は、読み取りタスクと書き込みタスク間の I/O リソースの過剰な競合を回避する新しいメカニズムを提供します。読み取りタスクと書き込みタスクへの応答のバランスを取り、読み取り/書き込みワークロードに従ってレートを自動的に制限します。

    [ユーザー文書](/tiflash/tiflash-configuration.md)

-   **TiKVフロー制御の安定性向上**

    TiKV は、以前の RocksDB 書き込みストール メカニズムに代わる新しいフロー制御メカニズムを導入しています。書き込みストール メカニズムと比較して、この新しいメカニズムは、フォアグラウンド書き込みの安定性への影響を軽減します。

    具体的には、RocksDB コンパクションのストレスが蓄積されると、次の問題を回避するために、RocksDBレイヤーではなく TiKV スケジューラーレイヤーでフロー制御が実行されます。

    -   Raftstoreがスタックします。これは、RocksDB の書き込みストールが原因です。
    -   Raft選出がタイムアウトになり、結果としてノード リーダーが転送されます。

    この新しいメカニズムにより、フロー制御アルゴリズムが改善され、書き込みトラフィックが多い場合の QPS の低下が軽減されます。

    [ユーザー文書](/tikv-configuration-file.md#storageflow-control) 、 [#10137](https://github.com/tikv/tikv/issues/10137)

-   **クラスター内の単一の遅い TiKV ノードによって引き起こされた影響を自動的に検出して回復します**

    TiKV では、低速ノード検出メカニズムが導入されています。このメカニズムは、TiKV Raftstoreのレートを検査してスコアを計算し、ストア ハートビートを通じて PD にスコアを報告します。一方、PD に`evict-slow-store-scheduler`スケジューラーを追加して、単一の低速 TiKV ノードのリーダーを自動的に削除します。このようにして、クラスター全体への影響が軽減されます。同時に、遅いノードに関するより多くのアラート項目が導入され、問題を迅速に特定して解決するのに役立ちます。

    [ユーザー文書](/tikv-configuration-file.md#inspect-interval) 、 [#10539](https://github.com/tikv/tikv/issues/10539)

### データ移行 {#data-migration}

-   **データ移行 (DM) の操作を簡素化**

    DM v2.0.6 は、VIP を使用してデータ ソースの変更イベント (フェイルオーバーまたはプランの変更) を自動的に識別し、新しいデータ ソース インスタンスに自動的に接続して、データ レプリケーションのレイテンシーを短縮し、操作手順を簡素化できます。

-   TiDB Lightning は、 CSV データでカスタマイズされた行末記号をサポートし、MySQL LOAD DATA CSV データ形式と互換性があります。その後、 TiDB Lightning をデータ フローアーキテクチャで直接使用できます。

    [#1297](https://github.com/pingcap/br/pull/1297)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

TiCDC は、HTTP プロトコル (OpenAPI) を使用して TiCDC タスクを管理することをサポートしています。これは、Kubernetes とオンプレミス環境の両方にとってよりユーザーフレンドリーな操作方法です。 (Experimental機能)

[#2411](https://github.com/pingcap/tiflow/issues/2411)

### 展開と運用 {#deployment-and-operations}

Apple M1 チップを搭載した Mac コンピュータでの`tiup playground`コマンドの実行をサポートします。

## 機能強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   TiDB 用に設計されたバイナリ MQ 形式を追加します。 JSON [#1621](https://github.com/pingcap/tiflow/pull/1621)に基づくオープン プロトコルよりもコンパクトです。
        -   ファイル ソーター[#2114](https://github.com/pingcap/tiflow/pull/2114)のサポートを削除
        -   ログ ローテーション構成のサポート[#2182](https://github.com/pingcap/tiflow/pull/2182)

    -   TiDB Lightning

        -   カスタマイズされたライン ターミネータをサポート ( `\r`と`\n`を除く) [#1297](https://github.com/pingcap/br/pull/1297)
        -   式インデックスと仮想生成列に依存するインデックスをサポート[#1407](https://github.com/pingcap/br/pull/1407)

    -   Dumpling

        -   MySQL 互換データベースのバックアップをサポートしますが、 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE` [#311](https://github.com/pingcap/dumpling/pull/311)はサポートしません

## 改良点 {#improvements}

-   TiDB

    -   組み込み関数`json_unquote()`を TiKV [#24415](https://github.com/pingcap/tidb/issues/24415)にプッシュ ダウンするサポート
    -   デュアル テーブル[#25614](https://github.com/pingcap/tidb/pull/25614)からの`union`ブランチの削除をサポート
    -   集計演算子のコスト ファクター[#25241](https://github.com/pingcap/tidb/pull/25241)を最適化する
    -   MPP 外部結合が、テーブルの行数[#25142](https://github.com/pingcap/tidb/pull/25142)に基づいて構築テーブルを選択できるようにします。
    -   リージョン[#24724](https://github.com/pingcap/tidb/pull/24724)に基づく異なるTiFlashノード間での MPP クエリ ワークロードのバランス調整をサポート
    -   MPP クエリ実行後のキャッシュ内の古いリージョンの無効化をサポート[#24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子の組み込み関数`str_to_date`の MySQL 互換性を向上させる`%b/%M/%r/%T` [#25767](https://github.com/pingcap/tidb/pull/25767)
    -   同じクエリに対して異なるバインディングを再作成した後、複数の TiDB で一貫性のないバインディング キャッシュが作成される可能性がある問題を修正します[#26015](https://github.com/pingcap/tidb/pull/26015)
    -   アップグレード後に既存のバインディングをキャッシュにロードできない問題を修正します[#23295](https://github.com/pingcap/tidb/pull/23295)
    -   ( `original_sql` , `update_time` ) [#26139](https://github.com/pingcap/tidb/pull/26139)による`SHOW BINDINGS`の結果の順序付けをサポート
    -   バインディングが存在する場合のクエリ最適化のロジックを改善し、クエリの最適化時間を短縮します[#26141](https://github.com/pingcap/tidb/pull/26141)
    -   「削除済み」ステータスのバインディングのガベージコレクションの自動完了をサポート[#26206](https://github.com/pingcap/tidb/pull/26206)
    -   `EXPLAIN VERBOSE` [#26930](https://github.com/pingcap/tidb/pull/26930)の結果でバインディングがクエリの最適化に使用されているかどうかを示すサポート
    -   新しいステータス バリエーション`last_plan_binding_update_time`を追加して、現在の TiDB インスタンスのバインディング キャッシュに対応するタイムスタンプを表示します[#26340](https://github.com/pingcap/tidb/pull/26340)
    -   他の機能に影響を与えるベースラインの進化 (オンプレミスの TiDB バージョンでは現在、実験的`admin evolve bindings`であるため無効になっています) を禁止するために、バインディングの進化の開始時または実行時のエラー報告をサポートします[#26333](https://github.com/pingcap/tidb/pull/26333)

-   PD

    -   ホットリージョンスケジューリング用の QPS ディメンションを追加し、スケジューリングの優先順位の調整をサポートします[#3869](https://github.com/tikv/pd/issues/3869)
    -   TiFlash [#3900](https://github.com/tikv/pd/pull/3900)の書き込みホットスポットのホットリージョンバランス スケジューリングをサポート

-   TiFlash

    -   演算子の追加: `MOD / %` 、 `LIKE`
    -   文字列関数の追加: `ASCII()` 、 `COALESCE()` 、 `LENGTH()` 、 `POSITION()` 、 `TRIM()`
    -   数学関数の追加: `CONV()` 、 `CRC32()` 、 `DEGREES()` 、 `EXP()` 、 `LN()` 、 `LOG()` 、 `LOG10()` 、 `LOG2()` 、 `POW()` 、 `RADIANS()` 、 `ROUND(decimal)` 、 `SIN()` 、 `MOD()`
    -   日付関数の追加: `ADDDATE(string, real)` 、 `DATE_ADD(string, real)` 、 `DATE()`
    -   他の関数を追加: `INET_NTOA()` , `INET_ATON()` , `INET6_ATON` , `INET6_NTOA()`
    -   新しい照合順序が有効な場合、MPP モードで Shuffled Hash Join 計算と Shuffled Hash 集計計算をサポートします。
    -   基本的なコードを最適化して MPP のパフォーマンスを向上させる
    -   `STRING`型から`DOUBLE`型へのキャスト対応
    -   複数のスレッドを使用して、右外部結合で結合されていないデータを最適化する
    -   MPP クエリで古いリージョンを自動的に無効にするサポート

-   ツール

    -   TiCDC

        -   kv クライアント[#1899](https://github.com/pingcap/tiflow/pull/1899)のインクリメンタル スキャンに同時実行制限を追加します。
        -   TiCDC は常に古い値を内部でプルできます[#2271](https://github.com/pingcap/tiflow/pull/2271)
        -   回復不能な DML エラーが発生すると、TiCDC が失敗し、すぐに終了することがある[#1928](https://github.com/pingcap/tiflow/pull/1928)
        -   `resolve lock`リージョンが初期化された直後に実行することはできません[#2235](https://github.com/pingcap/tiflow/pull/2235)
        -   ワーカプールを最適化して、高い並行性の下でゴルーチンの数を減らす[#2201](https://github.com/pingcap/tiflow/pull/2201)

    -   Dumpling

        -   TiDB v3.x テーブルを常に`tidb_rowid`で分割して TiDBメモリを節約することをサポート[#301](https://github.com/pingcap/dumpling/pull/301)
        -   Dumplingのアクセスを`information_schema`に減らして安定性を向上させる[#305](https://github.com/pingcap/dumpling/pull/305)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SET`型の列[#25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると、誤った結果が返される問題を修正します。
    -   `IN`式の引数[#25591](https://github.com/pingcap/tidb/issues/25591)のデータ破損の問題を修正します
    -   GC のセッションがグローバル変数の影響を受けないようにする[#24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリで`limit`を使用すると発生するpanicの問題を修正します[#25344](https://github.com/pingcap/tidb/issues/25344)
    -   `Limit` [#24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリするときに返される間違った値を修正します
    -   `ENUM`または`SET`タイプの列[#24944](https://github.com/pingcap/tidb/issues/24944)で`IFNULL`が正しく反映されない問題を修正
    -   結合サブクエリの`count` `first_row` [#24865](https://github.com/pingcap/tidb/issues/24865)に変更することによって引き起こされる誤った結果を修正します。
    -   `TopN`演算子[#24930](https://github.com/pingcap/tidb/issues/24930)の下で`ParallelApply`使用すると発生するクエリ ハングの問題を修正します。
    -   複数列のプレフィックス インデックス[#24356](https://github.com/pingcap/tidb/issues/24356)を使用して SQL ステートメントを実行すると、予想よりも多くの結果が返される問題を修正します。
    -   `<=>`オペレーターが正しく発効できない問題を修正[#24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列`Apply`演算子[#23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合の問題を修正します。
    -   PartitionUnion 演算子[#23919](https://github.com/pingcap/tidb/issues/23919)の IndexMerge の結果を並べ替えると、 `index out of range`のエラーが報告される問題を修正します。
    -   `tidb_snapshot`変数を予想外に大きな値に設定すると、トランザクションの分離が損なわれる可能性がある問題を修正します[#25680](https://github.com/pingcap/tidb/issues/25680)
    -   ODBC スタイルの定数 (たとえば、 `{d '2020-01-01'}` ) を式[#25531](https://github.com/pingcap/tidb/issues/25531)として使用できないという問題を修正します。
    -   `SELECT DISTINCT`を`Batch Get`に変換すると誤った結果が生じる問題を修正[#25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashから TiKV へのバックオフ クエリがトリガーされない問題を修正します。 [#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    -   `only_full_group_by` [#23839](https://github.com/pingcap/tidb/issues/23839)のチェック時に発生する`index-out-of-range`エラーを修正します。
    -   相関サブクエリのインデックス結合の結果が間違っている問題を修正[#25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`メトリクスを修正する[#10330](https://github.com/tikv/tikv/issues/10330)
    -   コプロセッサ[#10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正します。
    -   グレースフル シャットダウン中にコールバックのクリアをスキップして、場合によってはACIDの中断を回避します[#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    -   Leader[#10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正します。
    -   `DOUBLE`を`DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)にキャストする間違った関数を修正

-   PD

    -   複数のスケジューラー間でのスケジュールの競合により、期待されるスケジュールが生成されない問題を修正します[#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)

-   TiFlash

    -   分割失敗によりTiFlash が再起動し続ける問題を修正
    -   TiFlash が差分データを削除できない潜在的な問題を修正
    -   TiFlashが`CAST`関数で非バイナリ文字に誤ったパディングを追加するバグを修正
    -   複雑な`GROUP BY`列の集計クエリを処理するときに誤った結果が生じる問題を修正
    -   書き込み圧力が高い場合に発生するTiFlashpanicの問題を修正します。
    -   右側の jon キーが nullable ではなく、左側の join キーが nullable の場合に発生するpanicを修正します。
    -   `read-index`リクエストに時間がかかる潜在的な問題を修正
    -   読み取り負荷が高い場合に発生するpanicの問題を修正
    -   `Date_Format`関数が`STRING`の型引数と`NULL`値で呼び出されたときに発生する可能性があるpanicの問題を修正します。

-   ツール

    -   TiCDC

        -   チェックポイント[#1902](https://github.com/pingcap/tiflow/issues/1902)の更新時にTiCDCオーナーが異常終了する不具合を修正
        -   changefeed の作成が成功した直後に失敗するバグを修正[#2113](https://github.com/pingcap/tiflow/issues/2113)
        -   ルール フィルター[#1625](https://github.com/pingcap/tiflow/issues/1625)の無効な形式が原因で変更フィードが失敗するバグを修正します。
        -   TiCDC 所有者がパニックに陥ったときの潜在的な DDL 損失の問題を修正します[#1260](https://github.com/pingcap/tiflow/issues/1260)
        -   デフォルトの sort-engine オプション[#2373](https://github.com/pingcap/tiflow/issues/2373)での 4.0.x クラスターの CLI 互換性の問題を修正します。
        -   TiCDC が`ErrSchemaStorageTableMiss`エラー[#2422](https://github.com/pingcap/tiflow/issues/2422)を取得したときに、changefeed が予期せずリセットされることがあるというバグを修正します。
        -   TiCDC が`ErrGCTTLExceeded`エラー[#2391](https://github.com/pingcap/tiflow/issues/2391)を取得すると、changefeed を削除できないバグを修正します。
        -   TiCDC が大きなテーブルを cdclog に同期できないバグを修正[#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)
        -   TiCDC がテーブルを再スケジュールしているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるというバグを修正します[#2230](https://github.com/pingcap/tiflow/issues/2230)

    -   バックアップと復元 (BR)

        -   リストア中にBR がすべてのシステム テーブルのリストアをスキップするバグを修正します[#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        -   cdclog [#870](https://github.com/pingcap/br/issues/870)の復元時にBR がDDL 操作を見逃すバグを修正

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイル[#1272](https://github.com/pingcap/br/pull/1272)の`DECIMAL`データ型の解析に失敗するバグを修正
        -   テーブル スキーマの復元時にTiDB Lightning が「エラー 9007: 書き込み競合」エラーを報告するバグを修正します[#1290](https://github.com/pingcap/br/issues/1290)
        -   TiDB Lightning がint ハンドルのオーバーフローによりデータのインポートに失敗する不具合を修正[#1291](https://github.com/pingcap/br/issues/1291)
        -   ローカル バックエンド モード[#1403](https://github.com/pingcap/br/issues/1403)でのデータ損失により、 TiDB Lightning でチェックサムの不一致エラーが発生する可能性があるバグを修正
        -   TiDB Lightningがテーブル スキーマを復元しているときに、クラスタ化されたインデックスでライトニングの非互換性の問題を修正します[#1362](https://github.com/pingcap/br/issues/1362)

    -   Dumpling

        -   Dumpling GC セーフポイントの設定が遅すぎるためにデータのエクスポートが失敗するバグを修正[#290](https://github.com/pingcap/dumpling/pull/290)
        -   特定の MySQL バージョン[#322](https://github.com/pingcap/dumpling/issues/322)でアップストリーム データベースからテーブル名をエクスポートするときにDumplingがスタックする問題を修正します。
