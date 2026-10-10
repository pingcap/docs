---
title: データ保護ポリシー
summary: 保存された値を変更せずに機密情報を保護する、マスキングポリシーと行アクセスポリシーについて学びます。
---

# データ保護ポリシー

{{{ .lake }}} は、保存された値を変更することなく、クエリ実行時に機密データを保護します。

| Policy | 役割 |
|--------|----------------|
| [マスキングポリシー](/tidb-cloud-lake/guides/masking-policy.md) | カラム値を変換します — 権限のないユーザーにはマスクされたデータが表示されます |
| [行アクセス ポリシー](/tidb-cloud-lake/guides/row-access-policy.md) | 行全体をフィルタリングします — 権限のないユーザーには行自体が表示されません |

どちらもアプリケーションに対して透過的です。コード変更、追加のビュー、データコピーは不要です。

## 適切なポリシーを選ぶ {#choose-the-right-policy}

| シナリオ | 使用方法 |
|----------|-----|
| 行全体を隠す | Row Access |
| 行は残しつつ、カラムをマスクする | Masking |
| 同じカラムでもロールごとに異なる精度で表示する | Masking |
| マルチテナント / リージョン分離 | Row Access |
| ロールごとの時間帯制御 | Row Access |
| JSON / VARIANT 内のキーを隠す | Masking |
| 行の分離 + カラムのマスキング | 両方 (同じカラムには適用不可) |

例: phone、amount、region を持つ `orders` テーブル。

| 要件 | ポリシー |
|-------------|--------|
| サポート担当者は自分のリージョンのみ参照可能 | `region` に対する Row Access |
| アナリストには `138****1234` を表示 | `phone` に対する Masking |
| 管理者はすべて参照可能 | 両方のポリシーを通過するロール |

## どのように連携するか {#how-they-work-together}

```
Query
  → Row Access Policy filters rows
  → Masking Policy transforms surviving columns
  → Result returned
```

最初に行フィルタリングが実行されます。マスキングは、残った行に対してのみ適用されます。

| | マスキングポリシー | 行アクセスポリシー |
|---|---|---|
| 対象範囲 | カラム値 | 行全体 |
| 戻り値の型 | カラム型に一致 | BOOLEAN |
| 制限 | カラムごとに 1 つ | テーブルごとに 1 つ |
| 影響対象 | `SELECT` | `SELECT`, `UPDATE`, `DELETE`, `MERGE` |
| 保存データ / `INSERT` | 変更なし / フィルタなし | 変更なし / フィルタなし |

同じテーブルで両方を使用できます。ただし、同じ **column** を両方にバインドすることはできません。

```sql
-- Rows: sales only see their region
CREATE ROW ACCESS POLICY rap_region
AS (r STRING) RETURNS BOOLEAN ->
CASE
  WHEN is_role_in_session('admin') THEN true
  ELSE is_role_in_session(r)
END;

ALTER TABLE customers ADD ROW ACCESS POLICY rap_region ON (region);

-- Columns: non-HR see redacted SSN
CREATE MASKING POLICY mask_ssn
AS (val STRING) RETURNS STRING ->
CASE
  WHEN is_role_in_session('hr') THEN val
  ELSE '***-**-****'
END;

ALTER TABLE customers MODIFY COLUMN ssn SET MASKING POLICY mask_ssn;
```

## エンドツーエンド: 職務分離 {#end-to-end-separation-of-duties}

RBAC を両方のポリシーと組み合わせることで、作成者、適用者、閲覧者を分離したままにできます。

| Role | 役割 | 表示内容 |
|------|-----|------|
| `security_admin` | ポリシーを作成 / 所有する | テーブルの SELECT なし |
| `data_engineer` | テーブルを所有し、ポリシーをアタッチする | 全行、phone は生データ |
| `analyst_apac` | APAC を分析する | APAC の行、phone はマスク済み |
| `support_global` | グローバルサポート | 全行、phone は生データ |

