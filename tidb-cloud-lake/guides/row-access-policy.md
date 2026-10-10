---
title: 行アクセス ポリシー
summary: 行アクセス ポリシーは、クエリ時にテーブルの行をフィルタリングすることでデータを保護します。ブール述語を一度だけ定義してテーブルに関連付けることで、ユーザーにはポリシーを満たす行だけが表示されます。
---

# 行アクセス ポリシー

行アクセス ポリシーは、クエリ時にテーブルの行をフィルタリングします。ブール述語を一度定義してテーブルに関連付けると、ユーザーにはそのポリシーを通過した行だけが表示されます。

行を非表示にするのではなく、カラムレベルでマスキングしたい場合は、[マスキングポリシー](/tidb-cloud-lake/guides/masking-policy.md) を使用してください。

> **Note:**
>
> これは**実験的**機能です。`SET enable_experimental_row_access_policy = 1`（セッション）または `SET GLOBAL enable_experimental_row_access_policy = 1`（アカウント）で有効にします。

## 使用する場面 {#when-to-use}

- マルチテナント分離 — 各テナントは自分の行だけを参照可能
- リージョン / 部門の分離 — 営業は自分の担当領域だけを参照可能
- 時間ウィンドウ制御 — アラートは 1 日分をスキャンし、オフライン分析は 7 日分をスキャン可能
- ベクトル / RAG 検索 — 共有ナレッジベースで、ロールベースのドキュメント可視性を実現
- コンプライアンス — 監査担当者は承認済みの時間範囲またはサブセットだけを参照可能

## クイックスタート {#quick-start}

```sql
SET enable_experimental_row_access_policy = 1;

CREATE TABLE employees (
  id INT,
  name STRING,
  department STRING
);

INSERT INTO employees VALUES
  (1, 'Alice', 'Engineering'),
  (2, 'Bob', 'Sales'),
  (3, 'Charlie', 'Engineering');

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('admin') THEN true
  WHEN dept = 'Engineering' THEN true
  ELSE false
END;

-- ON (column) maps to the policy argument by position
ALTER TABLE employees ADD ROW ACCESS POLICY rap_engineering ON (department);

SELECT id, name, department FROM employees ORDER BY id;
```

```
id | name    | department
---|---------|-------------
 1 | Alice   | Engineering
 3 | Charlie | Engineering
```

**仕組み**

- クエリ時のみ適用 — 保存済みデータは変更されません
- テーブルごとに 1 つのポリシー。引数は `ON (...)` 内で位置に基づいてカラムにマッピングされます
- ユーザーが `SET ROLE` で回避できないように、`current_role()` より `IS_ROLE_IN_SESSION()` を優先してください

複数カラムのポリシー:

```sql
CREATE ROW ACCESS POLICY rap_region_dept
AS (region STRING, dept STRING)
RETURNS BOOLEAN ->
  region = 'APAC' AND dept = 'Engineering';

ALTER TABLE employees
ADD ROW ACCESS POLICY rap_region_dept ON (office_region, department);
```

## 例 {#examples}

### ベクトル / RAG ドキュメント可視性 {#vector-rag-document-visibility}

共有ナレッジベース テーブルとベクトル検索を組み合わせた例です。可視性を一度設定すれば、検索 SQL にドキュメント ID フィルタを含める必要はありません。[ベクトル検索](/tidb-cloud-lake/guides/vector-search-guide.md) を参照してください。

| ロール | 参照可能な内容 |
|------|------|
| `admin` | すべての行 |
| `sales` | `dept = 'sales'` + public |
| `finance` | `dept = 'finance'` + public |

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROLE IF NOT EXISTS admin;
CREATE ROLE IF NOT EXISTS sales;
CREATE ROLE IF NOT EXISTS finance;

CREATE TABLE knowledge_docs (
  doc_id    BIGINT,
  title     STRING,
  dept      STRING,
  is_public BOOLEAN,
  embedding VECTOR(4),
  VECTOR INDEX idx_emb(embedding) distance='cosine'
);

