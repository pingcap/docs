---
title: TiDB 4.0.6 Release Notes
---

# TiDB 4.0.6 リリースノート {#tidb-4-0-6-release-notes}

発売日：2020年9月15日

TiDB バージョン: 4.0.6

## 新機能 {#new-features}

-   TiFlash

    -   TiFlashブロードキャスト ジョインで外部ジョインをサポート

-   TiDB ダッシュボード

    -   クエリ エディターと実行 UI を追加 (実験的) [#713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
    -   店舗ロケーション トポロジの視覚化のサポート[#719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
    -   クラスター構成 UI を追加 (実験的) [#733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
    -   現在のセッションの共有をサポート[#741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
    -   SQL ステートメント リスト[#746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)で実行プランの数を表示するサポート

-   ツール

    -   TiCDC (v4.0.6 から一般提供)

        -   `maxwell`フォーマット[#869](https://github.com/pingcap/tiflow/pull/869)でのデータ出力をサポート

## 改良点 {#improvements}

-   TiDB

    -   エラーコードとメッセージを標準エラーに置き換えます[#19888](https://github.com/pingcap/tidb/pull/19888)
    -   パーティションテーブル[#19649](https://github.com/pingcap/tidb/pull/19649)の書き込みパフォーマンスを改善する
    -   より多くの RPC ランタイム情報を`Cop Runtime`統計に記録する[#19264](https://github.com/pingcap/tidb/pull/19264)
    -   `metrics_schema`と`performance_schema` [#19792](https://github.com/pingcap/tidb/pull/19792)でのテーブルの作成を禁止する
    -   ユニオン エグゼキュータ[#19886](https://github.com/pingcap/tidb/pull/19886)の同時実行性の調整をサポート
    -   ブロードキャスト ジョイン[#19664](https://github.com/pingcap/tidb/pull/19664)のアウト ジョインをサポート
    -   プロセス リスト[#19829](https://github.com/pingcap/tidb/pull/19829)の SQL ダイジェストを追加します。
    -   autocommit ステートメントの再試行[#19796](https://github.com/pingcap/tidb/pull/19796)の悲観的トランザクション モードに切り替えます
    -   `Str_to_date()` [#19693](https://github.com/pingcap/tidb/pull/19693)で`%r`と`%T`データ形式をサポート
    -   ファイル特権を要求するために`SELECT INTO OUTFILE`有効にします[#19577](https://github.com/pingcap/tidb/pull/19577)
    -   `stddev_pop`機能[#19541](https://github.com/pingcap/tidb/pull/19541)をサポート
    -   `TiDB-Runtime`ダッシュボードを追加する[#19396](https://github.com/pingcap/tidb/pull/19396)
    -   `ALTER TABLE`アルゴリズムの互換性を向上[#19364](https://github.com/pingcap/tidb/pull/19364)
    -   スローログ`plan`フィールド[#19269](https://github.com/pingcap/tidb/pull/19269)に`insert` / `delete` / `update`プランをエンコード

-   TiKV

    -   `DropTable`または`TruncateTable`実行時のQPS低下を軽減[#8627](https://github.com/tikv/tikv/pull/8627)
    -   エラーコードのメタファイル生成をサポート[#8619](https://github.com/tikv/tikv/pull/8619)
    -   cf スキャンの詳細のパフォーマンス統計を追加します[#8618](https://github.com/tikv/tikv/pull/8618)
    -   Grafana のデフォルト テンプレート[#8467](https://github.com/tikv/tikv/pull/8467)に`rocksdb perf context`パネルを追加します。

-   PD

    -   TiDB ダッシュボードを v2020.09.08.1 に更新[#2928](https://github.com/pingcap/pd/pull/2928)
    -   リージョンのメトリクスを追加し、ハートビートを保存する[#2891](https://github.com/tikv/pd/pull/2891)
    -   低スペースしきい値を制御する元の方法に戻す[#2875](https://github.com/pingcap/pd/pull/2875)
    -   標準エラーコードをサポート
        -   [#2918](https://github.com/tikv/pd/pull/2918) [#2911](https://github.com/tikv/pd/pull/2911) [#2913](https://github.com/tikv/pd/pull/2913) [#2915](https://github.com/tikv/pd/pull/2915) [#2912](https://github.com/tikv/pd/pull/2912)
        -   [#2907](https://github.com/tikv/pd/pull/2907) [#2906](https://github.com/tikv/pd/pull/2906) [#2903](https://github.com/tikv/pd/pull/2903) [#2806](https://github.com/tikv/pd/pull/2806) [#2900](https://github.com/tikv/pd/pull/2900) [#2902](https://github.com/tikv/pd/pull/2902)

-   TiFlash

    -   データ レプリケーション用の Grafana パネルを追加します ( `apply Region snapshots`および`ingest SST files` )。
    -   `write stall`の Grafana パネルを追加
    -   `dt_segment_force_merge_delta_rows`と`dt_segment_force_merge_delta_deletes`を足して`write stall`のしきい値を調整します
    -   TiFlashで`raftstore.snap-handle-pool-size` ～ `0`の設定をサポート - マルチスレッドによるリージョンスナップショットの適用を無効にして、データ レプリケーション中のメモリ消費を削減するプロキシ
    -   `https_port`と`metrics_port`で CN チェックをサポート

-   ツール

    -   TiCDC

        -   プラーの初期化中に解決されたロックをスキップする[#910](https://github.com/pingcap/tiflow/pull/910)
        -   PD 書き込み頻度を下げる[#937](https://github.com/pingcap/tiflow/pull/937)

    -   バックアップと復元 (BR)

        -   要約ログ[#486](https://github.com/pingcap/br/issues/486)にリアルタイム コストを追加

    -   Dumpling

        -   列名[#135](https://github.com/pingcap/dumpling/pull/135)の出力`INSERT`をサポート
        -   `--filesize`と`--statement-size`の定義をmydumper [#142](https://github.com/pingcap/dumpling/pull/142)の定義に統一

    -   TiDB Lightning

        -   リージョンをより正確なサイズに分割して取り込む[#369](https://github.com/pingcap/tidb-lightning/pull/369)

    -   TiDBBinlog

        -   `go time`パッケージ形式で GC 時間の設定をサポート[#996](https://github.com/pingcap/tidb-binlog/pull/996)

## バグの修正 {#bug-fixes}

-   TiDB

    -   メトリック プロファイル[#19881](https://github.com/pingcap/tidb/pull/19881)で`tikv_cop_wait`回を収集する問題を修正します。
    -   `SHOW GRANTS` [#19834](https://github.com/pingcap/tidb/pull/19834)の間違った結果を修正
    -   `!= ALL (subq)` [#19831](https://github.com/pingcap/tidb/pull/19831)の誤ったクエリ結果を修正
    -   `enum`と`set`型の変換のバグを修正[#19778](https://github.com/pingcap/tidb/pull/19778)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET` [#19760](https://github.com/pingcap/tidb/pull/19760)の権限チェックを追加
    -   `builtinGreatestStringSig`と`builtinLeastStringSig` [#19758](https://github.com/pingcap/tidb/pull/19758)が原因で列の長さが一致しないというエラーを修正
    -   不要なエラーまたは警告が発生した場合、ベクトル化された制御式はスカラー実行にフォールバックします[#19749](https://github.com/pingcap/tidb/pull/19749)
    -   相関列のタイプが`Bit` [#19692](https://github.com/pingcap/tidb/pull/19692)の場合の`Apply`演算子のエラーを修正します。
    -   ユーザーが MySQL 8.0 クライアント[#19690](https://github.com/pingcap/tidb/pull/19690)で`processlist`と`cluster_log`クエリしたときに発生する問題を修正します。
    -   同じタイプのプランが異なるプラン ダイジェストを持つ問題を修正します[#19684](https://github.com/pingcap/tidb/pull/19684)
    -   列タイプを`Decimal`から`Int` [#19682](https://github.com/pingcap/tidb/pull/19682)に変更することを禁止します
    -   `SELECT ... INTO OUTFILE`実行時エラー[#19672](https://github.com/pingcap/tidb/pull/19672)を返す問題を修正
    -   `builtinRealIsFalseSig` [#19670](https://github.com/pingcap/tidb/pull/19670)の間違った実装を修正
    -   パーティション式チェックでかっこ式[#19614](https://github.com/pingcap/tidb/pull/19614)が欠落する問題を修正
    -   `HashJoin` [#19611](https://github.com/pingcap/tidb/pull/19611)に`Apply`演算子がある場合のクエリ エラーを修正
    -   `Real`を`Time` [#19594](https://github.com/pingcap/tidb/pull/19594)としてキャストするベクトル化の誤った結果を修正
    -   `SHOW GRANTS`ステートメントが存在しないユーザーの付与を示すバグを修正します[#19588](https://github.com/pingcap/tidb/pull/19588)
    -   `IndexLookupJoin` [#19566](https://github.com/pingcap/tidb/pull/19566)に`Apply` executor がある場合のクエリ エラーを修正
    -   パーティションテーブルで`Apply`を`HashJoin`に変換するときの間違った結果を修正する[#19546](https://github.com/pingcap/tidb/pull/19546)
    -   `Apply` [#19508](https://github.com/pingcap/tidb/pull/19508)の内側に`IndexLookUp` executor がある場合の誤った結果を修正
    -   ビュー[#19491](https://github.com/pingcap/tidb/pull/19491)使用時の予期しないpanicを修正
    -   `anti-semi-join`クエリ[#19477](https://github.com/pingcap/tidb/pull/19477)の誤った結果を修正
    -   統計が削除されたときに`TopN`統計が削除されないバグを修正します[#19465](https://github.com/pingcap/tidb/pull/19465)
    -   batch point get [#19460](https://github.com/pingcap/tidb/pull/19460)の誤った使用による間違った結果を修正
    -   仮想生成カラムで`indexLookupJoin`にカラムが見つからない不具合を修正[#19439](https://github.com/pingcap/tidb/pull/19439)
    -   `select`と`update`クエリの異なるプランがデータ[#19403](https://github.com/pingcap/tidb/pull/19403)を比較するエラーを修正
    -   リージョンキャッシュ[#19362](https://github.com/pingcap/tidb/pull/19362)のTiFlashワーク インデックスのデータ競合を修正
    -   `logarithm`関数で警告が表示されない不具合を修正[#19291](https://github.com/pingcap/tidb/pull/19291)
    -   TiDB がデータをディスクに永続化するときに発生する予期しないエラーを修正します[#19272](https://github.com/pingcap/tidb/pull/19272)
    -   インデックス結合[#19197](https://github.com/pingcap/tidb/pull/19197)の内側で単一のパーティションテーブルを使用するサポート
    -   10 進数[#19188](https://github.com/pingcap/tidb/pull/19188)に対して生成された間違ったハッシュ キー値を修正します。
    -   テーブル endKey とリージョン endKey が同じ[#19895](https://github.com/pingcap/tidb/pull/19895)の場合、TiDB が`no regions`エラーを返す問題を修正
    -   パーティション[#19891](https://github.com/pingcap/tidb/pull/19891)の変更が予期せず成功する問題を修正
    -   プッシュ ダウン式[#19876](https://github.com/pingcap/tidb/pull/19876)に許可されるデフォルトの最大パケット長の誤った値を修正します。
    -   `ENUM` / `SET`列の`Max` / `Min`関数の間違った動作を修正[#19869](https://github.com/pingcap/tidb/pull/19869)
    -   一部のTiFlashノードがオフラインの場合の`tiflash_segments`および`tiflash_tables`システム テーブルからの読み取りエラーを修正します[#19748](https://github.com/pingcap/tidb/pull/19748)
    -   `Count(col)`集計関数の間違った結果を修正[#19628](https://github.com/pingcap/tidb/pull/19628)
    -   `TRUNCATE`操作[#19445](https://github.com/pingcap/tidb/pull/19445)の実行時エラーを修正
    -   `Var`に大文字が含まれていると`PREPARE statement FROM @Var`が失敗する問題を修正[#19378](https://github.com/pingcap/tidb/pull/19378)
    -   大文字のスキーマでスキーマの文字セットを変更するとpanic[#19302](https://github.com/pingcap/tidb/pull/19302)が発生するバグを修正します
    -   情報に`tikv/tiflash` [#19159](https://github.com/pingcap/tidb/pull/19159)が含まれている場合、 `information_schema.statements_summary`と`explain`の間の計画の矛盾を修正します
    -   `select into outfile` [#19725](https://github.com/pingcap/tidb/pull/19725)のファイルが存在しないというテストのエラーを修正
    -   `INFORMATION_SCHEMA.CLUSTER_HARDWARE`にraidデバイス情報がない問題を修正[#19457](https://github.com/pingcap/tidb/pull/19457)
    -   構文解析エラー[#19395](https://github.com/pingcap/tidb/pull/19395)が発生した場合、 `case-when`で生成された列を持つ`add index`操作を正常に終了できるようにします。
    -   DDL操作の再試行に時間がかかりすぎるバグを修正[#19488](https://github.com/pingcap/tidb/pull/19488)
    -   `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)`のようなステートメントを最初に実行せずに実行する`use db` [#19471](https://github.com/pingcap/tidb/pull/19471)
    -   サーバー・ログ・ファイルのディスパッチ・エラーを`Error`から`Info`メッセージに変更します[#19454](https://github.com/pingcap/tidb/pull/19454)

-   TiKV

    -   照合順序が有効になっている場合の非インデックス列の推定エラーを修正します[#8620](https://github.com/tikv/tikv/pull/8620)
    -   リージョン転送[#8460](https://github.com/tikv/tikv/pull/8460)のプロセス中に Green GC がロックを見逃す可能性がある問題を修正します。
    -   Raftメンバーシップの変更中に TiKV の実行が非常に遅くなると発生するpanicの問題を修正します[#8497](https://github.com/tikv/tikv/pull/8497)
    -   PD 同期要求を呼び出すときに PD クライアント スレッドと他のスレッド間で発生するデッドロックの問題を修正します[#8612](https://github.com/tikv/tikv/pull/8612)
    -   jemalloc を v5.2.1 にアップグレードして、ヒュージ ページ[#8463](https://github.com/tikv/tikv/pull/8463)でのメモリ割り当ての問題に対処します。
    -   実行時間の長いクエリで統合スレッド プールがハングする問題を修正します[#8427](https://github.com/tikv/tikv/pull/8427)

-   PD

    -   `initial-cluster-token`構成を追加して、ブートストラップ中に異なるクラスターが相互に通信するのを防ぎます[#2922](https://github.com/pingcap/pd/pull/2922)
    -   モードが`auto` [#2826](https://github.com/pingcap/pd/pull/2826)のときのストアリミットレートの単位を修正
    -   一部のスケジューラーがエラーを解決せずに構成を保持する問題を修正します[#2818](https://github.com/tikv/pd/pull/2818)
    -   スケジューラーの空の HTTP 応答を修正します[#2871](https://github.com/tikv/pd/pull/2871) [#2874](https://github.com/tikv/pd/pull/2874)

-   TiFlash

    -   v4.0.4/v4.0.5にアップグレード後、以前のバージョンで主キー列の名前を変更した後、 TiFlashが起動しない場合がある問題を修正
    -   列の`nullable`属性を変更した後に発生する例外を修正します
    -   テーブルのレプリケーション ステータスの計算によって発生するクラッシュを修正します
    -   ユーザーがサポートされていない DDL 操作を適用した後、データの読み取りにTiFlashを使用できないという問題を修正します。
    -   `utf8mb4_bin`として扱われるサポートされていない照合によって発生する例外を修正します。
    -   Grafana でTiFlashコプロセッサ エグゼキュータの QPS パネルに常に`0`表示される問題を修正
    -   入力が`NULL`場合の`FROM_UNIXTIME`関数の間違った結果を修正

-   ツール

    -   TiCDC

        -   場合によっては TiCDC でメモリリークが発生する問題を修正[#942](https://github.com/pingcap/tiflow/pull/942)
        -   Kafka シンク[#912](https://github.com/pingcap/tiflow/pull/912)で TiCDC がpanicになる可能性がある問題を修正します。
        -   puller [#927](https://github.com/pingcap/tiflow/pull/927)で CommitTs または ResolvedTs (CRT) が`resolvedTs`未満になる可能性がある問題を修正します。
        -   `changefeed`が MySQL ドライバー[#936](https://github.com/pingcap/tiflow/pull/936)によってブロックされる可能性がある問題を修正します。
        -   TiCDC [#8573](https://github.com/tikv/tikv/pull/8573)の誤った Resolved Ts 間隔を修正

    -   バックアップと復元 (BR)

        -   チェックサム[#479](https://github.com/pingcap/br/pull/479)中に発生する可能性のあるpanicを修正します。
        -   PDLeader[#496](https://github.com/pingcap/br/pull/496)の変更後に発生することがあるpanicを修正します。

    -   Dumpling

        -   `NULL`バイナリ型の値が正しく処理されない問題を修正[#137](https://github.com/pingcap/dumpling/pull/137)

    -   TiDB Lightning

        -   書き込みと取り込みのすべての失敗した操作が誤って成功として表示される問題を修正します[#381](https://github.com/pingcap/tidb-lightning/pull/381)
        -   TiDB Lightningが終了する前に、一部のチェックポイントの更新がデータベースに書き込まれない可能性がある問題を修正します[#386](https://github.com/pingcap/tidb-lightning/pull/386)
