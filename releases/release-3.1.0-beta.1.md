---
title: TiDB 3.1 Beta.1 Release Notes
---

# TiDB 3.1 Beta.1 リリースノート {#tidb-3-1-beta-1-release-notes}

発売日：2020年1月10日

TiDB バージョン: 3.1.0-beta.1

TiDB アンシブル バージョン: 3.1.0-beta.1

## TiKV {#tikv}

-   バックアップ
    -   バックアップ ファイルの名前を`start_key`からハッシュ値`start_key`に変更して、読みやすいようにファイル名の長さを短くします[#6198](https://github.com/tikv/tikv/pull/6198)
    -   RocksDB の`force_consistency_checks`チェックを無効にして、一貫性チェック[#6249](https://github.com/tikv/tikv/pull/6249)での誤検知を回避します
    -   増分バックアップ機能の追加[#6286](https://github.com/tikv/tikv/pull/6286)

-   sst_importer
    -   復元中に SST ファイルに MVCC プロパティがない問題を修正[#6378](https://github.com/tikv/tikv/pull/6378)
    -   `tikv_import_download_duration` 、 `tikv_import_download_bytes` 、 `tikv_import_ingest_duration` 、 `tikv_import_ingest_bytes` 、 `tikv_import_error_counter`などの監視項目を追加して、SST ファイルのダウンロードと取り込みのオーバーヘッドを観察します[#6404](https://github.com/tikv/tikv/pull/6404)

-   いかだ屋
    -   リーダーが変更されたときにフォロワーが古いデータを読み取り、トランザクションの分離を壊すというFollower Readの問題を修正します[#6343](https://github.com/tikv/tikv/pull/6343)

## ツール {#tools}

-   BR (バックアップと復元)
    -   不正確なバックアップ進行状況情報を修正する[#127](https://github.com/pingcap/br/pull/127)
    -   リージョン[#122](https://github.com/pingcap/br/pull/122)の分割のパフォーマンスを向上させる
    -   パーティション化されたテーブルのバックアップおよび復元機能を追加する[#137](https://github.com/pingcap/br/pull/137)
    -   PDスケジューラの自動スケジューリング機能を追加[#123](https://github.com/pingcap/br/pull/123)
    -   `PKIsHandle`以外のテーブルが復元された後にデータが上書きされる問題を修正します[#139](https://github.com/pingcap/br/pull/139)

## TiDB アンシブル {#tidb-ansible}

-   初期化フェーズ[#1086](https://github.com/pingcap/tidb-ansible/pull/1086)で、オペレーティング システムの Transparent Huge Pages (THP) を自動的に無効にする機能を追加します。
-   BRコンポーネントの Grafana モニタリングを追加する[#1093](https://github.com/pingcap/tidb-ansible/pull/1093)
-   関連するディレクトリを自動的に作成することにより、 TiDB Lightningの展開を最適化します[#1104](https://github.com/pingcap/tidb-ansible/pull/1104)
