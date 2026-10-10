---
title: TAG_REFERENCES
summary: 指定したデータベースオブジェクトに割り当てられているすべてのタグを返します。
---

# TAG_REFERENCES

指定したデータベースオブジェクトに割り当てられているすべてのタグを返します。ガバナンスおよびコンプライアンスのためにタグの割り当てを監査する際に、この関数を使用します。

関連情報: [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

## 構文 {#syntax}

```sql
SELECT * FROM TAG_REFERENCES('<object_name>', '<domain>')
```

| パラメータ       | 説明                                                        |
|-----------------|--------------------------------------------------------------------|
| `object_name`   | オブジェクトの名前。テーブル/ビュー/ストリームの場合は、`db.name` 形式を使用します。プロシージャの場合は、型シグネチャ（例: `my_proc(INT)`）を含めます。 |
| `domain`        | オブジェクトタイプ: `DATABASE`, `TABLE`, `VIEW`, `STREAM`, `STAGE`, `CONNECTION`, `USER`, `ROLE`, `UDF`, または `PROCEDURE`。        |

## 出力カラム {#output-columns}

| カラム            | 型             | 説明                                 |
|-------------------|------------------|---------------------------------------------|
| `tag_name`        | String           | タグの名前                                              |
| `tag_value`       | String           | タグに割り当てられた値                                    |
| `object_database` | Nullable(String) | データベース名（STAGE、CONNECTION、USER、ROLE、UDF、PROCEDURE の場合は NULL） |
| `object_id`       | Nullable(UInt64) | オブジェクト ID（DATABASE、TABLE、VIEW の場合のみ non-NULL）          |
| `object_name`     | String           | オブジェクトの名前                                           |
| `domain`          | String           | オブジェクトタイプ                                                  |

## 例 {#examples}

### テーブル上のタグを照会する {#query-tags-on-a-table}

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod');
CREATE TAG owner;

CREATE TABLE default.users (id INT, name STRING);
ALTER TABLE default.users SET TAG env = 'prod', owner = 'team_a';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('default.users', 'TABLE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ prod      │ default         │ users       │ TABLE        │
│ owner    │ team_a    │ default         │ users       │ TABLE        │
└───────────────────────────────────────────────────────────────────────┘
```

### stage 上のタグを照会する {#query-tags-on-a-stage}

```sql
CREATE STAGE data_stage;
ALTER STAGE data_stage SET TAG env = 'staging', owner = 'data_team';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('data_stage', 'STAGE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ staging   │ NULL            │ data_stage  │ STAGE        │
│ owner    │ data_team │ NULL            │ data_stage  │ STAGE        │
└───────────────────────────────────────────────────────────────────────┘
```

### データベース上のタグを照会する {#query-tags-on-a-database}

```sql
ALTER DATABASE default SET TAG env = 'prod';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('default', 'DATABASE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ prod      │ default         │ default     │ DATABASE     │
└───────────────────────────────────────────────────────────────────────┘
```