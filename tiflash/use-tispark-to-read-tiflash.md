---
title: Use TiSpark to Read TiFlash Replicas
summary: TiSpark を使用してTiFlashレプリカを読み取る方法を学習します。
---

# TiSparkを使用してTiFlashレプリカを読み取る {#use-tispark-to-read-tiflash-replicas}

このドキュメントでは、TiSpark を使用してTiFlashレプリカを読み取る方法を紹介します。

現在、TiSpark は TiDB のエンジン分離と同様の方法でTiFlashレプリカを読み取ることができます。この方法は、パラメータ`spark.tispark.isolation_read_engines`設定することです。パラメータ値はデフォルトで`tikv,tiflash`に設定されており、これは TiDB が CBO の選択に応じてTiFlashまたは TiKV からデータを読み取ります。パラメータ値を`tiflash`に設定すると、TiDB は強制的にTiFlashからデータを読み取ることを意味します。

> **注記：**
>
> このパラメータを`tiflash`に設定すると、クエリに関係するすべてのテーブルのTiFlashレプリカのみが読み取られます。これらのテーブルにはTiFlashレプリカが必要です。TiFlashTiFlashを持たないテーブルの場合はエラーが報告されます。このパラメータを`tikv`に設定すると、TiKVレプリカのみが読み取られます。

このパラメータは、次のいずれかの方法で設定できます。

-   `spark-defaults.conf`ファイルに次の項目を追加します。

        spark.tispark.isolation_read_engines tiflash

-   Spark シェルまたは Thriftサーバーを初期化するときに、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`追加します。

-   Spark シェルで`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`リアルタイムで設定します。

-   サーバーがbeeline 経由で接続された後、Thriftサーバーに`set spark.tispark.isolation_read_engines=tiflash`設定します。
