---
title: PostgreSQL セッションパラメータ
summary: PostgreSQL 互換の TiDB Cloud Starter で PostgreSQL のセッションパラメータを表示および設定する方法を学びます。
---

# PostgreSQL セッションパラメータ

PostgreSQL 互換の {{{ .starter }}} は、トランザクションの動作、スキーマ解決、タイムゾーン、クエリタイムアウト、出力形式、その他のセッション設定を制御する PostgreSQL 互換のセッションパラメータをサポートしています。

## パラメータの設定と表示 {#set-and-view-parameters}

現在のセッションのパラメータを変更するには、`SET` を使用します。

```sql
SET statement_timeout = '120s';
```

現在のトランザクションに対してのみパラメータを変更するには、`SET LOCAL` を使用します。

```sql
BEGIN;

SET LOCAL statement_timeout = '30s';

SELECT *
FROM large_table;

COMMIT;
```

現在の値を表示するには、`SHOW` を使用します。

```sql
SHOW statement_timeout;
```

認識されているすべてのパラメータを一覧表示します。

```sql
SHOW ALL;
```

1 つのパラメータをデフォルト値に戻すには、`RESET` を使用します。

```sql
RESET statement_timeout;
```

すべてのセッションパラメータをリセットします。

```sql
RESET ALL;
```

## 設定関数 {#configuration-functions}

パラメータを読み取るには、`current_setting()` を使用します。

```sql
SELECT current_setting('statement_timeout');
```

パラメータを変更するには、`set_config()` を使用します。

```sql
SELECT set_config(
    'statement_timeout',
    '120s',
    false
);
```

3 番目の引数はスコープを制御します。

- `false`: セッションスコープ
- `true`: トランザクションローカルスコープ

## 一般的な PostgreSQL 互換パラメータ {#common-postgresql-compatible-parameters}

以下のよく使用されるパラメータがサポートされています。

| パラメータ | デフォルト | 変更可能 | 説明 |
| --- | --- | --- | --- |
| `application_name` | 空 | はい | セッションに関連付けられたアプリケーション名。 |
| `bytea_output` | `hex` | はい | `BYTEA` 値の出力形式。 |
| `client_encoding` | `UTF8` | はい | クライアント文字エンコーディング。 |
| `client_min_messages` | `notice` | はい | クライアントに送信される最小メッセージ重大度。 |
| `datestyle` | `ISO, MDY` | いいえ | 日付の表示形式。 |
| `default_transaction_isolation` | `read committed` | はい | 新しいトランザクションのデフォルト分離レベル。 |
| `default_transaction_read_only` | `off` | はい | 新しいトランザクションのデフォルトの読み取り専用状態。 |
| `extra_float_digits` | `1` | はい | 浮動小数点出力の追加精度。 |
| `search_path` | `$user, public` | はい | スキーマの検索順序。 |
| `server_encoding` | `UTF8` | いいえ | サーバー側の文字エンコーディング。 |
| `standard_conforming_strings` | `on` | いいえ | 文字列定数内のバックスラッシュを文字どおりに扱います。 |
| `statement_timeout` | `60000ms` | はい | クエリタイムアウト。タイムアウトなしにするには `0` を設定します。 |
| `timezone` | `UTC` | はい | セッションのタイムゾーン。 |
| `transaction_isolation` | `read committed` | はい | 現在のトランザクション分離レベル。 |
| `lock_timeout` | `0` | はい | ロック取得タイムアウト。 |
| `password_encryption` | `scram-sha-256` | はい | パスワードハッシュアルゴリズム。 |
| `max_identifier_length` | `63` | いいえ | PostgreSQL 互換の識別子長 63 バイトを報告します。この制限は現在は適用されません。 |
| `lc_messages` | `C` | はい | サーバーメッセージに使用されるロケール。 |

現在の PostgreSQL 互換の {{{ .starter }}} インスタンスで利用可能な完全なパラメータセットを確認するには、`SHOW ALL` を使用するのが最適です。

## 検索パス {#search-path}

`search_path` パラメータは、スキーマ解決の順序を制御します。

現在の検索パスを表示します。

```sql
SHOW search_path;
```

現在のセッションに対して変更します。

```sql
SET search_path = app, public;
```

この変更後、修飾されていない名前は `public` より前に `app` に対して解決されます。

## タイムゾーン {#time-zone}

現在のタイムゾーンを表示します。

```sql
SHOW timezone;
```

