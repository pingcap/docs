---
title: TiDB 4.0.1 Release Notes
---

# TiDB4.0.1リリースノート {#tidb-4-0-1-release-notes}

発売日：2020年6月12日

TiDBバージョン：4.0.1

## 新機能 {#new-features}

-   TiKV

    -   `--advertise-status-addr`開始フラグを追加して、アドバタイズするステータスアドレスを指定します[＃8046](https://github.com/tikv/tikv/pull/8046)

-   PD

    -   組み込みのTiDBダッシュボード[＃2511](https://github.com/pingcap/pd/pull/2511)の内部プロキシをサポートする
    -   PDクライアント[＃2509](https://github.com/pingcap/pd/pull/2509)のカスタムタイムアウトの設定をサポート

-   TiFlash

    -   TiDBの新しい照合順序フレームワークをサポートする
    -   `BitAnd/BitOr` `Json_length`を`If`に`BitXor/BitNot`ダウンすることをサポート
    -   TiFlashでの大規模なトランザクションのロックの解決ロジックをサポートする

-   ツール

    -   バックアップと復元（BR）

        -   BRとTiDBクラスタに互換性がないという問題を回避するために、BRの起動時にバージョンチェックを追加します[＃311](https://github.com/pingcap/br/pull/311)

## バグの修正 {#bug-fixes}

-   TiKV

    -   スタートアップログの`use-unified-pool`構成が正しく印刷されない問題を修正します[＃7946](https://github.com/tikv/tikv/pull/7946)
    -   tikv-ctlが相対パス[＃7963](https://github.com/tikv/tikv/pull/7963)をサポートしない問題を修正します
    -   ポイント選択の監視メトリックが不正確であるというバグを修正します[＃8033](https://github.com/tikv/tikv/pull/8033)
    -   ネットワークの分離がなくなった後、ピアが破壊されない可能性があるという問題を修正します[＃8006](https://github.com/tikv/tikv/pull/8006)
    -   読み取りインデックスのリクエストが古いコミットインデックスを取得する可能性がある問題を修正します[＃8043](https://github.com/tikv/tikv/pull/8043)
    -   S3およびGCSストレージを使用したバックアップと復元の信頼性の向上[＃7917](https://github.com/tikv/tikv/pull/7917)

-   PD

    -   状況によっては配置ルールの設定ミスを防ぐ[＃2516](https://github.com/pingcap/pd/pull/2516)
    -   配置ルールを削除するとパニックが発生する可能性がある問題を修正します[＃2515](https://github.com/pingcap/pd/pull/2515)
    -   ストアの使用サイズがゼロの場合、ストア情報を取得できないバグを修正します[＃2474](https://github.com/pingcap/pd/pull/2474)

-   TiFlash

    -   TiFlashの`bit`タイプ列のデフォルト値が誤って解析される問題を修正します
    -   TiFlashの一部のタイムゾーンでの`1970-01-01 00:00:00 UTC`の誤算を修正
