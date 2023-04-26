---
title: TiDB 2.1.17 Release Notes
---

# TiDB 2.1.17 リリースノート {#tidb-2-1-17-release-notes}

発売日：2019年9月11日

TiDB バージョン: 2.1.17

TiDB アンシブル バージョン: 2.1.17

-   新機能
    -   TiDB の`SHOW TABLE REGIONS`構文に`WHERE`句を追加します
    -   TiKV と PD に`config-check`機能を追加して、構成項目を確認します。
    -   pd-ctl に`remove-tombstone`コマンドを追加して、廃棄ストアのレコードをクリアします
    -   Reparoに`worker-count`と`txn-batch`構成項目を追加して、回復速度を制御します

-   改良点
    -   オペレーターの積極的なプッシュをサポートすることで、PD のスケジューリング プロセスを最適化します。
    -   TiKV の起動プロセスを最適化して、ノードの再起動によって発生するジッターを減らします

-   行動の変化
    -   前回の再試行時刻から最初の実行時刻までの TiDB スロー クエリ ログの`start ts`を変更します。
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`フィールドに置き換えて、スロー クエリ ログの使いやすさを向上させます。
    -   TiDB の構成ファイルに`split-region-max-num`パラメーターを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。これは、デフォルト構成で 1,000 から 10,000 に増加します。

## TiDB {#tidb}

-   SQL オプティマイザー
    -   `EvalSubquery`建造中にエラーが発生した場合、エラーメッセージが正しく返ってこない問題を修正`Executor` [#11811](https://github.com/pingcap/tidb/pull/11811)
    -   インデックス参照結合で、外部テーブルの行数が 1 バッチの行数よりも多い場合、クエリの結果が正しくない場合がある問題を修正しました。 Index Lookup Join の機能範囲を拡張します。 `UnionScan` `IndexJoin` [#11843](https://github.com/pingcap/tidb/pull/11843)のサブノードとして使用できます
    -   無効なキー ( `invalid encoded key flag 252`など) の表示を`SHOW STAT_BUCKETS`構文に追加し、統計フィードバック プロセス中に無効なキーが発生する可能性がある状況に備えます[#12098](https://github.com/pingcap/tidb/pull/12098)
-   SQL 実行エンジン
    -   `CAST`関数が数値型[#11712](https://github.com/pingcap/tidb/pull/11712)を変換しているときに、最初に`UINT`に変換される数値によって引き起こされる、いくつかの誤った結果 ( `select cast(13835058000000000000 as double)`など) を修正します。
    -   `DIV`計算の被除数が小数で、この計算に負の数[#11812](https://github.com/pingcap/tidb/pull/11812)含まれている場合、計算結果が正しくない場合がある問題を修正
    -   `ConvertStrToIntStrict`関数を追加して、 `SELECT` / `EXPLAIN`ステートメントの実行時に一部の文字列が`INT`型に変換されることによって発生する MySQL の非互換性の問題を修正します[#11892](https://github.com/pingcap/tidb/pull/11892)
    -   `EXPLAIN ... FOR CONNECTION`を使用すると`stmtCtx`の構成が間違っているために`Explain`結果が正しくない場合がある問題を修正[#11978](https://github.com/pingcap/tidb/pull/11978)
    -   `unaryMinus`関数で返される結果が MySQL と互換性がない問題を修正します。これは、整数の結果がオーバーフローしたときに非 10 進数の結果が原因で発生します[#11990](https://github.com/pingcap/tidb/pull/11990)
    -   `LOAD DATA`ステートメント実行時のカウント順により`last_insert_id()`が正しくない場合がある問題を修正[#11994](https://github.com/pingcap/tidb/pull/11994)
    -   ユーザーが自動インクリメント列データを明示的および暗黙的な混合方法で書き込むと、 `last_insert_id()`が正しくない可能性がある問題を修正します[#12001](https://github.com/pingcap/tidb/pull/12001)
    -   `JSON_UNQUOTE`関数のオーバークォートのバグを修正: 二重引用符 ( `"` ) で囲まれた値のみを引用解除する必要があります。たとえば、「 `SELECT JSON_UNQUOTE("\\\\")` 」の結果は「 `\\` 」になるはずです (変更なし) [#12096](https://github.com/pingcap/tidb/pull/12096)
