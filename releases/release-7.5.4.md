---
title: TiDB 7.5.4 Release Notes
summary: TiDB 7.5.4 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.5.4 リリースノート {#tidb-7-5-4-release-notes}

発売日: 2024年10月15日

TiDB バージョン: 7.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.5/docs/tidb_http_api.md)から取得される DDL 履歴タスクのデフォルトの制限を 2048 に設定して、履歴タスク[＃55711](https://github.com/pingcap/tidb/issues/55711) @ [ジョッカウ](https://github.com/joccau)の過剰による OOM の問題を防止します。

## 改善点 {#improvements}

-   ティビ

    -   `EXPLAIN`ステートメントの出力に`tidb_redact_log`設定を適用し、ログ[＃54565](https://github.com/pingcap/tidb/issues/54565) @ [ホーキングレイ](https://github.com/hawkingrei)の処理ロジックをさらに最適化することをサポート
    -   TiDB の遅いクエリのクエリ速度を最適化する[＃54630](https://github.com/pingcap/tidb/pull/54630) @ [いびん87](https://github.com/yibin87)

-   ティクヴ

    -   RocksDB 圧縮のトリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。
    -   ピアメッセージチャネル[＃16229](https://github.com/tikv/tikv/issues/16229) @ [コナー1996](https://github.com/Connor1996)のメモリ使用量を削減
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV [＃15874](https://github.com/tikv/tikv/issues/15874) @ [リクササシネーター](https://github.com/LykxSassinator)の安定性を向上しました。
    -   TiKV の`DiskFull`検出を最適化して RaftEngine の`spill-dir`構成と互換性を持たせ、この機能が[＃17356](https://github.com/tikv/tikv/issues/17356) @ [リクササシネーター](https://github.com/LykxSassinator)で一貫して動作するようにしました。

-   TiFlash

    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化[＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [翻訳者](https://github.com/xzhangxian1008)
    -   TLS を有効にした後に証明書を更新することでTiFlash がpanicになる可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [風の話し手](https://github.com/windtalker)
    -   JOIN 演算子のキャンセル メカニズムを改善し、JOIN 演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [風の話し手](https://github.com/windtalker)

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV が各 SST ファイルをダウンロードする前に、TiKV のディスク容量が十分かどうかのチェックをサポートします。容量が不十分な場合、 BR は復元を終了し、エラー[＃17224](https://github.com/tikv/tikv/issues/17224) @ [リドリス](https://github.com/RidRisR)を返します。

    -   ティCDC

        -   ダウンストリームが`SUPER`権限が付与された TiDB の場合、TiCDC は、場合によっては DDL ステートメントの実行を再試行する際のタイムアウトによるデータ複製の失敗を回避するために、ダウンストリーム データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします[＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   ティビ

    -   データベースに多数のテーブルが存在する場合に`FLASHBACK DATABASE`失敗する問題を修正[＃54415](https://github.com/pingcap/tidb/issues/54415) @ [ランス6716](https://github.com/lance6716)
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   `UNION`を含むクエリ ステートメントが誤った結果[＃52985](https://github.com/pingcap/tidb/issues/52985) @ [徐懐玉](https://github.com/XuHuaiyu)を返す可能性がある問題を修正しました
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [うわー](https://github.com/wshwsh12)
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに、繰り返しの開閉操作[＃53600](https://github.com/pingcap/tidb/issues/53600) @ [徐懐玉](https://github.com/XuHuaiyu)によって以前のパラメータ値が再利用されたために発生する予期しないエラーを修正します。
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [クレイジーcs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   `Sort`演算子がスピルした後にディスク ファイルが削除されず、クエリ エラーが発生する可能性がある問題を修正しました[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [うわー](https://github.com/wshwsh12)
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3ハンター](https://github.com/D3Hunter)
    -   DMから複製されたテーブルのインデックス長が`max-index-length` [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [ランス6716](https://github.com/lance6716)で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました。
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)になる問題を修正しました
    -   DML文にネストされた生成列[＃53967](https://github.com/pingcap/tidb/issues/53967) @ [翻訳:](https://github.com/wjhuang2016)が含まれている場合にエラーが発生する問題を修正
    -   `mysql.stats_histograms`の表の`tot_col_size`列目が負の数[＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロッツ](https://github.com/solotzg)のデータ競合問題を修正
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [いびん87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL ステートメント[＃53713](https://github.com/pingcap/tidb/issues/53713) @ [アイリンキッド](https://github.com/AilinKid)を実行すると`runtime error: index out of range`発生する問題を修正しました。
    -   `SELECT ... WHERE ... ORDER BY ...`ステートメント実行のパフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [天菜まお](https://github.com/tiancaiamao)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました[＃53867](https://github.com/pingcap/tidb/issues/53867) @ [翻訳者](https://github.com/xzhangxian1008)
    -   copタスク構築中にTiDBクエリをキャンセルできない問題を修正[＃55957](https://github.com/pingcap/tidb/issues/55957) @ [いびん87](https://github.com/yibin87)
    -   整数型[＃55837](https://github.com/pingcap/tidb/issues/55837) @ [風の話し手](https://github.com/windtalker)の列に小さい表示幅が指定された場合、 `out of range`エラーが発生する可能性がある問題を修正しました。
    -   ユニークインデックス[＃56161](https://github.com/pingcap/tidb/issues/56161) @ [タンジェンタ](https://github.com/tangenta)を追加するときに`duplicate entry`発生する可能性がある問題を修正
    -   `IMPORT INTO`ステートメント[＃55970](https://github.com/pingcap/tidb/issues/55970) @ [D3ハンター](https://github.com/D3Hunter)を使用して一時テーブルをインポートするときに TiDB がパニックになる問題を修正しました。
    -   インデックス追加[＃55808](https://github.com/pingcap/tidb/issues/55808) @ [ランス6716](https://github.com/lance6716)中の再試行によって発生するデータ インデックスの不整合の問題を修正

-   ティクヴ

    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるフロー制御の問題を修正[＃17304](https://github.com/tikv/tikv/issues/17304) @ [コナー1996](https://github.com/Connor1996)
    -   ブルームフィルタが以前のバージョン（v7.1以前）とそれ以降のバージョン[＃17272](https://github.com/tikv/tikv/issues/17272) @ [v01dスター](https://github.com/v01dstar)の間で互換性がない問題を修正しました
    -   マスターキーがキー管理サービス (KMS) [＃17410](https://github.com/tikv/tikv/issues/17410) @ [いいえ](https://github.com/hhwyt)に保存されている場合にマスターキーのローテーションが妨げられる問題を修正しました
    -   Grafana の TiKV パネルの**ストレージ非同期書き込み期間**監視メトリックが不正確であるという問題を修正[＃17579](https://github.com/tikv/tikv/issues/17579) @ [金星の上](https://github.com/overvenus)
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出に過度の負荷がかかり、TiKV OOM 問題[＃17394](https://github.com/tikv/tikv/issues/17394) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。

-   PD

    -   多数のリージョンが存在する場合にPDのリージョンAPIをリクエストできない問題を修正[＃55872](https://github.com/pingcap/tidb/issues/55872) @ [rleungx](https://github.com/rleungx)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが使用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   マイクロサービスモード[＃8538](https://github.com/tikv/pd/issues/8538) @ [翻訳者](https://github.com/lhy1024)でPDリーダーが切り替えられたときにスケジューリングサーバーでデータ競合が発生する可能性がある問題を修正
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値[＃7346](https://github.com/tikv/pd/issues/7346) @ [グオシャオゲ](https://github.com/guo-shaoge)より少なくなる問題を修正しました。
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブルの時間データ型が正しくない問題を修正[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [ヒューシャープ](https://github.com/HuSharp)
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャ[＃9282](https://github.com/pingcap/tiflash/issues/9282) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でTiFlash書き込みノードが再起動に失敗する可能性がある問題を修正しました
    -   TiFlashと PD 間のネットワーク パーティション (ネットワーク切断) により読み取り要求タイムアウト エラーが発生する可能性がある問題を修正[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロッツ](https://github.com/solotzg)
    -   分散storageおよびコンピューティングアーキテクチャ[＃9298](https://github.com/pingcap/tiflash/issues/9298) @ [ジンヘリン](https://github.com/JinheLin)で、 TiFlash書き込みノードの読み取りスナップショットがタイムリーにリリースされない問題を修正しました。
    -   テーブルに無効な文字[＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を含むデフォルト値を持つビット型列が含まれている場合に、 TiFlash がテーブル スキーマを解析できない問題を修正しました。
    -   遅延マテリアライゼーションが有効になっている場合に一部のクエリでエラーが報告される問題を修正[＃9472](https://github.com/pingcap/tiflash/issues/9472) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   データ型を`DECIMAL`型に変換すると、極端なケースで間違ったクエリ結果が返される可能性がある問題を修正しました[＃53892](https://github.com/pingcap/tidb/issues/53892) @ [グオシャオゲ](https://github.com/guo-shaoge)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [リーヴルス](https://github.com/Leavrth)
        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)
        -   ログ バックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD [＃17316](https://github.com/tikv/tikv/issues/17316) @ [リーヴルス](https://github.com/Leavrth)で適切にクリアされない問題を修正しました。
        -   ログバックアップが有効になっている場合にBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [リドリス](https://github.com/RidRisR)
        -   BR統合テスト ケースが不安定になる問題を修正し、スナップショットまたはログ バックアップ ファイルの破損をシミュレートする新しいテスト ケースを追加します[＃53835](https://github.com/pingcap/tidb/issues/53835) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   変更フィード チェックポイントの**バリア ts**監視メトリックが不正確になる可能性がある問題を修正[＃11553](https://github.com/pingcap/tiflow/issues/11553) @ [3エースショーハンド](https://github.com/3AceShowHand)

    -   TiDB データ移行 (DM)

        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正
        -   DM が`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーション エラー[＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。
        -   複数の DM マスター ノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   TiDB Lightning [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [ランス6716](https://github.com/lance6716)使用してデータインポート中にトランザクションの競合が発生する問題を修正
