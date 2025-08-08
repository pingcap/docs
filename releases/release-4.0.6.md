---
title: TiDB 4.0.6 Release Notes
summary: TiDB 4.0.6は2020年9月15日にリリースされました。新機能には、外部結合のためのTiFlashサポートとTiDBダッシュボードの改善が含まれます。TiCDCやTiKVなどのツールもアップデートされました。このリリースには、TiDB、TiKV、PD、 TiFlash、および各種ツールのバグ修正が含まれています。
---

# TiDB 4.0.6 リリースノート {#tidb-4-0-6-release-notes}

発売日：2020年9月15日

TiDB バージョン: 4.0.6

## 新機能 {#new-features}

-   TiFlash

    -   TiFlashブロードキャスト結合で外部結合をサポート

-   TiDBダッシュボード

    -   クエリエディタと実行UIの追加（実験的） [＃713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    -   店舗ロケーショントポロジ可視化[＃719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)サポート
    -   クラスタ構成UIの追加（実験的） [＃733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    -   現在のセッション[＃741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)共有をサポート
    -   SQLステートメントリスト[＃746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)で実行プランの数を表示する機能をサポート

-   ツール

    -   TiCDC (v4.0.6 以降 GA)

## 改善点 {#improvements}

-   TiDB

    -   エラーコードとメッセージを標準エラーに置き換える[＃19888](https://github.com/pingcap/tidb/pull/19888)
    -   パーティションテーブル[＃19649](https://github.com/pingcap/tidb/pull/19649)の書き込みパフォーマンスを向上させる
    -   `Cop Runtime`統計[＃19264](https://github.com/pingcap/tidb/pull/19264)でより多くのRPC実行時情報を記録
    -   `metrics_schema`と`performance_schema` [＃19792](https://github.com/pingcap/tidb/pull/19792)でのテーブル作成を禁止する
    -   ユニオンエグゼキュータ[＃19886](https://github.com/pingcap/tidb/pull/19886)の同時実行の調整をサポート
    -   サポートアウト参加イン放送参加[＃19664](https://github.com/pingcap/tidb/pull/19664)
    -   プロセスリスト[＃19829](https://github.com/pingcap/tidb/pull/19829)のSQLダイジェストを追加する
    -   自動コミット文の再試行[＃19796](https://github.com/pingcap/tidb/pull/19796)ために悲観的トランザクションモードに切り替える
    -   `Str_to_date()` [＃19693](https://github.com/pingcap/tidb/pull/19693)の`%r`と`%T`データ形式をサポート
    -   `SELECT INTO OUTFILE`有効にするとファイル権限[＃19577](https://github.com/pingcap/tidb/pull/19577)必要になります
    -   `stddev_pop`機能[＃19541](https://github.com/pingcap/tidb/pull/19541)サポートする
    -   `TiDB-Runtime`ダッシュボード[＃19396](https://github.com/pingcap/tidb/pull/19396)を追加する
    -   `ALTER TABLE`アルゴリズム[＃19364](https://github.com/pingcap/tidb/pull/19364)互換性を向上
    -   スローログ`plan`フィールド[＃19269](https://github.com/pingcap/tidb/pull/19269)に`insert`プラン`delete`エンコード`update`

-   TiKV

    -   `DropTable`または`TruncateTable`実行中に QPS の低下を減らす[＃8627](https://github.com/tikv/tikv/pull/8627)
    -   エラーコードのメタファイル生成をサポート[＃8619](https://github.com/tikv/tikv/pull/8619)
    -   cfスキャンの詳細[＃8618](https://github.com/tikv/tikv/pull/8618)にパフォーマンス統計を追加
    -   Grafanaのデフォルトテンプレート[＃8467](https://github.com/tikv/tikv/pull/8467)に`rocksdb perf context`パネルを追加する

-   PD

    -   TiDBダッシュボードをv2020.09.08.1 [＃2928](https://github.com/pingcap/pd/pull/2928)に更新
    -   リージョンとストアのハートビート[＃2891](https://github.com/tikv/pd/pull/2891)メトリクスを追加します
    -   低スペースしきい値[＃2875](https://github.com/pingcap/pd/pull/2875)を制御するための元の方法に戻す
    -   標準エラーコードのサポート
        -   [＃2918](https://github.com/tikv/pd/pull/2918) [＃2911](https://github.com/tikv/pd/pull/2911) [＃2913](https://github.com/tikv/pd/pull/2913) [＃2915](https://github.com/tikv/pd/pull/2915) [＃2912](https://github.com/tikv/pd/pull/2912)
        -   [＃2907](https://github.com/tikv/pd/pull/2907) [＃2906](https://github.com/tikv/pd/pull/2906) [＃2903](https://github.com/tikv/pd/pull/2903) [＃2806](https://github.com/tikv/pd/pull/2806) [＃2900](https://github.com/tikv/pd/pull/2900) [＃2902](https://github.com/tikv/pd/pull/2902)

-   TiFlash

    -   データ複製用のGrafanaパネルを追加する（ `apply Region snapshots`と`ingest SST files` ）
    -   `write stall`のGrafanaパネルを追加
    -   `dt_segment_force_merge_delta_rows`と`dt_segment_force_merge_delta_deletes`加算して`write stall`のしきい値を調整する
    -   TiFlash-Proxy で設定`raftstore.snap-handle-pool-size` ～ `0`サポートし、マルチスレッドによるリージョンスナップショットの適用を無効にして、データ複製時のメモリ消費を削減します。
    -   `https_port`と`metrics_port`のCNチェックをサポート

-   ツール

    -   TiCDC

        -   プーラー初期化中に解決されたロックをスキップする[＃910](https://github.com/pingcap/tiflow/pull/910)
        -   PD書き込み頻度を減らす[＃937](https://github.com/pingcap/tiflow/pull/937)

    -   バックアップと復元 (BR)

        -   概要ログ[＃486](https://github.com/pingcap/br/issues/486)にリアルタイムコストを追加

    -   Dumpling

        -   列名[＃135](https://github.com/pingcap/dumpling/pull/135)付き`INSERT`出力をサポート
        -   `--filesize`と`--statement-size`定義をmydumper [＃142](https://github.com/pingcap/dumpling/pull/142)の定義と統合する

    -   TiDB Lightning

        -   より正確なサイズで領域を分割して取り込む[＃369](https://github.com/pingcap/tidb-lightning/pull/369)

    -   TiDBBinlog

        -   `go time`パッケージ形式[＃996](https://github.com/pingcap/tidb-binlog/pull/996)で GC 時間の設定をサポート

## バグ修正 {#bug-fixes}

-   TiDB

    -   メトリックプロファイル[＃19881](https://github.com/pingcap/tidb/pull/19881)で`tikv_cop_wait`回収集する問題を修正
    -   `SHOW GRANTS` [＃19834](https://github.com/pingcap/tidb/pull/19834)の間違った結果を修正
    -   `!= ALL (subq)` [＃19831](https://github.com/pingcap/tidb/pull/19831)の誤ったクエリ結果を修正
    -   `enum`と`set`型[＃19778](https://github.com/pingcap/tidb/pull/19778)の変換のバグを修正
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET`権限チェックを追加する[＃19760](https://github.com/pingcap/tidb/pull/19760)
    -   `builtinGreatestStringSig`と`builtinLeastStringSig` [＃19758](https://github.com/pingcap/tidb/pull/19758)によって発生する列の長さの不一致のエラーを修正
    -   不要なエラーや警告が発生した場合、ベクトル化された制御式はスカラー実行にフォールバックします[＃19749](https://github.com/pingcap/tidb/pull/19749)
    -   相関列の型が`Bit` [＃19692](https://github.com/pingcap/tidb/pull/19692)の場合の`Apply`演算子のエラーを修正
    -   MySQL 8.0クライアント[＃19690](https://github.com/pingcap/tidb/pull/19690)でユーザーが`processlist`と`cluster_log`クエリするときに発生する問題を修正しました
    -   同じタイプのプランが異なるプランダイジェストを持つ問題を修正[＃19684](https://github.com/pingcap/tidb/pull/19684)
    -   列タイプを`Decimal`から`Int` [＃19682](https://github.com/pingcap/tidb/pull/19682)に変更することを禁止する
    -   `SELECT ... INTO OUTFILE`ランタイムエラー[＃19672](https://github.com/pingcap/tidb/pull/19672)を返す問題を修正
    -   `builtinRealIsFalseSig` [＃19670](https://github.com/pingcap/tidb/pull/19670)の誤った実装を修正
    -   パーティション式チェックで括弧式[＃19614](https://github.com/pingcap/tidb/pull/19614)欠落する問題を修正
    -   `HashJoin` [＃19611](https://github.com/pingcap/tidb/pull/19611)に`Apply`演算子がある場合のクエリエラーを修正しました
    -   `Real` `Time` [＃19594](https://github.com/pingcap/tidb/pull/19594)に変換するベクトル化の誤った結果を修正
    -   `SHOW GRANTS`文で存在しないユーザー[＃19588](https://github.com/pingcap/tidb/pull/19588)権限が表示されるバグを修正
    -   `IndexLookupJoin` [＃19566](https://github.com/pingcap/tidb/pull/19566)に`Apply`実行者が存在する場合のクエリエラーを修正
    -   パーティションテーブル[＃19546](https://github.com/pingcap/tidb/pull/19546)で`Apply`を`HashJoin`に変換するときに誤った結果が発生する問題を修正しました
    -   `Apply` [＃19508](https://github.com/pingcap/tidb/pull/19508)の内側に`IndexLookUp`エグゼキュータがある場合の誤った結果を修正しました
    -   ビュー[＃19491](https://github.com/pingcap/tidb/pull/19491)使用時に予期しないpanicが発生する問題を修正しました
    -   `anti-semi-join`クエリ[＃19477](https://github.com/pingcap/tidb/pull/19477)の誤った結果を修正
    -   統計を削除しても統計`TopN`が削除されないバグを修正[＃19465](https://github.com/pingcap/tidb/pull/19465)
    -   バッチポイント取得[＃19460](https://github.com/pingcap/tidb/pull/19460)の誤った使用によって発生した誤った結果を修正
    -   仮想生成列[＃19439](https://github.com/pingcap/tidb/pull/19439)で`indexLookupJoin`が見つからないバグを修正
    -   `select`と`update`クエリの異なるプランがデータ[＃19403](https://github.com/pingcap/tidb/pull/19403)を比較するエラーを修正しました
    -   リージョンキャッシュ[＃19362](https://github.com/pingcap/tidb/pull/19362)のTiFlash作業インデックスのデータ競合を修正
    -   `logarithm`関数が警告を表示しないバグを修正[＃19291](https://github.com/pingcap/tidb/pull/19291)
    -   TiDBがディスク[＃19272](https://github.com/pingcap/tidb/pull/19272)にデータを永続化するときに発生する予期しないエラーを修正しました
    -   インデックス結合[＃19197](https://github.com/pingcap/tidb/pull/19197)の内側で単一のパーティションテーブルの使用をサポート
    -   10進数[＃19188](https://github.com/pingcap/tidb/pull/19188)に対して生成された間違ったハッシュキー値を修正
    -   テーブルのendKeyとリージョンのendKeyが同じ場合にTiDBが`no regions`エラーを返す問題を修正しました[＃19895](https://github.com/pingcap/tidb/pull/19895)
    -   パーティション[＃19891](https://github.com/pingcap/tidb/pull/19891)変更が予期せず成功する問題を修正
    -   プッシュダウンされた式[＃19876](https://github.com/pingcap/tidb/pull/19876)に許可されるデフォルトの最大パケット長の誤った値を修正しました
    -   `ENUM` `SET`の`Max`関数の誤った動作`Min`修正しました[＃19869](https://github.com/pingcap/tidb/pull/19869)
    -   一部のTiFlashノードがオフラインの場合の`tiflash_segments`および`tiflash_tables`システムテーブルからの読み取りエラーを修正[＃19748](https://github.com/pingcap/tidb/pull/19748)
    -   集計関数`Count(col)`の誤った結果を修正[＃19628](https://github.com/pingcap/tidb/pull/19628)
    -   `TRUNCATE`操作[＃19445](https://github.com/pingcap/tidb/pull/19445)のランタイムエラーを修正
    -   `PREPARE statement FROM @Var` `Var`大文字が含まれていると失敗する問題を修正[＃19378](https://github.com/pingcap/tidb/pull/19378)
    -   大文字スキーマでスキーマ文字セットを変更するとpanicが発生するバグを修正[＃19302](https://github.com/pingcap/tidb/pull/19302)
    -   情報に`tikv/tiflash` [＃19159](https://github.com/pingcap/tidb/pull/19159)含まれている場合の`information_schema.statements_summary`と`explain`間の計画の不一致を修正します
    -   `select into outfile` [＃19725](https://github.com/pingcap/tidb/pull/19725)ファイルが存在しないというテストのエラーを修正
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE` RAIDデバイス情報がない問題を修正[＃19457](https://github.com/pingcap/tidb/pull/19457)
    -   `case-when`で生成された列を持つ`add index`操作が解析エラー[＃19395](https://github.com/pingcap/tidb/pull/19395)に遭遇したときに正常に終了できるようにします。
    -   DDL操作の再試行に時間がかかりすぎるバグを修正[＃19488](https://github.com/pingcap/tidb/pull/19488)
    -   `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)`ような文を`use db` [＃19471](https://github.com/pingcap/tidb/pull/19471)を実行せずに実行する
    -   サーバーログファイル[＃19454](https://github.com/pingcap/tidb/pull/19454)のディスパッチエラーを`Error`から`Info`メッセージに変更します。

-   TiKV

    -   照合順序が有効になっている場合の非インデックス列の推定エラーを修正[＃8620](https://github.com/tikv/tikv/pull/8620)
    -   リージョン転送[＃8460](https://github.com/tikv/tikv/pull/8460)のプロセス中に Green GC がロックを見逃す可能性がある問題を修正しました
    -   Raftメンバーシップの変更中に TiKV の実行が非常に遅い場合に発生するpanic問題を修正しました[＃8497](https://github.com/tikv/tikv/pull/8497)
    -   PD同期リクエストを呼び出すときにPDクライアントスレッドと他のスレッド間で発生するデッドロックの問題を修正しました[＃8612](https://github.com/tikv/tikv/pull/8612)
    -   巨大ページ[＃8463](https://github.com/tikv/tikv/pull/8463)のメモリ割り当ての問題に対処するため、jemalloc を v5.2.1 にアップグレードします。
    -   長時間実行されるクエリで統合スレッドプールがハングする問題を修正[＃8427](https://github.com/tikv/tikv/pull/8427)

-   PD

    -   ブートストラップ[＃2922](https://github.com/pingcap/pd/pull/2922)中に異なるクラスタが相互に通信するのを防ぐために、 `initial-cluster-token`構成を追加します。
    -   モードが`auto` [＃2826](https://github.com/pingcap/pd/pull/2826)ときの店舗制限レートの単位を修正
    -   一部のスケジューラがエラーを解決せずに構成を保持する問題を修正[＃2818](https://github.com/tikv/pd/pull/2818)
    -   スケジューラ[＃2871](https://github.com/tikv/pd/pull/2871) [＃2874](https://github.com/tikv/pd/pull/2874)空のHTTPレスポンスを修正

-   TiFlash

    -   以前のバージョンで主キー列の名前を変更した後、v4.0.4/v4.0.5 にアップグレードするとTiFlash が起動しなくなる可能性がある問題を修正しました。
    -   列の`nullable`属性を変更した後に発生する例外を修正します
    -   テーブルのレプリケーションステータスの計算によって発生するクラッシュを修正
    -   ユーザーがサポートされていないDDL操作を適用した後に、 TiFlashがデータ読み取りに使用できなくなる問題を修正しました。
    -   `utf8mb4_bin`として扱われるサポートされていない照合によって発生する例外を修正しました
    -   TiFlashコプロセッサエグゼキュータのQPSパネルがGrafanaで常に`0`表示される問題を修正
    -   入力が`NULL`場合の`FROM_UNIXTIME`関数の誤った結果を修正

-   ツール

    -   TiCDC

        -   TiCDC がメモリを起こす場合がある問題を修正[＃942](https://github.com/pingcap/tiflow/pull/942)
        -   Kafka シンク[＃912](https://github.com/pingcap/tiflow/pull/912)で TiCDC がpanic可能性がある問題を修正しました
        -   プルラー[＃927](https://github.com/pingcap/tiflow/pull/927)でCommitTsまたはResolvedTs（CRTs）が`resolvedTs`未満になる可能性がある問題を修正しました
        -   `changefeed` MySQL ドライバ[＃936](https://github.com/pingcap/tiflow/pull/936)によってブロックされる可能性がある問題を修正しました
        -   TiCDC [＃8573](https://github.com/tikv/tikv/pull/8573)の誤ったResolved Ts間隔を修正

    -   バックアップと復元 (BR)

        -   チェックサム[＃479](https://github.com/pingcap/br/pull/479)中に発生する可能性のあるpanicを修正
        -   PDLeader[＃496](https://github.com/pingcap/br/pull/496)の変更後に発生する可能性のあるpanicを修正

    -   Dumpling

        -   バイナリタイプの`NULL`値が正しく処理されない問題を修正しました[＃137](https://github.com/pingcap/dumpling/pull/137)

    -   TiDB Lightning

        -   書き込みと取り込みの失敗した操作がすべて誤って成功として表示される問題を修正[＃381](https://github.com/pingcap/tidb-lightning/pull/381)
        -   TiDB Lightning [＃386](https://github.com/pingcap/tidb-lightning/pull/386)が終了する前に、一部のチェックポイント更新がデータベースに書き込まれない可能性がある問題を修正しました。
