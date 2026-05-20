---
title: Data Integration Overview
summary: データ統合シナリオの概要を学びましょう。
---

# データ統合の概要 {#data-integration-overview}

データ統合とは、さまざまなデータソース間でのデータの流れ、転送、および統合を意味します。データ量が指数関数的に増加し、データの価値がより深く探求されるにつれて、データ統合はますます普及し、緊急性を増しています。TiDBがデータサイロ化する状況を回避し、異なるプラットフォームとデータを統合するために、TiCDCはTiDBの増分データ変更ログを他のデータプラットフォームに複製する機能を提供します。このドキュメントでは、TiCDCを使用したデータ統合アプリケーションについて説明します。お客様のビジネスシナリオに適した統合ソリューションを選択できます。

## Confluent Cloud、Snowflake、ksqlDB、SQL Serverとの統合 {#integrate-with-confluent-cloud-snowflake-ksqldb-and-sql-server}

TiCDC を使用して、増分データを TiDB から Confluent Cloud にレプリケートし、そのデータを Confluent Cloud 経由で Snowflake、ksqlDB、SQL Server にレプリケートできます。詳細については、 [Confluent Cloud、Snowflake、ksqlDB、SQL Serverとデータを統合する](/ticdc/integrate-confluent-using-ticdc.md)参照してください。

## Apache KafkaおよびApache Flinkとの統合 {#integrate-with-apache-kafka-and-apache-flink}

TiCDC を使用すると、増分データを TiDB から Apache Kafka にレプリケートし、Apache Flink を使用してデータを消費できます。詳細については、 [Apache KafkaおよびApache Flinkとの統合](/replicate-data-to-kafka.md)を参照してください。

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="How to Replicate TiDB to a Mirrored Database in Microsoft Fabric with TiCDC" type="blog" link="https://www.pingcap.com/blog/replicate-tidb-mirrored-database-microsoft-fabric-ticdc/" imgSrc="https://static.pingcap.com/files/2025/10/27043308/20251027-170247.png" author="Guanglei Bao, Jasper Hu, Brian Foster" date="2025-10-27" />
</RelatedResources>
