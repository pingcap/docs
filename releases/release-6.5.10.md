---
title: TiDB 6.5.10 Release Notes
summary: TiDB 6.5.10 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.10 リリースノート {#tidb-6-5-10-release-notes}

発売日：2024年6月20日

TiDB バージョン: 6.5.10

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   以前のバージョンでは、 `UPDATE`変更を含むトランザクションを処理する際に、 `UPDATE`目のイベントで主キーまたは非NULLの一意インデックス値が変更されると、TiCDCはこのイベントを`DELETE`目と`INSERT`目のイベントに分割していました。v6.5.10以降では、MySQLシンクを使用する場合、 `UPDATE`の変更のトランザクション`commitTS`がTiCDC `thresholdTS` （TiCDCが対応するテーブルをダウンストリームに複製し始める際にPDから取得する現在のタイムスタンプ）より小さい場合、TiCDCは`UPDATE`目のイベントを`DELETE` `INSERT`と13件目のイベントに分割します。この動作変更は、TiCDCが受信した`UPDATE`目のイベントの順序が誤っている可能性があり、分割された`DELETE`と`INSERT`目のイベントの順序が誤っている可能性があるため、ダウンストリームデータの不整合が発生する問題に対処しています。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v6.5/ticdc-split-update-behavior#split-update-events-for-mysql-sinks) してください@ [lidezhu](https://github.com/lidezhu) [＃10918](https://github.com/pingcap/tiflow/issues/10918)
-   TiDB Lightning `strict-format`を使用して CSV ファイルをインポートする場合は、行末文字を設定する必要があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [lance6716](https://github.com/lance6716)

## 改善点 {#improvements}

-   TiDB

    -   `SHOW CREATE TABLE` の出力に表示される式のデフォルト値のMySQL互換性を改善しました [＃52939](https://github.com/pingcap/tidb/issues/52939) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   MPP ロード バランシング中にリージョンのないストアを削除する [＃52313](https://github.com/pingcap/tidb/issues/52313) @ [xzhangxian1008](https://github.com/xzhangxian1008)

-   TiKV

    -   TiKV のシャットダウン速度を加速 [＃16680](https://github.com/tikv/tikv/issues/16680) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   CDC イベント処理のキュー時間の監視メトリックを追加して、下流の CDC イベントレイテンシー問題のトラブルシューティングを容易にします[＃16282](https://github.com/tikv/tikv/issues/16282) @ [hicqu](https://github.com/hicqu)

-   ツール

    -   Backup & Restore (BR)

        -   BRはデータ復旧中に空のSSTファイルをクリーンアップします[＃16005](https://github.com/tikv/tikv/issues/16005) @ [Leavrth](https://github.com/Leavrth)
        -   DNSエラーによる失敗の再試行回数をから@ [YuJuncen](https://github.com/YuJuncen)増やす [＃53029](https://github.com/pingcap/tidb/issues/53029)
        -   リージョンのリーダーの不在によって発生した失敗の再試行回数を@ [Leavrth](https://github.com/Leavrth)に増やす [＃54017](https://github.com/pingcap/tidb/issues/54017)

    -   TiCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドストレージの場合に生のイベントを直接出力することをサポートします[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDOログを使用してデータリカバリ中のメモリの安定性を向上させ、OOM の確率を低減します。 [＃10900](https://github.com/pingcap/tiflow/issues/10900) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   トランザクション競合シナリオにおけるデータレプリケーションの安定性が大幅に向上し、パフォーマンスが最大10倍向上します[＃10896](https://github.com/pingcap/tiflow/issues/10896) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   統計の初期化中にメタデータをクエリすると、OOM が発生する可能性がある問題を修正しました。 [＃52219](https://github.com/pingcap/tidb/issues/52219) @ [hawkingrei](https://github.com/hawkingrei)
    -   `AUTO_ID_CACHE=1`AUTO_INCREMENT列を含むテーブルで、 `auto_increment_increment`と`auto_increment_offset`システム変数をデフォルト以外の値に設定すると、不正なAUTO_INCREMENT ID 割り当てが発生する可能性がある問題を修正しました。 [＃52622](https://github.com/pingcap/tidb/issues/52622) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `RESTORE`ステートメントを使用して`AUTO_ID_CACHE=1`のテーブルを復元すると`Duplicate entry`エラーが発生する可能性がある問題を修正しました [＃52680](https://github.com/pingcap/tidb/issues/52680) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `STATE`のフィールドのうち`size`番目が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`のテーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   外部キーを持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました。 [＃53652](https://github.com/pingcap/tidb/issues/53652) @ [hawkingrei](https://github.com/hawkingrei)
    -   クエリの同時実行数が多い場合に統計同期読み込みメカニズムが予期せず失敗する可能性がある問題を修正しました[＃52294](https://github.com/pingcap/tidb/issues/52294) @ [hawkingrei](https://github.com/hawkingrei)
    -   グローバル統計の`Distinct_count`情報が間違っている可能性がある問題を修正しました[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [hawkingrei](https://github.com/hawkingrei)
    -   TiDB を再起動した後、主キー列統計のヒストグラムと TopN がロードされない問題を修正しました [＃37548](https://github.com/pingcap/tidb/issues/37548) @ [hawkingrei](https://github.com/hawkingrei)
    -   クエリ内の特定のフィルター条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) を報告する可能性がある問題を修正しました [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [YangKeao](https://github.com/YangKeao) [＃53594](https://github.com/pingcap/tidb/issues/53594)
    -   `?`引数を含む`CONV` `EXECUTE` `PREPARE`を複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   オプティマイザーヒント使用時に誤った警告情報が表示される問題を修正しました [＃53767](https://github.com/pingcap/tidb/issues/53767) @ [hawkingrei](https://github.com/hawkingrei)
    -   情報スキーマキャッシュミスにより、古い読み取りのクエリレイテンシーが増加する問題を修正しました。 [＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)
    -   DDL ステートメントが etcd を誤って使用し、タスクがキューに入れられる問題を修正しました。 [＃52335](https://github.com/pingcap/tidb/issues/52335) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   式インデックスの名前を変更する`RENAME INDEX`を実行したときに内部列の名前が変更されない問題を修正しました [＃51431](https://github.com/pingcap/tidb/issues/51431) @ [ywqzzy](https://github.com/ywqzzy)
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラーが発生する可能性がある問題を修正 [＃53673](https://github.com/pingcap/tidb/issues/53673) @ [tangenta](https://github.com/tangenta)
    -   JOIN条件に暗黙的な型変換が含まれている場合にTiDBがpanic可能性がある問題を修正しました [＃46556](https://github.com/pingcap/tidb/issues/46556) @ [qw4990](https://github.com/qw4990)
    -   ネットワークの問題によりDDL操作が停止する問題を修正[＃47060](https://github.com/pingcap/tidb/issues/47060) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   IndexJoin が Left Outer Anti Semi type のハッシュ値を計算するときに重複行を生成する問題を修正しました。 [＃52902](https://github.com/pingcap/tidb/issues/52902) @ [yibin87](https://github.com/yibin87)
    -   `ALL`関数に含まれるサブクエリが誤った結果を引き起こす可能性がある問題を修正[＃52755](https://github.com/pingcap/tidb/issues/52755) @ [hawkingrei](https://github.com/hawkingrei)
    -   `TIMESTAMPADD()`関数が誤った結果を返す問題を修正[＃41052](https://github.com/pingcap/tidb/issues/41052) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `tidb_mem_quota_analyze`が有効になっていて、統計の更新に使用されるメモリが制限を超えると TiDB がクラッシュする可能性がある問題を修正しました。 [＃52601](https://github.com/pingcap/tidb/issues/52601) @ [hawkingrei](https://github.com/hawkingrei)
    -   `UPDATE`リスト内のサブクエリによって TiDB がpanic可能性がある問題を修正[＃52687](https://github.com/pingcap/tidb/issues/52687) @ [winoros](https://github.com/winoros)
    -   述語の`Longlong`型のオーバーフローの問題を修正 [＃45783](https://github.com/pingcap/tidb/issues/45783) @ [hawkingrei](https://github.com/hawkingrei)
    -   一意インデックスを追加するときに同時 DML 操作によって発生するデータ インデックスの不整合の問題を修正しました。 [＃52914](https://github.com/pingcap/tidb/issues/52914) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   インデックスデータを解析するときに TiDB がpanic可能性がある問題を修正しました [＃47115](https://github.com/pingcap/tidb/issues/47115) @ [zyguan](https://github.com/zyguan)
    -   スライスの浅いコピーを使用せずに列プルーニングを行うと、TiDB がpanic可能性がある問題を修正しました[＃52768](https://github.com/pingcap/tidb/issues/52768) @ [winoros](https://github.com/winoros)
    -   再帰CTE でビューの使用が機能しない問題を修正 [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [hawkingrei](https://github.com/hawkingrei)
    -   `LEADING`ヒントがブロックエイリアスのクエリをサポートしない問題を修正しました [＃44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)
    -   相関サブクエリにおける TopN 演算子の誤った結果を修正 [＃52777](https://github.com/pingcap/tidb/issues/52777) @ [yibin87](https://github.com/yibin87)
    -   列の不安定な一意のIDにより、 `UPDATE`文がエラーを返す可能性がある問題を修正しました。 [＃53236](https://github.com/pingcap/tidb/issues/53236) @ [winoros](https://github.com/winoros)
    -   TiDBがオフラインになっているTiFlashノードにプローブ要求を送信し続ける問題を修正[＃46602](https://github.com/pingcap/tidb/issues/46602) @ [zyguan](https://github.com/zyguan)
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   AutoIDLeaderの変更により、 `AUTO_ID_CACHE=1` の場合にAUTO_INCREMENT列の値が減少する可能性がある問題を修正しました。 [＃52600](https://github.com/pingcap/tidb/issues/52600) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   BIGINT 以外の符号なし整数が文字列/小数点と比較されたときに誤った結果を生成する可能性がある問題を修正しました [＃41736](https://github.com/pingcap/tidb/issues/41736) @ [LittleFall](https://github.com/LittleFall)
    -   `FLOAT`型から`UNSIGNED`型へのデータ変換で誤った結果が返される問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `VAR_SAMP()`ウィンドウ関数として使用できない問題を修正 [＃52933](https://github.com/pingcap/tidb/issues/52933) @ [Rustin170506](https://github.com/Rustin170506)
    -   間違った TableDual プランにより空のクエリ結果が発生する問題を修正しました [＃50051](https://github.com/pingcap/tidb/issues/50051) @ [onlyacat](https://github.com/onlyacat)
    -   TiDBの同期的な統計読み込みメカニズムが空の統計の読み込みを無期限に再試行し、 `fail to get stats version for this histogram` log を出力問題を修正しました。 [＃52657](https://github.com/pingcap/tidb/issues/52657) @ [hawkingrei](https://github.com/hawkingrei)
    -   空の投影により TiDB がpanicを引き起こす問題を修正しました [＃49109](https://github.com/pingcap/tidb/issues/49109) @ [winoros](https://github.com/winoros)
    -   TopN演算子が誤ってプッシュダウンされる可能性がある問題を修正しました [＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)
    -   常に`true` となる述語を持つ`SHOW ERRORS`文を実行すると TiDB がパニックを起こす問題を修正しました。 [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [elsa0520](https://github.com/elsa0520)
    -   プランキャッシュシナリオでメタデータロックがDDL操作の実行を阻止できない問題を修正 [＃51407](https://github.com/pingcap/tidb/issues/51407) @ [wjhuang2016](https://github.com/wjhuang2016)

-   TiKV

    -   1 つの TiKV ノードで遅い`check-leader`操作により、他の TiKV ノードの`resolved-ts`正常に進まなくなる問題を修正しました。 [＃15999](https://github.com/tikv/tikv/issues/15999) @ [crazycs520](https://github.com/crazycs520)
    -   クエリ内の`CONV()`関数が数値システム変換中にオーバーフローし、TiKV panicが発生する問題を修正しました。 [＃16969](https://github.com/tikv/tikv/issues/16969) @ [gengliqi](https://github.com/gengliqi)
    -   不安定なテストケースの問題を修正し、各テストが独立した一時ディレクトリを使用するようにして、オンライン構成の変更が他のテストケースに影響しないようにします。 [＃16871](https://github.com/tikv/tikv/issues/16871) @ [glorv](https://github.com/glorv)
    -   `DECIMAL`型の小数点部分が場合に正しくない問題を修正しました [＃16913](https://github.com/tikv/tikv/issues/16913) @ [gengliqi](https://github.com/gengliqi)
    -   古いリージョンピアがGCメッセージを無視するとresolve-tsがブロックされる問題を修正しました [＃16504](https://github.com/tikv/tikv/issues/16504) @ [crazycs520](https://github.com/crazycs520)

-   PD

    -   展開された2つのデータセンター間でリーダーを切り替えるとLeaderが失敗する問題を修正[＃7992](https://github.com/tikv/pd/issues/7992) @ [TonsnakeLin](https://github.com/TonsnakeLin)
    -   配置ルールを使用しているときに、ダウンしたピアが回復しない可能性がある問題を修正しました。 [＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)
    -   PDの`Filter target`監視メトリックが散布範囲情報を提供しない問題を修正[＃8125](https://github.com/tikv/pd/issues/8125) @ [HuSharp](https://github.com/HuSharp)

-   TiFlash

    -   データベース間で`ALTER TABLE ... EXCHANGE PARTITION`を実行した後にTiFlash がスキーマの同期に失敗する可能性がある問題を修正しました[＃7296](https://github.com/pingcap/tiflash/issues/7296) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   空のキー範囲を持つクエリがTiFlashで読み取りタスクを正しく生成できず、 TiFlashクエリがブロックされる可能性がある問題を修正しました。 [＃9108](https://github.com/pingcap/tiflash/issues/9108) @ [JinheLin](https://github.com/JinheLin)
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash のクラッシュを引き起こす可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [wshwsh12](https://github.com/wshwsh12)
    -   クラスタをv6.5.0より前のバージョンからv6.5.0以降にアップグレードするときに、 TiFlashメタデータが破損してプロセスがpanicになる可能性がある問題を修正しました[＃9039](https://github.com/pingcap/tiflash/issues/9039) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlash が高同時読み取りシナリオで一時的に誤った結果を返す可能性がある問題を修正[＃8845](https://github.com/pingcap/tiflash/issues/8845) @ [JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   テストケース`TestGetTSWithRetry`実行に時間がかかりすぎる問題を修正[＃52547](https://github.com/pingcap/tidb/issues/52547) @ [Leavrth](https://github.com/Leavrth)
        -   BRを使用してデータを復元する場合、または物理インポート モードでTiDB Lightningを使用してデータをインポートする場合に、PD から取得されたリージョンにLeaderがない問題を修正しました[＃51124](https://github.com/pingcap/tidb/issues/51124) [＃50501](https://github.com/pingcap/tidb/issues/50501) @ [Leavrth](https://github.com/Leavrth)
        -   PD接続障害により、ログバックアップアドバンサ所有者が配置されているTiDBインスタンスがpanicになる可能性がある問題を修正しました。 [＃52597](https://github.com/pingcap/tidb/issues/52597) @ [YuJuncen](https://github.com/YuJuncen)
        -   ログバックアップタスクを一時停止、停止、再構築した後、タスクの状態は正常であるが、チェックポイントがに進まない問題を修正しました。 [＃53047](https://github.com/pingcap/tidb/issues/53047) @ [RidRisR](https://github.com/RidRisR)
        -   TiKVノードにリーダーがいないためにデータ復元が遅くなる問題を修正 [＃50566](https://github.com/pingcap/tidb/issues/50566) @ [Leavrth](https://github.com/Leavrth)
        -   TiKV の再起動により、ログ バックアップのグローバル チェックポイントが実際のバックアップ ファイルの書き込みポイントよりも先に進められ、少量のバックアップ データが失われる可能性がある問題を修正しました[＃16809](https://github.com/tikv/tikv/issues/16809) @ [YuJuncen](https://github.com/YuJuncen)
        -   PDリーダーの転送により、データ復元時にBRがpanicになる可能性がある問題を修正しました。 [＃53724](https://github.com/pingcap/tidb/issues/53724) @ [Leavrth](https://github.com/Leavrth)
        -   PD へのネットワーク接続が不安定な状態で一時停止中のログバックアップタスクを再開すると TiKV がpanic可能性がある問題を修正しました [＃17020](https://github.com/tikv/tikv/issues/17020) @ [YuJuncen](https://github.com/YuJuncen)
        -   アドバンサー所有者の移行後にログバックアップが一時停止される可能性がある問題を修正しました [＃53561](https://github.com/pingcap/tidb/issues/53561) @ [RidRisR](https://github.com/RidRisR)
        -   復元プロセス中に複数のネストされた再試行によりBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   下流データベースのパスワードがBase64でエンコードされている場合、TiCDCが同期ポイントを有効にして変更フィードを作成できない問題を修正しました[＃10516](https://github.com/pingcap/tiflow/issues/10516) @ [asddongmen](https://github.com/asddongmen)
        -   `DROP PRIMARY KEY`と`DROP UNIQUE KEY`ステートメントが正しく複製されない問題を修正[＃10890](https://github.com/pingcap/tiflow/issues/10890) @ [asddongmen](https://github.com/asddongmen)
        -   `TIMEZONE`種類のデフォルト値が正しいタイムゾーンに従って設定されない問題を修正 [＃10931](https://github.com/pingcap/tiflow/issues/10931) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Lightning

        -   PDLeaderを強制終了すると、 TiDB Lightningがデータインポート中に`invalid store ID 0`エラーを報告する問題を修正しました。 [＃50501](https://github.com/pingcap/tidb/issues/50501) @ [Leavrth](https://github.com/Leavrth)
        -   TiDB Lightning Grafanaダッシュボードでデータが欠落する問題を修正 [＃43357](https://github.com/pingcap/tidb/issues/43357) @ [lichunzhu](https://github.com/lichunzhu)
        -   TiDB Lightningがサーバーモードでログに機密情報を出力する可能性がある問題を修正しました [＃36374](https://github.com/pingcap/tidb/issues/36374) @ [kennytm](https://github.com/kennytm)
        -   TiDB Lightning を使用して`SHARD_ROW_ID_BITS`と`AUTO_ID_CACHE=1`両方が設定されたテーブルをインポートした後、TiDB がAUTO_INCREMENT ID を生成できず、エラー`Failed to read auto-increment value from storage engine`を報告する問題を修正しました。 [＃52654](https://github.com/pingcap/tidb/issues/52654) @ [D3Hunter](https://github.com/D3Hunter)

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [tangenta](https://github.com/tangenta)

    -   TiDB Binlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正しました[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [tangenta](https://github.com/tangenta)
