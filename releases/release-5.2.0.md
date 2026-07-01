---
title: TiDB 5.2 Release Notes
summary: TiDB 5.2.0では、式インデックスのサポート、Lock ビュー GA、 TiFlashのI/Oトラフィック制限など、新機能と改善点が導入されています。互換性の変更点としては、新しいシステム変数と構成ファイルパラメータが追加されています。また、TiDB、TiKV、 TiFlash、およびTiCDC、 BR、Lightning、 Dumplingなどのツールに対するバグ修正と機能強化も含まれています。
---

# TiDB 5.2 リリースノート {#tidb-5-2-release-notes}

発売日：2021年8月27日

TiDB バージョン: 5.2.0

> **警告：**
>
> このバージョンには既知の不具合がいくつかあり、これらの不具合は新しいバージョンで修正されています。最新の5.2.xバージョンをご利用いただくことをお勧めします。

バージョン5.2の主な新機能と改善点は以下のとおりです。

-   式インデックスで複数の関数を使用することをサポートし、クエリのパフォーマンスを大幅に向上させます。
-   最適な実行プランの選択を支援するために、オプティマイザのカーディナリティ推定の精度を向上させる。
-   トランザクションのロックイベントを監視し、デッドロックの問題をトラブルシューティングするためのロックビュー機能の一般提供（GA）を発表します。
-   TiFlashの読み書きの安定性を向上させるため、 TiFlash I/Oトラフィック制限機能を追加しました。
-   TiKVは、従来のRocksDB書き込み停止メカニズムに代わる新しいフロー制御メカニズムを導入し、TiKVフロー制御の安定性を向上させています。
-   データ移行（DM）の運用と保守を簡素化し、管理コストを削減する。
-   TiCDCは、TiCDCタスクの管理にHTTPプロトコルOpenAPIをサポートしています。これにより、Kubernetes環境とセルフホスト環境の両方において、よりユーザーフレンドリーな操作方法を提供します。（Experimental機能）

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.2 にアップグレードする場合、中間バージョンの互換性変更点を確認したい場合は、該当バージョンの[リリースノート](/releases/_index.md)を参照してください。

### システム変数 {#system-variables}

