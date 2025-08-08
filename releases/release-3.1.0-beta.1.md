---
title: TiDB 3.1 Beta.1 Release Notes
summary: TiDB 3.1 Beta.1は2020年1月10日にリリースされました。このリリースには、バックアップファイルの名前変更や増分バックアップ機能の追加など、TiKVへの変更が含まれています。BRなどのBRでは、バックアップの進行状況情報が改善され、パーティションテーブル向けの機能が追加されました。TiDB Ansibleでは、Transparent Huge Pages（透過的巨大ページ）が自動的に無効化され、 BRコンポーネントのGrafanaモニタリング機能が追加されました。全体として、このリリースはバックアップとリストアのプロセス、監視、そしてデプロイメントの最適化の改善に重点を置いています。
---

# TiDB 3.1 ベータ 1 リリースノート {#tidb-3-1-beta-1-release-notes}

発売日：2020年1月10日

TiDB バージョン: 3.1.0-beta.1

TiDB Ansible バージョン: 3.1.0-beta.1

## TiKV {#tikv}

-   バックアップ
    -   バックアップファイルの名前を`start_key`からハッシュ値`start_key`に変更して、ファイル名の長さを短くし、読みやすくします[＃6198](https://github.com/tikv/tikv/pull/6198)
    -   整合性チェック[＃6249](https://github.com/tikv/tikv/pull/6249)での誤検出を避けるため、RocksDBの`force_consistency_checks`チェックを無効にする
    -   増分バックアップ機能を追加する[＃6286](https://github.com/tikv/tikv/pull/6286)

-   sst_importer
    -   復元中にSSTファイルにMVCCプロパティがない問題を修正しました[＃6378](https://github.com/tikv/tikv/pull/6378)
    -   `tikv_import_download_duration` `tikv_import_ingest_bytes`の監視`tikv_import_ingest_duration`を追加して`tikv_import_download_bytes` SSTファイル[＃6404](https://github.com/tikv/tikv/pull/6404)ダウンロードと取り込みのオーバーヘッドを観察します`tikv_import_error_counter`

-   ラフトストア
    -   リーダーが変更されたときにフォロワーが古いデータを読み取り、トランザクションの分離が壊れるFollower Readの問題を修正しました[＃6343](https://github.com/tikv/tikv/pull/6343)

## ツール {#tools}

-   BR (バックアップと復元)
    -   不正確なバックアップ進行状況情報を修正[＃127](https://github.com/pingcap/br/pull/127)
    -   領域[＃122](https://github.com/pingcap/br/pull/122)分割のパフォーマンスを向上
    -   パーティションテーブル[＃137](https://github.com/pingcap/br/pull/137)のバックアップと復元機能を追加する
    -   PDスケジューラ[＃123](https://github.com/pingcap/br/pull/123)自動スケジュール機能を追加
    -   `PKIsHandle`以外のテーブルを復元した後にデータが上書きされる問題を修正[＃139](https://github.com/pingcap/br/pull/139)

## TiDB アンシブル {#tidb-ansible}

-   初期化フェーズ[＃1086](https://github.com/pingcap/tidb-ansible/pull/1086)中にオペレーティング システムで Transparent Huge Pages (THP) を自動的に無効にする機能を追加します。
-   BRコンポーネント[＃1093](https://github.com/pingcap/tidb-ansible/pull/1093)のGrafana監視を追加する
-   関連ディレクトリを自動的に作成してTiDB Lightningの展開を最適化します[＃1104](https://github.com/pingcap/tidb-ansible/pull/1104)
