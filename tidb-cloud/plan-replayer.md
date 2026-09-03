---
title: Plan Replayer を使用して SQL パフォーマンスをトラブルシュートする
summary: SQL パフォーマンスのトラブルシューティングのために、インスタンスから Plan Replayer ファイルを生成する方法と、TiDB Cloudサポートに対して限られた期間そのファイルへのアクセスを許可する方法を学びます。
---

# Plan Replayer を使用して SQL パフォーマンスをトラブルシュートする

Plan Replayer は、SQL 実行プランの調査に必要な情報をファイルにまとめるのに役立ちます。このファイルには、TiDB のバージョンと設定、セッション変数、SQL バインディング、テーブルスキーマ、テーブル統計情報、`EXPLAIN` または `EXPLAIN ANALYZE` の出力、およびオプティマイザーの内部情報を含めることができます。

TiDB Cloud Essential または Premium インスタンスで SQL パフォーマンスの問題をトラブルシュートする場合は、`PLAN REPLAYER DUMP` を使用して特定の SQL 文に対する Plan Replayer ファイルを生成し、返された URL からそのファイルをダウンロードできます。Plan Replayer ファイルは、予期しない実行プラン、プランのリグレッション、不正確な統計情報、またはたまにしか発生しない問題のあるプランなどの問題を調査するのに役立ちます。

SQL パフォーマンスの問題のトラブルシューティングで TiDB Cloudサポートの支援が必要な場合は、限られた期間、TiDB Cloudサポートが Plan Replayer ファイルにアクセスできるよう一時的に許可できます。

> **Note:**
>
> Plan Replayer ファイルには実際のテーブル行データは含まれませんが、SQL テキスト、テーブル定義、オプティマイザー統計情報、およびその他の機密性がある可能性のある情報が含まれる場合があります。サポートへのアクセスを許可する前に、ファイルの内容と組織のデータ共有要件を確認してください。

## 開始前に {#before-you-start}

- SQL クライアントを使用して、対象の TiDB Cloud Essential または Premium インスタンスに接続します。
- 必要な SQL 文を実行する権限を持つアカウントを使用します。
- 調査したい SQL 文、SQL digest、または plan digest を特定します。
- 可能であれば、SQL テキスト内の機密リテラルを削除またはマスクします。Plan Replayer にはテーブル行は含まれませんが、SQL テキストやスキーマ名に機密情報が含まれている可能性があります。

## Plan Replayer ファイルを生成する {#generate-a-plan-replayer-file}

このセクションでは、特定の SQL 文に対する Plan Replayer ファイルを生成する方法について説明します。

### 文に対するファイルを生成する {#generate-a-file-for-a-statement}

調査したい文を指定して `PLAN REPLAYER DUMP` を実行します。オプティマイザーが見積もった実行プランを取得するには `EXPLAIN` を使用します。

```sql
PLAN REPLAYER DUMP EXPLAIN
SELECT * FROM orders WHERE customer_id = 1001;
```

この文は、`File_token` カラムにダウンロード URL を返します。この URL は一時的なものです。安全に保存し、有効期限が切れる前に Plan Replayer の ZIP ファイルをダウンロードしてください。

### 実行時情報を含める {#include-runtime-information}

パフォーマンスの問題が実際の実行動作に関係している場合は、`EXPLAIN ANALYZE` を使用して、実行プランに加えて実行時の実行情報も含めます。

```sql
PLAN REPLAYER DUMP EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 1001;
```

### 履歴統計情報を使用する {#use-historical-statistics}

履歴統計情報が有効になっており、パフォーマンスの問題が特定の時刻に発生した場合は、`WITH STATS AS OF TIMESTAMP` を使用して、その時点で利用可能だった統計情報を要求します。TiDB は、指定したタイムスタンプより前に利用可能な最新の履歴統計情報を使用します。

```sql
PLAN REPLAYER DUMP WITH STATS AS OF TIMESTAMP
'2026-08-31 12:00:00'
EXPLAIN SELECT * FROM orders WHERE customer_id = 1001;
```

調査に必要な場合は、Unix タイムスタンプを指定することもできます。指定した時刻より前に利用可能な履歴統計情報がない場合、TiDB は利用可能な最新の統計情報を使用し、関連するエラー情報をパッケージに記録します。

## TiDB Cloudサポートからのアクセスを管理する {#manage-access-from-tidb-cloud-support}

サポートアクセスはインスタンスレベルで制御されます。この許可により、TiDB Cloudサポートのエンジニアは、限られた期間中、SQL パフォーマンスのトラブルシューティングのために生成された Plan Replayer ファイルにアクセスできます。

### TiDB Cloudサポートを許可する {#authorize-tidb-cloud-support}

SQL パフォーマンスのトラブルシューティングのために生成された Plan Replayer ファイルへ TiDB Cloudサポートが一時的にアクセスできるよう許可するには、次の手順を実行します。

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で、対象の TiDB Cloud Essential または Premium インスタンスの概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Security** をクリックします。
3. **Security** ページの **SQL Plan Replayer Files Access Authorization** セクションで、**Authorize** をクリックします。
4. ドロップダウンリストから、想定されるトラブルシューティング期間をカバーするアクセス期間を選択します。
5. 許可に関する記述を確認し、確認用チェックボックスを選択します。
6. **Authorize** をクリックして一時アクセスを許可します。

アクセスはすぐに開始され、選択した有効期限に達すると自動的に取り消されます。

### 許可期間を延長する {#extend-the-authorization-period}

許可期間の期限が近づいており、問題の調査がまだ続いている場合は、対象の TiDB Cloud Essential または Premium インスタンスの **Security** ページに移動し、**Extend Access** をクリックして有効期限を更新します。

更新を確認すると、新しい有効期限が有効になります。

### アクセスを取り消す {#revoke-access}

トラブルシューティングが完了したとき、または TiDB Cloudサポートに Plan Replayer ファイルへのアクセスを許可したくなくなったときは、対象の TiDB Cloud Essential または Premium インスタンスの **Security** ページに移動し、**Revoke Access** をクリックして操作を確認します。

取り消しは即時に有効になります。診断アクセスフローに関連するファイルは、製品の保持ポリシーに従って削除される場合もあります。

## ベストプラクティス {#best-practices}

機密情報の保護、不必要なアクセスの最小化、およびサポート効率の向上のために、次のベストプラクティスに従ってください。

- 調査時点にできるだけ近いタイミングで Plan Replayer ファイルを生成します。
- TiDB Cloudサポートへの許可期間は、実務上可能な限り短くします。
- 関連するサポートチケットに Plan Replayer ファイル識別子を含めます。
- 問題が解決したらアクセスを取り消します。

## セキュリティと保持 {#security-and-retention}

Plan Replayer は、実際のテーブル行をエクスポートせずに、オプティマイザーおよび実行プランのコンテキストを共有できるよう設計されています。ただし、SQL テキスト、オブジェクト名、テーブル定義、設定、バインディング、および統計情報には、業務上機密性の高い情報が含まれる可能性があります。Plan Replayer ファイルを TiDB Cloudサポートと共有する必要がある場合は、必要最小限のアクセス期間を使用し、調査後にアクセスを取り消してください。

Plan Replayer ファイルは一時的な診断用アーティファクトです。TiDB は、保持期間の経過後に生成済みファイルを自動的に削除する場合があります。以前のファイルの有効期限が切れた、または利用できなくなった場合は、新しいファイルを生成してください。

## 関連ドキュメント {#related-documentation}

[TiDB: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster](https://docs.pingcap.com/tidb/stable/sql-plan-replayer/)