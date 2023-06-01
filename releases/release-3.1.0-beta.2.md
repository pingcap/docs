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
        -   構成ファイルで構成されていない特定の項目については、 [<a href="/tidb-lightning/tidb-lightning-configuration.md">TiDB Lightningコンフィグレーション</a>](/tidb-lightning/tidb-lightning-configuration.md)で指定したデフォルト構成を使用します[<a href="https://github.com/pingcap/tidb-lightning/pull/255">#255</a>](https://github.com/pingcap/tidb-lightning/pull/255)
        -   `--tidb-password` CLI パラメータを追加して TiDB パスワードを設定します[<a href="https://github.com/pingcap/tidb-lightning/pull/253">#253</a>](https://github.com/pingcap/tidb-lightning/pull/253)

## 新機能 {#new-features}

-   TiDB
    -   TiDB がランダムな整数を主キーに自動的に割り当てることができるように、column 属性に`AutoRandom`キーワードを追加することをサポートします。これにより、 `AUTO_INCREMENT`の主キーによって引き起こされる書き込みホット スポットが回避されます[<a href="https://github.com/pingcap/tidb/pull/14555">#14555</a>](https://github.com/pingcap/tidb/pull/14555)
    -   DDL ステートメントによる列ストア レプリカの作成または削除のサポート[<a href="https://github.com/pingcap/tidb/pull/14537">#14537</a>](https://github.com/pingcap/tidb/pull/14537)
    -   オプティマイザーが異なるstorageエンジンを個別に選択できる機能を追加します[<a href="https://github.com/pingcap/tidb/pull/14537">#14537</a>](https://github.com/pingcap/tidb/pull/14537)
    -   SQL ヒントがさまざまなstorageエンジンをサポートする機能を追加[<a href="https://github.com/pingcap/tidb/pull/14537">#14537</a>](https://github.com/pingcap/tidb/pull/14537)
    -   `tidb_replica_read`システム変数[<a href="https://github.com/pingcap/tidb/pull/13464">#13464</a>](https://github.com/pingcap/tidb/pull/13464)を使用して、フォロワーからのデータの読み取りをサポートします。
-   TiKV
    -   Raftstore
        -   `peer_address`パラメータを追加して、他のノードを TiKVサーバー[<a href="https://github.com/tikv/tikv/pull/6491">#6491</a>](https://github.com/tikv/tikv/pull/6491)に接続します。
        -   `read_index`と`read_index_resp`監視メトリックを追加して、 `ReadIndex`のリクエストの数を監視します[<a href="https://github.com/tikv/tikv/pull/6610">#6610</a>](https://github.com/tikv/tikv/pull/6610)
-   PDクライアント
    -   PD [<a href="https://github.com/tikv/tikv/pull/6605">#6605</a>](https://github.com/tikv/tikv/pull/6605)へのローカル スレッドの統計レポートのサポート
-   バックアップ
    -   `RocksIOLimiter`フロー制御ライブラリを Rust の`async-speed-limit`フロー制御ライブラリに置き換えて、ファイル[<a href="https://github.com/tikv/tikv/pull/6462">#6462</a>](https://github.com/tikv/tikv/pull/6462)をバックアップする際の余分なメモリコピーを排除します。
-   PD
    -   場所ラベル名にバックスラッシュを使用できるようにする[<a href="https://github.com/pingcap/pd/pull/2084">#2084</a>](https://github.com/pingcap/pd/pull/2084)
-   TiFlash
    -   初回リリース
-   TiDB Ansible
    -   1 つのクラスターでの複数の Grafana/Prometheus/Alertmanager のデプロイのサポート[<a href="https://github.com/pingcap/tidb-ansible/pull/1143">#1143</a>](https://github.com/pingcap/tidb-ansible/pull/1143)
    -   TiFlashコンポーネントの展開のサポート[<a href="https://github.com/pingcap/tidb-ansible/pull/1148">#1148</a>](https://github.com/pingcap/tidb-ansible/pull/1148)
    -   TiFlashコンポーネント[<a href="https://github.com/pingcap/tidb-ansible/pull/1152">#1152</a>](https://github.com/pingcap/tidb-ansible/pull/1152)に関連する監視メトリクスを追加します。

## バグの修正 {#bug-fixes}

-   TiKV
    -   Raftstore
        -   Hibernate リージョン[<a href="https://github.com/tikv/tikv/pull/6450">#6450</a>](https://github.com/tikv/tikv/pull/6450)からデータが適切に読み取られないため、読み取りリクエストが処理できない問題を修正します。
        -   リーダー転送プロセス[<a href="https://github.com/tikv/tikv/pull/6613">#6613</a>](https://github.com/tikv/tikv/pull/6613)中の`ReadIndex`リクエストによって引き起こされるpanicの問題を修正
        -   一部の特殊な状況で休止領域が正しく起動されない問題を修正[<a href="https://github.com/tikv/tikv/pull/6730">#6730</a>](https://github.com/tikv/tikv/pull/6730) [<a href="https://github.com/tikv/tikv/pull/6737">#6737</a>](https://github.com/tikv/tikv/pull/6737) [<a href="https://github.com/tikv/tikv/pull/6972">#6972</a>](https://github.com/tikv/tikv/pull/6972)
    -   バックアップ
        -   追加データのバックアップによって引き起こされる復元中のデータ インデックスの不一致を修正します[<a href="https://github.com/tikv/tikv/pull/6659">#6659</a>](https://github.com/tikv/tikv/pull/6659)
        -   バックアップ中に削除された値が誤って処理されることによって引き起こされるpanicを修正します[<a href="https://github.com/tikv/tikv/pull/6726">#6726</a>](https://github.com/tikv/tikv/pull/6726)
-   PD
    -   ルール チェッカーが店舗をリージョン[<a href="https://github.com/pingcap/pd/pull/2161">#2161</a>](https://github.com/pingcap/pd/pull/2161)に割り当てることができないために発生したpanicを修正しました。
-   ツール
    -   TiDB Lightning
        -   Webインターフェースがサーバーモード[<a href="https://github.com/pingcap/tidb-lightning/pull/259">#259</a>](https://github.com/pingcap/tidb-lightning/pull/259)以外で動作しないバグを修正
    -   BR (バックアップと復元)
        -   データ[<a href="https://github.com/pingcap/br/pull/152">#152</a>](https://github.com/pingcap/br/pull/152)の復元時に発生した回復不能エラーにより、 BR が時間内に終了できない問題を修正します。
-   TiDB Ansible
    -   一部のシナリオでPDLeaderが取得できないため、ローリングアップデートコマンドが失敗する問題を修正[<a href="https://github.com/pingcap/tidb-ansible/pull/1122">#1122</a>](https://github.com/pingcap/tidb-ansible/pull/1122)
