---
title: FeiShuBot
summary: 本页介绍如何创建 `FeiShuBot` 数据源。该数据源用于存储飞书机器人 webhook 和消息模板，适用于任务失败通知等场景。
---

# FeiShuBot

本页介绍如何创建 `FeiShuBot` 数据源。该数据源用于存储飞书机器人 webhook 和消息模板，通常用于任务失败通知。

## 使用场景 {#use-cases}

- 在任务运行失败时向飞书群发送通知
- 在多个任务之间复用同一套机器人配置和消息模板
- 集中管理通知端点和消息格式

## 创建 FeiShuBot {#create-feishubot}

1. 进入 **Data** > **Data Sources**，然后点击 **Create Data Source**。
2. 选择 **FeiShuBot** 作为服务类型，然后填写以下字段：

    | 字段 | 必填 | 描述 |
    |-------|----------|-------------|
    | **Name** | 是 | 该数据源的描述性名称。仅支持字母、数字和下划线 |
    | **URL** | 是 | 自定义飞书机器人 webhook URL |
    | **Warehouse** | 是 | 用于创建 `NOTIFICATION INTEGRATION` 的计算集群 |
    | **Payload** | 是 | 消息负载类型。目前仅支持 `Task Error` |
    | **Template** | 是 | 自定义消息模板 |

3. 点击 **Test Connectivity** 验证配置。如果测试成功，点击 **OK** 保存数据源。

## 用法 {#usage}

`FeiShuBot` 可与 SQL Task 的 `ERROR_INTEGRATION` 属性一起使用，也可以在控制台的任务流 (Task Flow) UI 中通过 **Error Notification** 引用。

### 设置 SQL Task 属性 {#set-a-sql-task-property}

设置 Task 的 `ERROR_INTEGRATION` 属性。在以下示例中，数据源名称为 `test_1`：

```sql
CREATE TASK my_daily_task
   WAREHOUSE = 'compute_wh'
   SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
   COMMENT = 'Daily summary task'
   ERROR_INTEGRATION = 'test_1'
AS
   INSERT INTO summary_table SELECT * FROM source_table;
```

### 在任务流 UI 中配置 {#configure-it-in-the-task-flow-ui}

在创建或编辑页面中，将 **Error Notification** 设置为对应的 `FeiShuBot` 数据源。

### 自定义任务错误模板 {#customize-the-task-error-template}

默认模板：

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

收到的消息示例如下：

![FeiShu notification example](/media/tidb-cloud-lake/feishubot-example.png)

自定义模板支持：

- Markdown 内容
- Golang 模板语法

可用变量如下：

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

## 注意事项 {#notes}

`FeiShuBot` 是一种面向通知的数据源，不用于将业务数据加载到 {{{ .lake }}} 中。
