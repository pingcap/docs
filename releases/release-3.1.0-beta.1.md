---
title: TiDB 3.1 Beta.1 Release Notes
---

# TiDB 3.1 ベータ.1 リリースノート {#tidb-3-1-beta-1-release-notes}

発売日：2020年1月10日

TiDB バージョン: 3.1.0-beta.1

TiDB Ansible バージョン: 3.1.0-beta.1

## TiKV {#tikv}

-   バックアップ
    -   読みやすいようにファイル名の長さを短くするために、バックアップ ファイルの名前を`start_key`からハッシュ値`start_key`に変更します[<a href="https://github.com/tikv/tikv/pull/6198">#6198</a>](https://github.com/tikv/tikv/pull/6198)
    -   RocksDB の`force_consistency_checks`チェックを無効にして、一貫性チェック[<a href="https://github.com/tikv/tikv/pull/6249">#6249</a>](https://github.com/tikv/tikv/pull/6249)での誤検知を回避します。
    -   増分バックアップ機能の追加[<a href="https://github.com/tikv/tikv/pull/6286">#6286</a>](https://github.com/tikv/tikv/pull/6286)

-   sst_importer
    -   リストア中に SST ファイルに MVCC プロパティが存在しない問題を修正[<a href="https://github.com/tikv/tikv/pull/6378">#6378</a>](https://github.com/tikv/tikv/pull/6378)
    -   `tikv_import_download_duration` 、 `tikv_import_download_bytes` 、 `tikv_import_ingest_duration` 、 `tikv_import_ingest_bytes` 、 `tikv_import_error_counter`などの監視項目を追加して、SST ファイルのダウンロードと取り込みのオーバーヘッドを観察します[<a href="https://github.com/tikv/tikv/pull/6404">#6404</a>](https://github.com/tikv/tikv/pull/6404)

-   ラフトストア
    -   リーダーが変わるとフォロワーが古いデータを読み取り、トランザクション分離[<a href="https://github.com/tikv/tikv/pull/6343">#6343</a>](https://github.com/tikv/tikv/pull/6343)が壊れるというFollower Readの問題を修正しました。

## ツール {#tools}

-   BR (バックアップと復元)
    -   不正確なバックアップ進行状況情報を修正[<a href="https://github.com/pingcap/br/pull/127">#127</a>](https://github.com/pingcap/br/pull/127)
    -   領域[<a href="https://github.com/pingcap/br/pull/122">#122</a>](https://github.com/pingcap/br/pull/122)の分割のパフォーマンスを向上させます。
    -   パーティション化されたテーブルのバックアップおよび復元機能を追加する[<a href="https://github.com/pingcap/br/pull/137">#137</a>](https://github.com/pingcap/br/pull/137)
    -   PDスケジューラ[<a href="https://github.com/pingcap/br/pull/123">#123</a>](https://github.com/pingcap/br/pull/123)の自動スケジュール機能を追加
    -   `PKIsHandle`以外のテーブルが復元された後にデータが上書きされる問題を修正[<a href="https://github.com/pingcap/br/pull/139">#139</a>](https://github.com/pingcap/br/pull/139)

## TiDB Ansible {#tidb-ansible}

-   初期化フェーズ[<a href="https://github.com/pingcap/tidb-ansible/pull/1086">#1086</a>](https://github.com/pingcap/tidb-ansible/pull/1086)中にオペレーティング システムの Transparent Huge Pages (THP) を自動的に無効にする機能を追加します。
-   BRコンポーネントの Grafana モニタリングを追加[<a href="https://github.com/pingcap/tidb-ansible/pull/1093">#1093</a>](https://github.com/pingcap/tidb-ansible/pull/1093)
-   関連ディレクトリを自動的に作成することで、 TiDB Lightningの展開を最適化します[<a href="https://github.com/pingcap/tidb-ansible/pull/1104">#1104</a>](https://github.com/pingcap/tidb-ansible/pull/1104)
