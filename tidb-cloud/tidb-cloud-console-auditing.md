---
title: Console Audit Logging
summary: Learn about the log auditing feature for the TiDB Cloud console.
---

# コンソール監査ログ {#console-audit-logging}

TiDB Cloudは、 TiDB Cloudコンソール操作の監査ログ機能を提供します。これは、ユーザー アクセスの詳細 (コンソールへのユーザー ログインやクラスター作成操作など) の履歴を記録します。

> **ノート：**
>
> 現在、**監査ログ**機能は実験的です。出力は変更される場合があります。

## 制限事項 {#limitations}

現在、コンソール監査ログ機能には次の制限があります。

-   コンソール監査ログはデフォルトで有効になっており、ユーザーが無効にすることはできません。
-   機能の監査フィルター規則を指定することはできません。
-   監査ログにアクセスするには、PingCAP サポートが必要です。

## 監査イベントの種類 {#audit-event-types}

TiDB Cloudコンソールでのすべてのユーザー操作は、イベントとして監査ログに記録されます。監査ログは、次のイベント タイプを対象としています。

| 監査イベントの種類                            | 説明                                |
| ------------------------------------ | --------------------------------- |
| AuditEventSignIn                     | サインイン                             |
| AuditEventSignOut                    | サインアウト                            |
| AuditEventUpdateUserProfile          | ユーザーの姓名を更新する                      |
| AuditEventUpdateMFA                  | MFA を有効または無効にする                   |
| AuditEventCreateProject              | 新しいプロジェクトを作成する                    |
| AuditEventUpdateProject              | プロジェクト名を更新する                      |
| AuditEventDeleteProject              | プロジェクトを削除する                       |
| AuditEventInviteUserIntoProject      | ユーザーをプロジェクトに招待する                  |
| AuditEventDeleteProjectUser          | プロジェクト ユーザーを削除する                  |
| AuditEventUpdateOrg                  | 組織名とタイムゾーンを更新する                   |
| AuditEventCreateIntegration          | 統合を作成する                           |
| 監査イベント削除統合                           | 統合を削除する                           |
| AuditEventListOrgUsers               | 組織内のユーザーを一覧表示する                   |
| AuditEventListProjectUsers           | プロジェクト内のユーザーを一覧表示する               |
| AuditEventAddNewPaymentMethod        | 新しいクレジット カードを追加する                 |
| AuditEventUpdatePaymentMethod        | クレジットカード情報の更新                     |
| AuditEventDeletePaymentMethod        | クレジット カードを削除する                    |
| AuditEventCreateAWSVpcPeering        | AWS VPC ピアリングを作成する                |
| AuditEventCreateGCPVpcPeering        | GCP VPC ピアリングを作成する                |
| AuditEventListAWSVpcPeering          | プロジェクト内のすべての AWS VPC ピアリングを一覧表示する |
| AuditEventListGCPVpcPeering          | プロジェクト内のすべての GCP VPC ピアリングを一覧表示する |
| AuditEventDeleteAWSVpcPeering        | AWS VPC ピアリングを削除する                |
| AuditEventDeleteGCPVpcPeering        | GCP VPC ピアリングを削除する                |
| AuditEventGetProjectTrafficFilter    | プロジェクトのトラフィック フィルター リストを取得する      |
| AuditEventUpdateProjectTrafficFilter | プロジェクトのトラフィック フィルタ リストを更新する       |
| AuditEventGetTrafficFilter           | クラスタのトラフィック フィルタ リストを取得する         |
| AuditEventUpdateTrafficFilter        | クラスタのトラフィック フィルタ リストを更新する         |
| AuditEventCreateProjectCIDR          | 新しいプロジェクト CIDR を作成する              |
| AuditEventGetProjectCIDR             | リージョンの CIDR を一覧表示する               |
| AuditEventGetProjectRegionCIDR       | プロジェクト内のすべての CIDR を一覧表示する         |
| AuditEventDeleteBackupInRecycleBin   | ごみ箱にある削除済みクラスターのバックアップを削除する       |
| AuditEventChangeClusterRootPassword  | クラスターのルート パスワードをリセットする            |
| AuditEventCreateImportTask           | インポート タスクを作成する                    |
| AuditEventCancleImportTask           | インポート タスクをキャンセルする                 |
| AuditEventExitImportTask             | インポート タスクを終了する                    |
| AuditEventCreateCluster              | クラスターを作成する                        |
| AuditEventDeleteCluster              | クラスターを削除する                        |
| AuditEventScaleCluster               | クラスターをスケーリングする                    |
| AuditEventCreateBackup               | バックアップを作成する                       |
| AuditEventDeleteBackup               | バックアップを削除する                       |
| AuditEventRestoreBackup              | バックアップからの復元                       |
| AuditEventUpdateAuditLogStatus       | データベース監査ログを有効または無効にする             |
| AuditEventCreateAuditLogAccessRecord | データベース監査ログのフィルター条件を追加する           |
| AuditEventDeleteAuditLogAccessRecord | データベース監査ログのフィルター条件を削除する           |
| AuditEventUpdateUserRole             | ユーザーの役割を変更する                      |

