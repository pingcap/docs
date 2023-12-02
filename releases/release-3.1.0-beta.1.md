---
title: TiDB 3.1 Beta.1 Release Notes
---

# TiDB 3.1 ベータ.1 リリースノート {#tidb-3-1-beta-1-release-notes}

発売日：2020年1月10日

TiDB バージョン: 3.1.0-beta.1

TiDB Ansible バージョン: 3.1.0-beta.1

## TiKV {#tikv}

-   バックアップ
    -   読みやすいようにファイル名の長さを短くするために、バックアップ ファイルの名前を`start_key`からハッシュ値`start_key`に変更します[#6198](https://github.com/tikv/tikv/pull/6198)
    -   RocksDB の`force_consistency_checks`チェックを無効にして、一貫性チェック[#6249](https://github.com/tikv/tikv/pull/6249)での誤検知を回避します。
    -   増分バックアップ機能の追加[#6286](https://github.com/tikv/tikv/pull/6286)

-   sst_importer
    -   リストア中に SST ファイルに MVCC プロパティが存在しない問題を修正[#6378](https://github.com/tikv/tikv/pull/6378)
    -   `tikv_import_download_duration` 、 `tikv_import_download_bytes` 、 `tikv_import_ingest_duration` 、 `tikv_import_ingest_bytes` 、 `tikv_import_error_counter`などの監視項目を追加して、SST ファイルのダウンロードと取り込みのオーバーヘッドを観察します[#6404](https://github.com/tikv/tikv/pull/6404)

-   ラフトストア
    -   リーダーが変わるとフォロワーが古いデータを読み取り、トランザクション分離[#6343](https://github.com/tikv/tikv/pull/6343)が壊れるというFollower Readの問題を修正しました。

## ツール {#tools}

-   BR (バックアップと復元)
    -   不正確なバックアップ進行状況情報を修正[#127](https://github.com/pingcap/br/pull/127)
    -   領域[#122](https://github.com/pingcap/br/pull/122)の分割のパフォーマンスを向上させます。
    -   パーティション化されたテーブルのバックアップおよび復元機能を追加します[#137](https://github.com/pingcap/br/pull/137)
    -   PDスケジューラ[#123](https://github.com/pingcap/br/pull/123)の自動スケジュール機能を追加
    -   `PKIsHandle`以外のテーブルが復元された後にデータが上書きされる問題を修正[#139](https://github.com/pingcap/br/pull/139)

## TiDB Ansible {#tidb-ansible}

-   初期化フェーズ[#1086](https://github.com/pingcap/tidb-ansible/pull/1086)中にオペレーティング システムの Transparent Huge Pages (THP) を自動的に無効にする機能を追加します。
-   BRコンポーネントの Grafana モニタリングを追加[#1093](https://github.com/pingcap/tidb-ansible/pull/1093)
-   関連ディレクトリを自動的に作成することで、 TiDB Lightningの展開を最適化します[#1104](https://github.com/pingcap/tidb-ansible/pull/1104)
