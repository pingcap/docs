---
title: Use TiSpark to Read TiFlash Replicas
summary: Learn how to use TiSpark to read TiFlash replicas.
---

# TiSpark を使用して TiFlash レプリカを読み取る {#use-tispark-to-read-tiflash-replicas}

このドキュメントでは、TiSpark を使用して TiFlash レプリカを読み取る方法を紹介します。

現在、TiSpark を使用して、TiDB のエンジン分離と同様の方法で TiFlash レプリカを読み取ることができます。このメソッドは、 `spark.tispark.isolation_read_engines`つのパラメーターを構成することです。パラメータ値のデフォルトは`tikv,tiflash`です。これは、CBO の選択に従って、TiDB が TiFlash または TiKV からデータを読み取ることを意味します。パラメータ値を`tiflash`に設定すると、TiDB が強制的に TiFlash からデータを読み取ることを意味します。

> **ノート：**
>
> このパラメーターが`tiflash`に設定されている場合、クエリに含まれるすべてのテーブルの TiFlash レプリカのみが読み取られ、これらのテーブルには TiFlash レプリカが必要です。 TiFlash レプリカを持たないテーブルの場合、エラーが報告されます。このパラメーターを`tikv`に設定すると、TiKV レプリカのみが読み取られます。

このパラメーターは、次のいずれかの方法で構成できます。

-   `spark-defaults.conf`ファイルに次の項目を追加します。

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

-   Spark シェルまたは Thriftサーバーを初期化するときに、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`を追加します。

-   リアルタイムで Spark シェルに`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`を設定します。

-   サーバーがビーライン経由で接続された後、Thriftサーバーに`set spark.tispark.isolation_read_engines=tiflash`を設定します。
