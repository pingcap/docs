---
title: Use TiSpark to Read TiFlash Replicas
summary: Learn how to use TiSpark to read TiFlash replicas.
---

# TiSpark を使用してTiFlashレプリカを読み取る {#use-tispark-to-read-tiflash-replicas}

このドキュメントでは、TiSpark を使用してTiFlashレプリカを読み取る方法を紹介します。

現在、TiSpark を使用して、TiDB のエンジン分離と同様の方法でTiFlashレプリカを読み取ることができます。この方法は`spark.tispark.isolation_read_engines`パラメータを設定する方法です。パラメータ値のデフォルトは`tikv,tiflash`です。これは、TiDB が CBO の選択に従ってTiFlashまたは TiKV からデータを読み取ることを意味します。パラメータ値を`tiflash`に設定すると、TiDB がTiFlashからデータを強制的に読み取ります。

> **注記：**
>
> このパラメータが`tiflash`に設定されている場合、クエリに含まれるすべてのテーブルのTiFlashレプリカのみが読み取られ、これらのテーブルにはTiFlashレプリカが必要です。 TiFlashレプリカがないテーブルの場合、エラーが報告されます。このパラメータを`tikv`に設定すると、TiKV レプリカのみが読み取られます。

このパラメータは、次のいずれかの方法で構成できます。

-   `spark-defaults.conf`ファイルに次の項目を追加します。

        spark.tispark.isolation_read_engines tiflash

-   Spark シェルまたは Thriftサーバーを初期化する場合は、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`を追加します。

-   Spark シェルにリアルタイムで`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`を設定します。

-   サーバーがbeeline経由で接続された後、Thriftサーバーに`set spark.tispark.isolation_read_engines=tiflash`を設定します。
