---
title: Warehouse
summary: "{{{ .lake }}} の Warehouse 関連 SQL コマンド。"
---

# Warehouse

{{{ .lake }}} の Warehouse 関連 SQL コマンド。

## 一般ルール {#general-rules}

- **Warehouse の命名**: 3～63 文字で、使用できるのは `A-Z`、`a-z`、`0-9`、`-` のみです。
- **文字列と識別子**: スペースを含まない場合、裸の識別子では引用符を省略できます。それ以外の場合は、単一引用符で囲みます。文法上はキーワードや数値/ブールリテラルを名前として使用できますが、実行時の検証は引き続き適用されます。
- **数値パラメータ**: `nullable_unsigned_number` / `nullable_signed_number` は整数または `NULL` を受け付けます。`NULL` を指定すると値がリセットされます（たとえば、`AUTO_SUSPEND = NULL` は `0` と同じです）。
- **時間パラメータ**: `QUERY_HISTORY` は `YYYY-MM-DD HH:MM:SS`（UTC または明示的なタイムゾーン）を使用します。小数秒が省略された場合は、秒単位の値として解釈されます。
- **ブールパラメータ**: `TRUE`/`FALSE` のみ受け付けます。
- **`WITH` キーワード**: オプションリスト全体の前、または各オプションの前に指定できます。オプションは空白で区切られ、カンマは文法の一部ではありません。

## Warehouse 管理 {#warehouse-management}

タグは、AWS リソースタグと同様に、Warehouse の分類や整理に役立つキーと値のペアです。一般的に、次の用途で使用されます。

- **コスト配分**: チーム、プロジェクト、またはコストセンターごとに Warehouse のコストを追跡する
- **環境の識別**: Warehouse を dev、staging、または 本番 としてマークする
- **チーム所有権**: どのチームが Warehouse を所有または管理しているかを識別する
- **カスタムメタデータ**: 組織上の目的のために任意のメタデータを追加する

タグのキーと値は任意の文字列です（スペースや特殊文字を含む場合は引用符で囲みます）。タグは次のように扱えます。

- `WITH TAG (key = 'value', ...)` を使用して Warehouse 作成時に追加する
- `ALTER WAREHOUSE ... SET TAG key = 'value'` を使用して後から更新または追加する
- `ALTER WAREHOUSE ... UNSET TAG key` を使用して削除する

タグは API レスポンスで返され、`SHOW WAREHOUSES` でも確認できます。

**タグの制限:**

- 1 つの Warehouse あたり最大 10 個のタグ
- タグ名（キー）の最大長: 128 文字
- タグ値の最大長: 256 文字

## サポートされるステートメント {#supported-statements}

| 文 | 目的                         | 注記                                                       |
| ------------------ | ---------------------------- | ---------------------------------------------------------- |
| `CREATE WAREHOUSE` | Warehouse を作成             | `IF NOT EXISTS` とオプションリストをサポート               |
| `ALTER WAREHOUSE`  | 一時停止/再開/変更/名前変更  | `SUSPEND`/`RESUME`、`SET <options>`、または `RENAME TO <name>` |
| `DROP WAREHOUSE`   | Warehouse を削除             | `IF EXISTS` は省略可能                                     |
| `USE WAREHOUSE`    | 現在のセッションにバインド   | 存在確認のみを行います                                     |
| `SHOW WAREHOUSES`  | Warehouse を一覧表示         | `LIKE` フィルタは省略可能                                  |
| `QUERY_HISTORY`    | クエリログを確認             | Warehouse、時間範囲、件数制限でフィルタ可能                |

## Warehouse SQL コマンド {#warehouse-sql-commands}

| コマンド                                 | 説明                                       |
| --------------------------------------- | ------------------------------------------------- |
| [CREATE WAREHOUSE](/tidb-cloud-lake/sql/create-warehouse.md) | 新しい Warehouse を作成します                     |
| [USE WAREHOUSE](/tidb-cloud-lake/sql/use-warehouse.md)       | セッションの現在の Warehouse を設定します         |
| [SHOW WAREHOUSES](/tidb-cloud-lake/sql/show-warehouses.md)   | オプションのフィルタ付きですべての Warehouse を一覧表示します |
| [ALTER WAREHOUSE](/tidb-cloud-lake/sql/alter-warehouse.md)   | Warehouse の一時停止、再開、または設定変更を行います |
| [ALTER WAREHOUSE ASSIGN NODES](/tidb-cloud-lake/sql/alter-warehouse-assign-nodes.md) | Warehouse クラスターにノードを割り当てます |
| [ALTER WAREHOUSE UNASSIGN NODES](/tidb-cloud-lake/sql/alter-warehouse-unassign-nodes.md) | Warehouse クラスターから割り当て済みノードを削除します |
| [DROP WAREHOUSE](/tidb-cloud-lake/sql/drop-warehouse.md)     | Warehouse を削除します                             |
| [QUERY_HISTORY](/tidb-cloud-lake/sql/query-history.md)       | Warehouse のクエリログを確認します                 |

> **Note:**
>
> Warehouse は、{{{ .lake }}} でクエリを実行するために使用されるコンピュートリソースを表します。