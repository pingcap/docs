---
title: Data Integration Overview
summary: Learn the overview of data integration scenarios.
---

# データ統合の概要 {#data-integration-overview}

データ統合とは、さまざまなデータ ソース間でのデータの流れ、転送、および統合を意味します。データの量が指数関数的に増加し、データの価値がより深く探求されるにつれて、データ統合はますます一般的かつ緊急になっています。 TiDB がデータ サイロになる状況を回避し、データをさまざまなプラットフォームと統合するために、TiCDC は、TiDB の増分データ変更ログを他のデータ プラットフォームに複製する機能を提供します。このドキュメントでは、TiCDC を使用したデータ統合アプリケーションについて説明します。ビジネス シナリオに適した統合ソリューションを選択できます。

## Confluent Cloud および Snowflake との統合 {#integrate-with-confluent-cloud-and-snowflake}

TiCDC を使用して、TiDB から Confluent Cloud に増分データをレプリケートし、Confluent Cloud を介して Snowflake、ksqlDB、および SQL Server にデータをレプリケートできます。詳細については、 [Confluent Cloud および Snowflake との統合](/ticdc/integrate-confluent-using-ticdc.md)を参照してください。

## Apache Kafka および Apache Flink と統合する {#integrate-with-apache-kafka-and-apache-flink}

TiCDC を使用して、TiDB から Apache Kafka に増分データをレプリケートし、Apache Flink を使用してデータを消費できます。詳細については、 [Apache Kafka および Apache Flink と統合する](/replicate-data-to-kafka.md)を参照してください。
