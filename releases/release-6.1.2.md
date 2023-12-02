---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 リリースノート {#tidb-6-1-2-release-notes}

発売日：2022年10月24日

TiDB バージョン: 6.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.2#version-list)

## 改善点 {#improvements}

-   TiDB

    -   1 つのテーブルで配置ルールとTiFlashレプリカを同時に設定できるようにします[#37171](https://github.com/pingcap/tidb/issues/37171) @ [ルクワンチャオ](https://github.com/lcwangchao)

-   TiKV

    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストすることを避けるための`unreachable_backoff`項目の設定をサポート[#13054](https://github.com/tikv/tikv/issues/13054) @ [5kbps](https://github.com/5kbpers)
    -   RocksDB 書き込み停止設定をフロー制御しきい値[#13467](https://github.com/tikv/tikv/issues/13467) @ [タボキー](https://github.com/tabokie)よりも小さい値に構成することをサポート

-   ツール

    -   TiDB Lightning

        -   チェックサム中に再試行可能なエラーを追加して堅牢性を向上[#37690](https://github.com/pingcap/tidb/issues/37690) @ [D3ハンター](https://github.com/D3Hunter)

    -   TiCDC

        -   解決された TS をバッチ[#7078](https://github.com/pingcap/tiflow/issues/7078) @ [スドジ](https://github.com/sdojjy)で処理することで、リージョン ワーカーのパフォーマンスを向上させます。

## バグの修正 {#bug-fixes}

-   TiDB

    -   データベースレベルの権限が誤ってクリーンアップされる問題を修正[#38363](https://github.com/pingcap/tidb/issues/38363) @ [ドヴィーデン](https://github.com/dveeden)
    -   `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526) @ [ゼボックス](https://github.com/xhebox)の誤った出力を修正
    -   1 つの PD ノードがダウンすると、他の PD ノード[#35708](https://github.com/pingcap/tidb/issues/35708) @ [タンジェンタ](https://github.com/tangenta)が再試行されないために`information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正します。
    -   `UNION`演算子が予期しない空の結果[#36903](https://github.com/pingcap/tidb/issues/36903) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を返す可能性がある問題を修正します。
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254) @ [wshwsh12](https://github.com/wshwsh12)のパーティション化されたテーブルで動的モードを有効にしたときに発生する間違った結果を修正しました。
    -   リージョンが[#37141](https://github.com/pingcap/tidb/issues/37141) @ [スティックナーフ](https://github.com/sticnarf)でマージされるときに、リージョンキャッシュが時間内にクリーンアップされない問題を修正します。
    -   KV クライアントが不要な ping メッセージを送信する問題を修正[#36861](https://github.com/pingcap/tidb/issues/36861) @ [ジャッキースプ](https://github.com/jackysp)
    -   DML エグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正します[#37373](https://github.com/pingcap/tidb/issues/37373) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `ORDER BY`句に相関サブクエリ[#18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が含まれている場合、 `GROUP CONCAT` with `ORDER BY`が失敗する可能性がある問題を修正します。
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合に`Can't find column`が報告される問題を修正
    -   特定のシナリオ[#37187](https://github.com/pingcap/tidb/issues/37187) @ [懐かしい](https://github.com/Reminiscent)で`EXECUTE`予期しないエラーをスローする可能性がある問題を修正します。

-   TiKV

    -   リージョン[#13553](https://github.com/tikv/tikv/issues/13553) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)にわたるバッチ スナップショットが原因でスナップショット データが不完全になる可能性がある問題を修正
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に[#11424](https://github.com/tikv/tikv/issues/11424) @ [コナー1996](https://github.com/Connor1996)に設定されている場合の QPS ドロップの問題を修正
    -   TiKV が Web ID プロバイダーからエラーを取得し、デフォルトのプロバイダー[#13122](https://github.com/tikv/tikv/issues/13122) @ [3ポインター](https://github.com/3pointer)にフェイルバックすると、アクセス許可拒否エラーが発生する問題を修正します。
    -   TiKV インスタンスが隔離されたネットワーク環境[#12966](https://github.com/tikv/tikv/issues/12966) @ [コスベン](https://github.com/cosven)にある場合、TiKV サービスが数分間利用できなくなる問題を修正します。

-   PD

    -   リージョンツリーの統計が不正確になる可能性がある問題を修正[#5318](https://github.com/tikv/pd/issues/5318) @ [ルルンクス](https://github.com/rleungx)
    -   TiFlash学習者のレプリカが作成されないことがある問題を修正[#5401](https://github.com/tikv/pd/issues/5401) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   PD がダッシュボード プロキシ リクエスト[#5321](https://github.com/tikv/pd/issues/5321) @ [フンドゥンDM](https://github.com/HunDunDM)を正しく処理できない問題を修正
    -   異常なリージョンにより PDpanic[#5491](https://github.com/tikv/pd/issues/5491) @ [ノールーシュ](https://github.com/nolouch)が発生する可能性がある問題を修正

-   TiFlash

    -   I/O リミッターが一括書き込み後にクエリ リクエストの I/O スループットを誤って調整し、クエリのパフォーマンスが低下する可能性がある問題を修正します[#5801](https://github.com/pingcap/tiflash/issues/5801) @ [ジンヘリン](https://github.com/JinheLin)
    -   クエリがキャンセルされたときにウィンドウ関数によってTiFlashがクラッシュする可能性がある問題を修正[#5814](https://github.com/pingcap/tiflash/issues/5814) @ [シーライズ](https://github.com/SeaRise)
    -   `NULL`値[#5859](https://github.com/pingcap/tiflash/issues/5859) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   TiDB Lightning

        -   無効なメトリック カウンター[#37338](https://github.com/pingcap/tidb/issues/37338) @ [D3ハンター](https://github.com/D3Hunter)によって引き起こされるTiDB Lightningのpanicを修正

    -   TiDB データ移行 (DM)

        -   DM タスクが同期ユニットに入って中断されると、上流のテーブル構造情報が失われる問題を修正します[#7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)
        -   チェックポイント[#5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)を保存するときに SQL ステートメントを分割することで、大規模なトランザクション エラーを修正しました。
        -   DM 事前チェックに`INFORMATION_SCHEMA` [#7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)の`SELECT`権限が必要である問題を修正
        -   高速/完全バリデータ[#7241](https://github.com/pingcap/tiflow/issues/7241) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)で DM タスクを実行した後、DM ワーカーがデッドロック エラーを引き起こす問題を修正
        -   DM が`Specified key was too long`エラー[#5315](https://github.com/pingcap/tiflow/issues/5315) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正
        -   レプリケーション[#7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正

    -   TiCDC

        -   CDCサーバーが完全に起動する前に HTTP リクエストを受信すると、CDCサーバーがpanic可能性がある問題を修正します[#6838](https://github.com/pingcap/tiflow/issues/6838) @ [東門](https://github.com/asddongmen)
        -   アップグレード[#7235](https://github.com/pingcap/tiflow/issues/7235) @ [こんにちはラスティン](https://github.com/hi-rustin)中のログフラッディング問題を修正
        -   ChangeFeed の REDO ログ ファイルが誤って削除される可能性がある問題を修正[#6413](https://github.com/pingcap/tiflow/issues/6413) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   etcd トランザクションでコミットされる操作が多すぎると TiCDC が使用できなくなる可能性がある問題を修正[#7131](https://github.com/pingcap/tiflow/issues/7131) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   REDO ログ内の非再入可能 DDL ステートメントが 2 回実行されるとデータの不整合が発生する可能性がある問題を修正[#6927](https://github.com/pingcap/tiflow/issues/6927) @ [ひっくり返る](https://github.com/hicqu)

    -   バックアップと復元 (BR)

        -   復元中に同時実行数の設定が大きすぎるため、リージョンのバランスが取れない問題を修正[#37549](https://github.com/pingcap/tidb/issues/37549) @ [3ポインター](https://github.com/3pointer)
        -   外部storage[#37469](https://github.com/pingcap/tidb/issues/37469) @ [モクイシュル28](https://github.com/MoCuishle28)の認証キーに特殊文字が存在する場合、バックアップと復元が失敗する可能性がある問題を修正
