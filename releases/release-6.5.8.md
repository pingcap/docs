---
title: TiDB 6.5.8 Release Notes
summary: TiDB 6.5.8は2024年2月2日にリリースされました。このバージョンでは、TiKVの構成項目`gc.num-threads`が導入され、TiFlashやツールの改善が行われました。さらに、多数のバグが修正されています。PDやTiKV、TiFlash、ツールなど、さまざまな部分で修正が行われています。
---

# TiDB 6.5.8 リリースノート {#tidb-6-5-8-release-notes}

発売日：2024年2月2日

TiDB バージョン: 6.5.8

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.8#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiKV 構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658)を導入して、 `enable-compaction-filter`が`false` [#16101](https://github.com/tikv/tikv/issues/16101) @ [トニーシュクキ](https://github.com/tonyxuqqi)の場合の GC スレッドの数を設定します。

## 改善点 {#improvements}

-   TiFlash

    -   バックグラウンド GC タスクが読み取りおよび書き込みタスクのレイテンシーに及ぼす影響を軽減します[#8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   TiCDC

        -   サポート[変更フィードのダウンストリーム同期ステータスのクエリ](https://docs.pingcap.com/tidb/v6.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed)は、TiCDC が受信したアップストリーム データ変更がダウンストリーム システムに完全に同期されているかどうかを判断するのに役立ちます[#10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユニャン](https://github.com/hongyunyan)

    -   TiDB Lightning

        -   多数の小さなテーブル[#50105](https://github.com/pingcap/tidb/issues/50105) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときの`ALTER TABLE`のパフォーマンスを向上させます。

## バグの修正 {#bug-fixes}

-   TiDB

    -   クエリでソートを強制するオプティマイザ ヒント ( `STREAM_AGG()`など) が使用されており、その実行プランに`IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、強制ソートが無効になる可能性がある問題を修正します。
    -   ヒストグラムの境界に`NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正します。
    -   `REPLACE INTO`ステートメント[#34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   `STREAM_AGG()`の CI [#49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)の処理が間違っているため、クエリ結果が正しくない問題を修正します。
    -   間違ったパーティション プルーニング[#50082](https://github.com/pingcap/tidb/issues/50082) @ [定義2014](https://github.com/Defined2014)により、場合によってはレンジパーティションテーブルのクエリ結果が正しくなくなる問題を修正
    -   `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の自動インクリメント列を使用すると、同時競合により自動インクリメント ID 割り当てでエラーが報告される問題を修正します。
    -   多数のテーブルまたはパーティション[#50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)を処理するときに TiDB ノードで OOM エラーが発生する可能性がある問題を軽減します。
    -   DDL 所有者がネットワーク分離された後に`ADD INDEX`実行すると、TiDB 分散実行フレームワーク (DXF) でデータが矛盾する問題を修正[#49773](https://github.com/pingcap/tidb/issues/49773) @ [タンジェンタ](https://github.com/tangenta)
    -   panicに適用演算子が含まれており、 `fatal error: concurrent map writes`エラーが発生すると TiDB がパニックになる可能性がある問題を修正します[#50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)
    -   `COM_STMT_EXECUTE`を介して実行された`COMMIT`または`ROLLBACK`操作が、タイムアウト[#49151](https://github.com/pingcap/tidb/issues/49151) @ [ジグアン](https://github.com/zyguan)になったトランザクションを終了できない問題を修正します。
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`を実行すると、エラー[#49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)ではなく成功メッセージが誤って返される問題を修正します。
    -   `ORDER BY`句を使用して`UNIQUE`インデックス ルックアップを実行すると、エラー[#49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキースプ](https://github.com/jackysp)が発生する可能性がある問題を修正します。
    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス ルックアップを使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正[#50012](https://github.com/pingcap/tidb/issues/50012) @ [タンジェンタ](https://github.com/tangenta)
    -   短期間に多数の`CREATE TABLE`ステートメントを実行するときに、TiDB が新しい統計メタデータを同時に確立できない可能性がある問題を修正します[#36004](https://github.com/pingcap/tidb/issues/36004) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   `LEADING`ヒントが`UNION ALL`のステートメント[#50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正
    -   古いインターフェースを使用すると、テーブル[#49751](https://github.com/pingcap/tidb/issues/49751) @ [ホーキングレイ](https://github.com/hawkingrei)のメタデータが不整合になる可能性がある問題を修正
    -   `UNION ALL`ステートメント[#50068](https://github.com/pingcap/tidb/issues/50068) @ [ホーキングレイ](https://github.com/hawkingrei)で共通ヒントが有効にならない問題を修正
    -   定数伝播[#49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理すると、TiDB が間違ったクエリ結果を返す問題を修正

-   TiKV

    -   gRPC スレッドが`is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanicになる可能性がある問題を修正
    -   TiKV がブラジルとエジプトのタイムゾーンを誤って変換する問題を修正します[#16220](https://github.com/tikv/tikv/issues/16220) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   TiDB と TiKV が`DECIMAL`算術乗算切り捨て[#16268](https://github.com/tikv/tikv/issues/16268) @ [ソロッツグ](https://github.com/solotzg)を処理するときに一貫性のない結果を生成する可能性がある問題を修正します。

-   PD

    -   `pd-ctl`を使用してリーダーなしでリージョンをクエリすると、PD がpanic[#7630](https://github.com/tikv/pd/issues/7630) @ [ルルンクス](https://github.com/rleungx)になる可能性がある問題を修正します。

-   TiFlash

    -   `lowerUTF8`および`upperUTF8`関数で、大文字と小文字が異なる文字が異なるバイト[#8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリチ](https://github.com/gengliqi)を占めることができない問題を修正します。
    -   Null 許容カラムを Null 非許容カラム[#8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)に変更する`ALTER TABLE ... MODIFY COLUMN ... NOT NULL`の実行後にTiFlashがパニックになる問題を修正
    -   クエリ終了後、 TiFlash上の多数のタスクが同時にキャンセルされると同時データの競合によりTiFlashがクラッシュする問題を修正[#7432](https://github.com/pingcap/tiflash/issues/7432) @ [シーライズ](https://github.com/SeaRise)

-   ツール

    -   バックアップと復元 (BR)

        -   古いバージョン[#49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポインター](https://github.com/3pointer)のバックアップからデータを復元すると`Unsupported collation`エラーが報告される問題を修正します。
        -   S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @ [レヴルス](https://github.com/Leavrth)からファイルの内容を読み取るときにエラーが発生した場合にBR が再試行できない問題を修正
        -   同じノード[#50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポインター](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログのバックアップが停止する問題を修正

    -   TiCDC

        -   `ignore-event`で構成された`add table partition`イベントをフィルタリングした後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[#10524](https://github.com/pingcap/tiflow/issues/10524) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートしない問題を修正します。
        -   上流テーブル[#10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`が実行された後、変更フィードがエラーを報告する問題を修正します。
        -   極端なケース[#10157](https://github.com/pingcap/tiflow/issues/10157) @ [スドジ](https://github.com/sdojjy)でチェンジフィード`resolved ts`が進まない問題を修正
        -   複数の変更フィード[#10430](https://github.com/pingcap/tiflow/issues/10430) @ [CharlesCheung96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正

    -   TiDB Lightning

        -   EBS BR [#49517](https://github.com/pingcap/tidb/issues/49517) @ [ミタルリシャブ](https://github.com/mittalrishabh)が実行されているときにTiDB Lightning がデータのインポートに失敗する可能性がある問題を修正
        -   TiDB Lightning がバッチ[#50198](https://github.com/pingcap/tidb/issues/50198) @ [D3ハンター](https://github.com/D3Hunter)でファイルを取り込むときにデータが失われる可能性がある問題を修正
