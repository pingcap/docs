---
title: TiDB 4.0.0 Beta.2 Release Notes
---

# TiDB4.0.0Beta.2リリースノート {#tidb-4-0-0-beta-2-release-notes}

発売日：2020年3月18日

TiDBバージョン：4.0.0-beta.2

TiDB Ansibleバージョン：4.0.0-beta.2

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDB Binlog
        -   Drainer5で`disable-dispatch`と`disable-causality`が構成されている場合にシステムがエラーを返し終了する問題を修正し[＃915](https://github.com/pingcap/tidb-binlog/pull/915)

## 新機能 {#new-features}

-   TiKV
    -   動的に更新された構成をハードウェアディスクに永続化することをサポート[＃6684](https://github.com/tikv/tikv/pull/6684)

-   PD
    -   動的に更新された構成をハードウェアディスクに永続化することをサポート[＃2153](https://github.com/pingcap/pd/pull/2153)

-   ツール
    -   TiDB Binlog
        -   TiDBクラスター間の双方向データレプリケーションをサポートする[＃879](https://github.com/pingcap/tidb-binlog/pull/879) [＃903](https://github.com/pingcap/tidb-binlog/pull/903)
    -   TiDB Lightning
        -   TLS構成をサポートする[＃40](https://github.com/tikv/importer/pull/40) [＃270](https://github.com/pingcap/tidb-lightning/pull/270)
    -   TiCDC
        -   次の機能を提供する変更データキャプチャ（CDC）の初期リリース。
            -   TiKVからの変更されたデータのキャプチャをサポート
            -   変更されたデータをTiKVからMySQL互換データベースに複製することをサポートし、最終的なデータの一貫性を保証します
            -   変更されたデータのKafkaへの複製をサポートし、最終的なデータの一貫性または行レベルの秩序のいずれかを保証します
            -   プロセスレベルの高可用性を提供する
    -   バックアップと復元（BR）
        -   増分バックアップや[＃175](https://github.com/pingcap/br/pull/175)へのファイルのバックアップなどの実験的機能を有効にする

-   TiDB Ansible
    -   [＃1196](https://github.com/pingcap/tidb-ansible/pull/1196)へのノード情報の注入をサポートします。
    -   ARMプラットフォームでのTiDBサービスの展開のサポート[＃1204](https://github.com/pingcap/tidb-ansible/pull/1204)

## バグの修正 {#bug-fixes}

-   TiKV
    -   バックアップ中に空の短い値を満たすときに発生する可能性のあるパニックの問題を修正します[＃6718](https://github.com/tikv/tikv/pull/6718)
    -   場合によっては休止状態の[＃6772](https://github.com/tikv/tikv/pull/6672)が正しく起動されない可能性があるという問題を修正し[＃6648](https://github.com/tikv/tikv/pull/6648) [＃6376](https://github.com/tikv/tikv/pull/6736)

-   PD
    -   ルールチェッカーがリージョン[＃2160](https://github.com/pingcap/pd/pull/2160)にストアを割り当てられないというパニックの問題を修正します
    -   動的構成を有効にした後、リーダーが切り替えられているときに構成にレプリケーション遅延が発生する可能性があるという問題を修正します[＃2154](https://github.com/pingcap/pd/pull/2154)

-   ツール
    -   バックアップと復元（BR）
        -   PDが大きなサイズのデータを処理できないためにBRが大きなサイズのデータを復元できない可能性がある問題を修正します[＃167](https://github.com/pingcap/br/pull/167)
        -   BRバージョンがTiDBバージョン[＃186](https://github.com/pingcap/br/pull/186)と互換性がないために発生したBR障害を修正します
        -   BRバージョンがTiFlash1と互換性がないために発生したBR障害を修正し[＃194](https://github.com/pingcap/br/pull/194)
