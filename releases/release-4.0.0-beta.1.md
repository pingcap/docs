---
title: TiDB 4.0.0 Beta.1 Release Notes
---

# TiDB 4.0.0 ベータ.1 リリースノート {#tidb-4-0-0-beta-1-release-notes}

発売日：2020年2月28日

TiDB バージョン: 4.0.0-beta.1

TiDB Ansible バージョン: 4.0.0-beta.1

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   `log.enable-slow-log`構成項目のタイプを整数からブール値[<a href="https://github.com/pingcap/tidb/pull/14864">#14864</a>](https://github.com/pingcap/tidb/pull/14864)に変更します。
    -   `mysql.user`システム テーブルの`password`フィールド名を`authentication_string`に変更して、 MySQL 5.7との一貫性を確保します (**この互換性の変更は、以前のバージョンにロールバックできないことを意味します)。** [<a href="https://github.com/pingcap/tidb/pull/14598">#14598</a>](https://github.com/pingcap/tidb/pull/14598)
    -   `txn-total-size-limit`設定項目のデフォルト値を`1GB`から`100MB`に調整します[<a href="https://github.com/pingcap/tidb/pull/14522">#14522</a>](https://github.com/pingcap/tidb/pull/14522)
    -   PD [<a href="https://github.com/pingcap/tidb/pull/14750">#14750</a>](https://github.com/pingcap/tidb/pull/14750) [<a href="https://github.com/pingcap/tidb/pull/14303">#14303</a>](https://github.com/pingcap/tidb/pull/14303) [<a href="https://github.com/pingcap/tidb/pull/14830">#14830</a>](https://github.com/pingcap/tidb/pull/14830)から読み取られた構成アイテムの動的変更または更新をサポート

-   TiKV
    -   `readpool.unify-read-pool`構成項目 (デフォルトでは`True` ) を追加して、ポイント クエリがコプロセッサー[<a href="https://github.com/tikv/tikv/pull/6375">#6375</a>](https://github.com/tikv/tikv/pull/6375) [<a href="https://github.com/tikv/tikv/pull/6401">#6401</a>](https://github.com/tikv/tikv/pull/6401) [<a href="https://github.com/tikv/tikv/pull/6534">#6534</a>](https://github.com/tikv/tikv/pull/6534) [<a href="https://github.com/tikv/tikv/pull/6582">#6582</a>](https://github.com/tikv/tikv/pull/6582) [<a href="https://github.com/tikv/tikv/pull/6585">#6585</a>](https://github.com/tikv/tikv/pull/6585) [<a href="https://github.com/tikv/tikv/pull/6593">#6593</a>](https://github.com/tikv/tikv/pull/6593) [<a href="https://github.com/tikv/tikv/pull/6597">#6597</a>](https://github.com/tikv/tikv/pull/6597) [<a href="https://github.com/tikv/tikv/pull/6677">#6677</a>](https://github.com/tikv/tikv/pull/6677)と同じスレッドを使用するかどうかを制御します。

-   PD
    -   HTTP API を最適化して、構成マネージャー[<a href="https://github.com/pingcap/pd/pull/2080">#2080</a>](https://github.com/pingcap/pd/pull/2080)と互換性を持たせる

-   TiDB Lightning
    -   構成ファイルで構成されていない特定の項目については、ドキュメントで指定されているデフォルト構成を使用します[<a href="https://github.com/pingcap/tidb-lightning/pull/255">#255</a>](https://github.com/pingcap/tidb-lightning/pull/255)

-   TiDB Ansible
    -   `theflash`から`tiflash` [<a href="https://github.com/pingcap/tidb-ansible/pull/1130">#1130</a>](https://github.com/pingcap/tidb-ansible/pull/1130)に名前を変更します
    -   TiFlash の設定ファイル[<a href="https://github.com/pingcap/tidb-ansible/pull/1138">#1138</a>](https://github.com/pingcap/tidb-ansible/pull/1138)のデフォルト値と関連設定を最適化します。

## 新機能 {#new-features}

-   TiDB
    -   `SLOW_QUERY / CLUSTER_SLOW_QUERY`システム テーブル内の任意の時点の低速ログのクエリのサポート[<a href="https://github.com/pingcap/tidb/pull/14840">#14840</a>](https://github.com/pingcap/tidb/pull/14840) [<a href="https://github.com/pingcap/tidb/pull/14878">#14878</a>](https://github.com/pingcap/tidb/pull/14878)
    -   SQLパフォーマンス診断をサポート
        -   [<a href="https://github.com/pingcap/tidb/pull/14843">#14843</a>](https://github.com/pingcap/tidb/pull/14843) [<a href="https://github.com/pingcap/tidb/pull/14810">#14810</a>](https://github.com/pingcap/tidb/pull/14810) [<a href="https://github.com/pingcap/tidb/pull/14835">#14835</a>](https://github.com/pingcap/tidb/pull/14835) [<a href="https://github.com/pingcap/tidb/pull/14801">#14801</a>](https://github.com/pingcap/tidb/pull/14801) [<a href="https://github.com/pingcap/tidb/pull/14743">#14743</a>](https://github.com/pingcap/tidb/pull/14743)
        -   [<a href="https://github.com/pingcap/tidb/pull/14718">#14718</a>](https://github.com/pingcap/tidb/pull/14718) [<a href="https://github.com/pingcap/tidb/pull/14721">#14721</a>](https://github.com/pingcap/tidb/pull/14721) [<a href="https://github.com/pingcap/tidb/pull/14670">#14670</a>](https://github.com/pingcap/tidb/pull/14670) [<a href="https://github.com/pingcap/tidb/pull/14663">#14663</a>](https://github.com/pingcap/tidb/pull/14663) [<a href="https://github.com/pingcap/tidb/pull/14668">#14668</a>](https://github.com/pingcap/tidb/pull/14668)
        -   [<a href="https://github.com/pingcap/tidb/pull/14896">#14896</a>](https://github.com/pingcap/tidb/pull/14896)
    -   `Sequence`機能をサポート[<a href="https://github.com/pingcap/tidb/pull/14731">#14731</a>](https://github.com/pingcap/tidb/pull/14731) [<a href="https://github.com/pingcap/tidb/pull/14589">#14589</a>](https://github.com/pingcap/tidb/pull/14589) [<a href="https://github.com/pingcap/tidb/pull/14674">#14674</a>](https://github.com/pingcap/tidb/pull/14674) [<a href="https://github.com/pingcap/tidb/pull/14442">#14442</a>](https://github.com/pingcap/tidb/pull/14442) [<a href="https://github.com/pingcap/tidb/pull/14303">#14303</a>](https://github.com/pingcap/tidb/pull/14303) [<a href="https://github.com/pingcap/tidb/pull/14830">#14830</a>](https://github.com/pingcap/tidb/pull/14830)
    -   PD [<a href="https://github.com/pingcap/tidb/pull/14750">#14750</a>](https://github.com/pingcap/tidb/pull/14750) [<a href="https://github.com/pingcap/tidb/pull/14303">#14303</a>](https://github.com/pingcap/tidb/pull/14303) [<a href="https://github.com/pingcap/tidb/pull/14830">#14830</a>](https://github.com/pingcap/tidb/pull/14830)から読み取られた構成アイテムの動的変更または更新をサポート
    -   負荷分散ポリシーに従ってさまざまなロールからデータを自動的に読み取る機能を追加し、この機能を有効にする`leader-and-follower`システム変数を追加します[<a href="https://github.com/pingcap/tidb/pull/14761">#14761</a>](https://github.com/pingcap/tidb/pull/14761)
    -   `Coercibility`機能を追加[<a href="https://github.com/pingcap/tidb/pull/14739">#14739</a>](https://github.com/pingcap/tidb/pull/14739)
    -   パーティションテーブルでのTiFlashレプリカの設定をサポート[<a href="https://github.com/pingcap/tidb/pull/14735">#14735</a>](https://github.com/pingcap/tidb/pull/14735) [<a href="https://github.com/pingcap/tidb/pull/14713">#14713</a>](https://github.com/pingcap/tidb/pull/14713) [<a href="https://github.com/pingcap/tidb/pull/14644">#14644</a>](https://github.com/pingcap/tidb/pull/14644)
    -   `SLOW_QUERY`テーブル[<a href="https://github.com/pingcap/tidb/pull/14451">#14451</a>](https://github.com/pingcap/tidb/pull/14451)の権限チェックを改善します。
    -   SQL 結合の使用時にメモリが不十分な場合、中間結果をディスク ファイルに自動的に書き込む機能をサポート[<a href="https://github.com/pingcap/tidb/pull/14708">#14708</a>](https://github.com/pingcap/tidb/pull/14708) [<a href="https://github.com/pingcap/tidb/pull/14279">#14279</a>](https://github.com/pingcap/tidb/pull/14279)
    -   `information_schema.PARTITIONS`システム テーブル[<a href="https://github.com/pingcap/tidb/pull/14347">#14347</a>](https://github.com/pingcap/tidb/pull/14347)に対するクエリによるテーブル パーティションのチェックのサポート
    -   `json_objectagg`集計関数[<a href="https://github.com/pingcap/tidb/pull/11154">#11154</a>](https://github.com/pingcap/tidb/pull/11154)を追加します。
    -   拒否された接続試行の監査ログへの記録をサポート[<a href="https://github.com/pingcap/tidb/pull/14594">#14594</a>](https://github.com/pingcap/tidb/pull/14594)
    -   `max-server-connections`構成項目 (デフォルトでは`4096` ) を追加して、単一サーバーへの接続数を制御します[<a href="https://github.com/pingcap/tidb/pull/14409">#14409</a>](https://github.com/pingcap/tidb/pull/14409)
    -   サーバーレベル[<a href="https://github.com/pingcap/tidb/pull/14440">#14440</a>](https://github.com/pingcap/tidb/pull/14440)で複数のstorageエンジンを指定した分離読み取りをサポートします。
    -   `Apply`オペレーターと`Sort`オペレーターのコスト モデルを最適化して安定性を向上[<a href="https://github.com/pingcap/tidb/pull/13550">#13550</a>](https://github.com/pingcap/tidb/pull/13550) [<a href="https://github.com/pingcap/tidb/pull/14708">#14708</a>](https://github.com/pingcap/tidb/pull/14708)

-   TiKV
    -   HTTP API [<a href="https://github.com/tikv/tikv/pull/6480">#6480</a>](https://github.com/tikv/tikv/pull/6480)を介したステータス ポートからの構成アイテムの取得をサポートします。
    -   コプロセッサー[<a href="https://github.com/tikv/tikv/pull/6341">#6341</a>](https://github.com/tikv/tikv/pull/6341)の`Chunk Encoder`のパフォーマンスを最適化します。

-   PD
    -   ダッシュボード UI [<a href="https://github.com/pingcap/pd/pull/2086">#2086</a>](https://github.com/pingcap/pd/pull/2086)を介したクラスター内のホットスポットの分散へのアクセスのサポート
    -   クラスターコンポーネント[<a href="https://github.com/pingcap/pd/pull/2116">#2116</a>](https://github.com/pingcap/pd/pull/2116)の`START_TIME`と`UPTIME`のキャプチャと表示をサポート
    -   `member` API [<a href="https://github.com/pingcap/pd/pull/2130">#2130</a>](https://github.com/pingcap/pd/pull/2130)の返されるメッセージにデプロイメント パスとコンポーネントのバージョンの情報を追加します。
    -   pd-ctl に`component`サブコマンドを追加して、他のコンポーネントの構成を変更および確認します (実験的) [<a href="https://github.com/pingcap/pd/pull/2092">#2092</a>](https://github.com/pingcap/pd/pull/2092)

-   TiDBBinlog
    -   コンポーネント間の TLS をサポート[<a href="https://github.com/pingcap/tidb-binlog/pull/904">#904</a>](https://github.com/pingcap/tidb-binlog/pull/904) [<a href="https://github.com/pingcap/tidb-binlog/pull/894">#894</a>](https://github.com/pingcap/tidb-binlog/pull/894)
    -   Drainerに`kafka-client-id`構成項目を追加して、Kafka のクライアント ID [<a href="https://github.com/pingcap/tidb-binlog/pull/902">#902</a>](https://github.com/pingcap/tidb-binlog/pull/902)を構成します。
    -   Drainer [<a href="https://github.com/pingcap/tidb-binlog/pull/885">#885</a>](https://github.com/pingcap/tidb-binlog/pull/885)の増分バックアップ データのパージをサポート

-   TiDB Ansible
    -   1 つのクラスターでの複数の Grafana/Prometheus/Alertmanager のデプロイのサポート[<a href="https://github.com/pingcap/tidb-ansible/pull/1142">#1142</a>](https://github.com/pingcap/tidb-ansible/pull/1142)
    -   TiFlash の設定ファイル[<a href="https://github.com/pingcap/tidb-ansible/pull/1145">#1145</a>](https://github.com/pingcap/tidb-ansible/pull/1145)に`metric_port`設定項目 (デフォルトでは`8234` ) を追加します。
    -   TiFlash の設定ファイル[<a href="https://github.com/pingcap/tidb-ansible/pull/1141">#1141</a>](https://github.com/pingcap/tidb-ansible/pull/1141)に`flash_proxy_status_port`設定項目 (デフォルトでは`20292` ) を追加します。
    -   TiFlashモニタリング ダッシュボードを追加する[<a href="https://github.com/pingcap/tidb-ansible/pull/1147">#1147</a>](https://github.com/pingcap/tidb-ansible/pull/1147) [<a href="https://github.com/pingcap/tidb-ansible/pull/1151">#1151</a>](https://github.com/pingcap/tidb-ansible/pull/1151)

## バグの修正 {#bug-fixes}

-   TiDB
    -   64 文字を超える列名で`view`を作成するとエラーが報告される問題を修正[<a href="https://github.com/pingcap/tidb/pull/14850">#14850</a>](https://github.com/pingcap/tidb/pull/14850)
    -   `create or replace view`ステートメントが正しく処理されないため、 `information_schema.views`に重複データが存在する問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14832">#14832</a>](https://github.com/pingcap/tidb/pull/14832)
    -   `plan cache`が有効な場合の`BatchPointGet`の誤った結果を修正[<a href="https://github.com/pingcap/tidb/pull/14855">#14855</a>](https://github.com/pingcap/tidb/pull/14855)
    -   タイムゾーンが変更された後、データが間違ったパーティションテーブルに挿入される問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14370">#14370</a>](https://github.com/pingcap/tidb/pull/14370)
    -   外部結合の単純化[<a href="https://github.com/pingcap/tidb/pull/14515">#14515</a>](https://github.com/pingcap/tidb/pull/14515)中に`IsTrue`関数の無効な名前を使用して式を再構築すると発生したpanicを修正しました。
    -   `show binding`ステートメント[<a href="https://github.com/pingcap/tidb/pull/14443">#14443</a>](https://github.com/pingcap/tidb/pull/14443)の誤った権限チェックを修正しました。

-   TiKV
    -   TiDB と TiKV の`CAST`関数の一貫性のない動作を修正[<a href="https://github.com/tikv/tikv/pull/6463">#6463</a>](https://github.com/tikv/tikv/pull/6463) [<a href="https://github.com/tikv/tikv/pull/6461">#6461</a>](https://github.com/tikv/tikv/pull/6461) [<a href="https://github.com/tikv/tikv/pull/6459">#6459</a>](https://github.com/tikv/tikv/pull/6459) [<a href="https://github.com/tikv/tikv/pull/6474">#6474</a>](https://github.com/tikv/tikv/pull/6474) [<a href="https://github.com/tikv/tikv/pull/6492">#6492</a>](https://github.com/tikv/tikv/pull/6492) [<a href="https://github.com/tikv/tikv/pull/6569">#6569</a>](https://github.com/tikv/tikv/pull/6569)

-   TiDB Lightning
    -   Webインターフェースがサーバーモード[<a href="https://github.com/pingcap/tidb-lightning/pull/259">#259</a>](https://github.com/pingcap/tidb-lightning/pull/259)以外で動作しないバグを修正
