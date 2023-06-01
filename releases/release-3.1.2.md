---
title: TiDB 3.1.2 Release Notes
---

# TiDB 3.1.2 リリースノート {#tidb-3-1-2-release-notes}

発売日：2020年6月4日

TiDB バージョン: 3.1.2

## バグの修正 {#bug-fixes}

-   TiKV

    -   S3 および GCS [<a href="https://github.com/tikv/tikv/pull/7965">#7965</a>](https://github.com/tikv/tikv/pull/7965)でのバックアップおよび復元中のエラー処理の問題を修正
    -   `DefaultNotFound`復元中に発生するエラーを修正[<a href="https://github.com/tikv/tikv/pull/7938">#7838</a>](https://github.com/tikv/tikv/pull/7938)

-   ツール

    -   バックアップと復元 (BR)

        -   S3 および GCS ストレージの安定性を向上させるために、ネットワークの状態が悪いときに自動的に再試行します[<a href="https://github.com/pingcap/br/pull/314">#314</a>](https://github.com/pingcap/br/pull/314) [<a href="https://github.com/tikv/tikv/pull/7965">#7965</a>](https://github.com/tikv/tikv/pull/7965)
        -   小さなテーブル[<a href="https://github.com/pingcap/br/pull/303">#303</a>](https://github.com/pingcap/br/pull/303)を復元するときにリージョンリーダーが見つからないために発生する復元エラーを修正しました。
        -   テーブルの行 ID が`2^(63)` [<a href="https://github.com/pingcap/br/pull/323">#323</a>](https://github.com/pingcap/br/pull/323)を超える場合の復元中のデータ損失の問題を修正
        -   空のデータベースとテーブルを復元できない問題を修正[<a href="https://github.com/pingcap/br/pull/318">#318</a>](https://github.com/pingcap/br/pull/318)
        -   S3storageをターゲットとする場合のサーバー側暗号化 (SSE) のための AWS KMS の使用のサポート[<a href="https://github.com/pingcap/br/pull/261">#261</a>](https://github.com/pingcap/br/pull/261)