INSERT INTO knowledge_docs VALUES
  (1, 'Sales contract template',  'sales',   false, [0.90, 0.10, 0.05, 0.05]),
  (2, 'Q2 financial draft',       'finance', false, [0.10, 0.90, 0.05, 0.05]),
  (3, 'Public company handbook',  'hr',      true,  [0.20, 0.20, 0.90, 0.10]),
  (4, 'Competitor pricing notes', 'sales',   false, [0.85, 0.15, 0.10, 0.05]),
  (5, 'Internal audit checklist', 'finance', false, [0.15, 0.85, 0.10, 0.05]);

CREATE ROW ACCESS POLICY rap_knowledge_docs
AS (dept STRING, is_public BOOLEAN)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('admin') THEN true
  WHEN is_public THEN true
  WHEN IS_ROLE_IN_SESSION('sales') AND dept = 'sales' THEN true
  WHEN IS_ROLE_IN_SESSION('finance') AND dept = 'finance' THEN true
  ELSE false
END;

ALTER TABLE knowledge_docs
ADD ROW ACCESS POLICY rap_knowledge_docs ON (dept, is_public);

GRANT SELECT ON knowledge_docs TO ROLE sales;
GRANT SELECT ON knowledge_docs TO ROLE finance;

-- Activate one role for the session, then run the same search SQL
SET ROLE sales;
SET SECONDARY ROLES NONE;

SELECT doc_id, title,
       round(cosine_distance(embedding, [0.88, 0.12, 0.08, 0.05]::VECTOR(4)), 4) AS dist
FROM knowledge_docs
ORDER BY dist
LIMIT 10;
```

| `sales` の場合 | `finance` の場合 (`SET ROLE finance`) |
|------------|-------------------------------------|
| 1 Sales contract template `0.0009` | 3 Public company handbook `0.6731` |
| 4 Competitor pricing notes `0.0011` | 5 Internal audit checklist `0.6855` |
| 3 Public company handbook `0.6731` | 2 Q2 financial draft `0.7504` |

### ロールによる時間範囲アクセス {#time-range-access-by-role}

サービスアカウントごとに、スキャンできる履歴ウィンドウが異なる場合があります。

| アカウント | ロール | 期間 |
|---------|-------|--------|
| `svc_realtime_alert` | `rap_role_1_day` | 直近 1 日 |
| `svc_offline_analysis` | `rap_role_1_day`, `rap_role_7_day` | 最大 7 日 |

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROLE rap_role_7_day;
CREATE ROLE rap_role_1_day;

-- CASE is top-down: put the wider window first
CREATE ROW ACCESS POLICY rap_time_range
AS (start_time TIMESTAMP)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('rap_role_7_day') THEN
    start_time >= now() - INTERVAL 7 DAY
  WHEN IS_ROLE_IN_SESSION('rap_role_1_day') THEN
    start_time >= now() - INTERVAL 1 DAY
  ELSE false
END;

CREATE TABLE metrics(id INT, start_time TIMESTAMP);
INSERT INTO metrics VALUES
  (1, now() - INTERVAL 15 DAY),
  (2, now() - INTERVAL 5 DAY),
  (3, now() - INTERVAL 12 HOUR),
  (4, now() - INTERVAL 1 HOUR),
  (5, now() - INTERVAL 8 DAY);

ALTER TABLE metrics ADD ROW ACCESS POLICY rap_time_range ON (start_time);

GRANT ROLE rap_role_1_day TO USER svc_realtime_alert;
GRANT ROLE rap_role_1_day TO USER svc_offline_analysis;
GRANT ROLE rap_role_7_day TO USER svc_offline_analysis;

SELECT id, start_time FROM metrics ORDER BY id;
```

ログイン後、{{{ .lake }}} は付与されたすべてのロールを有効化します（`SECONDARY ROLES ALL`）。

| セッション | 表示される行 |
|---------|--------------|
| `svc_realtime_alert` (1 日のみ) | 直近 1 日 |
| `svc_offline_analysis` (両方のロール) | デフォルトで直近 7 日 |

オフラインアカウントを 1 日に絞り込むには、次を実行します。

```sql
SET ROLE rap_role_1_day;
SET SECONDARY ROLES NONE;
SELECT id, start_time FROM metrics ORDER BY id;
```

再び広げるには、次を実行します。

