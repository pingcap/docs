---
title: 任务流 (Task Flow)
summary: "任务流 (Task Flow) 是 {{{ .lake }}} 内置的工作流编排功能。它允许你将基于 SQL 的数据流水线定义、调度和监控为有向无环图 (DAG)。"
---

# 任务流 (Task Flow)

任务流 (Task Flow) 是 {{{ .lake }}} 内置的工作流编排功能。它允许你将基于 SQL 的数据流水线定义、调度和监控为有向无环图 (DAG)。图中的每个节点都是一个 **Task**——一条具有自身调度、依赖关系和执行设置的 SQL 语句。**Flow** 将多个任务组合在一起，并自动管理它们的执行顺序。

## 概述 {#overview}

Task Flow 用更强大的模型替代了旧版的 Task List：

| 功能               | 旧版任务列表 | 任务流 (Task Flow) |
| --------------------- | ---------------- | --------- |
| 单个 SQL 任务       | ✅               | ✅        |
| 多任务 DAG        | ❌               | ✅        |
| 可视化图形编辑器   | ❌               | ✅        |
| 版本历史       | ❌               | ✅        |
| 基于流的触发器 | ❌               | ✅        |
| 批量操作       | ❌               | ✅        |

## 核心概念 {#key-concepts}

### Task {#task}

Task 是最小的工作单元。它包含：

- 一条要执行的 SQL 语句
- 调度方式（手动、间隔或 cron）
- 对其他任务或 stream 的可选依赖关系
- 高级设置（失败阈值、查询结果缓存、最小执行间隔）

### Flow {#flow}

Flow 是一组具有依赖关系的命名任务集合。{{{ .lake }}} 会根据 DAG 结构自动确定执行顺序。一个 flow 包含：

- 名称和分配的计算集群 (Warehouse)
- 一个或多个已定义依赖关系的任务
- 生命周期：Created → Started → Suspended → Resumed → Dropped

### DAG (Directed Acyclic Graph) {#dag-directed-acyclic-graph}

任务之间的依赖图。如果 Task B 依赖于 Task A，{{{ .lake }}} 会先运行 Task A，并且只有在 Task A 成功后才会触发 Task B。不允许存在循环依赖。

## 快速开始 {#getting-started}

### 创建任务流 {#creating-a-task-flow}

1. 在左侧边栏中，导航到 **Data** > **Task & Flows**。
2. 点击右上角的 **Create**。
3. 在 flow 弹窗中：
    - 输入 **Flow Name**。
    - 选择用于运行任务的 **Warehouse**。
4. 点击 **Add Task to Flow** 添加第一个任务。

### 配置任务 {#configuring-a-task}

在任务表单中，填写以下内容：

**Basic Settings**

| 字段     | 描述                                                                     |
| --------- | ------------------------------------------------------------------------ |
| Task Name | flow 内的唯一名称                                                        |
| Schedule  | 运行时间：Manual、Interval（例如每 5 分钟）或 Cron 表达式               |
| Timezone  | 用于 cron 调度计算的时区                                                 |
| SQL       | 要执行的 SQL 语句                                                        |
| Comment   | 可选描述                                                                 |

**Dependencies**

| 字段          | 描述                                                         |
| -------------- | ------------------------------------------------------------------- |
| Require Tasks  | 在此任务运行前必须完成的其他任务                                    |
| Require Stream | 在触发此任务前必须有新数据的数据库 stream                           |

**Advanced Options**

| 字段                           | 描述                                                                    |
| ------------------------------- | ----------------------------------------------------------------------- |
| Suspend Task After Num Failures        | 连续失败 N 次后自动暂停该任务（0 = 从不）                              |
| Enable Query Result Cache                | 缓存查询结果以避免重复计算                                              |
| Min Execute Seconds                    | 两次执行之间的最小间隔（5s / 10s / 15s / 30s）                          |

1. 点击 **Save** 将任务添加到 flow 中。
2. 重复上述步骤以添加更多任务。使用 **Require Tasks** 定义它们之间的依赖关系。
3. 点击 **Publish** 创建 flow。

> **Note:**
>
> 只有 `account_admin` 或 flow 创建者可以编辑或删除 flow。

## 可视化 Flow {#visualizing-the-flow}

创建 flow 后，点击其名称以打开详情页。**Latest Run** 标签页会显示 DAG 可视化图。

每个节点会显示：

- 任务名称
- 最近一次执行状态（用颜色区分）
- 执行时间范围
- 错误信息（如果失败）

**状态颜色：**

