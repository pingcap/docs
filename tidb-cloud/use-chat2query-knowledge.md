---
title: Use Knowledge Bases
summary: Chat2Query ナレッジ ベース API を使用して Chat2Query の結果を改善する方法を学びます。
---

# ナレッジベースを使用する {#use-knowledge-bases}

ナレッジ ベースは、Chat2Query の SQL 生成機能を強化するために使用できる構造化データのコレクションです。

v3 以降、Chat2Query API を使用すると、Chat2Query データ アプリのナレッジ ベース関連のエンドポイントを呼び出すことによって、ナレッジ ベースを追加または変更できるようになります。

> **注記：**
>
> ナレッジベース関連エンドポイントは、AWS でホストされている[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでのみご利用いただけます。3 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでナレッジベース関連エンドポイントをご利用になる場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## 始める前に {#before-you-begin}

データベースのナレッジ ベースを作成する前に、次のものを用意してください。

-   A [Chat2Queryデータアプリ](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app)
-   [Chat2QueryデータアプリのAPIキー](/tidb-cloud/use-chat2query-api.md#create-an-api-key)

## ステップ1. リンクされたデータベースのナレッジベースを作成する {#step-1-create-a-knowledge-base-for-the-linked-database}

> **注記：**
>
> Chat2Queryが使用する知識は、**データベースのディメンションに基づいて構造化されて**います。複数のChat2Queryデータアプリを同じデータベースに接続できますが、各Chat2Queryデータアプリは、リンクされている特定のデータベースの知識のみを使用できます。

Chat2Queryデータアプリでは、エンドポイント`/v3/knowledgeBases`呼び出すことで、特定のデータベースのナレッジベースを作成できます。作成後は、将来のナレッジ管理のために`knowledge_base_id`付与されます。

以下は、このエンドポイントを呼び出すための一般的なコード例です。

> **ヒント：**
>
> エンドポイントの具体的なコード例を取得するには、データアプリの左側のペインでエンドポイント名をクリックし、 **「コード例を表示」**をクリックします。詳細については、 [エンドポイントのサンプルコードを取得する](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint)参照してください。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "<The ID of the cluster to which the database belongs>",
    "database": "<The name of the target database>",
    "description": "<Your knowledge base description>"
}'
```

応答の例は次のとおりです。

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

応答を取得したら、後で使用するために応答内の`knowledge_base_id`値を記録します。

## ステップ2. 知識の種類を選択する {#step-2-choose-a-knowledge-type}

各データベースのナレッジベースには、複数の種類のナレッジを含めることができます。ナレッジベースにナレッジを追加する前に、ユースケースに最適なナレッジの種類を選択する必要があります。

現在、Chat2Queryナレッジベースは以下のナレッジタイプをサポートしています。各タイプは異なるシナリオ向けに特別に設計されており、独自のナレッジ構造を持っています。

-   [少数ショットの例](#few-shot-example)
-   [契約書の説明](#term-sheet-explanation)
-   [命令](#instruction)

### 少数ショットの例 {#few-shot-example}

少数のサンプルとは、Chat2Queryに提供されるQ&amp;A学習サンプルを指します。サンプルの質問とそれに対応する回答が含まれています。これらのサンプルは、Chat2Queryが新しいタスクをより効率的に処理するのに役立ちます。

> **注記：**
>
> 新しく追加した例文の精度を確認してください。例文の質はChat2Queryの学習効率に影響します。質問と回答が一致しないなど、質の低い例は、新しいタスクにおけるChat2Queryのパフォーマンスを低下させる可能性があります。

#### 知識構造 {#knowledge-structure}

各例は、サンプルの質問とそれに対応する回答で構成されています。

例えば：

```json
{
    "question": "How many records are in the 'test' table?",
    "answer": "SELECT COUNT(*) FROM `test`;"
}
```

#### ユースケース {#use-cases}

Few-Shot の例を使用すると、次のようなさまざまなシナリオで Chat2Query のパフォーマンスを大幅に向上させることができます。

1.  **まれな質問や複雑な質問を扱う場合**: Chat2Query がまれな質問や複雑な質問に遭遇した場合、数回の例を追加すると理解が深まり、結果の精度が向上します。

2.  **特定の種類の質問に苦労している場合**: Chat2Query が頻繁に間違いを犯したり、特定の質問で困難を抱えたりする場合、少数の例を追加すると、これらの質問でのパフォーマンスの向上に役立ちます。

### 契約書の説明 {#term-sheet-explanation}

用語シートの説明とは、特定の用語または類似の用語のグループに関する包括的な説明を指し、Chat2Query がこれらの用語の意味と使用法を理解するのに役立ちます。

> **注記：**
>
> 新しく追加された用語の説明の正確性を確認してください。説明の質はChat2Queryの学習効率に影響します。誤った解釈はChat2Queryの結果を向上させるどころか、悪影響をもたらす可能性があります。

#### 知識構造 {#knowledge-structure}

それぞれの説明には、単一の用語、または類似の用語のリストとその詳細な説明が含まれます。

例えば：

```json
{
    "term": ["OSS"],
    "description": "OSS Insight is a powerful tool that provides online data analysis for users based on nearly 6 billion rows of GitHub event data."
}
```

#### ユースケース {#use-cases}

条件書の説明は主に、特に次のような状況で、Chat2Query によるユーザークエリの理解を向上させるために使用されます。

-   **業界固有の用語や頭字語への対処**: クエリに、一般的には認識されていない可能性のある業界固有の用語や頭字語が含まれている場合、用語シートの説明を使用すると、Chat2Query がこれらの用語の意味と使用法を理解するのに役立ちます。
-   **ユーザークエリの曖昧さへの対処**: クエリに曖昧な概念が含まれており混乱を招く場合、用語シートの説明を使用すると、Chat2Query がこれらの曖昧さを明確にするのに役立ちます。
-   **さまざまな意味を持つ用語の取り扱い**: クエリにさまざまなコンテキストで異なる意味を持つ用語が含まれている場合、用語シートの説明を使用すると、Chat2Query が正しい解釈を判断するのに役立ちます。

### 命令 {#instruction}

命令とは、テキスト形式のコマンドです。Chat2Queryの動作をガイドまたは制御するために使用され、具体的には、特定の要件や条件に応じてSQLを生成する方法を指示します。

> **注記：**
>
> -   命令の長さは 512 文字に制限されます。
> -   Chat2Query が指示を効果的に理解して実行できるように、できるだけ明確で具体的な指示を提供するようにしてください。

#### 知識構造 {#knowledge-structure}

指示にはテキスト コマンドのみが含まれます。

例えば：

```json
{
    "instruction": "If the task requires calculating the sequential growth rate, use the LAG function with the OVER clause in SQL"
}
```

#### ユースケース {#use-cases}

指示はさまざまなシナリオで使用でき、Chat2Query が要件に応じて出力するようにガイドできます。これには次のものが含まれますが、これらに限定されません。

-   **クエリ範囲の制限**: SQL で特定のテーブルまたは列のみを考慮する場合は、これを指定する命令を使用します。
-   **SQL 構造のガイド**: SQL 構造に特定の要件がある場合は、Chat2Query をガイドする指示を使用します。

## ステップ3. 新しく作成したナレッジベースに知識を追加する {#step-3-add-knowledge-to-the-newly-created-knowledge-base}

新しい知識を追加するには、 `/v3/knowledgeBases/{knowledge_base_id}/data`エンドポイントを呼び出すことができます。

### 数ショットの例の知識を追加する {#add-a-few-shot-example-type-of-knowledge}

たとえば、Chat2Query を使用して、特定の構造内のテーブル内の行数の SQL ステートメントを生成する場合は、次のように`/v3/knowledgeBases/{knowledge_base_id}/data`呼び出して、数回のサンプル タイプの知識を追加できます。

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

上記のコード例では、 `"type": "few-shot"`少数ショットの例の知識タイプを表します。

### タームシートの説明タイプの知識を追加する {#add-a-term-sheet-explanation-type-of-knowledge}

たとえば、提供された説明を使用して Chat2Query に用語`OSS`の意味を理解してもらいたい場合は、次のように`/v3/knowledgeBases/{knowledge_base_id}/data`呼び出して用語シートの説明タイプの知識を追加できます。

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

上記のコード例では、 `"type": "term-sheet"`用語シートの説明の知識タイプを表します。

### 指示タイプの知識を追加する {#add-an-instruction-type-of-knowledge}

たとえば、連続成長率の計算に関する質問を処理するときに、Chat2Query が SQL クエリで`OVER`句を含む`LAG`関数を一貫して使用するようにしたい場合は、次のように`/v3/knowledgeBases/{knowledge_base_id}/data`呼び出して、指示タイプの知識を追加できます。

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

上記のコード例では、 `"type": "instruction"`命令の知識タイプを表します。
