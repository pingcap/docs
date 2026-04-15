---
title: Schema Cache
summary: TiDBは、スキーマ情報に対してLRU（Least Recently Used：最も使用頻度の低いもの）ベースのキャッシュメカニズムを採用しており、これによりメモリ使用量が大幅に削減され、データベースやテーブルの数が多いシナリオでのパフォーマンスが向上します。
---

# スキーマキャッシュ {#schema-cache}

マルチテナント環境では、データベースやテーブルが数十万、あるいは数百万にも及ぶ場合があります。これらのデータベースやテーブルすべてのスキーマ情報をメモリにロードすると、大量のメモリを消費するだけでなく、アクセス性能も低下します。この問題を解決するため、TiDBはLRU（Least Recently Used：最小使用頻度）に似たスキーマキャッシュメカニズムを導入しています。最も最近アクセスされたデータベースやテーブルのスキーマ情報のみがメモリにキャッシュされます。

> **注記：**
>
> 現在、この機能は[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## スキーマキャッシュの設定 {#configure-schema-cache}

システム変数[`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)を設定することで、スキーマキャッシュ機能を有効にできます。

## ベストプラクティス {#best-practices}

-   データベースとテーブルの数が非常に多い場合（例えば、10万を超えるデータベースとテーブルがある場合）、またはデータベースとテーブルの数がシステムのパフォーマンスに影響を与えるほど多い場合は、スキーマキャッシュ機能を有効にすることをお勧めします。
-   TiDBダッシュボードの**「スキーマロード**」セクションにあるサブパネル**「Infoschema v2 Cache Operation」**を確認することで、スキーマキャッシュのヒット率を監視できます。ヒット率が低い場合は、 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)の値を増やすことができます。
-   TiDBダッシュボードの**「スキーマロード」**セクションにあるサブパネル**「Infoschema v2 Cache Size」**を確認することで、現在使用されているスキーマキャッシュのサイズを監視できます。

<CustomContent platform="tidb">

-   TiDBの起動時間を短縮するために、 [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)を無効にすることをお勧めします。
-   多数のテーブル（例えば、10万個以上のテーブル）を作成する必要がある場合は、リージョンの数を減らし、TiKVのメモリ使用量を削減するために、 [`split-table`](/tidb-configuration-file.md#split-table)パラメータを`false`に設定することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDBの起動時間を短縮するために、 [`performance.force-init-stats`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#force-init-stats-new-in-v657-and-v710)を無効にすることをお勧めします。
-   多数のテーブル（例えば、10万個以上のテーブル）を作成する必要がある場合は、リージョンの数を減らし、TiKVのメモリ使用量を削減するために、 [`split-table`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#split-table)パラメータを`false`に設定することをお勧めします。

</CustomContent>

## 既知の制限事項 {#known-limitations}

多数のデータベースとテーブルが存在するシナリオでは、以下の既知の問題が存在します。

-   単一クラスター内のテーブル数は300万を超えることはできません。

-   単一クラスタ内のテーブル数が 300,000 を超える場合は、 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)の値を`0`に設定しないでください。TiDB のメモリ不足 (OOM) を引き起こす可能性があります。

-   外部キーを使用すると、クラスタ環境におけるDDL操作の実行時間が長くなる可能性があります。

-   テーブルへのアクセスが不規則な場合（例えば、あるテーブル群が時刻1にアクセスされ、別のテーブル群が時刻2にアクセスされる場合など）、 `tidb_schema_cache_size`の値が小さいと、スキーマ情報が頻繁に削除およびキャッシュされ、パフォーマンスの変動につながる可能性があります。この機能は、頻繁にアクセスされるデータベースやテーブルが比較的固定されているシナリオに適しています。

-   統計情報は適時に収集されない可能性がある。

-   一部のメタデータ情報へのアクセス速度が低下する可能性があります。

-   スキーマキャッシュのオン/オフを切り替えるには、待機時間が必要です。

-   すべてのメタデータ情報を列挙する操作は、以下のような場合に遅くなる可能性があります。

    -   `SHOW FULL TABLES`
    -   `FLASHBACK`
    -   `ALTER TABLE ... SET TIFLASH MODE ...`

-   [`AUTO_INCREMENT`](/auto-increment.md)または[`AUTO_RANDOM`](/auto-random.md)属性を持つテーブルを使用する場合、スキーマ キャッシュ サイズが小さいと、これらのテーブルのメタデータが頻繁にキャッシュに出入りする可能性があります。その結果、割り当てられた ID 範囲が完全に使用される前に無効になり、ID ジャンプが発生する可能性があります。書き込みが集中するシナリオでは、ID 範囲が枯渇することさえあります。異常な ID 割り当て動作を最小限に抑え、システムの安定性を向上させるために、次の対策を講じることをお勧めします。

    -   監視パネルでスキーマキャッシュのヒット率とサイズをビュー、キャッシュ設定が適切かどうかを評価してください。スキーマキャッシュのサイズを適切に増やすことで、キャッシュの強制削除頻度を減らすことができます。
    -   IDジャンプを防ぐには、 [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) `1`に設定してください。
    -   ID 範囲が小さすぎることを避けるため、 `AUTO_RANDOM`のシャードビットと予約ビットを適切に設定してください。
