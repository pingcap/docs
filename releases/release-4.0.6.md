---
title: TiDB 4.0.6 Release Notes
---

# TiDB 4.0.6 リリースノート {#tidb-4-0-6-release-notes}

発売日：2020年9月15日

TiDB バージョン: 4.0.6

## 新機能 {#new-features}

-   TiFlash

    -   TiFlashブロードキャスト結合で外部結合をサポート

-   TiDB ダッシュボード

    -   クエリ エディターと実行 UI を追加 (実験的) [<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/713">#713</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    -   店舗の場所のトポロジの視覚化をサポート[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/719">#719</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
    -   クラスター構成 UI の追加 (実験的) [<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/733">#733</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    -   現在のセッションの共有をサポート[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/741">#741</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
    -   SQL ステートメント リスト[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/746">#746</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)の実行プランの数の表示をサポート

-   ツール

    -   TiCDC (v4.0.6 以降 GA)

        -   `maxwell`形式[<a href="https://github.com/pingcap/tiflow/pull/869">#869</a>](https://github.com/pingcap/tiflow/pull/869)でのデータ出力をサポート

## 改善点 {#improvements}

-   TiDB

    -   エラー コードとメッセージを標準エラーに置き換えます[<a href="https://github.com/pingcap/tidb/pull/19888">#19888</a>](https://github.com/pingcap/tidb/pull/19888)
    -   パーティションテーブル[<a href="https://github.com/pingcap/tidb/pull/19649">#19649</a>](https://github.com/pingcap/tidb/pull/19649)の書き込みパフォーマンスを向上させます。
    -   より多くの RPC ランタイム情報を`Cop Runtime`統計[<a href="https://github.com/pingcap/tidb/pull/19264">#19264</a>](https://github.com/pingcap/tidb/pull/19264)に記録します。
    -   `metrics_schema`と`performance_schema`でのテーブルの作成を禁止する[<a href="https://github.com/pingcap/tidb/pull/19792">#19792</a>](https://github.com/pingcap/tidb/pull/19792)
    -   Union Executor [<a href="https://github.com/pingcap/tidb/pull/19886">#19886</a>](https://github.com/pingcap/tidb/pull/19886)の同時実行性の調整をサポート
    -   ブロードキャスト参加[<a href="https://github.com/pingcap/tidb/pull/19664">#19664</a>](https://github.com/pingcap/tidb/pull/19664)の参加をサポート
    -   プロセスリスト[<a href="https://github.com/pingcap/tidb/pull/19829">#19829</a>](https://github.com/pingcap/tidb/pull/19829)のSQLダイジェストを追加
    -   自動コミットステートメントの再試行[<a href="https://github.com/pingcap/tidb/pull/19796">#19796</a>](https://github.com/pingcap/tidb/pull/19796)のために悲観的トランザクション モードに切り替える
    -   `Str_to_date()` [<a href="https://github.com/pingcap/tidb/pull/19693">#19693</a>](https://github.com/pingcap/tidb/pull/19693)の`%r`および`%T`データ形式をサポート
    -   `SELECT INTO OUTFILE`を有効にすると、ファイル権限[<a href="https://github.com/pingcap/tidb/pull/19577">#19577</a>](https://github.com/pingcap/tidb/pull/19577)が必要になります。
    -   `stddev_pop`機能[<a href="https://github.com/pingcap/tidb/pull/19541">#19541</a>](https://github.com/pingcap/tidb/pull/19541)をサポート
    -   `TiDB-Runtime`ダッシュボードの追加[<a href="https://github.com/pingcap/tidb/pull/19396">#19396</a>](https://github.com/pingcap/tidb/pull/19396)
    -   `ALTER TABLE`アルゴリズムの互換性を向上[<a href="https://github.com/pingcap/tidb/pull/19364">#19364</a>](https://github.com/pingcap/tidb/pull/19364)
    -   スローログ`plan`フィールド[<a href="https://github.com/pingcap/tidb/pull/19269">#19269</a>](https://github.com/pingcap/tidb/pull/19269)で`insert` / `delete` / `update`プランをエンコードする

-   TiKV

    -   `DropTable`または`TruncateTable`実行時のQPS低下を軽減[<a href="https://github.com/tikv/tikv/pull/8627">#8627</a>](https://github.com/tikv/tikv/pull/8627)
    -   エラーコードのメタファイルの生成をサポート[<a href="https://github.com/tikv/tikv/pull/8619">#8619</a>](https://github.com/tikv/tikv/pull/8619)
    -   cf スキャンの詳細[<a href="https://github.com/tikv/tikv/pull/8618">#8618</a>](https://github.com/tikv/tikv/pull/8618)のパフォーマンス統計を追加
    -   Grafana のデフォルト テンプレート[<a href="https://github.com/tikv/tikv/pull/8467">#8467</a>](https://github.com/tikv/tikv/pull/8467)に`rocksdb perf context`パネルを追加します。

-   PD

    -   TiDB ダッシュボードを v2020.09.08.1 に更新します[<a href="https://github.com/pingcap/pd/pull/2928">#2928</a>](https://github.com/pingcap/pd/pull/2928)
    -   リージョンとストアハートビート[<a href="https://github.com/tikv/pd/pull/2891">#2891</a>](https://github.com/tikv/pd/pull/2891)のメトリクスを追加します。
    -   低スペースしきい値を制御する元の方法に戻します[<a href="https://github.com/pingcap/pd/pull/2875">#2875</a>](https://github.com/pingcap/pd/pull/2875)
    -   標準エラーコードをサポート
        -   [<a href="https://github.com/tikv/pd/pull/2918">#2918</a>](https://github.com/tikv/pd/pull/2918) [<a href="https://github.com/tikv/pd/pull/2911">#2911</a>](https://github.com/tikv/pd/pull/2911) [<a href="https://github.com/tikv/pd/pull/2913">#2913</a>](https://github.com/tikv/pd/pull/2913) [<a href="https://github.com/tikv/pd/pull/2915">#2915</a>](https://github.com/tikv/pd/pull/2915) [<a href="https://github.com/tikv/pd/pull/2912">#2912</a>](https://github.com/tikv/pd/pull/2912)
        -   [<a href="https://github.com/tikv/pd/pull/2907">#2907</a>](https://github.com/tikv/pd/pull/2907) [<a href="https://github.com/tikv/pd/pull/2906">#2906</a>](https://github.com/tikv/pd/pull/2906) [<a href="https://github.com/tikv/pd/pull/2903">#2903</a>](https://github.com/tikv/pd/pull/2903) [<a href="https://github.com/tikv/pd/pull/2806">#2806</a>](https://github.com/tikv/pd/pull/2806) [<a href="https://github.com/tikv/pd/pull/2900">#2900</a>](https://github.com/tikv/pd/pull/2900) [<a href="https://github.com/tikv/pd/pull/2902">#2902</a>](https://github.com/tikv/pd/pull/2902)

-   TiFlash

    -   データ複製用の Grafana パネルの追加 ( `apply Region snapshots`および`ingest SST files` )
    -   Grafana パネルを`write stall`追加
    -   `dt_segment_force_merge_delta_rows`と`dt_segment_force_merge_delta_deletes`を追加してしきい値`write stall`を調整します
    -   TiFlash-Proxy の設定`raftstore.snap-handle-pool-size` ～ `0`をサポートし、マルチスレッドによるリージョンスナップショットの適用を無効にし、データ レプリケーション中のメモリ消費を削減します。
    -   `https_port`と`metrics_port`のCNチェックをサポート

-   ツール

    -   TiCDC

        -   プラーの初期化中に解決されたロックをスキップする[<a href="https://github.com/pingcap/tiflow/pull/910">#910</a>](https://github.com/pingcap/tiflow/pull/910)
        -   PD書き込み頻度を下げる[<a href="https://github.com/pingcap/tiflow/pull/937">#937</a>](https://github.com/pingcap/tiflow/pull/937)

    -   バックアップと復元 (BR)

        -   サマリーログ[<a href="https://github.com/pingcap/br/issues/486">#486</a>](https://github.com/pingcap/br/issues/486)にリアルタイムコストを追加

    -   Dumpling

        -   列名[<a href="https://github.com/pingcap/dumpling/pull/135">#135</a>](https://github.com/pingcap/dumpling/pull/135)を含む`INSERT`の出力をサポート
        -   `--filesize`と`--statement-size`の定義を mydumper [<a href="https://github.com/pingcap/dumpling/pull/142">#142</a>](https://github.com/pingcap/dumpling/pull/142)の定義と統合します。

    -   TiDB Lightning

        -   より正確なサイズで領域を分割して取り込む[<a href="https://github.com/pingcap/tidb-lightning/pull/369">#369</a>](https://github.com/pingcap/tidb-lightning/pull/369)

    -   TiDBBinlog

        -   `go time`パッケージ形式[<a href="https://github.com/pingcap/tidb-binlog/pull/996">#996</a>](https://github.com/pingcap/tidb-binlog/pull/996)で GC 時間の設定をサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   メトリクス プロファイル[<a href="https://github.com/pingcap/tidb/pull/19881">#19881</a>](https://github.com/pingcap/tidb/pull/19881)の`tikv_cop_wait`回の収集の問題を修正
    -   `SHOW GRANTS` [<a href="https://github.com/pingcap/tidb/pull/19834">#19834</a>](https://github.com/pingcap/tidb/pull/19834)の間違った結果を修正します
    -   `!= ALL (subq)` [<a href="https://github.com/pingcap/tidb/pull/19831">#19831</a>](https://github.com/pingcap/tidb/pull/19831)の誤ったクエリ結果を修正
    -   `enum`と`set`タイプを変換するバグを修正[<a href="https://github.com/pingcap/tidb/pull/19778">#19778</a>](https://github.com/pingcap/tidb/pull/19778)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET`の権限チェックを追加[<a href="https://github.com/pingcap/tidb/pull/19760">#19760</a>](https://github.com/pingcap/tidb/pull/19760)
    -   `builtinGreatestStringSig`と`builtinLeastStringSig`によって引き起こされる列の長さが一致しないエラーを修正[<a href="https://github.com/pingcap/tidb/pull/19758">#19758</a>](https://github.com/pingcap/tidb/pull/19758)
    -   不要なエラーまたは警告が発生した場合、ベクトル化された制御式はスカラー実行[<a href="https://github.com/pingcap/tidb/pull/19749">#19749</a>](https://github.com/pingcap/tidb/pull/19749)に戻ります。
    -   相関列の型が`Bit` [<a href="https://github.com/pingcap/tidb/pull/19692">#19692</a>](https://github.com/pingcap/tidb/pull/19692)の場合の`Apply`演算子のエラーを修正
    -   ユーザーが MySQL 8.0 クライアント[<a href="https://github.com/pingcap/tidb/pull/19690">#19690</a>](https://github.com/pingcap/tidb/pull/19690)で`processlist`と`cluster_log`クエリしたときに発生する問題を修正します。
    -   同じ種類のプランでもプラン ダイジェストが異なる問題を修正[<a href="https://github.com/pingcap/tidb/pull/19684">#19684</a>](https://github.com/pingcap/tidb/pull/19684)
    -   列タイプを`Decimal`から`Int`に変更することを禁止します[<a href="https://github.com/pingcap/tidb/pull/19682">#19682</a>](https://github.com/pingcap/tidb/pull/19682)
    -   `SELECT ... INTO OUTFILE`実行時エラー[<a href="https://github.com/pingcap/tidb/pull/19672">#19672</a>](https://github.com/pingcap/tidb/pull/19672)を返す問題を修正
    -   `builtinRealIsFalseSig` [<a href="https://github.com/pingcap/tidb/pull/19670">#19670</a>](https://github.com/pingcap/tidb/pull/19670)の誤った実装を修正
    -   パーティション式チェックで括弧式[<a href="https://github.com/pingcap/tidb/pull/19614">#19614</a>](https://github.com/pingcap/tidb/pull/19614)が見逃される問題を修正します。
    -   `HashJoin` [<a href="https://github.com/pingcap/tidb/pull/19611">#19611</a>](https://github.com/pingcap/tidb/pull/19611)に`Apply`演算子がある場合のクエリ エラーを修正しました。
    -   `Real`を`Time` [<a href="https://github.com/pingcap/tidb/pull/19594">#19594</a>](https://github.com/pingcap/tidb/pull/19594)としてキャストするベクトル化の誤った結果を修正
    -   `SHOW GRANTS`ステートメントが存在しないユーザー[<a href="https://github.com/pingcap/tidb/pull/19588">#19588</a>](https://github.com/pingcap/tidb/pull/19588)に対する許可を表示するバグを修正
    -   `IndexLookupJoin` [<a href="https://github.com/pingcap/tidb/pull/19566">#19566</a>](https://github.com/pingcap/tidb/pull/19566)に`Apply`のエグゼキュータがある場合のクエリ エラーを修正しました。
    -   パーティションテーブル[<a href="https://github.com/pingcap/tidb/pull/19546">#19546</a>](https://github.com/pingcap/tidb/pull/19546)で`Apply`を`HashJoin`に変換するときの間違った結果を修正しました。
    -   `Apply` [<a href="https://github.com/pingcap/tidb/pull/19508">#19508</a>](https://github.com/pingcap/tidb/pull/19508)の内側に`IndexLookUp`エグゼキュータがある場合の誤った結果を修正
    -   ビュー[<a href="https://github.com/pingcap/tidb/pull/19491">#19491</a>](https://github.com/pingcap/tidb/pull/19491)使用時の予期しないpanicを修正
    -   `anti-semi-join`クエリ[<a href="https://github.com/pingcap/tidb/pull/19477">#19477</a>](https://github.com/pingcap/tidb/pull/19477)の誤った結果を修正します。
    -   統計を削除した場合に`TopN`統計が削除されないバグを修正[<a href="https://github.com/pingcap/tidb/pull/19465">#19465</a>](https://github.com/pingcap/tidb/pull/19465)
    -   バッチポイント取得[<a href="https://github.com/pingcap/tidb/pull/19460">#19460</a>](https://github.com/pingcap/tidb/pull/19460)の誤った使用によって引き起こされる間違った結果を修正
    -   仮想生成列[<a href="https://github.com/pingcap/tidb/pull/19439">#19439</a>](https://github.com/pingcap/tidb/pull/19439)で`indexLookupJoin`で列が見つからないバグを修正
    -   `select`と`update`クエリの異なるプランがデータ[<a href="https://github.com/pingcap/tidb/pull/19403">#19403</a>](https://github.com/pingcap/tidb/pull/19403)を比較するというエラーを修正
    -   リージョンキャッシュ[<a href="https://github.com/pingcap/tidb/pull/19362">#19362</a>](https://github.com/pingcap/tidb/pull/19362)のTiFlash作業インデックスのデータ競合を修正
    -   `logarithm`機能で警告が表示されないバグを修正[<a href="https://github.com/pingcap/tidb/pull/19291">#19291</a>](https://github.com/pingcap/tidb/pull/19291)
    -   TiDB がデータをディスク[<a href="https://github.com/pingcap/tidb/pull/19272">#19272</a>](https://github.com/pingcap/tidb/pull/19272)に保存するときに発生する予期しないエラーを修正しました。
    -   インデックス結合[<a href="https://github.com/pingcap/tidb/pull/19197">#19197</a>](https://github.com/pingcap/tidb/pull/19197)の内側で単一のパーティションテーブルの使用をサポート
    -   10 進数[<a href="https://github.com/pingcap/tidb/pull/19188">#19188</a>](https://github.com/pingcap/tidb/pull/19188)に対して生成された間違ったハッシュ キー値を修正しました。
    -   テーブル endKey とリージョンendKey が同じ[<a href="https://github.com/pingcap/tidb/pull/19895">#19895</a>](https://github.com/pingcap/tidb/pull/19895)の場合、TiDB が`no regions`エラーを返す問題を修正
    -   パーティション[<a href="https://github.com/pingcap/tidb/pull/19891">#19891</a>](https://github.com/pingcap/tidb/pull/19891)の変更が予期せず成功する問題を修正
    -   プッシュダウンされた式[<a href="https://github.com/pingcap/tidb/pull/19876">#19876</a>](https://github.com/pingcap/tidb/pull/19876)に許可されるデフォルトの最大パケット長の誤った値を修正しました。
    -   `ENUM` / `SET`列の`Max` / `Min`関数の誤った動作を修正[<a href="https://github.com/pingcap/tidb/pull/19869">#19869</a>](https://github.com/pingcap/tidb/pull/19869)
    -   一部のTiFlashノードがオフラインの場合の`tiflash_segments`および`tiflash_tables`システム テーブルからの読み取りエラーを修正[<a href="https://github.com/pingcap/tidb/pull/19748">#19748</a>](https://github.com/pingcap/tidb/pull/19748)
    -   `Count(col)`集計関数の間違った結果を修正します[<a href="https://github.com/pingcap/tidb/pull/19628">#19628</a>](https://github.com/pingcap/tidb/pull/19628)
    -   `TRUNCATE`オペレーション[<a href="https://github.com/pingcap/tidb/pull/19445">#19445</a>](https://github.com/pingcap/tidb/pull/19445)の実行時エラーを修正
    -   `Var`に大文字が含まれる場合、 `PREPARE statement FROM @Var`が失敗する問題を修正[<a href="https://github.com/pingcap/tidb/pull/19378">#19378</a>](https://github.com/pingcap/tidb/pull/19378)
    -   大文字のスキーマでスキーマ文字セットを変更するとpanic[<a href="https://github.com/pingcap/tidb/pull/19302">#19302</a>](https://github.com/pingcap/tidb/pull/19302)が発生するバグを修正
    -   情報に`tikv/tiflash` [<a href="https://github.com/pingcap/tidb/pull/19159">#19159</a>](https://github.com/pingcap/tidb/pull/19159)が含まれる場合、 `information_schema.statements_summary`と`explain`の間の計画の不一致を修正します。
    -   `select into outfile` [<a href="https://github.com/pingcap/tidb/pull/19725">#19725</a>](https://github.com/pingcap/tidb/pull/19725)のファイルが存在しないというテストのエラーを修正
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`に RAID デバイス情報がない問題を修正[<a href="https://github.com/pingcap/tidb/pull/19457">#19457</a>](https://github.com/pingcap/tidb/pull/19457)
    -   `case-when`式で生成された列を持つ`add index`操作が、解析エラーが発生したときに正常に終了できるようにします[<a href="https://github.com/pingcap/tidb/pull/19395">#19395</a>](https://github.com/pingcap/tidb/pull/19395)
    -   DDL 操作のリトライに時間がかかりすぎるバグを修正[<a href="https://github.com/pingcap/tidb/pull/19488">#19488</a>](https://github.com/pingcap/tidb/pull/19488)
    -   `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)`のようなステートメントを最初に実行せずに実行させる`use db` [<a href="https://github.com/pingcap/tidb/pull/19471">#19471</a>](https://github.com/pingcap/tidb/pull/19471)
    -   サーバーログファイルのディスパッチエラーをメッセージ`Error`から`Info`に変更します[<a href="https://github.com/pingcap/tidb/pull/19454">#19454</a>](https://github.com/pingcap/tidb/pull/19454)

-   TiKV

    -   照合順序が有効になっている場合の非インデックス列の推定エラーを修正[<a href="https://github.com/tikv/tikv/pull/8620">#8620</a>](https://github.com/tikv/tikv/pull/8620)
    -   リージョン転送[<a href="https://github.com/tikv/tikv/pull/8460">#8460</a>](https://github.com/tikv/tikv/pull/8460)のプロセス中に Green GC がロックをミスする可能性がある問題を修正
    -   Raftメンバーシップの変更[<a href="https://github.com/tikv/tikv/pull/8497">#8497</a>](https://github.com/tikv/tikv/pull/8497)中に TiKV の実行が非常に遅い場合に発生するpanicの問題を修正します。
    -   PD 同期リクエストを呼び出すときに PD クライアント スレッドと他のスレッドの間で発生するデッドロックの問題を修正します[<a href="https://github.com/tikv/tikv/pull/8612">#8612</a>](https://github.com/tikv/tikv/pull/8612)
    -   巨大ページ[<a href="https://github.com/tikv/tikv/pull/8463">#8463</a>](https://github.com/tikv/tikv/pull/8463)のメモリ割り当ての問題に対処するために、jemalloc を v5.2.1 にアップグレードします。
    -   長時間実行されるクエリに対して統合スレッド プールがハングする問題を修正します[<a href="https://github.com/tikv/tikv/pull/8427">#8427</a>](https://github.com/tikv/tikv/pull/8427)

-   PD

    -   `initial-cluster-token`構成を追加して、ブートストラップ[<a href="https://github.com/pingcap/pd/pull/2922">#2922</a>](https://github.com/pingcap/pd/pull/2922)中に異なるクラスターが相互に通信しないようにします。
    -   モード`auto` [<a href="https://github.com/pingcap/pd/pull/2826">#2826</a>](https://github.com/pingcap/pd/pull/2826)時のストアリミットレートの単位を修正
    -   一部のスケジューラーがエラーを解決せずに構成を保持する問題を修正します[<a href="https://github.com/tikv/pd/pull/2818">#2818</a>](https://github.com/tikv/pd/pull/2818)
    -   スケジューラ[<a href="https://github.com/tikv/pd/pull/2871">#2871</a>](https://github.com/tikv/pd/pull/2871) [<a href="https://github.com/tikv/pd/pull/2874">#2874</a>](https://github.com/tikv/pd/pull/2874)の空の HTTP 応答を修正

-   TiFlash

    -   以前のバージョンで主キー列の名前を変更した後、v4.0.4/v4.0.5 にアップグレードした後にTiFlashが起動しない場合がある問題を修正
    -   列の`nullable`属性を変更した後に発生する例外を修正します。
    -   テーブルのレプリケーションステータスの計算によって発生するクラッシュを修正
    -   ユーザーがサポートされていない DDL 操作を適用した後、 TiFlash がデータ読み取りに使用できなくなる問題を修正
    -   サポートされていない照合順序が`utf8mb4_bin`として扱われることによって発生する例外を修正しました。
    -   TiFlashコプロセッサ エグゼキュータの QPS パネルが Grafana で常に`0`と表示される問題を修正
    -   入力が`NULL`場合の`FROM_UNIXTIME`関数の誤った結果を修正

-   ツール

    -   TiCDC

        -   TiCDC が場合によってメモリリークを起こす問題を修正[<a href="https://github.com/pingcap/tiflow/pull/942">#942</a>](https://github.com/pingcap/tiflow/pull/942)
        -   Kafka シンク[<a href="https://github.com/pingcap/tiflow/pull/912">#912</a>](https://github.com/pingcap/tiflow/pull/912)で TiCDC がpanicになる可能性がある問題を修正
        -   プラー[<a href="https://github.com/pingcap/tiflow/pull/927">#927</a>](https://github.com/pingcap/tiflow/pull/927)で CommitTs または ResolvedTs (CRT) が`resolvedTs`未満になる可能性がある問題を修正
        -   `changefeed`が MySQL ドライバー[<a href="https://github.com/pingcap/tiflow/pull/936">#936</a>](https://github.com/pingcap/tiflow/pull/936)によってブロックされる可能性がある問題を修正
        -   TiCDC [<a href="https://github.com/tikv/tikv/pull/8573">#8573</a>](https://github.com/tikv/tikv/pull/8573)の誤った解決された Ts 間隔を修正しました。

    -   バックアップと復元 (BR)

        -   チェックサム[<a href="https://github.com/pingcap/br/pull/479">#479</a>](https://github.com/pingcap/br/pull/479)中に発生する可能性のあるpanicを修正しました。
        -   PDLeader[<a href="https://github.com/pingcap/br/pull/496">#496</a>](https://github.com/pingcap/br/pull/496)の変更後に発生する可能性のpanicを修正

    -   Dumpling

        -   バイナリ型の`NULL`値が正しく処理されない問題を修正[<a href="https://github.com/pingcap/dumpling/pull/137">#137</a>](https://github.com/pingcap/dumpling/pull/137)

    -   TiDB Lightning

        -   失敗した書き込みおよび取り込み操作がすべて誤って成功として表示される問題を修正します[<a href="https://github.com/pingcap/tidb-lightning/pull/381">#381</a>](https://github.com/pingcap/tidb-lightning/pull/381)
        -   TiDB Lightningが終了する前に、一部のチェックポイント更新がデータベースに書き込まれない可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb-lightning/pull/386">#386</a>](https://github.com/pingcap/tidb-lightning/pull/386)
