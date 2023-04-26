---
title: TiDB 4.0.0 Beta.2 Release Notes
---

# TiDB 4.0.0 Beta.2 リリースノート {#tidb-4-0-0-beta-2-release-notes}

発売日：2020年3月18日

TiDB バージョン: 4.0.0-beta.2

TiDB アンシブル バージョン: 4.0.0-beta.2

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDBBinlog
        -   Drainer [#915](https://github.com/pingcap/tidb-binlog/pull/915)で`disable-dispatch`と`disable-causality`が構成されている場合、システムがエラーを返し、終了する問題を修正します。

## 新機能 {#new-features}

-   TiKV
    -   動的に更新された構成をハードウェア ディスクに保持するサポート[#6684](https://github.com/tikv/tikv/pull/6684)

-   PD
    -   動的に更新された構成をハードウェア ディスクに保持するサポート[#2153](https://github.com/pingcap/pd/pull/2153)

-   ツール
    -   TiDBBinlog
        -   TiDB クラスタ間の双方向データ複製をサポート[#879](https://github.com/pingcap/tidb-binlog/pull/879) [#903](https://github.com/pingcap/tidb-binlog/pull/903)
    -   TiDB Lightning
        -   TLS 構成のサポート[#40](https://github.com/tikv/importer/pull/40) [#270](https://github.com/pingcap/tidb-lightning/pull/270)
    -   TiCDC
        -   次の機能を提供する変更データ キャプチャ (CDC) の初期リリース:
            -   TiKV からの変更データのキャプチャをサポート
            -   TiKV から MySQL 互換データベースへの変更データの複製をサポートし、最終的なデータの一貫性を保証します
            -   変更されたデータの Kafka へのレプリケートをサポートし、最終的なデータの整合性または行レベルの順序性を保証します
            -   プロセスレベルの高可用性を提供
    -   バックアップと復元 (BR)
        -   増分バックアップや Amazon S3 へのファイルのバックアップなどの実験的機能を有効にする[#175](https://github.com/pingcap/br/pull/175)

-   TiDB アンシブル
    -   etcd [#1196](https://github.com/pingcap/tidb-ansible/pull/1196)へのノード情報の注入のサポート
    -   ARM プラットフォームでの TiDB サービスの展開をサポート[#1204](https://github.com/pingcap/tidb-ansible/pull/1204)

## バグの修正 {#bug-fixes}

-   TiKV
    -   バックアップ中に空の短い値に遭遇したときに発生する可能性があるpanicの問題を修正します[#6718](https://github.com/tikv/tikv/pull/6718)
    -   場合によっては Hibernate Regions が正しく起動されない可能性がある問題を修正します[#6772](https://github.com/tikv/tikv/pull/6672) [#6648](https://github.com/tikv/tikv/pull/6648) [#6376](https://github.com/tikv/tikv/pull/6736)

-   PD
    -   ルール チェッカーがストアをリージョン[#2160](https://github.com/pingcap/pd/pull/2160)に割り当てられないというpanicの問題を修正します。
    -   動的構成が有効になった後、Leaderが切り替えられているときに構成でレプリケーションの遅延が発生する可能性があるという問題を修正します[#2154](https://github.com/pingcap/pd/pull/2154)

-   ツール
    -   バックアップと復元 (BR)
        -   PD が大容量データを処理できないため、 BRが大容量データの復元に失敗する場合がある問題を修正[#167](https://github.com/pingcap/br/pull/167)
        -   BRのバージョンが TiDB バージョン[#186](https://github.com/pingcap/br/pull/186)と互換性がないために発生したBRの障害を修正
        -   BRのバージョンがTiFlash [#194](https://github.com/pingcap/br/pull/194)と互換性がないために発生したBRの障害を修正
