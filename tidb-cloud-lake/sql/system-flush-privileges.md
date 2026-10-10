---
title: SYSTEM FLUSH PRIVILEGES
summary: すべてのクエリノードに権限メタデータの更新をブロードキャストし、GRANT と REVOKE の変更を即座に有効にします。
---

# SYSTEM FLUSH PRIVILEGES

`SYSTEM FLUSH PRIVILEGES` は、すべてのクエリノードに更新リクエストをブロードキャストし、各ノードが Meta service から権限およびロールのメタデータを即座に再読み込みできるようにします。デフォルトの 15 秒のロールキャッシュ間隔を待たずに、変更をクラスター全体で有効にする必要がある場合は、`GRANT` または `REVOKE` 文の後にこのコマンドを実行します。

関連情報:

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [REVOKE](/tidb-cloud-lake/sql/revoke.md)

## 構文 {#syntax}

```sql
SYSTEM FLUSH PRIVILEGES
```

## 使用上の注意 {#usage-notes}

- `ACCOUNT ADMIN` など、システム管理コマンドの実行が許可されたロールが必要です。
- キャッシュされた権限メタデータのみを更新します。ロールや付与内容自体を変更するものではありません。
- すでに実行中の文は、開始時に解決された権限を引き続き使用します。変更を反映させるには、flush 後にその文を再実行してください。

## 例 {#example}

次のシーケンスでは、ロールにデータベースへのアクセス権を付与し、キャッシュを即座に flush することで、新しい権限をすべてのクエリノードから参照できるようにします。

```sql
GRANT SELECT ON DATABASE marketing TO ROLE analyst;

SYSTEM FLUSH PRIVILEGES;
```

flush の完了後、`analyst` ロールで実行される新しいクエリは、キャッシュの有効期限切れを待つことなく、更新後の権限セットを受け取ります。