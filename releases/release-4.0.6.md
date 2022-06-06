---
title: TiDB 4.0.6 Release Notes
---

# TiDB4.0.6リリースノート {#tidb-4-0-6-release-notes}

発売日：2020年9月15日

TiDBバージョン：4.0.6

## 新機能 {#new-features}

-   TiFlash

    -   TiFlashブロードキャスト参加で外部参加をサポート

-   TiDBダッシュボード

    -   クエリエディタと実行UIを追加する（実験的） [＃713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    -   店舗の場所のトポロジーの視覚化をサポートする[＃719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
    -   クラスタ構成UIの追加（実験的） [＃733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    -   現在のセッションの共有をサポートする[＃741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
    -   SQLステートメントリスト[＃746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)での実行プランの数の表示をサポート

-   ツール

    -   TiCDC（v4.0.6以降のGA）

        -   `maxwell`形式でのデータ出力をサポート[＃869](https://github.com/pingcap/tiflow/pull/869)

## 改善 {#improvements}

-   TiDB

    -   エラーコードとメッセージを標準エラーに置き換える[＃19888](https://github.com/pingcap/tidb/pull/19888)
    -   パーティションテーブル[＃19649](https://github.com/pingcap/tidb/pull/19649)の書き込みパフォーマンスを向上させる
    -   `Cop Runtime`の統計にRPCランタイム情報をさらに記録する[＃19264](https://github.com/pingcap/tidb/pull/19264)
    -   `metrics_schema`と`performance_schema`でのテーブルの作成を[＃19792](https://github.com/pingcap/tidb/pull/19792)する
    -   ユニオンエグゼキュータ[＃19886](https://github.com/pingcap/tidb/pull/19886)の同時実行性の調整をサポート
    -   ブロードキャスト参加[＃19664](https://github.com/pingcap/tidb/pull/19664)での参加のサポート
    -   プロセスリストのSQLダイジェストを追加する[＃19829](https://github.com/pingcap/tidb/pull/19829)
    -   autocommitステートメントの再試行のために悲観的なトランザクションモードに切り替えます[＃19796](https://github.com/pingcap/tidb/pull/19796)
    -   `Str_to_date()`で`%r`および`%T`データ形式を[＃19693](https://github.com/pingcap/tidb/pull/19693)する
    -   `SELECT INTO OUTFILE`を有効にすると、ファイル特権[＃19577](https://github.com/pingcap/tidb/pull/19577)が必要になります
    -   `stddev_pop`機能[＃19541](https://github.com/pingcap/tidb/pull/19541)をサポート
    -   `TiDB-Runtime`のダッシュボードを追加します[＃19396](https://github.com/pingcap/tidb/pull/19396)
    -   `ALTER TABLE`アルゴリズムの互換性を向上させる[＃19364](https://github.com/pingcap/tidb/pull/19364)
    -   スローログ`update`フィールド`plan`に`insert`プランを[＃19269](https://github.com/pingcap/tidb/pull/19269)し`delete`

-   TiKV

    -   `DropTable`または`TruncateTable`が実行されているときのQPSドロップを減らします[＃8627](https://github.com/tikv/tikv/pull/8627)
    -   エラーコードのメタファイルの生成をサポート[＃8619](https://github.com/tikv/tikv/pull/8619)
    -   cfスキャン詳細のパフォーマンス統計を追加する[＃8618](https://github.com/tikv/tikv/pull/8618)
    -   Grafanaのデフォルトテンプレート[＃8467](https://github.com/tikv/tikv/pull/8467)に`rocksdb perf context`のパネルを追加します

-   PD

    -   TiDBダッシュボードをv2020.09.08.1に更新します[＃2928](https://github.com/pingcap/pd/pull/2928)
    -   リージョンのメトリックをさらに追加し、ハートビート[＃2891](https://github.com/tikv/pd/pull/2891)を保存します
    -   元の方法に戻って、低スペースのしきい値を制御します[＃2875](https://github.com/pingcap/pd/pull/2875)
    -   標準エラーコードをサポートする
        -   [＃2918](https://github.com/tikv/pd/pull/2918) [＃2911](https://github.com/tikv/pd/pull/2911) [＃2913](https://github.com/tikv/pd/pull/2913) [＃2915](https://github.com/tikv/pd/pull/2915) [＃2912](https://github.com/tikv/pd/pull/2912)
        -   [＃2907](https://github.com/tikv/pd/pull/2907) [＃2906](https://github.com/tikv/pd/pull/2906) [＃2903](https://github.com/tikv/pd/pull/2903) [＃2806](https://github.com/tikv/pd/pull/2806) [＃2900](https://github.com/tikv/pd/pull/2900) [＃2902](https://github.com/tikv/pd/pull/2902)

-   TiFlash

    -   データ複製用のGrafanaパネルを追加します（ `apply Region snapshots`および`ingest SST files` ）
    -   `write stall`のGrafanaパネルを追加
    -   `dt_segment_force_merge_delta_rows`と`dt_segment_force_merge_delta_deletes`を追加して、 `write stall`のしきい値を調整します
    -   データレプリケーション中のメモリ消費を削減するためにマルチスレッドによるリージョンスナップショットの適用を無効にするTiFlash-Proxyの設定`raftstore.snap-handle-pool-size`から`0`をサポート
    -   `https_port`と`metrics_port`のCNチェックをサポート

-   ツール

    -   TiCDC

        -   プーラーの初期化中に解決されたロックをスキップする[＃910](https://github.com/pingcap/tiflow/pull/910)
        -   PDの書き込み頻度を減らす[＃937](https://github.com/pingcap/tiflow/pull/937)

    -   バックアップと復元（BR）

        -   サマリーログ[＃486](https://github.com/pingcap/br/issues/486)にリアルタイムのコストを追加します

    -   Dumpling

        -   列名[＃135](https://github.com/pingcap/dumpling/pull/135)で`INSERT`を出力することをサポートします
        -   `--filesize`と`--statement-size`の定義をmydumper5の定義と統合し[＃142](https://github.com/pingcap/dumpling/pull/142)

    -   TiDB Lightning

        -   より正確なサイズでリージョンを分割して取り込む[＃369](https://github.com/pingcap/tidb-lightning/pull/369)

    -   TiDB Binlog

        -   `go time`パッケージ形式でのGC時間の設定をサポート[＃996](https://github.com/pingcap/tidb-binlog/pull/996)

## バグの修正 {#bug-fixes}

-   TiDB

    -   メトリックプロファイル[＃19881](https://github.com/pingcap/tidb/pull/19881)で`tikv_cop_wait`回収集する問題を修正します
    -   [＃19834](https://github.com/pingcap/tidb/pull/19834)の間違った結果を修正し`SHOW GRANTS`
    -   [＃19831](https://github.com/pingcap/tidb/pull/19831)の誤ったクエリ結果を修正し`!= ALL (subq)`
    -   `enum`と`set`のタイプを変換するバグを修正します[＃19778](https://github.com/pingcap/tidb/pull/19778)
    -   `SHOW STATS_META`と[＃19760](https://github.com/pingcap/tidb/pull/19760)の特権チェックを追加し`SHOW STATS_BUCKET`
    -   `builtinGreatestStringSig`と[＃19758](https://github.com/pingcap/tidb/pull/19758)によって引き起こされる不一致の列の長さのエラーを修正し`builtinLeastStringSig`
    -   不要なエラーや警告が発生した場合、ベクトル化された制御式はスカラー実行にフォールバックします[＃19749](https://github.com/pingcap/tidb/pull/19749)
    -   相関列のタイプが[＃19692](https://github.com/pingcap/tidb/pull/19692)の場合の`Apply`演算子のエラーを修正し`Bit`
    -   ユーザーがMySQL8.0クライアント[＃19690](https://github.com/pingcap/tidb/pull/19690)で`processlist`と`cluster_log`をクエリしたときに発生する問題を修正します
    -   同じタイプのプランのプランダイジェストが異なるという問題を修正します[＃19684](https://github.com/pingcap/tidb/pull/19684)
    -   列タイプを`Decimal`から35に変更することを[＃19682](https://github.com/pingcap/tidb/pull/19682)し`Int`
    -   `SELECT ... INTO OUTFILE`がランタイムエラー[＃19672](https://github.com/pingcap/tidb/pull/19672)を返す問題を修正します
    -   [＃19670](https://github.com/pingcap/tidb/pull/19670)の誤った実装を修正し`builtinRealIsFalseSig`
    -   パーティション式のチェックで括弧式[＃19614](https://github.com/pingcap/tidb/pull/19614)が欠落する問題を修正します
    -   [＃19611](https://github.com/pingcap/tidb/pull/19611)に`Apply`の演算子がある場合のクエリエラーを修正し`HashJoin`
    -   `Real`を[＃19594](https://github.com/pingcap/tidb/pull/19594)としてキャストするベクトル化の誤った結果を修正し`Time`
    -   `SHOW GRANTS`ステートメントが存在しないユーザーへの付与を示すバグを修正します[＃19588](https://github.com/pingcap/tidb/pull/19588)
    -   35に`Apply` [＃19566](https://github.com/pingcap/tidb/pull/19566)エグゼキュータがある場合のクエリエラーを修正し`IndexLookupJoin`
    -   パーティションテーブル[＃19546](https://github.com/pingcap/tidb/pull/19546)で`Apply`を`HashJoin`に変換するときの間違った結果を修正します
    -   [＃19508](https://github.com/pingcap/tidb/pull/19508)の内側に`IndexLookUp` `Apply`エグゼキュータがある場合の誤った結果を修正
    -   ビュー[＃19491](https://github.com/pingcap/tidb/pull/19491)を使用する際の予期しないパニックを修正
    -   `anti-semi-join`クエリ[＃19477](https://github.com/pingcap/tidb/pull/19477)の誤った結果を修正します
    -   統計が削除されたときに`TopN`統計が削除されないバグを修正します[＃19465](https://github.com/pingcap/tidb/pull/19465)
    -   バッチポイント[＃19460](https://github.com/pingcap/tidb/pull/19460)の誤った使用によって引き起こされた間違った結果を修正します
    -   仮想生成された列[＃19439](https://github.com/pingcap/tidb/pull/19439)で列が`indexLookupJoin`に見つからないというバグを修正します
    -   `select`クエリと`update`クエリの異なるプランがデータム[＃19403](https://github.com/pingcap/tidb/pull/19403)を比較するというエラーを修正します
    -   リージョンキャッシュ[＃19362](https://github.com/pingcap/tidb/pull/19362)のTiFlash作業インデックスのデータ競合を修正
    -   `logarithm`関数が警告を表示しないバグを修正します[＃19291](https://github.com/pingcap/tidb/pull/19291)
    -   TiDBがデータをディスクに保持するときに発生する予期しないエラーを修正します[＃19272](https://github.com/pingcap/tidb/pull/19272)
    -   インデックス結合[＃19197](https://github.com/pingcap/tidb/pull/19197)の内側で単一のパーティションテーブルを使用することをサポートします
    -   10進数[＃19188](https://github.com/pingcap/tidb/pull/19188)に対して生成された間違ったハッシュキー値を修正します
    -   テーブルendKeyとRegionendKeyが同じ場合にTiDBが`no regions`エラーを返す問題を修正します[＃19895](https://github.com/pingcap/tidb/pull/19895)
    -   パーティション[＃19891](https://github.com/pingcap/tidb/pull/19891)の変更の予期しない成功を修正
    -   プッシュダウン式で許可されるデフォルトの最大パケット長の誤った値を修正します[＃19876](https://github.com/pingcap/tidb/pull/19876)
    -   `ENUM`列の`Max` [＃19869](https://github.com/pingcap/tidb/pull/19869)の誤った動作を修正し`Min` `SET`
    -   一部のTiFlashノードがオフラインの場合の`tiflash_segments`および`tiflash_tables`システムテーブルからの読み取りエラーを修正します[＃19748](https://github.com/pingcap/tidb/pull/19748)
    -   `Count(col)`集計関数[＃19628](https://github.com/pingcap/tidb/pull/19628)の間違った結果を修正します
    -   `TRUNCATE`操作の実行時エラーを修正します[＃19445](https://github.com/pingcap/tidb/pull/19445)
    -   `Var`に大文字の文字が含まれていると`PREPARE statement FROM @Var`が失敗する問題を修正します[＃19378](https://github.com/pingcap/tidb/pull/19378)
    -   大文字のスキーマでスキーマ文字セットを変更するとパニックが発生するバグを修正します[＃19302](https://github.com/pingcap/tidb/pull/19302)
    -   情報に[＃19159](https://github.com/pingcap/tidb/pull/19159)が含まれている場合に、 `information_schema.statements_summary`と`explain`の間の計画の不整合を修正し`tikv/tiflash` 。
    -   `select into outfile`のファイルが存在しないというテストのエラーを修正し[＃19725](https://github.com/pingcap/tidb/pull/19725)
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`にRAIDデバイス情報がないという問題を修正します[＃19457](https://github.com/pingcap/tidb/pull/19457)
    -   `case-when`式で生成された列を持つ`add index`操作を、解析エラー[＃19395](https://github.com/pingcap/tidb/pull/19395)が発生したときに正常に終了できるようにします。
    -   DDL操作が再試行に時間がかかりすぎるというバグを修正します[＃19488](https://github.com/pingcap/tidb/pull/19488)
    -   最初に`use db`を実行せずに`alter table db.t1 add constraint fk foreign key (c2) references t2(c1)`のような[＃19471](https://github.com/pingcap/tidb/pull/19471)を実行する
    -   サーバーログファイル[＃19454](https://github.com/pingcap/tidb/pull/19454)のディスパッチエラーを`Error`から`Info`のメッセージに変更します。

-   TiKV

    -   照合順序が有効になっている場合の非インデックス列の推定エラーを修正[＃8620](https://github.com/tikv/tikv/pull/8620)
    -   リージョン転送[＃8460](https://github.com/tikv/tikv/pull/8460)のプロセス中にGreenGCがロックを見逃す可能性がある問題を修正します
    -   Raftメンバーシップの変更中にTiKVの実行が非常に遅い場合に発生するパニックの問題を修正します[＃8497](https://github.com/tikv/tikv/pull/8497)
    -   PD同期要求を呼び出すときにPDクライアントスレッドと他のスレッドの間で発生するデッドロックの問題を修正します[＃8612](https://github.com/tikv/tikv/pull/8612)
    -   jemallocをv5.2.1にアップグレードして、巨大なページ[＃8463](https://github.com/tikv/tikv/pull/8463)のメモリ割り当ての問題に対処します。
    -   長時間実行されるクエリで統合スレッドプールがハングする問題を修正します[＃8427](https://github.com/tikv/tikv/pull/8427)

-   PD

    -   `initial-cluster-token`の構成を追加して、ブートストラップ[＃2922](https://github.com/pingcap/pd/pull/2922)中に異なるクラスターが相互に通信しないようにします。
    -   [＃2826](https://github.com/pingcap/pd/pull/2826)が`auto`の場合の店舗制限率の単位を修正する
    -   一部のスケジューラーがエラーを解決せずに構成を保持する問題を修正します[＃2818](https://github.com/tikv/pd/pull/2818)
    -   スケジューラー[＃2871](https://github.com/tikv/pd/pull/2871)の空のHTTP応答を修正します[＃2874](https://github.com/tikv/pd/pull/2874)

-   TiFlash

    -   以前のバージョンで主キー列の名前を変更した後、v4.0.4/v4.0.5にアップグレードした後にTiFlashが起動しない可能性がある問題を修正します
    -   列の`nullable`属性を変更した後に発生する例外を修正します
    -   テーブルのレプリケーションステータスの計算によって引き起こされるクラッシュを修正します
    -   ユーザーがサポートされていないDDL操作を適用した後、TiFlashがデータ読み取りに使用できない問題を修正します
    -   `utf8mb4_bin`として扱われるサポートされていない照合によって引き起こされる例外を修正します
    -   TiFlashコプロセッサーエグゼキューターのQPSパネルがGrafanaで常に`0`を表示する問題を修正します
    -   入力が`NULL`の場合の`FROM_UNIXTIME`関数の誤った結果を修正します

-   ツール

    -   TiCDC

        -   場合によってはTiCDCがメモリをリークする問題を修正します[＃942](https://github.com/pingcap/tiflow/pull/942)
        -   TiCDCがKafkaシンク[＃912](https://github.com/pingcap/tiflow/pull/912)でパニックになる可能性がある問題を修正します
        -   プーラー[＃927](https://github.com/pingcap/tiflow/pull/927)でCommitTまたはResolvedT（CRT）が`resolvedTs`未満になる可能性がある問題を修正します
        -   `changefeed`がMySQLドライバー[＃936](https://github.com/pingcap/tiflow/pull/936)によってブロックされる可能性がある問題を修正します
        -   TiCDC1の誤った解決済みTs間隔を修正し[＃8573](https://github.com/tikv/tikv/pull/8573)

    -   バックアップと復元（BR）

        -   チェックサム[＃479](https://github.com/pingcap/br/pull/479)中に発生する可能性のあるパニックを修正する
        -   PDリーダー[＃496](https://github.com/pingcap/br/pull/496)の変更後に発生する可能性のあるパニックを修正します

    -   Dumpling

        -   バイナリタイプの`NULL`値が適切に処理されない問題を修正します[＃137](https://github.com/pingcap/dumpling/pull/137)

    -   TiDB Lightning

        -   書き込みと取り込みのすべての失敗した操作が誤って成功として表示される問題を修正します[＃381](https://github.com/pingcap/tidb-lightning/pull/381)
        -   TiDBLightningが終了する前に一部のチェックポイント更新がデータベースに書き込まれない可能性がある問題を修正します[＃386](https://github.com/pingcap/tidb-lightning/pull/386)
