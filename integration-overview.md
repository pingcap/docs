---
title: Data Integration Overview
summary: Learn the overview of data integration scenarios.
---

# データ統合の概要 {#data-integration-overview}

データ統合とは、さまざまなデータ ソース間でのデータのフロー、転送、統合を意味します。データの量が急激に増加し、データの価値がより深く探求されるにつれて、データ統合の人気と緊急性がますます高まっています。 TiDB がデータ サイロになる状況を回避し、異なるプラットフォームとデータを統合するために、TiCDC は、TiDB 増分データ変更ログを他のデータ プラットフォームに複製する機能を提供します。このドキュメントでは、TiCDC を使用したデータ統合アプリケーションについて説明します。ビジネス シナリオに合った統合ソリューションを選択できます。

## Confluent Cloud および Snowflake との統合 {#integrate-with-confluent-cloud-and-snowflake}

TiCDC を使用して、増分データを TiDB から Confluent Cloud にレプリケートし、そのデータを Confluent Cloud 経由で Snowflake、ksqlDB、SQL Server にレプリケートできます。詳細は[Confluent Cloud および Snowflake との統合](/ticdc/integrate-confluent-using-ticdc.md)を参照してください。

## Apache Kafka および Apache Flink との統合 {#integrate-with-apache-kafka-and-apache-flink}

TiCDC を使用すると、増分データを TiDB から Apache Kafka にレプリケートし、Apache Flink を使用してデータを消費できます。詳細は[Apache Kafka および Apache Flink との統合](/replicate-data-to-kafka.md)を参照してください。
