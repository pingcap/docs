---
title: Changefeed
---

# チェンジフィード {#changefeed}

TiDB Cloudは、 TiDB Cloudからデータをストリーミングするのに役立つ次の変更フィードを提供します。

-   [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
-   [MySQL にシンク](/tidb-cloud/changefeed-sink-to-mysql.md)

TiDB Cloudでの変更フィードの課金については、 [変更フィードの請求](/tidb-cloud/tidb-cloud-billing-tcu.md)を参照してください。

> **ノート：**
>
> 変更フィードがある場合は[クラスターを一時停止します](/tidb-cloud/pause-or-resume-tidb-cluster.md)できません。クラスターを一時停止する前に、既存の変更フィード ( [Apache Kafka へのシンクの削除](/tidb-cloud/changefeed-sink-to-apache-kafka.md#manage-the-changefeed)または[MySQL へのシンクの削除](/tidb-cloud/changefeed-sink-to-mysql.md#delete-a-sink) ) を削除する必要があります。
