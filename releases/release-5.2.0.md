---
title: TiDB 5.2 Release Notes
---

# TiDB 5.2 リリースノート {#tidb-5-2-release-notes}

発売日：2021年8月27日

TiDB バージョン: 5.2.0

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 5.2.x バージョンを使用することをお勧めします。

v5.2 の主な新機能と改善点は次のとおりです。

-   式インデックスでの複数の関数の使用をサポートし、クエリのパフォーマンスを大幅に向上させます。
-   オプティマイザーのカーディナリティ推定の精度を向上させ、最適な実行計画を選択できるようにします。
-   トランザクション ロック イベントを監視し、デッドロックの問題をトラブルシューティングするためのロックビュー機能の一般提供 (GA) を発表します。
-   TiFlash I/O トラフィック制限機能を追加して、 TiFlashの読み取りおよび書き込みの安定性を向上させます。
-   TiKV は、以前の RocksDB 書き込み停止メカニズムを置き換える新しいフロー制御メカニズムを導入し、TiKV フロー制御の安定性を向上させます。
-   データ移行 (DM) の運用と保守を簡素化し、管理コストを削減します。
-   TiCDC は、TiCDC タスクを管理するために HTTP プロトコル OpenAPI をサポートしています。 Kubernetes 環境とセルフホスト環境の両方に対して、よりユーザーフレンドリーな操作方法を提供します。 (Experimental機能)

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.2 にアップグレードする場合、すべての中間バージョンの互換性変更メモを知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認してください。

### システム変数 {#system-variables}

