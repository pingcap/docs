---
title: Use TiSpark to Read TiFlash Replicas
summary: Learn how to use TiSpark to read TiFlash replicas.
---

# TiSparkを使用してTiFlashレプリカを読み取る {#use-tispark-to-read-tiflash-replicas}

このドキュメントでは、TiSparkを使用してTiFlashレプリカを読み取る方法を紹介します。

現在、TiSparkを使用して、TiDBのエンジン分離と同様の方法でTiFlashレプリカを読み取ることができます。この方法は、 `spark.tispark.isolation_read_engines`つのパラメーターを構成するためのものです。パラメータ値のデフォルトは`tikv,tiflash`です。これは、TiDBがCBOの選択に従ってTiFlashまたはTiKVからデータを読み取ることを意味します。パラメータ値を`tiflash`に設定すると、TiDBがTiFlashからデータを強制的に読み取ることを意味します。

> **ノート**
>
> このパラメーターが`tiflash`に設定されている場合、クエリに関係するすべてのテーブルのTiFlashレプリカのみが読み取られ、これらのテーブルにはTiFlashレプリカが必要です。 TiFlashレプリカを持たないテーブルの場合、エラーが報告されます。このパラメーターを`tikv`に設定すると、TiKVレプリカのみが読み取られます。

このパラメーターは、次のいずれかの方法で構成できます。

-   `spark-defaults.conf`のファイルに次の項目を追加します。

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

-   SparkシェルまたはThriftサーバーを初期化するときに、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`を追加します。

-   リアルタイムでSparkシェルに`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`を設定します。

-   サーバーがbeeline経由で接続された後、Thriftサーバーで`set spark.tispark.isolation_read_engines=tiflash`を設定します。
