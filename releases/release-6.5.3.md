---
title: TiDB 6.5.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.3.
---

# TiDB 6.5.3 リリースノート {#tidb-6-5-3-release-notes}

発売日：2023年6月14日

TiDB バージョン: 6.5.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.3#version-list)

## 改善点 {#improvements}

-   TiDB

    -   配置ルール[#43070](https://github.com/pingcap/tidb/issues/43070) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を使用してパーティション化テーブルの`TRUNCATE`のパフォーマンスを向上させる
    -   ロック[#43659](https://github.com/pingcap/tidb/issues/43659) @ [あなた06](https://github.com/you06)を解決した後の無効なステイル読み取りの再試行を回避します。
    -   ステイル読み取り で`DataIsNotReady`エラー[#765](https://github.com/tikv/client-go/pull/765) @ [テーマ](https://github.com/Tema)が発生した場合、リーダー読み取りを使用してレイテンシーを短縮します。
    -   ステイル読み取り [#43325](https://github.com/pingcap/tidb/issues/43325) @ [あなた06](https://github.com/you06)を使用する場合、ヒット率とトラフィックを追跡するために`Stale Read OPS`および`Stale Read MBps`メトリクスを追加します。

-   TiKV

    -   gzip を使用して`check_leader`リクエスト[#14839](https://github.com/tikv/tikv/issues/14839) @ [cfzjywxk](https://github.com/cfzjywxk)を圧縮することでトラフィックを削減します。

-   PD

    -   他のリクエストの影響を防ぐために、PD リーダーの選出には別の gRPC 接続を使用します[#6403](https://github.com/tikv/pd/issues/6403) @ [ルルンクス](https://github.com/rleungx)

-   ツール

    -   TiCDC

        -   TiCDC が DDL を処理する方法を最適化して、DDL が他の無関係な DML イベントの使用をブロックしないようにし、メモリ使用量を削減します[#8106](https://github.com/pingcap/tiflow/issues/8106) @ [東門](https://github.com/asddongmen)
        -   Decoder インターフェイスを最適化し、新しいメソッドを追加します`AddKeyValue` [#8861](https://github.com/pingcap/tiflow/issues/8861) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   オブジェクトstorage[#8890](https://github.com/pingcap/tiflow/issues/8890) @ [CharlesCheung96](https://github.com/CharlesCheung96)にデータをレプリケートするシナリオで DDL イベントが発生したときにディレクトリ構造を最適化します。
        -   Kafka-on-Pulsar ダウンストリーム[#8892](https://github.com/pingcap/tiflow/issues/8892) @ [こんにちはラスティン](https://github.com/hi-rustin)へのデータのレプリケーションのサポート
        -   Kafka [#8865](https://github.com/pingcap/tiflow/issues/8865) @ [こんにちはラスティン](https://github.com/hi-rustin)にデータをレプリケートする際の検証のための OAuth プロトコルの使用のサポート
        -   TiCDC が Avro または CSV プロトコルを使用してデータ レプリケーション中に`UPDATE`ステートメントを処理する方法を最適化します。これは、 `UPDATE` `DELETE`と`INSERT`ステートメントに分割することで、 `DELETE`ステートメント[#9086](https://github.com/pingcap/tiflow/issues/9086) @ [3エースショーハンド](https://github.com/3AceShowHand)から古い値を取得できるようにします。
        -   TLS [#8867](https://github.com/pingcap/tiflow/issues/8867) @ [こんにちはラスティン](https://github.com/hi-rustin)を有効にするシナリオで認証アルゴリズムを設定するかどうかを制御する構成項目`insecure-skip-verify`を追加します。
        -   DDL レプリケーション操作を最適化して、ダウンストリームレイテンシー[#8686](https://github.com/pingcap/tiflow/issues/8686) @ [こんにちはラスティン](https://github.com/hi-rustin)に対する DDL 操作の影響を軽減します。
        -   TiCDC レプリケーション タスクが失敗した場合のアップストリームの GC TLS 設定方法を最適化します[#8403](https://github.com/pingcap/tiflow/issues/8403) @ [チャールズジェン44](https://github.com/charleszheng44)

    -   TiDBBinlog

        -   テーブル情報の取得方法を最適化し、 Drainer [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @ [リチュンジュ](https://github.com/lichunzhu)の初期化時間とメモリ使用量を削減します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `min, max`クエリ結果が正しくない問題を修正[#43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   ウィンドウ関数をTiFlash [#43922](https://github.com/pingcap/tidb/issues/43922) @ [ゲンリキ](https://github.com/gengliqi)にプッシュダウンするときに実行プランが正しくない問題を修正
    -   CTE を使用したクエリにより TiDB がハングする問題を修正[#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `AES_DECRYPT`式[#43063](https://github.com/pingcap/tidb/issues/43063) @ [ルクワンチャオ](https://github.com/lcwangchao)を使用すると、SQL ステートメントで`runtime error: index out of range`エラーが報告される問題を修正します。
    -   `SHOW PROCESSLIST`ステートメントがサブクエリ時間の長いステートメント[#40851](https://github.com/pingcap/tidb/issues/40851) @ [クレイジークス520](https://github.com/crazycs520)のトランザクションの TxnStart を表示できない問題を修正
    -   PD 分離により実行中の DDL [#44014](https://github.com/pingcap/tidb/issues/44014) [#43755](https://github.com/pingcap/tidb/issues/43755) [#44267](https://github.com/pingcap/tidb/issues/44267) @ [wjhuang2016](https://github.com/wjhuang2016)がブロックされる可能性がある問題を修正
    -   `UNION` [#42563](https://github.com/pingcap/tidb/issues/42563) @ [ルクワンチャオ](https://github.com/lcwangchao)を使用してユニオン ビューと一時テーブルをクエリするときに発生する TiDBpanicの問題を修正しました。
    -   パーティション化されたテーブルの配置ルールの動作の問題を修正し、削除されたパーティションの配置ルールを正しく設定してリサイクルできるようにします[#44116](https://github.com/pingcap/tidb/issues/44116) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   パーティションテーブルのパーティションを切り捨てると、パーティションの配置ルールが無効になる可能性がある問題を修正します[#44031](https://github.com/pingcap/tidb/issues/44031) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   テーブルの名前変更[#43338](https://github.com/pingcap/tidb/issues/43338) @ [タンジェンタ](https://github.com/tangenta)中に TiCDC が行の変更の一部を失う可能性がある問題を修正
    -   BR [#43725](https://github.com/pingcap/tidb/issues/43725) @ [タンジェンタ](https://github.com/tangenta)を使用してテーブルをインポートした後に DDL ジョブ履歴が失われる問題を修正
    -   `JSON_OBJECT`が場合によってはエラーを報告する場合がある問題を修正[#39806](https://github.com/pingcap/tidb/issues/39806) @ [ヤンケオ](https://github.com/YangKeao)
    -   IPv6 環境[#43286](https://github.com/pingcap/tidb/issues/43286) @ [定義2014](https://github.com/Defined2014)でクラスターが一部のシステム ビューをクエリできない問題を修正
    -   PDメンバーアドレスが変更されると、 `AUTO_INCREMENT`カラムへのID割り当てが長時間ブロックされる問題を修正[#42643](https://github.com/pingcap/tidb/issues/42643) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   配置ルールのリサイクル中に TiDB が重複したリクエストを PD に送信し、PD ログ[#33069](https://github.com/pingcap/tidb/issues/33069) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に多数の`full config reset`エントリが発生する問題を修正します。
    -   `SHOW PRIVILEGES`ステートメントが不完全な権限リスト[#40591](https://github.com/pingcap/tidb/issues/40591) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を返す問題を修正します。
    -   `ADMIN SHOW DDL JOBS LIMIT`が間違った結果[#42298](https://github.com/pingcap/tidb/issues/42298) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を返す問題を修正
    -   パスワードの複雑さのチェックが有効になっている場合に`tidb_auth_token`ユーザーの作成に失敗する問題を修正します[#44098](https://github.com/pingcap/tidb/issues/44098) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   動的プルーニング モード[#43686](https://github.com/pingcap/tidb/issues/43686) @ [むじょん](https://github.com/mjonss)での内部結合中にパーティションが見つからない問題を修正
    -   パーティションテーブル[#41118](https://github.com/pingcap/tidb/issues/41118) @ [むじょん](https://github.com/mjonss)で`MODIFY COLUMN`実行すると`Data Truncated`警告が発生する問題を修正
    -   IPv6 環境[#43260](https://github.com/pingcap/tidb/issues/43260) @ [ネクスター](https://github.com/nexustar)で誤った TiDB アドレスが表示される問題を修正
    -   述語[#43645](https://github.com/pingcap/tidb/issues/43645) @ [ウィノロス](https://github.com/winoros)をプッシュダウンすると CTE の結果が正しくなくなる問題を修正
    -   非相関サブクエリ[#44051](https://github.com/pingcap/tidb/issues/44051) @ [ウィノロス](https://github.com/winoros)を含むステートメントで共通テーブル式 (CTE) を使用すると、誤った結果が返される可能性がある問題を修正します。
    -   結合したテーブルの再配置により不正な外部結合結果[#44314](https://github.com/pingcap/tidb/issues/44314) @ [アイリンキッド](https://github.com/AilinKid)が発生する可能性がある問題を修正
    -   極端な場合、悲観的トランザクションの最初のステートメントが再試行されるときに、このトランザクションのロックを解決するとトランザクションの正確性に影響を与える可能性があるという問題を修正します[#42937](https://github.com/pingcap/tidb/issues/42937) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   まれに、GC がロック[#43243](https://github.com/pingcap/tidb/issues/43243) @ [ミョンケミンタ](https://github.com/MyonKeminta)を解決するときに、悲観的トランザクションの残存する悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正します。
    -   `batch cop`の実行時のスキャン詳細情報が不正確になる場合がある問題を修正[#41582](https://github.com/pingcap/tidb/issues/41582) @ [あなた06](https://github.com/you06)
    -   ステイル読み取りと`PREPARE`ステートメントが同時に使用されると、TiDB がデータ更新を読み取れない問題を修正[#43044](https://github.com/pingcap/tidb/issues/43044) @ [あなた06](https://github.com/you06)
    -   `LOAD DATA`ステートメント[#43849](https://github.com/pingcap/tidb/issues/43849) @ [あなた06](https://github.com/you06)を実行すると、誤って`assertion failed`エラーが報告される可能性がある問題を修正
    -   ステイル読み取り [#43365](https://github.com/pingcap/tidb/issues/43365) @ [あなた06](https://github.com/you06)の使用中に`region data not ready`エラーが発生した場合、コプロセッサーがリーダーにフォールバックできない問題を修正します。

-   TiKV

    -   TiKV ノードに障害が発生したときに、対応するリージョンのピアが誤って休止状態になる問題を修正します[#14547](https://github.com/tikv/tikv/issues/14547) @ [ひっくり返る](https://github.com/hicqu)
    -   継続的プロファイリング[#14224](https://github.com/tikv/tikv/issues/14224) @ [タボキー](https://github.com/tabokie)でのファイル ハンドル リークの問題を修正
    -   PD クラッシュにより PITR が続行できない可能性がある問題を修正[#14184](https://github.com/tikv/tikv/issues/14184) @ [ユジュンセン](https://github.com/YuJuncen)
    -   暗号化キー ID の競合により古いキー[#14585](https://github.com/tikv/tikv/issues/14585) @ [タボキー](https://github.com/tabokie)が削除される可能性がある問題を修正
    -   自動コミットとポイント取得レプリカ読み取りにより線形化可能性[#14715](https://github.com/tikv/tikv/issues/14715) @ [cfzjywxk](https://github.com/cfzjywxk)が壊れる可能性がある問題を修正
    -   クラスターが以前のバージョンから v6.5 以降のバージョン[#14780](https://github.com/tikv/tikv/issues/14780) @ [ミョンケミンタ](https://github.com/MyonKeminta)にアップグレードされるときに、蓄積されたロック レコードによって引き起こされるパフォーマンス低下の問題を修正します。
    -   TiDB Lightning がSST ファイル漏洩を引き起こす可能性がある問題を修正[#14745](https://github.com/tikv/tikv/issues/14745) @ [ユジュンセン](https://github.com/YuJuncen)
    -   TiKV の起動失敗の原因となる可能性がある、暗号化キーと raft ログ ファイルの削除の間の潜在的な競合を修正します[#14761](https://github.com/tikv/tikv/issues/14761) @ [コナー1996](https://github.com/Connor1996)

-   TiFlash

    -   リージョン転送[#7519](https://github.com/pingcap/tiflash/issues/7519) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)中のパーティション TableScan オペレーターのパフォーマンス低下の問題を修正
    -   `GENERATED`タイプ フィールドが`TIMESTAMP`または`TIME`タイプ[#7468](https://github.com/pingcap/tiflash/issues/7468) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)とともに存在する場合、 TiFlashクエリでエラーが報告される可能性がある問題を修正します。
    -   大規模な更新トランザクションによってTiFlashが繰り返しエラーを報告し、 [#7316](https://github.com/pingcap/tiflash/issues/7316) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を再起動する可能性がある問題を修正します。
    -   `INSERT SELECT`ステートメント[#7348](https://github.com/pingcap/tiflash/issues/7348) @ [ウィンドトーカー](https://github.com/windtalker)でTiFlashからデータを読み取るときに、「Truncate error Cast Decimal as Decimal」エラーが発生する問題を修正
    -   結合ビルド側のデータが非常に大きく、小さな文字列型の列[#7416](https://github.com/pingcap/tiflash/issues/7416) @ [イービン87](https://github.com/yibin87)が多数含まれている場合、クエリが必要以上のメモリを消費する可能性がある問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ失敗時のBRのエラー メッセージ「ロック タイムアウトの解決」が誤解を招き、実際のエラー情報が隠蔽される問題を修正[#43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   テーブル[#7872](https://github.com/pingcap/tiflow/issues/7872) @ [スドジ](https://github.com/sdojjy)が 50,000 個もある場合に発生する可能性がある OOM の問題を修正します。
        -   アップストリームの TiDB [#8561](https://github.com/pingcap/tiflow/issues/8561) @ [オーバーヴィーナス](https://github.com/overvenus)で OOM が発生したときに TiCDC がスタックする問題を修正
        -   ネットワーク分離や PD オーナー ノードの再起動など、PD が失敗したときに TiCDC がスタックする問題を修正[#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @ [東門](https://github.com/asddongmen)
        -   TiCDC タイムゾーン設定[#8798](https://github.com/pingcap/tiflow/issues/8798) @ [こんにちはラスティン](https://github.com/hi-rustin)の問題を修正
        -   上流の TiKV ノードの 1 つがクラッシュしたときにチェックポイント ラグが増加する問題を修正します[#8858](https://github.com/pingcap/tiflow/issues/8858) @ [ひっくり返る](https://github.com/hicqu)
        -   ダウンストリーム MySQL にデータをレプリケートするときに、アップストリーム TiDB [#8040](https://github.com/pingcap/tiflow/issues/8040) @ [東門](https://github.com/asddongmen)で`FLASHBACK CLUSTER TO TIMESTAMP`ステートメントが実行された後にレプリケーション エラーが発生する問題を修正します。
        -   オブジェクトstorageにデータをレプリケートするときに、アップストリームの`EXCHANGE PARTITION`オペレーションがダウンストリーム[#8914](https://github.com/pingcap/tiflow/issues/8914) @ [CharlesCheung96](https://github.com/CharlesCheung96)に適切にレプリケートできない問題を修正します。
        -   一部の特殊なシナリオ[#8974](https://github.com/pingcap/tiflow/issues/8974) @ [ひっくり返る](https://github.com/hicqu)におけるソーターコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正します。
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームで過度のワークロードが発生する問題を修正します[#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   Kafka メッセージのサイズ超過によりレプリケーション エラーが発生した場合、メッセージ本文がログ[#9031](https://github.com/pingcap/tiflow/issues/9031) @ [ダラエス](https://github.com/darraes)に記録される問題を修正
        -   ダウンストリーム Kafka シンクがローリング再起動されるときに発生する TiCDC ノードpanicを修正します[#9023](https://github.com/pingcap/tiflow/issues/9023) @ [東門](https://github.com/asddongmen)
        -   データをstorageサービスにレプリケートするときに、ダウンストリーム DDL ステートメントに対応する JSON ファイルにテーブル フィールド[#9066](https://github.com/pingcap/tiflow/issues/9066) @ [CharlesCheung96](https://github.com/CharlesCheung96)のデフォルト値が記録されない問題を修正します。

    -   TiDB Lightning

        -   ワイドテーブル[#43728](https://github.com/pingcap/tidb/issues/43728) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときに OOM が発生する可能性がある問題を修正
        -   大量のデータをインポートする場合の`write to tikv with no leader returned`の問題を修正[#43055](https://github.com/pingcap/tidb/issues/43055) @ [ランス6716](https://github.com/lance6716)
        -   データ ファイル[#40400](https://github.com/pingcap/tidb/issues/40400) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)に閉じられていない区切り文字がある場合に発生する可能性がある OOM の問題を修正します。
        -   データのインポート中に`unknown RPC`エラーが発生した場合の再試行メカニズムを追加[#43291](https://github.com/pingcap/tidb/issues/43291) @ [D3ハンター](https://github.com/D3Hunter)

    -   TiDBBinlog

        -   `CANCELED` DDL ステートメント[#1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [オクジャン](https://github.com/okJiang)が発生したときに TiDB Binlogがエラーを報告する問題を修正
