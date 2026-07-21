---
title: TiDB 6.5.3 Release Notes
summary: TiDB 6.5.3 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.3 リリースノート {#tidb-6-5-3-release-notes}

発売日：2023年6月14日

TiDB バージョン: 6.5.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

### 動作の変更 {#behavior-changes}

-   更新イベントの処理中に、イベント内の主キーまたはnull以外の一意インデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-a-single-update-change)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   配置ルールでパーティション テーブル上の`TRUNCATE`のパフォーマンスを向上します。 [＃43070](https://github.com/pingcap/tidb/issues/43070) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   ロックを解決した後の無効なステイル読み取り再試行を回避する [＃43659](https://github.com/pingcap/tidb/issues/43659) @ [you06](https://github.com/you06)
    -   ステイル読み取りで`DataIsNotReady`エラーが発生した場合にリーダー読み取りを使用してレイテンシーを削減します。 [＃765](https://github.com/tikv/client-go/pull/765) @ [Tema](https://github.com/Tema)
    -   ステイル読み取り を使用するときにヒット率とトラフィックを追跡するために`Stale Read OPS`と`Stale Read MBps`メトリックを追加します [＃43325](https://github.com/pingcap/tidb/issues/43325) @ [you06](https://github.com/you06)

-   TiKV

    -   gzip を使用して`check_leader`リクエストをで圧縮し、トラフィックを削減します [＃14839](https://github.com/tikv/tikv/issues/14839) @ [cfzjywxk](https://github.com/cfzjywxk)

-   PD

    -   他のリクエストの影響を防ぐために、PDリーダー選出には別のgRPC接続を使用する [＃6403](https://github.com/tikv/pd/issues/6403) @ [rleungx](https://github.com/rleungx)

-   ツール

    -   TiCDC

        -   TiCDC が DDL を処理する方法を最適化し、DDL が他の無関係な DML イベントの使用をブロックしないようにし、メモリ使用量を削減します[＃8106](https://github.com/pingcap/tiflow/issues/8106) @ [asddongmen](https://github.com/asddongmen)
        -   デコーダーインターフェースを最適化し、新しいメソッド`AddKeyValue` を追加します [＃8861](https://github.com/pingcap/tiflow/issues/8861) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   オブジェクトストレージにデータを複製するシナリオでDDLイベントが発生した場合にディレクトリ構造を最適化する[＃8890](https://github.com/pingcap/tiflow/issues/8890) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   Kafka-on-Pulsar ダウンストリームへのデータ複製をサポート[＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [Rustin170506](https://github.com/Rustin170506)
        -   Kafka にデータを複製する際の検証に OAuth プロトコルの使用をサポート [＃8865](https://github.com/pingcap/tiflow/issues/8865) @ [Rustin170506](https://github.com/Rustin170506)
        -   AvroまたはCSVプロトコルを使用してデータレプリケーション中にTiCDCが`UPDATE`ステートメントを処理する方法を最適化し、 `UPDATE` `DELETE`と`INSERT`ステートメントに分割して、 `DELETE`ステートメントから古い値を取得できるようにします。 [＃9086](https://github.com/pingcap/tiflow/issues/9086) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   TLS を有効にするシナリオで認証アルゴリズムを設定するかどうかを制御する構成項目`insecure-skip-verify`を追加します。 [＃8867](https://github.com/pingcap/tiflow/issues/8867) @ [Rustin170506](https://github.com/Rustin170506)
        -   DDL レプリケーション操作を最適化して、DDL 操作による下流レイテンシーへの影響を軽減します。 [＃8686](https://github.com/pingcap/tiflow/issues/8686) @ [Rustin170506](https://github.com/Rustin170506)
        -   TiCDC レプリケーションタスクが失敗したときにアップストリームの GC TLS を設定する方法を最適化します[＃8403](https://github.com/pingcap/tiflow/issues/8403) @ [charleszheng44](https://github.com/charleszheng44)

    -   TiDB Binlog

        -   テーブル情報の取得方法を最適化し、 Drainer の初期化時間とメモリ使用量を削減します。 [＃1137](https://github.com/pingcap/tidb-binlog/issues/1137) @ [lichunzhu](https://github.com/lichunzhu)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `min, max`クエリ結果が正しくない問題を修正[＃43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   ウィンドウ関数をTiFlash にプッシュダウンする際の実行プランが正しくない問題を修正しました [＃43922](https://github.com/pingcap/tidb/issues/43922) @ [gengliqi](https://github.com/gengliqi)
    -   CTE を含むクエリによって TiDB がハングする問題を修正[＃43749](https://github.com/pingcap/tidb/issues/43749) [＃36896](https://github.com/pingcap/tidb/issues/36896) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `AES_DECRYPT`式を使用すると SQL 文が`runtime error: index out of range`エラーを報告する問題を修正しました [＃43063](https://github.com/pingcap/tidb/issues/43063) @ [lcwangchao](https://github.com/lcwangchao)
    -   `SHOW PROCESSLIST`文でサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [crazycs520](https://github.com/crazycs520)
    -   PD分離により実行中のDDL [＃44014](https://github.com/pingcap/tidb/issues/44014) がブロックされる可能性がある問題を修正 [＃44267](https://github.com/pingcap/tidb/issues/44267) @ [wjhuang2016](https://github.com/wjhuang2016) [＃43755](https://github.com/pingcap/tidb/issues/43755)
    -   `UNION` でユニオンビューと一時テーブルをクエリするときに発生する TiDBのpanic問題を修正しました。 [＃42563](https://github.com/pingcap/tidb/issues/42563) @ [lcwangchao](https://github.com/lcwangchao)
    -   パーティション化されたテーブルにおける配置ルールの動作の問題を修正し、削除されたパーティションにおける配置ルールが正しく設定され、再利用されるようになりました[＃44116](https://github.com/pingcap/tidb/issues/44116) @ [lcwangchao](https://github.com/lcwangchao)
    -   パーティションテーブルのパーティションを切り捨てるとパーティションの配置ルールが無効になる可能性がある問題を修正[＃44031](https://github.com/pingcap/tidb/issues/44031) @ [lcwangchao](https://github.com/lcwangchao)
    -   テーブル名の変更中に TiCDC が行の変更の一部を失う可能性がある問題を修正[＃43338](https://github.com/pingcap/tidb/issues/43338) @ [tangenta](https://github.com/tangenta)
    -   BR を使用してテーブルをインポートした後に DDL ジョブ履歴が失われる問題を修正しました [＃43725](https://github.com/pingcap/tidb/issues/43725) @ [tangenta](https://github.com/tangenta)
    -   `JSON_OBJECT`で場合によってはエラーが報告される可能性がある問題を修正[＃39806](https://github.com/pingcap/tidb/issues/39806) @ [YangKeao](https://github.com/YangKeao)
    -   IPv6環境でクラスターが一部のシステムビューを照会できない問題を修正 [＃43286](https://github.com/pingcap/tidb/issues/43286) @ [Defined2014](https://github.com/Defined2014)
    -   PDメンバーのアドレスが変更されると、 `AUTO_INCREMENT`列のIDの割り当てが長時間ブロックされる問題を修正[＃42643](https://github.com/pingcap/tidb/issues/42643) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   配置ルールのリサイクル中に TiDB が PD に重複したリクエストを送信し、PD ログに多数の`full config reset`エントリが発生する問題を修正しました。 [＃33069](https://github.com/pingcap/tidb/issues/33069) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `SHOW PRIVILEGES`文が不完全な権限リストを返す問題を修正しました [＃40591](https://github.com/pingcap/tidb/issues/40591) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   `ADMIN SHOW DDL JOBS LIMIT`誤った結果を返す問題を修正[＃42298](https://github.com/pingcap/tidb/issues/42298) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   パスワードの複雑さのチェックが有効になっているときに`tidb_auth_token`ユーザーの作成に失敗する問題を修正[＃44098](https://github.com/pingcap/tidb/issues/44098) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   動的プルーニングモードで内部結合中にパーティションが見つからない問題を修正 [＃43686](https://github.com/pingcap/tidb/issues/43686) @ [mjonss](https://github.com/mjonss)
    -   パーティションテーブルで`MODIFY COLUMN`実行すると`Data Truncated`警告が発生する問題を修正しました [＃41118](https://github.com/pingcap/tidb/issues/41118) @ [mjonss](https://github.com/mjonss)
    -   IPv6環境で誤ったTiDBアドレスが表示される問題を修正[＃43260](https://github.com/pingcap/tidb/issues/43260) @ [nexustar](https://github.com/nexustar)
    -   述語をプッシュダウンするときに CTE 結果が正しくない問題を修正しました [＃43645](https://github.com/pingcap/tidb/issues/43645) @ [winoros](https://github.com/winoros)
    -   非相関サブクエリを含むステートメントで共通テーブル式 (CTE) を使用すると誤った結果が返される可能性がある問題を修正しました [＃44051](https://github.com/pingcap/tidb/issues/44051) @ [winoros](https://github.com/winoros)
    -   結合したテーブルの再配置により外部結合結果が不正確になる可能性がある問題を修正[＃44314](https://github.com/pingcap/tidb/issues/44314) @ [AilinKid](https://github.com/AilinKid)
    -   極端なケースで、悲観的トランザクションの最初のステートメントが再試行されるときに、このトランザクションのロックを解決するとトランザクションの正確性に影響する可能性がある問題を修正しました[＃42937](https://github.com/pingcap/tidb/issues/42937) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   GC がロックを解決するときに、まれに悲観的トランザクションの残余悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正しました。 [＃43243](https://github.com/pingcap/tidb/issues/43243) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   `batch cop`実行中のスキャン詳細情報が不正確になる可能性がある問題を修正[＃41582](https://github.com/pingcap/tidb/issues/41582) @ [you06](https://github.com/you06)
    -   ステイル読み取りと`PREPARE`文が同時に使用されている場合にTiDBがデータ更新を読み取れない問題を修正[＃43044](https://github.com/pingcap/tidb/issues/43044) @ [you06](https://github.com/you06)
    -   `LOAD DATA`文を実行すると`assertion failed`エラーが誤って報告される可能性がある問題を修正しました [＃43849](https://github.com/pingcap/tidb/issues/43849) @ [you06](https://github.com/you06)
    -   ステイル読み取り の使用中に`region data not ready`エラーが発生した場合にコプロセッサがリーダーにフォールバックできない問題を修正しました。 [＃43365](https://github.com/pingcap/tidb/issues/43365) @ [you06](https://github.com/you06)

-   TiKV

    -   TiKVノードが失敗したときに、対応するリージョンのピアが誤って休止状態になる問題を修正しました [＃14547](https://github.com/tikv/tikv/issues/14547) @ [hicqu](https://github.com/hicqu)
    -   継続的プロファイリングにおけるファイル ハンドル リークの問題を修正しました [＃14224](https://github.com/tikv/tikv/issues/14224) @ [tabokie](https://github.com/tabokie)
    -   PD クラッシュにより PITR が続行できなくなる問題を修正しました [＃14184](https://github.com/tikv/tikv/issues/14184) @ [YuJuncen](https://github.com/YuJuncen)
    -   暗号化キーIDの競合により古いキーが削除される可能性がある問題を修正しました [＃14585](https://github.com/tikv/tikv/issues/14585) @ [tabokie](https://github.com/tabokie)
    -   自動コミットとPointGetレプリカ読み取りによって線形化可能性が破壊される可能性がある問題を修正しました [＃14715](https://github.com/tikv/tikv/issues/14715) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   クラスタを以前のバージョンからv6.5以降のバージョンにアップグレードしたときに、蓄積されたロックレコードによって引き起こされるパフォーマンス低下の問題を修正しました。 [＃14780](https://github.com/tikv/tikv/issues/14780) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   TiDB Lightning がSST ファイルの漏洩を引き起こす可能性がある問題を修正[＃14745](https://github.com/tikv/tikv/issues/14745) @ [YuJuncen](https://github.com/YuJuncen)
    -   暗号化キーとラフトログファイルの削除の間の潜在的な競合を修正しました。これにより、TiKV が起動しなくなる可能性があります。 [＃14761](https://github.com/tikv/tikv/issues/14761) @ [Connor1996](https://github.com/Connor1996)

-   TiFlash

    -   リージョン転送中のパーティション TableScan 演算子のパフォーマンス低下の問題を修正しました [＃7519](https://github.com/pingcap/tiflash/issues/7519) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `GENERATED`型フィールドが`TIMESTAMP`型または`TIME`型と一緒に存在する場合、 TiFlashクエリでエラーが報告される可能性がある問題を修正しました。 [＃7468](https://github.com/pingcap/tiflash/issues/7468) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   大規模な更新トランザクションにより、 TiFlash が繰り返しエラーを報告し、 を再起動する可能性がある問題を修正しました。 [＃7316](https://github.com/pingcap/tiflash/issues/7316) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   `INSERT SELECT`文でTiFlashからデータを読み取るときに「Truncate error cast decimal as decimal」というエラーが発生する問題を修正しました。 [＃7348](https://github.com/pingcap/tiflash/issues/7348) @ [windtalker](https://github.com/windtalker)
    -   Joinビルド側のデータが非常に大きく、多くの小さな文字列型の列が含まれている場合に、クエリが必要以上にメモリを消費する可能性がある問題を修正しました。 [＃7416](https://github.com/pingcap/tiflash/issues/7416) @ [yibin87](https://github.com/yibin87)

-   ツール

    -   Backup & Restore (BR)

        -   バックアップが失敗したときにBRのエラーメッセージ「ロックタイムアウトを解決してください」が誤解を招き、実際のエラー情報が隠れてしまう問題を修正しました[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   50,000 個のテーブルがある場合に発生する可能性のある OOM 問題を修正しました[＃7872](https://github.com/pingcap/tiflow/issues/7872) @ [sdojjy](https://github.com/sdojjy)
        -   上流 TiDB で OOM が発生したときに TiCDC が停止する問題を修正しました [＃8561](https://github.com/pingcap/tiflow/issues/8561) @ [overvenus](https://github.com/overvenus)
        -   ネットワーク分離やPDオーナーノードの再起動などのPD障害時にTiCDCが停止する問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [asddongmen](https://github.com/asddongmen)
        -   TiCDC タイムゾーン設定の問題を修正 [＃8798](https://github.com/pingcap/tiflow/issues/8798) @ [Rustin170506](https://github.com/Rustin170506)
        -   上流の TiKV ノードの 1 つがクラッシュするとチェックポイントの遅延が増加する問題を修正しました [＃8858](https://github.com/pingcap/tiflow/issues/8858) @ [hicqu](https://github.com/hicqu)
        -   下流のMySQLにデータを複製するときに、上流のTiDB で`FLASHBACK CLUSTER TO TIMESTAMP`ステートメントが実行された後にレプリケーションエラーが発生する問題を修正しました。 [＃8040](https://github.com/pingcap/tiflow/issues/8040) @ [asddongmen](https://github.com/asddongmen)
        -   オブジェクトストレージにデータを複製する際に、上流の`EXCHANGE PARTITION`操作が下流のに正しく複製されない問題を修正しました。 [＃8914](https://github.com/pingcap/tiflow/issues/8914) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   一部の特殊なシナリオでソートコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正[＃8974](https://github.com/pingcap/tiflow/issues/8974) @ [hicqu](https://github.com/hicqu)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードを引き起こす問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [Rustin170506](https://github.com/Rustin170506)
        -   Kafka メッセージのサイズが大きすぎるためにレプリケーションエラーが発生した場合に、メッセージ本文がログに記録される問題を修正しました。 [＃9031](https://github.com/pingcap/tiflow/issues/9031) @ [darraes](https://github.com/darraes)
        -   下流の Kafka シンクがローリング再起動されたときに発生する TiCDC ノードpanicを修正しました[＃9023](https://github.com/pingcap/tiflow/issues/9023) @ [asddongmen](https://github.com/asddongmen)
        -   ストレージサービスにデータを複製するときに、下流のDDLステートメントに対応するJSONファイルにテーブルフィールドのデフォルト値が記録されない問題を修正しました。 [＃9066](https://github.com/pingcap/tiflow/issues/9066) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Lightning

        -   幅の広いテーブルをインポートするときに OOM が発生する可能性がある問題を修正しました [＃43728](https://github.com/pingcap/tidb/issues/43728) @ [D3Hunter](https://github.com/D3Hunter)
        -   大量のデータをインポートする際の`write to tikv with no leader returned`の問題を修正[＃43055](https://github.com/pingcap/tidb/issues/43055) @ [lance6716](https://github.com/lance6716)
        -   データファイルに閉じられていない区切り文字がある場合に発生する可能性のある OOM 問題を修正しました。 [＃40400](https://github.com/pingcap/tidb/issues/40400) @ [buchuitoudegou](https://github.com/buchuitoudegou)
        -   データのインポート中にエラーが発生した場合に再試行メカニズム[＃43291](https://github.com/pingcap/tidb/issues/43291) `unknown RPC` [D3ハンター](https://github.com/D3Hunter)

    -   TiDB Binlog

        -   TiDB Binlogが`CANCELED` DDL文に遭遇したときにエラーを報告する問題を修正しました [＃1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [okJiang](https://github.com/okJiang)
