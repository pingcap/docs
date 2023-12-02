---
title: TiDB 4.0.0 Beta.1 Release Notes
---

# TiDB 4.0.0 ベータ.1 リリースノート {#tidb-4-0-0-beta-1-release-notes}

発売日：2020年2月28日

TiDB バージョン: 4.0.0-beta.1

TiDB Ansible バージョン: 4.0.0-beta.1

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   `log.enable-slow-log`構成項目のタイプを整数からブール値[#14864](https://github.com/pingcap/tidb/pull/14864)に変更します。
    -   `mysql.user`システム テーブルの`password`フィールド名を`authentication_string`に変更して、 MySQL 5.7との一貫性を確保します (**この互換性の変更は、以前のバージョンにロールバックできないことを意味します)。** [#14598](https://github.com/pingcap/tidb/pull/14598)
    -   `txn-total-size-limit`設定項目のデフォルト値を`1GB`から`100MB`に調整します[#14522](https://github.com/pingcap/tidb/pull/14522)
    -   PD [#14750](https://github.com/pingcap/tidb/pull/14750) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)から読み取られた構成アイテムの動的変更または更新をサポート

-   TiKV
    -   `readpool.unify-read-pool`構成項目 (デフォルトでは`True` ) を追加して、ポイント クエリがコプロセッサー[#6375](https://github.com/tikv/tikv/pull/6375) [#6401](https://github.com/tikv/tikv/pull/6401) [#6534](https://github.com/tikv/tikv/pull/6534) [#6582](https://github.com/tikv/tikv/pull/6582) [#6585](https://github.com/tikv/tikv/pull/6585) [#6593](https://github.com/tikv/tikv/pull/6593) [#6597](https://github.com/tikv/tikv/pull/6597) [#6677](https://github.com/tikv/tikv/pull/6677)と同じスレッドを使用するかどうかを制御します。

-   PD
    -   HTTP API を最適化して、構成マネージャー[#2080](https://github.com/pingcap/pd/pull/2080)と互換性を持たせる

-   TiDB Lightning
    -   構成ファイルで構成されていない特定の項目については、ドキュメントで指定されているデフォルト構成を使用します[#255](https://github.com/pingcap/tidb-lightning/pull/255)

-   TiDB Ansible
    -   `theflash`から`tiflash` [#1130](https://github.com/pingcap/tidb-ansible/pull/1130)に名前を変更します
    -   TiFlash の設定ファイル[#1138](https://github.com/pingcap/tidb-ansible/pull/1138)のデフォルト値と関連設定を最適化します。

## 新機能 {#new-features}

-   TiDB
    -   `SLOW_QUERY / CLUSTER_SLOW_QUERY`システム テーブル内の任意の時点の低速ログのクエリのサポート[#14840](https://github.com/pingcap/tidb/pull/14840) [#14878](https://github.com/pingcap/tidb/pull/14878)
    -   SQLパフォーマンス診断をサポート
        -   [#14843](https://github.com/pingcap/tidb/pull/14843) [#14810](https://github.com/pingcap/tidb/pull/14810) [#14835](https://github.com/pingcap/tidb/pull/14835) [#14801](https://github.com/pingcap/tidb/pull/14801) [#14743](https://github.com/pingcap/tidb/pull/14743)
        -   [#14718](https://github.com/pingcap/tidb/pull/14718) [#14721](https://github.com/pingcap/tidb/pull/14721) [#14670](https://github.com/pingcap/tidb/pull/14670) [#14663](https://github.com/pingcap/tidb/pull/14663) [#14668](https://github.com/pingcap/tidb/pull/14668)
        -   [#14896](https://github.com/pingcap/tidb/pull/14896)
    -   `Sequence`機能をサポート[#14731](https://github.com/pingcap/tidb/pull/14731) [#14589](https://github.com/pingcap/tidb/pull/14589) [#14674](https://github.com/pingcap/tidb/pull/14674) [#14442](https://github.com/pingcap/tidb/pull/14442) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)
    -   PD [#14750](https://github.com/pingcap/tidb/pull/14750) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)から読み取られた構成アイテムの動的変更または更新をサポート
    -   負荷分散ポリシーに従ってさまざまなロールからデータを自動的に読み取る機能を追加し、この機能を有効にする`leader-and-follower`システム変数を追加します[#14761](https://github.com/pingcap/tidb/pull/14761)
    -   `Coercibility`機能を追加[#14739](https://github.com/pingcap/tidb/pull/14739)
    -   パーティションテーブルでのTiFlashレプリカの設定をサポート[#14735](https://github.com/pingcap/tidb/pull/14735) [#14713](https://github.com/pingcap/tidb/pull/14713) [#14644](https://github.com/pingcap/tidb/pull/14644)
    -   `SLOW_QUERY`テーブル[#14451](https://github.com/pingcap/tidb/pull/14451)の権限チェックを改善します。
    -   SQL 結合の使用時にメモリが不十分な場合、中間結果をディスク ファイルに自動的に書き込むサポート[#14708](https://github.com/pingcap/tidb/pull/14708) [#14279](https://github.com/pingcap/tidb/pull/14279)
    -   `information_schema.PARTITIONS`システム テーブル[#14347](https://github.com/pingcap/tidb/pull/14347)に対するクエリによるテーブル パーティションのチェックのサポート
    -   `json_objectagg`集計関数[#11154](https://github.com/pingcap/tidb/pull/11154)を追加します。
    -   拒否された接続試行の監査ログへの記録をサポート[#14594](https://github.com/pingcap/tidb/pull/14594)
    -   `max-server-connections`構成項目 (デフォルトでは`4096` ) を追加して、単一サーバーへの接続数を制御します[#14409](https://github.com/pingcap/tidb/pull/14409)
    -   サーバーレベル[#14440](https://github.com/pingcap/tidb/pull/14440)で複数のstorageエンジンを指定した分離読み取りをサポートします。
    -   `Apply`オペレーターと`Sort`オペレーターのコスト モデルを最適化して安定性を向上[#13550](https://github.com/pingcap/tidb/pull/13550) [#14708](https://github.com/pingcap/tidb/pull/14708)

-   TiKV
    -   HTTP API [#6480](https://github.com/tikv/tikv/pull/6480)を介したステータス ポートからの構成アイテムの取得をサポートします。
    -   コプロセッサー[#6341](https://github.com/tikv/tikv/pull/6341)の`Chunk Encoder`のパフォーマンスを最適化します。

-   PD
    -   ダッシュボード UI [#2086](https://github.com/pingcap/pd/pull/2086)を介したクラスター内のホットスポットの分散へのアクセスのサポート
    -   クラスターコンポーネント[#2116](https://github.com/pingcap/pd/pull/2116)の`START_TIME`と`UPTIME`のキャプチャと表示をサポート
    -   `member` API [#2130](https://github.com/pingcap/pd/pull/2130)の返されるメッセージにデプロイメント パスとコンポーネントのバージョンの情報を追加します。
    -   pd-ctl に`component`サブコマンドを追加して、他のコンポーネントの構成を変更および確認します (実験的) [#2092](https://github.com/pingcap/pd/pull/2092)

-   TiDBBinlog
    -   コンポーネント間の TLS をサポート[#904](https://github.com/pingcap/tidb-binlog/pull/904) [#894](https://github.com/pingcap/tidb-binlog/pull/894)
    -   Drainerに`kafka-client-id`構成項目を追加して、Kafka のクライアント ID [#902](https://github.com/pingcap/tidb-binlog/pull/902)を構成します。
    -   Drainer [#885](https://github.com/pingcap/tidb-binlog/pull/885)の増分バックアップ データのパージをサポート

-   TiDB Ansible
    -   1 つのクラスターでの複数の Grafana/Prometheus/Alertmanager のデプロイのサポート[#1142](https://github.com/pingcap/tidb-ansible/pull/1142)
    -   TiFlash の設定ファイル[#1145](https://github.com/pingcap/tidb-ansible/pull/1145)に`metric_port`設定項目 (デフォルトでは`8234` ) を追加します。
    -   TiFlash の設定ファイル[#1141](https://github.com/pingcap/tidb-ansible/pull/1141)に`flash_proxy_status_port`設定項目 (デフォルトでは`20292` ) を追加します。
    -   TiFlashモニタリング ダッシュボードを追加する[#1147](https://github.com/pingcap/tidb-ansible/pull/1147) [#1151](https://github.com/pingcap/tidb-ansible/pull/1151)

## バグの修正 {#bug-fixes}

-   TiDB
    -   64 文字を超える列名で`view`を作成するとエラーが報告される問題を修正[#14850](https://github.com/pingcap/tidb/pull/14850)
    -   `create or replace view`ステートメントが正しく処理されないため、 `information_schema.views`に重複データが存在する問題を修正します[#14832](https://github.com/pingcap/tidb/pull/14832)
    -   `plan cache`が有効な場合の`BatchPointGet`の誤った結果を修正[#14855](https://github.com/pingcap/tidb/pull/14855)
    -   タイムゾーンが変更された後、データが間違ったパーティションテーブルに挿入される問題を修正します[#14370](https://github.com/pingcap/tidb/pull/14370)
    -   外部結合の単純化[#14515](https://github.com/pingcap/tidb/pull/14515)中に`IsTrue`関数の無効な名前を使用して式を再構築すると発生したpanicを修正しました。
    -   `show binding`ステートメント[#14443](https://github.com/pingcap/tidb/pull/14443)の誤った権限チェックを修正しました。

-   TiKV
    -   TiDB と TiKV の`CAST`関数の一貫性のない動作を修正[#6463](https://github.com/tikv/tikv/pull/6463) [#6461](https://github.com/tikv/tikv/pull/6461) [#6459](https://github.com/tikv/tikv/pull/6459) [#6474](https://github.com/tikv/tikv/pull/6474) [#6492](https://github.com/tikv/tikv/pull/6492) [#6569](https://github.com/tikv/tikv/pull/6569)

-   TiDB Lightning
    -   Webインターフェースがサーバーモード[#259](https://github.com/pingcap/tidb-lightning/pull/259)以外で動作しないバグを修正