| 変数名                                                                                                       | 変更の種類  | 説明                                                                     |
| :-------------------------------------------------------------------------------------------------------- | :------- | :--------------------------------------------------------------------- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                     | 新しく追加された | サーバーが公開する認証方法を設定します。デフォルト値は`mysql_native_password`です。                  |
| [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) | 新しく追加された | 生成列または式インデックスを作成する際に`AUTO_INCREMENT`列を含めるかどうかを決定します。デフォルト値は`OFF`です。    |
| [`tidb_opt_enable_correlation_adjustment`](/system-variables.md#tidb_opt_enable_correlation_adjustment)   | 新しく追加された | オプティマイザが列の順序相関に基づいて行数を推定するかどうかを制御します。デフォルト値は`ON`です。                    |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold)           | 新しく追加された | Limit または TopN 演算子を TiKV にプッシュするかどうかを決定するしきい値を設定します。デフォルト値は`100`です。    |
| [`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40)    | 変更     | ステートメントサマリーテーブルがメモリに格納するステートメントの最大数を設定します。デフォルト値は`200`から`3000`に変更されます。 |
| `tidb_enable_streaming`                                                                                   | 非推奨      | システム変数`enable-streaming`は非推奨であり、今後は使用しないことをお勧めします。                     |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションアイテム                                                                                                                | 変更の種類  | 説明                                                                                                                              |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------ |
| TiDB設定ファイル     | [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable)        | 新しく追加された | [`INFORMATION\_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロックエラーメッセージを収集するかどうかを制御します。 |
| TiDB設定ファイル     | [`security.auto-tls`](/tidb-configuration-file.md#auto-tls)                                                                   | 新しく追加された | 起動時にTLS証明書を自動的に生成するかどうかを決定します。デフォルト値は`false`です。                                                                                 |
| TiDB設定ファイル     | `stmt-summary.max-stmt-count`                                                                                                 | 変更     | ステートメントサマリーテーブルに保存できるSQLカテゴリの最大数を示します。デフォルト値は`200`から`3000`に変更されます。                                                              |
| TiDB設定ファイル     | `experimental.allow-expression-index`                                                                                         | 非推奨      | TiDB 設定ファイル内の`allow-expression-index`設定は非推奨です。                                                                                  |
| TiKV設定ファイル     | [`raftstore.cmd-batch`](/tikv-configuration-file.md#cmd-batch)                                                                | 新しく追加された | リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。デフォルト値は`true`です。                                                        |
| TiKV設定ファイル     | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                  | 新しく追加された | TiKV は一定間隔でRaftstoreコンポーネントのレイテンシーを検査します。この設定項目は検査間隔を指定します。レイテンシーがこの値を超えると、この検査はタイムアウトとしてマークされます。デフォルト値は`500ms`です。              |
| TiKV設定ファイル     | [`raftstore.max-peer-down-duration`](/tikv-configuration-file.md#max-peer-down-duration)                                      | 変更     | ピアに許可される最長の非アクティブ期間を示します。タイムアウトしたピアは`down`とマークされ、PD は後でそれを削除しようとします。デフォルト値は`5m`から`10m`に変更されます。                                  |
| TiKV設定ファイル     | [`server.raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                                         | 新しく追加された | TiKV のRaftメッセージのキュー サイズを指定します。デフォルト値は`8192`です。                                                                                  |
| TiKV設定ファイル     | [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)                                                           | 新しく追加された | フロー制御メカニズムを有効にするかどうかを決定します。デフォルト値は`true`です。                                                                                     |
| TiKV設定ファイル     | [`storage.flow-control.memtables-threshold`](/tikv-configuration-file.md#memtables-threshold)                                 | 新しく追加された | kvDB の memtable の数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。デフォルト値は`5`です。                                                                |
| TiKV設定ファイル     | [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                   | 新しく追加された | kvDB L0 ファイルの数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。デフォルト値は`9`です。                                                                    |
| TiKV設定ファイル     | [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 新しく追加された | KvDB の保留中の圧縮バイト数がこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し、 `ServerIsBusy`エラーを報告します。デフォルト値は「192GB」です。                                |
| TiKV設定ファイル     | [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit) | 新しく追加された | KvDB の保留中の圧縮バイト数がこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`エラーを報告します。デフォルト値は「1024GB」です。                              |

### その他 {#others}

-   アップグレードの前に、 [`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40)システム変数の値が`ON`であるかどうかを確認してください。値が`ON`の場合は、 `OFF`に設定してください。そうでない場合、アップグレードは失敗します。
-   TiDB クラスターを v4.0 から v5.2 にアップグレードすると、 [`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)のデフォルト値が`WARN`から`OFF`に変更されます。
-   アップグレード前に、TiDB 設定の[`feedback-probability`](https://docs-archive.pingcap.com/tidb/v5.2/tidb-configuration-file#feedback-probability)の値を確認してください。値が`0`でない場合、アップグレード後に「回復可能なゴルーチンでpanicが発生しました」というエラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDBはMySQL 5.7のnoop変数`innodb_default_row_format`と互換性を持つようになりました。この変数を設定しても効果はありません。 [#23541](https://github.com/pingcap/tidb/issues/23541)
-   TiDB 5.2以降では、システムセキュリティを向上させるため、クライアントからの接続のトランスレイヤーを暗号化することが推奨されています（必須ではありません）。TiDBは、TiDB内で暗号化を自動的に構成および有効化するAuto TLS機能を提供します。Auto TLS機能を使用するには、TiDBのアップグレード前に、TiDB構成ファイルの[`security.auto-tls`](/tidb-configuration-file.md#auto-tls)を`true`に設定してください。
-   MySQL 8.0 からの移行を容易にし、セキュリティを向上させるために、 `caching_sha2_password`認証方式をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   **式インデックスで複数の関数を使用することをサポートします。**

    式インデックスは、式に基づいて作成できる特殊なインデックスの一種です。式インデックスが作成されると、TiDBは式ベースのクエリをサポートし、クエリのパフォーマンスを大幅に向上させます。

    [ユーザー向けドキュメント](/sql-statements/sql-statement-create-index.md)、 [#25150](https://github.com/pingcap/tidb/issues/25150)

-   **Oracleの`translate`機能をサポートする**

    `translate`関数は、文字列内のすべての文字を他の文字に置き換えます。TiDB では、この関数は Oracle のように空文字列を`NULL`として扱いません。

    [ユーザー向けドキュメント](/functions-and-operators/string-functions.md)

-   **HashAggのスピルをサポート**

    HashAgg をディスクに書き出す機能をサポートします。HashAgg 演算子を含む SQL ステートメントでメモリ不足 (OOM) が発生した場合、この演算子の同時実行数を`1`に設定してディスクへの書き出しをトリガーし、メモリ負荷を軽減することができます。

    [ユーザー向けドキュメント](/configure-memory-usage.md#other-memory-control-behaviors-of-tidb-server)、 [#25882](https://github.com/pingcap/tidb/issues/25882)

-   **オプティマイザのカーディナリティ推定の精度を向上させる**

    -   TiDBのTopN/Limit推定精度を向上させます。例えば、 `order by col limit x`条件を含む大規模テーブルに対するページネーションクエリの場合、TiDBは適切なインデックスをより容易に選択し、クエリ応答時間を短縮できます。
    -   範囲外推定の精度を向上させます。たとえば、1 日の統計情報が更新されていなくても、TiDB は`where date=Now()`を含むクエリに対して対応するインデックスを正確に選択できます。
    -   オプティマイザが Limit/TopN を押し下げる動作を制御するために`tidb_opt_limit_push_down_threshold`変数を導入します。これにより、誤った推定のために一部の状況で Limit/TopN を押し下げることができないという問題が解決されます。

    [ユーザー向けドキュメント](/system-variables.md#tidb_opt_limit_push_down_threshold)、 [#26085](https://github.com/pingcap/tidb/issues/26085)

-   **オプティマイザのインデックス選択を改善する**

    インデックス選択のためのプルーニングルールを追加します。TiDBは、比較統計を使用する前に、これらのルールを使用して選択可能なインデックスの範囲を絞り込み、最適でないインデックスを選択する可能性を低減します。

    [ユーザー向けドキュメント](/choose-index.md)

### トランザクション {#transaction}

-   **Lock ビューの一般提供開始（GA）**

    ロックビュー機能は、悲観的ロックのロック競合とロック待機に関する詳細情報を提供し、DBAがトランザクションのロックイベントを監視し、デッドロックの問題をトラブルシューティングするのに役立ちます。

    バージョン5.2では、ロックビューに以下の機能強化が加えられました。

    -   ロックビュー関連テーブルのSQLダイジェスト列に加えて、対応する正規化されたSQLテキストを表示する列をこれらのテーブルに追加してください。SQLダイジェストに対応するステートメントを手動でクエリする必要はありません。
    -   `TIDB_DECODE_SQL_DIGESTS`関数を追加して、クラスタ内の一連の SQL ダイジェストに対応する正規化された SQL ステートメント (フォーマットや引数のない形式) を照会します。これにより、トランザクションによって過去に実行されたステートメントの照会操作が簡素化されます。
    -   `DATA_LOCK_WAITS`および`DEADLOCKS`システム テーブルに、テーブル名、行 ID、インデックス値、およびキーから解釈されるその他のキー情報を表示する列を追加します。これにより、キーが属するテーブルの検索やキー情報の解釈などの操作が簡素化されます。
    -   `DEADLOCKS`テーブルで再試行可能なデッドロック エラーの情報を収集する機能をサポートします。これにより、そのようなエラーによって発生する問題のトラブルシューティングが容易になります。エラー収集はデフォルトでは無効になっており、 `pessimistic-txn.deadlock-history-collect-retryable`設定を使用して有効にできます。
    -   `TIDB_TRX`システム テーブルで、クエリ実行中のトランザクションとアイドル状態のトランザクションを区別できるようにしました。 `Normal`状態は`Running`と`Idle`の状態に分割されました。

    ユーザー向けドキュメント：

    -   クラスタ内のすべての TiKV ノードで発生している悲観的ロック待機イベントを確認する: [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDBノードで最近発生したデッドロックエラーを確認する: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDBノードで実行中のトランザクションを確認する: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

-   `AUTO_RANDOM`または`SHARD_ROW_ID_BITS`属性を持つテーブルにインデックスを追加するユーザーシナリオを最適化します。

### 安定性 {#stability}

-   **TiFlashのI/Oトラフィック制限を追加する**

    この新機能は、ディスク帯域幅が小さく特定のサイズのクラウドストレージに適しています。デフォルトでは無効になっています。

    TiFlash I/Oレートリミッターは、読み取りタスクと書き込みタスク間のI/Oリソースの過剰な競合を回避するための新しいメカニズムを提供します。読み取りタスクと書き込みタスクへの応答のバランスを取り、読み取り/書き込みワークロードに応じてレートを自動的に制限します。

    [ユーザー向けドキュメント](/tiflash/tiflash-configuration.md)

-   **TiKV流量制御の安定性を向上させる**

    TiKVは、従来のRocksDBの書き込み停止メカニズムに代わる新しいフロー制御メカニズムを導入しました。この新しいメカニズムは、従来の書き込み停止メカニズムと比較して、フォアグラウンド書き込みの安定性への影響を軽減します。

    具体的には、RocksDBの圧縮による負荷が蓄積した場合、以下の問題を回避するために、RocksDBレイヤーではなくTiKVスケジューラレイヤーでフロー制御が実行されます。

    -   Raftstoreが停止していますが、これはRocksDBの書き込み停止が原因です。
    -   Raftの選挙がタイムアウトし、その結果、ノードリーダーが移管されます。

    この新しいメカニズムは、書き込みトラフィックが多い場合にQPS（1秒あたりのクエリ数）が低下するのを軽減するために、フロー制御アルゴリズムを改善します。

    [ユーザー向けドキュメント](/tikv-configuration-file.md#storageflow-control)、 [#10137](https://github.com/tikv/tikv/issues/10137)

-   **クラスタ内の単一の低速なTiKVノードによって引き起こされる影響を自動的に検出し、復旧する**

    TiKVは、スローノード検出メカニズムを導入しました。このメカニズムは、TiKV Raftstoreのレートを検査してスコアを計算し、ストアハートビートを通じてPDにスコアを報告します。同時に、PDに`evict-slow-store-scheduler`スケジューラを追加し、単一のスローTiKVノード上のリーダーを自動的に排除します。これにより、クラスタ全体への影響が軽減されます。また、スローノードに関するアラート項目がさらに追加され、問題の迅速な特定と解決に役立ちます。

    [ユーザー向けドキュメント](/tikv-configuration-file.md#inspect-interval)、 [#10539](https://github.com/tikv/tikv/issues/10539)

### データ移行 {#data-migration}

-   **データ移行（DM）の作業を簡素化する**

    DM v2.0.6は、VIPを使用してデータソースの変更イベント（フェイルオーバーまたはプラン変更）を自動的に識別し、新しいデータソースインスタンスに自動的に接続することで、データレプリケーションのレイテンシーを削減し、操作手順を簡素化できます。

-   TiDB Lightningは、CSVデータにおけるカスタム改行文字をサポートしており、MySQLのLOAD DATA CSVデータ形式と互換性があります。そのため、データフローアーキテクチャ内でTiDB Lightningを直接使用できます。

    [#1297](https://github.com/pingcap/br/pull/1297)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

TiCDCは、HTTPプロトコル（OpenAPI）を使用してTiCDCタスクを管理する機能をサポートしており、Kubernetes環境とセルフホスト環境の両方において、よりユーザーフレンドリーな操作方法を提供します。（Experimental機能）

[#2411](https://github.com/pingcap/tiflow/issues/2411)

### 展開と運用 {#deployment-and-operations}

Apple M1チップを搭載したMacコンピュータで`tiup playground`コマンドを実行することをサポートします。

## 機能強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   TiDB向けに設計されたバイナリMQフォーマットを追加します。これはJSONベースのオープンプロトコルよりもコンパクトです。 [#1621](https://github.com/pingcap/tiflow/pull/1621)
        -   ファイルソーターのサポートを削除 [#2114](https://github.com/pingcap/tiflow/pull/2114)
        -   ログローテーション構成のサポート [#2182](https://github.com/pingcap/tiflow/pull/2182)

    -   TiDB Lightning

        -   カスタム行末文字のサポート（ `\r`および`\n`を除く） [#1297](https://github.com/pingcap/br/pull/1297)
        -   式インデックスと仮想生成列に依存するインデックスのサポート [#1407](https://github.com/pingcap/br/pull/1407)

    -   Dumpling

        -   MySQL互換データベースのバックアップをサポートしますが、 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`はサポートしません [#311](https://github.com/pingcap/dumpling/pull/311)

## 改善点 {#improvements}

-   TiDB

    -   TiKV への組み込み関数`json_unquote()`のプッシュダウンをサポートする [#24415](https://github.com/pingcap/tidb/issues/24415)
    -   デュアルテーブルから`union`ブランチを削除することをサポートします [#25614](https://github.com/pingcap/tidb/pull/25614)
    -   集約事業者のコスト係数を最適化する [#25241](https://github.com/pingcap/tidb/pull/25241)
    -   MPP外部結合で、テーブルの行数に基づいて構築テーブルを選択できるようにする [#25142](https://github.com/pingcap/tidb/pull/25142)
    -   リージョンに基づいて、異なるTiFlashノード間でMPPクエリワークロードのバランスを取ることをサポートする [#24724](https://github.com/pingcap/tidb/pull/24724)
    -   MPPクエリ実行後にキャッシュ内の古いリージョンを無効化する機能をサポートする [#24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子`str_to_date`に対する組み込み関数`%b/%M/%r/%T` } の MySQL 互換性を向上させる [#25767](https://github.com/pingcap/tidb/pull/25767)
    -   同じクエリに対して異なるバインディングを再作成した後に、複数の TiDB で一貫性のないバインディング キャッシュが作成される可能性がある問題を修正します [#26015](https://github.com/pingcap/tidb/pull/26015)
    -   アップグレード後に既存のバインディングをキャッシュにロードできない問題を修正しました [#23295](https://github.com/pingcap/tidb/pull/23295)
    -   `SHOW BINDINGS`の結果を ( `original_sql` 、 `update_time` ) で並べ替えることをサポートする [#26139](https://github.com/pingcap/tidb/pull/26139)
    -   バインディングが存在する場合のクエリ最適化ロジックを改善し、クエリの最適化時間を短縮する [#26141](https://github.com/pingcap/tidb/pull/26141)
    -   「削除済み」ステータスのバインディングに対してガベージコレクションを自動的に完了する機能をサポートする [#26206](https://github.com/pingcap/tidb/pull/26206)
    -   `EXPLAIN VERBOSE`の結果で、バインディングがクエリ最適化に使用されているかどうかを表示する機能のサポート [#26930](https://github.com/pingcap/tidb/pull/26930)
    -   現在の TiDB インスタンスのバインディング キャッシュに対応するタイムスタンプを表示するための新しいステータス バリエーション`last_plan_binding_update_time`を追加します [#26340](https://github.com/pingcap/tidb/pull/26340)
    -   バインディング進化の開始時、またはベースライン進化を禁止する`admin evolve bindings`実行時にエラーを報告する機能をサポートする（現在、実験的機能であるため、TiDB Self-Managed バージョンでは無効になっている）。これにより、他の機能に影響が出る。 [#26333](https://github.com/pingcap/tidb/pull/26333)

-   PD

    -   ホットリージョンスケジューリングにQPSディメンションを追加し、スケジューリングの優先度調整をサポートします [#3869](https://github.com/tikv/pd/issues/3869)
    -   TiFlashの書き込みホットスポットにおけるホットリージョンバランススケジューリングのサポート [#3900](https://github.com/tikv/pd/pull/3900)

-   TiFlash

    -   演算子を追加します: `MOD / %` 、 `LIKE`
    -   文字列関数を追加します: `ASCII()` 、 `COALESCE()` 、 `LENGTH()` 、 `POSITION()` 、 `TRIM()`
    -   数学関数を追加します: `CONV()` 、 `CRC32()` 、 `DEGREES()` 、 `EXP()` 、 `LN()` 、 `LOG()` 、 `LOG10()` 、 `LOG2()` 、 `POW()` 、 `RADIANS()` 、 `ROUND(decimal)` 、 `SIN()` 、 `MOD()`
    -   日付関数を追加します: `ADDDATE(string, real)` 、 `DATE_ADD(string, real)` 、 `DATE()`
    -   その他の関数を追加します: `INET_NTOA()` 、 `INET_ATON()` 、 `INET6_ATON` 、 `INET6_NTOA()`
    -   新しい照合順序が有効になっている場合、MPP モードでシャッフル ハッシュ結合計算とシャッフル ハッシュ集計計算をサポートします。
    -   MPPのパフォーマンスを向上させるために基本コードを最適化します
    -   `STRING`型から`DOUBLE`型へのキャストをサポートします。
    -   複数のスレッドを使用して、右外部結合における非結合データを最適化する
    -   MPPクエリにおける古いリージョンの自動無効化をサポートする

-   ツール

    -   TiCDC

        -   kvクライアントの増分スキャンに同時実行制限を追加する [#1899](https://github.com/pingcap/tiflow/pull/1899)
        -   TiCDCは常に内部的に古い値を取得できる [#2271](https://github.com/pingcap/tiflow/pull/2271)
        -   TiCDCは、回復不能なDMLエラーが発生するとすぐに失敗して終了する可能性がある [#1928](https://github.com/pingcap/tiflow/pull/1928)
        -   `resolve lock`リージョンの初期化直後には実行できません [#2235](https://github.com/pingcap/tiflow/pull/2235)
        -   高並行処理時のゴルーチン数を削減するためにワーカープールを最適化する [#2201](https://github.com/pingcap/tiflow/pull/2201)

    -   Dumpling

        -   TiDB v3.x テーブルを常に`tidb_rowid`で分割して TiDBメモリを節約するサポート [#301](https://github.com/pingcap/dumpling/pull/301)
        -   安定性を向上させるため、Dumplingの`information_schema`へのアクセスを減らします [#305](https://github.com/pingcap/dumpling/pull/305)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `SET`型の列でマージ結合を使用した場合に誤った結果が返される問題を修正しました [#25669](https://github.com/pingcap/tidb/issues/25669)
    -   `IN`式の引数におけるデータ破損の問題を修正しました [#25591](https://github.com/pingcap/tidb/issues/25591)
    -   GCセッションがグローバル変数の影響を受けないようにする [#24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリで`limit`を使用した場合に発生するpanic問題を修正しました [#25344](https://github.com/pingcap/tidb/issues/25344)
    -   `Limit`を使用してパーティションテーブルをクエリしたときに返される誤った値を修正する [#24636](https://github.com/pingcap/tidb/issues/24636)
    -   `IFNULL`が`ENUM`または`SET`タイプの列に正しく適用されない問題を修正します。 [#24944](https://github.com/pingcap/tidb/issues/24944)
    -   結合サブクエリ内の`count`を`first_row`に変更したことで発生した誤った結果を修正します [#24865](https://github.com/pingcap/tidb/issues/24865)
    -   `ParallelApply`演算子の下で`TopN`を使用した場合に発生するクエリのハング問題を修正します [#24930](https://github.com/pingcap/tidb/issues/24930)
    -   複数列プレフィックスインデックスを使用したSQLステートメントの実行時に、予想よりも多くの結果が返される問題を修正しました [#24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`演算子が正しく機能しない問題を修正しました [#24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列演算子`Apply`のデータ競合問題を修正 [#23280](https://github.com/pingcap/tidb/issues/23280)
    -   PartitionUnion 演算子の IndexMerge 結果をソートする際に`index out of range`エラーが報告される問題を修正しました [#23919](https://github.com/pingcap/tidb/issues/23919)
    -   `tidb_snapshot`変数に予想外に大きな値を設定するとトランザクション分離が損なわれる可能性がある問題を修正しました [#25680](https://github.com/pingcap/tidb/issues/25680)
    -   ODBC スタイルの定数 (例: `{d '2020-01-01'}` ) を式として使用できない問題を修正しました [#25531](https://github.com/pingcap/tidb/issues/25531)
    -   `SELECT DISTINCT` `Batch Get`に変換されることで誤った結果が生じる問題を修正します [#25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashからTiKVへのバックオフクエリがトリガーできない問題を修正[#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    -   `index-out-of-range`をチェックした際に発生する`only_full_group_by`エラーを修正します[#23839](https://github.com/pingcap/tidb/issues/23839) )
    -   相関サブクエリにおけるインデックス結合の結果が間違っている問題を修正しました [#25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   誤った`tikv_raftstore_hibernated_peer_state`メトリック [#10330](https://github.com/tikv/tikv/issues/10330)を修正
    -   コプロセッサ内の`json_unquote()`関数の引数の型が間違っている問題を修正 [#10176](https://github.com/tikv/tikv/issues/10176)
    -   場合によってはACIDが損なわれるのを避けるため、正常シャットダウン時にクリアリングコールバックをスキップする[#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    -   Leader上でレプリカ読み取り時に読み取りインデックスが共有されるバグを修正 [#10347](https://github.com/tikv/tikv/issues/10347)
    -   `DOUBLE`を`DOUBLE`にキャストする誤った関数を修正 [#25200](https://github.com/pingcap/tidb/issues/25200)

-   PD

    -   複数のスケジューラ間のスケジューリング競合により、期待されるスケジューリングが生成できない問題を修正します[#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)

-   TiFlash

    -   分割エラーが原因でTiFlashが再起動を繰り返す問題を修正します。
    -   TiFlashがデルタデータを削除できない可能性のある問題を修正します。
    -   TiFlashが`CAST`関数で非バイナリ文字に誤ったパディングを追加するバグを修正しました。
    -   複雑な`GROUP BY`列を含む集計クエリを処理する際に、結果が正しくない問題を修正しました。
    -   書き込み負荷が高い場合に発生するTiFlashpanic問題を修正します。
    -   右側の結合キーがnull許容でなく、左側の結合キーがnull許容である場合に発生するpanicを修正します。
    -   `read-index`リクエストの処理に時間がかかる可能性がある問題を修正します。
    -   読み込み負荷が高いときに発生するpanic問題を修正します。
    -   `Date_Format`panicが`STRING`型の引数と`NULL`の値で呼び出されたときに発生する可能性のあるパニック問題を修正します。

-   ツール

    -   TiCDC

        -   TiCDCのオーナーがチェックポイントを更新する際に異常終了するバグを修正しました [#1902](https://github.com/pingcap/tiflow/issues/1902)
        -   変更フィードが正常に作成された直後に失敗するバグを修正 [#2113](https://github.com/pingcap/tiflow/issues/2113)
        -   ルールフィルターの形式が不正なためにchangefeedが失敗するバグを修正しました [#1625](https://github.com/pingcap/tiflow/issues/1625)
        -   TiCDCオーナーがパニックになった際に発生する可能性のあるDDL損失問題を修正 [#1260](https://github.com/pingcap/tiflow/issues/1260)
        -   デフォルトのソートエンジンオプションにおける4.0.xクラスターとのCLI互換性の問題を修正 [#2373](https://github.com/pingcap/tiflow/issues/2373)
        -   TiCDCが`ErrSchemaStorageTableMiss`エラー [#2422](https://github.com/pingcap/tiflow/issues/2422)を受け取った際に、changefeedが予期せずリセットされる可能性があるバグを修正しました。
        -   TiCDC `ErrGCTTLExceeded`エラー [#2391](https://github.com/pingcap/tiflow/issues/2391)を受け取った際にchangefeedを削除できないバグを修正しました。
        -   TiCDCが大きなテーブルをcdclogに同期できないバグを修正[#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)
        -   TiCDCがテーブルを再スケジュールしている際に、複数のプロセッサが同じテーブルにデータを書き込む可能性があるバグを修正しました [#2230](https://github.com/pingcap/tiflow/issues/2230)

    -   Backup & Restore (BR)

        -   BRが復元時にすべてのシステムテーブルの復元をスキップするバグを修正[#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        -   CDclog復元時にBRがDDL操作を見逃すバグを修正 [#870](https://github.com/pingcap/br/issues/870)

    -   TiDB Lightning

        -   TiDB LightningがParquetファイル内の`DECIMAL`データ型を解析できないバグを修正しました [#1272](https://github.com/pingcap/br/pull/1272)
        -   TiDB Lightningがテーブルスキーマの復元時に「エラー9007：書き込み競合」エラーを報告するバグを修正しました [#1290](https://github.com/pingcap/br/issues/1290)
        -   intハンドルのオーバーフローが原因でTiDB Lightningがデータをインポートできないバグを修正しました [#1291](https://github.com/pingcap/br/issues/1291)
        -   TiDB Lightningでローカルバックエンドモードでのデータ損失によりチェックサム不一致エラーが発生する可能性があるバグを修正しました [#1403](https://github.com/pingcap/br/issues/1403)
        -   TiDB Lightningがテーブルスキーマを復元する際に、クラスター化インデックスとのLightning互換性の問題を修正する [#1362](https://github.com/pingcap/br/issues/1362)

    -   Dumpling

        -   Dumpling GCのセーフポイントの設定が遅すぎるためにデータエクスポートが失敗するバグを修正しました [#290](https://github.com/pingcap/dumpling/pull/290)
        -   特定のMySQLバージョンで、アップストリームデータベースからテーブル名をエクスポートする際にDumplingが停止する問題を修正しました [#322](https://github.com/pingcap/dumpling/issues/322)
