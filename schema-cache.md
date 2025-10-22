---
title: Schema Cache
summary: TiDB は、スキーマ情報に対して LRU (Least Recently Used) ベースのキャッシュ メカニズムを採用しており、これによりメモリ使用量が大幅に削減され、多数のデータベースとテーブルがあるシナリオでのパフォーマンスが向上します。
---

# スキーマキャッシュ {#schema-cache}

マルチテナントのシナリオによっては、数十万、あるいは数百万ものデータベースやテーブルが存在する場合があります。これらすべてのデータベースとテーブルのスキーマ情報をメモリにロードすると、大量のメモリを消費するだけでなく、アクセスパフォーマンスも低下します。この問題に対処するため、TiDBはLRU（Least Recently Used：最長時間未使用）に似たスキーマキャッシュメカニズムを導入しています。メモリにキャッシュされるのは、最も最近アクセスされたデータベースとテーブルのスキーマ情報のみです。

> **注記：**
>
> 現在、この機能はクラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## スキーマキャッシュを構成する {#configure-schema-cache}

システム変数[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)構成することで、スキーマ キャッシュ機能を有効にすることができます。

## ベストプラクティス {#best-practices}

-   データベースとテーブルの数が多いシナリオ (たとえば、100,000 を超えるデータベースとテーブル) の場合、またはデータベースとテーブルの数がシステム パフォーマンスに影響を与えるほど大きい場合は、スキーマ キャッシュ機能を有効にすることをお勧めします。
-   スキーマキャッシュのヒット率は、TiDBダッシュボードの**「スキーマロード」**セクションにあるサブパネル**「Infoschema v2 Cache Operation」**で監視できます。ヒット率が低い場合は、値を[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)に増やしてください。
-   TiDB ダッシュボードの**スキーマ ロード**セクションのサブパネル**Infoschema v2 キャッシュ サイズ**を観察することで、使用されているスキーマ キャッシュの現在のサイズを監視できます。

<CustomContent platform="tidb">

-   TiDB の起動時間を短縮するには、 [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)無効にすることをお勧めします。
-   多数のテーブル (たとえば、100,000 を超えるテーブル) を作成する必要がある場合は、 [`split-table`](/tidb-configuration-file.md#split-table)パラメータを`false`に設定してリージョンの数を減らし、TiKV のメモリ使用量を減らすことをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB の起動時間を短縮するには、 [`performance.force-init-stats`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#force-init-stats-new-in-v657-and-v710)無効にすることをお勧めします。
-   多数のテーブル (たとえば、100,000 を超えるテーブル) を作成する必要がある場合は、 [`split-table`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#split-table)パラメータを`false`に設定してリージョンの数を減らし、TiKV のメモリ使用量を減らすことをお勧めします。

</CustomContent>

## 既知の制限事項 {#known-limitations}

多数のデータベースとテーブルがあるシナリオでは、次の既知の問題が存在します。

-   1 つのクラスター内のテーブル数は 300 万を超えることはできません。

-   1 つのクラスター内のテーブル数が 300,000 を超える場合は、値[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)を`0`に設定しないでください。TiDB のメモリ不足 (OOM) が発生する可能性があります。

-   外部キーを使用すると、クラスター内の DDL 操作の実行時間が長くなる可能性があります。

-   テーブルへのアクセスが不規則な場合（例えば、あるテーブルセットがtime1にアクセスされ、別のテーブルセットがtime2にアクセスされるなど）、かつ`tidb_schema_cache_size`の値が小さい場合、スキーマ情報が頻繁に削除・キャッシュされ、パフォーマンスの変動につながる可能性があります。この機能は、頻繁にアクセスされるデータベースやテーブルが比較的固定されているシナリオに適しています。

-   統計情報はタイムリーに収集されない可能性があります。

-   一部のメタデータ情報へのアクセスが遅くなる可能性があります。

-   スキーマ キャッシュのオン/オフを切り替えるには、待機期間が必要です。

-   次のような、すべてのメタデータ情報を列挙する操作は遅くなる可能性があります。

    -   `SHOW FULL TABLES`
    -   `FLASHBACK`
    -   `ALTER TABLE ... SET TIFLASH MODE ...`

-   属性が[`AUTO_INCREMENT`](/auto-increment.md)または[`AUTO_RANDOM`](/auto-random.md)テーブルを使用する場合、スキーマキャッシュのサイズが小さいと、これらのテーブルのメタデータがキャッシュに頻繁に入出力される可能性があります。その結果、割り当てられたID範囲が完全に使用される前に無効になり、IDジャンプが発生する可能性があります。書き込みが集中するシナリオでは、ID範囲が使い果たされる可能性もあります。異常なID割り当て動作を最小限に抑え、システムの安定性を向上させるために、以下の対策を講じることをお勧めします。

    -   監視パネルでスキーマキャッシュのヒット率とサイズをビュー、キャッシュ設定が適切かどうかを評価します。スキーマキャッシュのサイズを適切に増やすことで、頻繁な削除を削減できます。
    -   ID ジャンプを防ぐには[`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache)を`1`に設定します。
    -   ID 範囲が狭くなりすぎないように、シャード ビットと予約ビットを`AUTO_RANDOM`に適切に構成します。
