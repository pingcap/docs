---
title: Console Audit Logging
summary: TiDB Cloudコンソールの監査ログ機能について学習します。
---

# コンソール監査ログ {#console-audit-logging}

TiDB Cloudは、 [TiDB Cloudコンソール](https://tidbcloud.com)上のユーザーのさまざまな行動や操作を追跡するのに役立つコンソール監査ログ機能を提供します。例えば、ユーザーを組織に招待したり、クラスターを作成したりするなどの操作を追跡できます。

## 前提条件 {#prerequisites}

- TiDB Cloudにおいて、組織の`Organization Owner`または`Organization Console Audit Manager`ロールに所属している必要があります。そうでない場合、 TiDB Cloudコンソールでコンソール監査ログ関連のオプションを表示できません。

## コンソール監査ログを有効にする {#enable-console-audit-logging}

コンソール監査ログ機能はデフォルトで無効になっています。有効にすると、TiDB Cloudコンソールでサポートされているすべてのイベントタイプが監査され、特定のイベントタイプのみを監査するように設定することはできません。有効にするには、以下の手順を実行してください。

1. [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボボックスを使用して対象の組織に切り替えます。
2. 左側のナビゲーションペインで、 **Console Audit Logging**をクリックします。
3. 右上隅の**Settings**をクリックし、コンソール監査ログを有効にして、 **Update**をクリックします。

## コンソール監査ログを無効にする {#disable-console-audit-logging}

コンソール監査ログを無効にするには、次の手順を実行します。

1. [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボボックスを使用して対象の組織に切り替えます。
2. 左側のナビゲーションペインで、 **Console Audit Logging**をクリックします。
3. 右上隅の**Settings**をクリックし、コンソール監査ログを無効にして、 **Update**をクリックします。

## コンソール監査ログを確認する {#view-console-audit-logs}

組織のコンソール監査ログのみを表示できます。

> **Note:**
>
> - 組織でコンソール監査ログを初めて有効にする場合、コンソール監査ログは空です。監査対象イベントが実行されると、対応するログが表示されます。
> - コンソール監査ログが無効になってから 90日以上経過した場合、ログは表示されません。

1. [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボボックスを使用して対象の組織に切り替えます。
2. 左側のナビゲーションペインで、 **Console Audit Logging**をクリックします。
3. 監査ログの特定の部分を取得するには、イベントの種類、操作ステータス、および時間範囲をフィルタリングできます。
4. (オプション) さらにフィールドをフィルターするには、 **Advanced filter**をクリックし、さらにフィルターを追加して、 **Apply**をクリックします。
5. ログの行をクリックすると、右側のペインに詳細情報が表示されます。

## コンソール監査ログをエクスポートする {#export-console-audit-logs}

組織のコンソール監査ログをエクスポートするには、次の手順を実行します。

1. [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボボックスを使用して対象の組織に切り替えます。
2. 左側のナビゲーションペインで、 **Console Audit Logging**をクリックします。
3. （オプション）コンソール監査ログの特定の部分をエクスポートする必要がある場合は、さまざまな条件でフィルタリングできます。それ以外の場合は、この手順をスキップしてください。
4. **Download logs**をクリックし、JSON または CSV で希望のエクスポート形式を選択します。

## コンソール監査ログストレージポリシー {#console-audit-log-storage-policy}

コンソール監査ログのストレージ期間は 90日間で、その後はログは自動的にクリーンアップされます。

> **Note:**
>
> - TiDB Cloudではコンソール監査ログのストレージの場所を指定できません。
> - 監査ログを手動で削除することはできません。

## コンソール監査ログの完全性とアクセス制御 {#console-audit-log-integrity-and-access-control}

規制コンプライアンス要件への対応を支援するために、TiDB Cloud はコンソール監査ログについて次の制御を提供します。

- **Completeness**: 組織でコンソール監査ログが有効になっている場合、監査システムは[サポートされているイベントタイプ](#console-audit-event-types)をトリガーするユーザー操作を記録します。ログエントリは通常、イベント発生から 60分以内に、表示、ダウンロード、および API を介したプログラムによるアクセスが可能になります。

    > **Note:**
    >
    > コンソール監査ログは、有効化された後に発生したサポート対象のすべてのイベントを記録します。監査ログを有効にする前に実行された操作は記録されません。TiDB Cloud は、監査対象イベントタイプのカバレッジを継続的に拡大しています。

- **Access control**: 組織の`Organization Owner`または`Organization Console Audit Manager`ロールを持つユーザーのみが、その組織のコンソール監査ログを管理できます。他の組織メンバーは、監査ログの有効化または無効化、あるいはログ設定の変更を行うことはできません。

## コンソール監査イベントの種類 {#console-audit-event-types}

コンソール監査ログには、イベントタイプを通じてTiDB Cloudコンソール上のさまざまなユーザー アクティビティが記録されます。

> **Note:**
>
> 現在、 TiDB Cloudコンソール上のほとんどのイベントタイプが監査対象となっており、以下の表で確認できます。まだ対応していない残りのイベントタイプについても、 TiDB Cloud は引き続き対応に向けて取り組んでいきます。

| コンソール監査イベントタイプ         | 説明                                                                   |
| ---------------------- | -------------------------------------------------------------------- |
| CreateOrganization | 組織を作成する                                                              |
| LoginOrganization | 組織にログインする                                                            |
| SwitchOrganization | 現在の組織から別の組織に切り替える                                                    |
| LogoutOrganization | 組織からログアウトする                                                          |
| InviteUserToOrganization | ユーザーを組織に招待する                                                         |
| DeleteInvitationToOrganization | 組織への参加を希望するユーザーの招待を削除する                                              |
| ResendInvitationToOrganization | 組織に参加するためのユーザーへの招待状を再送信する                                            |
| ConfirmJoinOrganization | 招待されたユーザーが組織への参加を確認する                                                |
| DeleteUserFromOrganization | 組織に参加しているユーザーを削除する                                                   |
| UpdateUserRoleInOrganization | 組織内のユーザーの役割を更新する                                                     |
| CreateAPIKey | APIキーを作成する                                                           |
| EditAPIKey | APIキーを編集する                                                           |
| DeleteAPIKey | APIキーを削除する                                                           |
| UpdateTimezone | 組織のタイムゾーンを更新する                                                       |
| ShowBill | 組織の請求書を表示                                                            |
| DownloadBill | 組織法案をダウンロード                                                          |
| ShowCredits | 組織のクレジットを表示                                                          |
| AddPaymentCard | 支払いカードを追加する                                                          |
| UpdatePaymentCard | 支払いカードを更新する                                                          |
| DeletePaymentCard | 支払いカードを削除する                                                          |
| SetDefaultPaymentCard | デフォルトの支払いカードを設定する                                                    |
| EditBillingProfile | 請求プロファイル情報を編集する                                                      |
| ContractAction | 契約関連活動を整理する                                                          |
| EnableConsoleAuditLog | コンソール監査ログを有効にする                                                      |
| ShowConsoleAuditLog | コンソール監査ログを表示する                                                       |
| InviteUserToProject | ユーザーをプロジェクトに招待する                                                     |
| DeleteInvitationToProject | プロジェクトへのユーザーの招待を削除する                                                 |
| ResendInvitationToProject | ユーザーにプロジェクトへの参加を依頼する招待状を再送信する                                        |
| ConfirmJoinProject | 招待されたユーザーがプロジェクトへの参加を確認する                                            |
| DeleteUserFromProject | プロジェクトに参加しているユーザーを削除する                                               |
| CreateProject | プロジェクトを作成する                                                          |
| CreateProjectCIDR | 新しいプロジェクトCIDRを作成する                                                   |
| CreateAWSVPCPeering | AWS VPCピアリングを作成する                                                    |
| DeleteAWSVPCPeering | AWS VPCピアリングを削除する                                                    |
| CreateGCPVPCPeering | Google Cloud VPC ピアリングを作成する                                          |
| DeleteGCPVPCPeering | Google Cloud VPC ピアリングを削除する                                          |
| CreatePrivateEndpointService | プライベートエンドポイントサービスを作成する                                               |
| DeletePrivateEndpointService | プライベートエンドポイントサービスを削除する                                               |
| CreateAWSPrivateEndPoint | AWSプライベートエンドポイントを作成する                                                |
| DeleteAWSPrivateEndPoint | AWSプライベートエンドポイントを削除する                                                |
| SubscribeAlerts | アラートを購読する                                                            |
| UnsubscribeAlerts | アラートの購読解除                                                            |
| CreateDatadogIntegration | Datadog統合を作成する                                                       |
| DeleteDatadogIntegration | Datadog統合を削除する                                                       |
| CreateVercelIntegration | vercel統合を作成する                                                        |
| DeleteVercelIntegration | vercel統合を削除                                                          |
| CreatePrometheusIntegration | Prometheus統合を作成する                                                    |
| DeletePrometheusIntegration | Prometheus統合を削除する                                                    |
| CreateCluster | クラスターを作成する                                                           |
| DeleteCluster | クラスターを削除する                                                           |
| PauseCluster | クラスターを一時停止する                                                         |
| ResumeCluster | クラスターを再開する                                                           |
| ScaleCluster | クラスターをスケールする                                                         |
| DownloadTiDBClusterCA | CA証明書をダウンロード                                                         |
| OpenWebSQLConsole | Web SQL 経由で TiDB クラスターに接続する                                          |
| SetRootPassword | TiDBクラスタのルートパスワードを設定する                                               |
| UpdateIPAccessList | TiDB クラスタの IP アクセス リストを更新する                                          |
| SetAutoBackup | TiDBクラスタの自動バックアップメカニズムを設定する                                          |
| DoManualBackup | TiDBクラスタの手動バックアップを実行する                                               |
| BackupCompleted | バックアップタスクが完了しました                                                     |
| DeleteBackupTask | バックアップタスクを削除する                                                       |
| DeleteBackup | バックアップファイルを削除する                                                      |
| RestoreFromBackup | バックアップファイルに基づいてTiDBクラスタに復元する                                         |
| RestoreFromTrash | ゴミ箱内のバックアップファイルに基づいてTiDBクラスタに復元する                                    |
| ImportDataFromAWS | AWSからデータをインポートする                                                     |
| ImportDataFromGCP | Google Cloud からデータをインポートする                                           |
| ImportDataFromLocal | ローカルディスクからデータをインポートする                                                |
| CreateMigrationJob | 移行ジョブを作成する                                                           |
| SuspendMigrationJob | 移行ジョブを一時停止する                                                         |
| ResumeMigrationJob | 移行ジョブを再開する                                                           |
| DeleteMigrationJob | 移行ジョブを削除する                                                           |
| ShowDiagnose | 診断情報を表示                                                              |
| DBAuditLogAction | データベース監査ログのアクティビティを設定する                                              |
| AddDBAuditFilter | データベース監査ログフィルタを追加する                                                  |
| DeleteDBAuditFilter | データベース監査ログフィルタを削除する                                                  |
| EditProject | プロジェクトの情報を編集する                                                       |
| DeleteProject | プロジェクトを削除する                                                          |
| BindSupportPlan | サポートプランを締結する                                                         |
| CancelSupportPlan | サポートプランをキャンセルする                                                      |
| UpdateOrganizationName | 組織名を更新する                                                             |
| SetSpendLimit | TiDB Cloud Starter クラスターの支出制限を編集する                                   |
| UpdateMaintenanceWindow | メンテナンスウィンドウの開始時刻を変更する                                                |
| DeferMaintenanceTask | メンテナンスタスクを延期する                                                       |
| CreateBranch | TiDB Cloud Starter またはTiDB Cloud Essential クラスターのブランチを作成する           |
| DeleteBranch | TiDB Cloud Starter またはTiDB Cloud Essential クラスターのブランチを削除します          |
| SetBranchRootPassword | TiDB Cloud Starter またはTiDB Cloud Essential クラスターのブランチのルートパスワードを設定する |
| ConnectBranchGitHub | クラスターをGitHubリポジトリに接続してブランチ統合を有効にする                                   |
| DisconnectBranchGitHub | ブランチ統合を無効にするには、クラスターを GitHub リポジトリから切断します。                           |
| UpdateAuthenticationMethod | Cloud Organization SSO の認証方法を更新する                                    |

## コンソール監査ログフィールド {#console-audit-log-fields}

ユーザー アクティビティを追跡できるように、 TiDB Cloud各コンソール監査ログに次のフィールドが用意されています。

| フィールド名       | データ型    | 説明                                                             |
| ------------ | --------- | -------------------------------------------------------------- |
| type          | string    | イベントの種類                                                        |
| ends_at       | timestamp | イベント時間                                                         |
| operator_type | enum      | オペレーターの種類: `user`または`api_key`                                     |
| operator_id   | uint64    | オペレーターID                                                       |
| operator_name | string    | オペレーター名                                                        |
| operator_ip   | string    | オペレーターのIPアドレス                                                  |
| operator_login_method | enum      | `microsoft`のログイン`github` : `google` `email`または`api_key`        |
| org_id        | uint64    | イベントが属する組織ID                                                   |
| org_name      | string    | イベントが属する組織名                                                    |
| project_id    | uint64    | イベントが属するプロジェクトID                                               |
| project_name  | string    | イベントが属するプロジェクト名                                                |
| cluster_id    | uint64    | イベントが属するクラスタID                                                 |
| cluster_name  | string    | イベントが属するクラスタ名                                                  |
| trace_id      | string    | オペレーターによって開始されたリクエストのトレースID。このフィールドは現在空ですが、将来のリリースで利用可能になる予定です。 |
| result        | enum      | イベント結果: `success`または`failure`                                  |
| details       | json      | イベントの詳細な説明                                                     |
