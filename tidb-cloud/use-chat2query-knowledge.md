---
title: Use Knowledge Bases
summary: Learn how to improve your Chat2Query results by using Chat2Query knowledge base APIs.
---

# Use Knowledge Bases

A knowledge base is a collection of structured data that can be used to enhance the SQL generation capabilities of Chat2Query.

Starting from v3, the Chat2Query API enables you to add or modify knowledge bases by calling knowledge base related endpoints of your Chat2Query Data App.

> **Note:**
>
> Knowledge base related endpoints are available for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters by default.

## Before you begin

Before creating a knowledge base for your database, make sure that you have the following:

- A [Chat2Query Data App](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app)
- An [API key for the Chat2Query Data App](/tidb-cloud/use-chat2query-api.md#create-an-api-key)

## Step 1. Create a knowledge base for the linked database

> **Note:**
>
> The knowledge used by Chat2Query is **structured according to the database dimension**. You can connect multiple Chat2Query Data Apps to the same database, but each Chat2Query Data App can only use knowledge from a specific database it is linked to.

In your Chat2Query Data App, you can create a knowledge base for a specific database by calling the `/v3/knowledgeBases` endpoint. After creation, you will get a `knowledge_base_id` for future knowledge management.

The following is a general code example for calling this endpoint.

> **Tip:**
>
> To get a specific code example for your endpoint, click the endpoint name in the left pane of your Data App, and then click **Show Code Example**. For more information, see [Get the example code of an endpoint](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint).

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "<The ID of the cluster to which the database belongs>",
    "database": "<The name of the target database>",
    "description": "<Your knowledge base description>"
}'
```

An example response is as follows:

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

After getting the response, record the `knowledge_base_id` value in your response for later use.

## Step 2. Choose a knowledge type

The knowledge base of each database can contain multiple types of knowledge. Before adding knowledge to your knowledge base, you need to choose a knowledge type that best suits your use case.

Currently, Chat2Query knowledge bases support the following knowledge types. Each type is specifically designed for different scenarios and has a unique knowledge structure.

- [Few-shot example](#few-shot-example)
- [Term-sheet explanation](#term-sheet-explanation)
- [Instruction](#instruction)

### Few-shot example

Few-shot example refers to the Q&A learning samples provided to Chat2Query, which include sample questions and their corresponding answers. These examples help Chat2Query handle new tasks more effectively.

> **Note:**
>
> Make sure the accuracy of newly added examples, because the quality of examples affects how well Chat2Query learns. Poor examples, such as mismatched questions and answers, can degrade the performance of Chat2Query on new tasks.

#### Knowledge structure

Each example consists of a sample question and its corresponding answer.

For example:

```json
{
    "question": "How many records are in the 'test' table?",
    "answer": "SELECT COUNT(*) FROM `test`;"
}
```

#### Use cases

Few-Shot examples can significantly improve the performance of Chat2Query in various scenarios, including but not limited to the following:

1. **When dealing with rare or complex questions**: if Chat2Query encounters infrequent or complex questions, adding few-shot examples can enhance its understanding and improve the accuracy of the results.

2. **When struggling with a certain type of question**: if Chat2Query frequently makes mistakes or has difficulty with specific questions, adding few-shot examples can help improve its performance on these questions.

### Term-sheet explanation

Term-sheet explanation refers to a comprehensive explanation of a specific term or a group of similar terms, helping Chat2Query understand the meaning and usage of these terms.

> **Note:**
>
> Make sure the accuracy of newly added term explanations, because the quality of explanations affects how well Chat2Query learns. Incorrect interpretations do not improve Chat2Query results but also potentially lead to adverse effects.

#### Knowledge structure

Each explanation includes either a single term or a list of similar terms and their detailed descriptions.

For example:

```json
{
    "term": ["OSS"],
    "description": "OSS Insight is a powerful tool that provides online data analysis for users based on nearly 6 billion rows of GitHub event data."
}
```

#### Use cases

Term-sheet explanation is primarily used to improve Chat2Query's comprehension of user queries, especially in these situations:

- **Dealing with industry-specific terminology or acronyms**: when your query contains industry-specific terminology or acronyms that might not be universally recognized, using a term-sheet explanation can help Chat2Query understand the meaning and usage of these terms.
- **Dealing with ambiguities in user queries**: when your query contains ambiguous concepts that is confusing, using a term-sheet explanation can help Chat2Query clarify these ambiguities.
- **Dealing with terms with various meanings**: when your query contains terms that carry different meanings in various contexts, using a term-sheet explanation can assist Chat2Query in discerning the correct interpretation.

### Instruction

Instruction is a piece of textual command. It is used to guide or control the behavior of Chat2Query, specifically instructing it on how to generate SQL according to specific requirements or conditions.

> **Note:**
>
> - The instruction has a length limit of 512 characters.
> - Make sure to provide as clear and specific instructions as possible to ensure that Chat2Query can understand and execute the instructions effectively.

#### Knowledge structure

Instruction only includes a piece of textual command.

For example:

```json
{
    "instruction": "If the task requires calculating the sequential growth rate, use the LAG function with the OVER clause in SQL"
}
```

#### Use cases

Instruction can be used in many scenarios to guide Chat2Query to output according to your requirements, including but not limited to the following:

- **Limiting query scope**: if you want the SQL to consider only certain tables or columns, use an instruction to specify this.
- **Guiding SQL structure**: if you have specific requirements for the SQL structure, use an instruction to guide Chat2Query.

## Step 3. Add knowledge to the newly created knowledge base

To add new knowledge, you can call the `/v3/knowledgeBases/{knowledge_base_id}/data` endpoint.

### Add a few-shot example type of knowledge

For example, if you want Chat2Query to generate SQL statements of the count of rows in a table in a specific structure, you can add a few-shot example type of knowledge by calling `/v3/knowledgeBases/{knowledge_base_id}/data` as follows:

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

In the preceding example code, `"type": "few-shot"` represents the few-shot example knowledge type.

### Add a term-sheet explanation type of knowledge

For example, if you want Chat2Query to comprehend the meaning of the term `OSS` using your provided explanation, you can add a term-sheet explanation type of knowledge by calling `/v3/knowledgeBases/{knowledge_base_id}/data` as follows:

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

In the preceding example code, `"type": "term-sheet"` represents the term-sheet explanation knowledge type.

### Add an instruction type of knowledge

For example, if you want Chat2Query to consistently use the `LAG` function with the `OVER` clause in SQL queries when dealing with questions about sequential growth rate calculation, you can add an instruction type of knowledge by calling `/v3/knowledgeBases/{knowledge_base_id}/data` as follows:

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

In the preceding example code, `"type": "instruction"` represents the instruction knowledge type.