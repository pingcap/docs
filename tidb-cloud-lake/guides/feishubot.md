---
title: FeiShuBot
summary: このページでは、`FeiShuBot` データソースを作成する方法について説明します。このデータソースには、タスク失敗通知などのシナリオで使用する FeiShu bot の webhook とメッセージテンプレートが保存されます。
---

# FeiShuBot

このページでは、`FeiShuBot` データソースを作成する方法について説明します。このデータソースには FeiShu bot の webhook とメッセージテンプレートが保存され、通常はタスク失敗通知に使用されます。

## ユースケース {#use-cases}

- タスク実行が失敗したときに、FeiShu グループへ通知を送信する
- 複数のタスク間で同じ bot 設定とメッセージテンプレートを再利用する
- 通知エンドポイントとメッセージ形式を一元管理する

## FeiShuBot を作成する {#create-feishubot}

1. **Data** > **Data Sources** に移動し、**Create Data Source** をクリックします。
2. サービスタイプとして **FeiShuBot** を選択し、次のフィールドを入力します。

    | フィールド | 必須 | 説明 |
    |-------|----------|-------------|
    | **Name** | はい | このデータソースの説明的な名前です。使用できるのは英字、数字、アンダースコアのみです |
    | **URL** | はい | カスタム FeiShu bot webhook URL |
    | **Warehouse** | はい | `NOTIFICATION INTEGRATION` の作成に使用する Warehouse |
    | **Payload** | はい | メッセージ payload の種類です。現在は `Task Error` のみサポートされています |
    | **Template** | はい | カスタムメッセージテンプレート |

3. **Test Connectivity** をクリックして設定を検証します。テストが成功したら、**OK** をクリックしてデータソースを保存します。

## 使用方法 {#usage}

`FeiShuBot` は、SQL Task の `ERROR_INTEGRATION` プロパティとともに使用するか、コンソールのタスクフロー (task flow) UI の **Error Notification** から参照できます。

### SQL Task プロパティを設定する {#set-a-sql-task-property}

Task の `ERROR_INTEGRATION` プロパティを設定します。次の例では、データソース名は `test_1` です。

```sql
CREATE TASK my_daily_task
   WAREHOUSE = 'compute_wh'
   SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
   COMMENT = 'Daily summary task'
   ERROR_INTEGRATION = 'test_1'
AS
   INSERT INTO summary_table SELECT * FROM source_table;
```

### タスクフロー UI で設定する {#configure-it-in-the-task-flow-ui}

作成ページまたは編集ページで、**Error Notification** を対応する `FeiShuBot` データソースに設定します。

### Task Error テンプレートをカスタマイズする {#customize-the-task-error-template}

デフォルトテンプレート:

```text
**[ALERT] {{ .MessageType }} - {{ .TaskName }}**
---
taskId: {{ .TaskId }}
taskName: {{ .TaskName }}
tenantId: {{ .TenantId }}

Messages: {{ range .Messages }}
- runId: {{ .RunId }}
  queryId: {{ .QueryId }}
  error: {{ .ErrorKind }} ({{ .ErrorCode }})
  message: {{ .ErrorMessage }} {{ end }}

---
{{ .Timestamp }}
```

受信されるメッセージは、次のようになります。

![FeiShu 通知の例](/media/tidb-cloud-lake/feishubot-example.png)

カスタムテンプレートでサポートされる内容:

- Markdown コンテンツ
- Golang テンプレート構文

使用可能な変数は次のとおりです。

```golang
type ErrorIntegrationPayload struct {
        Version      string          `json:"version"`
        MessageId    string          `json:"messageId"`
        MessageType  string          `json:"messageType"`
        Timestamp    time.Time       `json:"timestamp"`
        TenantId     string          `json:"tenantId"`
        TaskName     string          `json:"taskName"`
        TaskId       string          `json:"taskId"`
        RootTaskName string          `json:"rootTaskName"`
        RootTaskId   string          `json:"rootTaskId"`
        Messages     []*ErrorMessage `json:"messages"`
}

type ErrorMessage struct {
        RunId          string     `json:"runId"`
        ScheduledTime  time.Time  `json:"scheduledTime"`
        QueryStartTime *time.Time `json:"queryStartTime"`
        CompletedTime  *time.Time `json:"completedTime"`
        QueryId        string     `json:"queryId"`
        ErrorKind      string     `json:"errorKind"`
        ErrorCode      string     `json:"errorCode"`
        ErrorMessage   string     `json:"errorMessage"`
}
```

## 注意事項 {#notes}

`FeiShuBot` は通知用途のデータソースです。これは、ビジネスデータを {{{ .lake }}} にロードするためには使用されません。