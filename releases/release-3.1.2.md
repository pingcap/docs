---
title: TiDB 3.1.2 Release Notes
---

# TiDB3.1.2リリースノート {#tidb-3-1-2-release-notes}

発売日：2020年6月4日

TiDBバージョン：3.1.2

## バグの修正 {#bug-fixes}

-   TiKV

    -   S3およびGCS1を使用したバックアップおよび復元中のエラー処理の問題を修正し[＃7965](https://github.com/tikv/tikv/pull/7965)
    -   復元中に発生する`DefaultNotFound`のエラーを修正します[＃7838](https://github.com/tikv/tikv/pull/7938)

-   ツール

    -   バックアップと復元（BR）

        -   ネットワークが貧弱な場合は自動的に再試行して、S3およびGCSストレージの安定性を向上させます[＃314](https://github.com/pingcap/br/pull/314) [＃7965](https://github.com/tikv/tikv/pull/7965)
        -   小さなテーブルを復元するときにリージョンリーダーが見つからないために発生する復元の失敗を修正します[＃303](https://github.com/pingcap/br/pull/303)
        -   テーブルの行IDが`2^(63)`を超える場合の復元中のデータ損失の問題を修正し[＃323](https://github.com/pingcap/br/pull/323)
        -   空のデータベースとテーブルを復元できない問題を修正します[＃318](https://github.com/pingcap/br/pull/318)
        -   S3ストレージをターゲットとする場合のサーバー側暗号化（SSE）でのAWSKMSの使用のサポート[＃261](https://github.com/pingcap/br/pull/261)
