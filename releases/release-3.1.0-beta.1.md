---
title: TiDB 3.1 Beta.1 Release Notes
---

# TiDB3.1Beta.1リリースノート {#tidb-3-1-beta-1-release-notes}

発売日：2020年1月10日

TiDBバージョン：3.1.0-beta.1

TiDB Ansibleバージョン：3.1.0-beta.1

## TiKV {#tikv}

-   バックアップ
    -   バックアップファイルの名前を`start_key`からハッシュ値`start_key`に変更して、ファイル名の長さを短くし、読みやすくします[＃6198](https://github.com/tikv/tikv/pull/6198)
    -   RocksDBの`force_consistency_checks`チェックを無効にして、整合性チェック[＃6249](https://github.com/tikv/tikv/pull/6249)での誤検知を回避します
    -   増分バックアップ機能を追加する[＃6286](https://github.com/tikv/tikv/pull/6286)

-   sst_importer
    -   復元中にSSTファイルにMVCCプロパティがない問題を修正します[＃6378](https://github.com/tikv/tikv/pull/6378)
    -   `tikv_import_download_duration`などの監視項目を追加して、 [＃6404](https://github.com/tikv/tikv/pull/6404)ファイルのダウンロードと`tikv_import_ingest_duration`の`tikv_import_error_counter`を監視し`tikv_import_download_bytes` `tikv_import_ingest_bytes`

-   いかだ店
    -   リーダーが変更されたときにフォロワーが古いデータを読み取るため、トランザクションの分離が解除されるというフォロワー読み取りの問題を修正します[＃6343](https://github.com/tikv/tikv/pull/6343)

## ツール {#tools}

-   BR（バックアップと復元）
    -   不正確なバックアップの進行状況情報を修正する[＃127](https://github.com/pingcap/br/pull/127)
    -   リージョン[＃122](https://github.com/pingcap/br/pull/122)の分割のパフォーマンスを向上させる
    -   パーティションテーブルのバックアップと復元機能を追加する[＃137](https://github.com/pingcap/br/pull/137)
    -   PDスケジューラを自動的にスケジュールする機能を追加する[＃123](https://github.com/pingcap/br/pull/123)
    -   `PKIsHandle`以外のテーブルが復元された後にデータが上書きされる問題を修正します[＃139](https://github.com/pingcap/br/pull/139)

## TiDB Ansible {#tidb-ansible}

-   初期化フェーズ[＃1086](https://github.com/pingcap/tidb-ansible/pull/1086)の間にオペレーティングシステムでTransparentHugePages（THP）を自動的に無効にする機能を追加します
-   BRコンポーネントのGrafanaモニタリングを追加する[＃1093](https://github.com/pingcap/tidb-ansible/pull/1093)
-   関連するディレクトリを自動的に作成して、 TiDB Lightningの展開を最適化します[＃1104](https://github.com/pingcap/tidb-ansible/pull/1104)
