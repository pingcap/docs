---
title: TiDB 6.5.8 Release Notes
summary: TiDB 6.5.8 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.8 リリースノート {#tidb-6-5-8-release-notes}

発売日：2024年2月2日

TiDB バージョン: 6.5.8

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiKV構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658)を導入して、 `enable-compaction-filter`が`false` の場合のGCスレッド数を設定します。 [＃16101](https://github.com/tikv/tikv/issues/16101) @ [tonyxuqqi](https://github.com/tonyxuqqi)

## 改善点 {#improvements}

-   TiFlash

    -   バックグラウンド GC タスクによる読み取りおよび書き込みタスクのレイテンシーへの影響を軽減[＃8650](https://github.com/pingcap/tiflash/issues/8650) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   TiCDC

        -   サポート[チェンジフィードの下流同期ステータスの照会](https://docs.pingcap.com/tidb/v6.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed) 、TiCDC が受信した上流データの変更が下流システムに完全に同期されているかどうかを判断するのに役立ちます[＃10289](https://github.com/pingcap/tiflow/issues/10289) @ [hongyunyan](https://github.com/hongyunyan)

    -   TiDB Lightning

        -   多数の小さなテーブルをインポートする際のパフォーマンスを向上`ALTER TABLE` [＃50105](https://github.com/pingcap/tidb/issues/50105) @ [D3Hunter](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   TiDB

    -   クエリがソートを強制するオプティマイザヒント（ `STREAM_AGG()`など）を使用し、その実行プランに`IndexMerge` が含まれている場合、強制ソートが無効になる可能性がある問題を修正しました。 [＃49605](https://github.com/pingcap/tidb/issues/49605) @ [AilinKid](https://github.com/AilinKid)
    -   ヒストグラムの境界に`NULL` が含まれている場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正しました。 [＃49823](https://github.com/pingcap/tidb/issues/49823) @ [AilinKid](https://github.com/AilinKid)
    -   `REPLACE INTO`文でヒントが使用できない問題を修正 [＃34325](https://github.com/pingcap/tidb/issues/34325) @ [YangKeao](https://github.com/YangKeao)
    -   `STREAM_AGG()` CI を誤って処理したためにクエリ結果が正しくない問題を修正しました [＃49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)
    -   誤ったパーティションプルーニングが原因で、範囲パーティションテーブルのクエリ結果が間違っている場合がある問題を修正しました。 [＃50082](https://github.com/pingcap/tidb/issues/50082) @ [Defined2014](https://github.com/Defined2014)
    -   `AUTO_ID_CACHE=1` のAUTO_INCREMENT列を使用すると同時競合によりAUTO_INCREMENT ID 割り当てでエラーが報告される問題を修正しました。 [＃50519](https://github.com/pingcap/tidb/issues/50519) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   多数のテーブルまたはパーティションを処理するときに TiDB ノードが OOM エラーに遭遇する可能性がある問題を軽減します。 [＃50077](https://github.com/pingcap/tidb/issues/50077) @ [zimulala](https://github.com/zimulala)
    -   DDL所有者がネットワークから分離されている後に`ADD INDEX`実行すると、TiDB分散実行フレームワーク（DXF）でデータが不整合になる問題を修正しました [＃49773](https://github.com/pingcap/tidb/issues/49773) @ [tangenta](https://github.com/tangenta)
    -   クエリに Apply 演算子が含まれており、 `fatal error: concurrent map writes`エラーが発生すると TiDB がpanic可能性がある問題を修正しました。 [＃50347](https://github.com/pingcap/tidb/issues/50347) @ [SeaRise](https://github.com/SeaRise)
    -   `COM_STMT_EXECUTE`まで実行された`COMMIT`または`ROLLBACK`操作が、タイムアウトしたトランザクションをで終了できない問題を修正しました。 [＃49151](https://github.com/pingcap/tidb/issues/49151) @ [zyguan](https://github.com/zyguan)
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`実行すると、エラーではなく、誤って成功メッセージが返される問題を修正しました。 [＃49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)
    -   `ORDER BY`句で`UNIQUE`インデックス検索を実行するとエラーが発生する可能性がある問題を修正しました。 [＃49920](https://github.com/pingcap/tidb/issues/49920) @ [jackysp](https://github.com/jackysp)
    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス検索を使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正しました[＃50012](https://github.com/pingcap/tidb/issues/50012) @ [tangenta](https://github.com/tangenta)
    -   `LEADING`ヒントが`UNION ALL`ステートメントで有効にならない問題を修正しました [＃50067](https://github.com/pingcap/tidb/issues/50067) @ [hawkingrei](https://github.com/hawkingrei)
    -   古いインターフェースを使用するとテーブルメタデータに不整合が生じる可能性がある問題を修正しました [＃49751](https://github.com/pingcap/tidb/issues/49751) @ [hawkingrei](https://github.com/hawkingrei)
    -   共通ヒントが`UNION ALL`文で有効にならない問題を修正 [＃50068](https://github.com/pingcap/tidb/issues/50068) @ [hawkingrei](https://github.com/hawkingrei)
    -   定数伝播で`ENUM`または`SET`型を処理するときに TiDB が間違ったクエリ結果を返す問題を修正しました [＃49440](https://github.com/pingcap/tidb/issues/49440) @ [winoros](https://github.com/winoros)

-   TiKV

    -   gRPC スレッドが`is_shutdown` をチェックしているときに TiKV がpanic可能性がある問題を修正しました [＃16236](https://github.com/tikv/tikv/issues/16236) @ [pingyu](https://github.com/pingyu)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [overvenus](https://github.com/overvenus)
    -   `DECIMAL`算術乗算切り捨てを処理するときに TiDB と TiKV が矛盾した結果を生成する可能性がある問題を修正しました [＃16268](https://github.com/tikv/tikv/issues/16268) @ [solotzg](https://github.com/solotzg)

-   PD

    -   `pd-ctl`使用してリーダーのないリージョンを照会すると、PD がpanicになる可能性がある問題を修正しました。 [＃7630](https://github.com/tikv/pd/issues/7630) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   `lowerUTF8`と`upperUTF8`関数で、大文字と小文字が異なるバイトを占めることができない問題を修正しました。 [＃8484](https://github.com/pingcap/tiflash/issues/8484) @ [gengliqi](https://github.com/gengliqi)
    -   `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`実行した後にTiFlash がパニックを起こし、NULL 可能列がに非 NULL に変更される問題を修正しました。 [＃8419](https://github.com/pingcap/tiflash/issues/8419) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリを終了した後、 TiFlash上の多数のタスクが同時にキャンセルされると、同時データの競合によりTiFlashがクラッシュする問題を修正[＃7432](https://github.com/pingcap/tiflash/issues/7432) @ [SeaRise](https://github.com/SeaRise)

-   ツール

    -   Backup & Restore (BR)

        -   古いバージョンのバックアップからデータを復元するときに`Unsupported collation`エラーが報告される問題を修正しました [＃49466](https://github.com/pingcap/tidb/issues/49466) @ [3pointer](https://github.com/3pointer)
        -   S3 からファイル コンテンツを読み取っているときにエラーが発生した場合にBR が再試行できない問題を修正しました [＃49942](https://github.com/pingcap/tidb/issues/49942) @ [Leavrth](https://github.com/Leavrth)
        -   同じノードで TiKV IP アドレスを変更した後にログ バックアップが停止する問題を修正しました [＃50445](https://github.com/pingcap/tidb/issues/50445) @ [3pointer](https://github.com/3pointer)

    -   TiCDC

        -   `ignore-event`で`add table partition`イベントをフィルタリングするように構成した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリームに複製しない問題を修正しました。 [＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   アップストリームテーブルで`TRUNCATE PARTITION`が実行された後にチェンジフィードがエラーを報告する問題を修正しました [＃10522](https://github.com/pingcap/tiflow/issues/10522) @ [sdojjy](https://github.com/sdojjy)
        -   極端なケースでチェンジフィード`resolved ts`が進まない問題を修正[＃10157](https://github.com/pingcap/tiflow/issues/10157) @ [sdojjy](https://github.com/sdojjy)
        -   複数のチェンジフィードを同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正しました [＃10430](https://github.com/pingcap/tiflow/issues/10430) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Lightning

        -   EBS BRが実行されているときにTiDB Lightningがデータのインポートに失敗する可能性がある問題を修正しました [＃49517](https://github.com/pingcap/tidb/issues/49517) @ [mittalrishabh](https://github.com/mittalrishabh)
        -   TiDB Lightningがファイルをバッチで取り込むときにデータが失われる可能性がある問題を修正しました [＃50198](https://github.com/pingcap/tidb/issues/50198) @ [D3Hunter](https://github.com/D3Hunter)
