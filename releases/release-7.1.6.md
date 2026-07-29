---
title: TiDB 7.1.6 Release Notes
summary: TiDB 7.1.6 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.6 リリースノート {#tidb-7-1-6-release-notes}

発売日：2024年11月21日

TiDB バージョン: 7.1.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.1/docs/tidb_http_api.md)から取得される DDL 履歴タスクのデフォルトの制限を 2048 に設定して、過剰な履歴タスクによる OOM の問題を防止します。 [＃55711](https://github.com/pingcap/tidb/issues/55711) @ [joccau](https://github.com/joccau)
-   以前のバージョンでは、 `UPDATE`変更を含むトランザクションを処理する際に、 `UPDATE`目のイベントで主キーまたは非NULLの一意インデックス値が変更されると、TiCDCはこのイベントを`DELETE`目と`INSERT`目のイベントに分割していました。v7.1.6以降では、MySQLシンクを使用する場合、 `UPDATE`の変更のトランザクション`commitTS` TiCDC `thresholdTS` （TiCDCが対応するテーブルをダウンストリームに複製し始める際にPDから取得する現在のタイムスタンプ）より小さい場合、TiCDCは`UPDATE`件目のイベントを`DELETE`目と`INSERT`件目のイベントに分割します。この動作変更は、TiCDCが受信した`UPDATE`目のイベントの順序が誤っている可能性があり、その結果、分割された`DELETE`と`INSERT`目のイベントの順序が誤っている可能性があることで発生するダウンストリームデータの不整合の問題を解決します。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v7.1/ticdc-split-update-behavior#split-update-events-for-mysql-sinks) してください@ [lidezhu](https://github.com/lidezhu) [＃10918](https://github.com/pingcap/tiflow/issues/10918)
-   TiDB Lightning `strict-format`を使用して CSV ファイルをインポートする場合は、行末文字を設定する必要があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [lance6716](https://github.com/lance6716)
-   TiKV構成項目[`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)のスコープを変更します。

    -   v7.1.6 より前の v7.1.x バージョンでは、この構成項目は TiKV ノード間の gRPC メッセージの圧縮アルゴリズムにのみ影響します。
    -   v7.1.6以降、この設定項目はTiKVからTiDBに送信されるgRPC応答メッセージの圧縮アルゴリズムにも影響します。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります[＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)

## 改善点 {#improvements}

-   TiDB

    -   統計情報がすべて TopN で構成され、対応するテーブル統計の変更された行数が 0 以外である場合に、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [terry1purcell](https://github.com/terry1purcell)
    -   MPP ロード バランシング中にリージョンのないストアを削除する [＃52313](https://github.com/pingcap/tidb/issues/52313) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `SHOW CREATE TABLE` の出力に表示される式のデフォルト値のMySQL互換性を改善しました [＃52939](https://github.com/pingcap/tidb/issues/52939) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   TiFlash配置ルールを一括削除することで、パーティションテーブルで`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。 [＃54068](https://github.com/pingcap/tidb/issues/54068) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   同期ロードパフォーマンスを改善し、統計情報のロード時のレイテンシーを削減します[＃52294](https://github.com/pingcap/tidb/issues/52294) @ [hawkingrei](https://github.com/hawkingrei)

-   TiKV

    -   ピアのスローログを追加し、メッセージを保存します。 [＃16600](https://github.com/tikv/tikv/issues/16600) @ [Connor1996](https://github.com/Connor1996)
    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョンを処理するときにディスク領域の再利用を高速化します。 [＃17269](https://github.com/tikv/tikv/issues/17269) @ [AndreMouche](https://github.com/AndreMouche)
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV の安定性を向上しました。 [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   不要な非同期ブロックを削除してメモリ使用量を削減する[＃16540](https://github.com/tikv/tikv/issues/16540) @ [overvenus](https://github.com/overvenus)

-   TiFlash

    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化 [＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   TLS を有効にした後に証明書を更新することでTiFlash がpanicする可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [windtalker](https://github.com/windtalker)
    -   JOIN演算子のキャンセルメカニズムを改善し、JOIN演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [windtalker](https://github.com/windtalker)
    -   同時実行性の高いデータ読み取り操作におけるロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [JinheLin](https://github.com/JinheLin)
    -   クラスター化インデックスを持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。 [＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   ログバックアップのマージ操作に対する許容度を向上します。適度に長いマージ操作が発生した場合、ログバックアップタスクがエラー状態に陥る可能性が低くなります。 [＃16554](https://github.com/tikv/tikv/issues/16554) @ [YuJuncen](https://github.com/YuJuncen)
        -   BRはデータ復旧中に空のSSTファイルをクリーンアップします[＃16005](https://github.com/tikv/tikv/issues/16005) @ [Leavrth](https://github.com/Leavrth)
        -   DNSエラーによる失敗の再試行回数を[＃53029](https://github.com/pingcap/tidb/issues/53029) / @ [YuJuncen](https://github.com/YuJuncen)に増やす
        -   リージョンのリーダー不在による失敗の再試行回数を@ [Leavrth](https://github.com/Leavrth)に増やす [＃54017](https://github.com/pingcap/tidb/issues/54017)
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [Leavrth](https://github.com/Leavrth)
        -   TiKVが各SSTファイルをダウンロードする前に、TiKVのディスク容量が十分かどうかのチェックをサポートします。容量が不足している場合、 BRは復元を終了し、エラーを返します。 [＃17224](https://github.com/tikv/tikv/issues/17224) @ [RidRisR](https://github.com/RidRisR)
        -   環境変数を介した Alibaba Cloud アクセス資格情報の設定をサポート [＃45551](https://github.com/pingcap/tidb/issues/45551) @ [RidRisR](https://github.com/RidRisR)
        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドストレージの場合、生のイベントを直接出力することをサポート[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDOログを使用してデータリカバリ中のメモリの安定性を向上させ、OOM の確率を低減します。 [＃10900](https://github.com/pingcap/tiflow/issues/10900) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   下流が`SUPER`権限が付与されたTiDBの場合、TiCDCは下流データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします。これにより、DDL文の実行を再試行する際のタイムアウトによるデータ複製の失敗を回避できる場合があります。 [＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Data Migration (DM)

        -   19文字を超えるパスワードを使用してMySQLサーバー8.0に接続できるように、 `go-mysql`を1.9.1にアップグレードします[＃11603](https://github.com/pingcap/tiflow/pull/11603) @ [fishiu](https://github.com/fishiu)

## バグ修正 {#bug-fixes}

-   TiDB

    -   一意インデックスを追加するときに同時 DML 操作によって発生するデータ インデックスの不一致の問題を修正しました。 [＃52914](https://github.com/pingcap/tidb/issues/52914) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加する際のネットワーク パーティションによって、データ インデックスの不整合が発生する可能性がある問題を修正しました。 [＃54897](https://github.com/pingcap/tidb/issues/54897) @ [tangenta](https://github.com/tangenta)
    -   `SHOW WARNINGS;`を使用して警告を取得するとpanicが発生する可能性がある問題を修正しました [＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると TiDB がpanicを起こす可能性がある問題を修正[＃54324](https://github.com/pingcap/tidb/issues/54324) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子の駆動側サブノードである場合に`memTracker`切り離されないことで発生する異常に高いメモリ使用量の問題を修正しました。 [＃54005](https://github.com/pingcap/tidb/issues/54005) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   再帰CTEクエリが無効なポインタを生成する可能性がある問題を修正しました [＃54449](https://github.com/pingcap/tidb/issues/54449) @ [hawkingrei](https://github.com/hawkingrei)
    -   空の投影により TiDB がpanicを引き起こす問題を修正しました [＃49109](https://github.com/pingcap/tidb/issues/49109) @ [winoros](https://github.com/winoros)
    -   データ変更操作を含むトランザクションで仮想列を持つテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました [＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)
    -   `AUTO_ID_CACHE=1`AUTO_INCREMENT列を含むテーブルで、 `auto_increment_increment`と`auto_increment_offset`システム変数をデフォルト以外の値に設定すると、不正なAUTO_INCREMENT ID 割り当てが発生する可能性がある問題を修正しました。 [＃52622](https://github.com/pingcap/tidb/issues/52622) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `ALL`関数に含まれるサブクエリが誤った結果を引き起こす可能性がある問題を修正[＃52755](https://github.com/pingcap/tidb/issues/52755) @ [hawkingrei](https://github.com/hawkingrei)
    -   SQLクエリのフィルタ条件に仮想列が含まれており、実行条件に`UnionScan` が含まれている場合に述語を適切にプッシュダウンできない問題を修正しました。 [＃54870](https://github.com/pingcap/tidb/issues/54870) @ [qw4990](https://github.com/qw4990)
    -   `UPDATE`リスト内のサブクエリによって TiDB がpanicを起こす可能性がある問題を修正[＃52687](https://github.com/pingcap/tidb/issues/52687) @ [winoros](https://github.com/winoros)
    -   `GROUP BY`ステートメント内の間接プレースホルダ`?`参照が列を見つけられない問題を修正しました [＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)
    -   `Sort`演算子がスピルした後にディスクファイルが削除されず、クエリエラーが発生する可能性がある問題を修正[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [wshwsh12](https://github.com/wshwsh12)
    -   `SELECT ... FOR UPDATE` の間違ったPointGetプランを再利用する問題を修正しました [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)
    -   複数のレベルの`max_execute_time`設定が互いに干渉する問題を修正[＃50914](https://github.com/pingcap/tidb/issues/50914) @ [jiyfhust](https://github.com/jiyfhust)
    -   TiDB を再起動した後、主キー列統計のヒストグラムと TopN がロードされない問題を修正しました [＃37548](https://github.com/pingcap/tidb/issues/37548) @ [hawkingrei](https://github.com/hawkingrei)
    -   TopN演算子が誤ってプッシュダウンされる可能性がある問題を修正しました [＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)
    -   `SELECT ... WHERE ... ORDER BY ...`文の実行パフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   TiDBが接続を閉じるときにログにエラーを報告する場合がある問題を修正[＃53689](https://github.com/pingcap/tidb/issues/53689) @ [jackysp](https://github.com/jackysp)
    -   場合によっては無効な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [tangenta](https://github.com/tangenta)
    -   ビュー定義でサブクエリが列定義として使用されている場合、 `information_schema.columns`を使用して列情報を取得すると警告1356が返される問題を修正しました。 [＃54343](https://github.com/pingcap/tidb/issues/54343) @ [lance6716](https://github.com/lance6716)
    -   クエリ条件`column IS NULL` で一意インデックスにアクセスするときに、オプティマイザが行数を誤って 1 と推定する問題を修正しました。 [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [hawkingrei](https://github.com/hawkingrei)
    -   クラスター化インデックスを述語として使用すると`SELECT INTO OUTFILE`機能しない問題を修正[＃42093](https://github.com/pingcap/tidb/issues/42093) @ [qw4990](https://github.com/qw4990)
    -   オプティマイザーヒント使用時に誤った警告情報が表示される問題を修正しました [＃53767](https://github.com/pingcap/tidb/issues/53767) @ [hawkingrei](https://github.com/hawkingrei)
    -   同期負荷QPSモニタリングメトリックが正しくない問題を修正[＃53558](https://github.com/pingcap/tidb/issues/53558) @ [hawkingrei](https://github.com/hawkingrei)
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラーが発生する可能性がある問題を修正 [＃53673](https://github.com/pingcap/tidb/issues/53673) @ [tangenta](https://github.com/tangenta)
    -   `RESTORE`ステートメントを使用して`AUTO_ID_CACHE=1`のテーブルを復元すると`Duplicate entry`エラーが発生する可能性がある問題を修正しました [＃52680](https://github.com/pingcap/tidb/issues/52680) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` になる問題を修正しました [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [Defined2014](https://github.com/Defined2014)
    -   述語の`Longlong`型のオーバーフローの問題を修正 [＃45783](https://github.com/pingcap/tidb/issues/45783) @ [hawkingrei](https://github.com/hawkingrei)
    -   キャッシュされた実行プランに日付型と`unix_timestamp` の比較が含まれている場合に誤った結果が返される問題を修正しました。 [＃48165](https://github.com/pingcap/tidb/issues/48165) @ [qw4990](https://github.com/qw4990)
    -   照合順序が`utf8_bin`または`utf8mb4_bin` の場合に`LENGTH()`条件が予期せず削除される問題を修正しました [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [elsa0520](https://github.com/elsa0520)
    -   `UPDATE`または`DELETE`ステートメントに再帰 CTE が含まれている場合、ステートメントがエラーを報告したり、 が有効にならない可能性がある問題を修正しました。 [＃55666](https://github.com/pingcap/tidb/issues/55666) @ [time-and-fate](https://github.com/time-and-fate)
    -   相関サブクエリと CTE を含むクエリを実行すると、TiDB がハングしたり、誤った結果が返されたりする問題を修正しました。 [＃55551](https://github.com/pingcap/tidb/issues/55551) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   統計を初期化するときに、非バイナリ照合の文字列列の統計の読み込みに失敗する可能性がある問題を修正しました。 [＃55684](https://github.com/pingcap/tidb/issues/55684) @ [winoros](https://github.com/winoros)
    -   IndexJoin が Left Outer Anti Semi type のハッシュ値を計算するときに重複行を生成する問題を修正しました。 [＃52902](https://github.com/pingcap/tidb/issues/52902) @ [yibin87](https://github.com/yibin87)
    -   `UNION`を含むクエリステートメントが誤った結果を返す可能性がある問題を修正しました [＃52985](https://github.com/pingcap/tidb/issues/52985) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました [＃53867](https://github.com/pingcap/tidb/issues/53867) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   厳密に自己増分ではないRANGEパーティションテーブルが作成できる問題を修正 [＃54829](https://github.com/pingcap/tidb/issues/54829) @ [Defined2014](https://github.com/Defined2014)
    -   メモリ使用量が`tidb_mem_quota_query` で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [yibin87](https://github.com/yibin87)
    -   `STATE`フィールドのうち`size`が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`テーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `IndexNestedLoopHashJoin` のデータ競合問題を修正 [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [solotzg](https://github.com/solotzg)
    -   間違った TableDual プランにより空のクエリ結果が発生する問題を修正しました [＃50051](https://github.com/pingcap/tidb/issues/50051) @ [onlyacat](https://github.com/onlyacat)
    -   `mysql.stats_histograms`表の`tot_col_size`番目の列が負の数になる可能性がある問題を修正しました [＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)
    -   `FLOAT`型から`UNSIGNED`型へのデータ変換で誤った結果が返される問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `auth_socket`認証プラグインを使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。 [＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)
    -   `memory_quota`ヒントがサブクエリで機能しない可能性がある問題を修正しました [＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)
    -   プランキャッシュシナリオでメタデータロックがDDL操作の実行を阻止できない問題を修正 [＃51407](https://github.com/pingcap/tidb/issues/51407) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   列のデフォルト値として`CURRENT_DATE()`を使用すると、クエリ結果が正しくなくなる問題を修正しました [＃53746](https://github.com/pingcap/tidb/issues/53746) @ [tangenta](https://github.com/tangenta)
    -   `COALESCE()`関数が`DATE`の型パラメータに対して誤った結果型を返す問題を修正しました [＃46475](https://github.com/pingcap/tidb/issues/46475) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに発生する予期しないエラーを修正します。これはの繰り返し操作による以前のパラメータ値の再利用が原因です。 [＃53600](https://github.com/pingcap/tidb/issues/53600) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   相関サブクエリにおける TopN 演算子の誤った結果を修正 [＃52777](https://github.com/pingcap/tidb/issues/52777) @ [yibin87](https://github.com/yibin87)
    -   再帰CTE演算子がメモリ使用量を誤って追跡する問題を修正しました [＃54181](https://github.com/pingcap/tidb/issues/54181) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `SHOW COLUMNS`を使用してビューの列を表示するとエラーが発生する問題を修正しました [＃54964](https://github.com/pingcap/tidb/issues/54964) @ [lance6716](https://github.com/lance6716)
    -   TTLジョブ実行中に値を`tidb_ttl_delete_worker_count`減らすとジョブが完了しなくなる問題を修正しました [＃55561](https://github.com/pingcap/tidb/issues/55561) @ [lcwangchao](https://github.com/lcwangchao)
    -   再帰CTE でビューの使用が機能しない問題を修正 [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [hawkingrei](https://github.com/hawkingrei)
    -   外部キーを持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました。 [＃53652](https://github.com/pingcap/tidb/issues/53652) @ [hawkingrei](https://github.com/hawkingrei)
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3Hunter](https://github.com/D3Hunter)
    -   クエリの同時実行数が多い場合に統計同期読み込みメカニズムが予期せず失敗する可能性がある問題を修正しました[＃52294](https://github.com/pingcap/tidb/issues/52294) @ [hawkingrei](https://github.com/hawkingrei)
    -   クエリ内の特定のフィルタ条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) を報告する可能性がある問題を修正しました [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [YangKeao](https://github.com/YangKeao) [＃53594](https://github.com/pingcap/tidb/issues/53594)
    -   TiDBの同期的な統計読み込みメカニズムが空の統計の読み込みを無期限に再試行し、 `fail to get stats version for this histogram` log を出力問題を修正しました。 [＃52657](https://github.com/pingcap/tidb/issues/52657) @ [hawkingrei](https://github.com/hawkingrei)
    -   最初の引数が`month`で、2番目の引数が負の場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。 [＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `tidb_mem_quota_analyze`が有効になっていて、統計の更新に使用されるメモリがの制限を超えると、TiDB がクラッシュする可能性がある問題を修正しました。 [＃52601](https://github.com/pingcap/tidb/issues/52601) @ [hawkingrei](https://github.com/hawkingrei)
    -   一意インデックスを追加するときに`duplicate entry`発生する可能性がある問題を修正 [＃56161](https://github.com/pingcap/tidb/issues/56161) @ [tangenta](https://github.com/tangenta)
    -   情報スキーマキャッシュミスにより、古い読み取りのクエリレイテンシーが増加する問題を修正しました。 [＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)
    -   GlobalStatsの`Distinct_count`情報が正しくない可能性がある問題を修正しました[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [hawkingrei](https://github.com/hawkingrei)
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [hawkingrei](https://github.com/hawkingrei)
    -   クエリに利用可能なインデックスマージ実行プランがある場合に`read_from_storage`ヒントが有効にならない可能性がある問題を修正しました [＃56217](https://github.com/pingcap/tidb/issues/56217) @ [AilinKid](https://github.com/AilinKid)
    -   `TIMESTAMPADD()`関数が誤った結果を返す問題を修正[＃41052](https://github.com/pingcap/tidb/issues/41052) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `?`の引数を含む`CONV`の式を持つ`PREPARE` `EXECUTE`ステートメントを複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [ekexium](https://github.com/ekexium)
    -   スライスの浅いコピーを使用せずに列プルーニングを行うと、TiDB がpanicを起こす可能性がある問題を修正しました[＃52768](https://github.com/pingcap/tidb/issues/52768) @ [winoros](https://github.com/winoros)
    -   ウィンドウ関数を含むSQLバインディングが場合によっては有効にならない可能性がある問題を修正[＃55981](https://github.com/pingcap/tidb/issues/55981) @ [winoros](https://github.com/winoros)
    -   インデックスデータを解析するときに TiDB がpanicする可能性がある問題を修正しました [＃47115](https://github.com/pingcap/tidb/issues/47115) @ [zyguan](https://github.com/zyguan)
    -   起動時に統計情報をロードするときに、TiDB が GC によるエラーを報告する可能性がある問題を修正[＃53592](https://github.com/pingcap/tidb/issues/53592) @ [you06](https://github.com/you06)
    -   DML文にネストされた生成列が含まれている場合にエラーが発生する問題を修正しました [＃53967](https://github.com/pingcap/tidb/issues/53967) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   常に`true` となる述語を持つ`SHOW ERRORS`ステートメントを実行すると TiDB がパニックを起こす問題を修正しました。 [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [elsa0520](https://github.com/elsa0520)
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [zimulala](https://github.com/zimulala)
    -   インデックス追加中の再試行によって発生するデータ インデックスの不整合の問題を修正しました [＃55808](https://github.com/pingcap/tidb/issues/55808) @ [lance6716](https://github.com/lance6716)
    -   列の不安定な一意のIDにより、 `UPDATE`文がエラーを返す可能性がある問題を修正しました。 [＃53236](https://github.com/pingcap/tidb/issues/53236) @ [winoros](https://github.com/winoros)
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panicが発生する可能性がある問題を修正しました。 [＃53540](https://github.com/pingcap/tidb/issues/53540) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   `RECOVER TABLE BY JOB JOB_ID;`を実行すると TiDB がpanicを起こす可能性がある問題を修正[＃55113](https://github.com/pingcap/tidb/issues/55113) @ [crazycs520](https://github.com/crazycs520)
    -   分散実行フレームワークの PD メンバーを変更した後に`ADD INDEX`実行が失敗する可能性がある問題を修正しました [＃48680](https://github.com/pingcap/tidb/issues/48680) @ [lance6716](https://github.com/lance6716)
    -   2人のDDL所有者が同時に存在する可能性がある問題を修正[＃54689](https://github.com/pingcap/tidb/issues/54689) @ [joccau](https://github.com/joccau)
    -   `ADD INDEX`の実行中に TiDB のローリング再起動が発生すると、インデックスの追加操作が失敗する可能性がある問題を修正しました[＃52805](https://github.com/pingcap/tidb/issues/52805) @ [tangenta](https://github.com/tangenta)
    -   `LOAD DATA ... REPLACE INTO`操作でデータの不整合が発生する問題を修正[＃56408](https://github.com/pingcap/tidb/issues/56408) @ [fzzf678](https://github.com/fzzf678)
    -   `IMPORT INTO`ステートメントを使用してデータをインポートした後、 `AUTO_INCREMENT`フィールドが正しく設定されない問題を修正しました。 [＃56476](https://github.com/pingcap/tidb/issues/56476) @ [D3Hunter](https://github.com/D3Hunter)
    -   TiDBがチェックポイントから復元する前にローカルファイルの存在を確認しない問題を修正しました [＃53009](https://github.com/pingcap/tidb/issues/53009) @ [lance6716](https://github.com/lance6716)
    -   DMスキーマトラッカーがデフォルトの長さよりも長いインデックスを作成できない問題を修正しました [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [lance6716](https://github.com/lance6716)
    -   `ALTER TABLE` `AUTO_INCREMENT`フィールドを正しく処理しない問題を修正[＃47899](https://github.com/pingcap/tidb/issues/47899) @ [D3Hunter](https://github.com/D3Hunter)
    -   解放されていないセッションリソースがメモリリークを引き起こす可能性がある問題を修正[＃56271](https://github.com/pingcap/tidb/issues/56271) @ [lance6716](https://github.com/lance6716)
    -   浮動小数点数または整数オーバーフローがプランキャッシュに影響を与える問題を修正しました [＃46538](https://github.com/pingcap/tidb/issues/46538) @ [hawkingrei](https://github.com/hawkingrei)
    -   `IndexLookUp`演算子のメモリの一部が追跡されない問題を修正 [＃56440](https://github.com/pingcap/tidb/issues/56440) @ [wshwsh12](https://github.com/wshwsh12)
    -   stale read が読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間の間にオフセットが存在する場合に、トランザクションの一貫性にわずかながら影響する可能性が生じます。 [＃56809](https://github.com/pingcap/tidb/issues/56809) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   ストレージエンジンとしてTiKVが選択されていない場合にTTLが失敗する可能性がある問題を修正 [＃56402](https://github.com/pingcap/tidb/issues/56402) @ [YangKeao](https://github.com/YangKeao)
    -   書き込み競合が発生したときにTTLタスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [YangKeao](https://github.com/YangKeao)
    -   科学表記法で大きすぎる数値を挿入するとエラーが発生する問題を修正`ERROR 1264 (22003)` 。動作を MySQL と一致させる。 [＃47787](https://github.com/pingcap/tidb/issues/47787) @ [lcwangchao](https://github.com/lcwangchao)
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   `INSERT ... ON DUPLICATE KEY`文が`mysql_insert_id` と互換性がない問題を修正 [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   SQLが実行プランを構築できない場合に監査ログフィルタリングが有効にならない問題を修正 [＃50988](https://github.com/pingcap/tidb/issues/50988) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   v6.5からv7.5以降にアップグレードされたクラスターで、既存のTTLタスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   `CAST`関数が文字セットの明示的な設定をサポートしていない問題を修正しました [＃55677](https://github.com/pingcap/tidb/issues/55677) @ [Defined2014](https://github.com/Defined2014)
    -   `ADD INDEX` を実行するときに TiDB がインデックスの長さ制限をチェックしない問題を修正しました [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [fzzf678](https://github.com/fzzf678)

-   TiKV

    -   `RawKvMaxTimestampNotSynced`エラーを追加し、 `errorpb.Error.max_ts_not_synced`に詳細なエラー情報をログに記録し、このエラーが発生したときに`must_raw_put`操作の再試行メカニズムを追加します[＃16789](https://github.com/tikv/tikv/issues/16789) @ [pingyu](https://github.com/pingyu)
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるトラフィック制御の問題を修正しました [＃17304](https://github.com/tikv/tikv/issues/17304) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   読み取りスレッドがRaft EngineのMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。 [＃17383](https://github.com/tikv/tikv/issues/17383) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   TiDB Lightningによってインポートされた SST ファイルが TiKV の再起動後に失われる問題を修正[＃15912](https://github.com/tikv/tikv/issues/15912) @ [lance6716](https://github.com/lance6716)
    -   削除された`sst_importer` SST ファイルを取り込むことにより TiKV がpanicになる可能性がある問題を修正しました [＃15053](https://github.com/tikv/tikv/issues/15053) @ [lance6716](https://github.com/lance6716)
    -   TiKVインスタンスに多数のリージョンがある場合、データインポート中にTiKVがOOMになる可能性がある問題を修正しました。 [＃16229](https://github.com/tikv/tikv/issues/16229) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   ブルームフィルタが以前のバージョン（v7.1より前）とそれ以降のバージョンの間で互換性がない問題を修正しました [＃17272](https://github.com/tikv/tikv/issues/17272) @ [v01dstar](https://github.com/v01dstar)
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB に送信されるメッセージには反映されない問題を修正しました。 [＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)
    -   不安定なテストケースの問題を修正し、各テストが独立した一時ディレクトリを使用するようにして、オンライン構成の変更が他のテストケースに影響しないようにします。 [＃16871](https://github.com/tikv/tikv/issues/16871) @ [glorv](https://github.com/glorv)
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出への過度の圧力によって TiKV OOM 問題が発生する可能性がある問題を修正しました [＃17394](https://github.com/tikv/tikv/issues/17394) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   `DECIMAL`型の小数点部分がの場合に正しくない問題を修正しました [＃16913](https://github.com/tikv/tikv/issues/16913) @ [gengliqi](https://github.com/gengliqi)
    -   クエリ内の`CONV()`関数が数値システム変換中にオーバーフローし、TiKV panicが発生する問題を修正しました。 [＃16969](https://github.com/tikv/tikv/issues/16969) @ [gengliqi](https://github.com/gengliqi)
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカの即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。 [＃17469](https://github.com/tikv/tikv/issues/17469) @ [hbisheng](https://github.com/hbisheng)
    -   同時実行性の高いコプロセッサー要求により TiKV OOM が発生する可能性がある問題を修正しました [＃16653](https://github.com/tikv/tikv/issues/16653) @ [overvenus](https://github.com/overvenus)
    -   マスターキーがキー管理サービス (KMS) に保存されているときにマスターキーのローテーションを妨げる問題を修正しました [＃17410](https://github.com/tikv/tikv/issues/17410) @ [hhwyt](https://github.com/hhwyt)
    -   tikv-ctlの`raft region`コマンドの出力にリージョンステータス情報が含まれていない問題を修正しました [＃17037](https://github.com/tikv/tikv/issues/17037) @ [glorv](https://github.com/glorv)
    -   Grafana の TiKV パネルの**ストレージ非同期書き込み期間の**監視メトリックが不正確であるという問題を修正しました[＃17579](https://github.com/tikv/tikv/issues/17579) @ [overvenus](https://github.com/overvenus)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [overvenus](https://github.com/overvenus)

-   PD

    -   ラベル統計のメモリリーク問題を修正 [＃8700](https://github.com/tikv/pd/issues/8700) @ [lhy1024](https://github.com/lhy1024)
    -   リソース グループが過剰なログを出力する問題を修正しました [＃8159](https://github.com/tikv/pd/issues/8159) @ [nolouch](https://github.com/nolouch)
    -   乱数ジェネレータの頻繁な作成によって発生するパフォーマンスジッターの問題を修正しました [＃8674](https://github.com/tikv/pd/issues/8674) @ [rleungx](https://github.com/rleungx)
    -   リージョン統計のメモリリーク問題を修正 [＃8710](https://github.com/tikv/pd/issues/8710) @ [rleungx](https://github.com/rleungx)
    -   ホットスポット キャッシュのメモリリーク問題を修正 [＃8698](https://github.com/tikv/pd/issues/8698) @ [lhy1024](https://github.com/lhy1024)
    -   同じストアID で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正 [＃8756](https://github.com/tikv/pd/issues/8756) @ [okJiang](https://github.com/okJiang)
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が起動しなくなる問題を修正 [＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)
    -   設定ファイル経由でログレベルを変更しても反映されない問題を修正[＃8117](https://github.com/tikv/pd/issues/8117) @ [rleungx](https://github.com/rleungx)
    -   同時実行性が高い場合にリソース グループがリソース使用量を効果的に制限できない問題を修正[＃8435](https://github.com/tikv/pd/issues/8435) @ [nolouch](https://github.com/nolouch)
    -   PD がオペレータ チェック中に遭遇するデータ競合問題を修正しました [＃8263](https://github.com/tikv/pd/issues/8263) @ [lhy1024](https://github.com/lhy1024)
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [nolouch](https://github.com/nolouch)
    -   一部のログが編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   ロールをリソースグループにバインドするときにエラーが報告されない問題を修正しました [＃54417](https://github.com/pingcap/tidb/issues/54417) @ [JmPotato](https://github.com/JmPotato)
    -   多数のリージョンが存在する場合にPDのリージョンAPIをリクエストできない問題を修正[＃55872](https://github.com/pingcap/tidb/issues/55872) @ [rleungx](https://github.com/rleungx)
    -   リソースグループクエリをキャンセルするときに再試行回数が多すぎる問題を修正 [＃8217](https://github.com/tikv/pd/issues/8217) @ [nolouch](https://github.com/nolouch)
    -   暗号化マネージャーが使用前に初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [rleungx](https://github.com/rleungx)
    -   PDの`Filter target`監視メトリックが散布範囲情報を提供しない問題を修正[＃8125](https://github.com/tikv/pd/issues/8125) @ [HuSharp](https://github.com/HuSharp)
    -   リソースグループのデータ競合問題を修正 [＃8267](https://github.com/tikv/pd/issues/8267) @ [HuSharp](https://github.com/HuSharp)
    -   TiKV構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB未満の値に設定するとPD panicが発生する問題を修正しました [＃8323](https://github.com/tikv/pd/issues/8323) @ [JmPotato](https://github.com/JmPotato)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが利用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値より少なくなる問題を修正しました。 [＃7346](https://github.com/tikv/pd/issues/7346) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   配置ルールを使用しているときに、ダウンしたピアが回復しない可能性がある問題を修正しました。 [＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   クラスタをv6.5.0より前のバージョンからv6.5.0以降にアップグレードするときに、 TiFlashメタデータが破損してプロセスがpanicになる可能性がある問題を修正しました[＃9039](https://github.com/pingcap/tiflash/issues/9039) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される可能性がある問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [JinheLin](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になっている場合に一部のクエリでエラーが報告される可能性がある問題を修正[＃9472](https://github.com/pingcap/tiflash/issues/9472) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash にプッシュダウンされる問題を修正しました [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [windtalker](https://github.com/windtalker)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラーが発生する可能性がある問題を修正しました。 [＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   BRまたはTiDB Lightning 経由でデータをインポートした後、FastScanモードで多数の重複行が読み取られる可能性がある問題を修正しました。 [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [JinheLin](https://github.com/JinheLin)
    -   テーブルに無効な文字を含むデフォルト値を持つビット型の列が含まれている場合、 TiFlash がテーブル スキーマを解析できない問題を修正しました。 [＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [JinheLin](https://github.com/JinheLin)
    -   データベース間で`ALTER TABLE ... EXCHANGE PARTITION`を実行した後にTiFlash がスキーマの同期に失敗する可能性がある問題を修正しました [＃7296](https://github.com/pingcap/tiflash/issues/7296) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   データベースが作成直後に削除されるとTiFlash がpanicする可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [solotzg](https://github.com/solotzg)
    -   TiFlash が高同時読み取りシナリオで一時的に誤った結果を返す可能性がある問題を修正[＃8845](https://github.com/pingcap/tiflash/issues/8845) @ [JinheLin](https://github.com/JinheLin)
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash のクラッシュを引き起こす可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [wshwsh12](https://github.com/wshwsh12)
    -   クラスタ内で長期間にわたって頻繁に`EXCHANGE PARTITION`と`DROP TABLE`操作を行うと、 TiFlashテーブル メタデータのレプリケーションが遅くなり、クエリ パフォーマンスが低下する可能性がある問題を修正しました[＃9227](https://github.com/pingcap/tiflash/issues/9227) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   空のキー範囲を持つクエリがTiFlash上で読み取りタスクを正しく生成できず、 TiFlashクエリがブロックされる可能性がある問題を修正しました。 [＃9108](https://github.com/pingcap/tiflash/issues/9108) @ [JinheLin](https://github.com/JinheLin)
    -   特定のケースで関数`CAST AS DECIMAL`の結果の符号が正しくない問題を修正[＃9301](https://github.com/pingcap/tiflash/issues/9301) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `SUBSTRING()`関数が特定の整数型に対して`pos`と`len`引数をサポートせず、クエリエラーが発生する問題を修正しました [＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [gengliqi](https://github.com/gengliqi)
    -   大きなテーブルで`DROP TABLE`を実行するとTiFlash OOM が発生する可能性がある問題を修正しました [＃9437](https://github.com/pingcap/tiflash/issues/9437) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   BR統合テストケースが不安定になる問題を修正し、スナップショットまたはログバックアップファイルの破損をシミュレートする新しいテストケースを追加します[＃53835](https://github.com/pingcap/tidb/issues/53835) @ [Leavrth](https://github.com/Leavrth)
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア中に正しく回復されない可能性がある問題を修正しました。 [＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3pointer](https://github.com/3pointer)
        -   ログバックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD で適切にクリアされない問題を修正しました。 [＃17316](https://github.com/tikv/tikv/issues/17316) @ [Leavrth](https://github.com/Leavrth)
        -   アドバンサーオーナーの移行後にログバックアップが一時停止される可能性がある問題を修正しました [＃53561](https://github.com/pingcap/tidb/issues/53561) @ [RidRisR](https://github.com/RidRisR)
        -   増分バックアップ中の DDL ジョブのスキャンの非効率性の問題を修正 [＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3pointer](https://github.com/3pointer)
        -   リージョンリーダーの探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。 [＃17168](https://github.com/tikv/tikv/issues/17168) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップが有効になっているときにBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [RidRisR](https://github.com/RidRisR)
        -   復元プロセス中に複数のネストされた再試行によりBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [RidRisR](https://github.com/RidRisR)
        -   PD へのネットワーク接続が不安定な状態で一時停止中のログバックアップタスクを再開すると TiKV がpanicする可能性がある問題を修正しました [＃17020](https://github.com/tikv/tikv/issues/17020) @ [YuJuncen](https://github.com/YuJuncen)
        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [Leavrth](https://github.com/Leavrth)
        -   バックアップと復元のチェックポイントパスが一部の外部ストレージと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [Leavrth](https://github.com/Leavrth)
        -   BRを使用してデータを復元する場合、または物理インポート モードでTiDB Lightningを使用してデータをインポートする場合に、PD から取得されたリージョンにLeaderがない問題を修正しました[＃51124](https://github.com/pingcap/tidb/issues/51124) [＃50501](https://github.com/pingcap/tidb/issues/50501) @ [Leavrth](https://github.com/Leavrth)
        -   PDリーダーの転送により、データの復元時にBRがpanicになる可能性がある問題を修正しました。 [＃53724](https://github.com/pingcap/tidb/issues/53724) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップタスクを一時停止、停止、再構築した後、タスクの状態は正常であるが、チェックポイントが進まない問題を修正しました。 [＃53047](https://github.com/pingcap/tidb/issues/53047) @ [RidRisR](https://github.com/RidRisR)
        -   ログバックアップが残留ロックをすぐに解決できず、チェックポイントが進まない問題を修正しました。 [＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3pointer](https://github.com/3pointer)

    -   TiCDC

        -   `TIMEZONE`タイプのデフォルト値が正しいタイムゾーンに従って設定されない問題を修正 [＃10931](https://github.com/pingcap/tiflow/issues/10931) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   ソーターモジュールがディスクデータを読み取るときにTiCDCがpanicになる可能性がある問題を修正しました [＃10853](https://github.com/pingcap/tiflow/issues/10853) @ [hicqu](https://github.com/hicqu)
        -   マルチノード環境で大量の`UPDATE`操作を実行する際にChangefeedを繰り返し再起動するとデータの不整合が発生する可能性がある問題を修正[＃11219](https://github.com/pingcap/tiflow/issues/11219) @ [lidezhu](https://github.com/lidezhu)
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように設定した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリームに複製しない問題を修正しました。 [＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `DROP PRIMARY KEY`と`DROP UNIQUE KEY`ステートメントが正しく複製されない問題を修正[＃10890](https://github.com/pingcap/tiflow/issues/10890) @ [asddongmen](https://github.com/asddongmen)
        -   下流の Kafka にアクセスできない場合にプロセッサモジュールがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   DMが`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーションエラーが発生する問題を修正しました。 [＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [lance6716](https://github.com/lance6716)
        -   複数の DM マスターノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   `go-mysql` にアップグレードして接続ブロックの問題を修正しました [＃11041](https://github.com/pingcap/tiflow/issues/11041) @ [D3Hunter](https://github.com/D3Hunter)
        -   インデックスの長さがデフォルト値の`max-index-length` を超えるとデータレプリケーションが中断される問題を修正しました [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [michaelmdeng](https://github.com/michaelmdeng)
        -   LISTパーティションテーブルの`ALTER TABLE ... DROP PARTITION`文を複製するときにDMがエラーを返す問題を修正しました。 [＃54760](https://github.com/pingcap/tidb/issues/54760) @ [lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB LightningがTiKV から送信されたサイズ超過のメッセージを受信できない問題を修正しました [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [fishiu](https://github.com/fishiu)
        -   TiDB Lightning のインポートモードを無効にした後にデータをインポートすると TiKV データが破損する可能性がある問題を修正しました [＃47694](https://github.com/pingcap/tidb/issues/47694) @ [lance6716](https://github.com/lance6716) [＃15003](https://github.com/tikv/tikv/issues/15003)
        -   TiDB Lightning を使用してデータのインポート中にトランザクションの競合が発生する問題を修正しました [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [lance6716](https://github.com/lance6716)
        -   EBS BRが実行されているときにTiDB Lightningがデータのインポートに失敗する可能性がある問題を修正しました [＃49517](https://github.com/pingcap/tidb/issues/49517) @ [mittalrishabh](https://github.com/mittalrishabh)
        -   2つのインスタンスが同時に並列インポートタスクを開始し、同じタスクID が割り当てられている場合に、 TiDB Lightningが`verify allocator base failed`エラーを報告する問題を修正しました。 [＃55384](https://github.com/pingcap/tidb/issues/55384) @ [ei-sugimoto](https://github.com/ei-sugimoto)
        -   PDLeaderを強制終了すると、 TiDB Lightningがデータインポート中に`invalid store ID 0`エラーを報告する問題を修正しました。 [＃50501](https://github.com/pingcap/tidb/issues/50501) @ [Leavrth](https://github.com/Leavrth)

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [tangenta](https://github.com/tangenta)

    -   TiDB Binlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`の実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正しました[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [tangenta](https://github.com/tangenta)
