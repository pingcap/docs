---
title: Use Knowledge Bases
summary: Chat2Query ナレッジ ベース API を使用して Chat2Query の結果を改善する方法を学びます。
---

# ナレッジベースを使用する {#use-knowledge-bases}

ナレッジ ベースは、Chat2Query の SQL 生成機能を強化するために使用できる構造化データのコレクションです。

v3 以降では、Chat2Query API を使用すると、Chat2Query データ アプリのナレッジ ベース関連のエンドポイントを呼び出すことで、ナレッジ ベースを追加または変更できるようになります。

> **注記：**
>
> ナレッジ ベース関連のエンドポイントは、デフォルトで[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターで使用できます。ナレッジ ベース関連のエンドポイントを[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで使用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## 始める前に {#before-you-begin}

データベースのナレッジ ベースを作成する前に、次のものを用意してください。

-   [Chat2Query データ アプリ](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app)
-   [Chat2Query データ アプリの API キー](/tidb-cloud/use-chat2query-api.md#create-an-api-key)

## ステップ1. リンクされたデータベースのナレッジベースを作成する {#step-1-create-a-knowledge-base-for-the-linked-database}

> **注記：**
>
> Chat2Query が使用する知識は**、データベース ディメンションに従って構造化されます**。複数の Chat2Query データ アプリを同じデータベースに接続できますが、各 Chat2Query データ アプリは、リンクされている特定のデータベースの知識のみを使用できます。

Chat2Query データ アプリでは、 `/v3/knowledgeBases`エンドポイントを呼び出すことで、特定のデータベースのナレッジ ベースを作成できます。作成後は、将来のナレッジ管理用に`knowledge_base_id`取得されます。

以下は、このエンドポイントを呼び出すための一般的なコード例です。

> **ヒント：**
>
> エンドポイントの特定のコード例を取得するには、データ アプリの左側のペインでエンドポイント名をクリックし、 **[コード例の表示]**をクリックします。詳細については、 [エンドポイントのサンプルコードを取得する](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint)を参照してください。

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

各データベースのナレッジ ベースには、複数の種類のナレッジを含めることができます。ナレッジ ベースにナレッジを追加する前に、ユース ケースに最適なナレッジ タイプを選択する必要があります。

現在、Chat2Query ナレッジ ベースは次のナレッジ タイプをサポートしています。各タイプはさまざまなシナリオに合わせて特別に設計されており、独自のナレッジ構造を持っています。

-   [数ショットの例](#few-shot-example)
-   [条件説明書の説明](#term-sheet-explanation)
-   [命令](#instruction)

### 数ショットの例 {#few-shot-example}

少数のサンプルとは、Chat2Query に提供される Q&amp;A 学習サンプルのことで、サンプルの質問とそれに対応する回答が含まれています。これらのサンプルは、Chat2Query が新しいタスクをより効率的に処理するのに役立ちます。

> **注記：**
>
> 新しく追加された例の正確さを確認してください。例の品質は Chat2Query の学習の質に影響します。質問と回答が一致しないなどの質の悪い例は、新しいタスクでの Chat2Query のパフォーマンスを低下させる可能性があります。

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

Few-Shot の例を使用すると、次のようなさまざまなシナリオで Chat2Query のパフォーマンスを大幅に向上できます。

1.  **まれな質問や複雑な質問を扱う場合**: Chat2Query がまれな質問や複雑な質問に遭遇した場合、少数の例を追加すると理解が深まり、結果の精度が向上します。

2.  **特定の種類の質問に苦労している場合**: Chat2Query が頻繁に間違いを犯したり、特定の質問で困難が生じたりする場合、いくつかの例を追加すると、これらの質問でのパフォーマンスを向上させることができます。

### 条件説明書の説明 {#term-sheet-explanation}

用語集の説明とは、特定の用語または類似の用語のグループについての包括的な説明を指し、Chat2Query がこれらの用語の意味と使用法を理解するのに役立ちます。

> **注記：**
>
> 新しく追加された用語の説明の正確さを確認してください。説明の質は Chat2Query の学習の質に影響します。解釈が間違っていると Chat2Query の結果は改善されず、悪影響が生じる可能性もあります。

#### 知識構造 {#knowledge-structure}

各説明には、単一の用語、または類似の用語のリストとその詳細な説明が含まれます。

例えば：

```json
{
    "term": ["OSS"],
    "description": "OSS Insight is a powerful tool that provides online data analysis for users based on nearly 6 billion rows of GitHub event data."
}
```

#### ユースケース {#use-cases}

条件書の説明は主に、特に次のような状況で、Chat2Query によるユーザークエリの理解を向上させるために使用されます。

-   **業界固有の用語や頭字語の取り扱い**: クエリに、一般的には認識されていない可能性のある業界固有の用語や頭字語が含まれている場合、用語集の説明を使用すると、Chat2Query がこれらの用語の意味と使用法を理解するのに役立ちます。
-   **ユーザークエリの曖昧さへの対処**: クエリに曖昧な概念が含まれており混乱を招く場合、用語集の説明を使用すると、Chat2Query がこれらの曖昧さを明確にするのに役立ちます。
-   **さまざまな意味を持つ用語の取り扱い**: クエリにさまざまなコンテキストで異なる意味を持つ用語が含まれている場合、用語集の説明を使用すると、Chat2Query が正しい解釈を判断するのに役立ちます。

### 命令 {#instruction}

命令はテキスト コマンドの一部です。Chat2Query の動作をガイドまたは制御するために使用され、具体的には特定の要件または条件に従って SQL を生成する方法を指示します。

> **注記：**
>
> -   命令の長さは 512 文字に制限されます。
> -   Chat2Query が指示を効果的に理解して実行できるように、できるだけ明確で具体的な指示を提供するようにしてください。

#### 知識構造 {#knowledge-structure}

指示にはテキストコマンドのみが含まれます。

例えば：

```json
{
    "instruction": "If the task requires calculating the sequential growth rate, use the LAG function with the OVER clause in SQL"
}
```

#### ユースケース {#use-cases}

指示は、さまざまなシナリオで使用して、Chat2Query が要件に応じて出力するようにガイドできます。これには、以下が含まれますが、これらに限定されません。

-   **クエリ範囲の制限**: SQL で特定のテーブルまたは列のみを考慮する場合は、これを指定する命令を使用します。
-   **SQL 構造のガイド**: SQL 構造に特定の要件がある場合は、Chat2Query をガイドする指示を使用します。

## ステップ3. 新しく作成したナレッジベースに知識を追加する {#step-3-add-knowledge-to-the-newly-created-knowledge-base}

新しい知識を追加するには、 `/v3/knowledgeBases/{knowledge_base_id}/data`エンドポイントを呼び出すことができます。

### 数ショットの例の知識を追加する {#add-a-few-shot-example-type-of-knowledge}

たとえば、Chat2Query で特定の構造のテーブル内の行数の SQL ステートメントを生成する場合は、次のように`/v3/knowledgeBases/{knowledge_base_id}/data`呼び出して、いくつかの例のタイプの知識を追加できます。

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

上記のサンプル コードでは、 `"type": "few-shot"`少数ショットのサンプル知識タイプを表します。

### タームシートの説明タイプの知識を追加する {#add-a-term-sheet-explanation-type-of-knowledge}

たとえば、提供された説明を使用して Chat2Query に用語`OSS`の意味を理解してもらいたい場合は、次のように`/v3/knowledgeBases/{knowledge_base_id}/data`を呼び出して用語シートの説明タイプの知識を追加できます。

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

上記のコード例では、 `"type": "term-sheet"`条件シートの説明の知識タイプを表します。

### 指示タイプの知識を追加する {#add-an-instruction-type-of-knowledge}

たとえば、連続成長率の計算に関する質問を処理するときに、Chat2Query が SQL クエリで`OVER`句とともに`LAG`関数を一貫して使用するようにしたい場合は、次のように`/v3/knowledgeBases/{knowledge_base_id}/data`呼び出して、指示タイプの知識を追加できます。

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
