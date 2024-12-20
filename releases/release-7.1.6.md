---
title: TiDB 7.1.6 Release Notes
summary: TiDB 7.1.6 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.1.6 リリースノート {#tidb-7-1-6-release-notes}

発売日: 2024年11月21日

TiDB バージョン: 7.1.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.1/docs/tidb_http_api.md)から取得される DDL 履歴タスクのデフォルトの制限を 2048 に設定して、履歴タスク[＃55711](https://github.com/pingcap/tidb/issues/55711) @ [ジョッカウ](https://github.com/joccau)の過剰による OOM の問題を防止します。
-   以前のバージョンでは、 `UPDATE`の変更を含むトランザクションを処理するときに、 `UPDATE`イベントで主キーまたは非 NULL の一意のインデックス値が変更されると、TiCDC はこのイベントを`DELETE`のイベントと`INSERT`イベントに分割していました。v7.1.6 以降では、MySQL シンクを使用する場合、 `UPDATE`の変更のトランザクション`commitTS`が TiCDC `thresholdTS` (TiCDC が対応するテーブルをダウンストリームに複製し始めるときに PD から取得される現在のタイムスタンプ) より小さい場合、TiCDC は`UPDATE`イベントを`DELETE`のイベントと`INSERT`のイベントに分割します。この動作変更により、TiCDC が受信した`UPDATE`イベントの順序が誤っている可能性があり、分割された`DELETE`と`INSERT`イベントの順序が誤っている可能性があるため、ダウンストリーム データの不整合の問題に対処できます。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v7.1/ticdc-split-update-behavior#split-update-events-for-mysql-sinks)参照してください[＃10918](https://github.com/pingcap/tiflow/issues/10918) @ [リデズ](https://github.com/lidezhu)
-   TiDB Lightning `strict-format`使用して CSV ファイルをインポートする場合は、行末文字を設定する必要があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [ランス6716](https://github.com/lance6716)

## 改善点 {#improvements}

-   ティビ

    -   統計がすべて TopN で構成され、対応するテーブル統計の変更された行数が 0 以外の場合、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   MPP ロード バランシング中にリージョンのないストアを削除する[＃52313](https://github.com/pingcap/tidb/issues/52313) @ [翻訳者](https://github.com/xzhangxian1008)
    -   `SHOW CREATE TABLE` [＃52939](https://github.com/pingcap/tidb/issues/52939) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の出力に表示される式のデフォルト値の MySQL 互換性を改善しました
    -   TiFlash配置ルールを一括削除することで、パーティションテーブル[＃54068](https://github.com/pingcap/tidb/issues/54068) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。
    -   同期ロードパフォーマンスを改善して、統計情報のロード時のレイテンシーを削減します[＃52294](https://github.com/pingcap/tidb/issues/52294) [ホーキングレイ](https://github.com/hawkingrei)

-   ティクヴ

    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します。
    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV [＃15874](https://github.com/tikv/tikv/issues/15874) @ [リクササシネーター](https://github.com/LykxSassinator)の安定性を向上しました。
    -   不要な非同期ブロックを削除してメモリ使用量を削減する[＃16540](https://github.com/tikv/tikv/issues/16540) @ [金星の上](https://github.com/overvenus)

-   TiFlash

    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化[＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [翻訳者](https://github.com/xzhangxian1008)
    -   TLS を有効にした後に証明書を更新することでTiFlash がpanicになる可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [風の話し手](https://github.com/windtalker)
    -   JOIN 演算子のキャンセル メカニズムを改善し、JOIN 演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [風の話し手](https://github.com/windtalker)
    -   同時実行性の高いデータ読み取り操作でのロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [ジンヘリン](https://github.com/JinheLin)
    -   クラスター化インデックス[＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップのマージ操作に対する許容度を高めます。適度に長いマージ操作が発生した場合、ログバックアップタスクがエラー状態[＃16554](https://github.com/tikv/tikv/issues/16554) @ [ユジュンセン](https://github.com/YuJuncen)に入る可能性が低くなります。
        -   BR はデータ復旧中に空の SST ファイルをクリーンアップします[＃16005](https://github.com/tikv/tikv/issues/16005) @ [リーヴルス](https://github.com/Leavrth)
        -   DNSエラーによる失敗の再試行回数を[＃53029](https://github.com/pingcap/tidb/issues/53029)から[ユジュンセン](https://github.com/YuJuncen)増やす
        -   リージョン[＃54017](https://github.com/pingcap/tidb/issues/54017)のリーダー不在による失敗の再試行回数を[リーヴルス](https://github.com/Leavrth)増やす
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [リーヴルス](https://github.com/Leavrth)
        -   TiKV が各 SST ファイルをダウンロードする前に、TiKV のディスク容量が十分かどうかのチェックをサポートします。容量が不十分な場合、 BR は復元を終了し、エラー[＃17224](https://github.com/tikv/tikv/issues/17224) @ [リドリス](https://github.com/RidRisR)を返します。
        -   環境変数[＃45551](https://github.com/pingcap/tidb/issues/45551) @ [リドリス](https://github.com/RidRisR)による Alibaba Cloud アクセス資格情報の設定をサポート
        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドstorageの場合、生のイベントを直接出力することをサポートします[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   REDOログを使用してデータリカバリ中のメモリの安定性を向上させ、OOM [＃10900](https://github.com/pingcap/tiflow/issues/10900) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)の可能性を低減します。
        -   ダウンストリームが`SUPER`権限が付与された TiDB の場合、TiCDC は、場合によっては DDL ステートメントの実行を再試行する際のタイムアウトによるデータ複製の失敗を回避するために、ダウンストリーム データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします[＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

    -   TiDB データ移行 (DM)

        -   19文字を超えるパスワードを使用してMySQLサーバー8.0に接続できるように、 `go-mysql`を1.9.1にアップグレードします[＃11603](https://github.com/pingcap/tiflow/pull/11603) @ [フィシュウ](https://github.com/fishiu)

## バグ修正 {#bug-fixes}

-   ティビ

    -   一意のインデックス[＃52914](https://github.com/pingcap/tidb/issues/52914) @ [翻訳:](https://github.com/wjhuang2016)を追加するときに同時 DML 操作によって発生するデータ インデックスの不整合の問題を修正しました。
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [うわー](https://github.com/wshwsh12)
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加するときにネットワーク パーティションが発生すると、データ インデックス[＃54897](https://github.com/pingcap/tidb/issues/54897) @ [タンジェンタ](https://github.com/tangenta)に不整合が発生する可能性がある問題を修正しました。
    -   `SHOW WARNINGS;`使用して警告を取得するとpanicが発生する可能性がある問題を修正[＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると TiDB がpanicになる可能性がある問題を修正[＃54324](https://github.com/pingcap/tidb/issues/54324) @ [天菜まお](https://github.com/tiancaiamao)
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子[＃54005](https://github.com/pingcap/tidb/issues/54005) @ [徐懐玉](https://github.com/XuHuaiyu)の駆動側サブノードである場合に`memTracker`切り離されないことが原因で異常に高いメモリ使用量が発生する問題を修正しました。
    -   再帰 CTE クエリによって無効なポインタ[＃54449](https://github.com/pingcap/tidb/issues/54449) @ [ホーキングレイ](https://github.com/hawkingrei)が生成される可能性がある問題を修正しました。
    -   空の投影により TiDB がpanicになる問題を修正[＃49109](https://github.com/pingcap/tidb/issues/49109) @ [ウィノロス](https://github.com/winoros)
    -   データ変更操作[＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)を含むトランザクションで仮想列を持つテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました。
    -   `AUTO_ID_CACHE=1`自動増分列を含むテーブルで、 `auto_increment_increment`と`auto_increment_offset`システム変数をデフォルト以外の値に設定すると、不正な自動増分 ID 割り当て[＃52622](https://github.com/pingcap/tidb/issues/52622) @ [天菜まお](https://github.com/tiancaiamao)が発生する可能性がある問題を修正しました。
    -   `ALL`関数に含まれるサブクエリが誤った結果を引き起こす可能性がある問題を修正[＃52755](https://github.com/pingcap/tidb/issues/52755) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   SQLクエリのフィルタ条件に仮想列が含まれ、実行条件に`UnionScan` [＃54870](https://github.com/pingcap/tidb/issues/54870) @ [qw4990](https://github.com/qw4990)が含まれている場合に述語を適切にプッシュダウンできない問題を修正しました。
    -   `UPDATE`リスト内のサブクエリによって TiDB がpanicを起こす可能性がある問題を修正[＃52687](https://github.com/pingcap/tidb/issues/52687) @ [ウィノロス](https://github.com/winoros)
    -   `GROUP BY`ステートメント内の間接プレースホルダー`?`参照が列[＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)を見つけられない問題を修正しました
    -   `Sort`演算子がスピルした後にディスク ファイルが削除されず、クエリ エラーが発生する可能性がある問題を修正しました[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [うわー](https://github.com/wshwsh12)
    -   `SELECT ... FOR UPDATE` [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)の間違ったポイント取得プランを再利用する問題を修正
    -   複数のレベルの`max_execute_time`設定が互いに干渉する問題を修正[＃50914](https://github.com/pingcap/tidb/issues/50914) @ [ジフハウス](https://github.com/jiyfhust)
    -   TiDB [＃37548](https://github.com/pingcap/tidb/issues/37548) @ [ホーキングレイ](https://github.com/hawkingrei)を再起動した後、主キー列統計のヒストグラムと TopN がロードされない問題を修正しました。
    -   TopN演算子が誤ってプッシュダウンされる可能性がある問題を修正[＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)
    -   `SELECT ... WHERE ... ORDER BY ...`ステートメント実行のパフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [天菜まお](https://github.com/tiancaiamao)
    -   一部のケースで接続を閉じるときに TiDB がログにエラーを報告する問題を修正[＃53689](https://github.com/pingcap/tidb/issues/53689) @ [ジャッキー](https://github.com/jackysp)
    -   場合によっては不正な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [タンジェンタ](https://github.com/tangenta)
    -   ビュー定義[＃54343](https://github.com/pingcap/tidb/issues/54343) @ [ランス6716](https://github.com/lance6716)でサブクエリが列定義として使用されている場合、 `information_schema.columns`使用して列情報を取得すると警告 1356 が返される問題を修正しました。
    -   クエリ条件`column IS NULL` [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [ホーキングレイ](https://github.com/hawkingrei)で一意のインデックスにアクセスするときに、オプティマイザが行数を誤って 1 と見積もる問題を修正しました。
    -   クラスター化インデックスを述語として使用すると`SELECT INTO OUTFILE`機能しない問題を修正[＃42093](https://github.com/pingcap/tidb/issues/42093) @ [qw4990](https://github.com/qw4990)
    -   オプティマイザーヒント[＃53767](https://github.com/pingcap/tidb/issues/53767) @ [ホーキングレイ](https://github.com/hawkingrei)使用時に誤った警告情報が表示される問題を修正しました
    -   同期ロード QPS モニタリング メトリックが正しくない問題を修正[＃53558](https://github.com/pingcap/tidb/issues/53558) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラー[＃53673](https://github.com/pingcap/tidb/issues/53673) @ [タンジェンタ](https://github.com/tangenta)が発生する可能性がある問題を修正
    -   `RESTORE`ステートメントを使用して`AUTO_ID_CACHE=1`のテーブルを復元すると`Duplicate entry`エラー[＃52680](https://github.com/pingcap/tidb/issues/52680) @ [天菜まお](https://github.com/tiancaiamao)が発生する可能性がある問題を修正しました
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)になる問題を修正しました
    -   述語[＃45783](https://github.com/pingcap/tidb/issues/45783) @ [ホーキングレイ](https://github.com/hawkingrei)の`Longlong`型のオーバーフローの問題を修正
    -   キャッシュされた実行プランに日付型と`unix_timestamp` [＃48165](https://github.com/pingcap/tidb/issues/48165) @ [qw4990](https://github.com/qw4990)の比較が含まれている場合に誤った結果が返される問題を修正しました。
    -   照合順序が`utf8_bin`または`utf8mb4_bin` [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [エルサ0520](https://github.com/elsa0520)の場合に`LENGTH()`条件が予期せず削除される問題を修正しました
    -   `UPDATE`または`DELETE`ステートメントに再帰 CTE が含まれている場合、ステートメントがエラーを報告したり、 [＃55666](https://github.com/pingcap/tidb/issues/55666) @ [時間と運命](https://github.com/time-and-fate)有効にならない可能性がある問題を修正しました。
    -   相関サブクエリと CTE [＃55551](https://github.com/pingcap/tidb/issues/55551) @ [グオシャオゲ](https://github.com/guo-shaoge)含むクエリを実行すると、TiDB がハングしたり、誤った結果が返されたりする問題を修正しました。
    -   統計[＃55684](https://github.com/pingcap/tidb/issues/55684) @ [ウィノロス](https://github.com/winoros)を初期化するときに、非バイナリ照合順序の文字列列の統計が読み込まれない可能性がある問題を修正しました。
    -   IndexJoin が Left Outer Anti Semi 型[＃52902](https://github.com/pingcap/tidb/issues/52902) @ [いびん87](https://github.com/yibin87)のハッシュ値を計算するときに重複行を生成する問題を修正しました。
    -   `UNION`を含むクエリ ステートメントが誤った結果[＃52985](https://github.com/pingcap/tidb/issues/52985) @ [徐懐玉](https://github.com/XuHuaiyu)を返す可能性がある問題を修正しました
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました[＃53867](https://github.com/pingcap/tidb/issues/53867) @ [翻訳者](https://github.com/xzhangxian1008)
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [いびん87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   `STATE`フィールドのうち`size`が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`テーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [翻訳](https://github.com/cfzjywxk)
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロッツ](https://github.com/solotzg)のデータ競合問題を修正
    -   間違った TableDual プランにより空のクエリ結果[＃50051](https://github.com/pingcap/tidb/issues/50051) @ [猫のみ](https://github.com/onlyacat)が発生する問題を修正
    -   `mysql.stats_histograms`の表の`tot_col_size`列目が負の数[＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました
    -   `FLOAT`型から`UNSIGNED`型へのデータ変換で誤った結果が返される問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `auth_socket`認証プラグイン[＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)を使用する場合、TiDB が認証されていないユーザー接続を拒否できないことがある問題を修正しました。
    -   `memory_quota`ヒントがサブクエリ[＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)で機能しない可能性がある問題を修正しました
    -   プラン キャッシュ シナリオ[＃51407](https://github.com/pingcap/tidb/issues/51407) @ [翻訳:](https://github.com/wjhuang2016)でメタデータ ロックが DDL 操作の実行を阻止できない問題を修正しました。
    -   列のデフォルト値として`CURRENT_DATE()`使用するとクエリ結果が不正確になる問題を修正[＃53746](https://github.com/pingcap/tidb/issues/53746) @ [タンジェンタ](https://github.com/tangenta)
    -   `COALESCE()`関数が`DATE`の型パラメータ[＃46475](https://github.com/pingcap/tidb/issues/46475) @ [翻訳者](https://github.com/xzhangxian1008)に対して誤った結果型を返す問題を修正しました
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに、繰り返しの開閉操作[＃53600](https://github.com/pingcap/tidb/issues/53600) @ [徐懐玉](https://github.com/XuHuaiyu)によって以前のパラメータ値が再利用されたために発生する予期しないエラーを修正します。
    -   相関サブクエリ[＃52777](https://github.com/pingcap/tidb/issues/52777) @ [いびん87](https://github.com/yibin87)の TopN 演算子の誤った結果を修正
    -   再帰 CTE 演算子がメモリ使用量[＃54181](https://github.com/pingcap/tidb/issues/54181) @ [グオシャオゲ](https://github.com/guo-shaoge)を誤って追跡する問題を修正しました
    -   `SHOW COLUMNS`使用してビュー[＃54964](https://github.com/pingcap/tidb/issues/54964) @ [ランス6716](https://github.com/lance6716)列を表示するとエラーが発生する問題を修正しました
    -   TTLジョブ実行中に`tidb_ttl_delete_worker_count`の値を減らすとジョブが[＃55561](https://github.com/pingcap/tidb/issues/55561) @ [lcwangchao](https://github.com/lcwangchao)で完了しなくなる問題を修正
    -   再帰 CTE [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [ホーキングレイ](https://github.com/hawkingrei)でビューの使用が機能しない問題を修正
    -   外部キー[＃53652](https://github.com/pingcap/tidb/issues/53652) @ [ホーキングレイ](https://github.com/hawkingrei)を持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3ハンター](https://github.com/D3Hunter)
    -   クエリの同時実行性が高い場合に統計同期読み込みメカニズムが予期せず失敗する可能性がある問題を修正[＃52294](https://github.com/pingcap/tidb/issues/52294) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   クエリ内の特定のフィルター条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) [＃53594](https://github.com/pingcap/tidb/issues/53594) [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [ヤンケオ](https://github.com/YangKeao)を報告する可能性がある問題を修正しました。
    -   TiDB の同期的な統計読み込みメカニズムが空の統計の読み込みを無期限に再試行し、 `fail to get stats version for this histogram` log [＃52657](https://github.com/pingcap/tidb/issues/52657) @ [ホーキングレイ](https://github.com/hawkingrei)を出力問題を修正しました。
    -   最初の引数が`month`で、2 番目の引数が負の[＃54908](https://github.com/pingcap/tidb/issues/54908) @ [翻訳者](https://github.com/xzhangxian1008)場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。
    -   `tidb_mem_quota_analyze`が有効になっていて、統計の更新に使用されるメモリが制限[＃52601](https://github.com/pingcap/tidb/issues/52601) @ [ホーキングレイ](https://github.com/hawkingrei)を超えると TiDB がクラッシュする可能性がある問題を修正しました
    -   ユニークインデックス[＃56161](https://github.com/pingcap/tidb/issues/56161) @ [タンジェンタ](https://github.com/tangenta)を追加するときに`duplicate entry`発生する可能性がある問題を修正
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [クレイジーcs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   GlobalStatsの`Distinct_count`情報が間違っている可能性がある問題を修正[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   クエリに利用可能なインデックスマージ実行プラン[＃56217](https://github.com/pingcap/tidb/issues/56217) @ [アイリンキッド](https://github.com/AilinKid)がある場合に`read_from_storage`ヒントが有効にならない可能性がある問題を修正しました。
    -   `TIMESTAMPADD()`関数が誤った結果を返す問題を修正[＃41052](https://github.com/pingcap/tidb/issues/41052) @ [翻訳者](https://github.com/xzhangxian1008)
    -   `?`引数を含む`CONV`の式を持つ`PREPARE` `EXECUTE`を複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   トランザクションによって使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [エキシウム](https://github.com/ekexium)
    -   スライスの浅いコピーを使用せずに列を整理すると TiDB がpanicを起こす可能性がある問題を修正[＃52768](https://github.com/pingcap/tidb/issues/52768) @ [ウィノロス](https://github.com/winoros)
    -   ウィンドウ関数を含むSQLバインディングが場合によっては有効にならない可能性がある問題を修正[＃55981](https://github.com/pingcap/tidb/issues/55981) @ [ウィノロス](https://github.com/winoros)
    -   インデックスデータ[＃47115](https://github.com/pingcap/tidb/issues/47115) @ [ジグアン](https://github.com/zyguan)を解析するときに TiDB がpanicになる可能性がある問題を修正しました
    -   起動時に統計をロードするときに TiDB が GC によるエラーを報告する可能性がある問題を修正[＃53592](https://github.com/pingcap/tidb/issues/53592) @ [あなた06](https://github.com/you06)
    -   DML文にネストされた生成列[＃53967](https://github.com/pingcap/tidb/issues/53967) @ [翻訳:](https://github.com/wjhuang2016)が含まれている場合にエラーが発生する問題を修正
    -   常に`true` [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [エルサ0520](https://github.com/elsa0520)の述語を持つ`SHOW ERRORS`ステートメントを実行すると TiDB がパニックになる問題を修正しました。
    -   特定の状況下でプラン キャッシュを使用する際に、メタデータ ロックを不適切に使用すると異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   インデックス追加[＃55808](https://github.com/pingcap/tidb/issues/55808) @ [ランス6716](https://github.com/lance6716)中の再試行によって発生するデータ インデックスの不整合の問題を修正
    -   列の不安定な一意の ID により、 `UPDATE`ステートメントがエラー[＃53236](https://github.com/pingcap/tidb/issues/53236) @ [ウィノロス](https://github.com/winoros)を返す可能性がある問題を修正しました。
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panic[＃53540](https://github.com/pingcap/tidb/issues/53540) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   `RECOVER TABLE BY JOB JOB_ID;`実行すると TiDB がpanicになる可能性がある問題を修正[＃55113](https://github.com/pingcap/tidb/issues/55113) @ [クレイジーcs520](https://github.com/crazycs520)
    -   分散実行フレームワーク[＃48680](https://github.com/pingcap/tidb/issues/48680) @ [ランス6716](https://github.com/lance6716)で PD メンバーを変更した後に`ADD INDEX`実行が失敗する可能性がある問題を修正
    -   2人のDDL所有者が同時に存在する可能性がある問題を修正[＃54689](https://github.com/pingcap/tidb/issues/54689) @ [ジョッカウ](https://github.com/joccau)
    -   `ADD INDEX`の実行中に TiDB のローリング再起動を行うと、インデックス追加操作が失敗する可能性がある問題を修正[＃52805](https://github.com/pingcap/tidb/issues/52805) @ [タンジェンタ](https://github.com/tangenta)
    -   `LOAD DATA ... REPLACE INTO`操作でデータの不整合が発生する問題を修正[＃56408](https://github.com/pingcap/tidb/issues/56408) @ [ふーふー](https://github.com/fzzf678)
    -   `IMPORT INTO`ステートメント[＃56476](https://github.com/pingcap/tidb/issues/56476) @ [D3ハンター](https://github.com/D3Hunter)を使用してデータをインポートした後、 `AUTO_INCREMENT`フィールドが正しく設定されない問題を修正しました。
    -   TiDB がチェックポイント[＃53009](https://github.com/pingcap/tidb/issues/53009) @ [ランス6716](https://github.com/lance6716)から復元する前にローカル ファイルの存在をチェックしない問題を修正しました。
    -   DM スキーマ トラッカーがデフォルトの長さ[＃55138](https://github.com/pingcap/tidb/issues/55138) @ [ランス6716](https://github.com/lance6716)より長いインデックスを作成できない問題を修正しました。
    -   `ALTER TABLE` `AUTO_INCREMENT`フィールドを正しく処理しない問題を修正[＃47899](https://github.com/pingcap/tidb/issues/47899) @ [D3ハンター](https://github.com/D3Hunter)
    -   解放されていないセッションリソースがメモリリークを引き起こす可能性がある問題を修正[＃56271](https://github.com/pingcap/tidb/issues/56271) @ [ランス6716](https://github.com/lance6716)
    -   浮動小数点数または整数オーバーフローがプランキャッシュ[＃46538](https://github.com/pingcap/tidb/issues/46538) @ [ホーキングレイ](https://github.com/hawkingrei)に影響する問題を修正
    -   `IndexLookUp`演算子のメモリの一部が追跡されない問題を修正[＃56440](https://github.com/pingcap/tidb/issues/56440) @ [うわー](https://github.com/wshwsh12)
    -   古い読み取りが読み取り操作のタイムスタンプを厳密に検証しない問題を修正しました。その結果、TSO と実際の物理時間[＃56809](https://github.com/pingcap/tidb/issues/56809) @ [ミョンケミンタ](https://github.com/MyonKeminta)の間にオフセットが存在する場合に、トランザクションの一貫性にわずかながら影響が出る可能性があります。
    -   storageエンジン[＃56402](https://github.com/pingcap/tidb/issues/56402) @ [ヤンケオ](https://github.com/YangKeao)として TiKV が選択されていない場合に TTL が失敗する可能性がある問題を修正しました
    -   書き込み競合が発生したときに TTL タスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [ヤンケオ](https://github.com/YangKeao)
    -   科学表記法で大きすぎる数値を挿入するとエラーが発生する問題を修正`ERROR 1264 (22003)`し、動作を MySQL [＃47787](https://github.com/pingcap/tidb/issues/47787) @ [lcwangchao](https://github.com/lcwangchao)と一致させました。
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   `INSERT ... ON DUPLICATE KEY`ステートメントが`mysql_insert_id` [＃55965](https://github.com/pingcap/tidb/issues/55965) @ [天菜まお](https://github.com/tiancaiamao)と互換性がない問題を修正
    -   SQL が実行プラン[＃50988](https://github.com/pingcap/tidb/issues/50988) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を構築できない場合に監査ログのフィルタリングが有効にならない問題を修正しました
    -   v6.5 から v7.5 以降にアップグレードされたクラスターで、既存の TTL タスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   `CAST`関数が文字セット[＃55677](https://github.com/pingcap/tidb/issues/55677) @ [定義2014](https://github.com/Defined2014)の明示的な設定をサポートしていない問題を修正
    -   `ADD INDEX` [＃56930](https://github.com/pingcap/tidb/issues/56930) @ [ふーふー](https://github.com/fzzf678)を実行するときに TiDB がインデックスの長さ制限をチェックしない問題を修正しました

-   ティクヴ

    -   `RawKvMaxTimestampNotSynced`エラーを追加し、 `errorpb.Error.max_ts_not_synced`に詳細なエラー情報をログに記録し、このエラーが発生したときに`must_raw_put`操作の再試行メカニズムを追加します[＃16789](https://github.com/tikv/tikv/issues/16789) @ [ピンギュ](https://github.com/pingyu)
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるトラフィック制御の問題を修正[＃17304](https://github.com/tikv/tikv/issues/17304) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   読み取りスレッドがRaft Engine[＃17383](https://github.com/tikv/tikv/issues/17383) @ [リクササシネーター](https://github.com/LykxSassinator)のMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   TiDB Lightningによってインポートされた SST ファイルが TiKV の再起動後に失われる問題を修正[＃15912](https://github.com/tikv/tikv/issues/15912) @ [ランス6716](https://github.com/lance6716)
    -   削除された`sst_importer` SST ファイル[＃15053](https://github.com/tikv/tikv/issues/15053) @ [ランス6716](https://github.com/lance6716)を取り込むことで TiKV がpanicになる可能性がある問題を修正
    -   TiKV インスタンスに多数のリージョンがある場合、データ インポート[＃16229](https://github.com/tikv/tikv/issues/16229) @ [スペードA-タン](https://github.com/SpadeA-Tang)中に TiKV が OOM になる可能性がある問題を修正しました。
    -   ブルームフィルタが以前のバージョン（v7.1以前）とそれ以降のバージョン[＃17272](https://github.com/tikv/tikv/issues/17272) @ [v01dスター](https://github.com/v01dstar)の間で互換性がない問題を修正しました
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB [＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)に送信されるメッセージには反映されない問題を修正しました。
    -   不安定なテストケースの問題を修正し、各テストが独立した一時ディレクトリを使用するようにして、オンライン構成の変更が他のテストケースに影響しないようにします[＃16871](https://github.com/tikv/tikv/issues/16871) @ [栄光](https://github.com/glorv)
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出に過度の負荷がかかり、TiKV OOM 問題[＃17394](https://github.com/tikv/tikv/issues/17394) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   `DECIMAL`型の小数部が[＃16913](https://github.com/tikv/tikv/issues/16913) @ [ゲンリキ](https://github.com/gengliqi)場合に正しくない問題を修正
    -   クエリ内の`CONV()`関数が数値システム変換中にオーバーフローし、TiKVpanic[＃16969](https://github.com/tikv/tikv/issues/16969) @ [ゲンリキ](https://github.com/gengliqi)が発生する問題を修正しました。
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。
    -   同時実行性の高いコプロセッサー要求により TiKV OOM [＃16653](https://github.com/tikv/tikv/issues/16653) @ [金星の上](https://github.com/overvenus)が発生する可能性がある問題を修正
    -   マスターキーがキー管理サービス (KMS) [＃17410](https://github.com/tikv/tikv/issues/17410) @ [いいえ](https://github.com/hhwyt)に保存されている場合にマスターキーのローテーションが妨げられる問題を修正しました
    -   tikv-ctlの`raft region`コマンドの出力にリージョンステータス情報[＃17037](https://github.com/tikv/tikv/issues/17037) @ [栄光](https://github.com/glorv)が含まれていない問題を修正
    -   Grafana の TiKV パネルの**ストレージ非同期書き込み期間**監視メトリックが不正確であるという問題を修正[＃17579](https://github.com/tikv/tikv/issues/17579) @ [金星の上](https://github.com/overvenus)
    -   TiKV がブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)

-   PD

    -   ラベル統計[＃8700](https://github.com/tikv/pd/issues/8700) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   リソース グループが過剰なログ[＃8159](https://github.com/tikv/pd/issues/8159) @ [ノルーシュ](https://github.com/nolouch)を出力する問題を修正しました
    -   乱数ジェネレータ[＃8674](https://github.com/tikv/pd/issues/8674) @ [rleungx](https://github.com/rleungx)の頻繁な作成によって発生するパフォーマンスジッターの問題を修正しました
    -   リージョン統計[＃8710](https://github.com/tikv/pd/issues/8710) @ [rleungx](https://github.com/rleungx)のメモリリーク問題を修正
    -   ホットスポット キャッシュ[＃8698](https://github.com/tikv/pd/issues/8698) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   同じストアID [＃8756](https://github.com/tikv/pd/issues/8756) @ [ok江](https://github.com/okJiang)で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正
    -   設定ファイル経由でログレベルを変更しても反映されない問題を修正[＃8117](https://github.com/tikv/pd/issues/8117) @ [rleungx](https://github.com/rleungx)
    -   同時実行性が高い場合にリソース グループがリソースの使用を効果的に制限できない問題を修正[＃8435](https://github.com/tikv/pd/issues/8435) @ [ノルーシュ](https://github.com/nolouch)
    -   オペレータチェック[＃8263](https://github.com/tikv/pd/issues/8263) @ [翻訳者](https://github.com/lhy1024)中に PD が遭遇するデータ競合問題を修正
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [ノルーシュ](https://github.com/nolouch)
    -   一部のログが編集されていない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   ロールをリソース グループ[＃54417](https://github.com/pingcap/tidb/issues/54417) @ [じゃがいも](https://github.com/JmPotato)にバインドするときにエラーが報告されない問題を修正しました
    -   多数のリージョンが存在する場合にPDのリージョンAPIをリクエストできない問題を修正[＃55872](https://github.com/pingcap/tidb/issues/55872) @ [rleungx](https://github.com/rleungx)
    -   リソース グループ クエリ[＃8217](https://github.com/tikv/pd/issues/8217) @ [ノルーシュ](https://github.com/nolouch)をキャンセルするときに再試行が大量に発生する問題を修正しました
    -   使用前に暗号化マネージャーが初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [rleungx](https://github.com/rleungx)
    -   PDの`Filter target`監視メトリックが散布範囲情報を提供しない問題を修正[＃8125](https://github.com/tikv/pd/issues/8125) @ [ヒューシャープ](https://github.com/HuSharp)
    -   リソース グループ[＃8267](https://github.com/tikv/pd/issues/8267) @ [ヒューシャープ](https://github.com/HuSharp)のデータ競合問題を修正
    -   TiKV 構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB 未満の値に設定すると PDpanic[＃8323](https://github.com/tikv/pd/issues/8323) @ [じゃがいも](https://github.com/JmPotato)が発生する問題を修正しました。
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが使用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値[＃7346](https://github.com/tikv/pd/issues/7346) @ [グオシャオゲ](https://github.com/guo-shaoge)より少なくなる問題を修正しました。
    -   配置ルール[＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)を使用すると、ダウンしたピアが回復しない可能性がある問題を修正しました。

-   TiFlash

    -   クラスターを v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードするときに、 TiFlashメタデータが破損してプロセスがpanicになる可能性がある問題を修正しました[＃9039](https://github.com/pingcap/tiflash/issues/9039) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [ジンヘリン](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になっている場合に一部のクエリでエラーが報告される問題を修正[＃9472](https://github.com/pingcap/tiflash/issues/9472) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [風の話し手](https://github.com/windtalker)にプッシュダウンされる問題を修正しました
    -   TiFlashで SSL 証明書構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashと PD 間のネットワーク パーティション (ネットワーク切断) により読み取り要求タイムアウト エラーが発生する可能性がある問題を修正[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   BRまたはTiDB Lightning [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [ジンヘリン](https://github.com/JinheLin)経由でデータをインポートした後、FastScan モードで多数の重複行が読み取られる可能性がある問題を修正しました。
    -   テーブルに無効な文字[＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を含むデフォルト値を持つビット型列が含まれている場合に、 TiFlash がテーブル スキーマを解析できない問題を修正しました。
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [ジンヘリン](https://github.com/JinheLin)
    -   データベース間で`ALTER TABLE ... EXCHANGE PARTITION`実行した後にTiFlash がスキーマの同期に失敗する可能性がある問題を修正[＃7296](https://github.com/pingcap/tiflash/issues/7296) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   データベースが作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロッツ](https://github.com/solotzg)
    -   同時実行性の高い読み取りシナリオでTiFlash が一時的に誤った結果を返す可能性がある問題を修正[＃8845](https://github.com/pingcap/tiflash/issues/8845) @ [ジンヘリン](https://github.com/JinheLin)
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash をクラッシュさせる可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [うわー](https://github.com/wshwsh12)
    -   クラスタ内で長期間にわたって`EXCHANGE PARTITION`と`DROP TABLE`操作を頻繁に実行すると、 TiFlashテーブル メタデータのレプリケーションが遅くなり、クエリ パフォーマンスが低下する可能性がある問題を修正しました[＃9227](https://github.com/pingcap/tiflash/issues/9227) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   空のキー範囲を持つクエリがTiFlash上で読み取りタスクを正しく生成できず、 TiFlashクエリ[＃9108](https://github.com/pingcap/tiflash/issues/9108) @ [ジンヘリン](https://github.com/JinheLin)がブロックされる可能性がある問題を修正しました。
    -   特定のケースで`CAST AS DECIMAL`関数の結果の符号が正しくない問題を修正[＃9301](https://github.com/pingcap/tiflash/issues/9301) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `SUBSTRING()`関数が特定の整数型の`pos`番目と`len`引数をサポートせず、クエリ エラー[＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [ゲンリキ](https://github.com/gengliqi)が発生する問題を修正しました。
    -   大きなテーブルで`DROP TABLE`実行するとTiFlash OOM [＃9437](https://github.com/pingcap/tiflash/issues/9437) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が発生する可能性がある問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   BR統合テスト ケースが不安定になる問題を修正し、スナップショットまたはログ バックアップ ファイルの破損をシミュレートする新しいテスト ケースを追加します[＃53835](https://github.com/pingcap/tidb/issues/53835) @ [リーヴルス](https://github.com/Leavrth)
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア[＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3ポインター](https://github.com/3pointer)中に正しく回復されない可能性がある問題を修正しました。
        -   ログ バックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD [＃17316](https://github.com/tikv/tikv/issues/17316) @ [リーヴルス](https://github.com/Leavrth)で適切にクリアされない問題を修正しました。
        -   アドバンサー所有者の移行[＃53561](https://github.com/pingcap/tidb/issues/53561) @ [リドリス](https://github.com/RidRisR)後にログバックアップが一時停止される可能性がある問題を修正
        -   増分バックアップ[＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3ポインター](https://github.com/3pointer)中の DDL ジョブのスキャンにおける非効率性の問題を修正
        -   リージョンリーダー[＃17168](https://github.com/tikv/tikv/issues/17168) @ [リーヴルス](https://github.com/Leavrth)シークの中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。
        -   ログバックアップが有効になっている場合にBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [リドリス](https://github.com/RidRisR)
        -   復元プロセス中に複数のネストされた再試行が原因でBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [リドリス](https://github.com/RidRisR)
        -   PD [＃17020](https://github.com/tikv/tikv/issues/17020) @ [ユジュンセン](https://github.com/YuJuncen)へのネットワーク接続が不安定な状態で一時停止中のログ バックアップ タスクを再開すると TiKV がpanicになる可能性がある問題を修正しました。
        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [リーヴルス](https://github.com/Leavrth)
        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)
        -   BR を使用してデータを復元する場合、または物理インポート モードでTiDB Lightning を使用してデータをインポートする場合に、PD から取得されたリージョンにLeaderがない問題を修正しました[＃51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @ [リーヴルス](https://github.com/Leavrth)
        -   PDリーダーの転送により、データ[＃53724](https://github.com/pingcap/tidb/issues/53724) @ [リーヴルス](https://github.com/Leavrth)を復元するときにBRがpanicになる可能性がある問題を修正しました。
        -   ログバックアップタスクを一時停止、停止、再構築した後、タスクの状態は正常であるが、チェックポイントが[＃53047](https://github.com/pingcap/tidb/issues/53047) @ [リドリス](https://github.com/RidRisR)に進まない問題を修正しました。
        -   ログバックアップが残留ロックをすぐに解決できず、チェックポイントが[＃57134](https://github.com/pingcap/tidb/issues/57134) @ [3ポインター](https://github.com/3pointer)に進まない問題を修正しました。

    -   ティCDC

        -   `TIMEZONE`種類のデフォルト値が正しいタイムゾーン[＃10931](https://github.com/pingcap/tiflow/issues/10931) @ [3エースショーハンド](https://github.com/3AceShowHand)に従って設定されない問題を修正
        -   ソーターモジュールがディスクデータ[＃10853](https://github.com/pingcap/tiflow/issues/10853) @ [ヒック](https://github.com/hicqu)を読み取るときに TiCDC がpanicになる可能性がある問題を修正しました。
        -   マルチノード環境で大量の`UPDATE`操作を実行する際にChangefeedを繰り返し再起動するとデータの不整合が発生する可能性がある問題を修正[＃11219](https://github.com/pingcap/tiflow/issues/11219) @ [リデズ](https://github.com/lidezhu)
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように構成した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に複製しない問題を修正しました。
        -   Kafka [＃9855](https://github.com/pingcap/tiflow/issues/9855) @ [ヒック](https://github.com/hicqu)にデータを複製するときに TiCDC が停止する可能性がある問題を修正しました
        -   `DROP PRIMARY KEY`と`DROP UNIQUE KEY`ステートメントが正しく複製されない問題を修正[＃10890](https://github.com/pingcap/tiflow/issues/10890) @ [アズドンメン](https://github.com/asddongmen)
        -   下流の Kafka にアクセスできない場合にプロセッサ モジュールが停止する可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   DM が`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーション エラー[＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。
        -   複数の DM マスター ノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   `go-mysql` [＃11041](https://github.com/pingcap/tiflow/issues/11041) @ [D3ハンター](https://github.com/D3Hunter)にアップグレードして接続ブロックの問題を修正
        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正
        -   LIST パーティション テーブル[＃54760](https://github.com/pingcap/tidb/issues/54760) @ [ランス6716](https://github.com/lance6716)の`ALTER TABLE ... DROP PARTITION`ステートメントを複製するときに DM がエラーを返す問題を修正しました。

    -   TiDB Lightning

        -   TiDB Lightning がTiKV [＃56114](https://github.com/pingcap/tidb/issues/56114) @ [フィシュウ](https://github.com/fishiu)から送信されたサイズ超過のメッセージを受信できない問題を修正しました
        -   TiDB Lightning [＃15003](https://github.com/tikv/tikv/issues/15003) [＃47694](https://github.com/pingcap/tidb/issues/47694) @ [ランス6716](https://github.com/lance6716)のインポート モードを無効にした後にデータをインポートすると TiKV データが破損する可能性がある問題を修正しました
        -   TiDB Lightning [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [ランス6716](https://github.com/lance6716)使用してデータインポート中にトランザクションの競合が発生する問題を修正
        -   EBS BRが[＃49517](https://github.com/pingcap/tidb/issues/49517) @ [ミッタルリシャブ](https://github.com/mittalrishabh)で実行されているときにTiDB Lightningがデータのインポートに失敗する可能性がある問題を修正しました
        -   2 つのインスタンスが同時に並列インポート タスクを開始し、同じタスク ID [＃55384](https://github.com/pingcap/tidb/issues/55384) @ [杉本栄](https://github.com/ei-sugimoto)が割り当てられている場合に、 TiDB Lightning が`verify allocator base failed`エラーを報告する問題を修正しました。
        -   PDLeaderを強制終了すると、 TiDB Lightning がデータ インポート[＃50501](https://github.com/pingcap/tidb/issues/50501) @ [リーヴルス](https://github.com/Leavrth)中に`invalid store ID 0`エラーを報告する問題を修正しました。

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [タンジェンタ](https://github.com/tangenta)

    -   TiDBBinlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`の実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [タンジェンタ](https://github.com/tangenta)
