---
title: TiDB 3.1.2 Release Notes
---

# TiDB 3.1.2 リリースノート {#tidb-3-1-2-release-notes}

発売日：2020年6月4日

TiDB バージョン: 3.1.2

## バグの修正 {#bug-fixes}

-   TiKV

    -   S3 および GCS [#7965](https://github.com/tikv/tikv/pull/7965)でのバックアップおよび復元中のエラー処理の問題を修正します。
    -   復元中に発生する`DefaultNotFound`エラーを修正します[#7838](https://github.com/tikv/tikv/pull/7938)

-   ツール

    -   バックアップと復元 (BR)

        -   S3 および GCS ストレージでの安定性を向上させるために、ネットワークが貧弱な場合に自動的に再試行します[#314](https://github.com/pingcap/br/pull/314) [#7965](https://github.com/tikv/tikv/pull/7965)
        -   小さなテーブルを復元するときにリージョンリーダーが見つからないために発生する復元の失敗を修正します[#303](https://github.com/pingcap/br/pull/303)
        -   テーブルの行 ID が`2^(63)` [#323](https://github.com/pingcap/br/pull/323)を超える場合の復元中のデータ損失の問題を修正します
        -   空のデータベースとテーブルを復元できない問題を修正します[#318](https://github.com/pingcap/br/pull/318)
        -   S3storage[#261](https://github.com/pingcap/br/pull/261)をターゲットとする場合、サーバー側の暗号化 (SSE) に AWS KMS を使用するサポート
