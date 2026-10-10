---
title: SHOW SETTINGS
summary: "{{{ .lake }}} には、{{{ .lake }}} の動作を制御するためのさまざまなシステム設定があります。このコマンドは、利用可能なシステム設定の現在値とデフォルト値、および Setting Levels を表示します。設定を更新するには、SET または UNSET コマンドを使用します。"
---

# SHOW SETTINGS

{{{ .lake }}} には、{{{ .lake }}} の動作を制御するためのさまざまなシステム設定があります。このコマンドは、利用可能なシステム設定の現在値とデフォルト値、および [Setting Levels](#setting-levels) を表示します。設定を更新するには、[SET](/tidb-cloud-lake/sql/set.md) または [UNSET](/tidb-cloud-lake/sql/unset.md) コマンドを使用します。

- {{{ .lake }}} の一部の動作はシステム設定では変更できないため、{{{ .lake }}} を使用する際に考慮する必要があります。たとえば、次のとおりです。
    - {{{ .lake }}} は文字列を UTF-8 文字セットにエンコードします。
    - {{{ .lake }}} は配列に対して 1 始まりの番号付け規則を使用します。
- {{{ .lake }}} はシステム設定をシステムテーブル [system.settings](/tidb-cloud-lake/sql/system-settings.md) に保存します。

## 構文 {#syntax}

```sql
SHOW SETTINGS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## Setting Levels {#setting-levels}

各 {{{ .lake }}} 設定には、Global、Default、または Session のいずれかのレベルがあります。次の表は、各レベルの違いを示しています。

|   レベル    |   説明                                                                                                                                                                                                                                                              |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   Global   |   このレベルの設定はメタサービスに書き込まれ、同じテナント内のすべてのクラスターに影響します。このレベルでの変更はグローバルに影響し、複数のクラスターで共有されるデータベース環境全体に適用されます。                                                |
|   Default  |   このレベルの設定は、個々のクエリインスタンスに対するサービスのデフォルト設定です。このレベルでの変更は、デフォルトが適用されるクエリインスタンスにのみ影響します。  |
|   Session  |   このレベルの設定は、単一のリクエストまたはセッションに限定されます。最も狭いスコープを持ち、進行中の特定のセッションまたはリクエストにのみ適用されるため、セッション単位で設定をカスタマイズできます。                                       |

## 例 {#examples}

> **Note:**
>
> {{{ .lake }}} ではシステム設定が随時更新されるため、この例には最新の結果が表示されていない場合があります。{{{ .lake }}} の最新のシステム設定を確認するには、{{{ .lake }}} インスタンス内で `SHOW SETTINGS;` を実行してください。

```sql
SHOW SETTINGS LIMIT 5;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                     name                    │  value │ default │   range  │  level  │                                                                     description                                                                    │  type  │
├─────────────────────────────────────────────┼────────┼─────────┼──────────┼─────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┤
│ acquire_lock_timeout                        │ 15     │ 15      │ None     │ DEFAULT │ Sets the maximum timeout in seconds for acquire a lock.                                                                                            │ UInt64 │
│ aggregate_spilling_bytes_threshold_per_proc │ 0      │ 0       │ None     │ DEFAULT │ Sets the maximum amount of memory in bytes that an aggregator can use before spilling data to storage during query execution.                      │ UInt64 │
│ aggregate_spilling_memory_ratio             │ 0      │ 0       │ [0, 100] │ DEFAULT │ Sets the maximum memory ratio in bytes that an aggregator can use before spilling data to storage during query execution.                          │ UInt64 │
│ auto_compaction_imperfect_blocks_threshold  │ 50     │ 50      │ None     │ DEFAULT │ Threshold for triggering auto compaction. This occurs when the number of imperfect blocks in a snapshot exceeds this value after write operations. │ UInt64 │
│ collation                                   │ utf8   │ utf8    │ ["utf8"] │ DEFAULT │ Sets the character collation. Available values include "utf8".                                                                                     │ String │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```