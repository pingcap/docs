---
title: TiDB 3.1.2 Release Notes
summary: TiDB 3.1.2は2020年6月4日にリリースされました。バグ修正には、S3およびGCSを使用したバックアップおよびリストア時のエラー処理、およびリストア中の「DefaultNotFound」エラーが含まれます。バックアップ＆リストア（BR）などのツールは、ネットワーク状態が悪い場合に自動的に再試行するようになり、リストアの失敗やデータ損失の問題を修正し、S3storageを使用したサーバー側暗号化のためのAWS KMSをサポートします。
---

# TiDB 3.1.2 リリースノート {#tidb-3-1-2-release-notes}

発売日：2020年6月4日

TiDB バージョン: 3.1.2

## バグ修正 {#bug-fixes}

-   TiKV

    -   S3 と GCS [＃7965](https://github.com/tikv/tikv/pull/7965)を使用したバックアップと復元中のエラー処理の問題を修正
    -   復元中に発生する`DefaultNotFound`エラーを修正する[＃7838](https://github.com/tikv/tikv/pull/7938)

-   ツール

    -   バックアップと復元 (BR)

        -   ネットワークの状態が悪い場合は自動的に再試行して、S3 および GCS ストレージの安定性を向上させます[＃314](https://github.com/pingcap/br/pull/314) [＃7965](https://github.com/tikv/tikv/pull/7965)
        -   小さなテーブルを復元するときにリージョンリーダーが見つからないために発生する復元エラーを修正[＃303](https://github.com/pingcap/br/pull/303)
        -   テーブルの行IDが`2^(63)` [＃323](https://github.com/pingcap/br/pull/323)を超えると復元中にデータ損失が発生する問題を修正しました
        -   空のデータベースとテーブルを復元できない問題を修正[＃318](https://github.com/pingcap/br/pull/318)
        -   S3storageをターゲットとする場合、サーバー側暗号化（SSE）にAWS KMSを使用するサポート[＃261](https://github.com/pingcap/br/pull/261)
