---
title: TiDB 3.1.2 Release Notes
summary: TiDB 3.1.2 は 2020 年 6 月 4 日にリリースされました。バグ修正には、S3 および GCS を使用したバックアップと復元中のエラー処理、および復元中の DefaultNotFound` エラーが含まれます。Backup & Restore (BR) などのツールは、ネットワークの状態が悪い場合に自動的に再試行し、復元の失敗やデータ損失の問題を修正し、S3storageを使用したサーバー側暗号化用の AWS KMS をサポートするようになりました。
---

# TiDB 3.1.2 リリースノート {#tidb-3-1-2-release-notes}

発売日: 2020年6月4日

TiDB バージョン: 3.1.2

## バグ修正 {#bug-fixes}

-   ティクヴ

    -   S3 および GCS [＃7965](https://github.com/tikv/tikv/pull/7965)を使用したバックアップと復元中のエラー処理の問題を修正
    -   復元中に発生する`DefaultNotFound`エラーを修正する[＃7838](https://github.com/tikv/tikv/pull/7938)

-   ツール

    -   バックアップと復元 (BR)

        -   ネットワークの状態が悪い場合は自動的に再試行し、S3 および GCS ストレージの安定性を向上させます[＃314](https://github.com/pingcap/br/pull/314) [＃7965](https://github.com/tikv/tikv/pull/7965)
        -   小さなテーブルを復元するときにリージョンリーダーが見つからないために発生する復元エラーを修正[＃303](https://github.com/pingcap/br/pull/303)
        -   テーブルの行IDが`2^(63)` [＃323](https://github.com/pingcap/br/pull/323)を超えると復元中にデータ損失が発生する問題を修正
        -   空のデータベースとテーブルを復元できない問題を修正[＃318](https://github.com/pingcap/br/pull/318)
        -   S3storageをターゲットにする場合、サーバー側暗号化（SSE）にAWS KMSを使用するサポート[＃261](https://github.com/pingcap/br/pull/261)
