---
title: TiDB 4.0.6 Release Notes
summary: TiDB 4.0.6は2020年9月15日にリリースされました。新機能には、外部結合のためのTiFlashサポートとTiDB Dashboardの改善が含まれます。TiCDCやTiKVなどのツールもアップデートされました。このリリースには、TiDB、TiKV、PD、 TiFlash、および各種ツールのバグ修正が含まれています。
---

# TiDB 4.0.6 リリースノート {#tidb-4-0-6-release-notes}

発売日：2020年9月15日

TiDB バージョン: 4.0.6

## 新機能 {#new-features}

-   TiFlash

    -   TiFlashブロードキャスト結合で外部結合をサポート

-   TiDB Dashboard

    -   クエリエディタと実行UIの追加（実験的） [＃713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    -   ストアロケーショントポロジ可視化サポート [＃719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
    -   クラスタ構成UIの追加（実験的） [＃733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    -   現在のセッション共有をサポート [＃741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
    -   SQLステートメントリストで実行プランの数を表示する機能をサポート [＃746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)

-   ツール

    -   TiCDC (v4.0.6 以降 GA)

## 改善点 {#improvements}

-   TiDB

    -   エラーコードとメッセージを標準エラーに置き換える[＃19888](https://github.com/pingcap/tidb/pull/19888)
    -   パーティションテーブルの書き込みパフォーマンスを向上させる [＃19649](https://github.com/pingcap/tidb/pull/19649)
    -   `Cop Runtime`統計でより多くのRPC実行時情報を記録 [＃19264](https://github.com/pingcap/tidb/pull/19264)
    -   `metrics_schema`と`performance_schema` でのテーブル作成を禁止する [＃19792](https://github.com/pingcap/tidb/pull/19792)
    -   ユニオンエグゼキュータの同時実行の調整をサポート [＃19886](https://github.com/pingcap/tidb/pull/19886)
    -   外部結合とブロードキャスト結合をサポート[＃19664](https://github.com/pingcap/tidb/pull/19664)
    -   プロセスリストのSQLダイジェストを追加する [＃19829](https://github.com/pingcap/tidb/pull/19829)
    -   自動コミット文の再試行ために悲観的トランザクションモードに切り替える [＃19796](https://github.com/pingcap/tidb/pull/19796)
    -   `Str_to_date()` の`%r`と`%T`データ形式をサポート [＃19693](https://github.com/pingcap/tidb/pull/19693)
    -   `SELECT INTO OUTFILE`有効にするとファイル権限必要になります [＃19577](https://github.com/pingcap/tidb/pull/19577)
    -   `stddev_pop`機能サポートする [＃19541](https://github.com/pingcap/tidb/pull/19541)
    -   `TiDB-Runtime`ダッシュボードを追加する [＃19396](https://github.com/pingcap/tidb/pull/19396)
    -   `ALTER TABLE`アルゴリズム互換性を向上 [＃19364](https://github.com/pingcap/tidb/pull/19364)
    -   スローログ`plan`フィールドに`insert`プラン`delete`エンコード`update` [＃19269](https://github.com/pingcap/tidb/pull/19269)

-   TiKV

    -   `DropTable`または`TruncateTable`実行中に QPS の低下を減らす[＃8627](https://github.com/tikv/tikv/pull/8627)
    -   エラーコードのメタファイル生成をサポート[＃8619](https://github.com/tikv/tikv/pull/8619)
    -   cfスキャンの詳細にパフォーマンス統計を追加 [＃8618](https://github.com/tikv/tikv/pull/8618)
    -   Grafanaのデフォルトテンプレートに`rocksdb perf context`パネルを追加する [＃8467](https://github.com/tikv/tikv/pull/8467)

-   PD

    -   TiDB Dashboardをv2020.09.08.1 に更新 [＃2928](https://github.com/pingcap/pd/pull/2928)
    -   リージョンとストアのハートビートメトリクスを追加します [＃2891](https://github.com/tikv/pd/pull/2891)
    -   低スペースしきい値を制御するための元の方法に戻す [＃2875](https://github.com/pingcap/pd/pull/2875)
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

    -   Backup & Restore (BR)

        -   概要ログにリアルタイムコストを追加 [＃486](https://github.com/pingcap/br/issues/486)

    -   Dumpling

        -   列名付き`INSERT`出力をサポート [＃135](https://github.com/pingcap/dumpling/pull/135)
        -   `--filesize`と`--statement-size`定義をmydumper の定義と統合する [＃142](https://github.com/pingcap/dumpling/pull/142)

    -   TiDB Lightning

        -   より正確なサイズでリージョンを分割して取り込む[＃369](https://github.com/pingcap/tidb-lightning/pull/369)

    -   TiDB Binlog

        -   `go time`パッケージ形式で GC 時間の設定をサポート [＃996](https://github.com/pingcap/tidb-binlog/pull/996)

## バグ修正 {#bug-fixes}

-   TiDB

    -   メトリックプロファイルで`tikv_cop_wait`回収集する問題を修正 [＃19881](https://github.com/pingcap/tidb/pull/19881)
    -   `SHOW GRANTS` の間違った結果を修正 [＃19834](https://github.com/pingcap/tidb/pull/19834)
    -   `!= ALL (subq)` の誤ったクエリ結果を修正 [＃19831](https://github.com/pingcap/tidb/pull/19831)
    -   `enum`と`set`型の変換のバグを修正 [＃19778](https://github.com/pingcap/tidb/pull/19778)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET`権限チェックを追加する[＃19760](https://github.com/pingcap/tidb/pull/19760)
    -   `builtinGreatestStringSig`と`builtinLeastStringSig` によって発生する列の長さの不一致のエラーを修正 [＃19758](https://github.com/pingcap/tidb/pull/19758)
    -   不要なエラーや警告が発生した場合、ベクトル化された制御式はスカラー実行にフォールバックします[＃19749](https://github.com/pingcap/tidb/pull/19749)
    -   相関列の型が`Bit` の場合の`Apply`演算子のエラーを修正 [＃19692](https://github.com/pingcap/tidb/pull/19692)
    -   MySQL 8.0クライアントでユーザーが`processlist`と`cluster_log`クエリするときに発生する問題を修正しました [＃19690](https://github.com/pingcap/tidb/pull/19690)
    -   同じタイプのプランが異なるプランダイジェストを持つ問題を修正[＃19684](https://github.com/pingcap/tidb/pull/19684)
    -   列タイプを`Decimal`から`Int` に変更することを禁止する [＃19682](https://github.com/pingcap/tidb/pull/19682)
    -   `SELECT ... INTO OUTFILE`ランタイムエラーを返す問題を修正 [＃19672](https://github.com/pingcap/tidb/pull/19672)
    -   `builtinRealIsFalseSig` の誤った実装を修正 [＃19670](https://github.com/pingcap/tidb/pull/19670)
    -   パーティション式チェックで括弧式欠落する問題を修正 [＃19614](https://github.com/pingcap/tidb/pull/19614)
    -   `HashJoin` に`Apply`演算子がある場合のクエリエラーを修正しました [＃19611](https://github.com/pingcap/tidb/pull/19611)
    -   `Real` `Time` に変換するベクトル化の誤った結果を修正 [＃19594](https://github.com/pingcap/tidb/pull/19594)
    -   `SHOW GRANTS`文で存在しないユーザー権限が表示されるバグを修正 [＃19588](https://github.com/pingcap/tidb/pull/19588)
    -   `IndexLookupJoin` に`Apply`実行者が存在する場合のクエリエラーを修正 [＃19566](https://github.com/pingcap/tidb/pull/19566)
    -   パーティションテーブルで`Apply`を`HashJoin`に変換するときに誤った結果が発生する問題を修正しました [＃19546](https://github.com/pingcap/tidb/pull/19546)
    -   `Apply` の内側に`IndexLookUp`エグゼキュータがある場合の誤った結果を修正しました [＃19508](https://github.com/pingcap/tidb/pull/19508)
    -   ビュー使用時に予期しないpanicが発生する問題を修正しました [＃19491](https://github.com/pingcap/tidb/pull/19491)
    -   `anti-semi-join`クエリの誤った結果を修正 [＃19477](https://github.com/pingcap/tidb/pull/19477)
    -   統計を削除しても統計`TopN`が削除されないバグを修正[＃19465](https://github.com/pingcap/tidb/pull/19465)
    -   バッチPointGetの誤った使用によって発生した誤った結果を修正 [＃19460](https://github.com/pingcap/tidb/pull/19460)
    -   仮想生成列で`indexLookupJoin`が見つからないバグを修正 [＃19439](https://github.com/pingcap/tidb/pull/19439)
    -   `select`と`update`クエリの異なるプランがデータを比較するエラーを修正しました [＃19403](https://github.com/pingcap/tidb/pull/19403)
    -   リージョンキャッシュのTiFlash作業インデックスのデータ競合を修正 [＃19362](https://github.com/pingcap/tidb/pull/19362)
    -   `logarithm`関数が警告を表示しないバグを修正[＃19291](https://github.com/pingcap/tidb/pull/19291)
    -   TiDBがディスクにデータを永続化するときに発生する予期しないエラーを修正しました [＃19272](https://github.com/pingcap/tidb/pull/19272)
    -   インデックス結合の内側で単一のパーティションテーブルの使用をサポート [＃19197](https://github.com/pingcap/tidb/pull/19197)
    -   10進数に対して生成された間違ったハッシュキー値を修正 [＃19188](https://github.com/pingcap/tidb/pull/19188)
    -   テーブルのendKeyとリージョンのendKeyが同じ場合にTiDBが`no regions`エラーを返す問題を修正しました[＃19895](https://github.com/pingcap/tidb/pull/19895)
    -   パーティション変更が予期せず成功する問題を修正 [＃19891](https://github.com/pingcap/tidb/pull/19891)
    -   プッシュダウンされた式に許可されるデフォルトの最大パケット長の誤った値を修正しました [＃19876](https://github.com/pingcap/tidb/pull/19876)
    -   `ENUM` `SET`の`Max`関数の誤った動作`Min`修正しました[＃19869](https://github.com/pingcap/tidb/pull/19869)
    -   一部のTiFlashノードがオフラインの場合の`tiflash_segments`および`tiflash_tables`システムテーブルからの読み取りエラーを修正[＃19748](https://github.com/pingcap/tidb/pull/19748)
    -   集計関数`Count(col)`の誤った結果を修正[＃19628](https://github.com/pingcap/tidb/pull/19628)
    -   `TRUNCATE`操作のランタイムエラーを修正 [＃19445](https://github.com/pingcap/tidb/pull/19445)
    -   `PREPARE statement FROM @Var` `Var`大文字が含まれていると失敗する問題を修正[＃19378](https://github.com/pingcap/tidb/pull/19378)
    -   大文字スキーマでスキーマ文字セットを変更するとpanicが発生するバグを修正[＃19302](https://github.com/pingcap/tidb/pull/19302)
    -   情報に`tikv/tiflash` 含まれている場合の`information_schema.statements_summary`と`explain`間の計画の不一致を修正します [＃19159](https://github.com/pingcap/tidb/pull/19159)
    -   `select into outfile` ファイルが存在しないというテストのエラーを修正 [＃19725](https://github.com/pingcap/tidb/pull/19725)
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE` RAIDデバイス情報がない問題を修正[＃19457](https://github.com/pingcap/tidb/pull/19457)
    -   `case-when`で生成された列を持つ`add index`操作が解析エラーに遭遇したときに正常に終了できるようにします。 [＃19395](https://github.com/pingcap/tidb/pull/19395)
    -   DDL操作の再試行に時間がかかりすぎるバグを修正[＃19488](https://github.com/pingcap/tidb/pull/19488)
    -   `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)`ような文を`use db` を実行せずに実行する [＃19471](https://github.com/pingcap/tidb/pull/19471)
    -   サーバーログファイルのディスパッチエラーを`Error`から`Info`メッセージに変更します。 [＃19454](https://github.com/pingcap/tidb/pull/19454)

-   TiKV

    -   照合順序が有効になっている場合の非インデックス列の推定エラーを修正[＃8620](https://github.com/tikv/tikv/pull/8620)
    -   リージョン転送のプロセス中に Green GC がロックを見逃す可能性がある問題を修正しました [＃8460](https://github.com/tikv/tikv/pull/8460)
    -   Raftメンバーシップの変更中に TiKV の実行が非常に遅い場合に発生するpanic問題を修正しました[＃8497](https://github.com/tikv/tikv/pull/8497)
    -   PD同期リクエストを呼び出すときにPDクライアントスレッドと他のスレッド間で発生するデッドロックの問題を修正しました[＃8612](https://github.com/tikv/tikv/pull/8612)
    -   巨大ページのメモリ割り当ての問題に対処するため、jemalloc を v5.2.1 にアップグレードします。 [＃8463](https://github.com/tikv/tikv/pull/8463)
    -   長時間実行されるクエリで統合スレッドプールがハングする問題を修正[＃8427](https://github.com/tikv/tikv/pull/8427)

-   PD

    -   ブートストラップ中に異なるクラスタが相互に通信するのを防ぐために、 `initial-cluster-token`構成を追加します。 [＃2922](https://github.com/pingcap/pd/pull/2922)
    -   モードが`auto` ときのストア制限レートの単位を修正 [＃2826](https://github.com/pingcap/pd/pull/2826)
    -   一部のスケジューラがエラーを解決せずに構成を保持する問題を修正[＃2818](https://github.com/tikv/pd/pull/2818)
    -   スケジューラ 空のHTTPレスポンスを修正 [＃2874](https://github.com/tikv/pd/pull/2874) [＃2871](https://github.com/tikv/pd/pull/2871)

-   TiFlash

    -   以前のバージョンで主キー列の名前を変更した後、v4.0.4/v4.0.5 にアップグレードするとTiFlash が起動しなくなる可能性がある問題を修正しました。
    -   列の`nullable`属性を変更した後に発生する例外を修正します
    -   テーブルのレプリケーションステータスの計算によって発生するクラッシュを修正
    -   ユーザーがサポートされていないDDL操作を適用した後に、 TiFlashがデータ読み取りに使用できなくなる問題を修正しました。
    -   `utf8mb4_bin`として扱われるサポートされていない照合によって発生する例外を修正しました
    -   TiFlashコプロセッサエグゼキュータのQPSパネルがGrafanaで常に`0`が表示される問題を修正
    -   入力が`NULL`の場合の`FROM_UNIXTIME`関数の誤った結果を修正

-   ツール

    -   TiCDC

        -   TiCDC がメモリを起こす場合がある問題を修正[＃942](https://github.com/pingcap/tiflow/pull/942)
        -   Kafka シンクで TiCDC がpanic可能性がある問題を修正しました [＃912](https://github.com/pingcap/tiflow/pull/912)
        -   プルラーでCommitTsまたはResolvedTs（CRTs）が`resolvedTs`未満になる可能性がある問題を修正しました [＃927](https://github.com/pingcap/tiflow/pull/927)
        -   `changefeed` MySQL ドライバによってブロックされる可能性がある問題を修正しました [＃936](https://github.com/pingcap/tiflow/pull/936)
        -   TiCDC の誤ったResolved Ts間隔を修正 [＃8573](https://github.com/tikv/tikv/pull/8573)

    -   Backup & Restore (BR)

        -   チェックサム中に発生する可能性のあるpanicを修正 [＃479](https://github.com/pingcap/br/pull/479)
        -   PDリーダーの変更後に発生する可能性のあるpanicを修正 [＃496](https://github.com/pingcap/br/pull/496)

    -   Dumpling

        -   バイナリ型の`NULL`値が正しく処理されない問題を修正しました[＃137](https://github.com/pingcap/dumpling/pull/137)

    -   TiDB Lightning

        -   書き込みと取り込みの失敗した操作がすべて誤って成功として表示される問題を修正[＃381](https://github.com/pingcap/tidb-lightning/pull/381)
        -   TiDB Lightning が終了する前に、一部のチェックポイント更新がデータベースに書き込まれない可能性がある問題を修正しました。 [＃386](https://github.com/pingcap/tidb-lightning/pull/386)
