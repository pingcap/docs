---
title: マスキングポリシー
summary: マスキングポリシーは、クエリ実行時にカラム値を動的に変換することで機密データを保護します。これにより、機密情報へのロールベースのアクセス制御が可能になり、権限のあるユーザーには実データが表示され、それ以外のユーザーにはマスクされた値が表示されます。
---

# マスキングポリシー

マスキングポリシーは、クエリ時にカラム値を変換します。権限のあるロールには実データが表示され、それ以外にはマスクされた値が表示されます。保存されているデータ自体は変更されません。

カラムをマスクするのではなく行全体を非表示にしたい場合は、[行アクセス ポリシー](/tidb-cloud-lake/guides/row-access-policy.md)を使用してください。

## 使用する場面 {#when-to-use}

- カスタマーサポート — 担当者は注文を確認でき、ID は `3201**********1234` のように表示される
- 分析 — 集計を壊さずに email を `***@***.com` として表示する
- VARIANT ログ — 非管理者に対して `secret_key` / `token` のような JSON キーを隠す
- 部分的なマスキング — 確認用にカード番号の下 4 桁だけを表示する

## クイックスタート {#quick-start}

```sql
CREATE TABLE user_info (id INT, email STRING NOT NULL);

CREATE MASKING POLICY email_mask
AS (val STRING)
RETURNS STRING ->
CASE
  WHEN is_role_in_session('managers') THEN val
  ELSE '*********'
END;

ALTER TABLE user_info MODIFY COLUMN email SET MASKING POLICY email_mask;

INSERT INTO user_info VALUES (1, 'user@example.com');
SELECT * FROM user_info;
```

```
id | email
---|----------
 1 | *********
```

**仕組み**

- クエリ時のみ — `SELECT` はマスクされるが、`INSERT` / `UPDATE` / `DELETE` では実際の値が使われる
- カラム単位 — 1 つのカラムにつき 1 つのポリシー。テーブルをまたいで再利用可能
- `current_role()` より `is_role_in_session()` を優先することで、ユーザーが `SET ROLE` で回避できないようにする

## 例 {#examples}

### 条件付きマスキング (`USING`) {#conditional-masking-using}

別のカラムに基づいてマスクします。

```sql
CREATE MASKING POLICY vip_mask
AS (val STRING, is_vip BOOLEAN)
RETURNS STRING ->
CASE
  WHEN is_vip = true THEN val
  ELSE '*********'
END;

ALTER TABLE user_info
MODIFY COLUMN email SET MASKING POLICY vip_mask USING (email, is_vip);

INSERT INTO user_info (id, email, is_vip) VALUES
  (1, 'vip@example.com', true),
  (2, 'normal@example.com', false);

SELECT * FROM user_info;
```

```
id | email           | is_vip
---|-----------------|-------
 1 | vip@example.com | true
 2 | *********       | false
```

ポリシー本体で必要な場合にのみ、カラムを `USING` に追加してください。

### VARIANT サブフィールドのマスキング {#variant-sub-field-masking}

`object_delete` を使って特定の JSON キーを隠します。すべてのアクセスパスでマスクが適用されます（添字、パス関数、cast、`json_object_keys`）。

```sql
CREATE TABLE events (id INT, data VARIANT);

INSERT INTO events VALUES
  (1, parse_json('{"name":"alice","content":"secret data","secret_key":"sk_123","age":30}')),
  (2, parse_json('{"name":"bob","content":"private info","secret_key":"sk_456","age":25}'));

CREATE ROLE data_admin;
CREATE ROLE data_reader;

CREATE MASKING POLICY mask_variant_sensitive
AS (val VARIANT) RETURNS VARIANT ->
CASE
  WHEN is_role_in_session('data_admin') OR is_role_in_session('account_admin') THEN val
  ELSE object_delete(val, 'content', 'secret_key')
END;

ALTER TABLE events MODIFY COLUMN data SET MASKING POLICY mask_variant_sensitive;

GRANT SELECT ON default.events TO ROLE data_admin;
GRANT SELECT ON default.events TO ROLE data_reader;
```

| `data_admin` として | `data_reader` として |
|-----------------|------------------|
| 完全な JSON | `content` / `secret_key` が削除される |

