---
title: {{{ .starter }}} と Essential のための Project API 移行ガイド
summary: TiDB Cloud が TiDB X インスタンス向けに個別のプロジェクトタイプを導入した後も、既存の v1beta API 呼び出しを動作させ続けるために必要な最小限の変更について説明します。
---

# {{{ .starter }}} と Essential のための Project API 移行ガイド

2026 年 4 月 15 日より、TiDB Cloud はリソースタイプごとに個別のプロジェクトタイプを導入します。{{{ .starter }}} と Essential インスタンスについては、TiDB X プロジェクト内、または組織レベルで管理できるようになります。詳細は、[TiDB X Instances の Project Migration FAQ](/tidb-cloud/tidbx-instance-move-faq.md) を参照してください。

このガイドは、既存の `v1beta` 呼び出しの大部分を引き続き動作させつつ、{{{ .starter }}} と Essential インスタンスに対するプロジェクト検索およびクラスタ作成にのみ最小限の変更を加えたい API 呼び出し元を対象としています。

これらのプロジェクトモデルの変更により、以下の API 変更に注意してください。

- {{{ .starter }}} と Essential インスタンスの `project_id` 値は、TiDB Cloud コンソールでこれらのインスタンスをプロジェクト間で移動できるため、**変更される可能性があります**。`project_id` の値をハードコードしないでください。
- プロジェクトのレスポンスには `type` フィールドが含まれるようになりました。指定可能な値については、[Project type values](#project-type-values) を参照してください。

## Project API の変更 {#project-api-changes}

### GET /api/v1beta/projects {#get-api-v1beta-projects}

`GET /api/v1beta/projects` は、各プロジェクトに対して `type` フィールドを返すようになりました。

#### Project type values {#project-type-values}

| Value | Description |
|---|---|
| `dedicated` | TiDB Cloud Dedicated クラスタのみを含むプロジェクトです。 |
| `tidbx` | {{{ .starter }}} や Essential など、TiDB X インスタンスのみを含むプロジェクトです。 |
| `tidbx_virtual` | どのプロジェクトにも割り当てられていない TiDB X インスタンス用の、デフォルトの組織レベルプロジェクトです。各組織には 1 つの `tidbx_virtual` プロジェクトのみ存在します。 |

> **Note:**
>
> {{{ .starter }}} と Essential インスタンスは、どちらも `tidbx` プロジェクトタイプを使用します。

**アプリケーションがプロジェクトレスポンスから `id` と `name` フィールドのみを読み取る場合**、変更は不要です。

**アプリケーションでプロジェクトタイプを区別する必要がある場合**（たとえば、dedicated プロジェクト、TiDB X プロジェクト、または TiDB X 仮想プロジェクトをフィルタリングする場合）は、`type` フィールドの読み取りを開始してください。

### POST /api/v1beta/projects {#post-api-v1beta-projects}

`POST /api/v1beta/projects` を使用してプロジェクトを作成する場合は、以下に注意してください。

- プロジェクト作成時に有効な `type` 値は `dedicated` と `tidbx` のみです。
- `type` を省略すると、API はデフォルトで `dedicated` プロジェクトを作成します。

## 既存インスタンスの project ID を取得する方法 {#how-to-get-a-project-id-for-an-existing-instance}

すでに {{{ .starter }}} または Essential インスタンスを所有しており、現在の `project_id` のみが必要な場合は、その値をハードコードする代わりに、以下の方法を使用してください。

1. クラスタ詳細エンドポイントを呼び出します。

    ```http
    GET https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}
    ```

2. レスポンスから `labels["tidb.cloud/project"]` を読み取ります。

    ```json
    {
      "clusterId": "1048576",
      "labels": {
        "tidb.cloud/project": "2293484"
      }
    }
    ```

3. 取得した `project_id` を既存の `v1beta` エンドポイントで使用します。例:

    - `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
    - `DELETE /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
    - `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`
    - `POST /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`

> **Note:**
>
> - この方法は、`POST /api/v1beta/projects/{project_id}/clusters` を使用したクラスタ作成には適用されません。
> - `v1beta` で作成できるのは {{{ .starter }}} インスタンスと TiDB Cloud Dedicated クラスタのみです。{{{ .essential }}} インスタンスを作成するには、代わりに `v1beta1` API を使用してください。詳細は、[TiDB Cloud API documentation](https://docs.pingcap.com/api/) を参照してください。 
> - 新しい {{{ .starter }}} または Essential インスタンスを作成する場合は、クラスタ作成ワークフローが `tidbx` プロジェクトを対象としていることを確認してください。

## 必要な変更の概要 {#summary-of-required-changes}

| Scenario | Action required |
|---|---|
| プロジェクトレスポンスから `id` と `name` のみを読み取る | 変更は不要です。 |
| {{{ .starter }}} または Essential インスタンスの `project_id` をハードコードしている | ハードコードした値を、`labels["tidb.cloud/project"]` を使用した動的な取得に置き換えてください。 |
| プロジェクトを作成し、TiDB X インスタンスを対象にする必要がある | `POST /api/v1beta/projects` のリクエストボディに `"type": "tidbx"` を渡してください。 |
| タイプでプロジェクトをフィルタリングしている | `GET /api/v1beta/projects` のレスポンスから `type` フィールドを読み取るようにしてください。 |