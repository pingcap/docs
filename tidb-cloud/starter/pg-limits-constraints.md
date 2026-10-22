---
title: PostgreSQL の制限事項と制約
summary: PostgreSQL 互換の TiDB Cloud Starter の SQL エンジンにおける制限事項と制約について説明します。
---

# PostgreSQL の制限事項と制約

このドキュメントでは、PostgreSQL 互換の {{{ .starter }}} に適用される SQL エンジンの制限事項と制約について説明します。

> **Note:**
>
> PostgreSQL 互換の {{{ .starter }}} は現在パブリックプレビューです。制限事項と制約は、プレビュー期間中に変更される可能性があります。

このページでは、SQL エンジンの動作に焦点を当てています。PostgreSQL 互換の {{{ .starter }}} の月間無料クォータおよび製品レベルの制限については、[TiDB Cloud Starter プランのドキュメント](/tidb-cloud/select-cluster-tier.md#postgresql-compatible-starter)を参照してください。

## エンジンの制限 {#engine-limits}

以下の制限が適用されます。

| リソース | 制限 |
| --- | --- |
| ステートメントタイムアウト | デフォルトで 60 秒 |
| アイドル状態のトランザクションタイムアウト | デフォルトで 600 秒（10 分） |
| ビューのネスト深度 | 64 レベル |
| 接続ごとの保留中ポータル数 | 32 |
| 識別子の長さ | PostgreSQL 互換性のため 63 バイトとして報告されますが、現在は強制されません |
| エンコーディング | UTF-8 のみ |
| `NUMERIC` の小数桁数 | 最大 28 |

ステートメントタイムアウトは、現在のセッションに対して変更できます。

例:

```sql
SET statement_timeout = '120s';
```

現在のセッションでタイムアウトを無効にするには、`0` に設定します。

```sql
SET statement_timeout = 0;
```

## 文字エンコーディング {#character-encoding}

PostgreSQL 互換の {{{ .starter }}} は、テキストを UTF-8 で保存します。

サーバーエンコーディングは次のように表示されます。

```sql
SHOW server_encoding;
```

結果は次のとおりです。

```text
UTF8
```

インポートするテキストデータが有効な UTF-8 であることを確認してください。

## 識別子の長さ {#identifier-length}

PostgreSQL 互換の {{{ .starter }}} は、PostgreSQL 互換性のために識別子の最大長を 63 バイトとして報告します。ただし、この制限は現在は強制されません。

報告される値は、次を使用して確認できます。

```sql
SHOW max_identifier_length;
```

結果は次のとおりです。

```text
63
```

PostgreSQL とは異なり、PostgreSQL 互換の {{{ .starter }}} は 63 バイトを超える識別子も自動的に切り詰めることなく受け入れることができます。

移植性を考慮し、スキーマ、テーブル、カラム、インデックス、制約、関数、およびロールの名前は 63 バイト以内に収めてください。より長い識別子は PostgreSQL へ移行する際に切り詰められる可能性があり、名前の競合やスキーマ移行の失敗を引き起こすおそれがあります。

## 再帰 CTE の制限 {#recursive-cte-limit}

再帰共通テーブル式は 1,000 回の反復に制限されます。

例:

```sql
WITH RECURSIVE numbers AS (
    SELECT 1 AS n

    UNION ALL

    SELECT n + 1
    FROM numbers
    WHERE n < 100
)
SELECT *
FROM numbers;
```

## 配列の制約 {#array-constraints}

1 次元配列がサポートされています。

多次元の PostgreSQL 配列はサポートされていません。

例:

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    tags TEXT[]
);
```

## COPY の制約 {#copy-constraints}

PostgreSQL の `COPY` プロトコルは、テキストおよび CSV データをサポートします。

| COPY 機能 | サポート |
| --- | --- |
| テーブル形式の `COPY FROM` | サポート |
| テーブル形式の `COPY TO STDOUT` | サポート |
| テキスト形式 | サポート |
| CSV 形式 | サポート |
| バイナリ形式 | 非サポート |
| `COPY (SELECT ...) TO STDOUT` | 非サポート |

ローカルファイルについては、クライアントがファイルを読み取り、PostgreSQL 接続を通じてデータを転送できるように、`psql` の `\copy` コマンドを使用してください。

## トランザクションの制約 {#transaction-constraints}

デフォルトの分離レベルは `READ COMMITTED` です。

`REPEATABLE READ` はサポートされています。

`READ UNCOMMITTED` は `READ COMMITTED` として動作します。

PostgreSQL Serializable Snapshot Isolation はサポートされていません。PostgreSQL ワイヤプロトコル経由で `SERIALIZABLE` が要求された場合、実効的な分離レベルは `REPEATABLE READ` になります。

`DEFERRABLE` トランザクションセマンティクスはサポートされていません。

## インデックスの制約 {#index-constraints}

サポートされているインデックスアクセスメソッドは次のとおりです。

- B-tree
- GIN
- HNSW

以下の PostgreSQL インデックスアクセスメソッドはサポートされていません。

- GiST
- Hash
- SP-GiST
- BRIN

## HNSW の制約 {#hnsw-constraints}

HNSW インデックスには追加の要件があります。

特に、以下の点に注意してください。

- HNSW インデックスには 1 つのベクトルカラムが含まれます。
- インデックス対象のカラムでは、`VECTOR(1024)` のように明示的なベクトル次元を宣言する必要があります。
- テーブルには単一カラムの主キーが必要です。主キーが `INTEGER` または `BIGINT` の場合、その値は非負である必要があります。
- 部分 HNSW インデックスはサポートされていません。
- オプティマイザが HNSW インデックスを使用するには、クエリで互換性のある距離演算子とクエリ形状を使用する必要があります。

HNSW のプランニング要件を満たさないクエリは、厳密スキャンにフォールバックします。

## 全文検索の制約 {#full-text-search-constraints}

PostgreSQL 互換の全文検索には、以下の主な制約があります。

- ドキュメント化されているテキスト検索設定のみがサポートされます。
- `:*` フラグを使用したプレフィックス一致はサポートされていません。プレフィックスフラグは拒否されるのではなく暗黙的に無視されるため、プレフィックスクエリは完全一致クエリとして動作します。たとえば、`to_tsquery('english', 'qui:*')` は `to_tsquery('english', 'qui')` として解釈されるため、`quick` には一致しません。パブリックプレビュー期間中はプレフィックス一致に依存しないでください。
- `:A` などの `tsquery` 式における語彙素の重み修飾子も、暗黙的に無視されます。たとえば、`to_tsquery('english', 'qui:A')` は重み修飾子なしで解釈されます。重み付きクエリマッチングのためにこれらの修飾子に依存しないでください。
- `ts_headline()` は中国語の漢字語句をハイライトしません。
- `TSVECTOR` 値の最大サイズは 1 MiB です。

## PL/pgSQL の制約 {#pl-pgsql-constraints}

PL/pgSQL は、一般的な変数、条件分岐、`FOR` ループ、動的 SQL、`SELECT ... INTO`、DML `RETURNING ... INTO`、およびその他の一般的な構文をサポートします。

以下の構文はサポートされていません。

- `WHILE`
- `FOREACH`
- カーソル操作
- `REFCURSOR`

例外ハンドラーとネストされた手続きブロックは、`DO` ブロック内でのみサポートされます。

`BEFORE` トリガー関数には、追加の手続き上の制限があります。

## トリガーの制約 {#trigger-constraints}

サポートされるトリガーのタイミング:

- `BEFORE`
- `AFTER`

サポートされるイベント:

- `INSERT`
- `UPDATE`
- `DELETE`

`FOR EACH STATEMENT` は受け付けられますが、現在は行ごとの動作で実行されます。予測可能なトリガーのセマンティクスが必要な場合は、`FOR EACH ROW` を使用してください。

## シーケンスの制約 {#sequence-constraints}

シーケンスの作成時には、次のようなシーケンスオプションを指定できます。

- `START`
- `INCREMENT`
- `MINVALUE`
- `MAXVALUE`
- `CACHE`
- `CYCLE`

`ALTER SEQUENCE` は所有権に関する操作をサポートしますが、シーケンス作成後にこれらの生成オプションを変更することはサポートしていません。

既存のシーケンスの位置を変更するには、`setval()` を使用してください。

## カスタム型の制約 {#custom-type-constraints}

enum 型と複合型は、互換性の違いはあるもののサポートされています。複合型はテキストリテラルを使って宣言および書き込みできますが、各フィールドを個別に読み取ることはできません。

enum 型では、比較と順序付けに宣言順ではなくラベルテキストが使用されます。

アプリケーションロジックが enum の順序に依存する場合は、enum の比較順序に依存するのではなく、明示的なランクを使用してください。

## 照合順序の制約 {#collation-constraints}

カスタム照合順序はサポートされていますが、次の制限があります。

- 明示的なカスタム照合順序を指定していないテキストでは、バイト単位の順序付けが使用されます。
- 集計およびウィンドウの `ORDER BY` 式では、カスタム照合順序による順序付けは適用されません。
- カスタム照合順序は、PostgreSQL のシステムカタログに完全には表現されません。

## システムカタログの制約 {#system-catalog-constraints}

PostgreSQL 互換のシステムカタログは、一般的なイントロスペクションのワークフローを想定したものですが、PostgreSQL 本体と同一ではありません。

特に、次の点に注意してください。

- PostgreSQL 本体のすべてのシステムカタログのリレーションまたはビューが利用できるわけではありません。
- 一部のシステムカタログのリレーションでは、PostgreSQL 本体のカラムの一部のみが公開されます。
- 対応する PostgreSQL 機能がサポートされていない場合でも、互換性のために一部のカタログオブジェクトが存在することがあります。
- `information_schema.views` は利用できません。

## 拡張機能の制限 {#extension-limits}

拡張機能および組み込み機能には、それぞれ独自の制限がある場合があります。

例:

- ベクトル検索には、HNSW インデックスおよびクエリ形状に関する制約があります。
- 全文検索には、トークナイザーおよびクエリに関する制約があります。
- Parquet インポートは、ドキュメント化されている URL スキームと型マッピングのみをサポートします。
- TiDB Cloud によって明示的に提供される拡張機能のみがサポートされます。