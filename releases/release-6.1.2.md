---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 リリースノート {#tidb-6-1-2-release-notes}

発売日：2022年10月24日

TiDB バージョン: 6.1.2

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.1.2#version-list)

## 改良点 {#improvements}

-   TiDB

    -   配置ルールとTiFlashレプリカを 1 つのテーブルで同時に設定できるようにする[#37171](https://github.com/pingcap/tidb/issues/37171) @ [ルクァンチャオ](https://github.com/lcwangchao)

-   TiKV

    -   `unreachable_backoff`つのピアが到達不能になった後にRaftstore があまりにも多くのメッセージをブロードキャストするのを避けるために、1 つのアイテムの構成をサポートします[#13054](https://github.com/tikv/tikv/issues/13054) @ [5kbps](https://github.com/5kbpers)
    -   フロー制御しきい値[#13467](https://github.com/tikv/tikv/issues/13467) @ [タボキー](https://github.com/tabokie)より小さい値への RocksDB 書き込みストール設定の構成をサポート

-   ツール

    -   TiDB Lightning

        -   チェックサム中に再試行可能なエラーを追加して、堅牢性を向上させます[#37690](https://github.com/pingcap/tidb/issues/37690) @ [D3ハンター](https://github.com/D3Hunter)

    -   TiCDC

        -   解決された TS をバッチ[#7078](https://github.com/pingcap/tiflow/issues/7078) @ [スドジ](https://github.com/sdojjy)で処理することにより、領域ワーカーのパフォーマンスを向上させます

## バグの修正 {#bug-fixes}

-   TiDB

    -   データベース レベルの権限が誤ってクリーンアップされる問題を修正します[#38363](https://github.com/pingcap/tidb/issues/38363) @ [ドヴィーデン](https://github.com/dveeden)
    -   `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526) @ [xhebox](https://github.com/xhebox)の間違った出力を修正
    -   1 つの PD ノードがダウンすると、他の PD ノード[#35708](https://github.com/pingcap/tidb/issues/35708) @ [接線](https://github.com/tangenta)が再試行されないために`information_schema.TIKV_REGION_STATUS`のクエリが失敗する問題を修正します
    -   `UNION`演算子が予期しない空の結果[#36903](https://github.com/pingcap/tidb/issues/36903) @ [ティアンカイマオ](https://github.com/tiancaiamao)を返す可能性がある問題を修正します
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254) @ [wshwsh12](https://github.com/wshwsh12)のパーティション テーブルで動的モードを有効にしたときに発生する間違った結果を修正します。
    -   リージョンが[#37141](https://github.com/pingcap/tidb/issues/37141) @ [スティックナーフ](https://github.com/sticnarf)にマージされるときに、リージョンキャッシュが時間内にクリーンアップされない問題を修正します。
    -   KV クライアントが不要な ping メッセージ[#36861](https://github.com/pingcap/tidb/issues/36861) @ [ジャッキスプ](https://github.com/jackysp)を送信する問題を修正します。
    -   トランザクション コミットが完了する前に、DML executor を含む`EXPLAIN ANALYZE`ステートメントが結果を返す可能性があるという問題を修正します[#37373](https://github.com/pingcap/tidb/issues/37373) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `ORDER BY`句に相関サブクエリ[#18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が含まれている場合、 `GROUP CONCAT` with `ORDER BY`が失敗する可能性がある問題を修正します。
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合に`Can't find column`が報告される問題を修正します。
    -   特定のシナリオ[#37187](https://github.com/pingcap/tidb/issues/37187) @ [思い出す](https://github.com/Reminiscent)で`EXECUTE`予期しないエラーをスローする可能性がある問題を修正します。

-   TiKV

    -   リージョン[#13553](https://github.com/tikv/tikv/issues/13553) @ [スペード・ア・タン](https://github.com/SpadeA-Tang)にまたがるバッチ スナップショットが原因で、スナップショット データが不完全になる可能性がある問題を修正します。
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に[#11424](https://github.com/tikv/tikv/issues/11424) @ [コナー1996](https://github.com/Connor1996)に設定されている場合の QPS ドロップの問題を修正します。
    -   TiKV が Web ID プロバイダーからエラーを取得し、デフォルト プロバイダー[#13122](https://github.com/tikv/tikv/issues/13122) @ [3ポインター](https://github.com/3pointer)にフェールバックすると、アクセス許可が拒否されたというエラーが発生する問題を修正します。
    -   TiKV インスタンスが隔離されたネットワーク環境にある場合、数分間 TiKV サービスが利用できない問題を修正します[#12966](https://github.com/tikv/tikv/issues/12966) @ [コスヴェン](https://github.com/cosven)

-   PD

    -   リージョンツリーの統計が不正確になる問題を修正[#5318](https://github.com/tikv/pd/issues/5318) @ [ルルング](https://github.com/rleungx)
    -   TiFlash学習者のレプリカが作成されない場合がある問題を修正[#5401](https://github.com/tikv/pd/issues/5401) @ [フンドゥンDM](https://github.com/HunDunDM)
    -   PD がダッシュボード プロキシ リクエスト[#5321](https://github.com/tikv/pd/issues/5321) @ [フンドゥンDM](https://github.com/HunDunDM)を正しく処理できない問題を修正します。
    -   異常なリージョンが PDpanic[#5491](https://github.com/tikv/pd/issues/5491) @ [ノルーチ](https://github.com/nolouch)を引き起こす可能性がある問題を修正します

-   TiFlash

    -   I/O リミッターが、一括書き込み後にクエリ要求の I/O スループットを誤って調整し、クエリのパフォーマンスを低下させる可能性がある問題を修正します[#5801](https://github.com/pingcap/tiflash/issues/5801) @ [リン・ジンヘ](https://github.com/JinheLin)
    -   ウィンドウ関数により、クエリがキャンセルされたときにTiFlashがクラッシュする可能性がある問題を修正します[#5814](https://github.com/pingcap/tiflash/issues/5814) @ [シーライズ](https://github.com/SeaRise)
    -   `NULL`値[#5859](https://github.com/pingcap/tiflash/issues/5859) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   TiDB Lightning

        -   無効なメトリクス カウンター[#37338](https://github.com/pingcap/tidb/issues/37338) @ [D3ハンター](https://github.com/D3Hunter)によって発生するTiDB Lightningのpanicを修正

    -   TiDB データ移行 (DM)

        -   DM タスクが同期ユニットに入り、中断されると、上流のテーブル構造情報が失われる問題を修正します[#7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)
        -   チェックポイント[#5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)を保存するときに SQL ステートメントを分割することにより、大きなトランザクション エラーを修正します。
        -   DM 事前チェックで`INFORMATION_SCHEMA` [#7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)の`SELECT`権限が必要になる問題を修正
        -   高速/完全バリデーター[#7241](https://github.com/pingcap/tiflow/issues/7241) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)で DM タスクを実行した後、DM-worker がデッドロック エラーをトリガーする問題を修正します。
        -   DM が`Specified key was too long`エラー[#5315](https://github.com/pingcap/tiflow/issues/5315) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正
        -   レプリケーション[#7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正します。

    -   TiCDC

        -   cdcサーバーが完全に起動する前に HTTP 要求を受信すると、cdcサーバーがpanic可能性がある問題を修正します[#6838](https://github.com/pingcap/tiflow/issues/6838) @ [アスドンメン](https://github.com/asddongmen)
        -   アップグレード[#7235](https://github.com/pingcap/tiflow/issues/7235) @ [ハイラスチン](https://github.com/hi-rustin)中のログ フラッディングの問題を修正します。
        -   changefeed の REDO ログファイルが誤って削除されることがある問題を修正[#6413](https://github.com/pingcap/tiflow/issues/6413) @ [ハイラスチン](https://github.com/hi-rustin)
        -   etcd トランザクションであまりにも多くの操作がコミットされた場合に TiCDC が使用できなくなる可能性がある問題を修正します[#7131](https://github.com/pingcap/tiflow/issues/7131) @ [ハイラスチン](https://github.com/hi-rustin)
        -   REDO ログで再入不可の DDL ステートメントを 2 回[#6927](https://github.com/pingcap/tiflow/issues/6927) @ [ヒック](https://github.com/hicqu)実行すると、データの不整合が発生する可能性がある問題を修正します。

    -   バックアップと復元 (BR)

        -   復元時に同時実行数が大きすぎるため、リージョンのバランスが取れていない問題を修正します[#37549](https://github.com/pingcap/tidb/issues/37549) @ [3ポインター](https://github.com/3pointer)
        -   外部storage[#37469](https://github.com/pingcap/tidb/issues/37469) @ [MoCuishle28](https://github.com/MoCuishle28)の認証キーに特殊文字が含まれていると、バックアップと復元に失敗する可能性がある問題を修正