| 颜色             | 状态              |
| ----------------- | ------------------- |
| 蓝色边框       | Scheduled           |
| 绿色边框      | Succeeded           |
| 红色边框        | Failed              |
| 浅蓝色边框 | Executing           |
| 灰色边框       | Cancelled / Waiting |

## 管理 Flows {#managing-flows}

### Flow 操作 {#flow-actions}

在 **Task & Flows** 列表中，每一行都有一个操作菜单，包含：

| 操作                | 描述                           |
| --------------------- | ------------------------------------- |
| Edit                  | 修改 flow 名称、计算集群或任务        |
| Suspend               | 暂停所有已调度的执行                  |
| Resume                | 重新启用已调度的执行                  |
| Execute Once          | 立即触发一次性运行                    |
| View Runs History     | 查看所有历史执行                      |
| View Versions History | 浏览并比较历史版本                    |
| Delete                | 永久删除该 flow                       |

### 批量操作 {#bulk-operations}

使用复选框选择多个 flow，然后使用批量操作菜单来：

- 暂停所有选中的 flow
- 恢复所有选中的 flow
- 删除所有选中的 flow

## 监控执行情况 {#monitoring-executions}

### 运行历史 {#runs-history}

在详情页点击 **Runs History** 以查看所有历史执行：

| 列            | 描述                                                   |
| -------------- | ------------------------------------------------------ |
| Task Name       | 运行的是哪个任务                                       |
| Warehouse | 使用的 Warehouse                                       |
| State           | Scheduled / Executing / Succeeded / Failed / Cancelled |
| SQL            | 已执行的 SQL（带 Query ID 链接）                       |
| Scheduled Time       | 运行被触发的时间                                       |
| Completed Time       | 运行完成的时间                                         |
| Comment           | 任务备注                                               |

失败或已取消的运行会显示错误提示。你可以点击错误查看详情或创建支持工单。

### 全局任务历史 {#global-task-history}

导航到 **Data** → **Task History**，查看组织中所有 flow 的执行情况。你可以按以下条件筛选：

- 任务名称（多选）
- 时间范围（最近 2 天、最近 3 天）

## 版本控制 {#version-control}

每次你发布对 flow 的更改时，{{{ .lake }}} 都会保存一个新版本。要访问版本历史：

1. 打开 flow 详情页。
2. 点击 **Versions History** 标签页。

### 比较版本 {#comparing-versions}

1. 使用复选框选择两个版本。
2. 点击 **Compare**。
3. 系统会打开一个并排的 SQL diff 抽屉，显示这两个版本之间的变更内容。

### 回退到先前版本 {#reverting-to-a-previous-version}

1. 从列表中选择一个版本。
2. 点击 **Revert**。
3. 在对话框中确认该操作。

flow 会恢复到所选版本，并创建一个新的版本记录。

## 调度参考 {#scheduling-reference}

### 调度类型 {#schedule-types}

**Manual**：任务仅在通过 **Execute Once** 触发时运行。不会自动调度。

**Interval**：每 N 分钟/小时运行一次。示例：`EVERY 5 MINUTE`。

**Cron**：带时区支持的标准 cron 表达式。示例：`0 9 * * 1-5`（工作日上午 9 点）。

### 基于 Stream 的触发器 {#stream-based-triggers}

如果任务具有 **Require Stream** 依赖关系，则只有在指定 stream 存在未消费数据时才会执行。这对于构建响应表变更（CDC）的事件驱动型流水线非常有用。

## 最佳实践 {#best-practices}

- **从简单开始**：先创建一个单任务流，以便在添加依赖关系之前验证 SQL。
- **对 CDC 管道使用 stream**：将 stream 触发器与 `MERGE INTO` 语句结合使用，以构建增量数据管道。
- **设置失败阈值**：使用 **Suspend Task After Num Failures**，防止失控重试消耗计算集群额度。
- **启用结果缓存**：对于重复查询相同数据的任务，启用 **Query Result Cache** 以降低计算成本。
- **使用版本历史**：在进行重大更改之前，记下当前版本号，以便在需要时回退。
- **按工作负载分离计算集群**：将较重的转换任务分配到更大的计算集群，将轻量任务分配到较小的计算集群。

## 权限 {#permissions}

| 角色          | 创建 | 编辑     | 删除     | 查看 |
| ------------- | ------ | -------- | -------- | ---- |
| account_admin | ✅     | ✅（任意） | ✅（任意） | ✅   |
| 创建者        | ✅     | ✅（自己的） | ✅（自己的） | ✅   |
| 其他用户      | ❌     | ❌       | ❌       | ✅   |
