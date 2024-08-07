---
title: TiDB 6.5.10 Release Notes
summary: TiDB 6.5.10 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.5.10 リリースノート {#tidb-6-5-10-release-notes}

発売日: 2024年6月20日

TiDB バージョン: 6.5.10

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   以前のバージョンでは、 `UPDATE`変更を含むトランザクションを処理するときに、 `UPDATE`イベントで主キーまたは非 NULL の一意のインデックス値が変更されると、TiCDC はこのイベントを`DELETE`のイベントと`INSERT`イベントに分割していました。v6.5.10 以降では、MySQL シンクを使用する場合、 `UPDATE`の変更のトランザクション`commitTS`が TiCDC `thresholdTS` (TiCDC が対応するテーブルをダウンストリームに複製し始めるときに PD から取得される現在のタイムスタンプ) より小さい場合、TiCDC は`UPDATE`イベントを`DELETE`のイベントと`INSERT`のイベントに分割します。この動作変更により、TiCDC が受信した`UPDATE`のイベントの順序が誤っている可能性があり、分割された`DELETE`と`INSERT`イベントの順序が誤っている可能性があるため、ダウンストリーム データの不整合の問題に対処できます。詳細については、 [ドキュメンテーション](https://docs.pingcap.com/tidb/v6.5/ticdc-split-update-behavior#split-update-events-for-mysql-sinks)を参照してください[＃10918](https://github.com/pingcap/tiflow/issues/10918) @ [リデズ](https://github.com/lidezhu)
-   TiDB Lightning `strict-format`を使用して CSV ファイルをインポートする場合は、行末文字を設定する必要があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [ランス6716](https://github.com/lance6716)

## 改善点 {#improvements}

-   ティビ

    -   `SHOW CREATE TABLE` [＃52939](https://github.com/pingcap/tidb/issues/52939) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の出力に表示される式のデフォルト値の MySQL 互換性を改善しました
    -   MPP ロード バランシング中にリージョンのないストアを削除する[＃52313](https://github.com/pingcap/tidb/issues/52313) @ [翻訳者](https://github.com/xzhangxian1008)

-   ティクヴ

    -   TiKV [＃16680](https://github.com/tikv/tikv/issues/16680) @ [ライクサッシネーター](https://github.com/LykxSassinator)のシャットダウン速度を加速する
    -   下流の CDC イベントレイテンシー問題のトラブルシューティングを容易にするために、CDC イベントを処理するためのキュー時間の監視メトリックを追加します[＃16282](https://github.com/tikv/tikv/issues/16282) @ [ヒック](https://github.com/hicqu)

-   ツール

    -   バックアップと復元 (BR)

        -   BR はデータ復旧中に空の SST ファイルをクリーンアップします[＃16005](https://github.com/tikv/tikv/issues/16005) @ [リーヴルス](https://github.com/Leavrth)
        -   DNSエラーによる失敗の再試行回数を[＃53029](https://github.com/pingcap/tidb/issues/53029)から[ユジュンセン](https://github.com/YuJuncen)に増やす
        -   リージョン[＃54017](https://github.com/pingcap/tidb/issues/54017)のリーダー不在による失敗の再試行回数を[リーヴルス](https://github.com/Leavrth)に増やす

    -   ティCDC

        -   ダウンストリームがメッセージキュー（MQ）またはクラウドstorageの場合、生のイベントを直接出力することをサポートします[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   REDOログを使用してデータリカバリ中のメモリの安定性を向上させ、OOM [＃10900](https://github.com/pingcap/tiflow/issues/10900) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)の可能性を低減します。
        -   トランザクション競合シナリオでのデータレプリケーションの安定性が大幅に向上し、パフォーマンスが最大10倍向上します[＃10896](https://github.com/pingcap/tiflow/issues/10896) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグの修正 {#bug-fixes}

-   ティビ

    -   統計の初期化中にメタデータをクエリするとOOM [＃52219](https://github.com/pingcap/tidb/issues/52219) @ [ホーキングレイ](https://github.com/hawkingrei)が発生する可能性がある問題を修正しました。
    -   `AUTO_ID_CACHE=1`自動増分列を含むテーブルで、 `auto_increment_increment`および`auto_increment_offset`システム変数をデフォルト以外の値に設定すると、不正な自動増分 ID 割り当て[＃52622](https://github.com/pingcap/tidb/issues/52622) @ [天菜まお](https://github.com/tiancaiamao)が発生する可能性がある問題を修正しました。
    -   `RESTORE`ステートメントを使用して`AUTO_ID_CACHE=1`テーブルを復元すると`Duplicate entry`エラー[＃52680](https://github.com/pingcap/tidb/issues/52680) @ [天菜まお](https://github.com/tiancaiamao)が発生する可能性がある問題を修正しました
    -   `STATE`のフィールドのうち`size`が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`のテーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [翻訳](https://github.com/cfzjywxk)
    -   外部キー[＃53652](https://github.com/pingcap/tidb/issues/53652) @ [ホーキングレイ](https://github.com/hawkingrei)を持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました
    -   クエリの同時実行性が高い場合に統計同期読み込みメカニズムが予期せず失敗する可能性がある問題を修正[＃52294](https://github.com/pingcap/tidb/issues/52294) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   GlobalStatsの`Distinct_count`情報が間違っている可能性がある問題を修正[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   TiDB [＃37548](https://github.com/pingcap/tidb/issues/37548) @ [ホーキングレイ](https://github.com/hawkingrei)を再起動した後、主キー列統計のヒストグラムと TopN がロードされない問題を修正しました。
    -   クエリ内の特定のフィルター条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) [＃53594](https://github.com/pingcap/tidb/issues/53594) [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [ヤンケオ](https://github.com/YangKeao)を報告する可能性がある問題を修正しました。
    -   `?`引数を含む`CONV` `EXECUTE`式を持つ`PREPARE`ステートメントを複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   オプティマイザーヒント[＃53767](https://github.com/pingcap/tidb/issues/53767) @ [ホーキングレイ](https://github.com/hawkingrei)使用時の誤った警告情報の問題を修正
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [クレイジーcs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   DDL ステートメントが誤って etcd を使用し、タスクが[＃52335](https://github.com/pingcap/tidb/issues/52335) @ [翻訳:](https://github.com/wjhuang2016)でキューに入れられる問題を修正しました。
    -   式インデックス[＃51431](https://github.com/pingcap/tidb/issues/51431) @ [うわー](https://github.com/ywqzzy)の名前を変更する`RENAME INDEX`を実行すると、内部列の名前が変更されない問題を修正しました。
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラー[＃53673](https://github.com/pingcap/tidb/issues/53673) @ [タンジェンタ](https://github.com/tangenta)が発生する可能性がある問題を修正
    -   JOIN条件に暗黙的な型変換[＃46556](https://github.com/pingcap/tidb/issues/46556) @ [qw4990](https://github.com/qw4990)が含まれている場合にTiDBがpanic可能性がある問題を修正
    -   ネットワークの問題により DDL 操作が停止する問題を修正[＃47060](https://github.com/pingcap/tidb/issues/47060) @ [翻訳:](https://github.com/wjhuang2016)
    -   IndexJoin が Left Outer Anti Semi 型[＃52902](https://github.com/pingcap/tidb/issues/52902) @ [いいえ](https://github.com/yibin87)のハッシュ値を計算するときに重複行を生成する問題を修正しました。
    -   `ALL`関数に含まれるサブクエリが誤った結果を引き起こす可能性がある問題を修正[＃52755](https://github.com/pingcap/tidb/issues/52755) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `TIMESTAMPADD()`関数が誤った結果を返す問題を修正[＃41052](https://github.com/pingcap/tidb/issues/41052) @ [翻訳者](https://github.com/xzhangxian1008)
    -   `tidb_mem_quota_analyze`が有効になっていて、統計の更新に使用されるメモリが制限[＃52601](https://github.com/pingcap/tidb/issues/52601) @ [ホーキングレイ](https://github.com/hawkingrei)を超えると TiDB がクラッシュする可能性がある問題を修正しました
    -   `UPDATE`リスト内のサブクエリによって TiDB がpanicを起こす可能性がある問題を修正[＃52687](https://github.com/pingcap/tidb/issues/52687) @ [ウィノロス](https://github.com/winoros)
    -   述語[＃45783](https://github.com/pingcap/tidb/issues/45783) @ [ホーキングレイ](https://github.com/hawkingrei)の`Longlong`型のオーバーフローの問題を修正
    -   一意のインデックス[＃52914](https://github.com/pingcap/tidb/issues/52914) @ [翻訳:](https://github.com/wjhuang2016)を追加するときに同時 DML 操作によって発生するデータ インデックスの不整合の問題を修正しました。
    -   インデックスデータ[＃47115](https://github.com/pingcap/tidb/issues/47115) @ [ジグアン](https://github.com/zyguan)を解析するときに TiDB がpanicになる可能性がある問題を修正しました
    -   スライスの浅いコピーを使用せずに列を整理すると TiDB がpanicを起こす可能性がある問題を修正[＃52768](https://github.com/pingcap/tidb/issues/52768) @ [ウィノロス](https://github.com/winoros)
    -   再帰 CTE [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [ホーキングレイ](https://github.com/hawkingrei)でビューの使用が機能しない問題を修正
    -   `LEADING`ヒントがブロック エイリアス[＃44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)のクエリをサポートしない問題を修正しました
    -   相関サブクエリ[＃52777](https://github.com/pingcap/tidb/issues/52777) @ [いいえ](https://github.com/yibin87)の TopN 演算子の誤った結果を修正
    -   列の不安定な一意の ID により、 `UPDATE`ステートメントがエラー[＃53236](https://github.com/pingcap/tidb/issues/53236) @ [ウィノロス](https://github.com/winoros)を返す可能性がある問題を修正しました。
    -   TiDB がオフラインになっているTiFlashノードにプローブ要求を送信し続ける問題を修正[＃46602](https://github.com/pingcap/tidb/issues/46602) @ [ジグアン](https://github.com/zyguan)
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   AutoIDLeaderの変更により、 `AUTO_ID_CACHE=1` [＃52600](https://github.com/pingcap/tidb/issues/52600) @ [天菜まお](https://github.com/tiancaiamao)の場合に自動増分列の値が減少する可能性がある問題を修正しました。
    -   BIGINT 以外の符号なし整数を文字列/小数と比較すると誤った結果が生成される可能性がある問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)
    -   `FLOAT`型から`UNSIGNED`型へのデータ変換で誤った結果が返される問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `VAR_SAMP()`ウィンドウ関数[＃52933](https://github.com/pingcap/tidb/issues/52933) @ [ハイラスティン](https://github.com/hi-rustin)として使用できない問題を修正
    -   間違った TableDual プランにより空のクエリ結果[＃50051](https://github.com/pingcap/tidb/issues/50051) @ [猫のみ](https://github.com/onlyacat)が発生する問題を修正
    -   TiDB の同期的な統計読み込みメカニズムが空の統計の読み込みを無期限に再試行し、 `fail to get stats version for this histogram` log [＃52657](https://github.com/pingcap/tidb/issues/52657) @ [ホーキングレイ](https://github.com/hawkingrei)を出力問題を修正しました。
    -   空の投影により TiDB がpanicになる問題を修正[＃49109](https://github.com/pingcap/tidb/issues/49109) @ [ウィノロス](https://github.com/winoros)
    -   TopN演算子が誤ってプッシュダウンされる可能性がある問題を修正[＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)
    -   常に`true` [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [エルサ0520](https://github.com/elsa0520)の述語を持つ`SHOW ERRORS`ステートメントを実行すると TiDB がパニックになる問題を修正しました。
    -   プラン キャッシュ シナリオ[＃51407](https://github.com/pingcap/tidb/issues/51407) @ [翻訳:](https://github.com/wjhuang2016)でメタデータ ロックが DDL 操作の実行を阻止できない問題を修正しました。

-   ティクヴ

    -   1 つの TiKV ノードでの遅い`check-leader`操作により、他の TiKV ノードでの`resolved-ts`正常に[＃15999](https://github.com/tikv/tikv/issues/15999) @ [クレイジーcs520](https://github.com/crazycs520)に進まなくなる問題を修正しました。
    -   クエリ内の`CONV()`関数が数値システム変換中にオーバーフローし、TiKVpanic[＃16969](https://github.com/tikv/tikv/issues/16969) @ [ゲンリキ](https://github.com/gengliqi)が発生する問題を修正しました。
    -   不安定なテストケースの問題を修正し、各テストが独立した一時ディレクトリを使用するようにして、オンライン構成の変更が他のテストケースに影響しないようにします[＃16871](https://github.com/tikv/tikv/issues/16871) @ [栄光](https://github.com/glorv)
    -   `DECIMAL`型の小数部が[＃16913](https://github.com/tikv/tikv/issues/16913) @ [ゲンリキ](https://github.com/gengliqi)場合に正しくない問題を修正
    -   古いリージョンピアがGCメッセージ[＃16504](https://github.com/tikv/tikv/issues/16504) @ [クレイジーcs520](https://github.com/crazycs520)を無視するとresolve-tsがブロックされる問題を修正

-   PD

    -   展開された 2 つのデータセンター間でリーダーを切り替えるとLeaderが失敗する問題を修正[＃7992](https://github.com/tikv/pd/issues/7992) @ [トンスネークリン](https://github.com/TonsnakeLin)
    -   配置ルール[＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)を使用すると、ダウンしたピアが回復しない可能性がある問題を修正しました。
    -   PDの`Filter target`監視メトリックが散布範囲情報を提供しない問題を修正[＃8125](https://github.com/tikv/pd/issues/8125) @ [ヒューシャープ](https://github.com/HuSharp)

-   TiFlash

    -   データベース間で`ALTER TABLE ... EXCHANGE PARTITION`実行した後にTiFlash がスキーマの同期に失敗する可能性がある問題を修正[＃7296](https://github.com/pingcap/tiflash/issues/7296) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   空のキー範囲を持つクエリがTiFlash上で読み取りタスクを正しく生成できず、 TiFlashクエリ[＃9108](https://github.com/pingcap/tiflash/issues/9108) @ [ジンヘリン](https://github.com/JinheLin)がブロックされる可能性がある問題を修正しました。
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlashをクラッシュさせる可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [うわー](https://github.com/wshwsh12)
    -   クラスターを v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードするときに、 TiFlashメタデータが破損してプロセスがpanicになる可能性がある問題を修正しました[＃9039](https://github.com/pingcap/tiflash/issues/9039) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   同時実行性の高い読み取りシナリオでTiFlash が一時的に誤った結果を返す可能性がある問題を修正[＃8845](https://github.com/pingcap/tiflash/issues/8845) @ [ジンヘリン](https://github.com/JinheLin)

-   ツール

    -   バックアップと復元 (BR)

        -   テストケース`TestGetTSWithRetry`実行に時間がかかりすぎる問題を修正[＃52547](https://github.com/pingcap/tidb/issues/52547) @ [リーヴルス](https://github.com/Leavrth)
        -   BRを使用してデータを復元する場合、または物理インポート モードでTiDB Lightningを使用してデータをインポートする場合に、PD から取得されたリージョンにLeaderがない問題を修正しました[＃51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @ [リーヴルス](https://github.com/Leavrth)
        -   PD 接続障害により、ログ バックアップ アドバンサ所有者が配置されている TiDB インスタンスがpanicになる可能性がある問題を修正しました[＃52597](https://github.com/pingcap/tidb/issues/52597) @ [ユジュンセン](https://github.com/YuJuncen)
        -   ログバックアップタスクを一時停止、停止、再構築した後、タスクの状態は正常であるが、チェックポイントが[＃53047](https://github.com/pingcap/tidb/issues/53047) @ [リドリス](https://github.com/RidRisR)に進まない問題を修正しました。
        -   TiKVノード[＃50566](https://github.com/pingcap/tidb/issues/50566) @ [リーヴルス](https://github.com/Leavrth)にリーダーがいないためにデータの復元が遅くなる問題を修正
        -   TiKV の再起動により、ログ バックアップのグローバル チェックポイントが実際のバックアップ ファイルの書き込みポイントよりも先に進められ、少量のバックアップ データが失われる可能性がある問題を修正しました[＃16809](https://github.com/tikv/tikv/issues/16809) @ [ユジュンセン](https://github.com/YuJuncen)
        -   PDリーダーの転送により、データ[＃53724](https://github.com/pingcap/tidb/issues/53724) @ [リーヴルス](https://github.com/Leavrth)を復元するときにBRがpanicになる可能性がある問題を修正しました。
        -   PD [＃17020](https://github.com/tikv/tikv/issues/17020) @ [ユジュンセン](https://github.com/YuJuncen)へのネットワーク接続が不安定な状態で一時停止中のログ バックアップ タスクを再開すると TiKV がpanicになる可能性がある問題を修正しました。
        -   アドバンサー所有者の移行[＃53561](https://github.com/pingcap/tidb/issues/53561) @ [リドリス](https://github.com/RidRisR)後にログ バックアップが一時停止される可能性がある問題を修正しました
        -   復元プロセス中に複数のネストされた再試行が原因でBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [リドリス](https://github.com/RidRisR)

    -   ティCDC

        -   ダウンストリーム データベースのパスワードが Base64 でエンコードされている場合、TiCDC が同期ポイントを有効にして変更フィードを作成できない問題を修正しました[＃10516](https://github.com/pingcap/tiflow/issues/10516) @ [アズドンメン](https://github.com/asddongmen)
        -   `DROP PRIMARY KEY`と`DROP UNIQUE KEY`ステートメントが正しく複製されない問題を修正[＃10890](https://github.com/pingcap/tiflow/issues/10890) @ [アズドンメン](https://github.com/asddongmen)
        -   `TIMEZONE`種類のデフォルト値が正しいタイムゾーン[＃10931](https://github.com/pingcap/tiflow/issues/10931) @ [3エースショーハンド](https://github.com/3AceShowHand)に従って設定されない問題を修正

    -   TiDB Lightning

        -   PDLeaderを強制終了すると、 TiDB Lightningがデータインポート[#50501](https://github.com/pingcap/tidb/issues/50501) @ [リーヴルス](https://github.com/Leavrth)中に`invalid store ID 0`エラーを報告する問題を修正しました。
        -   TiDB Lightning Grafanaダッシュボード[＃43357](https://github.com/pingcap/tidb/issues/43357) @ [リチュンジュ](https://github.com/lichunzhu)でデータが欠落する問題を修正
        -   TiDB Lightning がサーバーモード[＃36374](https://github.com/pingcap/tidb/issues/36374) @ [ケニー](https://github.com/kennytm)でログに機密情報を出力する可能性がある問題を修正しました。
        -   TiDB Lightning [＃52654](https://github.com/pingcap/tidb/issues/52654) @ [D3ハンター](https://github.com/D3Hunter)を使用して`SHARD_ROW_ID_BITS`と`AUTO_ID_CACHE=1`両方が設定されたテーブルをインポートした後、TiDB が自動増分 ID の生成に失敗し、エラー`Failed to read auto-increment value from storage engine`を報告する問題を修正しました。

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [タンジェンタ](https://github.com/tangenta)

    -   TiDBBinlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`の実行中に行を削除するとエラー`data and columnID count not match`報告される可能性がある問題を修正[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [タンジェンタ](https://github.com/tangenta)
