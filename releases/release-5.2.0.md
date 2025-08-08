---
title: TiDB 5.2 Release Notes
summary: TiDB 5.2.0では、式インデックスのサポート、Lock ビューのGA、 TiFlash I/Oトラフィック制限など、新機能と改善が導入されています。互換性に関する変更には、新しいシステム変数と設定ファイルパラメータが含まれます。また、このリリースには、TiDB、TiKV、 TiFlash、およびTiCDC、 BR、Lightning、 Dumplingなどのツールのバグ修正と機能強化も含まれています。
---

# TiDB 5.2 リリースノート {#tidb-5-2-release-notes}

発売日：2021年8月27日

TiDB バージョン: 5.2.0

> **警告：**
>
> このバージョンにはいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の5.2.xバージョンをご利用いただくことをお勧めします。

v5.2 の主な新機能と改善点は次のとおりです。

-   式インデックスで複数の関数の使用をサポートし、クエリのパフォーマンスを大幅に向上します。
-   オプティマイザのカーディナリティ推定の精度を向上させ、最適な実行プランを選択できるようにします。
-   トランザクションのロックイベントを監視し、デッドロックの問題をトラブルシューティングするためのロックビュー機能の一般提供（GA）を発表します。
-   TiFlashの読み取りと書き込みの安定性を向上させるために、 TiFlash I/Oトラフィック制限機能を追加しました。
-   TiKVは、以前のRocksDB書き込み停止メカニズムに代わる新しいフロー制御メカニズムを導入し、TiKVフロー制御の安定性を向上させました。
-   データ移行 (DM) の運用と保守を簡素化し、管理コストを削減します。
-   TiCDCは、TiCDCタスクの管理にHTTPプロトコルOpenAPIをサポートしています。Kubernetes環境とセルフホスト環境の両方で、よりユーザーフレンドリーな操作方法を提供します。（Experimental機能）

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.2 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                       | タイプを変更   | 説明                                                                     |
| :-------------------------------------------------------------------------------------------------------- | :------- | :--------------------------------------------------------------------- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                     | 新しく追加された | サーバーがアドバタイズする認証方法を設定します。デフォルト値は`mysql_native_password`です。              |
| [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) | 新しく追加された | 生成列または式インデックスを作成する際に、 `AUTO_INCREMENT`列を含めるかどうかを決定します。デフォルト値は`OFF`です。  |
| [`tidb_opt_enable_correlation_adjustment`](/system-variables.md#tidb_opt_enable_correlation_adjustment)   | 新しく追加された | オプティマイザが列順序の相関に基づいて行数を推定するかどうかを制御します。デフォルト値は`ON`です。                    |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold)           | 新しく追加された | Limit演算子またはTopN演算子をTiKVまで押し下げるかどうかを決定するしきい値を設定します。デフォルト値は`100`です。      |
| [`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40)    | 修正済み     | ステートメントサマリーテーブルがメモリに保存するステートメントの最大数を設定します。デフォルト値は`200`から`3000`に変更されます。 |
| `tidb_enable_streaming`                                                                                   | 非推奨      | システム変数`enable-streaming`非推奨であり、今後使用することはお勧めしません。                       |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                                                  | タイプを変更   | 説明                                                                                                                                |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| TiDB構成ファイル     | [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable)        | 新しく追加された | [`INFORMATION\_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロック エラー メッセージを収集するかどうかを制御します。 |
| TiDB構成ファイル     | [`security.auto-tls`](/tidb-configuration-file.md#auto-tls)                                                                   | 新しく追加された | 起動時にTLS証明書を自動生成するかどうかを決定します。デフォルト値は`false`です。                                                                                     |
| TiDB構成ファイル     | `stmt-summary.max-stmt-count`                                                                                                 | 修正済み     | ステートメントサマリーテーブルに保存できるSQLカテゴリの最大数を示します。デフォルト値は`200`から`3000`に変更されました。                                                               |
| TiDB構成ファイル     | `experimental.allow-expression-index`                                                                                         | 非推奨      | TiDB 構成ファイル内の`allow-expression-index`構成は非推奨です。                                                                                    |
| TiKV設定ファイル     | [`raftstore.cmd-batch`](/tikv-configuration-file.md#cmd-batch)                                                                | 新しく追加された | リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。デフォルト値は`true`です。                                                          |
| TiKV設定ファイル     | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                  | 新しく追加された | TiKVは一定の間隔でRaftstoreコンポーネントのレイテンシーを検査します。この設定項目は検査間隔を指定します。レイテンシーがこの値を超えると、検査はタイムアウトとしてマークされます。デフォルト値は`500ms`です。                  |
| TiKV設定ファイル     | [`raftstore.max-peer-down-duration`](/tikv-configuration-file.md#max-peer-down-duration)                                      | 修正済み     | ピアに許可される最長時間の非アクティブ期間を示します。タイムアウトが発生したピアは`down`とマークされ、PDは後でそのピアを削除しようとします。デフォルト値は`5m`から`10m`に変更されました。                             |
| TiKV設定ファイル     | [`server.raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                                         | 新しく追加された | TiKV内のRaftメッセージのキューサイズを指定します。デフォルト値は`8192`です。                                                                                     |
| TiKV設定ファイル     | [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)                                                           | 新しく追加された | フロー制御メカニズムを有効にするかどうかを決定します。デフォルト値は`true`です。                                                                                       |
| TiKV設定ファイル     | [`storage.flow-control.memtables-threshold`](/tikv-configuration-file.md#memtables-threshold)                                 | 新しく追加された | kvDBメモリテーブルの数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。デフォルト値は`5`です。                                                                       |
| TiKV設定ファイル     | [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                   | 新しく追加された | kvDB L0ファイルの数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。デフォルト値は`9`です。                                                                       |
| TiKV設定ファイル     | [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 新しく追加された | KvDB内の保留中の圧縮バイト数がこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し、エラー`ServerIsBusy`を報告します。デフォルト値は「192GB」です。                                   |
| TiKV設定ファイル     | [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit) | 新しく追加された | KvDB内の保留中の圧縮バイト数がこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、エラー`ServerIsBusy`を報告します。デフォルト値は「1024GB」です。                                 |

### その他 {#others}

-   アップグレード前に、システム変数[`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40)の値が`ON`なっているかどうかを確認してください。値が`ON`の場合は`OFF`に設定してください。そうでない場合、アップグレードは失敗します。
-   v4.0 から v5.2 にアップグレードされた TiDB クラスターの場合、デフォルト値[`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)が`WARN`から`OFF`に変更されます。
-   アップグレード前に、TiDB設定の値が[`feedback-probability`](https://docs.pingcap.com/tidb/v5.2/tidb-configuration-file#feedback-probability)を確認してください。値が`0`でない場合、アップグレード後に「回復可能なゴルーチンでpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDBはMySQL 5.7のnoop変数`innodb_default_row_format`と互換性を持つようになりました。この変数を設定しても効果はありません[＃23541](https://github.com/pingcap/tidb/issues/23541)
-   TiDB 5.2以降、システムセキュリティの向上のため、クライアントからの接続のトランスポートレイヤーを暗号化することが推奨されます（必須ではありません）。TiDBは、暗号化を自動的に設定して有効化するAuto TLS機能を提供しています。Auto TLS機能を使用するには、TiDBのアップグレード前に、TiDB設定ファイルで[`security.auto-tls`](/tidb-configuration-file.md#auto-tls) `true`に設定してください。
-   MySQL 8.0 からの移行を容易にし、セキュリティを向上させるために、 `caching_sha2_password`認証方法をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   **式インデックスで複数の関数の使用をサポート**

    式インデックスは、式に基づいて作成できる特殊なインデックスの一種です。式インデックスを作成すると、TiDBは式ベースのクエリをサポートし、クエリパフォーマンスを大幅に向上させます。

    [ユーザードキュメント](/sql-statements/sql-statement-create-index.md) [＃25150](https://github.com/pingcap/tidb/issues/25150)

-   **Oracleの`translate`機能をサポート**

    `translate`関数は、文字列内のすべての文字を他の文字に置き換えます。TiDBでは、この関数はOracleのように空文字列を`NULL`として扱いません。

    [ユーザードキュメント](/functions-and-operators/string-functions.md)

-   **HashAggの流出をサポート**

    HashAgg のディスクへのスピルをサポートします。HashAgg 演算子を含む SQL 文でメモリ不足 (OOM) が発生した場合、この演算子の同時実行数を`1`に設定してディスクへのスピルをトリガーすることで、メモリ負荷を軽減できます。

    [ユーザードキュメント](/configure-memory-usage.md#other-memory-control-behaviors-of-tidb-server) [＃25882](https://github.com/pingcap/tidb/issues/25882)

-   **オプティマイザーのカーディナリティ推定の精度を向上**

    -   TiDBのTopN/Limit推定精度を向上しました。例えば、 `order by col limit x`条件を含む大規模なテーブルに対するページネーションクエリの場合、TiDBは適切なインデックスをより簡単に選択し、クエリの応答時間を短縮できます。
    -   範囲外推定の精度を向上します。例えば、1日の統計情報が更新されていない場合でも、TiDBは`where date=Now()`を含むクエリに対応するインデックスを正確に選択できます。
    -   Limit/TopN を押し下げるオプティマイザーの動作を制御する`tidb_opt_limit_push_down_threshold`変数を導入します。これにより、誤った推定のために状況によっては Limit/TopN を押し下げることができないという問題が解決されます。

    [ユーザードキュメント](/system-variables.md#tidb_opt_limit_push_down_threshold) [＃26085](https://github.com/pingcap/tidb/issues/26085)

-   **オプティマイザのインデックス選択を改善する**

    インデックス選択のためのプルーニングルールを追加します。統計情報を比較に使用する前に、TiDBはこれらのルールを使用して選択可能なインデックスの範囲を絞り込み、最適でないインデックスが選択される可能性を低減します。

    [ユーザードキュメント](/choose-index.md)

### トランザクション {#transaction}

-   **Lock ビューの一般提供 (GA)**

    ロックビュー機能は、ロックの競合や悲観的ロックのロック待機に関する詳細情報を提供するため、DBA はトランザクション ロック イベントを観察し、デッドロックの問題をトラブルシューティングできます。

    v5.2 では、Lock ビューに次の機能強化が加えられました。

    -   ロックビュー関連テーブルのSQLダイジェスト列に加えて、対応する正規化されたSQLテキストを表示する列をこれらのテーブルに追加します。SQLダイジェストに対応するステートメントを手動でクエリする必要はありません。
    -   クラスタ内のSQLダイジェストセットに対応する正規化されたSQL文（フォーマットと引数のない形式）を照会する関数`TIDB_DECODE_SQL_DIGESTS`追加します。これにより、トランザクションによって過去に実行されたSQL文を照会する操作が簡素化されます。
    -   システムテーブル`DATA_LOCK_WAITS`と`DEADLOCKS`に列を追加し、キーから解釈されたテーブル名、行ID、インデックス値などのキー情報を表示します。これにより、キーが属するテーブルの検索やキー情報の解釈といった操作が簡素化されます。
    -   再試行可能なデッドロックエラーの情報を`DEADLOCKS`テーブルで収集できるようになりました。これにより、このようなエラーによって発生する問題のトラブルシューティングが容易になります。エラー収集はデフォルトで無効になっていますが、 `pessimistic-txn.deadlock-history-collect-retryable`設定で有効にできます。
    -   `TIDB_TRX`システムテーブルにおいて、クエリ実行中のトランザクションとアイドル状態のトランザクションを区別できるようになりました。3 状態`Normal` `Running`状態と`Idle`状態に分割されました。

    ユーザードキュメント:

    -   クラスター内のすべての TiKV ノードで発生している悲観的ロック待機イベントをビュー[`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDBノードで最近発生したデッドロックエラーをビュー: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDBノードで実行中のトランザクションをビュー: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

-   属性`AUTO_RANDOM`または`SHARD_ROW_ID_BITS`持つテーブルにインデックスを追加するユーザー シナリオを最適化します。

### 安定性 {#stability}

-   **TiFlash I/Oトラフィック制限を追加**

    この新機能は、ディスク帯域幅が小さく特定のサイズであるクラウドstorageに適しています。デフォルトでは無効になっています。

    TiFlash I/Oレートリミッターは、読み取りタスクと書き込みタスク間のI/Oリソースの過剰な競合を回避するための新しいメカニズムを提供します。読み取りタスクと書き込みタスクへの応答のバランスを取り、読み取り/書き込みワークロードに応じてレートを自動的に制限します。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md)

-   **TiKVフロー制御の安定性を向上**

    TiKVは、以前のRocksDB書き込みストールメカニズムに代わる新しいフロー制御メカニズムを導入します。この新しいメカニズムは、書き込みストールメカニズムと比較して、フォアグラウンド書き込みの安定性への影響を軽減します。

    具体的には、RocksDB の圧縮によるストレスが蓄積すると、RocksDBレイヤーではなく TiKV スケジューラレイヤーでフロー制御が実行され、以下の問題が回避されます。

    -   Raftstoreが停止しています。これは、RocksDB の書き込み停止によって発生します。
    -   Raft選出がタイムアウトし、その結果ノード リーダーが移管されます。

    この新しいメカニズムは、フロー制御アルゴリズムを改善し、書き込みトラフィックが多い場合の QPS の低下を軽減します。

    [ユーザードキュメント](/tikv-configuration-file.md#storageflow-control) [＃10137](https://github.com/tikv/tikv/issues/10137)

-   **クラスター内の単一の低速 TiKV ノードによって引き起こされる影響を自動的に検出して回復します。**

    TiKVは低速ノード検出メカニズムを導入しました。このメカニズムは、TiKV Raftstoreのレートを検査してスコアを計算し、ストアハートビートを介してPDにスコアを報告します。同時に、PDに`evict-slow-store-scheduler`スケジューラを追加し、単一の低速TiKVノードのリーダーノードを自動的に排除します。これにより、クラスター全体への影響が軽減されます。同時に、低速ノードに関するアラート項目が追加され、問題を迅速に特定して解決するのに役立ちます。

    [ユーザードキュメント](/tikv-configuration-file.md#inspect-interval) [＃10539](https://github.com/tikv/tikv/issues/10539)

### データ移行 {#data-migration}

-   **データ移行（DM）の運用を簡素化**

    DM v2.0.6 は、VIP を使用してデータ ソースの変更イベント (フェイルオーバーまたは計画変更) を自動的に識別し、新しいデータ ソース インスタンスに自動的に接続できるため、データ複製のレイテンシーが短縮され、操作手順が簡素化されます。

-   TiDB Lightningは、 CSVデータ内のカスタマイズされた行末文字をサポートし、MySQL LOAD DATAのCSVデータ形式と互換性があります。そのため、 TiDB Lightningをデータフローアーキテクチャ内で直接使用できます。

    [＃1297](https://github.com/pingcap/br/pull/1297)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

TiCDC は、HTTP プロトコル (OpenAPI) を使用した TiCDC タスクの管理をサポートしています。これは、Kubernetes とセルフホスト環境の両方でよりユーザーフレンドリーな操作方法です。(Experimental機能)

[＃2411](https://github.com/pingcap/tiflow/issues/2411)

### 展開と運用 {#deployment-and-operations}

Apple M1 チップを搭載した Mac コンピューターで`tiup playground`コマンドの実行をサポートします。

## 機能強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   TiDB向けに設計されたバイナリMQフォーマットを追加します。JSON [＃1621](https://github.com/pingcap/tiflow/pull/1621)に基づくオープンプロトコルよりもコンパクトです。
        -   ファイルソーター[＃2114](https://github.com/pingcap/tiflow/pull/2114)のサポートを削除
        -   ログローテーション構成のサポート[＃2182](https://github.com/pingcap/tiflow/pull/2182)

    -   TiDB Lightning

        -   カスタマイズされた行末文字をサポート（ `\r`と`\n`を除く） [＃1297](https://github.com/pingcap/br/pull/1297)
        -   式インデックスと仮想生成列に依存するインデックスをサポート[＃1407](https://github.com/pingcap/br/pull/1407)

    -   Dumpling

        -   MySQL互換データベースのバックアップをサポートしますが、 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE` [＃311](https://github.com/pingcap/dumpling/pull/311)はサポートしません。

## 改善点 {#improvements}

-   TiDB

    -   組み込み関数`json_unquote()`をTiKV [＃24415](https://github.com/pingcap/tidb/issues/24415)にプッシュダウンする機能をサポート
    -   デュアルテーブル[＃25614](https://github.com/pingcap/tidb/pull/25614)から`union`ブランチを削除することをサポート
    -   集計オペレータのコスト係数[＃25241](https://github.com/pingcap/tidb/pull/25241)を最適化する
    -   MPP外部結合がテーブル行数[＃25142](https://github.com/pingcap/tidb/pull/25142)に基づいてビルドテーブルを選択できるようにします。
    -   リージョン[＃24724](https://github.com/pingcap/tidb/pull/24724)に基づいて、異なるTiFlashノード間でMPPクエリワークロードのバランスをとることをサポート
    -   MPPクエリ実行後にキャッシュ内の古い領域を無効にする機能をサポート[＃24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子`%b/%M/%r/%T` [＃25767](https://github.com/pingcap/tidb/pull/25767)の組み込み関数`str_to_date`の MySQL 互換性を改善しました
    -   同じクエリに対して異なるバインディングを再作成した後に、複数の TiDB に矛盾したバインディング キャッシュが作成される可能性がある問題を修正しました[＃26015](https://github.com/pingcap/tidb/pull/26015)
    -   アップグレード[＃23295](https://github.com/pingcap/tidb/pull/23295)後に既存のバインディングをキャッシュにロードできない問題を修正
    -   `SHOW BINDINGS`の結果を ( `original_sql` , `update_time` ) [＃26139](https://github.com/pingcap/tidb/pull/26139)で順序付けすることをサポートします
    -   バインディングが存在する場合のクエリ最適化のロジックを改善し、クエリ[＃26141](https://github.com/pingcap/tidb/pull/26141)の最適化時間を短縮します。
    -   「削除済み」ステータスのバインディングのガベージコレクションの自動完了をサポート[＃26206](https://github.com/pingcap/tidb/pull/26206)
    -   `EXPLAIN VERBOSE` [＃26930](https://github.com/pingcap/tidb/pull/26930)の結果で、バインディングがクエリの最適化に使用されているかどうかの表示をサポートします。
    -   現在の TiDB インスタンス[＃26340](https://github.com/pingcap/tidb/pull/26340)バインディング キャッシュに対応するタイムスタンプを表示するための新しいステータス バリエーション`last_plan_binding_update_time`を追加します。
    -   バインディング進化の開始時または`admin evolve bindings`時にエラーを報告することをサポートし、他の機能[＃26333](https://github.com/pingcap/tidb/pull/26333)に影響を与えるベースライン進化を禁止します (これは実験的機能であるため、TiDB セルフマネージド バージョンでは現在無効になっています)。

-   PD

    -   ホットリージョンスケジューリングにQPSディメンションを追加し、スケジューリングの優先順位の調整をサポートします[＃3869](https://github.com/tikv/pd/issues/3869)
    -   TiFlash [＃3900](https://github.com/tikv/pd/pull/3900)の書き込みホットスポットのホットリージョンバランス スケジューリングをサポート

-   TiFlash

    -   `LIKE`演算子: `MOD / %`
    -   `LENGTH()` `TRIM()`関数`COALESCE()`追加`POSITION()` `ASCII()`
    -   `LOG()`関数`CRC32()` `DEGREES()` `EXP()` `LN()` `LOG10()` `CONV()` `LOG2()` `POW()` `RADIANS()` `ROUND(decimal)` `SIN()` `MOD()`
    -   日付関数`DATE_ADD(string, real)`追加`DATE()` `ADDDATE(string, real)`
    -   その他`INET6_NTOA()`関数`INET_ATON()`追加`INET6_ATON` `INET_NTOA()`
    -   新しい照合順序が有効な場合、MPPモードでシャッフルハッシュ結合計算とシャッフルハッシュ集計計算をサポートします。
    -   基本コードを最適化してMPPのパフォーマンスを向上させる
    -   `STRING`型から`DOUBLE`型へのキャストをサポート
    -   複数のスレッドを使用して右外部結合の非結合データを最適化する
    -   MPPクエリで古いリージョンを自動的に無効化する機能をサポート

-   ツール

    -   TiCDC

        -   kvクライアント[＃1899](https://github.com/pingcap/tiflow/pull/1899)の増分スキャンに同時実行制限を追加する
        -   TiCDCは常に内部的に古い値を引き出すことができます[＃2271](https://github.com/pingcap/tiflow/pull/2271)
        -   回復不可能なDMLエラーが発生すると、TiCDCは失敗してすぐに終了する可能性があります[＃1928](https://github.com/pingcap/tiflow/pull/1928)
        -   `resolve lock`リージョンが初期化された直後には実行できません[＃2235](https://github.com/pingcap/tiflow/pull/2235)
        -   ワーカープールを最適化して、高同時実行時のゴルーチンの数を減らす[＃2201](https://github.com/pingcap/tiflow/pull/2201)

    -   Dumpling

        -   TiDBメモリを節約するために、常に TiDB v3.x テーブルを`tidb_rowid`に分割することをサポートします[＃301](https://github.com/pingcap/dumpling/pull/301)
        -   安定性を向上させるために、 `information_schema`へのDumplingのアクセスを減らす[＃305](https://github.com/pingcap/dumpling/pull/305)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `SET`型列[＃25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると誤った結果が返される問題を修正しました
    -   `IN`式の引数[＃25591](https://github.com/pingcap/tidb/issues/25591)におけるデータ破損の問題を修正
    -   GCのセッションがグローバル変数の影響を受けないようにする[＃24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリ[＃25344](https://github.com/pingcap/tidb/issues/25344)で`limit`使用するときに発生するpanic問題を修正
    -   `Limit` [＃24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリしたときに返される誤った値を修正しました
    -   `IFNULL` `ENUM`または`SET`タイプの列[＃24944](https://github.com/pingcap/tidb/issues/24944)に正しく反映されない問題を修正
    -   結合サブクエリの`count` `first_row` [＃24865](https://github.com/pingcap/tidb/issues/24865)に変更することで発生する誤った結果を修正しました
    -   `ParallelApply` `TopN`演算子[＃24930](https://github.com/pingcap/tidb/issues/24930)下で使用された場合に発生するクエリ ハングの問題を修正しました
    -   マルチカラムプレフィックスインデックスを使用してSQL文を実行したときに予想よりも多くの結果が返される問題を修正[＃24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`演算子が正しく機能しない問題を修正[＃24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列`Apply`演算子[＃23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合問題を修正
    -   PartitionUnion演算子[＃23919](https://github.com/pingcap/tidb/issues/23919)のIndexMerge結果をソートするときに`index out of range`エラーが報告される問題を修正しました
    -   `tidb_snapshot`変数を予想外に大きな値に設定するとトランザクション分離[＃25680](https://github.com/pingcap/tidb/issues/25680)損なわれる可能性がある問題を修正しました
    -   ODBCスタイルの定数（たとえば、 `{d '2020-01-01'}` ）を式[＃25531](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正しました。
    -   `SELECT DISTINCT` `Batch Get`に変換すると誤った結果になる問題を修正[＃25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashからTiKVへのクエリのバックオフがトリガーされない問題を修正[＃23665](https://github.com/pingcap/tidb/issues/23665) [＃24421](https://github.com/pingcap/tidb/issues/24421)
    -   `only_full_group_by` [＃23839](https://github.com/pingcap/tidb/issues/23839)チェックするときに発生する`index-out-of-range`エラーを修正します)
    -   相関サブクエリのインデックス結合の結果が間違っている問題を修正[＃25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`指標を修正する[＃10330](https://github.com/tikv/tikv/issues/10330)
    -   コプロセッサ[＃10176](https://github.com/tikv/tikv/issues/10176)の関数`json_unquote()`の間違った引数の型を修正
    -   場合によってはACIDの破壊を避けるために、正常なシャットダウン中にコールバックのクリアをスキップする[＃10353](https://github.com/tikv/tikv/issues/10353) [＃10307](https://github.com/tikv/tikv/issues/10307)
    -   Leader[＃10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正しました
    -   `DOUBLE`を`DOUBLE` [＃25200](https://github.com/pingcap/tidb/issues/25200)に変換する間違った関数を修正

-   PD

    -   複数のスケジューラ間でスケジュールの競合が発生し、期待どおりのスケジュールを生成できない問題を修正[＃3807](https://github.com/tikv/pd/issues/3807) [＃3778](https://github.com/tikv/pd/issues/3778)

-   TiFlash

    -   分割失敗によりTiFlashが再起動し続ける問題を修正
    -   TiFlashがデルタデータを削除できない潜在的な問題を修正
    -   TiFlashが`CAST`関数で非バイナリ文字に間違ったパディングを追加するバグを修正しました
    -   複雑な`GROUP BY`列の集計クエリを処理するときに誤った結果が発生する問題を修正しました
    -   書き込み圧力が高い場合に発生するTiFlashpanic問題を修正
    -   右の結合キーが null 値不可で、左の結合キーが null 値可能な場合に発生するpanicを修正しました。
    -   `read-index`リクエストに長い時間がかかる可能性がある問題を修正しました
    -   読み取り負荷が大きい場合に発生するpanic問題を修正しました
    -   `Date_Format`の関数が`STRING`番目の型引数と`NULL`値で呼び出されたときに発生する可能性のあるpanic問題を修正しました。

-   ツール

    -   TiCDC

        -   チェックポイント[＃1902](https://github.com/pingcap/tiflow/issues/1902)更新時にTiCDCオーナーが異常終了するバグを修正
        -   チェンジフィードの作成が成功した直後に失敗するバグを修正[＃2113](https://github.com/pingcap/tiflow/issues/2113)
        -   ルールフィルタ[＃1625](https://github.com/pingcap/tiflow/issues/1625)の無効なフォーマットによりchangefeedが失敗するバグを修正しました
        -   TiCDC 所有者がパニックに陥った場合の潜在的な DDL 損失の問題を修正[＃1260](https://github.com/pingcap/tiflow/issues/1260)
        -   デフォルトのソートエンジンオプション[＃2373](https://github.com/pingcap/tiflow/issues/2373)での4.0.xクラスタとのCLI互換性の問題を修正しました。
        -   TiCDCが`ErrSchemaStorageTableMiss`エラー[＃2422](https://github.com/pingcap/tiflow/issues/2422)を取得したときに、changefeedが予期せずリセットされる可能性があるバグを修正しました。
        -   TiCDCが`ErrGCTTLExceeded`エラー[＃2391](https://github.com/pingcap/tiflow/issues/2391)を取得したときにchangefeedを削除できないバグを修正
        -   TiCDCがcdclog [＃1259](https://github.com/pingcap/tiflow/issues/1259) [＃2424](https://github.com/pingcap/tiflow/issues/2424)への大きなテーブルの同期に失敗するバグを修正
        -   TiCDCがテーブル[＃2230](https://github.com/pingcap/tiflow/issues/2230)を再スケジュールしているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるバグを修正しました。

    -   バックアップと復元 (BR)

        -   BRが復元中にすべてのシステムテーブルの復元をスキップするバグを修正[＃1197](https://github.com/pingcap/br/issues/1197) [＃1201](https://github.com/pingcap/br/issues/1201)
        -   cdclog [＃870](https://github.com/pingcap/br/issues/870)を復元するときにBRが DDL 操作を見逃すバグを修正しました

    -   TiDB Lightning

        -   TiDB LightningがParquetファイル[＃1272](https://github.com/pingcap/br/pull/1272)の`DECIMAL`データ型を解析できないバグを修正しました
        -   TiDB Lightning がテーブルスキーマ[＃1290](https://github.com/pingcap/br/issues/1290)を復元するときに「エラー 9007: 書き込み競合」エラーを報告するバグを修正しました
        -   TiDB Lightningがintハンドル[＃1291](https://github.com/pingcap/br/issues/1291)のオーバーフローによりデータのインポートに失敗するバグを修正しました
        -   ローカルバックエンドモード[＃1403](https://github.com/pingcap/br/issues/1403)でのデータ損失により、 TiDB Lightningがチェックサム不一致エラーを取得する可能性があるバグを修正しました。
        -   TiDB Lightningがテーブルスキーマ[＃1362](https://github.com/pingcap/br/issues/1362)を復元する際のクラスター化インデックスとのLightningの非互換性の問題を修正

    -   Dumpling

        -   Dumpling GC セーフポイントの設定が遅すぎるためにデータのエクスポートが失敗するバグを修正[＃290](https://github.com/pingcap/dumpling/pull/290)
        -   特定のMySQLバージョン[＃322](https://github.com/pingcap/dumpling/issues/322)でアップストリームデータベースからテーブル名をエクスポートするときにDumplingがスタックする問題を修正しました
