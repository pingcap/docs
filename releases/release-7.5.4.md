---
title: TiDB 7.5.4 Release Notes
summary: TiDB 7.5.4 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.4 リリースノート {#tidb-7-5-4-release-notes}

発売日：2024年10月15日

TiDB バージョン: 7.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.5/docs/tidb_http_api.md)から取得される DDL 履歴タスクのデフォルトの制限を 2048 に設定して、過剰な履歴タスクによる OOM の問題を防止します。 [＃55711](https://github.com/pingcap/tidb/issues/55711) @ [joccau](https://github.com/joccau)

## 改善点 {#improvements}

-   TiDB

    -   `EXPLAIN`ステートメントの出力に`tidb_redact_log`設定を適用し、ログの処理ロジックをさらに最適化することをサポート [＃54565](https://github.com/pingcap/tidb/issues/54565) @ [hawkingrei](https://github.com/hawkingrei)
    -   TiDB のスロークエリのクエリ速度を最適化します [＃54630](https://github.com/pingcap/tidb/pull/54630) @ [yibin87](https://github.com/yibin87)

-   TiKV

    -   RocksDB 圧縮のトリガー メカニズムを最適化し、多数の DELETE バージョンを処理するときにディスク領域の再利用を高速化します。 [＃17269](https://github.com/tikv/tikv/issues/17269) @ [AndreMouche](https://github.com/AndreMouche)
    -   ピアメッセージチャネルのメモリ使用量を@ [Connor1996](https://github.com/Connor1996)に減らす [＃16229](https://github.com/tikv/tikv/issues/16229)
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV の安定性を向上しました。 [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   TiKVの`DiskFull`検出を最適化してRaftEngineの`spill-dir`構成と互換性を持たせ、この機能が一貫して動作することを保証します。 [＃17356](https://github.com/tikv/tikv/issues/17356) @ [LykxSassinator](https://github.com/LykxSassinator)

-   TiFlash

    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化 [＃9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   TLS を有効にした後に証明書を更新することでTiFlash がpanicする可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [windtalker](https://github.com/windtalker)
    -   JOIN演算子のキャンセルメカニズムを改善し、JOIN演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [windtalker](https://github.com/windtalker)

-   ツール

    -   Backup & Restore (BR)

        -   TiKVが各SSTファイルをダウンロードする前に、TiKVのディスク容量が十分かどうかのチェックをサポートします。容量が不足している場合、 BRは復元を終了し、エラーを返します。 [＃17224](https://github.com/tikv/tikv/issues/17224) @ [RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   下流が`SUPER`権限が付与されたTiDBである場合、TiCDCは下流データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします。これにより、DDL文の実行を再試行する際のタイムアウトによるデータ複製の失敗を回避できます場合）。 [＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   データベースに多くのテーブルが存在する場合に`FLASHBACK DATABASE`失敗する問題を修正[＃54415](https://github.com/pingcap/tidb/issues/54415) @ [lance6716](https://github.com/lance6716)
    -   厳密に自己増分ではないRANGEパーティションテーブルが作成できる問題を修正 [＃54829](https://github.com/pingcap/tidb/issues/54829) @ [Defined2014](https://github.com/Defined2014)
    -   `UNION`を含むクエリステートメントが誤った結果を返す可能性がある問題を修正しました [＃52985](https://github.com/pingcap/tidb/issues/52985) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   SQLが異常中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに、繰り返しの開閉操作によって発生した以前のパラメータ値の再利用により発生する予期しないエラーを修正します。 [＃53600](https://github.com/pingcap/tidb/issues/53600) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   情報スキーマキャッシュミスにより、古い読み取りのクエリレイテンシーが増加する問題を修正しました。 [＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)
    -   `Sort`演算子がスピルした後にディスクファイルが削除されず、クエリエラーが発生する可能性がある問題を修正[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [wshwsh12](https://github.com/wshwsh12)
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3Hunter](https://github.com/D3Hunter)
    -   DMから複製されたテーブルのインデックスの長さが`max-index-length` で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [lance6716](https://github.com/lance6716)
    -   `INFORMATION_SCHEMA.STATISTICS`表の`SUB_PART`値が`NULL` である問題を修正しました [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [Defined2014](https://github.com/Defined2014)
    -   DML文にネストされた生成列が含まれている場合にエラーが発生する問題を修正しました [＃53967](https://github.com/pingcap/tidb/issues/53967) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `mysql.stats_histograms`表の`tot_col_size`列が負の数になる可能性がある問題を修正しました [＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)
    -   `IndexNestedLoopHashJoin` のデータ競合問題を修正 [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [solotzg](https://github.com/solotzg)
    -   メモリ使用量が`tidb_mem_quota_query` で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [yibin87](https://github.com/yibin87)
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL 文を実行すると`runtime error: index out of range`が発生する問題を修正しました。 [＃53713](https://github.com/pingcap/tidb/issues/53713) @ [AilinKid](https://github.com/AilinKid)
    -   `SELECT ... WHERE ... ORDER BY ...`文の実行パフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました [＃53867](https://github.com/pingcap/tidb/issues/53867) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   copタスク構築中にTiDBクエリをキャンセルできない問題を修正[＃55957](https://github.com/pingcap/tidb/issues/55957) @ [yibin87](https://github.com/yibin87)
    -   整数型の列に小さい表示幅が指定された場合、 `out of range`エラーが発生する可能性がある問題を修正しました。 [＃55837](https://github.com/pingcap/tidb/issues/55837) @ [windtalker](https://github.com/windtalker)
    -   一意インデックスを追加するときに`duplicate entry`発生する可能性がある問題を修正 [＃56161](https://github.com/pingcap/tidb/issues/56161) @ [tangenta](https://github.com/tangenta)
    -   `IMPORT INTO`文を使用して一時テーブルをインポートするときに TiDB がパニックになる問題を修正しました [＃55970](https://github.com/pingcap/tidb/issues/55970) @ [D3Hunter](https://github.com/D3Hunter)
    -   インデックス追加中の再試行によって発生するデータ インデックスの不整合の問題を修正しました [＃55808](https://github.com/pingcap/tidb/issues/55808) @ [lance6716](https://github.com/lance6716)

-   TiKV

    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカの即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。 [＃17469](https://github.com/tikv/tikv/issues/17469) @ [hbisheng](https://github.com/hbisheng)
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるフロー制御の問題を修正しました [＃17304](https://github.com/tikv/tikv/issues/17304) @ [Connor1996](https://github.com/Connor1996)
    -   ブルームフィルタが以前のバージョン（v7.1より前）とそれ以降のバージョンの間で互換性がない問題を修正しました [＃17272](https://github.com/tikv/tikv/issues/17272) @ [v01dstar](https://github.com/v01dstar)
    -   マスターキーがキー管理サービス (KMS) に保存されているときにマスターキーのローテーションが妨げられる問題を修正しました [＃17410](https://github.com/tikv/tikv/issues/17410) @ [hhwyt](https://github.com/hhwyt)
    -   Grafana の TiKV パネルの**ストレージ非同期書き込み期間の**監視メトリックが不正確であるという問題を修正しました[＃17579](https://github.com/tikv/tikv/issues/17579) @ [overvenus](https://github.com/overvenus)
    -   同じキーのロック解除のために多数のトランザクションがキューイングされ、キーが頻繁に更新される場合、デッドロック検出への過度の圧力によって TiKV OOM 問題が発生する可能性がある問題を修正しました。 [＃17394](https://github.com/tikv/tikv/issues/17394) @ [MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   多数のリージョンが存在する場合にPDのリージョンAPIをリクエストできない問題を修正[＃55872](https://github.com/pingcap/tidb/issues/55872) @ [rleungx](https://github.com/rleungx)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが利用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   マイクロサービスモードでPDリーダーが切り替えられたときにスケジューリングサーバーでデータ競合が発生する可能性がある問題を修正しました [＃8538](https://github.com/tikv/pd/issues/8538) @ [lhy1024](https://github.com/lhy1024)
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値より少なくなる問題を修正しました。 [＃7346](https://github.com/tikv/pd/issues/7346) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブルの時間データ型が正しくない問題を修正[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [HuSharp](https://github.com/HuSharp)
    -   `replication.strictly-match-label`を`true`に設定するとTiFlashが起動しなくなる問題を修正 [＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   分散ストレージおよびコンピューティングアーキテクチャでTiFlash書き込みノードが再起動に失敗する可能性がある問題を修正しました [＃9282](https://github.com/pingcap/tiflash/issues/9282) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラーが発生する可能性がある問題を修正しました。 [＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [solotzg](https://github.com/solotzg)
    -   分散ストレージおよびコンピューティングアーキテクチャで、 TiFlash書き込みノードの読み取りスナップショットがタイムリーにリリースされない問題を修正しました。 [＃9298](https://github.com/pingcap/tiflash/issues/9298) @ [JinheLin](https://github.com/JinheLin)
    -   テーブルに無効な文字を含むデフォルト値を持つビット型の列が含まれている場合、 TiFlash がテーブル スキーマを解析できない問題を修正しました。 [＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   遅延マテリアライゼーションが有効になっている場合に一部のクエリでエラーが報告される可能性がある問題を修正[＃9472](https://github.com/pingcap/tiflash/issues/9472) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   データ型を`DECIMAL`型に変換すると、極端なケースで間違ったクエリ結果が返される可能性がある問題を修正しました[＃53892](https://github.com/pingcap/tidb/issues/53892) @ [guo-shaoge](https://github.com/guo-shaoge)

-   ツール

    -   Backup & Restore (BR)

        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [Leavrth](https://github.com/Leavrth)
        -   バックアップと復元のチェックポイントパスが一部の外部ストレージと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップ PITR タスクが失敗して停止した後、そのタスクに関連するセーフポイントが PD で適切にクリアされない問題を修正しました。 [＃17316](https://github.com/tikv/tikv/issues/17316) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップが有効になっているときにBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [RidRisR](https://github.com/RidRisR)
        -   BR統合テストケースが不安定になる問題を修正し、スナップショットまたはログバックアップファイルの破損をシミュレートする新しいテストケースを追加します[＃53835](https://github.com/pingcap/tidb/issues/53835) @ [Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   変更フィードチェックポイントの**Barrier-ts**監視メトリックが不正確になる可能性がある問題を修正しました[＃11553](https://github.com/pingcap/tiflow/issues/11553) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Data Migration (DM)

        -   インデックスの長さがデフォルト値の`max-index-length` を超えるとデータレプリケーションが中断される問題を修正しました [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [michaelmdeng](https://github.com/michaelmdeng)
        -   DMが`ALTER DATABASE`文を処理するときにデフォルトのデータベースを設定せず、レプリケーションエラーが発生する問題を修正しました。 [＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [lance6716](https://github.com/lance6716)
        -   複数の DM マスターノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   TiDB Lightning を使用してデータのインポート中にトランザクションの競合が発生する問題を修正しました [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [lance6716](https://github.com/lance6716)
