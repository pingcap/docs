---
title: 使用状況の監視
summary: TiDB Cloud Lake は、プラットフォーム上でのあなたおよび組織メンバーの使用状況を包括的に把握できるようにする監視機能を提供します。Monitor ページにアクセスするには、ホームページのサイドバーメニューで Monitor をクリックします。このページには、以下のタブが含まれています。
---

# 使用状況の監視

{{{ .lake }}} は、プラットフォーム上でのあなたおよび組織メンバーの使用状況を包括的に把握できるようにする監視機能を提供します。**Monitor** ページにアクセスするには、ホームページのサイドバーメニューで **Monitor** をクリックします。このページには、以下のタブが含まれています。

- [Metrics](#metrics)
- [SQL History](#sql-history)
- [Task History](#task-history)
- [Audit](#audit): `account_admin` ユーザーのみに表示されます。

## Metrics {#metrics}

**Metrics** タブには、過去 1 時間、1 日、または 1 週間のデータを対象として、以下のメトリクスの使用統計を視覚的に示すチャートが表示されます。

- Storage Size
- SQL Query Count
- Session Connections
- Data Scanned / Written
- Warehouse Status
- Rows Scanned / Written

## SQL History {#sql-history}

**SQL History** タブには、組織内のすべてのユーザーによって実行された SQL ステートメントの一覧が表示されます。一覧の上部にある **Filter** をクリックすると、複数の条件でレコードを絞り込むことができます。

**SQL History** ページでレコードをクリックすると、{{{ .lake }}} がその SQL ステートメントをどのように実行したかに関する詳細情報が表示され、以下のタブにアクセスできます。

- **Query Details**: Query State（成功または失敗）、Rows Scanned、Warehouse、Bytes Scanned、Start Time、End Time、Handler Type が含まれます。
- **Query Profile**: SQL ステートメントがどのように実行されたかを示します。

## Task History {#task-history}

**Task History** タブでは、組織内で実行されたすべてのタスクの包括的なログが提供され、ユーザーはタスク設定を確認し、そのステータスを監視できます。

## Audit {#audit}

**Audit** タブには、操作タイプ、操作時刻、IP アドレス、操作を実行したアカウントを含む、組織メンバー全員の操作ログが記録されます。一覧の上部にある **Filter** をクリックすると、複数の条件でレコードを絞り込むことができます。