## 監査ログ ストレージ ポリシー {#audit-log-storage-policy}

-   監査ログ情報は AWS ES に保存されます。
-   保管期間は 90 日で、その後監査ログは自動的にクリーンアップされます。

## 監査ログをビューする {#view-audit-logs}

コンソールの監査ログは、 TiDB Cloudの内部担当者のみが一時的にアクセスできます。ログを表示する必要がある場合は、 [PingCAP サポート チーム](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## 監査ログ フィールド {#audit-log-fields}

監査ログのフィールドには、基本フィールドと拡張フィールドが含まれます。

基本的なフィールドは次のとおりです。

| フィールド名         | データ・タイプ | 説明        |
| -------------- | ------- | --------- |
| タイムスタンプ        | タイムスタンプ | 開催時間      |
| auditEventType | ストリング   | イベントタイプ   |
| ユーザーID         | uint64  | ユーザーID    |
| クライアントIP       | ストリング   | クライアント IP |
| は成功            | ブール     | イベント結果    |

拡張フィールドは、さまざまなイベント タイプに基づいてイベントの説明情報を補足し、監査情報の整合性と可用性を確保します。

> **ノート：**
>
> 基本フィールドでイベントを明確に説明できないシナリオについては、次の表に、これらのイベント タイプの拡張フィールド情報を示します。表にないイベントには拡張フィールドがありません。

| 監査イベントの種類                       | 拡張フィールド                  | 拡張フィールドのデータ型    | 拡張フィールドの説明                                            |
| ------------------------------- | ------------------------ | --------------- | ----------------------------------------------------- |
| AuditEventUpdateMFA             | enableMFA                | ブール             | MFA を有効または無効にする                                       |
| AuditEventCreateProject         | プロジェクト名                  | ストリング           | プロジェクト名                                               |
| AuditEventUpdateProject         | 古いプロジェクト名<br/>新しいプロジェクト名 | ストリング<br/>ストリング | 旧プロジェクト名<br/>新しいプロジェクト名                               |
| AuditEventDeleteProject         | プロジェクト名                  | ストリング           | プロジェクト名                                               |
| AuditEventInviteUserIntoProject | Eメール<br/>役割              | ストリング<br/>ストリング | Eメール<br/>ロール名                                         |
| AuditEventDeleteProjectUser     | Eメール<br/>役割              | ストリング<br/>ストリング | Eメール<br/>ロール名                                         |
| AuditEventUpdateOrg             | 組織名<br/>タイムゾーン           | ストリング<br/>ユニット  | 組織名<br/>タイムゾーン                                        |
| AuditEventCreateIntegration     | 統合タイプ                    | ストリング           | 統合タイプ                                                 |
| 監査イベント削除統合                      | 統合タイプ                    | ストリング           | 統合タイプ                                                 |
| AuditEventAddNewPaymentMethod   | カード番号                    | ストリング           | 支払いカード番号 (情報が鈍感化されています)                               |
| AuditEventUpdatePaymentMethod   | カード番号                    | ストリング           | 支払いカード番号 (情報が鈍感化されています)<br/> (現在、完全なフィールド情報を取得していません) |
| AuditEventDeletePaymentMethod   |                          |                 | (現在、完全なフィールド情報を取得していません)                              |
| AuditEventCreateCluster         | クラスタ名                    | ストリング           | クラスタ名                                                 |
| AuditEventDeleteCluster         | クラスター名                   | ストリング           | クラスタ名                                                 |
| AuditEventCreateBackup          | バックアップ名                  | ストリング           | バックアップ名                                               |
| AuditEventRestoreBackup         | クラスター名                   | ストリング           | クラスタ名                                                 |
| AuditEventUpdateAuditLogStatus  | enableAuditLog           | ブール             | データベース監査ログを有効または無効にする                                 |
| AuditEventUpdateUserRole        | 古い役割<br/>新しい役割           | ストリング<br/>ストリング | 旧ロール名<br/>新しいロール名                                     |