セッションのタイムゾーンを設定します。

```sql
SET timezone = 'America/Los_Angeles';
```

または:

```sql
SET TIME ZONE 'UTC';
```

セッションのタイムゾーンは、`TIMESTAMPTZ` 値の表示と解釈に影響します。

## ステートメントタイムアウト {#statement-timeout}

デフォルトのステートメントタイムアウトは 60 秒です。

長時間実行される操作に対して増やします。

```sql
SET statement_timeout = '180s';
```

現在のセッションのステートメントタイムアウトを無効にします。

```sql
SET statement_timeout = 0;
```

インデックス作成や大規模なデータ移行などの操作では、より大きなタイムアウトを慎重に使用してください。

## トランザクションパラメータ {#transaction-parameters}

後続のトランザクションのデフォルト分離レベルを設定します。

```sql
SET default_transaction_isolation = 'repeatable read';
```

新しいトランザクションをデフォルトで読み取り専用にします。

```sql
SET default_transaction_read_only = on;
```

現在のトランザクション設定を表示します。

```sql
SHOW transaction_isolation;
SHOW transaction_read_only;
```

## その他の受け入れられる PostgreSQL パラメータ {#other-accepted-postgresql-parameters}

以下の PostgreSQL 互換パラメータも認識されます。

- `default_table_access_method`
- `default_tablespace`
- `default_text_search_config`
- `default_transaction_deferrable`
- `idle_in_transaction_session_timeout`
- `in_hot_standby`
- `integer_datetimes`
- `intervalstyle`
- `lc_monetary`
- `lc_numeric`
- `lc_time`
- `max_index_keys`
- `row_security`
- `xmloption`

以下の追加パラメータは、`SHOW` で読み取ることができます。

- `is_superuser`
- `listen_addresses`
- `max_connections`
- `port`
- `role`
- `server_version`
- `server_version_num`
- `session_authorization`
- `transaction_deferrable`
- `transaction_read_only`

一部の値は、PostgreSQL クライアントおよびツールとの互換性のために公開されていますが、対応する PostgreSQL 本体のサーバーのすべての機能が利用可能であることを意味するものではありません。

## 互換性専用パラメータ {#compatibility-only-parameters}

一部の PostgreSQL パラメータは、PostgreSQL クライアントやフレームワークがセッションを正常に初期化できるように受け入れられますが、それらを変更してもクエリの動作は変わりません。

### `work_mem` {#work-mem}

`work_mem` は受け入れられ、セッション値を変更できます。

```sql
SET work_mem = '64MB';
SHOW work_mem;
```

設定された値は、PostgreSQL 互換 {{{ .starter }}} におけるクエリ実行メモリを制御しません。

### `check_function_bodies` {#check-function-bodies}

`check_function_bodies` は受け入れられますが、PostgreSQL と同じ方法で関数本体の検証を制御するものではありません。

PL/pgSQL 関数本体内の SQL 文は、関数が呼び出されたときにのみ検証される場合があります。関数を作成した後にテストしてください。

## `session_replication_role` {#session-replication-role}

`session_replication_role = 'replica'` はサポートされていません。

次の文は拒否されます。

```sql
SET session_replication_role = 'replica';
```

トリガーは通常の `origin` 動作で引き続き実行されます。

バルクロード中にトリガーを抑止するために `session_replication_role` に依存しないでください。

## 全文検索パラメータ {#full-text-search-parameter}

`default_text_search_config` パラメータは、デフォルトの全文検索設定を制御します。

現在の値を表示します。

```sql
SHOW default_text_search_config;
```

現在のセッションに設定します。

```sql
SET default_text_search_config = 'simple';
```

## ベクトル検索パラメータ {#vector-search-parameter}

`hnsw.ef_search` パラメータは、現在のセッションにおける HNSW の候補リストサイズを制御します。

表示するには、次を実行します。

```sql
SHOW hnsw.ef_search;
```

設定するには、次を実行します。

```sql
SET hnsw.ef_search = 100;
```

デフォルト値は `40` です。値を大きくすると、追加のクエリレイテンシーを伴う代わりに再現率が向上する場合があります。

## 埋め込みパラメータ {#embedding-parameter}

`embedding` 拡張機能を有効にすると、`embedding.dimensions` パラメータは、サポートされているサーバー側埋め込み関数で使用される出力次元を制御します。

例:

```sql
SET embedding.dimensions = 512;
```