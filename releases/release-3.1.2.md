---
title: TiDB 3.1.2 Release Notes
summary: TiDB 3.1.2 was released on June 4, 2020. Bug fixes include error handling during backup and restoration with S3 and GCS, and a `DefaultNotFound` error during restoration. Tools like Backup & Restore (BR) now automatically retry on poor network, fix restoration failures, data loss issues, and support AWS KMS for server-side encryption with S3 storage.
---

# TiDB 3.1.2 リリースノート {#tidb-3-1-2-release-notes}

発売日：2020年6月4日

TiDB バージョン: 3.1.2

## バグの修正 {#bug-fixes}

-   TiKV

    -   S3 および GCS [#7965](https://github.com/tikv/tikv/pull/7965)でのバックアップおよび復元中のエラー処理の問題を修正
    -   `DefaultNotFound`復元中に発生するエラーを修正[#7838](https://github.com/tikv/tikv/pull/7938)

-   ツール

    -   バックアップと復元 (BR)

        -   S3 および GCS ストレージの安定性を向上させるために、ネットワークの状態が悪いときに自動的に再試行します[#314](https://github.com/pingcap/br/pull/314) [#7965](https://github.com/tikv/tikv/pull/7965)
        -   小さなテーブル[#303](https://github.com/pingcap/br/pull/303)を復元するときにリージョンリーダーが見つからないために発生する復元エラーを修正しました。
        -   テーブルの行 ID が`2^(63)` [#323](https://github.com/pingcap/br/pull/323)を超える場合の復元中のデータ損失の問題を修正
        -   空のデータベースとテーブルを復元できない問題を修正[#318](https://github.com/pingcap/br/pull/318)
        -   S3storageをターゲットとする場合のサーバー側暗号化 (SSE) のための AWS KMS の使用のサポート[#261](https://github.com/pingcap/br/pull/261)
