---
title: TiDB 4.0.1 Release Notes
summary: TiDB 4.0.1は2020年6月12日にリリースされました。新機能には、PDクライアントのカスタムタイムアウトのサポートと、 TiFlashの新しい照合順序フレームワークが含まれます。バグ修正により、構成、監視メトリック、ストア情報の取得に関する問題が修正されました。バックアップとリストア（ BR）には、互換性の問題を回避するためのバージョンチェックが含まれるようになりました。
---

# TiDB 4.0.1 リリースノート {#tidb-4-0-1-release-notes}

発売日：2020年6月12日

TiDB バージョン: 4.0.1

## 新機能 {#new-features}

-   TiKV

    -   `--advertise-status-addr`開始フラグを追加して、 [＃8046](https://github.com/tikv/tikv/pull/8046)アドバタイズするステータスアドレスを指定します。

-   PD

    -   組み込みの TiDB ダッシュボード[＃2511](https://github.com/pingcap/pd/pull/2511)内部プロキシをサポート
    -   PDクライアント[＃2509](https://github.com/pingcap/pd/pull/2509)のカスタムタイムアウト設定をサポート

-   TiFlash

    -   TiDBの新しい照合順序フレームワークをサポート
    -   `If` / `BitAnd/BitOr` / `BitXor/BitNot` / `Json_length`関数をTiFlashにプッシュダウンする機能をサポート
    -   TiFlashの大規模トランザクションの Resolve Lock ロジックをサポート

-   ツール

    -   バックアップと復元 (BR)

        -   BRとTiDBクラスタの互換性がない問題を回避するために、 BRの起動時にバージョンチェックを追加します[＃311](https://github.com/pingcap/br/pull/311)

## バグ修正 {#bug-fixes}

-   TiKV

    -   起動ログの`use-unified-pool`構成が誤って印刷される問題を修正[＃7946](https://github.com/tikv/tikv/pull/7946)
    -   tikv-ctlが相対パス[＃7963](https://github.com/tikv/tikv/pull/7963)をサポートしない問題を修正
    -   ポイントセレクトのモニタリングメトリックが不正確になるバグを修正[＃8033](https://github.com/tikv/tikv/pull/8033)
    -   ネットワーク分離が消えた後にピアが破棄されない可能性がある問題を修正[＃8006](https://github.com/tikv/tikv/pull/8006)
    -   読み取りインデックスのリクエストで古いコミットインデックス[＃8043](https://github.com/tikv/tikv/pull/8043)が取得される可能性がある問題を修正しました
    -   S3とGCSストレージによるバックアップとリストアの信頼性の向上[＃7917](https://github.com/tikv/tikv/pull/7917)

-   PD

    -   いくつかの状況における配置ルールの誤った設定を防ぐ[＃2516](https://github.com/pingcap/pd/pull/2516)
    -   配置ルールを削除するとpanicが発生する可能性がある問題を修正[＃2515](https://github.com/pingcap/pd/pull/2515)
    -   ストアの使用サイズが0の場合にストア情報を取得できないバグを修正[＃2474](https://github.com/pingcap/pd/pull/2474)

-   TiFlash

    -   TiFlashの`bit`型列のデフォルト値が正しく解析されない問題を修正しました
    -   TiFlashの一部のタイムゾーンにおける`1970-01-01 00:00:00 UTC`の誤算を修正