```sql
SET ROLE data_reader;

SELECT data FROM events;
-- {"age":30,"name":"alice"}

SELECT data['content'] FROM events;                 -- NULL
SELECT data['name'] FROM events;                    -- "alice"
SELECT json_path_query_first(data, '$.content');    -- NULL
SELECT data::STRING FROM events;                    -- {"age":30,"name":"alice"}
SELECT json_object_keys(data) FROM events;          -- ["age","name"]
SELECT * FROM events WHERE data['content'] IS NOT NULL;
-- empty
```

ネストされたキーの場合:

```sql
ELSE delete_by_keypath(val, 'nested:secret')
```

## 読み取り / 書き込みの動作 {#read-write-behavior}

| 操作 | 効果 |
|-----------|--------|
| `SELECT` | マスクされた値 |
| `INSERT` / `UPDATE` / `DELETE` | 実際の値（書き込みはマスクされない） |

```sql
INSERT INTO user_info VALUES (2, 'admin@example.com');  -- stores real email
SELECT * FROM user_info WHERE id = 2;                   -- returns *********
```

## ポリシーの管理 {#manage-policies}

```sql
DESCRIBE MASKING POLICY email_mask;

ALTER TABLE user_info MODIFY COLUMN email UNSET MASKING POLICY;
DROP MASKING POLICY IF EXISTS email_mask;
```

`DROP MASKING POLICY` の前に、すべてのカラムとのバインドを解除してください。バインドは `POLICY_REFERENCES(POLICY_NAME => 'email_mask')` で確認できます。

## マスキングと行アクセスの比較 {#masking-vs-row-access}

| | マスキングポリシー | 行アクセスポリシー |
|---|---|---|
| 対象範囲 | カラム値 | 行全体 |
| 戻り値の型 | カラム型と一致する必要がある | 常に BOOLEAN |
| テーブルごと | カラムごとに 1 つ | テーブルごとに 1 つ |
| 影響対象 | `SELECT` | `SELECT`, `UPDATE`, `DELETE`, `MERGE` |

1 つのカラムに両方のポリシーを同時に設定することはできません。行は表示したままにしたい場合はマスキングを使用し、行自体を見えなくしたい場合は行アクセスを使用してください。

## 制限事項 {#limits}

- 1 つのカラムにつき 1 つのマスキングポリシー
- 戻り値の型はカラム型と一致している必要がある
- カラムを変更または削除する前にポリシーを解除する必要がある
- いずれかのテーブルから参照されているポリシーは削除できない
- `CREATE OR REPLACE MASKING POLICY` はない — 削除して再作成する
- 一時テーブル、ビュー、ストリームではサポートされない
- ポリシー名は、マスキングポリシーと行アクセスポリシー全体でグローバルに一意である必要がある
- ポリシー引数名は作成時に小文字化される

## ベストプラクティス {#best-practices}

1. `current_role()` より `is_role_in_session()` を優先してください。
2. `USING` は最小限に保ち、ポリシー本体で必要なカラムだけを含めてください。
3. アプリケーションが `LENGTH` / `LIKE` を呼び出す場合は、型に整合したプレースホルダー（email なら `***@***.com`）を返してください。
4. VARIANT では、値全体をマスクするのではなく `object_delete` / `delete_by_keypath` を使用してください。
5. 削除前にバインドを解除し、適用後は制限付きロールで確認してください。

## 権限と参照 {#privileges-references}

- ポリシーを作成するには、`*.*` に対する `CREATE MASKING POLICY` が必要です（作成者には OWNERSHIP が付与されます）
- アタッチ/デタッチするには、グローバル `APPLY MASKING POLICY` または `APPLY ON MASKING POLICY <name>` が必要です
- 監査: `SHOW GRANTS ON MASKING POLICY <name>`

以下も参照してください。

- [User & Role](/tidb-cloud-lake/sql/user-role.md)
- [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#column-operations)
- [Masking Policy コマンド](/tidb-cloud-lake/sql/masking-policy-sql.md)
- [行アクセス ポリシー](/tidb-cloud-lake/guides/row-access-policy.md)