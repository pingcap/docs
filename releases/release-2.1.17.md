---
title: TiDB 2.1.17 Release Notes
---

# TiDB2.1.17リリースノート {#tidb-2-1-17-release-notes}

発売日：2019年9月11日

TiDBバージョン：2.1.17

TiDB Ansibleバージョン：2.1.17

-   新機能
    -   TiDBの`SHOW TABLE REGIONS`構文に`WHERE`句を追加します
    -   TiKVとPDに`config-check`つの機能を追加して、構成項目を確認します
    -   pd-ctlに`remove-tombstone`コマンドを追加して、トゥームストーンストアレコードをクリアします
    -   Reparoに`worker-count`と`txn-batch`の構成項目を追加して、回復速度を制御します

-   改善
    -   積極的にプッシュするオペレーターをサポートすることにより、PDのスケジューリングプロセスを最適化する
    -   TiKVの開始プロセスを最適化して、ノードの再起動によって引き起こされるジッターを減らします

-   変更された動作
    -   TiDBの低速クエリログの`start ts`を最後の再試行時刻から最初の実行時刻に変更します
    -   低速クエリログの使いやすさを向上させるために、TiDB低速クエリログの`Index_ids`フィールドを`Index_names`フィールドに置き換えます
    -   TiDBの構成ファイルに`split-region-max-num`パラメーターを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。これはデフォルト構成では1,000から10,000に増加します。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `EvalSubquery`ビルド中にエラーが発生したときにエラーメッセージが正しく返されない問題を修正し`Executor` [＃11811](https://github.com/pingcap/tidb/pull/11811)
    -   外部テーブルの行数がインデックスルックアップ結合の単一バッチの行数よりも多い場合、クエリ結果が正しくない可能性がある問題を修正します。インデックスルックアップ結合の機能範囲を拡張します。 `UnionScan`は[＃11843](https://github.com/pingcap/tidb/pull/11843)のサブノードとして使用でき`IndexJoin`
    -   統計フィードバックプロセス中に無効なキーが発生する可能性がある状況のために、 `SHOW STAT_BUCKETS`の構文に無効なキー（ `invalid encoded key flag 252`など）の表示を追加します[＃12098](https://github.com/pingcap/tidb/pull/12098)
-   SQL実行エンジン
    -   `CAST`関数が数値タイプ[＃11712](https://github.com/pingcap/tidb/pull/11712)を変換しているときに、最初に`UINT`に変換される数値によって引き起こされるいくつかの誤った結果（ `select cast(13835058000000000000 as double)`など）を修正します。
    -   `DIV`の計算の被除数が小数であり、この計算に負の数[＃11812](https://github.com/pingcap/tidb/pull/11812)が含まれている場合、計算結果が正しくない可能性がある問題を修正します。
    -   `ConvertStrToIntStrict`関数を追加して、 `SELECT` / `EXPLAIN`ステートメント[＃11892](https://github.com/pingcap/tidb/pull/11892)の実行時に一部の文字列が`INT`タイプに変換されることによって引き起こされるMySQLの非互換性の問題を修正します。
    -   `EXPLAIN ... FOR CONNECTION`が使用されている場合に`stmtCtx`の設定が間違っているために`Explain`の結果が正しくない可能性があるという問題を修正します[＃11978](https://github.com/pingcap/tidb/pull/11978)
    -   `unaryMinus`関数によって返される結果がMySQLと互換性がないという問題を修正します。これは、整数の結果が[＃11990](https://github.com/pingcap/tidb/pull/11990)をオーバーフローしたときに非10進数の結果が原因で発生します。
    -   `LOAD DATA`ステートメントが実行されているときのカウント順序が原因で`last_insert_id()`が正しくない可能性があるという問題を修正します[＃11994](https://github.com/pingcap/tidb/pull/11994)
    -   ユーザーが明示的-暗黙的な混合方法で自動インクリメント列データを書き込むときに`last_insert_id()`が正しくない可能性があるという問題を修正します[＃12001](https://github.com/pingcap/tidb/pull/12001)
    -   `JSON_UNQUOTE`関数の引用符で囲まれたバグを修正します。二重引用符（ `"` ）で囲まれた値のみを引用符で囲まないようにする必要があります。たとえば、「 `SELECT JSON_UNQUOTE("\\\\")` 」の結果は「 `\\` 」（変更されない） [＃12096](https://github.com/pingcap/tidb/pull/12096)になります。
-   サーバ
    -   低速クエリログに記録された`start ts`を、TiDBトランザクションを再試行するときの最後の再試行時刻から最初の実行時刻に変更します[＃11878](https://github.com/pingcap/tidb/pull/11878)
    -   リージョン全体でのスキャン操作を回避し、キーの数が減ったときにロックを解決するコストを削減するために、トランザクションのキーの数を`LockResolver`に追加します[＃11889](https://github.com/pingcap/tidb/pull/11889)
    -   遅いクエリログで`succ`フィールド値が正しくない可能性がある問題を修正します[＃11886](https://github.com/pingcap/tidb/pull/11886)
    -   遅いクエリログの使いやすさを向上させるために、遅いクエリログにファイルされた`Index_ids`を`Index_names`フィールドに置き換えます[＃12063](https://github.com/pingcap/tidb/pull/12063)
    -   `Duration`に`-` （ `select time(‘--’)`など）が含まれている場合に、TiDBが`-`をEOFエラーに解析することによって発生する接続切断の問題を修正します[＃11910](https://github.com/pingcap/tidb/pull/11910)
    -   無効なリージョンを`RegionCache`からすばやく削除して、このリージョン[＃11931](https://github.com/pingcap/tidb/pull/11931)に送信されるリクエストの数を減らします。
    -   `oom-action = "cancel"`とOOMが`Insert Into … Select`構文[＃12126](https://github.com/pingcap/tidb/pull/12126)で発生した場合に、OOMパニックの問題を誤って処理することによって引き起こされる接続切断の問題を修正します。
-   DDL
    -   `tikvSnapshot`のリバーススキャンインターフェイスを追加して、DDL履歴ジョブを効率的にクエリします。このインターフェースを使用した後、 `ADMIN SHOW DDL JOBS`の実行時間は大幅に短縮されます[＃11789](https://github.com/pingcap/tidb/pull/11789)
    -   `CREATE TABLE ... PRE_SPLIT_REGION`構文を改善します。35の場合、事前分割領域の数を2 ^（N-1）から`PRE_SPLIT_REGION = N` ^Nに変更し[＃11797](https://github.com/pingcap/tidb/pull/11797/files) 。
    -   オンラインワークロードへの大きな影響を回避するために、 `Add Index`操作のバックグラウンドワーカースレッドのデフォルトパラメーター値を減らします[＃11875](https://github.com/pingcap/tidb/pull/11875)
    -   `SPLIT TABLE`の構文動作を改善します`SPLIT TABLE ... REGIONS N`を使用してリージョン[＃11929](https://github.com/pingcap/tidb/pull/11929)を分割する場合、N個のデータリージョンと1つのインデックスリージョンを生成します。
    -   構成ファイルに`split-region-max-num`つのパラメーター（デフォルトでは`10000` ）を追加して、 `SPLIT TABLE`の構文で許可されるリージョンの最大数を調整可能にします[＃12080](https://github.com/pingcap/tidb/pull/12080)
    -   システムがbinlog5を書き込むときに、この句のコメントがない`PRE_SPLIT_REGIONS`が原因で、ダウンストリームのMySQLが`CREATE TABLE`句を解析できない問題を修正し[＃12121](https://github.com/pingcap/tidb/pull/12121) 。
    -   `SHOW TABLE … REGIONS`と[＃12124](https://github.com/pingcap/tidb/pull/12124)に`WHERE`つの副節を追加し`SHOW TABLE .. INDEX … REGIONS`
-   モニター
    -   `connection_transient_failure_count`モニタリングメトリックを追加して、35の`tikvclient`接続エラーをカウントし[＃12092](https://github.com/pingcap/tidb/pull/12092)

## TiKV {#tikv}

-   場合によっては、リージョン内のキーをカウントした誤った結果を修正します[＃5415](https://github.com/tikv/tikv/pull/5415)
-   TiKVに`config-check`オプションを追加して、TiKV構成アイテムが有効かどうかを確認します[＃5391](https://github.com/tikv/tikv/pull/5391)
-   開始プロセスを最適化して、ノードの再起動によって引き起こされるジッターを減らします[＃5277](https://github.com/tikv/tikv/pull/5277)
-   場合によっては、解決ロックプロセスを最適化して、トランザクションの解決ロックを高速化します[＃5339](https://github.com/tikv/tikv/pull/5339)
-   `get_txn_commit_info`のプロセスを最適化して、トランザクションのコミットを高速化します[＃5062](https://github.com/tikv/tikv/pull/5062)
-   Raft関連のログを簡素化する[＃5425](https://github.com/tikv/tikv/pull/5425)
-   場合によってはTiKVが異常終了する問題を解決します[＃5441](https://github.com/tikv/tikv/pull/5441)

## PD {#pd}

-   PDに`config-check`オプションを追加して、PD構成アイテムが有効かどうかを確認します[＃1725](https://github.com/pingcap/pd/pull/1725)
-   墓石ストアレコードのクリアをサポートするために、pd-ctlに`remove-tombstone`コマンドを追加します[＃1705](https://github.com/pingcap/pd/pull/1705)
-   スケジュールをスピードアップするためにオペレーターを積極的にプッシュすることをサポートする[＃1686](https://github.com/pingcap/pd/pull/1686)

## ツール {#tools}

-   TiDB Binlog
    -   Reparoに`worker-count`と`txn-batch`の構成項目を追加して、回復速度を制御します[＃746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化して、並列実行効率を向上させます[＃735](https://github.com/pingcap/tidb-binlog/pull/735)
    -   場合によってはPumpが正常に終了できないバグを修正します[＃739](https://github.com/pingcap/tidb-binlog/pull/739)
    -   ポンプの`LevelDB`の処理ロジックを最適化して、 [＃720](https://github.com/pingcap/tidb-binlog/pull/720)の実行効率を向上させます
-   TiDB Lightning
    -   チェックポイント[＃239](https://github.com/pingcap/tidb-lightning/pull/239)からデータを再インポートすることによってtidb-lightningがクラッシュする可能性があるバグを修正します

## TiDB Ansible {#tidb-ansible}

-   Sparkバージョンを2.4.3に更新し、TiSparkバージョンをSpark 2.4.3 [＃914](https://github.com/pingcap/tidb-ansible/pull/914)と互換性のある2.2.0に更新し[＃919](https://github.com/pingcap/tidb-ansible/pull/927) 。
-   リモートマシンのパスワードの有効期限が切れると待ち時間が長くなる問題を修正し[＃948](https://github.com/pingcap/tidb-ansible/pull/948) [＃937](https://github.com/pingcap/tidb-ansible/pull/937)
