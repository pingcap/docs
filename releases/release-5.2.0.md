---
title: TiDB 5.2 Release Notes
---

# TiDB5.2リリースノート {#tidb-5-2-release-notes}

発売日：2021年8月27日

TiDBバージョン：5.2.0

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の5.2.xバージョンを使用することをお勧めします。

v5.2では、主な新機能と改善点は次のとおりです。

-   クエリのパフォーマンスを大幅に向上させるために、式インデックスでいくつかの関数を使用することをサポートします
-   オプティマイザーのカーディナリティ推定の精度を向上させて、最適な実行プランの選択に役立てます
-   トランザクションロックイベントを監視し、デッドロックの問題をトラブルシューティングするためのロックビュー機能の一般提供（GA）をアナウンスします
-   TiFlash I / Oトラフィック制限機能を追加して、TiFlashの読み取りと書き込みの安定性を向上させます
-   TiKVは、以前のRocksDB書き込みストールメカニズムを置き換える新しいフロー制御メカニズムを導入して、TiKVフロー制御の安定性を向上させます
-   データ移行（DM）の運用と保守を簡素化して、管理コストを削減します。
-   TiCDCは、HTTPプロトコルOpenAPIをサポートしてTiCDCタスクを管理します。 Kubernetesとオンプレミス環境の両方でよりユーザーフレンドリーな操作方法を提供します。 （実験的特徴）

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前のTiDBバージョンからv5.2にアップグレードするときに、すべての中間バージョンの互換性の変更に関する注意事項を知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                       | タイプを変更する   | 説明                                                                      |
| :-------------------------------------------------------------------------------------------------------- | :--------- | :---------------------------------------------------------------------- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                     | 新しく追加されました | サーバーがアドバタイズする認証方法を設定します。デフォルト値は`mysql_native_password`です。               |
| [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) | 新しく追加されました | 生成された列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定します。デフォルト値は`OFF`です。 |
| [`tidb_opt_enable_correlation_adjustment`](/system-variables.md#tidb_opt_enable_correlation_adjustment)   | 新しく追加されました | オプティマイザーが列の順序の相関に基づいて行数を推定するかどうかを制御します。デフォルト値は`ON`です。                   |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold)           | 新しく追加されました | LimitまたはTopN演算子をTiKVにプッシュするかどうかを決定するしきい値を設定します。デフォルト値は`100`です。          |
| [`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40)    | 変更         | ステートメントサマリーテーブルがメモリに保存するステートメントの最大数を設定します。デフォルト値は`200`から`3000`に変更されます。  |
| `tidb_enable_streaming`                                                                                   | 非推奨        | システム変数`enable-streaming`は非推奨であり、これ以上使用することはお勧めしません。                     |

### Configuration / コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| Configuration / コンフィグレーションファイル | Configuration / コンフィグレーション項目                                                                                                  | タイプを変更する   | 説明                                                                                                                              |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------ |
| TiDB構成ファイル                     | [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable)        | 新しく追加されました | [`INFORMATION\_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロックエラーメッセージを収集するかどうかを制御します。 |
| TiDB構成ファイル                     | [`security.auto-tls`](/tidb-configuration-file.md#auto-tls)                                                                   | 新しく追加されました | 起動時にTLS証明書を自動的に生成するかどうかを決定します。デフォルト値は`false`です。                                                                                 |
| TiDB構成ファイル                     | [`stmt-summary.max-stmt-count`](/tidb-configuration-file.md#max-stmt-count)                                                   | 変更         | ステートメントサマリーテーブルに保存できるSQLカテゴリの最大数を示します。デフォルト値は`200`から`3000`に変更されます。                                                              |
| TiDB構成ファイル                     | `experimental.allow-expression-index`                                                                                         | 非推奨        | TiDB構成ファイルの`allow-expression-index`つの構成は非推奨になりました。                                                                              |
| TiKV構成ファイル                     | [`raftstore.cmd-batch`](/tikv-configuration-file.md#cmd-batch)                                                                | 新しく追加されました | リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。デフォルト値は`true`です。                                                        |
| TiKV構成ファイル                     | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                  | 新しく追加されました | 一定の間隔で、TiKVはRaftstoreコンポーネントのレイテンシーを検査します。この構成項目は、検査の間隔を指定します。待ち時間がこの値を超える場合、この検査はタイムアウトとしてマークされます。デフォルト値は`500ms`です。            |
| TiKV構成ファイル                     | [`raftstore.max-peer-down-duration`](/tikv-configuration-file.md#max-peer-down-duration)                                      | 変更         | ピアに許可されている最長の非アクティブ期間を示します。タイムアウトのあるピアは`down`としてマークされ、PDは後でそれを削除しようとします。デフォルト値は`5m`から`10m`に変更されます。                              |
| TiKV構成ファイル                     | [`server.raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                                         | 新しく追加されました | TiKVのラフトメッセージのキューサイズを指定します。デフォルト値は`8192`です。                                                                                     |
| TiKV構成ファイル                     | [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)                                                           | 新しく追加されました | フロー制御メカニズムを有効にするかどうかを決定します。デフォルト値は`true`です。                                                                                     |
| TiKV構成ファイル                     | [`storage.flow-control.memtables-threshold`](/tikv-configuration-file.md#memtables-threshold)                                 | 新しく追加されました | kvDB memtableの数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。デフォルト値は`5`です。                                                                    |
| TiKV構成ファイル                     | [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                   | 新しく追加されました | kvDB L0ファイルの数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。デフォルト値は`9`です。                                                                      |
| TiKV構成ファイル                     | [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 新しく追加されました | KvDBの保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求の拒否を開始し、 `ServerIsBusy`エラーを報告します。デフォルト値は「192GB」です。                               |
| TiKV構成ファイル                     | [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit) | 新しく追加されました | KvDBの保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`のエラーを報告します。デフォルト値は「1024GB」です。                               |

### その他 {#others}

-   アップグレードする前に、 [`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40)のシステム変数の値が`ON`であるかどうかを確認してください。値が`ON`の場合は、 `OFF`に設定します。そうしないと、アップグレードは失敗します。
-   v4.0からv5.2にアップグレードされたTiDBクラスターの場合、デフォルト値の[`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)が`WARN`から`OFF`に変更されます。
-   アップグレードする前に、TiDB構成[`feedback-probability`](/tidb-configuration-file.md#feedback-probability)の値を確認してください。値が`0`でない場合、アップグレード後に「回復可能なゴルーチンのパニック」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDBは、MySQL5.7のnoop変数`innodb_default_row_format`と互換性があります。この変数を設定しても効果はありません。 [＃23541](https://github.com/pingcap/tidb/issues/23541)
-   TiDB 5.2以降、システムセキュリティを向上させるために、クライアントからの接続用にトランスポート層を暗号化することをお勧めします（必須ではありません）。 TiDBは、TiDBで暗号化を自動的に構成して有効にする自動TLS機能を提供します。自動TLS機能を使用するには、TiDBをアップグレードする前に、TiDB構成ファイルの[`security.auto-tls`](/tidb-configuration-file.md#auto-tls)を`true`に設定します。
-   MySQL 8.0からの移行を容易にし、セキュリティを向上させるために、 `caching_sha2_password`の認証方法をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   **式インデックスでのいくつかの関数の使用のサポート**

    式インデックスは、式に作成できる特殊なインデックスの一種です。式インデックスが作成された後、TiDBは式ベースのクエリをサポートします。これにより、クエリのパフォーマンスが大幅に向上します。

    [ユーザードキュメント](/sql-statements/sql-statement-create-index.md) [＃25150](https://github.com/pingcap/tidb/issues/25150)

-   **Oracleの`translate`機能をサポートする**

    `translate`関数は、文字列内で出現するすべての文字を他の文字に置き換えます。 TiDBでは、この関数はOracleのように空の文字列を`NULL`として扱いません。

    [ユーザードキュメント](/functions-and-operators/string-functions.md)

-   **こぼれるHashAggをサポートする**

    HashAggをディスクにこぼすことをサポートします。 HashAgg演算子を含むSQLステートメントがメモリ不足（OOM）を引き起こした場合、この演算子の同時実行性を`1`に設定して、ディスクスピルをトリガーし、メモリストレスを軽減することができます。

    [ユーザードキュメント](/configure-memory-usage.md#other-memory-control-behaviors-of-tidb-server) [＃25882](https://github.com/pingcap/tidb/issues/25882)

-   **オプティマイザのカーディナリティ推定の精度を向上させる**

    -   TiDBによるTopN/Limitの推定の精度を向上させます。たとえば、 `order by col limit x`の条件を含む大きなテーブルのページネーションクエリの場合、TiDBは適切なインデックスをより簡単に選択し、クエリの応答時間を短縮できます。
    -   範囲外推定の精度を向上させます。たとえば、1日の統計が更新されていない場合でも、TiDBは`where date=Now()`を含むクエリに対応するインデックスを正確に選択できます。
    -   `tidb_opt_limit_push_down_threshold`変数を導入して、Limit / TopNをプッシュダウンするオプティマイザーの動作を制御します。これにより、推定が間違っているためにLimit/TopNをプッシュダウンできない場合があるという問題が解決されます。

    [ユーザードキュメント](/system-variables.md#tidb_opt_limit_push_down_threshold) [＃26085](https://github.com/pingcap/tidb/issues/26085)

-   **オプティマイザのインデックス選択を改善する**

    インデックス選択のプルーニングルールを追加します。統計を比較に使用する前に、TiDBはこれらのルールを使用して、選択される可能性のあるインデックスの範囲を絞り込みます。これにより、最適でないインデックスを選択する可能性が低くなります。

    [ユーザードキュメント](/choose-index.md)

### 取引 {#transaction}

-   **Lock Viewの一般提供（GA）**

    ロックビュー機能は、ペシミスティックロックのロック競合とロック待機に関する詳細情報を提供します。これは、DBAがトランザクションロックイベントを監視し、デッドロックの問題をトラブルシューティングするのに役立ちます。

    v5.2では、ロックビューに次の機能拡張が行われました。

    -   ロックビュー関連のテーブルのSQLダイジェスト列に加えて、対応する正規化されたSQLテキストを示す列をこれらのテーブルに追加します。 SQLダイジェストに対応するステートメントを手動でクエリする必要はありません。
    -   `TIDB_DECODE_SQL_DIGESTS`関数を追加して、クラスタの一連のSQLダイジェストに対応する正規化されたSQLステートメント（形式と引数のないフォーム）をクエリします。これにより、トランザクションによって過去に実行されたステートメントをクエリする操作が簡素化されます。
    -   `DATA_LOCK_WAITS`および`DEADLOCKS`システム表に列を追加して、表名、行ID、索引値、および鍵から解釈されるその他の鍵情報を表示します。これにより、キーが属するテーブルの検索やキー情報の解釈などの操作が簡素化されます。
    -   `DEADLOCKS`テーブルでの再試行可能なデッドロック・エラーの情報の収集をサポートします。これにより、このようなエラーによって引き起こされた問題のトラブルシューティングが容易になります。エラー収集はデフォルトで無効になっており、 `pessimistic-txn.deadlock-history-collect-retryable`の構成を使用して有効にできます。
    -   `TIDB_TRX`システムテーブルでクエリ実行トランザクションとアイドルトランザクションの区別をサポートします。現在、 `Normal`の状態は`Running`つの状態と`Idle`の状態に分割されています。

    ユーザードキュメント：

    -   クラスタのすべてのTiKVノードで発生している悲観的なロック待機イベントを表示します： [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDBノードで最近発生したデッドロックエラーを表示します： [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDBノードで実行中のトランザクションを表示します： [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

-   `AUTO_RANDOM`または`SHARD_ROW_ID_BITS`属性を持つテーブルにインデックスを追加するユーザーシナリオを最適化します。

### 安定 {#stability}

-   **TiFlash I/Oトラフィック制限を追加する**

    この新機能は、ディスク帯域幅が小さく特定のサイズのクラウドストレージに適しています。デフォルトでは無効になっています。

    TiFlash I / Oレートリミッターは、読み取りタスクと書き込みタスクの間のI/Oリソースの過度の競合を回避するための新しいメカニズムを提供します。読み取りタスクと書き込みタスクへの応答のバランスを取り、読み取り/書き込みワークロードに応じてレートを自動的に制限します。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md)

-   **TiKVフロー制御の安定性を向上させる**

    TiKVは、以前のRocksDB書き込みストールメカニズムを置き換える新しいフロー制御メカニズムを導入しています。書き込みストールメカニズムと比較して、この新しいメカニズムは、フォアグラウンド書き込みの安定性への影響を軽減します。

    具体的には、RocksDB圧縮のストレスが蓄積すると、次の問題を回避するために、RocksDBレイヤーではなくTiKVスケジューラーレイヤーでフロー制御が実行されます。

    -   RocksDBの書き込みストールが原因でRaftstoreがスタックしています。
    -   いかだ選挙がタイムアウトし、その結果、ノードリーダーが転送されます。

    この新しいメカニズムは、フロー制御アルゴリズムを改善して、書き込みトラフィックが多い場合のQPSの低下を軽減します。

    [ユーザードキュメント](/tikv-configuration-file.md#storageflow-control) [＃10137](https://github.com/tikv/tikv/issues/10137)

-   **クラスタの単一の低速TiKVノードによって引き起こされた影響を自動的に検出して回復します**

    TiKVは、低速ノード検出メカニズムを導入しています。このメカニズムは、TiKV Raftstoreのレートを検査してスコアを計算し、ストアのハートビートを介してスコアをPDに報告します。一方、PDに`evict-slow-store-scheduler`のスケジューラーを追加して、単一の低速TiKVノードのリーダーを自動的に削除します。このようにして、クラスタ全体への影響が軽減されます。同時に、問題をすばやく特定して解決するのに役立つ、低速ノードに関するアラート項目がさらに導入されています。

    [ユーザードキュメント](/tikv-configuration-file.md#inspect-interval) [＃10539](https://github.com/tikv/tikv/issues/10539)

### データ移行 {#data-migration}

-   **データ移行（DM）の操作を簡素化する**

    DM v2.0.6は、VIPを使用してデータソースの変更イベント（フェイルオーバーまたは計画変更）を自動的に識別し、新しいデータソースインスタンスに自動的に接続して、データ複製の待ち時間を短縮し、操作手順を簡素化できます。

-   TiDB Lightningは、CSVデータでカスタマイズされたラインターミネータをサポートし、MySQL LOADDATACSVデータ形式と互換性があります。その後、データフローアーキテクチャで直接TiDBLightningを使用できます。

    [＃1297](https://github.com/pingcap/br/pull/1297)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

TiCDCは、HTTPプロトコル（OpenAPI）を使用したTiCDCタスクの管理をサポートしています。これは、Kubernetesとオンプレミス環境の両方にとってよりユーザーフレンドリーな操作方法です。 （実験的特徴）

[＃2411](https://github.com/pingcap/tiflow/issues/2411)

### 展開と運用 {#deployment-and-operations}

AppleM1チップを搭載したMacコンピュータでの`tiup playground`コマンドの実行をサポートします。

## 機能の強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   TiDB用に設計されたバイナリMQ形式を追加します。 [＃1621](https://github.com/pingcap/tiflow/pull/1621)に基づくオープンプロトコルよりもコンパクトです。
        -   ファイルソーター[＃2114](https://github.com/pingcap/tiflow/pull/2114)のサポートを削除します
        -   ログローテーション構成のサポート[＃2182](https://github.com/pingcap/tiflow/pull/2182)

    -   TiDB Lightning

        -   カスタマイズされたラインターミネータをサポート（ `\r`と`\n`を除く） [＃1297](https://github.com/pingcap/br/pull/1297)
        -   式インデックスと仮想生成列に依存するインデックスをサポート[＃1407](https://github.com/pingcap/br/pull/1407)

    -   Dumpling

        -   MySQL互換データベースのバックアップをサポートしますが、 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`をサポートしませ[＃311](https://github.com/pingcap/dumpling/pull/311)

## 改善 {#improvements}

-   TiDB

    -   内蔵機能`json_unquote()`から[＃24415](https://github.com/pingcap/tidb/issues/24415)へのプッシュダウンをサポート
    -   デュアルテーブル[＃25614](https://github.com/pingcap/tidb/pull/25614)からの`union`ブランチの削除をサポート
    -   骨材オペレーターのコストファクターを最適化する[＃25241](https://github.com/pingcap/tidb/pull/25241)
    -   MPP外部結合が、テーブルの行数[＃25142](https://github.com/pingcap/tidb/pull/25142)に基づいてビルドテーブルを選択できるようにします。
    -   リージョン[＃24724](https://github.com/pingcap/tidb/pull/24724)に基づく異なるTiFlashノード間でのMPPクエリワークロードのバランス調整をサポート
    -   MPPクエリの実行後にキャッシュ内の古いリージョンを無効にすることをサポートします[＃24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子[＃25767](https://github.com/pingcap/tidb/pull/25767)の組み込み関数`str_to_date`のMySQL互換性を改善し`%b/%M/%r/%T`
    -   同じクエリに対して異なるバインディングを再作成した後、一貫性のないバインディングキャッシュが複数のTiDBに作成される可能性がある問題を修正します[＃26015](https://github.com/pingcap/tidb/pull/26015)
    -   アップグレード後に既存のバインディングをキャッシュにロードできない問題を修正します[＃23295](https://github.com/pingcap/tidb/pull/23295)
    -   `SHOW BINDINGS` by（ `original_sql` ） `update_time`の結果の注文を[＃26139](https://github.com/pingcap/tidb/pull/26139)
    -   バインディングが存在する場合のクエリ最適化のロジックを改善し、クエリの最適化時間を短縮します[＃26141](https://github.com/pingcap/tidb/pull/26141)
    -   「削除済み」ステータスのバインディングのガベージコレクションの自動完了をサポート[＃26206](https://github.com/pingcap/tidb/pull/26206)
    -   [＃26930](https://github.com/pingcap/tidb/pull/26930)の結果でクエリ最適化にバインディングが使用されているかどうかを`EXPLAIN VERBOSE`サポート
    -   新しいステータスバリエーション`last_plan_binding_update_time`を追加して、現在のTiDBインスタンス[＃26340](https://github.com/pingcap/tidb/pull/26340)のバインディングキャッシュに対応するタイムスタンプを表示します。
    -   バインディングエボリューションを開始するとき、または`admin evolve bindings`を実行して、他の機能に影響を与えるベースラインエボリューション（オンプレミスのTiDBバージョンでは実験的機能であるため現在無効になっています）を禁止するときのエラーの報告をサポートします[＃26333](https://github.com/pingcap/tidb/pull/26333)

-   PD

    -   ホットリージョンスケジューリング用にQPSディメンションを追加し、スケジューリングの優先度の調整をサポートします[＃3869](https://github.com/tikv/pd/issues/3869)
    -   [＃3900](https://github.com/tikv/pd/pull/3900)の書き込みホットスポットのホットリージョンバランススケジューリングをサポートする

-   TiFlash

    -   `LIKE`の追加： `MOD / %`
    -   文字列`TRIM()`を`POSITION()`し`COALESCE()` `LENGTH()` `ASCII()`
    -   `POW()` `LOG2()` `MOD()` `LOG10()` `SIN()` `RADIANS()` `ROUND(decimal)` `CONV()` `CRC32()` `DEGREES()` `EXP()` `LN()` `LOG()`
    -   日付関数の`DATE_ADD(string, real)` `DATE()` `ADDDATE(string, real)`
    -   他の関数を`INET6_NTOA()`し`INET_ATON()` `INET6_ATON` `INET_NTOA()`
    -   新しい照合順序が有効になっている場合、MPPモードでシャッフルハッシュ結合計算とシャッフルハッシュ集計計算をサポートします
    -   基本コードを最適化してMPPパフォーマンスを向上させる
    -   `STRING`タイプから`DOUBLE`タイプへのキャストをサポート
    -   複数のスレッドを使用して、右外部結合で結合されていないデータを最適化します
    -   MPPクエリで古いリージョンを自動的に無効にすることをサポート

-   ツール

    -   TiCDC

        -   kvクライアント[＃1899](https://github.com/pingcap/tiflow/pull/1899)の増分スキャンに同時実行制限を追加します
        -   TiCDCは常に古い値を内部的にプルできます[＃2271](https://github.com/pingcap/tiflow/pull/2271)
        -   回復不能なDMLエラーが発生すると、TiCDCは失敗し、すぐに終了する可能性があります[＃1928](https://github.com/pingcap/tiflow/pull/1928)
        -   リージョンが初期化された直後に`resolve lock`を実行することはできません[＃2235](https://github.com/pingcap/tiflow/pull/2235)
        -   ワーカープールを最適化して、同時実行性が高い場合のゴルーチンの数を減らします[＃2201](https://github.com/pingcap/tiflow/pull/2201)

    -   Dumpling

        -   TiDBメモリを節約するためにTiDBv3.xテーブルを常に`tidb_rowid`に分割することをサポートします[＃301](https://github.com/pingcap/dumpling/pull/301)
        -   安定性を向上させるために`information_schema`へのDumplingのアクセスを減らします[＃305](https://github.com/pingcap/dumpling/pull/305)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SET`型列[＃25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると誤った結果が返される問題を修正します。
    -   `IN`式の引数[＃25591](https://github.com/pingcap/tidb/issues/25591)のデータ破損の問題を修正します
    -   GCのセッションがグローバル変数の影響を受けないようにする[＃24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリ[＃25344](https://github.com/pingcap/tidb/issues/25344)で`limit`を使用するときに発生するパニックの問題を修正します
    -   `Limit`を使用してパーティションテーブルをクエリするときに返される誤った値を修正し[＃24636](https://github.com/pingcap/tidb/issues/24636)
    -   `IFNULL`が`ENUM`または`SET`タイプの列[＃24944](https://github.com/pingcap/tidb/issues/24944)で正しく有効にならない問題を修正します
    -   結合サブクエリの`count`を[＃24865](https://github.com/pingcap/tidb/issues/24865)に変更することによって引き起こされる間違った結果を修正し`first_row`
    -   `TopN`演算子[＃24930](https://github.com/pingcap/tidb/issues/24930)で`ParallelApply`を使用した場合に発生するクエリハングの問題を修正します。
    -   複数列のプレフィックスインデックスを使用してSQLステートメントを実行すると、予想よりも多くの結果が返される問題を修正します[＃24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`オペレーターが正しく有効にできない問題を修正します[＃24477](https://github.com/pingcap/tidb/issues/24477)
    -   パラレル`Apply`オペレーター[＃23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合の問題を修正します
    -   PartitionUnionオペレーター[＃23919](https://github.com/pingcap/tidb/issues/23919)のIndexMerge結果をソートするときに`index out of range`エラーが報告される問題を修正します。
    -   `tidb_snapshot`変数を予想外に大きな値に設定すると、トランザクション分離が損なわれる可能性があるという問題を修正します[＃25680](https://github.com/pingcap/tidb/issues/25680)
    -   ODBCスタイルの定数（たとえば、 `{d '2020-01-01'}` ）を式[＃25531](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正します。
    -   `SELECT DISTINCT`を`Batch Get`に変換すると誤った結果が発生する問題を修正します[＃25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashからTiKVへのクエリのバックオフをトリガーできない問題を修正し[＃24421](https://github.com/pingcap/tidb/issues/24421) [＃23665](https://github.com/pingcap/tidb/issues/23665)
    -   `only_full_group_by`をチェックするときに発生する`index-out-of-range`のエラーを修正します[＃23839](https://github.com/pingcap/tidb/issues/23839) ）
    -   相関サブクエリでのインデックス結合の結果が間違っている問題を修正します[＃25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`メトリック[＃10330](https://github.com/tikv/tikv/issues/10330)を修正
    -   コプロセッサー[＃10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正してください
    -   場合によってはACIDの破損を回避するために、正常なシャットダウン中にコールバックのクリアをスキップします[＃10353](https://github.com/tikv/tikv/issues/10353) [＃10307](https://github.com/tikv/tikv/issues/10307)
    -   リーダー[＃10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正します
    -   `DOUBLE`から[＃25200](https://github.com/pingcap/tidb/issues/25200)をキャストする間違った関数を修正し`DOUBLE`

-   PD

    -   複数のスケジューラ間のスケジュールの競合が原因で、期待されるスケジューリングを生成できない問題を修正します[＃3807](https://github.com/tikv/pd/issues/3807) [＃3778](https://github.com/tikv/pd/issues/3778)

-   TiFlash

    -   分割の失敗が原因でTiFlashが再起動し続ける問題を修正します
    -   TiFlashがデルタデータを削除できないという潜在的な問題を修正します
    -   TiFlashが`CAST`関数の非バイナリ文字に間違ったパディングを追加するバグを修正します
    -   複雑な`GROUP BY`列の集計クエリを処理するときの誤った結果の問題を修正します
    -   書き込み圧力が高い場合に発生するTiFlashパニックの問題を修正します
    -   右のジョンキーがNULL可能ではなく、左の結合キーがNULL可能である場合に発生するパニックを修正します
    -   `read-index`のリクエストに時間がかかる可能性のある問題を修正します
    -   読み取り負荷が大きいときに発生するパニックの問題を修正します
    -   `Date_Format`の関数が`STRING`の型の引数と`NULL`の値で呼び出されたときに発生する可能性のあるパニックの問題を修正します

-   ツール

    -   TiCDC

        -   チェックポイント[＃1902](https://github.com/pingcap/tiflow/issues/1902)を更新するときにTiCDC所有者が異常終了するバグを修正します
        -   作成が成功した直後にchangefeedが失敗するバグを修正します[＃2113](https://github.com/pingcap/tiflow/issues/2113)
        -   ルールフィルター[＃1625](https://github.com/pingcap/tiflow/issues/1625)の形式が無効なためにchangefeedが失敗するバグを修正します
        -   TiCDC所有者がパニックに陥ったときに発生する可能性のあるDDL損失の問題を修正します[＃1260](https://github.com/pingcap/tiflow/issues/1260)
        -   デフォルトのsort-engineオプション[＃2373](https://github.com/pingcap/tiflow/issues/2373)での4.0.xクラスターとのCLI互換性の問題を修正します
        -   TiCDCが`ErrSchemaStorageTableMiss`エラー[＃2422](https://github.com/pingcap/tiflow/issues/2422)を取得したときにchangefeedが予期せずリセットされる可能性があるバグを修正します
        -   TiCDCが`ErrGCTTLExceeded`エラー[＃2391](https://github.com/pingcap/tiflow/issues/2391)を取得したときにchangefeedを削除できないバグを修正します
        -   TiCDCが大きなテーブルを[＃1259](https://github.com/pingcap/tiflow/issues/1259)に同期できないバグを修正し[＃2424](https://github.com/pingcap/tiflow/issues/2424) 。
        -   TiCDCがテーブルを再スケジュールしているときに複数のプロセッサが同じテーブルにデータを書き込む可能性があるバグを修正します[＃2230](https://github.com/pingcap/tiflow/issues/2230)

    -   バックアップと復元（BR）

        -   BRが復元中にすべてのシステムテーブルの復元をスキップするバグを修正し[＃1201](https://github.com/pingcap/br/issues/1201) [＃1197](https://github.com/pingcap/br/issues/1197)
        -   cdclog1を復元するときにBRがDDL操作を見逃すバグを修正し[＃870](https://github.com/pingcap/br/issues/870)

    -   TiDB Lightning

        -   TiDBLightningがParquetファイル[＃1272](https://github.com/pingcap/br/pull/1272)の`DECIMAL`データ型の解析に失敗するバグを修正します
        -   テーブルスキーマの復元時にTiDBLightningが「エラー9007：書き込みの競合」エラーを報告するバグを修正します[＃1290](https://github.com/pingcap/br/issues/1290)
        -   intハンドル[＃1291](https://github.com/pingcap/br/issues/1291)のオーバーフローが原因でTiDBLightningがデータのインポートに失敗するバグを修正します
        -   ローカルバックエンドモードでのデータ損失が原因でTiDBLightningがチェックサム不一致エラーを受け取る可能性があるバグを修正します[＃1403](https://github.com/pingcap/br/issues/1403)
        -   TiDBLightningがテーブルスキーマを復元しているときのクラスター化インデックスとのLightingの非互換性の問題を修正します[＃1362](https://github.com/pingcap/br/issues/1362)

    -   Dumpling

        -   DumplingGCセーフポイントの設定が遅すぎるためにデータのエクスポートが失敗するバグを修正します[＃290](https://github.com/pingcap/dumpling/pull/290)
        -   特定のMySQLバージョン[＃322](https://github.com/pingcap/dumpling/issues/322)でアップストリームデータベースからテーブル名をエクスポートするときにDumplingがスタックする問題を修正します