| 変数名                                                                                                       | 種類の変更    | 説明                                                                        |
| :-------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------ |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                     | 新しく追加された | サーバーがアドバタイズする認証方法を設定します。デフォルト値は`mysql_native_password`です。                 |
| [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) | 新しく追加された | 生成列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定します。デフォルト値は`OFF`です。      |
| [`tidb_opt_enable_correlation_adjustment`](/system-variables.md#tidb_opt_enable_correlation_adjustment)   | 新しく追加された | オプティマイザーが列の順序の相関に基づいて行数を推定するかどうかを制御します。デフォルト値は`ON`です。                     |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold)           | 新しく追加された | Limit 演算子または TopN 演算子を TiKV にプッシュダウンするかどうかを決定するしきい値を設定します。デフォルト値は`100`です。 |
| [`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40)    | 修正済み     | ステートメント概要テーブルがメモリに保存するステートメントの最大数を設定します。デフォルト値が`200`から`3000`に変更されました。     |
| `tidb_enable_streaming`                                                                                   | 廃止されました  | システム変数`enable-streaming`は非推奨となっており、今後使用することはお勧めできません。                     |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                                                  | 種類の変更    | 説明                                                                                                                                |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| TiDB 設定ファイル    | [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable)        | 新しく追加された | [`INFORMATION\_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロック エラー メッセージを収集するかどうかを制御します。 |
| TiDB 設定ファイル    | [`security.auto-tls`](/tidb-configuration-file.md#auto-tls)                                                                   | 新しく追加された | 起動時に TLS 証明書を自動的に生成するかどうかを決定します。デフォルト値は`false`です。                                                                                 |
| TiDB 設定ファイル    | `stmt-summary.max-stmt-count`                                                                                                 | 修正済み     | ステートメント要約テーブルに保存できる SQL カテゴリの最大数を示します。デフォルト値が`200`から`3000`に変更されました。                                                               |
| TiDB 設定ファイル    | `experimental.allow-expression-index`                                                                                         | 廃止されました  | TiDB 構成ファイルの`allow-expression-index`構成は非推奨になりました。                                                                                 |
| TiKV設定ファイル     | [`raftstore.cmd-batch`](/tikv-configuration-file.md#cmd-batch)                                                                | 新しく追加された | リクエストのバッチ処理を有効にするかどうかを制御します。これを有効にすると、書き込みパフォーマンスが大幅に向上します。デフォルト値は`true`です。                                                       |
| TiKV設定ファイル     | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)                                                  | 新しく追加された | TiKV は、特定の間隔でRaftstoreコンポーネントのレイテンシーを検査します。検査の間隔を指定する設定項目です。レイテンシーがこの値を超える場合、この検査はタイムアウトとしてマークされます。デフォルト値は`500ms`です。              |
| TiKV設定ファイル     | [`raftstore.max-peer-down-duration`](/tikv-configuration-file.md#max-peer-down-duration)                                      | 修正済み     | ピアに許可される非アクティブ期間の最長を示します。タイムアウトのあるピアは`down`としてマークされ、PD は後でそのピアを削除しようとします。デフォルト値が`5m`から`10m`に変更されました。                              |
| TiKV設定ファイル     | [`server.raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)                                         | 新しく追加された | TiKV のRaftメッセージのキュー サイズを指定します。デフォルト値は`8192`です。                                                                                    |
| TiKV設定ファイル     | [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)                                                           | 新しく追加された | フロー制御メカニズムを有効にするかどうかを決定します。デフォルト値は`true`です。                                                                                       |
| TiKV設定ファイル     | [`storage.flow-control.memtables-threshold`](/tikv-configuration-file.md#memtables-threshold)                                 | 新しく追加された | kvDB memtable の数がこのしきい値に達すると、フロー制御メカニズムが動作し始めます。デフォルト値は`5`です。                                                                     |
| TiKV設定ファイル     | [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)                                   | 新しく追加された | kvDB L0 ファイルの数がこのしきい値に達すると、フロー制御メカニズムが動作し始めます。デフォルト値は`9`です。                                                                       |
| TiKV設定ファイル     | [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) | 新しく追加された | KvDB 内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムが一部の書き込みリクエストの拒否を開始し、 `ServerIsBusy`エラーを報告します。デフォルト値は「192GB」です。                            |
| TiKV設定ファイル     | [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit) | 新しく追加された | KvDB 内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込みリクエストを拒否し、 `ServerIsBusy`エラーを報告します。デフォルト値は「1024GB」です。                             |

### その他 {#others}

-   アップグレードする前に、 [`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40)システム変数の値が`ON`であるかどうかを確認してください。値が`ON`の場合は`OFF`に設定します。そうしないと、アップグレードは失敗します。
-   v4.0 から v5.2 にアップグレードされた TiDB クラスターの場合、デフォルト値[`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)が`WARN`から`OFF`に変更されます。
-   アップグレードの前に、TiDB 構成の値を確認してください[`feedback-probability`](https://docs.pingcap.com/tidb/v5.2/tidb-configuration-file#feedback-probability) 。値が`0`でない場合、アップグレード後に「回復可能なゴルーチンのpanic」エラーが発生しますが、このエラーはアップグレードには影響しません。
-   TiDB は、 MySQL 5.7の noop 変数`innodb_default_row_format`と互換性を持つようになりました。この変数を設定しても効果はありません。 [#23541](https://github.com/pingcap/tidb/issues/23541)
-   TiDB 5.2 以降、システムのセキュリティを向上させるために、クライアントからの接続のトランスポートレイヤーを暗号化することが推奨されています (必須ではありません)。 TiDB は、TiDB で暗号化を自動的に構成して有効にする Auto TLS 機能を提供します。 Auto TLS 機能を使用するには、TiDB のアップグレード前に、TiDB 構成ファイルの[`security.auto-tls`](/tidb-configuration-file.md#auto-tls)を`true`に設定します。
-   MySQL 8.0 からの移行を容易にし、セキュリティを向上させるために`caching_sha2_password`認証方法をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   **式インデックスでの複数の関数の使用のサポート**

    式インデックスは、式に対して作成できる特殊なインデックスの一種です。式インデックスの作成後、TiDB は式ベースのクエリをサポートするため、クエリのパフォーマンスが大幅に向上します。

    [ユーザードキュメント](/sql-statements/sql-statement-create-index.md) [#25150](https://github.com/pingcap/tidb/issues/25150)

-   **Oracle の`translate`機能をサポートする**

    `translate`関数は、文字列内のすべての文字を他の文字に置き換えます。 TiDB では、この関数は Oracle のように空の文字列を`NULL`として扱いません。

    [ユーザードキュメント](/functions-and-operators/string-functions.md)

-   **HashAgg の流出をサポート**

    HashAgg のディスクへのスピルをサポートします。 HashAgg 演算子を含む SQL ステートメントによってメモリ不足 (OOM) が発生した場合、この演算子の同時実行数を`1`に設定してディスク スピルをトリガーし、メモリのストレスを軽減することができます。

    [ユーザードキュメント](/configure-memory-usage.md#other-memory-control-behaviors-of-tidb-server) [#25882](https://github.com/pingcap/tidb/issues/25882)

-   **オプティマイザのカーディナリティ推定の精度を向上させる**

    -   TiDB の TopN/Limit の推定の精度を向上させます。たとえば、条件`order by col limit x`を含む大きなテーブルに対するページネーション クエリの場合、TiDB は適切なインデックスをより簡単に選択し、クエリの応答時間を短縮できます。
    -   範囲外の推定の精度を向上させます。たとえば、1 日の統計が更新されていない場合でも、TiDB は`where date=Now()`含むクエリに対応するインデックスを正確に選択できます。
    -   `tidb_opt_limit_push_down_threshold`変数を導入して、Limit/TopN を押し下げるオプティマイザーの動作を制御します。これにより、間違った推定により、状況によっては Limit/TopN を押し下げることができない問題が解決されます。

    [ユーザードキュメント](/system-variables.md#tidb_opt_limit_push_down_threshold) [#26085](https://github.com/pingcap/tidb/issues/26085)

-   **オプティマイザーのインデックス選択を改善しました。**

    インデックス選択のためのプルーニング ルールを追加します。統計を比較に使用する前に、TiDB はこれらのルールを使用して選択可能なインデックスの範囲を絞り込み、最適でないインデックスが選択される可能性を減らします。

    [ユーザードキュメント](/choose-index.md)

### トランザクション {#transaction}

-   **Lock ビューの一般提供 (GA)**

    ロックビュー機能は、ロックの競合と悲観的ロックのロック待機に関する詳細情報を提供します。これは、DBA がトランザクション ロック イベントを観察し、デッドロックの問題をトラブルシューティングするのに役立ちます。

    v5.2 では、Lock ビューに次の機能強化が加えられています。

    -   ロック ビュー関連テーブルの SQL ダイジェスト列に加えて、対応する正規化された SQL テキストを示す列をこれらのテーブルに追加します。 SQL ダイジェストに対応するステートメントを手動でクエリする必要はありません。
    -   クラスター内の SQL ダイジェストのセットに対応する正規化された SQL ステートメント (形式と引数のない形式) をクエリする`TIDB_DECODE_SQL_DIGESTS`関数を追加します。これにより、トランザクションによって過去に実行されたステートメントをクエリする操作が簡素化されます。
    -   `DATA_LOCK_WAITS`および`DEADLOCKS`システム テーブルに列を追加して、テーブル名、行 ID、インデックス値、およびキーから解釈されたその他のキー情報を表示します。これにより、キーが属するテーブルの検索やキー情報の解釈などの操作が簡素化されます。
    -   `DEADLOCKS`テーブルでの再試行可能なデッドロック エラーの情報の収集をサポートします。これにより、そのようなエラーが原因で発生した問題のトラブルシューティングが容易になります。エラー収集はデフォルトでは無効になっていますが、 `pessimistic-txn.deadlock-history-collect-retryable`構成を使用して有効にできます。
    -   `TIDB_TRX`システム テーブル上のクエリ実行トランザクションとアイドル トランザクションの区別をサポートします。 `Normal`州は`Running`と`Idle`州に分割されました。

    ユーザードキュメント:

    -   クラスター内のすべての TiKV ノードで発生している悲観的ロック待機イベントをビュー。 [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    -   TiDB ノードで最近発生したデッドロック エラーをビュー: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    -   TiDB ノードで実行中のトランザクションをビュー: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

-   `AUTO_RANDOM`または`SHARD_ROW_ID_BITS`属性を持つテーブルにインデックスを追加するユーザー シナリオを最適化します。

### 安定性 {#stability}

-   **TiFlash I/O トラフィック制限を追加**

    この新機能は、ディスク帯域幅が小さく特定のサイズのクラウドstorageに適しています。デフォルトでは無効になっています。

    TiFlash I/O レート リミッターは、読み取りタスクと書き込みタスク間の I/O リソースの過剰な競合を回避するための新しいメカニズムを提供します。読み取りタスクと書き込みタスクへの応答のバランスをとり、読み取り/書き込みワークロードに応じて速度を自動的に制限します。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md)

-   **TiKV流量制御の安定性向上**

    TiKV では、以前の RocksDB 書き込み停止メカニズムに代わる新しいフロー制御メカニズムが導入されています。書き込み停止メカニズムと比較して、この新しいメカニズムはフォアグラウンド書き込みの安定性への影響を軽減します。

    具体的には、RocksDB 圧縮のストレスが蓄積すると、次の問題を回避するために、RocksDBレイヤーではなく TiKV スケジューラレイヤーでフロー制御が実行されます。

    -   Raftstoreがスタックします。これは、RocksDB の書き込み停止が原因です。
    -   Raftの選出がタイムアウトになり、その結果、ノード リーダーが転送されます。

    この新しいメカニズムにより、フロー制御アルゴリズムが改善され、書き込みトラフィックが多い場合の QPS の低下が軽減されます。

    [ユーザードキュメント](/tikv-configuration-file.md#storageflow-control) [#10137](https://github.com/tikv/tikv/issues/10137)

-   **クラスター内の単一の遅い TiKV ノードによる影響を自動的に検出して回復します。**

    TiKV では、低速ノード検出メカニズムが導入されています。このメカニズムは、 TiKV Raftstoreのレートを検査することでスコアを計算し、ストアのハートビートを通じてスコアを PD に報告します。一方、PD に`evict-slow-store-scheduler`スケジューラを追加して、単一の低速 TiKV ノード上のリーダーを自動的に排除します。このようにして、クラスター全体への影響が軽減されます。同時に、問題を迅速に特定して解決できるように、遅いノードに関するより多くの警告項目が導入されています。

    [ユーザードキュメント](/tikv-configuration-file.md#inspect-interval) [#10539](https://github.com/tikv/tikv/issues/10539)

### データ移行 {#data-migration}

-   **データ移行（DM）の運用を簡素化**

    DM v2.0.6 は、VIP を使用してデータ ソースの変更イベント (フェイルオーバーまたは計画変更) を自動的に識別し、新しいデータ ソース インスタンスに自動的に接続することで、データ レプリケーションのレイテンシーを短縮し、操作手順を簡素化できます。

-   TiDB Lightning は、 CSV データ内のカスタマイズされた行終端文字をサポートし、MySQL LOAD DATA CSV データ形式と互換性があります。これにより、データ フローアーキテクチャでTiDB Lightning を直接使用できるようになります。

    [#1297](https://github.com/pingcap/br/pull/1297)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

TiCDC は、HTTP プロトコル (OpenAPI) を使用した TiCDC タスクの管理をサポートしています。これは、Kubernetes 環境とセルフホスト環境の両方にとって、よりユーザーフレンドリーな操作方法です。 (Experimental機能)

[#2411](https://github.com/pingcap/tiflow/issues/2411)

### 導入と運用 {#deployment-and-operations}

Apple M1 チップを搭載した Mac コンピュータでの`tiup playground`コマンドの実行をサポートします。

## 機能強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   TiDB 用に設計されたバイナリ MQ 形式を追加します。 JSON [#1621](https://github.com/pingcap/tiflow/pull/1621)に基づくオープン プロトコルよりもコンパクトです。
        -   ファイルソーター[#2114](https://github.com/pingcap/tiflow/pull/2114)のサポートを削除
        -   ログ ローテーション構成のサポート[#2182](https://github.com/pingcap/tiflow/pull/2182)

    -   TiDB Lightning

        -   カスタマイズされた行終端記号のサポート ( `\r`と`\n`を除く) [#1297](https://github.com/pingcap/br/pull/1297)
        -   式インデックスと仮想生成列に依存するインデックスのサポート[#1407](https://github.com/pingcap/br/pull/1407)

    -   Dumpling

        -   MySQL 互換データベースのバックアップをサポートしますが、 `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE` [#311](https://github.com/pingcap/dumpling/pull/311)サポートしません

## 改善点 {#improvements}

-   TiDB

    -   組み込み関数`json_unquote()`の TiKV [#24415](https://github.com/pingcap/tidb/issues/24415)へのプッシュダウンをサポート
    -   デュアルテーブル[#25614](https://github.com/pingcap/tidb/pull/25614)からの`union`ブランチの削除をサポート
    -   集約オペレーターのコスト係数[#25241](https://github.com/pingcap/tidb/pull/25241)を最適化する
    -   MPP 外部結合がテーブル行数[#25142](https://github.com/pingcap/tidb/pull/25142)に基づいて構築テーブルを選択できるようにします。
    -   リージョン[#24724](https://github.com/pingcap/tidb/pull/24724)に基づいて、さまざまなTiFlashノード間の MPP クエリ ワークロードのバランスをサポートします。
    -   MPP クエリの実行後のキャッシュ内の古いリージョンの無効化をサポート[#24432](https://github.com/pingcap/tidb/pull/24432)
    -   書式指定子`%b/%M/%r/%T` [#25767](https://github.com/pingcap/tidb/pull/25767)の組み込み関数`str_to_date`の MySQL 互換性を向上します。
    -   同じクエリに対して異なるバインディングを再作成した後、複数の TiDB で一貫性のないバインディング キャッシュが作成される可能性がある問題を修正します[#26015](https://github.com/pingcap/tidb/pull/26015)
    -   アップグレード[#23295](https://github.com/pingcap/tidb/pull/23295)後に既存のバインディングをキャッシュにロードできない問題を修正
    -   `SHOW BINDINGS`の結果を ( `original_sql` , `update_time` ) [#26139](https://github.com/pingcap/tidb/pull/26139)で順序付けするサポート
    -   バインディングが存在する場合のクエリ最適化のロジックを改善し、クエリの最適化時間を短縮します[#26141](https://github.com/pingcap/tidb/pull/26141)
    -   「削除済み」ステータスのバインディングに対するガベージコレクションの自動完了のサポート[#26206](https://github.com/pingcap/tidb/pull/26206)
    -   `EXPLAIN VERBOSE` [#26930](https://github.com/pingcap/tidb/pull/26930)の結果でバインディングがクエリ最適化に使用されているかどうかを示すサポート
    -   新しいステータス バリエーション`last_plan_binding_update_time`を追加して、現在の TiDB インスタンスのバインディング キャッシュに対応するタイムスタンプを表示します[#26340](https://github.com/pingcap/tidb/pull/26340)
    -   バインディング進化を開始するとき、または他の機能に影響を与えるベースライン進化 (実験的機能であるため TiDB セルフホスト バージョンでは現在無効になっています) を禁止する`admin evolve bindings`を実行するときのエラー報告のサポート[#26333](https://github.com/pingcap/tidb/pull/26333)

-   PD

    -   ホットリージョンのスケジューリングに QPS ディメンションを追加し、スケジューリング[#3869](https://github.com/tikv/pd/issues/3869)の優先順位の調整をサポートします。
    -   TiFlash [#3900](https://github.com/tikv/pd/pull/3900)の書き込みホットスポットのホットリージョンバランス スケジューリングをサポート

-   TiFlash

    -   演算子の追加: `MOD / %` 、 `LIKE`
    -   文字列関数の追加: `ASCII()` 、 `COALESCE()` 、 `LENGTH()` 、 `POSITION()` 、 `TRIM()`
    -   数学関数の追加: `CONV()` 、 `CRC32()` 、 `DEGREES()` 、 `EXP()` 、 `LN()` 、 `LOG()` 、 `LOG10()` 、 `LOG2()` 、 `POW()` 、 `RADIANS()` 、 `ROUND(decimal)` 、 `SIN()` 、 `MOD()`
    -   日付関数の追加: `ADDDATE(string, real)` 、 `DATE_ADD(string, real)` 、 `DATE()`
    -   他の関数の追加: `INET_NTOA()` 、 `INET_ATON()` 、 `INET6_ATON` 、 `INET6_NTOA()`
    -   新しい照合順序が有効な場合、MPP モードでシャッフル ハッシュ結合計算とシャッフル ハッシュ集計計算をサポートします
    -   基本コードを最適化して MPP パフォーマンスを向上させる
    -   `STRING`型から`DOUBLE`型へのキャストをサポート
    -   複数のスレッドを使用して右外部結合の非結合データを最適化する
    -   MPP クエリでの古いリージョンの自動無効化のサポート

-   ツール

    -   TiCDC

        -   kv クライアント[#1899](https://github.com/pingcap/tiflow/pull/1899)の増分スキャンに同時実行制限を追加します。
        -   TiCDC は常に内部的に古い値を取得できます[#2271](https://github.com/pingcap/tiflow/pull/2271)
        -   回復不可能な DML エラーが発生すると、TiCDC が失敗し、すぐに終了する可能性がある[#1928](https://github.com/pingcap/tiflow/pull/1928)
        -   `resolve lock`リージョンが初期化された直後は実行できません[#2235](https://github.com/pingcap/tiflow/pull/2235)
        -   ワーカープールを最適化して、同時実行性が高い場合の goroutine の数を減らす[#2201](https://github.com/pingcap/tiflow/pull/2201)

    -   Dumpling

        -   TiDBメモリ[#301](https://github.com/pingcap/dumpling/pull/301)を節約するために、TiDB v3.x テーブルを常に`tidb_rowid`で分割するサポート
        -   Dumplingへのアクセスを減らす`information_schema`安定性を向上させる[#305](https://github.com/pingcap/dumpling/pull/305)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SET`型列[#25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると不正な結果が返される問題を修正
    -   `IN`式の引数[#25591](https://github.com/pingcap/tidb/issues/25591)のデータ破損の問題を修正します。
    -   GC のセッションがグローバル変数の影響を受けることを回避します[#24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリ[#25344](https://github.com/pingcap/tidb/issues/25344)で`limit`使用したときに発生するpanicの問題を修正します。
    -   `Limit` [#24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリしたときに返される間違った値を修正しました。
    -   `ENUM`または`SET`タイプの列[#24944](https://github.com/pingcap/tidb/issues/24944)に`IFNULL`が正しく反映されない問題を修正
    -   結合サブクエリの`count` `first_row` [#24865](https://github.com/pingcap/tidb/issues/24865)に変更することによって引き起こされる間違った結果を修正しました。
    -   `ParallelApply`が`TopN`演算子[#24930](https://github.com/pingcap/tidb/issues/24930)の下で使用されるときに発生するクエリハングの問題を修正します。
    -   複数列の接頭辞インデックスを使用して SQL ステートメントを実行すると、予想より多くの結果が返される問題を修正します[#24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`演算子が正しく有効にならない問題を修正[#24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列`Apply`オペレーター[#23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合問題を修正
    -   PartitionUnion 演算子[#23919](https://github.com/pingcap/tidb/issues/23919)の IndexMerge 結果を並べ替えるときに`index out of range`エラーが報告される問題を修正します。
    -   `tidb_snapshot`変数を予想外に大きな値に設定すると、トランザクション分離[#25680](https://github.com/pingcap/tidb/issues/25680)損なわれる可能性がある問題を修正します。
    -   ODBC スタイルの定数 (たとえば、 `{d '2020-01-01'}` ) を式[#25531](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正します。
    -   `SELECT DISTINCT`を`Batch Get`に変換すると誤った結果が生じる問題を修正[#25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashから TiKV へのバックオフ クエリをトリガーできない問題を修正[#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    -   `only_full_group_by` [#23839](https://github.com/pingcap/tidb/issues/23839) )のチェック時に発生する`index-out-of-range`エラーを修正
    -   相関サブクエリのインデクス結合結果が正しくない問題を修正[#25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`メトリック[#10330](https://github.com/tikv/tikv/issues/10330)を修正します
    -   コプロセッサ[#10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数の型を修正しました。
    -   場合によってはACIDの破損を避けるため、正常なシャットダウン中にコールバックのクリアをスキップします[#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    -   Leader[#10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正
    -   `DOUBLE`を`DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)にキャストする間違った関数を修正

-   PD

    -   複数のスケジューラ間でスケジュールの競合が発生し、期待したスケジュールが生成できない問題を修正[#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)

-   TiFlash

    -   スプリット障害によりTiFlashが再起動し続ける問題を修正
    -   TiFlash がデルタ データを削除できないという潜在的な問題を修正
    -   TiFlashが`CAST`関数で非バイナリ文字に間違ったパディングを追加するバグを修正
    -   複雑な`GROUP BY`列を含む集計クエリを処理するときに誤った結果が表示される問題を修正
    -   書き込み圧力が高い場合に発生するTiFlashpanicの問題を修正
    -   右のjoinキーがnull可能ではなく、左のjoinキーがnull可能な場合に発生するpanicを修正しました。
    -   `read-index`リクエストに時間がかかるという潜在的な問題を修正
    -   読み取り負荷が高いときに発生するpanicの問題を修正
    -   `Date_Format`関数が`STRING`型の引数と`NULL`値で呼び出されたときに発生する可能性があるpanicの問題を修正しました。

-   ツール

    -   TiCDC

        -   チェックポイント[#1902](https://github.com/pingcap/tiflow/issues/1902)の更新時にTiCDCオーナーが異常終了するバグを修正
        -   変更フィードの作成が成功した直後に失敗するバグを修正[#2113](https://github.com/pingcap/tiflow/issues/2113)
        -   ルールフィルター[#1625](https://github.com/pingcap/tiflow/issues/1625)の無効な形式により変更フィードが失敗するバグを修正
        -   TiCDC 所有者がパニックになった場合の潜在的な DDL 損失の問題を修正します[#1260](https://github.com/pingcap/tiflow/issues/1260)
        -   デフォルトのソートエンジンオプション[#2373](https://github.com/pingcap/tiflow/issues/2373)での 4.0.x クラスターとの CLI 互換性の問題を修正
        -   TiCDC が`ErrSchemaStorageTableMiss`エラー[#2422](https://github.com/pingcap/tiflow/issues/2422)を取得したときに変更フィードが予期せずリセットされる可能性があるバグを修正
        -   TiCDC が`ErrGCTTLExceeded`エラー[#2391](https://github.com/pingcap/tiflow/issues/2391)を取得した場合に変更フィードを削除できないバグを修正
        -   TiCDC が大きなテーブルを cdclog [#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)に同期できないというバグを修正しました。
        -   TiCDC がテーブル[#2230](https://github.com/pingcap/tiflow/issues/2230)を再スケジュールしているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるバグを修正

    -   バックアップと復元 (BR)

        -   BR が復元中にすべてのシステム テーブルの復元をスキップするバグを修正[#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        -   cdclog [#870](https://github.com/pingcap/br/issues/870)を復元するときにBR がDDL 操作を見逃すバグを修正

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイル[#1272](https://github.com/pingcap/br/pull/1272)の`DECIMAL`データ型の解析に失敗するバグを修正
        -   テーブル スキーマ[#1290](https://github.com/pingcap/br/issues/1290)の復元時にTiDB Lightning が「エラー 9007: 書き込み競合」エラーを報告するバグを修正
        -   TiDB Lightning がint ハンドル[#1291](https://github.com/pingcap/br/issues/1291)のオーバーフローによりデータのインポートに失敗するバグを修正
        -   ローカル バックエンド モード[#1403](https://github.com/pingcap/br/issues/1403)でのデータ損失により、 TiDB Lightning でチェックサム不一致エラーが発生する可能性があるバグを修正
        -   TiDB Lightning がテーブル スキーマ[#1362](https://github.com/pingcap/br/issues/1362)を復元するときの、クラスター化インデックスとの Lightning の非互換性の問題を修正します。

    -   Dumpling

        -   Dumpling GC セーフポイントの設定が遅すぎるためにデータのエクスポートが失敗するバグを修正[#290](https://github.com/pingcap/dumpling/pull/290)
        -   特定の MySQL バージョン[#322](https://github.com/pingcap/dumpling/issues/322)でアップストリーム データベースからテーブル名をエクスポートするときにDumplingがスタックする問題を修正しました。