-   サーバ
    -   TiDB トランザクション[#11878](https://github.com/pingcap/tidb/pull/11878)を再試行すると、最後の再試行時刻から最初の実行時刻までのスロー クエリ ログに記録される変更`start ts`
    -   トランザクションのキーの数を`LockResolver`に追加して、リージョン全体でのスキャン操作を回避し、キーの数が減ったときにロックを解決するためのコストを削減します[#11889](https://github.com/pingcap/tidb/pull/11889)
    -   スロー クエリ ログ[#11886](https://github.com/pingcap/tidb/pull/11886)で`succ`フィールド値が正しくない可能性がある問題を修正します。
    -   スロー クエリ ログの`Index_ids`フィールドを`Index_names`フィールドに置き換えて、スロー クエリ ログ[#12063](https://github.com/pingcap/tidb/pull/12063)の使いやすさを向上させます。
    -   `Duration` `-` ( `select time(‘--’)`など) が含まれている場合、TiDB が`-` EOF エラーに解析することによって発生する接続切断の問題を修正します[#11910](https://github.com/pingcap/tidb/pull/11910)
    -   無効なリージョンを`RegionCache`からより迅速に削除して、このリージョン[#11931](https://github.com/pingcap/tidb/pull/11931)に送信されるリクエストの数を減らします
    -   `oom-action = "cancel"`および`Insert Into … Select`構文で OOM が発生した場合の OOMpanic問題の不適切な処理によって引き起こされる接続切断の問題を修正します[#12126](https://github.com/pingcap/tidb/pull/12126)
-   DDL
    -   `tikvSnapshot`のリバース スキャン インターフェイスを追加して、DDL 履歴ジョブを効率的にクエリします。このインターフェースを使用した後、 `ADMIN SHOW DDL JOBS`の実行時間が大幅に短縮されました[#11789](https://github.com/pingcap/tidb/pull/11789)
    -   `CREATE TABLE ... PRE_SPLIT_REGION`構文を改善: `PRE_SPLIT_REGION = N` [#11797](https://github.com/pingcap/tidb/pull/11797/files)の場合、事前分割領域の数を 2^(N-1) から 2^N に変更します。
    -   `Add Index`操作のバックグラウンド ワーカー スレッドのデフォルト パラメータ値を減らして、オンライン ワークロードへの大きな影響を回避します[#11875](https://github.com/pingcap/tidb/pull/11875)
    -   `SPLIT TABLE`構文の動作を改善: 領域[#11929](https://github.com/pingcap/tidb/pull/11929)を分割するために`SPLIT TABLE ... REGIONS N`が使用される場合、N データリージョン(s) と 1 つのインデックスリージョンを生成します
    -   設定ファイルに`split-region-max-num`パラメータ (デフォルトでは`10000` ) を追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を調整可能にします[#12080](https://github.com/pingcap/tidb/pull/12080)
    -   システムがbinlog [#12121](https://github.com/pingcap/tidb/pull/12121)を書き込むときに、この句でコメント解除された`PRE_SPLIT_REGIONS`が原因で、下流の MySQL が`CREATE TABLE`句を解析できないという問題を修正します。
    -   `SHOW TABLE … REGIONS`と`SHOW TABLE .. INDEX … REGIONS` [#12124](https://github.com/pingcap/tidb/pull/12124)に`WHERE`節を追加
-   モニター
    -   `connection_transient_failure_count`モニタリング メトリクスを追加して、 `tikvclient` [#12092](https://github.com/pingcap/tidb/pull/12092)の gRPC 接続エラーをカウントします

## TiKV {#tikv}

-   場合によっては、リージョン内のキーをカウントする際の誤った結果を修正します[#5415](https://github.com/tikv/tikv/pull/5415)
-   TiKV に`config-check`オプションを追加して、TiKV 構成項目が有効かどうかを確認します[#5391](https://github.com/tikv/tikv/pull/5391)
-   起動プロセスを最適化して、ノード[#5277](https://github.com/tikv/tikv/pull/5277)の再起動によって発生するジッターを減らします
-   場合によっては、ロックの解決プロセスを最適化して、トランザクションのロックの解決を高速化します[#5339](https://github.com/tikv/tikv/pull/5339)
-   `get_txn_commit_info`プロセスを最適化してトランザクションのコミットを高速化する[#5062](https://github.com/tikv/tikv/pull/5062)
-   Raft 関連のログを簡素化する[#5425](https://github.com/tikv/tikv/pull/5425)
-   場合によっては TiKV が異常終了する問題を解決[#5441](https://github.com/tikv/tikv/pull/5441)

## PD {#pd}

-   PD に`config-check`オプションを追加して、PD 構成アイテムが有効かどうかを確認します[#1725](https://github.com/pingcap/pd/pull/1725)
-   pd-ctl に`remove-tombstone`コマンドを追加して、tombstone ストア レコードのクリアをサポートします[#1705](https://github.com/pingcap/pd/pull/1705)
-   スケジューリングをスピードアップするようオペレーターに積極的に働きかけるサポート[#1686](https://github.com/pingcap/pd/pull/1686)

## ツール {#tools}

-   TiDBBinlog
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して、回復速度を制御します[#746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化して並列実行効率を向上させる[#735](https://github.com/pingcap/tidb-binlog/pull/735)
    -   場合によってはPumpが正常に終了できない不具合を修正[#739](https://github.com/pingcap/tidb-binlog/pull/739)
    -   Pumpの`LevelDB`の処理ロジックを最適化し、GCの実行効率を向上させる[#720](https://github.com/pingcap/tidb-binlog/pull/720)
-   TiDB Lightning
    -   チェックポイント[#239](https://github.com/pingcap/tidb-lightning/pull/239)からデータを再インポートすると、tidb-lightning がクラッシュする可能性があるバグを修正します。

## TiDB アンシブル {#tidb-ansible}

-   Spark のバージョンを 2.4.3 に更新し、TiSpark のバージョンを Spark 2.4.3 と互換性のある 2.2.0 に更新します[#914](https://github.com/pingcap/tidb-ansible/pull/914) , [#919](https://github.com/pingcap/tidb-ansible/pull/927)
-   リモート マシンのパスワードが期限切れになると、長い待ち時間が発生する問題を修正します[#937](https://github.com/pingcap/tidb-ansible/pull/937) 、 [#948](https://github.com/pingcap/tidb-ansible/pull/948)
