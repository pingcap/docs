---
title: TiDB 6.5.8 Release Notes
summary: TiDB 6.5.8 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.8 リリースノート {#tidb-6-5-8-release-notes}

発売日：2024年2月2日

TiDB バージョン: 6.5.8

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiKV構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658)を導入して、 `enable-compaction-filter`が`false` [＃16101](https://github.com/tikv/tikv/issues/16101) @ [トニー・シュッキ](https://github.com/tonyxuqqi)の場合のGCスレッド数を設定します。

## 改善点 {#improvements}

-   TiFlash

    -   バックグラウンド GC タスクによる読み取りおよび書き込みタスクのレイテンシーへの影響を軽減[＃8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   TiCDC

        -   サポート[チェンジフィードの下流同期ステータスの照会](https://docs.pingcap.com/tidb/v6.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed) 、TiCDC が受信した上流データの変更が下流システムに完全に同期されているかどうかを判断するのに役立ちます[＃10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユニャン](https://github.com/hongyunyan)

    -   TiDB Lightning

        -   多数の小さなテーブルをインポートする際のパフォーマンスを向上`ALTER TABLE` [＃50105](https://github.com/pingcap/tidb/issues/50105) @ [D3ハンター](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   TiDB

    -   クエリがソートを強制するオプティマイザヒント（ `STREAM_AGG()`など）を使用し、その実行プランに`IndexMerge` [＃49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、強制ソートが無効になる可能性がある問題を修正しました。
    -   ヒストグラムの境界に`NULL` [＃49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正しました。
    -   `REPLACE INTO`文[＃34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   `STREAM_AGG()` CI [＃49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)を誤って処理したためにクエリ結果が正しくない問題を修正しました
    -   誤ったパーティションプルーニング[＃50082](https://github.com/pingcap/tidb/issues/50082) @ [定義2014](https://github.com/Defined2014)が原因で、範囲パーティションテーブルのクエリ結果が間違っている場合がある問題を修正しました。
    -   `AUTO_ID_CACHE=1` [＃50519](https://github.com/pingcap/tidb/issues/50519) @ [天菜まお](https://github.com/tiancaiamao)の自動インクリメント列を使用すると同時競合により自動インクリメント ID 割り当てでエラーが報告される問題を修正しました。
    -   多数のテーブルまたはパーティション[＃50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)を処理するときに TiDB ノードが OOM エラーに遭遇する可能性がある問題を軽減します。
    -   DDL所有者がネットワークから分離されている[＃49773](https://github.com/pingcap/tidb/issues/49773) @ [接線](https://github.com/tangenta)後に`ADD INDEX`実行すると、TiDB分散実行フレームワーク（DXF）でデータが不整合になる問題を修正しました
    -   クエリに Apply 演算子が含まれており、 `fatal error: concurrent map writes`エラーが[＃50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)で発生すると TiDB がpanic可能性がある問題を修正しました。
    -   `COM_STMT_EXECUTE`まで実行された`COMMIT`または`ROLLBACK`操作が、タイムアウトしたトランザクションを[＃49151](https://github.com/pingcap/tidb/issues/49151) @ [ジグアン](https://github.com/zyguan)で終了できない問題を修正しました。
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`実行すると、エラー[＃49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)ではなく、誤って成功メッセージが返される問題を修正しました。
    -   `ORDER BY`句で`UNIQUE`インデックス検索を実行するとエラー[＃49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキーsp](https://github.com/jackysp)が発生する可能性がある問題を修正しました。
    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス検索を使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正しました[＃50012](https://github.com/pingcap/tidb/issues/50012) @ [接線](https://github.com/tangenta)
    -   `LEADING`ヒントが`UNION ALL`ステートメント[＃50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正しました
    -   古いインターフェースを使用するとテーブル[＃49751](https://github.com/pingcap/tidb/issues/49751) @ [ホーキングレイ](https://github.com/hawkingrei)メタデータに不整合が生じる可能性がある問題を修正しました
    -   共通ヒントが`UNION ALL`文[＃50068](https://github.com/pingcap/tidb/issues/50068) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正
    -   定数伝播[＃49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理するときに TiDB が間違ったクエリ結果を返す問題を修正しました

-   TiKV

    -   gRPC スレッドが`is_shutdown` [＃16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanic可能性がある問題を修正しました
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   `DECIMAL`算術乗算切り捨て[＃16268](https://github.com/tikv/tikv/issues/16268) @ [ソロツグ](https://github.com/solotzg)を処理するときに TiDB と TiKV が矛盾した結果を生成する可能性がある問題を修正しました

-   PD

    -   `pd-ctl`使用してリーダーのないリージョンを照会すると、PD が[＃7630](https://github.com/tikv/pd/issues/7630) @ [rleungx](https://github.com/rleungx)でpanicになる可能性がある問題を修正しました。

-   TiFlash

    -   `lowerUTF8`と`upperUTF8`関数で、大文字と小文字が異なるバイト[＃8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリキ](https://github.com/gengliqi)を占めることができない問題を修正しました。
    -   `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`実行した後にTiFlash がパニックを起こし、NULL 可能列が[＃8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に非 NULL に変更される問題を修正しました。
    -   クエリを終了した後、 TiFlash上の多数のタスクが同時にキャンセルされると、同時データの競合によりTiFlashがクラッシュする問題を修正[＃7432](https://github.com/pingcap/tiflash/issues/7432) @ [シーライズ](https://github.com/SeaRise)

-   ツール

    -   バックアップと復元 (BR)

        -   古いバージョン[＃49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポイントシュート](https://github.com/3pointer)のバックアップからデータを復元するときに`Unsupported collation`エラーが報告される問題を修正しました
        -   S3 [＃49942](https://github.com/pingcap/tidb/issues/49942) @ [リーヴルス](https://github.com/Leavrth)からファイル コンテンツを読み取っているときにエラーが発生した場合にBR が再試行できない問題を修正しました
        -   同じノード[＃50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポイントシュート](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログ バックアップが停止する問題を修正しました

    -   TiCDC

        -   `ignore-event`で`add table partition`イベントをフィルタリングするように構成した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に複製しない問題を修正しました。
        -   アップストリームテーブル[＃10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`が実行された後にチェンジフィードがエラーを報告する問題を修正しました
        -   極端なケースでチェンジフィード`resolved ts`が進まない問題を修正[＃10157](https://github.com/pingcap/tiflow/issues/10157) @ [スドジ](https://github.com/sdojjy)
        -   複数のチェンジフィード[＃10430](https://github.com/pingcap/tiflow/issues/10430) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正しました

    -   TiDB Lightning

        -   EBS BRが[＃49517](https://github.com/pingcap/tidb/issues/49517) @ [ミッタルリシャブ](https://github.com/mittalrishabh)で実行されているときにTiDB Lightningがデータのインポートに失敗する可能性がある問題を修正しました
        -   TiDB Lightningがファイルをバッチ[＃50198](https://github.com/pingcap/tidb/issues/50198) @ [D3ハンター](https://github.com/D3Hunter)で取り込むときにデータが失われる可能性がある問題を修正しました
