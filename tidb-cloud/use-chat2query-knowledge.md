---
title: 使用知识库
summary: 了解如何通过使用 Chat2Query 知识库 API 提升 Chat2Query 的结果质量。
---

# 使用知识库

知识库是一组结构化数据，可用于增强 Chat2Query 的 SQL 生成能力。

从 v3 版本开始，Chat2Query API 支持你通过调用 Chat2Query Data App 的知识库相关接口来添加或修改知识库。

> **Note:**
>
> 知识库相关接口在 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群中默认可用。若要在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中使用知识库相关接口，请联系 [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md)。

## 开始前的准备

在为你的数据库创建知识库之前，请确保你已具备以下条件：

- 一个 [Chat2Query Data App](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app)
- 一个 [Chat2Query Data App 的 API key](/tidb-cloud/use-chat2query-api.md#create-an-api-key)

## 第 1 步：为已关联的数据库创建知识库

> **Note:**
>
> Chat2Query 使用的知识是**按照数据库维度进行结构化**的。你可以将多个 Chat2Query Data App 连接到同一个数据库，但每个 Chat2Query Data App 只能使用其所关联数据库的知识。

在你的 Chat2Query Data App 中，可以通过调用 `/v3/knowledgeBases` 接口为某个特定数据库创建知识库。创建完成后，你将获得一个 `knowledge_base_id`，用于后续的知识管理。

以下是调用该接口的一般代码示例。

> **Tip:**
>
> 若要获取该接口的具体代码示例，请在 Data App 左侧面板点击接口名称，然后点击 **Show Code Example**。更多信息参见 [Get the example code of an endpoint](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint)。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "<The ID of the cluster to which the database belongs>",
    "database": "<The name of the target database>",
    "description": "<Your knowledge base description>"
}'
```

示例响应如下：

```json
{
    "code":200,
    "msg":"",
    "result":
        {
            "default":true,
            "description":"",
            "knowledge_base_id":2
        }
}
```

收到响应后，请记录响应中的 `knowledge_base_id`，以便后续使用。

## 第 2 步：选择知识类型

每个数据库的知识库可以包含多种类型的知识。在向知识库添加知识之前，你需要选择最适合你用例的知识类型。

目前，Chat2Query 知识库支持以下知识类型。每种类型针对不同场景设计，具有独特的知识结构。

- [Few-shot example](#few-shot-example)
- [Term-sheet explanation](#term-sheet-explanation)
- [Instruction](#instruction)

### Few-shot example

Few-shot example 指为 Chat2Query 提供的问答学习样本，包括示例问题及其对应答案。这些示例有助于 Chat2Query 更有效地处理新任务。

> **Note:**
>
> 请确保新添加示例的准确性，因为示例的质量会影响 Chat2Query 的学习效果。低质量的示例（如问题与答案不匹配）会降低 Chat2Query 在新任务上的表现。

#### 知识结构

每个示例由一个示例问题及其对应答案组成。

例如：

```json
{
    "question": "How many records are in the 'test' table?",
    "answer": "SELECT COUNT(*) FROM `test`;"
}
```

#### 适用场景

Few-shot example 能显著提升 Chat2Query 在多种场景下的表现，包括但不限于以下情况：

1. **处理罕见或复杂问题时**：当 Chat2Query 遇到不常见或复杂的问题时，添加 few-shot example 可以增强其理解能力，提高结果的准确性。

2. **在某类问题上表现不佳时**：如果 Chat2Query 在某些特定问题上经常出错或难以处理，添加 few-shot example 可以帮助提升其在这些问题上的表现。

### Term-sheet explanation

Term-sheet explanation 指对某个特定术语或一组相似术语的详细解释，帮助 Chat2Query 理解这些术语的含义和用法。

> **Note:**
>
> 请确保新添加术语解释的准确性，因为解释的质量会影响 Chat2Query 的学习效果。错误的解释不仅无法提升 Chat2Query 的结果，还可能带来负面影响。

#### 知识结构

每条解释包含一个术语或一组相似术语及其详细描述。

例如：

```json
{
    "term": ["OSS"],
    "description": "OSS Insight is a powerful tool that provides online data analysis for users based on nearly 6 billion rows of GitHub event data."
}
```

#### 适用场景

Term-sheet explanation 主要用于提升 Chat2Query 对用户查询的理解能力，尤其适用于以下情况：

- **处理行业专有术语或缩写时**：当你的查询包含行业专有术语或缩写，且这些术语并非通用时，使用 term-sheet explanation 可以帮助 Chat2Query 理解其含义和用法。
- **处理用户查询中的歧义时**：当你的查询包含容易引起混淆的概念时，使用 term-sheet explanation 可以帮助 Chat2Query 澄清这些歧义。
- **处理多义词时**：当你的查询包含在不同语境下有不同含义的术语时，使用 term-sheet explanation 可以帮助 Chat2Query 判断正确的解释。

### Instruction

Instruction 是一段文本指令，用于引导或控制 Chat2Query 的行为，明确告知其在特定需求或条件下如何生成 SQL。

> **Note:**
>
> - Instruction 的长度限制为 512 个字符。
> - 请尽量提供清晰、具体的指令，以确保 Chat2Query 能够准确理解并执行。

#### 知识结构

Instruction 仅包含一段文本指令。

例如：

```json
{
    "instruction": "If the task requires calculating the sequential growth rate, use the LAG function with the OVER clause in SQL"
}
```

#### 适用场景

Instruction 可用于多种场景，引导 Chat2Query 按你的需求输出结果，包括但不限于以下情况：

- **限定查询范围**：如果你希望 SQL 只考虑某些表或列，可以通过 instruction 进行指定。
- **引导 SQL 结构**：如果你对 SQL 结构有特定要求，可以通过 instruction 指导 Chat2Query。

## 第 3 步：向新建的知识库添加知识

要添加新知识，可以调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 接口。

### 添加 few-shot example 类型的知识

例如，如果你希望 Chat2Query 以特定结构生成统计表中行数的 SQL 语句，可以通过如下方式调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 添加 few-shot example 类型的知识：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases/<knowledge_base_id>/data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "type": "few-shot",
    "meta_data": {},
    "raw_data": {
         "question": "How many records are in the 'test' table?",
         "answer": "SELECT COUNT(*) FROM `test`;"
    }
}'
```

在上述示例代码中，`"type": "few-shot"` 表示 few-shot example 知识类型。

### 添加 term-sheet explanation 类型的知识

例如，如果你希望 Chat2Query 能根据你提供的解释理解术语 `OSS` 的含义，可以通过如下方式调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 添加 term-sheet explanation 类型的知识：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases/<knowledge_base_id>/data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "type": "term-sheet",
    "meta_data": {},
    "raw_data": {
        "term": ["OSS"],
        "description": "OSS Insight is a powerful tool that provides online data analysis for users based on nearly 6 billion rows of GitHub event data."
    }
}'
```

在上述示例代码中，`"type": "term-sheet"` 表示 term-sheet explanation 知识类型。

### 添加 instruction 类型的知识

例如，如果你希望 Chat2Query 在处理关于序列增长率计算的问题时始终在 SQL 查询中使用 `LAG` 函数和 `OVER` 子句，可以通过如下方式调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 添加 instruction 类型的知识：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases/<knowledge_base_id>/data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "type": "instruction",
    "meta_data": {},
    "raw_data": {
        "instruction": "If the task requires calculating the sequential growth rate, use the LAG function with the OVER clause in SQL"
    }
}'
```

在上述示例代码中，`"type": "instruction"` 表示 instruction 知识类型。