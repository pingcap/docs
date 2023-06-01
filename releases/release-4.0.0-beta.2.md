---
title: TiDB 4.0.0 Beta.2 Release Notes
---

# TiDB 4.0.0 ベータ.2 リリースノート {#tidb-4-0-0-beta-2-release-notes}

発売日：2020年3月18日

TiDB バージョン: 4.0.0-beta.2

TiDB Ansible バージョン: 4.0.0-beta.2

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDBBinlog
        -   Drainer [<a href="https://github.com/pingcap/tidb-binlog/pull/915">#915</a>](https://github.com/pingcap/tidb-binlog/pull/915)で`disable-dispatch`と`disable-causality`が設定されている場合、システムがエラーを返して終了する問題を修正

## 新機能 {#new-features}

-   TiKV
    -   動的に更新された構成のハードウェア ディスクへの永続化のサポート[<a href="https://github.com/tikv/tikv/pull/6684">#6684</a>](https://github.com/tikv/tikv/pull/6684)

-   PD
    -   動的に更新された構成のハードウェア ディスクへの永続化のサポート[<a href="https://github.com/pingcap/pd/pull/2153">#2153</a>](https://github.com/pingcap/pd/pull/2153)

-   ツール
    -   TiDBBinlog
        -   TiDB クラスター間の双方向データ レプリケーションをサポート[<a href="https://github.com/pingcap/tidb-binlog/pull/879">#879</a>](https://github.com/pingcap/tidb-binlog/pull/879) [<a href="https://github.com/pingcap/tidb-binlog/pull/903">#903</a>](https://github.com/pingcap/tidb-binlog/pull/903)
    -   TiDB Lightning
        -   TLS 構成のサポート[<a href="https://github.com/tikv/importer/pull/40">#40</a>](https://github.com/tikv/importer/pull/40) [<a href="https://github.com/pingcap/tidb-lightning/pull/270">#270</a>](https://github.com/pingcap/tidb-lightning/pull/270)
    -   TiCDC
        -   変更データ キャプチャ (CDC) の初期リリースでは、次の機能が提供されます。
            -   TiKV からの変更データのキャプチャのサポート
            -   TiKV から MySQL 互換データベースへの変更データのレプリケーションをサポートし、最終的なデータの整合性を保証します
            -   変更されたデータの Kafka へのレプリケーションをサポートし、最終的なデータの整合性または行レベルの順序性を保証します。
            -   プロセスレベルの高可用性を提供する
    -   バックアップと復元 (BR)
        -   増分バックアップや Amazon S3 へのファイルのバックアップなどの実験的機能を有効にする[<a href="https://github.com/pingcap/br/pull/175">#175</a>](https://github.com/pingcap/br/pull/175)

-   TiDB Ansible
    -   etcd [<a href="https://github.com/pingcap/tidb-ansible/pull/1196">#1196</a>](https://github.com/pingcap/tidb-ansible/pull/1196)へのノード情報の注入のサポート
    -   ARM プラットフォームでの TiDB サービスの展開のサポート[<a href="https://github.com/pingcap/tidb-ansible/pull/1204">#1204</a>](https://github.com/pingcap/tidb-ansible/pull/1204)

## バグの修正 {#bug-fixes}

-   TiKV
    -   バックアップ中に空の short 値に遭遇したときに発生する可能性があるpanicの問題を修正します[<a href="https://github.com/tikv/tikv/pull/6718">#6718</a>](https://github.com/tikv/tikv/pull/6718)
    -   場合によっては Hibernate リージョンが正しく起動されないことがある問題を修正[<a href="https://github.com/tikv/tikv/pull/6672">#6772</a>](https://github.com/tikv/tikv/pull/6672) [<a href="https://github.com/tikv/tikv/pull/6648">#6648</a>](https://github.com/tikv/tikv/pull/6648) [<a href="https://github.com/tikv/tikv/pull/6736">#6376</a>](https://github.com/tikv/tikv/pull/6736)

-   PD
    -   ルール チェッカーがリージョン[<a href="https://github.com/pingcap/pd/pull/2160">#2160</a>](https://github.com/pingcap/pd/pull/2160)にストアを割り当てることができないというpanicの問題を修正します。
    -   動的構成を有効にした後、Leaderの切り替え時に構成にレプリケーション遅延が発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/pd/pull/2154">#2154</a>](https://github.com/pingcap/pd/pull/2154)

-   ツール
    -   バックアップと復元 (BR)
        -   PDが大容量データを処理できないため、 BRが大容量データのリストアに失敗する場合がある問題を修正[<a href="https://github.com/pingcap/br/pull/167">#167</a>](https://github.com/pingcap/br/pull/167)
        -   BRバージョンが TiDB バージョン[<a href="https://github.com/pingcap/br/pull/186">#186</a>](https://github.com/pingcap/br/pull/186)と互換性がないために発生したBRエラーを修正しました
        -   BRバージョンがTiFlash [<a href="https://github.com/pingcap/br/pull/194">#194</a>](https://github.com/pingcap/br/pull/194)と互換性がないために発生するBRエラーを修正
