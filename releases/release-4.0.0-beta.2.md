---
title: TiDB 4.0.0 Beta.2 Release Notes
summary: TiDB 4.0.0 Beta.2 は、2020 年 3 月 18 日にリリースされました。新機能には、動的に更新された構成の永続化、双方向データ レプリケーション、TLS 構成、変更データ キャプチャ、増分バックアップなどの実験的機能のサポートが含まれます。バグ修正では、panic、休止状態領域、レプリケーション遅延、互換性に関する問題に対処しています。TiDB Ansible は、etcd へのノード情報の挿入と ARM プラットフォームへのサービスのデプロイをサポートするようになりました。
---

# TiDB 4.0.0 Beta.2 リリースノート {#tidb-4-0-0-beta-2-release-notes}

発売日: 2020年3月18日

TiDB バージョン: 4.0.0-beta.2

TiDB Ansible バージョン: 4.0.0-beta.2

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDBBinlog
        -   Drainer [＃915](https://github.com/pingcap/tidb-binlog/pull/915)で`disable-dispatch`と`disable-causality`が設定されている場合、システムがエラーを返して終了する問題を修正しました。

## 新機能 {#new-features}

-   ティクヴ
    -   動的に更新された構成をハードウェアディスク[＃6684](https://github.com/tikv/tikv/pull/6684)に永続化することをサポートします。

-   PD
    -   動的に更新された構成をハードウェアディスク[＃2153](https://github.com/pingcap/pd/pull/2153)に永続化することをサポートします。

-   ツール
    -   TiDBBinlog
        -   TiDBクラスタ間の双方向データレプリケーションをサポート[＃879](https://github.com/pingcap/tidb-binlog/pull/879) [＃903](https://github.com/pingcap/tidb-binlog/pull/903)
    -   TiDB Lightning
        -   TLS構成をサポートする[＃40](https://github.com/tikv/importer/pull/40) [＃270](https://github.com/pingcap/tidb-lightning/pull/270)
    -   ティCDC
        -   変更データ キャプチャ (CDC) の初期リリース。次の機能が提供されます。
            -   TiKVから変更されたデータのキャプチャをサポート
            -   TiKVからMySQL互換データベースへの変更データの複製をサポートし、最終的なデータの一貫性を保証します。
            -   変更されたデータをKafkaに複製し、最終的なデータの一貫性または行レベルの順序性を保証することをサポート
            -   プロセスレベルの高可用性を提供する
    -   バックアップと復元 (BR)
        -   増分バックアップやAmazon S3へのファイルのバックアップなどの実験的機能を有効にする[＃175](https://github.com/pingcap/br/pull/175)

-   TiDB アンシブル
    -   etcd [＃1196](https://github.com/pingcap/tidb-ansible/pull/1196)へのノード情報の注入をサポート
    -   ARM プラットフォーム[＃1204](https://github.com/pingcap/tidb-ansible/pull/1204)への TiDB サービスの導入をサポート

## バグ修正 {#bug-fixes}

-   ティクヴ
    -   バックアップ中に空の短い値に遭遇したときに発生する可能性のあるpanic問題を修正しました[＃6718](https://github.com/tikv/tikv/pull/6718)
    -   場合によっては休止状態領域が正しく起動されない可能性がある問題を修正[＃6772](https://github.com/tikv/tikv/pull/6672) [＃6648](https://github.com/tikv/tikv/pull/6648) [＃6376](https://github.com/tikv/tikv/pull/6736)

-   PD
    -   ルールチェッカーがリージョン[＃2160](https://github.com/pingcap/pd/pull/2160)にストアを割り当てられないというpanic問題を修正しました。
    -   動的構成を有効にした後、Leaderが切り替えられるときに構成のレプリケーション遅延が発生する可能性がある問題を修正しました[＃2154](https://github.com/pingcap/pd/pull/2154)

-   ツール
    -   バックアップと復元 (BR)
        -   PDが大容量データを処理できないため、 BRが大容量データの復元に失敗する可能性がある問題を修正[＃167](https://github.com/pingcap/br/pull/167)
        -   BRバージョンがTiDBバージョン[＃186](https://github.com/pingcap/br/pull/186)と互換性がないため発生したBR障害を修正
        -   BRバージョンがTiFlash [＃194](https://github.com/pingcap/br/pull/194)と互換性がないため発生したBR障害を修正
