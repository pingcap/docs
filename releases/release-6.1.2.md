---
title: TiDB 6.1.2 Release Notes
summary: TiDB 6.1.2 は 2022 年 10 月 24 日にリリースされました。このリリースには、TiDB、TiKV、ツール、PD、 TiFlashの改善と、各コンポーネントのさまざまな問題に対するバグ修正が含まれています。改善には、配置ルールとTiFlashレプリカの同時設定、さまざまな設定の構成のサポート、パフォーマンスの向上が含まれます。バグ修正では、権限の誤ったクリーンアップ、誤った出力、クエリの失敗、パフォーマンスの問題などの問題に対処しています。
---

# TiDB 6.1.2 リリースノート {#tidb-6-1-2-release-notes}

発売日: 2022年10月24日

TiDB バージョン: 6.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 改善点 {#improvements}

-   ティビ

    -   1 つのテーブル[＃37171](https://github.com/pingcap/tidb/issues/37171) @ [lcwangchao](https://github.com/lcwangchao)で配置ルールとTiFlashレプリカを同時に設定できるようにする

-   ティクヴ

    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストするのを回避するための`unreachable_backoff`項目の構成をサポートします[＃13054](https://github.com/tikv/tikv/issues/13054) @ [5kbpsの](https://github.com/5kbpers)
    -   RocksDB 書き込みストール設定をフロー制御しきい値[＃13467](https://github.com/tikv/tikv/issues/13467) @ [タボキ](https://github.com/tabokie)より小さい値に設定できるようになりました。

-   ツール

    -   TiDB Lightning

        -   チェックサム中に再試行可能なエラーを追加して堅牢性を向上させる[＃37690](https://github.com/pingcap/tidb/issues/37690) @ [D3ハンター](https://github.com/D3Hunter)

    -   ティCDC

        -   解決されたTSをバッチ[＃7078](https://github.com/pingcap/tiflow/issues/7078) @ [スドジ](https://github.com/sdojjy)で処理することでリージョンワーカーのパフォーマンスを向上

## バグ修正 {#bug-fixes}

-   ティビ

    -   データベースレベルの権限が誤ってクリーンアップされる問題を修正[＃38363](https://github.com/pingcap/tidb/issues/38363) @ [ドヴェーデン](https://github.com/dveeden)
    -   `SHOW CREATE PLACEMENT POLICY` [＃37526](https://github.com/pingcap/tidb/issues/37526) @ [xhebox](https://github.com/xhebox)の誤った出力を修正
    -   1 つの PD ノードがダウンすると、他の PD ノード[＃35708](https://github.com/pingcap/tidb/issues/35708) @ [タンジェンタ](https://github.com/tangenta)を再試行しないため、 `information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正しました。
    -   `UNION`演算子が予期しない空の結果[＃36903](https://github.com/pingcap/tidb/issues/36903) @ [天菜まお](https://github.com/tiancaiamao)を返す可能性がある問題を修正しました
    -   TiFlash [＃37254](https://github.com/pingcap/tidb/issues/37254) @ [うわー](https://github.com/wshwsh12)のパーティション テーブルで動的モードを有効にしたときに発生する誤った結果を修正しました。
    -   リージョンが[＃37141](https://github.com/pingcap/tidb/issues/37141) @ [スティクナーフ](https://github.com/sticnarf)にマージされたときにリージョンキャッシュが時間内にクリーンアップされない問題を修正しました
    -   KVクライアントが不要なpingメッセージを送信する問題を修正[＃36861](https://github.com/pingcap/tidb/issues/36861) @ [ジャッキー](https://github.com/jackysp)
    -   DMLエグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正しました[＃37373](https://github.com/pingcap/tidb/issues/37373) @ [翻訳](https://github.com/cfzjywxk)
    -   `ORDER BY`節に相関サブクエリ[＃18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が含まれている場合に`GROUP CONCAT` with `ORDER BY`が失敗する可能性がある問題を修正しました。
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [＃35758](https://github.com/pingcap/tidb/issues/35758) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合に`Can't find column`が報告される問題を修正しました
    -   特定のシナリオで`EXECUTE`が予期しないエラーをスローする可能性がある問題を修正[＃37187](https://github.com/pingcap/tidb/issues/37187) @ [思い出させる](https://github.com/Reminiscent)

-   ティクヴ

    -   リージョン[＃13553](https://github.com/tikv/tikv/issues/13553)から[スペードA-タン](https://github.com/SpadeA-Tang)までのバッチ スナップショットによってスナップショット データが不完全になる可能性がある問題を修正しました。
    -   フロー制御が有効で、 `level0_slowdown_trigger`明示的に[＃11424](https://github.com/tikv/tikv/issues/11424) @ [コナー1996](https://github.com/Connor1996)に設定されている場合に QPS が低下する問題を修正しました。
    -   TiKV が Web ID プロバイダーからエラーを取得し、デフォルトのプロバイダー[＃13122](https://github.com/tikv/tikv/issues/13122) @ [3ポインター](https://github.com/3pointer)にフェールバックしたときに、権限拒否エラーが発生する問題を修正しました。
    -   TiKVインスタンスが隔離されたネットワーク環境にある場合、TiKVサービスが数分間利用できなくなる問題を修正[＃12966](https://github.com/tikv/tikv/issues/12966) @ [コスベン](https://github.com/cosven)

-   PD

    -   リージョンツリーの統計が不正確になる可能性がある問題を修正[＃5318](https://github.com/tikv/pd/issues/5318) @ [rleungx](https://github.com/rleungx)
    -   TiFlash学習レプリカが作成されない可能性がある問題を修正[＃5401](https://github.com/tikv/pd/issues/5401) @ [ハンダンDM](https://github.com/HunDunDM)
    -   PD がダッシュボード プロキシ要求[＃5321](https://github.com/tikv/pd/issues/5321) @ [ハンダンDM](https://github.com/HunDunDM)を正しく処理できない問題を修正
    -   不健全なリージョンがPDpanic[＃5491](https://github.com/tikv/pd/issues/5491) @ [ノルーシュ](https://github.com/nolouch)を引き起こす可能性がある問題を修正

-   TiFlash

    -   I/O リミッターが一括書き込み後のクエリ要求の I/O スループットを誤って制限し、クエリのパフォーマンスが低下する問題を修正しました[＃5801](https://github.com/pingcap/tiflash/issues/5801) @ [ジンヘリン](https://github.com/JinheLin)
    -   クエリがキャンセルされたときにウィンドウ関数によってTiFlashがクラッシュする可能性がある問題を修正[＃5814](https://github.com/pingcap/tiflash/issues/5814) @ [シーライズ](https://github.com/SeaRise)
    -   `NULL`値[＃5859](https://github.com/pingcap/tiflash/issues/5859) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   TiDB Lightning

        -   無効なメトリック カウンター[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [D3ハンター](https://github.com/D3Hunter)によって発生するTiDB Lightningのpanicを修正

    -   TiDB データ移行 (DM)

        -   DMタスクが同期ユニットに入り、中断されると上流のテーブル構造情報が失われる問題を修正[＃7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)
        -   チェックポイント[＃5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)を保存するときに SQL ステートメントを分割して、大規模なトランザクション エラーを修正します。
        -   DM事前チェックに`INFORMATION_SCHEMA` [＃7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)の`SELECT`権限が必要になる問題を修正
        -   高速/完全バリデータ[＃7241](https://github.com/pingcap/tiflow/issues/7241) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)で DM タスクを実行した後に DM ワーカーがデッドロック エラーをトリガーする問題を修正しました。
        -   DMが`Specified key was too long`エラー[＃5315](https://github.com/pingcap/tiflow/issues/5315) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正
        -   レプリケーション[＃7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正しました

    -   ティCDC

        -   CDCサーバーが完全に起動する前に HTTP 要求を受信すると CDCサーバーがpanicになる可能性がある問題を修正[＃6838](https://github.com/pingcap/tiflow/issues/6838) @ [アズドンメン](https://github.com/asddongmen)
        -   アップグレード[＃7235](https://github.com/pingcap/tiflow/issues/7235) @ [ハイラスティン](https://github.com/Rustin170506)中のログ フラッディング問題を修正
        -   changefeed の redo ログ ファイルが誤って削除される可能性がある問題を修正[＃6413](https://github.com/pingcap/tiflow/issues/6413) @ [ハイラスティン](https://github.com/Rustin170506)
        -   etcd トランザクションでコミットされる操作が多すぎると TiCDC が利用できなくなる問題を修正[＃7131](https://github.com/pingcap/tiflow/issues/7131) @ [ハイラスティン](https://github.com/Rustin170506)
        -   REDOログ内の非再入可能DDL文が2回実行されるとデータの不整合が発生する可能性がある問題を修正[＃6927](https://github.com/pingcap/tiflow/issues/6927) @ [ヒック](https://github.com/hicqu)

    -   バックアップと復元 (BR)

        -   復元中に同時実行性が大きすぎるために領域のバランスが取れない問題を修正[＃37549](https://github.com/pingcap/tidb/issues/37549) @ [3ポインター](https://github.com/3pointer)
        -   外部storage[＃37469](https://github.com/pingcap/tidb/issues/37469) @ [モクイシュル28](https://github.com/MoCuishle28)認証キーに特殊文字が含まれている場合にバックアップと復元が失敗する可能性がある問題を修正
