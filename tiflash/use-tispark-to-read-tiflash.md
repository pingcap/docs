---
title: Use TiSpark to Read TiFlash Replicas
summary: TiSpark を使用してTiFlashレプリカを読み取る方法を学習します。
---

# TiSparkを使用してTiFlashレプリカを読み取る {#use-tispark-to-read-tiflash-replicas}

このドキュメントでは、TiSpark を使用してTiFlashレプリカを読み取る方法について説明します。

現在、TiSpark を使用して、TiDB のエンジン分離と同様の方法でTiFlashレプリカを読み取ることができます。この方法は、 `spark.tispark.isolation_read_engines`パラメータを構成することです。パラメータ値のデフォルトは`tikv,tiflash`で、これは TiDB が CBO の選択に従ってTiFlashまたは TiKV からデータを読み取ることを意味します。パラメータ値を`tiflash`に設定すると、TiDB がTiFlashからデータを強制的に読み取ることを意味します。

> **注記：**
>
> このパラメータを`tiflash`に設定すると、クエリに関係するすべてのテーブルのTiFlashレプリカのみが読み取られ、これらのテーブルにはTiFlashレプリカが必要です。TiFlash レプリカがないテーブルの場合は、エラーが報告されます。このパラメータを`tikv`に設定すると、 TiFlashレプリカのみが読み取られます。

このパラメータは、次のいずれかの方法で設定できます。

-   `spark-defaults.conf`ファイルに次の項目を追加します。

        spark.tispark.isolation_read_engines tiflash

-   Spark シェルまたは Thriftサーバーを初期化するときに、初期化コマンドに`--conf spark.tispark.isolation_read_engines=tiflash`追加します。

-   Spark シェルで`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`リアルタイムで設定します。

-   サーバーがbeeline 経由で接続された後、Thriftサーバーに`set spark.tispark.isolation_read_engines=tiflash`設定します。
