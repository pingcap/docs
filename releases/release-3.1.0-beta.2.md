---
title: TiDB 3.1 Beta.2 Release Notes
---

# TiDB 3.1 ベータ.2 リリースノート {#tidb-3-1-beta-2-release-notes}

発売日：2020年3月9日

TiDB バージョン: 3.1.0-beta.2

TiDB Ansible バージョン: 3.1.0-beta.2

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 3.1.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDB Lightning
        -   構成ファイルで構成されていない特定の項目については、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)で指定したデフォルト構成を使用します[#255](https://github.com/pingcap/tidb-lightning/pull/255)
        -   `--tidb-password` CLI パラメータを追加して TiDB パスワードを設定します[#253](https://github.com/pingcap/tidb-lightning/pull/253)

## 新機能 {#new-features}

-   TiDB
    -   TiDB がランダムな整数を主キーに自動的に割り当てることができるように、column 属性に`AutoRandom`キーワードを追加することをサポートします。これにより、 `AUTO_INCREMENT`の主キーによって引き起こされる書き込みホット スポットが回避されます[#14555](https://github.com/pingcap/tidb/pull/14555)
    -   DDL ステートメントによる列ストア レプリカの作成または削除のサポート[#14537](https://github.com/pingcap/tidb/pull/14537)
    -   オプティマイザーが異なるstorageエンジンを個別に選択できる機能を追加します[#14537](https://github.com/pingcap/tidb/pull/14537)
    -   SQL ヒントがさまざまなstorageエンジンをサポートする機能を追加[#14537](https://github.com/pingcap/tidb/pull/14537)
    -   `tidb_replica_read`システム変数[#13464](https://github.com/pingcap/tidb/pull/13464)を使用して、フォロワーからのデータの読み取りをサポートします。
-   TiKV
    -   Raftstore
        -   `peer_address`パラメータを追加して、他のノードを TiKVサーバー[#6491](https://github.com/tikv/tikv/pull/6491)に接続します。
        -   `read_index`と`read_index_resp`監視メトリックを追加して、 `ReadIndex`のリクエストの数を監視します[#6610](https://github.com/tikv/tikv/pull/6610)
-   PDクライアント
    -   PD [#6605](https://github.com/tikv/tikv/pull/6605)へのローカル スレッドの統計レポートのサポート
-   バックアップ
    -   `RocksIOLimiter`フロー制御ライブラリを Rust の`async-speed-limit`フロー制御ライブラリに置き換えて、ファイル[#6462](https://github.com/tikv/tikv/pull/6462)をバックアップする際の余分なメモリコピーを排除します。
-   PD
    -   場所ラベル名にバックスラッシュを使用できるようにする[#2084](https://github.com/pingcap/pd/pull/2084)
-   TiFlash
    -   初回リリース
-   TiDB Ansible
    -   1 つのクラスターでの複数の Grafana/Prometheus/Alertmanager のデプロイのサポート[#1143](https://github.com/pingcap/tidb-ansible/pull/1143)
    -   TiFlashコンポーネントの展開のサポート[#1148](https://github.com/pingcap/tidb-ansible/pull/1148)
    -   TiFlashコンポーネント[#1152](https://github.com/pingcap/tidb-ansible/pull/1152)に関連する監視メトリクスを追加します。

## バグの修正 {#bug-fixes}

-   TiKV
    -   Raftstore
        -   Hibernate リージョン[#6450](https://github.com/tikv/tikv/pull/6450)からデータが適切に読み取られないため、読み取りリクエストが処理できない問題を修正します。
        -   リーダー転送プロセス[#6613](https://github.com/tikv/tikv/pull/6613)中の`ReadIndex`リクエストによって引き起こされるpanicの問題を修正
        -   一部の特殊な状況で休止領域が正しく起動されない問題を修正[#6730](https://github.com/tikv/tikv/pull/6730) [#6737](https://github.com/tikv/tikv/pull/6737) [#6972](https://github.com/tikv/tikv/pull/6972)
    -   バックアップ
        -   追加データのバックアップによって引き起こされる復元中のデータ インデックスの不一致を修正します[#6659](https://github.com/tikv/tikv/pull/6659)
        -   バックアップ中に削除された値が誤って処理されることによって引き起こされるpanicを修正します[#6726](https://github.com/tikv/tikv/pull/6726)
-   PD
    -   ルール チェッカーが店舗をリージョン[#2161](https://github.com/pingcap/pd/pull/2161)に割り当てることができないために発生したpanicを修正しました。
-   ツール
    -   TiDB Lightning
        -   Webインターフェースがサーバーモード[#259](https://github.com/pingcap/tidb-lightning/pull/259)以外で動作しないバグを修正
    -   BR (バックアップと復元)
        -   データ[#152](https://github.com/pingcap/br/pull/152)の復元時に発生した回復不可能なエラーにより、 BR が時間内に終了できない問題を修正します。
-   TiDB Ansible
    -   一部のシナリオでPDLeaderが取得できないため、ローリングアップデートコマンドが失敗する問題を修正[#1122](https://github.com/pingcap/tidb-ansible/pull/1122)
