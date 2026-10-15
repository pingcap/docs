---
title: TiDB に AI エージェントのメモリを保存する
summary: ベクトル検索、トランザクション、ユーザーごとのリコール、自動期限切れを使って、1 つの TiDB テーブルに SQL で AI エージェントのメモリを保存する方法を学びます。
---

# TiDB に AI エージェントのメモリを保存する

セッションをまたいでユーザーを記憶する AI エージェントでは、メモリストアに 4 つの機能が必要です。意味に基づいてメモリを見つけること、ユーザーと種類で絞り込むこと、古くなったメモリを中途半端な書き込み状態を残さずに置き換えること、そして期限切れになったときやユーザーから要求があったときにメモリを忘れることです。TiDB では、ベクトル検索、セカンダリインデックス、トランザクション、行の有効期限が同じデータベース内にあるため、1 つのテーブルと通常の SQL でこの 4 つすべてを実現できます。

このドキュメントでは、そのテーブルを順を追って説明します。同じ考え方に基づいて `pytidb` Python SDK で構築された完全なチャットアプリケーションについては、[AI エージェントのメモリの例](/ai/guides/memory-with-pytidb.md) を参照してください。

## 前提条件 {#prerequisites}

- {{{ .starter }}} インスタンス。無料の {{{ .starter }}} インスタンスは [TiDB Cloud](https://tidbcloud.com/free-trial) で作成できます。
- インスタンスに接続された MySQL クライアント。[TiDB Cloud コンソール](https://tidbcloud.com/) で {{{ .starter }}} インスタンスの概要ページに移動し、接続パラメータを確認するには **Connect** をクリックします。

この例では、SQL の例とクエリ結果を理解しやすくするために、手動で値を割り当てた 3 次元ベクトルを使用します。これらのベクトルはデモ用であり、埋め込みモデルによって生成された埋め込みを表すものではありません。実際のアプリケーションでは、ベクトル次元を埋め込みモデルの出力サイズに合わせて設定してください。たとえば `VECTOR(1536)` を使用し、各埋め込みはそのモデルで生成します。

## ステップ 1. メモリテーブルを作成する {#step-1-create-the-memory-table}

まずデータベースを選択します。この例では、すべての {{{ .starter }}} インスタンスにある `test` データベースを使用します。

```sql
USE test;

CREATE TABLE agent_memory (
    id          BIGINT PRIMARY KEY AUTO_RANDOM,
    user_id     VARCHAR(64) NOT NULL,
    kind        ENUM('fact', 'preference', 'episode') NOT NULL,
    content     TEXT NOT NULL,
    embedding   VECTOR(3) NOT NULL,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_user (user_id, is_active),
    VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
) TTL = `created_at` + INTERVAL 90 DAY TTL_ENABLE = 'ON';
```

テーブルの各要素は、それぞれ 1 つのメモリ操作に対応しています。

- `embedding` とベクトルインデックス `idx_embedding` により、意味に基づいてメモリを見つけられます。
- `user_id` と `kind` により、メモリを 1 人のユーザーと 1 つの種類に絞り込めます。`(user_id, is_active)` 上のセカンダリインデックス `idx_user` により、あるユーザーのアクティブなメモリを高速に読み取れます。
- `is_active` により、古くなったメモリを削除せずに無効化できます。
- `TTL` 句により、90 日を超えて保存されたメモリは TiDB が自動的にクリーンアップします。TTL のクリーンアップは定期的に実行されるため、期限切れのメモリが必ずしも即座に削除されるわけではありません。詳細は [TTL (Time to Live)](/time-to-live.md) を参照してください。

## ステップ 2. メモリを書き込む {#step-2-write-memories}

```sql
INSERT INTO agent_memory (user_id, kind, content, embedding) VALUES
  ('alice', 'fact',       'Alice is a data engineer at a fintech company.',    '[0.9, 0.1, 0.2]'),
  ('alice', 'preference', 'Alice prefers answers in Python.',                  '[0.2, 0.9, 0.1]'),
  ('alice', 'episode',    'Alice asked how to tune a slow join on 2026-10-01.', '[0.5, 0.4, 0.7]'),
  ('bob',   'fact',       'Bob runs a small online bookstore.',                '[0.8, 0.2, 0.3]'),
  ('bob',   'preference', 'Bob prefers short answers.',                        '[0.1, 0.8, 0.3]');
```

## ステップ 3. トランザクションで古いメモリを置き換える {#step-3-replace-an-outdated-memory-in-a-transaction}

ユーザーの好みが変わった場合は、古いメモリを無効化し、新しいメモリを書き込む処理を 1 つのトランザクションで行います。これにより、読み取り側が一部だけ適用された置き換えを見ることはありません。

同じユーザーに対して同時書き込みによって複数のアクティブな preference が作成されるのを防ぐには、[ユーザーごとにアクティブな preference を最大 1 つに制限する](#enforce-at-most-one-active-preference-per-user) で説明する一意制約を追加してください。

```sql
BEGIN;
UPDATE agent_memory SET is_active = FALSE
 WHERE user_id = 'alice' AND kind = 'preference' AND is_active;
INSERT INTO agent_memory (user_id, kind, content, embedding)
VALUES ('alice', 'preference', 'Alice now prefers answers in Go.', '[0.25, 0.85, 0.15]');
COMMIT;
```

結果を確認します。

```sql
SELECT content, is_active FROM agent_memory
WHERE user_id = 'alice' AND kind = 'preference'
ORDER BY is_active DESC;
```

```
+----------------------------------+-----------+
| content                          | is_active |
+----------------------------------+-----------+
| Alice now prefers answers in Go. |         1 |
| Alice prefers answers in Python. |         0 |
+----------------------------------+-----------+
```

トランザクション内のステートメントが失敗した場合、たとえば値がカラムに収まらない場合は、`COMMIT` ではなく `ROLLBACK` を実行してください。ステートメントが失敗してもトランザクション自体は終了しません。成功したステートメントは保留されたままであり、`COMMIT` を実行すると保存されます。たとえば、古い preference だけが無効化され、新しい preference がない状態になる可能性があります。`ROLLBACK` の後は、メモリは元の状態のままです。

### ユーザーごとにアクティブな preference を最大 1 つに制限する {#enforce-at-most-one-active-preference-per-user}

トランザクションにより各置き換えはアトミックになりますが、同時書き込みによって同じユーザーに複数のアクティブな preference が作成される可能性は残ります。たとえば、アクティブな preference が存在しない場合、2 つのトランザクションがそれぞれ 0 行を更新し、新しい preference を挿入して、どちらも正常にコミットできてしまいます。

アプリケーションでユーザーごとにアクティブな preference を 1 つだけ許可する場合は、次の生成カラムと一意インデックスを追加してください。既存のテーブルに対しては、まず各ユーザーについて重複するアクティブな preference を無効化または削除する必要があります。

```sql
ALTER TABLE agent_memory
ADD COLUMN active_preference_user VARCHAR(64)
GENERATED ALWAYS AS (
  CASE
    WHEN kind = 'preference' AND is_active THEN user_id
    ELSE NULL
  END
) VIRTUAL;

ALTER TABLE agent_memory
ADD UNIQUE KEY uk_active_preference (active_preference_user);
```

この生成カラムには、アクティブな preference に対してのみ `user_id` が入ります。一意インデックスにより、そのような行で同じユーザー ID を 2 つ持つことを防げます。その他の行ではこのカラムは `NULL` になるため、このインデックスはユーザーごとに複数の非アクティブな preference、fact、episode を許可します。

一意インデックスを追加した後は、上記のように 1 つのトランザクション内で古い preference を無効化し、新しい preference を挿入します。一意インデックスにより、同時書き込み下でもこの制限が適用されます。置き換えに失敗した場合は、トランザクションをロールバックしてください。再試行するには、新しいトランザクションを開始し、`UPDATE` と `INSERT` の両方を再度実行します。

## ステップ 4. 1 人のユーザーのメモリをリコールする {#step-4-recall-memories-for-one-user}

多くのエージェントリクエストでは、現在のユーザーのメモリだけが必要です。まずユーザーで絞り込み、その後で現在のリクエストの埋め込みとの距離で順位付けします。

```sql
SELECT kind, content, VEC_COSINE_DISTANCE(embedding, '[0.2, 0.9, 0.2]') AS distance
FROM agent_memory
WHERE user_id = 'alice' AND is_active
ORDER BY distance
LIMIT 3;
```

```
+------------+----------------------------------------------------+-----------------------+
| kind       | content                                            | distance              |
+------------+----------------------------------------------------+-----------------------+
| preference | Alice now prefers answers in Go.                   | 0.0032403313698232683 |
| episode    | Alice asked how to tune a slow join on 2026-10-01. |    0.3295984359391211 |
| fact       | Alice is a data engineer at a fintech company.     |     0.645662235088144 |
+------------+----------------------------------------------------+-----------------------+
```

このクエリではベクトルインデックスは使用されません。これは、`WHERE` フィルタが最近傍探索より前に適用されるためです。セカンダリインデックス `idx_user` を使ってこのユーザーのアクティブなメモリだけを読み取り、それぞれに対して正確な距離を計算できます。結果は正確であり、セカンダリインデックスが使われる場合のコストは主に一致するメモリ数に依存し、テーブル全体のスキャンは不要です。これは通常、ユーザー単位のエージェントメモリに適したパターンです。

## ステップ 5. すべてのユーザーをまたいでメモリをリコールする {#step-5-recall-memories-across-all-users}

アプリケーションがアクセスを許可されているユーザー群をまたいで類似した過去の会話を見つけるような機能では、テーブル全体を検索します。まずベクトルインデックスを使って近似最近傍を見つけ、その後でフィルタします。必要数より多めに候補を取得してください。フィルタによって一部が除外される可能性があるためです。ただし、追加の候補を取得しても、候補集合の外に一致するメモリがさらに存在する場合であっても、最終クエリが 3 件の一致を返すことは保証されません。

```sql
SELECT * FROM (
  SELECT user_id, kind, content, is_active,
         VEC_COSINE_DISTANCE(embedding, '[0.85, 0.15, 0.25]') AS distance
  FROM agent_memory
  ORDER BY distance
  LIMIT 20
) t
WHERE is_active
ORDER BY distance
LIMIT 3;
```

```
+---------+---------+----------------------------------------------------+-----------+-----------------------+
| user_id | kind    | content                                            | is_active | distance              |
+---------+---------+----------------------------------------------------+-----------+-----------------------+
| alice   | fact    | Alice is a data engineer at a fintech company.     |         1 | 0.0040039807124229165 |
| bob     | fact    | Bob runs a small online bookstore.                 |         1 | 0.0044730676562374505 |
| alice   | episode | Alice asked how to tune a slow join on 2026-10-01. |         1 |     0.225803083881864 |
+---------+---------+----------------------------------------------------+-----------+-----------------------+
```

このクエリに対して `EXPLAIN` を実行し、ベクトルインデックスが使われていることを確認してください。ベクトルインデックスが使用される場合、`operator info` カラムには `annIndex:` が含まれます。行数がごく少ないテーブルでは、オプティマイザが代わりに TiKV から読み取り、ベクトルインデックスをスキップすることがあります。テーブルが大きくなると、クエリとそのコスト見積もりに応じて、オプティマイザがベクトルインデックスを選択する場合があります。フィルタの配置がベクトルインデックスに与える影響については、[フィルター付きベクトルインデックスを使用する](/ai/reference/vector-search-index.md#use-the-vector-index-with-filters) を参照してください。

## ステップ 6. メモリを忘れる {#step-6-forget-memories}

`agent_memory` テーブルに保存された特定ユーザーのすべてのメモリを削除するには、たとえばユーザーから削除要求があった場合、`user_id` で削除します。

```sql
DELETE FROM agent_memory WHERE user_id = 'bob';
```

90 日より古いメモリは、ステップ 1 の `TTL` 句によって自動的に削除されます。{{{ .starter }}} では、期限切れ行は 15 分ごとに実行されるバックグラウンド TTL ジョブによってクリーンアップされ、`TTL_JOB_INTERVAL` は固定で変更できません。期限切れのメモリをただちにリコール対象から除外するには、`created_at` でフィルタします。ステップ 4 のクエリでは、`WHERE` 句に `AND created_at > NOW() - INTERVAL 90 DAY` を追加します。ステップ 5 のクエリでは、サブクエリで `created_at` を選択し、外側の `WHERE` 句で `is_active` の横にその条件を追加します。

```sql
SELECT * FROM (
  SELECT user_id, kind, content, is_active, created_at,
         VEC_COSINE_DISTANCE(embedding, '[0.85, 0.15, 0.25]') AS distance
  FROM agent_memory
  ORDER BY distance
  LIMIT 20
) t
WHERE is_active AND created_at > NOW() - INTERVAL 90 DAY
ORDER BY distance
LIMIT 3;
```

`created_at` のフィルタをサブクエリの内側に置かないでください。サブクエリ内のフィルタは最近傍探索より前に適用されるため、ベクトルインデックスが使用されません。

> **Note:**
>
> `DELETE` の後でも、削除された行は、ガベージコレクションが古い行バージョンを削除するまで、`SELECT ... AS OF TIMESTAMP` のような [ステイル読み取り](/stale-read.md) で短時間読み取れる場合があります。TiDB は古いバージョンを少なくとも [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) で設定された時間だけ保持します。デフォルトは 10 分です。

## 関連情報 {#see-also}

- [AI エージェントのメモリの例](/ai/guides/memory-with-pytidb.md)
- [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
- [トランザクション](/ai/guides/transactions.md)
- [TTL (Time to Live)](/time-to-live.md)