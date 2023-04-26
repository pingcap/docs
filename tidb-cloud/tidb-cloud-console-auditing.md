---
title: Console Audit Logging
summary: Learn about the audit logging feature for the TiDB Cloud console.
---

# コンソール監査ログ {#console-audit-logging}

TiDB Cloud は、コンソール監査ログ機能を提供して、ユーザーのさまざまな行動や操作を追跡するのに役立ちます[TiDB Cloudコンソール](https://tidbcloud.com) .たとえば、ユーザーを組織に招待したり、クラスターを作成したりするなどの操作を追跡できます。

## 前提条件 {#prerequisites}

-   TiDB Cloudで組織の所有者または監査管理者の役割に属している必要があります。そうしないと、 TiDB Cloudコンソールにコンソール監査ログ関連のオプションが表示されません。監査管理者の役割は要求があった場合にのみ表示されるため、所有者の役割を直接使用することをお勧めします。監査管理者の役割を使用する必要がある場合は、 **[?]**をクリックします。 [TiDB Cloudコンソール](https://tidbcloud.com)の右下隅にある をクリックし、 <strong>[Chat with Us]</strong>をクリックします。次に、 <strong>[説明</strong>] フィールドに「監査管理者ロールに申し込む」と入力し、 <strong>[送信]</strong>をクリックします。 TiDB Cloudでのロールの詳細については、 [ロール アクセスの管理](/tidb-cloud/manage-user-access.md#manage-role-access)を参照してください。
-   組織のコンソール監査ログのみを有効または無効にすることができます。組織内のユーザーのアクションのみを追跡できます。
-   コンソール監査ロギングが有効になった後、 TiDB Cloudコンソールのすべてのイベント タイプが監査され、それらの一部のみを監査するように指定することはできません。

## コンソール監査ログを有効にする {#enable-console-audit-logging}

コンソール監査ログ機能は、デフォルトで無効になっています。有効にするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある<mdsvgicon name="icon-top-organization">**組織**&gt;<strong>コンソール監査ログ</strong>。</mdsvgicon>
2.  右上隅の**[設定]**をクリックし、コンソール監査ログを有効にします。

## コンソール監査ログを無効にする {#disable-console-audit-logging}

コンソール監査ログを無効にするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある<mdsvgicon name="icon-top-organization">**組織**&gt;<strong>コンソール監査ログ</strong>。</mdsvgicon>
2.  右上隅の**[設定]**をクリックし、コンソールの監査ログを無効にします。

## コンソール監査ログをビュー {#view-console-audit-logs}

組織のコンソール監査ログのみを表示できます。

> **ノート：**
>
> -   組織が初めてコンソール監査ログを有効にする場合、コンソール監査ログは空です。監査対象のイベントが実行されると、対応するログが表示されます。
> -   コンソール監査ログが無効になってから 90 日以上経過している場合、ログは表示されません。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある<mdsvgicon name="icon-top-organization">**組織**&gt;<strong>コンソール監査ログ</strong>。</mdsvgicon>
2.  監査ログの特定の部分を取得するために、イベント タイプ、操作ステータス、および時間範囲をフィルター処理できます。
3.  (省略可能) さらにフィールドをフィルター処理するには、 **[高度なフィルター]**をクリックし、さらにフィルターを追加して、 <strong>[適用]</strong>をクリックします。
4.  ログの行をクリックして、右側のペインに詳細情報を表示します。

## コンソール監査ログのエクスポート {#export-console-audit-logs}

組織のコンソール監査ログをエクスポートするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある<mdsvgicon name="icon-top-organization">**組織**&gt;<strong>コンソール監査ログ</strong>。</mdsvgicon>
2.  (オプション) コンソール監査ログの特定の部分をエクスポートする必要がある場合は、さまざまな条件でフィルタリングできます。それ以外の場合は、この手順をスキップしてください。
3.  **[エクスポート]**をクリックし、JSON または CSV で目的のエクスポート形式を選択します。

## コンソール監査ログstorageポリシー {#console-audit-log-storage-policy}

コンソール監査ログのstorage期間は 90 日で、その後ログは自動的にクリーンアップされます。

> **ノート：**
>
> -   TiDB Cloudでコンソール監査ログのstorage場所を指定することはできません。
> -   監査ログを手動で削除することはできません。

## コンソール監査イベントの種類 {#console-audit-event-types}

コンソール監査ログは、イベント タイプを通じてTiDB Cloudコンソールでのさまざまなユーザー アクティビティを記録します。

> **ノート：**
>
> 現在、 TiDB Cloudコンソールのほとんどのイベント タイプは監査可能であり、次の表で確認できます。まだカバーされていない残りのイベントの種類については、 TiDB Cloud は継続的にそれらを含める作業を行います。

| コンソール監査イベント タイプ              | 説明                                   |
| ---------------------------- | ------------------------------------ |
| 組織の作成                        | 組織を作成する                              |
| ログイン組織                       | 組織にログインする                            |
| 組織の切り替え                      | 現在の組織から別の組織に切り替える                    |
| ログアウト組織                      | 組織からログアウトする                          |
| InviteUserToOrganization     | ユーザーを組織に招待する                         |
| 組織への招待を削除                    | 組織に参加するためのユーザーの招待を削除する               |
| 招待状を組織に再送信                   | ユーザーが組織に参加するための招待状を再送信する             |
| 確認参加組織                       | 招待されたユーザーが組織への参加を確認します               |
| 組織からユーザーを削除                  | 組織から参加ユーザーを削除する                      |
| UpdateUserRoleInOrganization | 組織内のユーザーの役割を更新する                     |
| CreateAPIKey                 | API キーを作成する                          |
| EditAPIKey                   | API キーを編集する                          |
| APIキーの削除                     | API キーを削除する                          |
| UpdateTimezone               | 組織のタイム ゾーンを更新する                      |
| ショービル                        | 組織の請求書を表示                            |
| ダウンロード請求書                    | 組織請求書をダウンロード                         |
| 表示クレジット                      | 組織のクレジットを表示                          |
| AddPaymentCard               | 支払いカードを追加する                          |
| UpdatePaymentCard            | 支払いカードを更新する                          |
| ペイメントカードの削除                  | 支払いカードを削除する                          |
| SetDefaultPaymentCard        | デフォルトの支払いカードを設定する                    |
| 請求プロファイルの編集                  | 請求プロファイル情報の編集                        |
| 契約アクション                      | 契約関連の活動を組織する                         |
| コンソール監査ログを有効にする              | コンソール監査ログを有効にする                      |
| ShowConsoleAuditLog          | コンソール監査ログを表示                         |
| InviteUserToProject          | ユーザーをプロジェクトに招待する                     |
| DeleteInvitationToProject    | プロジェクトに参加するためのユーザーの招待を削除する           |
| ResendInvitationToProject    | ユーザーがプロジェクトに参加するための招待状を再送信する         |
| プロジェクトへの参加の確認                | 招待されたユーザーがプロジェクトへの参加を確認します           |
| プロジェクトからユーザーを削除              | 参加しているユーザーをプロジェクトから削除する              |
| プロジェクトの作成                    | プロジェクトを作成する                          |
| CreateProjectCIDR            | 新しいプロジェクト CIDR を作成する                 |
| CreateAWSVPCPeering          | AWS VPC ピアリングを作成する                   |
| 削除AWSVPCピアリング                | AWS VPC ピアリングを削除する                   |
| CreateGCPVPCPeering          | GCP VPC ピアリングを作成する                   |
| 削除GCPVPCPeering              | GCP VPC ピアリングを削除する                   |
| CreatePrivateEndpointService | プライベート エンドポイント サービスを作成する             |
| プライベート エンドポイント サービスの削除       | プライベート エンドポイント サービスの削除               |
| CreateAWSPrivateEndPoint     | AWS プライベート エンドポイントを作成する              |
| AWSPrivateEndPoint の削除       | AWS プライベート エンドポイントを削除する              |
| 購読アラート                       | アラートを購読する                            |
| 購読解除アラート                     | アラートの登録解除                            |
| CreateDatadog統合              | Datadog 統合を作成する                      |
| Datadog統合の削除                 | Datadog 統合の削除                        |
| CreateVercelIntegration      | vercel 統合を作成する                       |
| 削除Vercel統合                   | バーセル統合の削除                            |
| プロメテウス統合の作成                  | Prometheus 統合の作成                     |
| プロメテウス統合の削除                  | Prometheus 統合の削除                     |
| CreateCluster                | クラスターを作成する                           |
| クラスターの削除                     | クラスターを削除する                           |
| PauseCluster                 | クラスターを一時停止する                         |
| ResumeCluster                | クラスターを再開する                           |
| スケールクラスター                    | クラスターをスケーリングする                       |
| ダウンロードTiDBClusterCA          | TiDB クラスター CA 証明書をダウンロードする           |
| OpenWebSQLConsole            | Web SQL を介して TiDB クラスターに接続する         |
| SetRootPassword              | TiDB クラスターの root パスワードを設定する          |
| UpdateIPAccessList           | TiDB クラスターの IP アクセス リストを更新する         |
| 自動バックアップの設定                  | TiDB クラスターの自動バックアップ メカニズムを設定する       |
| DoManualBackup               | TiDB クラスターの手動バックアップを実行する             |
| バックアップ タスクの削除                | バックアップ タスクを削除する                      |
| バックアップの削除                    | バックアップ ファイルを削除する                     |
| バックアップから復元                   | バックアップ ファイルに基づいて TiDB クラスターに復元する     |
| RestoreFromTrash             | ごみ箱のバックアップ ファイルに基づいて TiDB クラスターに復元する |
| ImportDataFromAWS            | AWS からデータをインポートする                    |
| ImportDataFromGCP            | GCP からデータをインポートする                    |
| ImportDataFromLocal          | ローカル ディスクからデータをインポートする               |
| CreateMigrationJob           | 移行ジョブを作成する                           |
| SuspendMigrationJob          | 移行ジョブを中断する                           |
| ResumeMigrationJob           | 移行ジョブを再開する                           |
| 移行ジョブの削除                     | 移行ジョブを削除する                           |
| ShowDiagnose                 | 診断情報を表示                              |
| DBAuditLogAction             | データベース監査ログのアクティビティを設定する              |
| AddDBAuditFilter             | データベース監査ログ フィルタを追加する                 |
| DeleteDBAuditFilter          | データベース監査ログ フィルタを削除する                 |
| プロジェクトの編集                    | プロジェクトの情報を編集する                       |
| プロジェクトの削除                    | プロジェクトを削除する                          |
| BindSupportPlan              | サポート プランをバインドする                      |
| キャンセルサポートプラン                 | サポート プランをキャンセルする                     |
| 更新組織名                        | 組織名を更新する                             |
| SetSpendLimit                | Serverless Tierクラスターの使用制限を編集する       |
| UpdateMaintenanceWindow      | メンテナンス ウィンドウの開始時刻を変更する               |
| DeferMaintenanceTask         | メンテナンス タスクを延期する                      |

## コンソール監査ログのフィールド {#console-audit-log-fields}

ユーザー アクティビティの追跡を支援するために、 TiDB Cloud は各コンソール監査ログに次のフィールドを提供します。

| フィールド名                | データ・タイプ | 説明                                                                       |
| --------------------- | ------- | ------------------------------------------------------------------------ |
| タイプ                   | 弦       | イベントタイプ                                                                  |
| end_at                | タイムスタンプ | イベント時間                                                                   |
| operator_type         | 列挙      | オペレーターの種類: `user`または`api_key`                                            |
| operator_id           | uint64  | オペレーターID                                                                 |
| operator_name         | 弦       | 事業者名                                                                     |
| operator_ip           | 弦       | オペレーターのIPアドレス                                                            |
| operator_login_method | 列挙      | オペレーターのログイン方法: `google` 、 `github` 、 `microsoft` 、 `email` 、または`api_key` |
| org_id                | uint64  | イベントが所属する組織ID                                                            |
| 組織名                   | 弦       | イベントの所属団体名                                                               |
| project_id            | uint64  | イベントが属するプロジェクト ID                                                        |
| プロジェクト名               | 弦       | イベントが属するプロジェクト名                                                          |
| cluster_id            | uint64  | イベントが属するクラスタID                                                           |
| cluster_name          | 弦       | イベントが属するクラスタ名                                                            |
| trace_id              | 弦       | オペレーターによって開始された要求のトレース ID。このフィールドは現在空で、将来のリリースで使用可能になります。                |
| 結果                    | 列挙      | イベント結果: `success`または`failure`                                            |
| 詳細                    | json    | イベントの詳しい説明                                                               |
