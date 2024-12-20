---
title: Data Integration Overview
summary: データ統合シナリオの概要を学習します。
---

# データ統合の概要 {#data-integration-overview}

データ統合とは、さまざまなデータ ソース間でのデータのフロー、転送、統合を意味します。データの量が飛躍的に増加し、データの価値がより深く探求されるにつれて、データ統合はますます普及し、緊急性が増しています。TiDB がデータ サイロになる状況を回避し、さまざまなプラットフォームとデータを統合するために、TiCDC は TiDB の増分データ変更ログを他のデータ プラットフォームに複製する機能を提供します。このドキュメントでは、TiCDC を使用したデータ統合アプリケーションについて説明します。ビジネス シナリオに適した統合ソリューションを選択できます。

## Confluent CloudとSnowflakeとの統合 {#integrate-with-confluent-cloud-and-snowflake}

TiCDC を使用すると、TiDB から Confluent Cloud に増分データを複製し、Confluent Cloud 経由で Snowflake、ksqlDB、SQL Server にデータを複製できます。詳細については、 [Confluent CloudとSnowflakeとの統合](/ticdc/integrate-confluent-using-ticdc.md)参照してください。

## Apache Kafka および Apache Flink との統合 {#integrate-with-apache-kafka-and-apache-flink}

TiCDC を使用すると、TiDB から Apache Kafka に増分データを複製し、Apache Flink を使用してデータを使用することができます。詳細については、 [Apache Kafka および Apache Flink との統合](/replicate-data-to-kafka.md)参照してください。
