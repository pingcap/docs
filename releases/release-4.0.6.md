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

    -   クエリ エディターと実行 UI を追加 (実験的) [#713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    -   店舗の場所のトポロジの視覚化をサポート[#719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
    -   クラスター構成 UI の追加 (実験的) [#733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    -   現在のセッションの共有をサポート[#741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
    -   SQL ステートメント リスト[#746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)の実行プランの数の表示をサポート

-   ツール

    -   TiCDC (v4.0.6 以降 GA)

        -   `maxwell`形式[#869](https://github.com/pingcap/tiflow/pull/869)でのデータ出力をサポート

## 改善点 {#improvements}

-   TiDB

    -   エラー コードとメッセージを標準エラーに置き換えます[#19888](https://github.com/pingcap/tidb/pull/19888)
    -   パーティションテーブル[#19649](https://github.com/pingcap/tidb/pull/19649)の書き込みパフォーマンスを向上させます。
    -   より多くの RPC ランタイム情報を`Cop Runtime`統計[#19264](https://github.com/pingcap/tidb/pull/19264)に記録します。
    -   `metrics_schema`と`performance_schema`でのテーブルの作成を禁止する[#19792](https://github.com/pingcap/tidb/pull/19792)
    -   Union Executor [#19886](https://github.com/pingcap/tidb/pull/19886)の同時実行性の調整をサポート
    -   ブロードキャスト参加[#19664](https://github.com/pingcap/tidb/pull/19664)の参加をサポート
    -   プロセスリスト[#19829](https://github.com/pingcap/tidb/pull/19829)のSQLダイジェストを追加
    -   自動コミットステートメントの再試行[#19796](https://github.com/pingcap/tidb/pull/19796)のために悲観的トランザクション モードに切り替える
    -   `Str_to_date()` [#19693](https://github.com/pingcap/tidb/pull/19693)の`%r`および`%T`データ形式をサポート
    -   `SELECT INTO OUTFILE`を有効にすると、ファイル権限[#19577](https://github.com/pingcap/tidb/pull/19577)が必要になります。
    -   `stddev_pop`機能[#19541](https://github.com/pingcap/tidb/pull/19541)をサポート
    -   `TiDB-Runtime`ダッシュボードの追加[#19396](https://github.com/pingcap/tidb/pull/19396)
    -   `ALTER TABLE`アルゴリズムの互換性を向上[#19364](https://github.com/pingcap/tidb/pull/19364)
    -   スローログ`plan`フィールド[#19269](https://github.com/pingcap/tidb/pull/19269)で`insert` / `delete` / `update`プランをエンコードする

-   TiKV

    -   `DropTable`または`TruncateTable`実行時のQPS低下を軽減[#8627](https://github.com/tikv/tikv/pull/8627)
    -   エラーコードのメタファイルの生成をサポート[#8619](https://github.com/tikv/tikv/pull/8619)
    -   cf スキャンの詳細[#8618](https://github.com/tikv/tikv/pull/8618)のパフォーマンス統計を追加
    -   Grafana のデフォルト テンプレート[#8467](https://github.com/tikv/tikv/pull/8467)に`rocksdb perf context`パネルを追加します。

-   PD

    -   TiDB ダッシュボードを v2020.09.08.1 に更新します[#2928](https://github.com/pingcap/pd/pull/2928)
    -   リージョンとストアハートビート[#2891](https://github.com/tikv/pd/pull/2891)のメトリクスを追加します。
    -   低スペースしきい値を制御する元の方法に戻します[#2875](https://github.com/pingcap/pd/pull/2875)
    -   標準エラーコードをサポート
        -   [#2918](https://github.com/tikv/pd/pull/2918) [#2911](https://github.com/tikv/pd/pull/2911) [#2913](https://github.com/tikv/pd/pull/2913) [#2915](https://github.com/tikv/pd/pull/2915) [#2912](https://github.com/tikv/pd/pull/2912)
        -   [#2907](https://github.com/tikv/pd/pull/2907) [#2906](https://github.com/tikv/pd/pull/2906) [#2903](https://github.com/tikv/pd/pull/2903) [#2806](https://github.com/tikv/pd/pull/2806) [#2900](https://github.com/tikv/pd/pull/2900) [#2902](https://github.com/tikv/pd/pull/2902)

-   TiFlash

    -   データ複製用の Grafana パネルの追加 ( `apply Region snapshots`および`ingest SST files` )
    -   Grafana パネルを`write stall`追加
    -   `dt_segment_force_merge_delta_rows`と`dt_segment_force_merge_delta_deletes`を追加してしきい値`write stall`を調整します
    -   TiFlash-Proxy で設定`raftstore.snap-handle-pool-size` ～ `0`をサポートし、マルチスレッドによるリージョンスナップショットの適用を無効にし、データ レプリケーション中のメモリ消費を削減します。
    -   `https_port`と`metrics_port`のCNチェックをサポート

-   ツール

    -   TiCDC

        -   プラーの初期化中に解決されたロックをスキップする[#910](https://github.com/pingcap/tiflow/pull/910)
        -   PD書き込み頻度を下げる[#937](https://github.com/pingcap/tiflow/pull/937)

    -   バックアップと復元 (BR)

        -   サマリーログ[#486](https://github.com/pingcap/br/issues/486)にリアルタイムコストを追加

    -   Dumpling

        -   列名[#135](https://github.com/pingcap/dumpling/pull/135)を含む`INSERT`の出力をサポート
        -   `--filesize`と`--statement-size`の定義を mydumper [#142](https://github.com/pingcap/dumpling/pull/142)の定義と統合します。

    -   TiDB Lightning

        -   より正確なサイズで領域を分割して取り込む[#369](https://github.com/pingcap/tidb-lightning/pull/369)

    -   TiDBBinlog

        -   `go time`パッケージ形式[#996](https://github.com/pingcap/tidb-binlog/pull/996)で GC 時間の設定をサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   メトリクス プロファイル[#19881](https://github.com/pingcap/tidb/pull/19881)の`tikv_cop_wait`回の収集の問題を修正
    -   `SHOW GRANTS` [#19834](https://github.com/pingcap/tidb/pull/19834)の間違った結果を修正します
    -   `!= ALL (subq)` [#19831](https://github.com/pingcap/tidb/pull/19831)の誤ったクエリ結果を修正
    -   `enum`と`set`タイプを変換するバグを修正[#19778](https://github.com/pingcap/tidb/pull/19778)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET`の権限チェックを追加[#19760](https://github.com/pingcap/tidb/pull/19760)
    -   `builtinGreatestStringSig`と`builtinLeastStringSig`によって引き起こされる列の長さが一致しないエラーを修正[#19758](https://github.com/pingcap/tidb/pull/19758)
    -   不要なエラーまたは警告が発生した場合、ベクトル化された制御式はスカラー実行[#19749](https://github.com/pingcap/tidb/pull/19749)に戻ります。
    -   相関列の型が`Bit` [#19692](https://github.com/pingcap/tidb/pull/19692)の場合の`Apply`演算子のエラーを修正
    -   ユーザーが MySQL 8.0 クライアント[#19690](https://github.com/pingcap/tidb/pull/19690)で`processlist`と`cluster_log`クエリしたときに発生する問題を修正します。
    -   同じ種類のプランでもプラン ダイジェストが異なる問題を修正[#19684](https://github.com/pingcap/tidb/pull/19684)
    -   列タイプを`Decimal`から`Int`に変更することを禁止します[#19682](https://github.com/pingcap/tidb/pull/19682)
    -   `SELECT ... INTO OUTFILE`実行時エラー[#19672](https://github.com/pingcap/tidb/pull/19672)を返す問題を修正
    -   `builtinRealIsFalseSig` [#19670](https://github.com/pingcap/tidb/pull/19670)の誤った実装を修正
    -   パーティション式チェックで括弧式[#19614](https://github.com/pingcap/tidb/pull/19614)が見逃される問題を修正します。
    -   `HashJoin` [#19611](https://github.com/pingcap/tidb/pull/19611)に`Apply`演算子がある場合のクエリ エラーを修正しました。
    -   `Real`を`Time` [#19594](https://github.com/pingcap/tidb/pull/19594)としてキャストするベクトル化の誤った結果を修正
    -   `SHOW GRANTS`ステートメントが存在しないユーザー[#19588](https://github.com/pingcap/tidb/pull/19588)に対する許可を表示するバグを修正
    -   `IndexLookupJoin` [#19566](https://github.com/pingcap/tidb/pull/19566)に`Apply`エグゼキュータがある場合のクエリ エラーを修正しました。
    -   パーティションテーブル[#19546](https://github.com/pingcap/tidb/pull/19546)で`Apply`を`HashJoin`に変換するときの間違った結果を修正しました。
    -   `Apply` [#19508](https://github.com/pingcap/tidb/pull/19508)の内側に`IndexLookUp`エグゼキュータがある場合の誤った結果を修正
    -   ビュー[#19491](https://github.com/pingcap/tidb/pull/19491)使用時の予期しないpanicを修正
    -   `anti-semi-join`クエリ[#19477](https://github.com/pingcap/tidb/pull/19477)の誤った結果を修正します。
    -   統計を削除した場合に`TopN`統計が削除されないバグを修正[#19465](https://github.com/pingcap/tidb/pull/19465)
    -   バッチポイント取得[#19460](https://github.com/pingcap/tidb/pull/19460)の誤った使用によって引き起こされる間違った結果を修正
    -   仮想生成列[#19439](https://github.com/pingcap/tidb/pull/19439)で`indexLookupJoin`で列が見つからないバグを修正
    -   `select`と`update`クエリの異なるプランがデータ[#19403](https://github.com/pingcap/tidb/pull/19403)を比較するというエラーを修正
    -   リージョンキャッシュ[#19362](https://github.com/pingcap/tidb/pull/19362)のTiFlash作業インデックスのデータ競合を修正
    -   `logarithm`機能で警告が表示されないバグを修正[#19291](https://github.com/pingcap/tidb/pull/19291)
    -   TiDB がデータをディスク[#19272](https://github.com/pingcap/tidb/pull/19272)に保存するときに発生する予期しないエラーを修正しました。
    -   インデックス結合[#19197](https://github.com/pingcap/tidb/pull/19197)の内側で単一のパーティションテーブルの使用をサポート
    -   10 進数[#19188](https://github.com/pingcap/tidb/pull/19188)に対して生成された間違ったハッシュ キー値を修正しました。
    -   テーブル endKey とリージョンendKey が同じ[#19895](https://github.com/pingcap/tidb/pull/19895)の場合、TiDB が`no regions`エラーを返す問題を修正
    -   パーティション[#19891](https://github.com/pingcap/tidb/pull/19891)の変更が予期せず成功する問題を修正
    -   プッシュダウンされた式[#19876](https://github.com/pingcap/tidb/pull/19876)に許可されるデフォルトの最大パケット長の誤った値を修正しました。
    -   `ENUM` / `SET`列の`Max` / `Min`関数の誤った動作を修正[#19869](https://github.com/pingcap/tidb/pull/19869)
    -   一部のTiFlashノードがオフラインの場合の`tiflash_segments`および`tiflash_tables`システム テーブルからの読み取りエラーを修正[#19748](https://github.com/pingcap/tidb/pull/19748)
    -   `Count(col)`集計関数の間違った結果を修正します[#19628](https://github.com/pingcap/tidb/pull/19628)
    -   `TRUNCATE`オペレーション[#19445](https://github.com/pingcap/tidb/pull/19445)の実行時エラーを修正
    -   `Var`に大文字が含まれる場合、 `PREPARE statement FROM @Var`が失敗する問題を修正[#19378](https://github.com/pingcap/tidb/pull/19378)
    -   大文字のスキーマでスキーマ文字セットを変更するとpanic[#19302](https://github.com/pingcap/tidb/pull/19302)が発生するバグを修正
    -   情報に`tikv/tiflash` [#19159](https://github.com/pingcap/tidb/pull/19159)が含まれる場合、 `information_schema.statements_summary`と`explain`の間の計画の不一致を修正します。
    -   `select into outfile` [#19725](https://github.com/pingcap/tidb/pull/19725)のファイルが存在しないというテストのエラーを修正
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`に RAID デバイス情報がない問題を修正[#19457](https://github.com/pingcap/tidb/pull/19457)
    -   `case-when`式で生成された列を持つ`add index`操作が、解析エラーが発生したときに正常に終了できるようにします[#19395](https://github.com/pingcap/tidb/pull/19395)
    -   DDL 操作のリトライに時間がかかりすぎるバグを修正[#19488](https://github.com/pingcap/tidb/pull/19488)
    -   `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)`のようなステートメントを最初に実行せずに実行させる`use db` [#19471](https://github.com/pingcap/tidb/pull/19471)
    -   サーバーログファイルのディスパッチエラーをメッセージ`Error`から`Info`に変更します[#19454](https://github.com/pingcap/tidb/pull/19454)

-   TiKV

    -   照合順序が有効になっている場合の非インデックス列の推定エラーを修正[#8620](https://github.com/tikv/tikv/pull/8620)
    -   リージョン転送[#8460](https://github.com/tikv/tikv/pull/8460)のプロセス中に Green GC がロックをミスする可能性がある問題を修正
    -   Raftメンバーシップの変更[#8497](https://github.com/tikv/tikv/pull/8497)中に TiKV の実行が非常に遅い場合に発生するpanicの問題を修正します。
    -   PD 同期リクエストを呼び出すときに PD クライアント スレッドと他のスレッドの間で発生するデッドロックの問題を修正します[#8612](https://github.com/tikv/tikv/pull/8612)
    -   巨大ページ[#8463](https://github.com/tikv/tikv/pull/8463)のメモリ割り当ての問題に対処するために、jemalloc を v5.2.1 にアップグレードします。
    -   長時間実行されるクエリに対して統合スレッド プールがハングする問題を修正します[#8427](https://github.com/tikv/tikv/pull/8427)

-   PD

    -   `initial-cluster-token`構成を追加して、ブートストラップ[#2922](https://github.com/pingcap/pd/pull/2922)中に異なるクラスターが相互に通信しないようにします。
    -   モード`auto` [#2826](https://github.com/pingcap/pd/pull/2826)時のストアリミットレートの単位を修正
    -   一部のスケジューラーがエラーを解決せずに構成を保持する問題を修正します[#2818](https://github.com/tikv/pd/pull/2818)
    -   スケジューラ[#2871](https://github.com/tikv/pd/pull/2871) [#2874](https://github.com/tikv/pd/pull/2874)の空の HTTP 応答を修正

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

        -   TiCDC が場合によってメモリリークを起こす問題を修正[#942](https://github.com/pingcap/tiflow/pull/942)
        -   Kafka シンク[#912](https://github.com/pingcap/tiflow/pull/912)で TiCDC がpanicになる可能性がある問題を修正
        -   プラー[#927](https://github.com/pingcap/tiflow/pull/927)で CommitTs または ResolvedTs (CRT) が`resolvedTs`未満になる可能性がある問題を修正
        -   `changefeed`が MySQL ドライバー[#936](https://github.com/pingcap/tiflow/pull/936)によってブロックされる可能性がある問題を修正
        -   TiCDC [#8573](https://github.com/tikv/tikv/pull/8573)の誤った解決された Ts 間隔を修正しました。

    -   バックアップと復元 (BR)

        -   チェックサム[#479](https://github.com/pingcap/br/pull/479)中に発生する可能性のあるpanicを修正しました。
        -   PDLeader[#496](https://github.com/pingcap/br/pull/496)の変更後に発生する可能性のpanicを修正

    -   Dumpling

        -   バイナリ型の`NULL`値が正しく処理されない問題を修正[#137](https://github.com/pingcap/dumpling/pull/137)

    -   TiDB Lightning

        -   失敗した書き込みおよび取り込み操作がすべて誤って成功として表示される問題を修正します[#381](https://github.com/pingcap/tidb-lightning/pull/381)
        -   TiDB Lightningが終了する前に、一部のチェックポイント更新がデータベースに書き込まれない可能性がある問題を修正します[#386](https://github.com/pingcap/tidb-lightning/pull/386)
