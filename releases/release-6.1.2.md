---
title: TiDB 6.1.2 Release Notes
summary: TiDB 6.1.2は2022年10月24日にリリースされました。このリリースには、TiDB、TiKV、ツール、PD、 TiFlashの改善と、各コンポーネントにおける様々な問題に対するバグ修正が含まれています。改善点には、配置ルールとTiFlashレプリカの同時設定、各種設定のサポート、パフォーマンスの向上が含まれます。バグ修正では、権限の不適切なクリーンアップ、出力の誤り、クエリの失敗、パフォーマンスの問題などが修正されています。
---

# TiDB 6.1.2 リリースノート {#tidb-6-1-2-release-notes}

発売日：2022年10月24日

TiDBバージョン: 6.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 改善点 {#improvements}

-   ティドブ

    -   1 つのテーブル[＃37171](https://github.com/pingcap/tidb/issues/37171) @ [lcwangchao](https://github.com/lcwangchao)で配置ルールとTiFlashレプリカを同時に設定できるようにします

-   TiKV

    -   1 つのピアが到達不能になった後にRaftstore が過剰なメッセージをブロードキャストすることを回避するための`unreachable_backoff`項目の設定をサポートします[＃13054](https://github.com/tikv/tikv/issues/13054) @ [5kbps](https://github.com/5kbpers)
    -   RocksDB 書き込みストール設定をフロー制御しきい値[＃13467](https://github.com/tikv/tikv/issues/13467) @ [タボキ](https://github.com/tabokie)より小さい値に設定できるようになりました。

-   ツール

    -   TiDB Lightning

        -   チェックサム中に再試行可能なエラーを追加して堅牢性を向上させる[＃37690](https://github.com/pingcap/tidb/issues/37690) @ [D3ハンター](https://github.com/D3Hunter)

    -   TiCDC

        -   解決されたTSをバッチ[＃7078](https://github.com/pingcap/tiflow/issues/7078) @ [スドジ](https://github.com/sdojjy)で処理することでリージョンワーカーのパフォーマンスを向上

## バグ修正 {#bug-fixes}

-   ティドブ

    -   データベースレベルの権限が誤ってクリーンアップされる問題を修正[＃38363](https://github.com/pingcap/tidb/issues/38363) @ [ドヴェーデン](https://github.com/dveeden)
    -   `SHOW CREATE PLACEMENT POLICY` [＃37526](https://github.com/pingcap/tidb/issues/37526) @ [xhebox](https://github.com/xhebox)の誤った出力を修正
    -   1 つの PD ノードがダウンすると、他の PD ノード[＃35708](https://github.com/pingcap/tidb/issues/35708) @ [接線](https://github.com/tangenta)を再試行しないため、 `information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正しました。
    -   `UNION`演算子が予期しない空の結果[＃36903](https://github.com/pingcap/tidb/issues/36903) @ [天菜麻緒](https://github.com/tiancaiamao)を返す可能性がある問題を修正しました
    -   TiFlash [＃37254](https://github.com/pingcap/tidb/issues/37254) @ [wshwsh12](https://github.com/wshwsh12)のパーティションテーブルでダイナミックモードを有効にしたときに発生する誤った結果を修正しました。
    -   リージョンが[＃37141](https://github.com/pingcap/tidb/issues/37141) @ [スティクナーフ](https://github.com/sticnarf)にマージされたときにリージョンキャッシュが時間内にクリーンアップされない問題を修正しました
    -   KVクライアントが不要なpingメッセージ[＃36861](https://github.com/pingcap/tidb/issues/36861) @ [ジャッキーsp](https://github.com/jackysp)を送信する問題を修正しました
    -   DMLエグゼキュータを使用した`EXPLAIN ANALYZE`文が、トランザクションコミットが完了する前に結果を返す可能性がある問題を修正しました[＃37373](https://github.com/pingcap/tidb/issues/37373) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `ORDER BY`節に相関サブクエリ[＃18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が含まれている場合に`GROUP CONCAT` with `ORDER BY`が失敗する可能性がある問題を修正しました。
    -   `UPDATE`文に共通テーブル式 (CTE) [＃35758](https://github.com/pingcap/tidb/issues/35758) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合に`Can't find column`が報告される問題を修正しました
    -   特定のシナリオで予期しないエラー[＃37187](https://github.com/pingcap/tidb/issues/37187) `EXECUTE` [思い出させる](https://github.com/Reminiscent)

-   ティクブ

    -   リージョン[＃13553](https://github.com/tikv/tikv/issues/13553)と[スペードA-タン](https://github.com/SpadeA-Tang)にわたるバッチ スナップショットによってスナップショット データが不完全になる可能性がある問題を修正しました。
    -   フロー制御が有効で、 `level0_slowdown_trigger`明示的に[＃11424](https://github.com/tikv/tikv/issues/11424) @ [コナー1996](https://github.com/Connor1996)に設定されている場合に QPS が低下する問題を修正しました
    -   TiKV が Web ID プロバイダーからエラーを取得し、デフォルトのプロバイダー[＃13122](https://github.com/tikv/tikv/issues/13122) @ [3ポイントシュート](https://github.com/3pointer)にフェイルバックしたときに、権限拒否エラーが発生する問題を修正しました。
    -   TiKVインスタンスが分離されたネットワーク環境にある場合、TiKVサービスが数分間利用できなくなる問題を修正[＃12966](https://github.com/tikv/tikv/issues/12966) @ [コスベン](https://github.com/cosven)

-   PD

    -   リージョンツリーの統計が不正確になる可能性がある問題を修正[＃5318](https://github.com/tikv/pd/issues/5318) @ [rleungx](https://github.com/rleungx)
    -   TiFlash学習者レプリカが作成されない可能性がある問題を修正[＃5401](https://github.com/tikv/pd/issues/5401) @ [ハンダンDM](https://github.com/HunDunDM)
    -   PD がダッシュボード プロキシ リクエスト[＃5321](https://github.com/tikv/pd/issues/5321) @ [ハンダンDM](https://github.com/HunDunDM)を正しく処理できない問題を修正しました
    -   不健全なリージョンがPDpanic[＃5491](https://github.com/tikv/pd/issues/5491) @ [ノルーシュ](https://github.com/nolouch)を引き起こす可能性がある問題を修正

-   TiFlash

    -   I/Oリミッターが、一括書き込み後のクエリ要求のI/Oスループットを誤って抑制し、クエリパフォーマンスが低下する問題を修正しました[＃5801](https://github.com/pingcap/tiflash/issues/5801) @ [ジンヘリン](https://github.com/JinheLin)
    -   クエリがキャンセルされたときにウィンドウ関数によってTiFlashがクラッシュする可能性がある問題を修正[＃5814](https://github.com/pingcap/tiflash/issues/5814) @ [シーライズ](https://github.com/SeaRise)
    -   `NULL`値[＃5859](https://github.com/pingcap/tiflash/issues/5859) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を含む列でプライマリインデックスを作成した後に発生するpanicを修正しました。

-   ツール

    -   TiDB Lightning

        -   無効なメトリックカウンタ[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [D3ハンター](https://github.com/D3Hunter)によって引き起こされるTiDB Lightningのpanicを修正

    -   TiDB データ移行 (DM)

        -   DMタスクが同期ユニットに入り、中断されると上流のテーブル構造情報が失われる問題を修正[＃7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)
        -   チェックポイント[＃5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)を保存するときに SQL ステートメントを分割して、大規模なトランザクション エラーを修正します。
        -   DM事前チェックに`INFORMATION_SCHEMA` [＃7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)の`SELECT`権限が必要になる問題を修正
        -   fast/fullバリデータ[＃7241](https://github.com/pingcap/tiflow/issues/7241) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)を使用して DM タスクを実行した後に DM ワーカーがデッドロック エラーをトリガーする問題を修正しました
        -   DMが`Specified key was too long`エラー[＃5315](https://github.com/pingcap/tiflow/issues/5315) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正
        -   レプリケーション[＃7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正しました

    -   TiCDC

        -   CDCサーバーが完全に起動する前に HTTP 要求を受信すると、CDCサーバーがpanic可能性がある問題を修正しました[＃6838](https://github.com/pingcap/tiflow/issues/6838) @ [アズドンメン](https://github.com/asddongmen)
        -   アップグレード[＃7235](https://github.com/pingcap/tiflow/issues/7235) @ [ハイ・ラスティン](https://github.com/Rustin170506)中のログ フラッディングの問題を修正
        -   changefeed の redo ログファイルが誤って削除される可能性がある問題を修正[＃6413](https://github.com/pingcap/tiflow/issues/6413) @ [ハイ・ラスティン](https://github.com/Rustin170506)
        -   etcdトランザクションでコミットされる操作が多すぎるとTiCDCが利用できなくなる問題を修正[＃7131](https://github.com/pingcap/tiflow/issues/7131) @ [ハイ・ラスティン](https://github.com/Rustin170506)
        -   REDOログ内の非再入可能DDL文が2回実行されるとデータの不整合が発生する可能性がある問題を修正[＃6927](https://github.com/pingcap/tiflow/issues/6927) @ [ヒック](https://github.com/hicqu)

    -   バックアップと復元 (BR)

        -   復元中に同時実行が大きすぎる設定になっているため、領域のバランスが取れていない問題を修正しました[＃37549](https://github.com/pingcap/tidb/issues/37549) @ [3ポイントシュート](https://github.com/3pointer)
        -   外部storage[＃37469](https://github.com/pingcap/tidb/issues/37469) @ [モクイシュル28](https://github.com/MoCuishle28)の認証キーに特殊文字が含まれている場合にバックアップと復元が失敗する可能性がある問題を修正しました