```sql
SET ROLE rap_role_7_day;
SELECT id, start_time FROM metrics ORDER BY id;
```

アカウントが有効化できるのは、自身に付与されたロールのみです。`svc_realtime_alert` は `SET ROLE rap_role_7_day` を実行できません。

## 読み取りと書き込みの動作 {#read-and-write-behavior}

| 操作 | 効果 |
|-----------|--------|
| `SELECT` | ポリシーで可視な行のみ |
| `UPDATE` / `DELETE` / `MERGE` | 可視な対象行にのみマッチし、変更される |
| `INSERT` | フィルタリングされない — 現時点で不可視でも行は保存される |

保存されているすべての行を確認するには、ポリシーを通過できるロールを使用するか、一時的にポリシーをデタッチします。

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_sales_only
AS (dept STRING) RETURNS BOOLEAN -> dept = 'sales';

CREATE TABLE orders(id INT, dept STRING, amount INT);
ALTER TABLE orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

INSERT INTO orders VALUES (1, 'sales', 100), (2, 'eng', 200), (3, 'sales', 300);

SELECT * FROM orders ORDER BY id;
-- 1 sales 100
-- 3 sales 300

UPDATE orders SET amount = amount + 10;
DELETE FROM orders WHERE dept = 'eng';   -- no-op: eng rows are invisible
DELETE FROM orders WHERE id = 1;         -- deletes visible row 1

-- MERGE only matches visible targets
CREATE TABLE src(id INT, new_amount INT);
INSERT INTO src VALUES (2, 777), (3, 888);

MERGE INTO orders AS t
USING src AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.amount = s.new_amount;

-- Detach to inspect storage
ALTER TABLE orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT * FROM orders ORDER BY id;
-- 2 eng 200   (never updated)
-- 3 sales 888 (merged)
```

## ポリシーの管理 {#manage-policies}

```sql
DESC ROW ACCESS POLICY rap_engineering;

ALTER TABLE employees DROP ROW ACCESS POLICY rap_engineering;
DROP ROW ACCESS POLICY rap_engineering;

ALTER TABLE employees DROP ALL ROW ACCESS POLICIES;
```

`DROP ROW ACCESS POLICY` の前にデタッチしてください。保護対象カラムを変更する前にも、削除またはデタッチが必要です。

## 制限事項 {#limits}

- テーブルごとに 1 つの row access policy
- 通常テーブルのみ対応 — ビュー、ストリーム、一時テーブル、ICE データベースは非対応
- カラムごとに 1 つの security policy（masking **または** row access のいずれか一方で、両方は不可）
- `CREATE OR REPLACE` / `ALTER` policy は非対応 — 削除して再作成が必要
- policy 名は masking policy と row access policy の間でグローバルに一意
- policy の引数名は作成時に小文字化される

## ベストプラクティス {#best-practices}

1. `current_role()` より `IS_ROLE_IN_SESSION()` を優先してください。
2. `CASE` の分岐は、最も広いもの → 最も狭いものの順に並べてください（admin を先頭）。
3. policy が lookup table を参照する場合は、保護対象テーブルと同じデータベースに配置してください。
4. アタッチ後は複数のロールで検証してください — admin、制限付き、非一致。
5. 全データの確認には、繰り返しデタッチ/アタッチするより、権限のあるロールを使うことを推奨します。

## 権限と参照情報 {#privileges-references}

- policy を作成するには `*.*` に対する `CREATE ROW ACCESS POLICY` が必要（作成者は OWNERSHIP を取得）
- アタッチ/デタッチするには、テーブルに対する `ALTER` と `APPLY ROW ACCESS POLICY`（グローバル）または `APPLY ON ROW ACCESS POLICY <name>` が必要
- 監査: `SHOW GRANTS ON ROW ACCESS POLICY <name>`
- 使用状況: [`POLICY_REFERENCES`](/tidb-cloud-lake/sql/policy-references.md)

以下も参照してください。

- [User & Role](/tidb-cloud-lake/sql/user-role.md)
- [CREATE ROW ACCESS POLICY](/tidb-cloud-lake/sql/create-row-access-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#row-access-policy-operations)
- [Row Access Policy コマンド](/tidb-cloud-lake/sql/row-access-policy-overview.md)