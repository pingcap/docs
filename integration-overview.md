---
title: Data Integration Overview
summary: データ統合シナリオの概要を学習します。
---

# データ統合の概要 {#data-integration-overview}

データ統合とは、様々なデータソース間でのデータのフロー、転送、統合を意味します。データ量が指数関数的に増加し、データの価値がより深く探求されるにつれて、データ統合はますます普及し、緊急の課題となっています。TiDBがデータサイロ化する状況を回避し、異なるプラットフォーム間でデータを統合するために、TiCDCはTiDBの増分データ変更ログを他のデータプラットフォームに複製する機能を提供します。このドキュメントでは、TiCDCを使用したデータ統合アプリケーションについて説明します。ビジネスシナリオに最適な統合ソリューションをお選びいただけます。

## Confluent CloudとSnowflakeとの統合 {#integrate-with-confluent-cloud-and-snowflake}

TiCDCを使用すると、TiDBからConfluent Cloudに増分データを複製し、Confluent Cloud経由でSnowflake、ksqlDB、SQL Serverにデータを複製できます。詳細については、 [Confluent CloudとSnowflakeとの統合](/ticdc/integrate-confluent-using-ticdc.md)ご覧ください。

## Apache Kafka および Apache Flink との統合 {#integrate-with-apache-kafka-and-apache-flink}

TiCDCを使用すると、TiDBからApache Kafkaに増分データを複製し、Apache Flinkを使用してデータを利用できます。詳細については、 [Apache Kafka および Apache Flink との統合](/replicate-data-to-kafka.md)参照してください。
