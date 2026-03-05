---
title: TiDB 6.5.3 Release Notes
summary: TiDB 6.5.3 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.3 リリースノート {#tidb-6-5-3-release-notes}

発売日：2023年6月14日

TiDB バージョン: 6.5.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

### 行動の変化 {#behavior-changes}

-   更新イベントの処理中に、イベント内の主キーまたはnull以外の一意のインデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-a-single-update-change)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   配置ルール[＃43070](https://github.com/pingcap/tidb/issues/43070) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)でパーティション テーブル上の`TRUNCATE`のパフォーマンスを向上します。
    -   ロック[＃43659](https://github.com/pingcap/tidb/issues/43659) @ [あなた06](https://github.com/you06)を解決した後の無効なステイル読み取り再試行を回避する
    -   ステイル読み取りで`DataIsNotReady`エラー[＃765](https://github.com/tikv/client-go/pull/765) @ [テーマ](https://github.com/Tema)が発生した場合にリーダー読み取りを使用してレイテンシーを削減します。
    -   ステイル読み取り [＃43325](https://github.com/pingcap/tidb/issues/43325) @ [あなた06](https://github.com/you06)を使用するときにヒット率とトラフィックを追跡するために`Stale Read OPS`と`Stale Read MBps`メトリックを追加します

-   TiKV

    -   gzip を使用して`check_leader`リクエストを[＃14839](https://github.com/tikv/tikv/issues/14839) @ [cfzjywxk](https://github.com/cfzjywxk)で圧縮し、トラフィックを削減します

-   PD

    -   他のリクエスト[＃6403](https://github.com/tikv/pd/issues/6403) @ [rleungx](https://github.com/rleungx)の影響を防ぐために、PDリーダー選出には別のgRPC接続を使用する

-   ツール

    -   TiCDC

        -   TiCDC が DDL を処理する方法を最適化し、DDL が他の無関係な DML イベントの使用をブロックしないようにし、メモリ使用量を削減します[＃8106](https://github.com/pingcap/tiflow/issues/8106) @ [アズドンメン](https://github.com/asddongmen)
        -   デコーダーインターフェースを最適化し、新しいメソッド`AddKeyValue` [＃8861](https://github.com/pingcap/tiflow/issues/8861) @ [3エースショーハンド](https://github.com/3AceShowHand)を追加します
        -   オブジェクトstorageにデータを複製するシナリオでDDLイベントが発生した場合にディレクトリ構造を最適化する[＃8890](https://github.com/pingcap/tiflow/issues/8890) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   Kafka-on-Pulsar ダウンストリームへのデータ複製をサポート[＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [ハイラスティン](https://github.com/Rustin170506)
        -   Kafka [＃8865](https://github.com/pingcap/tiflow/issues/8865) @ [ハイラスティン](https://github.com/Rustin170506)にデータを複製する際の検証に OAuth プロトコルの使用をサポート
        -   AvroまたはCSVプロトコルを使用してデータレプリケーション中にTiCDCが`UPDATE`ステートメントを処理する方法を最適化し、 `UPDATE` `DELETE`と`INSERT`ステートメントに分割して、 `DELETE`ステートメント[＃9086](https://github.com/pingcap/tiflow/issues/9086) @ [3エースショーハンド](https://github.com/3AceShowHand)から古い値を取得できるようにします。
        -   TLS [＃8867](https://github.com/pingcap/tiflow/issues/8867) @ [ハイラスティン](https://github.com/Rustin170506)を有効にするシナリオで認証アルゴリズムを設定するかどうかを制御する構成項目`insecure-skip-verify`を追加します。
        -   DDL レプリケーション操作を最適化して、DDL 操作による下流レイテンシー[＃8686](https://github.com/pingcap/tiflow/issues/8686) @ [ハイラスティン](https://github.com/Rustin170506)への影響を軽減します。
        -   TiCDC レプリケーションタスクが失敗したときにアップストリームの GC TLS を設定する方法を最適化します[＃8403](https://github.com/pingcap/tiflow/issues/8403) @ [charleszheng44](https://github.com/charleszheng44)

    -   TiDBBinlog

        -   テーブル情報の取得方法を最適化し、 Drainer [＃1137](https://github.com/pingcap/tidb-binlog/issues/1137) @ [リチュンジュ](https://github.com/lichunzhu)の初期化時間とメモリ使用量を削減します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `min, max`クエリ結果が正しくない問題を修正[＃43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   ウィンドウ関数をTiFlash [＃43922](https://github.com/pingcap/tidb/issues/43922) @ [ゲンリキ](https://github.com/gengliqi)にプッシュダウンする際の実行プランが正しくない問題を修正しました
    -   CTE を含むクエリによって TiDB がハングする問題を修正[＃43749](https://github.com/pingcap/tidb/issues/43749) [＃36896](https://github.com/pingcap/tidb/issues/36896) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `AES_DECRYPT`式[＃43063](https://github.com/pingcap/tidb/issues/43063) @ [lcwangchao](https://github.com/lcwangchao)を使用すると SQL 文が`runtime error: index out of range`エラーを報告する問題を修正しました
    -   `SHOW PROCESSLIST`文でサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [crazycs520](https://github.com/crazycs520)
    -   PD分離により実行中のDDL [＃44014](https://github.com/pingcap/tidb/issues/44014) [＃43755](https://github.com/pingcap/tidb/issues/43755) [＃44267](https://github.com/pingcap/tidb/issues/44267) @ [wjhuang2016](https://github.com/wjhuang2016)がブロックされる可能性がある問題を修正
    -   `UNION` [＃42563](https://github.com/pingcap/tidb/issues/42563) @ [lcwangchao](https://github.com/lcwangchao)でユニオンビューと一時テーブルをクエリするときに発生する TiDBpanic問題を修正しました。
    -   パーティション化されたテーブルにおける配置ルールの動作の問題を修正し、削除されたパーティションにおける配置ルールが正しく設定され、再利用されるようになりました[＃44116](https://github.com/pingcap/tidb/issues/44116) @ [lcwangchao](https://github.com/lcwangchao)
    -   パーティションテーブルのパーティションを切り捨てるとパーティションの配置ルールが無効になる可能性がある問題を修正[＃44031](https://github.com/pingcap/tidb/issues/44031) @ [lcwangchao](https://github.com/lcwangchao)
    -   テーブル名の変更中に TiCDC が行の変更の一部を失う可能性がある問題を修正[＃43338](https://github.com/pingcap/tidb/issues/43338) @ [接線](https://github.com/tangenta)
    -   BR [＃43725](https://github.com/pingcap/tidb/issues/43725) @ [接線](https://github.com/tangenta)を使用してテーブルをインポートした後に DDL ジョブ履歴が失われる問題を修正しました
    -   `JSON_OBJECT`場合によってはエラーが報告される可能性がある問題を修正[＃39806](https://github.com/pingcap/tidb/issues/39806) @ [ヤンケオ](https://github.com/YangKeao)
    -   IPv6環境[＃43286](https://github.com/pingcap/tidb/issues/43286) @ [定義2014](https://github.com/Defined2014)でクラスターが一部のシステムビューを照会できない問題を修正
    -   PDメンバーのアドレスが変更されると、 `AUTO_INCREMENT`列目のIDの割り当てが長時間ブロックされる問題を修正[＃42643](https://github.com/pingcap/tidb/issues/42643) @ [天菜まお](https://github.com/tiancaiamao)
    -   配置ルールのリサイクル中に TiDB が PD に重複したリクエストを送信し、PD ログ[＃33069](https://github.com/pingcap/tidb/issues/33069) @ [天菜まお](https://github.com/tiancaiamao)に多数の`full config reset`エントリが発生する問題を修正しました。
    -   `SHOW PRIVILEGES`文が不完全な権限リスト[＃40591](https://github.com/pingcap/tidb/issues/40591) @ [CbcWestwolf](https://github.com/CbcWestwolf)を返す問題を修正しました
    -   `ADMIN SHOW DDL JOBS LIMIT`誤った結果を返す問題を修正[＃42298](https://github.com/pingcap/tidb/issues/42298) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   パスワードの複雑さのチェックが有効になっているときに`tidb_auth_token`ユーザーの作成に失敗する問題を修正[＃44098](https://github.com/pingcap/tidb/issues/44098) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   動的プルーニングモード[＃43686](https://github.com/pingcap/tidb/issues/43686) @ [ミョンス](https://github.com/mjonss)で内部結合中にパーティションが見つからない問題を修正
    -   パーティションテーブル[＃41118](https://github.com/pingcap/tidb/issues/41118) @ [ミョンス](https://github.com/mjonss)で`MODIFY COLUMN`実行すると`Data Truncated`警告が発生する問題を修正しました
    -   IPv6環境で誤ったTiDBアドレスが表示される問題を修正[＃43260](https://github.com/pingcap/tidb/issues/43260) @ [ネクスター](https://github.com/nexustar)
    -   述語[＃43645](https://github.com/pingcap/tidb/issues/43645) @ [ウィノロス](https://github.com/winoros)をプッシュダウンするときに CTE 結果が正しくない問題を修正しました
    -   非相関サブクエリ[＃44051](https://github.com/pingcap/tidb/issues/44051) @ [ウィノロス](https://github.com/winoros)を含むステートメントで共通テーブル式 (CTE) を使用すると誤った結果が返される可能性がある問題を修正しました
    -   結合したテーブルの再配置により外部結合結果が不正確になる可能性がある問題を修正[＃44314](https://github.com/pingcap/tidb/issues/44314) @ [アイリンキッド](https://github.com/AilinKid)
    -   極端なケースで、悲観的トランザクションの最初のステートメントが再試行されるときに、このトランザクションのロックを解決するとトランザクションの正確性に影響する可能性がある問題を修正しました[＃42937](https://github.com/pingcap/tidb/issues/42937) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   GC がロック[＃43243](https://github.com/pingcap/tidb/issues/43243) @ [ミョンケミンタ](https://github.com/MyonKeminta)を解決するときに、まれに悲観的トランザクションの残余悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正しました。
    -   `batch cop`実行中のスキャン詳細情報が不正確になる可能性がある問題を修正[＃41582](https://github.com/pingcap/tidb/issues/41582) @ [あなた06](https://github.com/you06)
    -   ステイル読み取りと`PREPARE`文が同時に使用されている場合にTiDBがデータ更新を読み取れない問題を修正[＃43044](https://github.com/pingcap/tidb/issues/43044) @ [あなた06](https://github.com/you06)
    -   `LOAD DATA`文[＃43849](https://github.com/pingcap/tidb/issues/43849) @ [あなた06](https://github.com/you06)を実行すると`assertion failed`エラーが誤って報告される可能性がある問題を修正しました
    -   ステイル読み取り [＃43365](https://github.com/pingcap/tidb/issues/43365) @ [あなた06](https://github.com/you06)の使用中に`region data not ready`エラーが発生した場合にコプロセッサがリーダーにフォールバックできない問題を修正しました。

-   TiKV

    -   TiKVノードが[＃14547](https://github.com/tikv/tikv/issues/14547) @ [ヒック](https://github.com/hicqu)で失敗したときに、対応するリージョンのピアが誤って休止状態になる問題を修正しました
    -   継続的プロファイリング[＃14224](https://github.com/tikv/tikv/issues/14224) @ [タボキ](https://github.com/tabokie)におけるファイル ハンドル リークの問題を修正しました
    -   PD クラッシュにより PITR が[＃14184](https://github.com/tikv/tikv/issues/14184) @ [ユジュンセン](https://github.com/YuJuncen)で続行できなくなる問題を修正しました
    -   暗号化キーIDの競合により古いキー[＃14585](https://github.com/tikv/tikv/issues/14585) @ [タボキ](https://github.com/tabokie)が削除される可能性がある問題を修正しました
    -   自動コミットとポイント取得レプリカ読み取りによって線形化可能性[＃14715](https://github.com/tikv/tikv/issues/14715) @ [cfzjywxk](https://github.com/cfzjywxk)が破壊される可能性がある問題を修正しました
    -   クラスタを以前のバージョンからv6.5以降のバージョン[＃14780](https://github.com/tikv/tikv/issues/14780) @ [ミョンケミンタ](https://github.com/MyonKeminta)にアップグレードしたときに、蓄積されたロックレコードによって引き起こされるパフォーマンス低下の問題を修正しました。
    -   TiDB Lightning がSST ファイルの漏洩を引き起こす可能性がある問題を修正[＃14745](https://github.com/tikv/tikv/issues/14745) @ [ユジュンセン](https://github.com/YuJuncen)
    -   暗号化キーとラフトログファイルの削除の間の潜在的な競合を修正しました。これにより、TiKV が[＃14761](https://github.com/tikv/tikv/issues/14761) @ [コナー1996](https://github.com/Connor1996)で起動しなくなる可能性があります。

-   TiFlash

    -   リージョン転送[＃7519](https://github.com/pingcap/tiflash/issues/7519) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)中のパーティション TableScan 演算子のパフォーマンス低下の問題を修正しました
    -   `GENERATED`型フィールドが`TIMESTAMP`型または`TIME`型[＃7468](https://github.com/pingcap/tiflash/issues/7468) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)と一緒に存在する場合、 TiFlashクエリでエラーが報告される可能性がある問題を修正しました。
    -   大規模な更新トランザクションにより、 TiFlash が繰り返しエラーを報告し、 [＃7316](https://github.com/pingcap/tiflash/issues/7316) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を再起動する可能性がある問題を修正しました。
    -   `INSERT SELECT`文[＃7348](https://github.com/pingcap/tiflash/issues/7348) @ [ウィンドトーカー](https://github.com/windtalker)でTiFlashからデータを読み取るときに「Truncate error cast decimal as decimal」というエラーが発生する問題を修正しました。
    -   Joinビルド側のデータが非常に大きく、多くの小さな文字列型の列[＃7416](https://github.com/pingcap/tiflash/issues/7416) @ [イービン87](https://github.com/yibin87)が含まれている場合に、クエリが必要以上にメモリを消費する可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップが失敗したときにBRのエラーメッセージ「ロックタイムアウトを解決してください」が誤解を招き、実際のエラー情報が隠れてしまう問題を修正しました[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   50,000 個のテーブルがある場合に発生する可能性のある OOM 問題を修正しました[＃7872](https://github.com/pingcap/tiflow/issues/7872) @ [スドジ](https://github.com/sdojjy)
        -   上流 TiDB [＃8561](https://github.com/pingcap/tiflow/issues/8561) @ [金星の上](https://github.com/overvenus)で OOM が発生したときに TiCDC が停止する問題を修正しました
        -   ネットワーク分離やPDオーナーノードの再起動などのPD障害時にTiCDCが停止する問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [アズドンメン](https://github.com/asddongmen)
        -   TiCDC タイムゾーン設定[＃8798](https://github.com/pingcap/tiflow/issues/8798) @ [ハイラスティン](https://github.com/Rustin170506)の問題を修正
        -   上流の TiKV ノードの 1 つが[＃8858](https://github.com/pingcap/tiflow/issues/8858) @ [ヒック](https://github.com/hicqu)でクラッシュするとチェックポイントの遅延が増加する問題を修正しました
        -   下流のMySQLにデータを複製するときに、上流のTiDB [＃8040](https://github.com/pingcap/tiflow/issues/8040) @ [アズドンメン](https://github.com/asddongmen)で`FLASHBACK CLUSTER TO TIMESTAMP`ステートメントが実行された後にレプリケーションエラーが発生する問題を修正しました。
        -   オブジェクトstorageにデータを複製する際に、上流の`EXCHANGE PARTITION`操作が下流の[＃8914](https://github.com/pingcap/tiflow/issues/8914) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に正しく複製されない問題を修正しました。
        -   一部の特殊なシナリオでソートコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正[＃8974](https://github.com/pingcap/tiflow/issues/8974) @ [ヒック](https://github.com/hicqu)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードを引き起こす問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [ハイラスティン](https://github.com/Rustin170506)
        -   Kafka メッセージのサイズが大きすぎるためにレプリケーションエラーが発生した場合に、メッセージ本文がログ[＃9031](https://github.com/pingcap/tiflow/issues/9031) @ [ダラエス](https://github.com/darraes)に記録される問題を修正しました。
        -   下流の Kafka シンクがローリング再起動されたときに発生する TiCDC ノードpanicを修正しました[＃9023](https://github.com/pingcap/tiflow/issues/9023) @ [アズドンメン](https://github.com/asddongmen)
        -   storageサービスにデータを複製するときに、下流のDDLステートメントに対応するJSONファイルにテーブルフィールド[＃9066](https://github.com/pingcap/tiflow/issues/9066) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)のデフォルト値が記録されない問題を修正しました。

    -   TiDB Lightning

        -   幅の広いテーブル[＃43728](https://github.com/pingcap/tidb/issues/43728) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときに OOM が発生する可能性がある問題を修正しました
        -   大量のデータをインポートする際の`write to tikv with no leader returned`の問題を修正[＃43055](https://github.com/pingcap/tidb/issues/43055) @ [ランス6716](https://github.com/lance6716)
        -   データファイル[＃40400](https://github.com/pingcap/tidb/issues/40400) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)に閉じられていない区切り文字がある場合に発生する可能性のある OOM 問題を修正しました。
        -   データのインポート中にエラーが発生した場合に再試行メカニズム[＃43291](https://github.com/pingcap/tidb/issues/43291) `unknown RPC` [D3ハンター](https://github.com/D3Hunter)

    -   TiDBBinlog

        -   TiDB Binlogが`CANCELED` DDL文[＃1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [okJiang](https://github.com/okJiang)に遭遇したときにエラーを報告する問題を修正しました