```sql
-- account_admin: roles, users, CREATE privileges
CREATE ROLE security_admin;
CREATE ROLE data_engineer;
CREATE ROLE analyst_apac;
CREATE ROLE support_global;

CREATE USER sec_user IDENTIFIED BY 'password123';
CREATE USER eng_user IDENTIFIED BY 'password123';
CREATE USER analyst_user IDENTIFIED BY 'password123';
CREATE USER support_user IDENTIFIED BY 'password123';

GRANT ROLE security_admin TO USER sec_user;
GRANT ROLE data_engineer TO USER eng_user;
GRANT ROLE analyst_apac TO USER analyst_user;
GRANT ROLE support_global TO USER support_user;

GRANT CREATE DATABASE ON *.* TO ROLE data_engineer;
GRANT CREATE MASKING POLICY ON *.* TO ROLE security_admin;
GRANT CREATE ROW ACCESS POLICY ON *.* TO ROLE security_admin;
GRANT GRANT ON *.* TO ROLE security_admin;

-- data_engineer: table ownership
SET ROLE data_engineer;
CREATE DATABASE ecommerce;
CREATE TABLE ecommerce.orders (
  order_id INT,
  customer_name STRING,
  phone STRING,
  region STRING,
  amount DECIMAL(10,2),
  created_at TIMESTAMP
);
INSERT INTO ecommerce.orders VALUES
  (1, 'Alice',   '13812345678', 'APAC', 299.00, '2025-01-15 10:00:00'),
  (2, 'Bob',     '14987654321', 'EMEA', 150.00, '2025-01-16 11:00:00'),
  (3, 'Charlie', '13698765432', 'APAC', 520.00, '2025-01-17 09:30:00'),
  (4, 'Diana',   '15012349876', 'AMER',  89.00, '2025-01-18 14:00:00');

-- security_admin: create policies (auto OWNERSHIP)
SET ROLE security_admin;
SET enable_experimental_row_access_policy = 1;

CREATE MASKING POLICY mask_phone
AS (val STRING) RETURNS STRING ->
CASE
  WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN val
  ELSE CONCAT(SUBSTRING(val, 1, 3), '****', SUBSTRING(val, 8))
END;

CREATE ROW ACCESS POLICY rap_region
AS (r STRING) RETURNS BOOLEAN ->
CASE
  WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN true
  WHEN is_role_in_session('analyst_apac') AND r = 'APAC' THEN true
  ELSE false
END;

GRANT APPLY ON MASKING POLICY mask_phone TO ROLE data_engineer;
GRANT APPLY ON ROW ACCESS POLICY rap_region TO ROLE data_engineer;

-- data_engineer: attach (needs table ALTER + policy APPLY)
SET ROLE data_engineer;
SET enable_experimental_row_access_policy = 1;
ALTER TABLE ecommerce.orders MODIFY COLUMN phone SET MASKING POLICY mask_phone;
ALTER TABLE ecommerce.orders ADD ROW ACCESS POLICY rap_region ON (region);

-- account_admin: grant table access through roles
GRANT USAGE ON ecommerce.* TO ROLE analyst_apac;
GRANT USAGE ON ecommerce.* TO ROLE support_global;
GRANT SELECT ON ecommerce.orders TO ROLE analyst_apac;
GRANT SELECT ON ecommerce.orders TO ROLE support_global;
```

結果:

| 役割 | 行 | Phone |
|------|------|-------|
| `analyst_apac` | APAC のみ | マスク済み (`138****5678`) |
| `support_global` | すべて | 生データ |
| `security_admin` | — | 権限拒否 (no SELECT) |

```sql
SET ROLE analyst_apac;
SELECT * FROM ecommerce.orders;
-- Alice / Charlie only, phones masked

SET ROLE support_global;
SELECT * FROM ecommerce.orders;
-- all 4 rows, phones visible

SET ROLE security_admin;
SELECT * FROM ecommerce.orders;
-- ERROR: Permission denied
```

ロールを取り消すと、テーブル権限を変更しなくてもアクセス権が削除されます。

```sql
REVOKE ROLE analyst_apac FROM USER analyst_user;
```

**Rules of thumb:**

- ポリシーの作成 ≠ データのクエリ実行。アタッチには、ポリシーの `APPLY` とテーブルの `ALTER` の **両方** が必要です
- ユーザーではなくロールに権限を付与することを推奨します
- 作成者ロールには自動的に OWNERSHIP が付与されます
- `CREATE MASKING/ROW ACCESS POLICY` はユーザーではなくロールに付与されます
- `SHOW GRANTS ON MASKING POLICY ...`、`SHOW GRANTS ON ROW ACCESS POLICY ...`、および `POLICY_REFERENCES(...)` で監査できます

## 次のステップ {#next-steps}

- [マスキングポリシー](/tidb-cloud-lake/guides/masking-policy.md) — 条件付きマスキング、VARIANT キー
- [行アクセス ポリシー](/tidb-cloud-lake/guides/row-access-policy.md) — ベクトル / RAG の可視性、時間ウィンドウ、DML