---
title: Console Audit Logging
summary: Learn about the log auditing feature for the TiDB Cloud Console.
---

# コンソール監査ログ {#console-audit-logging}

TiDB Cloudは、 TiDB Cloudコンソール操作の監査ログ機能を提供します。これは、ユーザーアクセスの詳細（コンソールへのユーザーログインやクラスタ作成操作など）の履歴を記録します。

> **ノート：**
>
> 現在、**監査ログ**機能は実験的です。出力は変更される場合があります。

## 制限事項 {#limitations}

現在、コンソール監査ログ機能には次の制限があります。

-   コンソール監査ログはデフォルトで有効になっており、ユーザーが無効にすることはできません。
-   機能の監査フィルタリングルールを指定することはできません。
-   監査ログにアクセスするには、PingCAPサポートを使用する必要があります。

## イベントタイプの監査 {#audit-event-types}

TiDB Cloud Consoleでのすべてのユーザー操作は、イベントとして監査ログに記録されます。監査ログには、次のイベントタイプが含まれます。

| 監査イベントタイプ                            | 説明                              |
| ------------------------------------ | ------------------------------- |
| AuditEventSignIn                     | ログイン                            |
| AuditEventSignOut                    | サインアウト                          |
| AuditEventUpdateUserProfile          | ユーザーの名前と名前を更新する                 |
| AuditEventUpdateMFA                  | MFAを有効または無効にする                  |
| AuditEventCreateProject              | 新しいプロジェクトを作成する                  |
| AuditEventUpdateProject              | プロジェクト名を更新します                   |
| AuditEventDeleteProject              | プロジェクトを削除する                     |
| AuditEventInviteUserIntoProject      | ユーザーをプロジェクトに招待する                |
| AuditEventDeleteProjectUser          | プロジェクトユーザーを削除します                |
| AuditEventUpdateOrg                  | 組織名とタイムゾーンを更新します                |
| AuditEventCreateIntegration          | 統合を作成する                         |
| AuditEventDeleteIntegration          | 統合を削除する                         |
| AuditEventListOrgUsers               | 組織内のユーザーを一覧表示する                 |
| AuditEventListProjectUsers           | プロジェクトのユーザーを一覧表示する              |
| AuditEventAddNewPaymentMethod        | 新しいクレジットカードを追加します               |
| AuditEventUpdatePaymentMethod        | クレジットカード情報を更新する                 |
| AuditEventDeletePaymentMethod        | クレジットカードを削除する                   |
| AuditEventCreateAWSVpcPeering        | AWSVPCピアリングを作成する                |
| AuditEventCreateGCPVpcPeering        | GCPVPCピアリングを作成する                |
| AuditEventListAWSVpcPeering          | プロジェクト内のすべてのAWSVPCピアリングを一覧表示します |
| AuditEventListGCPVpcPeering          | プロジェクト内のすべてのGCPVPCピアリングを一覧表示します |
| AuditEventDeleteAWSVpcPeering        | AWSVPCピアリングを削除します               |
| AuditEventDeleteGCPVpcPeering        | GCPVPCピアリングを削除する                |
| AuditEventGetProjectTrafficFilter    | プロジェクトのトラフィックフィルターリストを取得する      |
| AuditEventUpdateProjectTrafficFilter | プロジェクトのトラフィックフィルターリストを更新する      |
| AuditEventGetTrafficFilter           | クラスタのトラフィックフィルターリストを取得する        |
| AuditEventUpdateTrafficFilter        | クラスタのトラフィックフィルターリストを更新する        |
| AuditEventCreateProjectCIDR          | 新しいプロジェクトCIDRを作成する              |
| AuditEventGetProjectCIDR             | リージョンのCIDRを一覧表示します              |
| AuditEventGetProjectRegionCIDR       | プロジェクト内のすべてのCIDRを一覧表示します        |
| AuditEventDeleteBackupInRecycleBin   | ごみ箱内の削除されたクラスターのバックアップを削除する     |
| AuditEventChangeClusterRootPassword  | クラスタのルートパスワードをリセットする            |
| AuditEventCreateImportTask           | インポートタスクを作成する                   |
| AuditEventCancleImportTask           | インポートタスクをキャンセルする                |
| AuditEventExitImportTask             | インポートタスクを終了します                  |
| AuditEventCreateCluster              | クラスタを作成する                       |
| AuditEventDeleteCluster              | クラスタを削除する                       |
| AuditEventScaleCluster               | クラスタをスケーリングする                   |
| AuditEventCreateBackup               | バックアップを作成する                     |
| AuditEventDeleteBackup               | バックアップを削除する                     |
| AuditEventRestoreBackup              | バックアップから復元する                    |
| AuditEventUpdateAuditLogStatus       | データベース監査ログを有効または無効にします          |
| AuditEventCreateAuditLogAccessRecord | データベース監査ログフィルター条件を追加します         |
| AuditEventDeleteAuditLogAccessRecord | データベース監査ログフィルター条件を削除します         |
| AuditEventUpdateUserRole             | ユーザーの役割を変更する                    |

