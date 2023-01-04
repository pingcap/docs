---
title: TiDB 4.0.1 Release Notes
---

# TiDB 4.0.1 リリースノート {#tidb-4-0-1-release-notes}

発売日：2020年6月12日

TiDB バージョン: 4.0.1

## 新機能 {#new-features}

-   TiKV

    -   `--advertise-status-addr`開始フラグを追加して、 [#8046](https://github.com/tikv/tikv/pull/8046)をアドバタイズするステータス アドレスを指定します。

-   PD

    -   組み込み TiDB ダッシュボード[#2511](https://github.com/pingcap/pd/pull/2511)の内部プロキシをサポート
    -   PD クライアント[#2509](https://github.com/pingcap/pd/pull/2509)のカスタム タイムアウトの設定をサポート

-   TiFlash

    -   TiDB の新しい照合順序フレームワークをサポート
    -   `If` / `BitAnd/BitOr` / `BitXor/BitNot` / `Json_length`関数のTiFlashへのプッシュダウンをサポート
    -   TiFlashでの大規模なトランザクションの解決ロック ロジックをサポートします。

-   ツール

    -   バックアップと復元 (BR)

        -   BRと TiDB クラスターが互換性がないという問題を回避するために、 BRの起動時にバージョン チェックを追加します[#311](https://github.com/pingcap/br/pull/311)

## バグの修正 {#bug-fixes}

-   TiKV

    -   起動ログの`use-unified-pool`構成が正しく出力されない問題を修正します[#7946](https://github.com/tikv/tikv/pull/7946)
    -   tikv-ctl が相対パス[#7963](https://github.com/tikv/tikv/pull/7963)をサポートしていない問題を修正
    -   Point Selects の監視メトリックが不正確であるというバグを修正します[#8033](https://github.com/tikv/tikv/pull/8033)
    -   ネットワークの分離が解除された後、ピアが破棄されない場合がある問題を修正します[#8006](https://github.com/tikv/tikv/pull/8006)
    -   読み取りインデックスのリクエストが古いコミット インデックス[#8043](https://github.com/tikv/tikv/pull/8043)を取得する可能性がある問題を修正します。
    -   S3 および GCS ストレージでバックアップと復元の信頼性を向上させる[#7917](https://github.com/tikv/tikv/pull/7917)

-   PD

    -   状況によっては配置ルールの構成ミスを防止する[#2516](https://github.com/pingcap/pd/pull/2516)
    -   配置ルールを削除するとpanic[#2515](https://github.com/pingcap/pd/pull/2515)が発生する可能性がある問題を修正
    -   ストアの使用サイズが[#2474](https://github.com/pingcap/pd/pull/2474)のときにストア情報が取得できない不具合を修正

-   TiFlash

    -   TiFlashの`bit`型列のデフォルト値が正しく解析されない問題を修正
    -   TiFlashの一部のタイムゾーンでの`1970-01-01 00:00:00 UTC`の誤算を修正
