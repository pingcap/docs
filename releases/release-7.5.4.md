---
title: TiDB 7.5.4 Release Notes
summary: TiDB 7.5.4 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.4 リリースノート {#tidb-7-5-4-release-notes}

発売日：2024年10月15日

TiDB バージョン: 7.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.5/docs/tidb_http_api.md)から取得される DDL 履歴タスクのデフォルトの制限を 2048 に設定して、過剰な履歴タスク[＃55711](https://github.com/pingcap/tidb/issues/55711) @ [ジョッカウ](https://github.com/joccau)による OOM の問題を防止します。

## 改善点 {#improvements}

-   TiDB

    -   `EXPLAIN`ステートメントの出力に`tidb_redact_log`設定を適用し、ログ[＃54565](https://github.com/pingcap/tidb/issues/54565) @ [ホーキングレイ](https://github.com/hawkingrei)の処理ロジックをさらに最適化することをサポート
    -   TiDB の遅いクエリ[＃54630](https://github.com/pingcap/tidb/pull/54630) @ [イービン87](https://github.com/yibin87)のクエリ速度を最適化します

-   TiKV

    -   RocksDB 圧縮のトリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。
    -   ピアメッセージチャネル[＃16229](https://github.com/tikv/tikv/issues/16229)のメモリ使用量を[コナー1996](https://github.com/Connor1996)に減らす
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)の安定性を向上しました。
    -   TiKVの`DiskFull`検出を最適化してRaftEngineの`spill-dir`構成と互換性を持たせ、この機能が[＃17356](https://github.com/tikv/tikv/issues/17356) @ [LykxSassinator](https://github.com/LykxSassinator)で一貫して動作することを保証します。

-   TiFlash

    -   `LENGTH()`と`ASCII()`関数[＃9344](https://github.com/pingcap/tiflash/issues/9344)の実行効率を[xzhangxian1008](https://github.com/xzhangxian1008)で最適化
    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [ウィンドトーカー](https://github.com/windtalker)
    -   JOIN演算子のキャンセルメカニズムを改善し、JOIN演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [ウィンドトーカー](https://github.com/windtalker)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKVが各SSTファイルをダウンロードする前に、TiKVのディスク容量が十分かどうかのチェックをサポートします。容量が不足している場合、 BRは復元を終了し、エラー[＃17224](https://github.com/tikv/tikv/issues/17224) @ [リドリスR](https://github.com/RidRisR)を返します。

    -   TiCDC

        -   下流が`SUPER`権限が付与されたTiDBである場合、TiCDCは下流データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします。これにより、DDL文の実行を再試行する際のタイムアウトによるデータ複製の失敗を回避できます[＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)場合）。

## バグ修正 {#bug-fixes}

-   TiDB

    -   データベースに多くのテーブルが存在する場合に`FLASHBACK DATABASE`失敗する問題を修正[＃54415](https://github.com/pingcap/tidb/issues/54415) @ [ランス6716](https://github.com/lance6716)
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   `UNION`を含むクエリステートメントが誤った結果[＃52985](https://github.com/pingcap/tidb/issues/52985) @ [徐淮嶼](https://github.com/XuHuaiyu)を返す可能性がある問題を修正しました
    -   SQLが異常中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに、繰り返しの開閉操作[＃53600](https://github.com/pingcap/tidb/issues/53600) @ [徐淮嶼](https://github.com/XuHuaiyu)によって発生した以前のパラメータ値の再利用により発生する予期しないエラーを修正します。
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   `Sort`演算子がスピルした後にディスクファイルが削除されず、クエリエラーが発生する可能性がある問題を修正[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [wshwsh12](https://github.com/wshwsh12)
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3ハンター](https://github.com/D3Hunter)
    -   DMから複製されたテーブルのインデックスの長さが`max-index-length` [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [ランス6716](https://github.com/lance6716)で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました
    -   `INFORMATION_SCHEMA.STATISTICS`表の`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)である問題を修正しました
    -   DML文にネストされた生成列[＃53967](https://github.com/pingcap/tidb/issues/53967) @ [wjhuang2016](https://github.com/wjhuang2016)が含まれている場合にエラーが発生する問題を修正しました
    -   `mysql.stats_histograms`表の`tot_col_size`列目が負の数[＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロツグ](https://github.com/solotzg)のデータ競合問題を修正
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [イービン87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL 文[＃53713](https://github.com/pingcap/tidb/issues/53713) @ [アイリンキッド](https://github.com/AilinKid)を実行すると`runtime error: index out of range`が発生する問題を修正しました。
    -   `SELECT ... WHERE ... ORDER BY ...`文の実行パフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [天菜まお](https://github.com/tiancaiamao)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB が[＃53867](https://github.com/pingcap/tidb/issues/53867) @ [xzhangxian1008](https://github.com/xzhangxian1008)でpanicを起こす可能性がある問題を修正しました
    -   copタスク構築中にTiDBクエリをキャンセルできない問題を修正[＃55957](https://github.com/pingcap/tidb/issues/55957) @ [イービン87](https://github.com/yibin87)
    -   整数型[＃55837](https://github.com/pingcap/tidb/issues/55837) @ [ウィンドトーカー](https://github.com/windtalker)の列に小さい表示幅が指定された場合、 `out of range`エラーが発生する可能性がある問題を修正しました。
    -   ユニークインデックス[＃56161](https://github.com/pingcap/tidb/issues/56161) @ [接線](https://github.com/tangenta)を追加するときに`duplicate entry`発生する可能性がある問題を修正
    -   `IMPORT INTO`文[＃55970](https://github.com/pingcap/tidb/issues/55970) @ [D3ハンター](https://github.com/D3Hunter)を使用して一時テーブルをインポートするときに TiDB がパニックになる問題を修正しました
    -   インデックス追加[＃55808](https://github.com/pingcap/tidb/issues/55808) @ [ランス6716](https://github.com/lance6716)中の再試行によって発生するデータ インデックスの不整合の問題を修正しました

-   TiKV

    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ヒビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。
    -   大きなテーブルやパーティション[＃17304](https://github.com/tikv/tikv/issues/17304) @ [コナー1996](https://github.com/Connor1996)を削除した後に発生する可能性のあるフロー制御の問題を修正しました
    -   ブルームフィルタが以前のバージョン（v7.1より前）とそれ以降のバージョン[＃17272](https://github.com/tikv/tikv/issues/17272) @ [v01dstar](https://github.com/v01dstar)の間で互換性がない問題を修正しました
    -   マスターキーがキー管理サービス (KMS) [＃17410](https://github.com/tikv/tikv/issues/17410) @ [hhwyt](https://github.com/hhwyt)に保存されているときにマスターキーのローテーションが妨げられる問題を修正しました
    -   Grafana の TiKV パネルの**ストレージ非同期書き込み期間の**監視メトリックが不正確であるという問題を修正しました[＃17579](https://github.com/tikv/tikv/issues/17579) @ [金星の上](https://github.com/overvenus)
    -   同じキーのロック解除のために多数のトランザクションがキューイングされ、キーが頻繁に更新される場合、デッドロック検出への過度の圧力によって TiKV OOM 問題[＃17394](https://github.com/tikv/tikv/issues/17394) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。

-   PD

    -   多数のリージョンが存在する場合にPDのリージョンAPIをリクエストできない問題を修正[＃55872](https://github.com/pingcap/tidb/issues/55872) @ [rleungx](https://github.com/rleungx)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが利用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   マイクロサービスモード[＃8538](https://github.com/tikv/pd/issues/8538) @ [lhy1024](https://github.com/lhy1024)でPDリーダーが切り替えられたときにスケジューリングサーバーでデータ競合が発生する可能性がある問題を修正しました
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値[＃7346](https://github.com/tikv/pd/issues/7346) @ [グオシャオゲ](https://github.com/guo-shaoge)より少なくなる問題を修正しました。
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブルの時間データ型が正しくない問題を修正[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [HuSharp](https://github.com/HuSharp)
    -   `replication.strictly-match-label`を`true`に設定するとTiFlashが[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャ[＃9282](https://github.com/pingcap/tiflash/issues/9282) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でTiFlash書き込みノードが再起動に失敗する可能性がある問題を修正しました
    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラー[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)が発生する可能性がある問題を修正しました。
    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロツグ](https://github.com/solotzg)
    -   分散storageおよびコンピューティングアーキテクチャ[＃9298](https://github.com/pingcap/tiflash/issues/9298) @ [ジンヘリン](https://github.com/JinheLin)で、 TiFlash書き込みノードの読み取りスナップショットがタイムリーにリリースされない問題を修正しました。
    -   テーブルに無効な文字[＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を含むデフォルト値を持つビット型の列が含まれている場合、 TiFlash がテーブル スキーマを解析できない問題を修正しました。
    -   遅延マテリアライゼーションが有効になっている場合に一部のクエリでエラーが報告される可能性がある問題を修正[＃9472](https://github.com/pingcap/tiflash/issues/9472) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   データ型を`DECIMAL`型に変換すると、極端なケースで間違ったクエリ結果が返される可能性がある問題を修正しました[＃53892](https://github.com/pingcap/tidb/issues/53892) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [リーヴルス](https://github.com/Leavrth)
        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップ PITR タスクが失敗して停止した後、そのタスクに関連するセーフポイントが PD [＃17316](https://github.com/tikv/tikv/issues/17316) @ [リーヴルス](https://github.com/Leavrth)で適切にクリアされない問題を修正しました。
        -   ログバックアップが有効になっているときにBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [リドリスR](https://github.com/RidRisR)
        -   BR統合テストケースが不安定になる問題を修正し、スナップショットまたはログバックアップファイルの破損をシミュレートする新しいテストケースを追加します[＃53835](https://github.com/pingcap/tidb/issues/53835) @ [リーヴルス](https://github.com/Leavrth)

    -   TiCDC

        -   変更フィードチェックポイントの**Barrier-ts**監視メトリックが不正確になる可能性がある問題を修正しました[＃11553](https://github.com/pingcap/tiflow/issues/11553) @ [3エースショーハンド](https://github.com/3AceShowHand)

    -   TiDB データ移行 (DM)

        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正しました
        -   DMが`ALTER DATABASE`文を処理するときにデフォルトのデータベースを設定せず、レプリケーションエラー[＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。
        -   複数の DM マスターノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   TiDB Lightning [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [ランス6716](https://github.com/lance6716)を使用してデータのインポート中にトランザクションの競合が発生する問題を修正しました