## 監査ログストレージポリシー {#audit-log-storage-policy}

-   監査ログ情報はAWSESに保存されます。
-   保存期間は90日で、その後、監査ログは自動的にクリーンアップされます。

## 監査ログをビューする {#view-audit-logs}

コンソール監査ログは、 TiDB Cloudの内部担当者のみが一時的にアクセスできます。ログを表示する必要がある場合は、 [PingCAPサポートチーム](/tidb-cloud/tidb-cloud-support.md)に連絡してください。

## 監査ログフィールド {#audit-log-fields}

監査ログのフィールドには、基本フィールドと拡張フィールドが含まれます。

基本的なフィールドは次のとおりです。

| フィールド名         | データ・タイプ | 説明       |
| -------------- | ------- | -------- |
| タイムスタンプ        | タイムスタンプ | イベントの時間  |
| auditEventType | ストリング   | イベントタイプ  |
| ユーザーID         | uint64  | ユーザーID   |
| clientIP       | ストリング   | クライアントIP |
| isSuccess      | ブール     | イベント結果   |

拡張フィールドは、監査情報の整合性と可用性を確保するために、さまざまなイベントタイプに基づいてイベントの説明情報を補足します

> **ノート：**
>
> 基本フィールドでイベントを明確に説明できないシナリオの場合、次の表に、これらのイベントタイプの拡張フィールド情報を示します。表にないイベントには拡張フィールドがありません。

| 監査イベントタイプ                       | 拡張フィールド                            | 拡張フィールドのデータ型    | 拡張フィールドの説明                                         |
| ------------------------------- | ---------------------------------- | --------------- | -------------------------------------------------- |
| AuditEventUpdateMFA             | enableMFA                          | ブール             | MFAを有効または無効にする                                     |
| AuditEventCreateProject         | projectName                        | ストリング           | プロジェクト名                                            |
| AuditEventUpdateProject         | oldProjectName<br/> newProjectName | ストリング<br/>ストリング | 古いプロジェクト名<br/>新しいプロジェクト名                           |
| AuditEventDeleteProject         | projectName                        | ストリング           | プロジェクト名                                            |
| AuditEventInviteUserIntoProject | Eメール<br/>役割                        | ストリング<br/>ストリング | Eメール<br/>役割名                                       |
| AuditEventDeleteProjectUser     | Eメール<br/>役割                        | ストリング<br/>ストリング | Eメール<br/>役割名                                       |
| AuditEventUpdateOrg             | orgName<br/> timeZone              | ストリング<br/>uint  | 組織名<br/>タイムゾーン                                     |
| AuditEventCreateIntegration     | IntegrationType                    | ストリング           | 統合タイプ                                              |
| AuditEventDeleteIntegration     | IntegrationType                    | ストリング           | 統合タイプ                                              |
| AuditEventAddNewPaymentMethod   | カード番号                              | ストリング           | ペイメントカード番号（情報の感度が低下）                               |
| AuditEventUpdatePaymentMethod   | カード番号                              | ストリング           | ペイメントカード番号（情報の感度が低下）<br/> （現在、完全なフィールド情報を取得していません） |
| AuditEventDeletePaymentMethod   |                                    |                 | （現在、完全なフィールド情報を取得していません）                           |
| AuditEventCreateCluster         | clusterName                        | ストリング           | クラスター名                                             |
| AuditEventDeleteCluster         | clusterName                        | ストリング           | クラスター名                                             |
| AuditEventCreateBackup          | backupName                         | ストリング           | バックアップ名                                            |
| AuditEventRestoreBackup         | clusterName                        | ストリング           | クラスター名                                             |
| AuditEventUpdateAuditLogStatus  | enableAuditLog                     | ブール             | データベース監査ログを有効または無効にします                             |
| AuditEventUpdateUserRole        | oldRole<br/> newRole               | ストリング<br/>ストリング | 古い役割名<br/>新しい役割名                                   |
