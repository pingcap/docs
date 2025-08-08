---
title: SHOW PROFILES
summary: TiDB データベースの SHOW PROFILES の使用法の概要。
---

# プロフィールを表示 {#show-profiles}

`SHOW PROFILES`ステートメントは現在、空の結果のみを返します。

## 概要 {#synopsis}

```ebnf+diagram
ShowProfilesStmt ::=
    "SHOW" "PROFILES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
SHOW PROFILES;
```

    Empty set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントはMySQLとの互換性のためにのみ含まれています。1 `SHOW PROFILES`実行すると常に空の結果が返されます。

代替案として、TiDB は SQL パフォーマンスの問題を理解するのに役立つ[明細書要約表](/statement-summary-tables.md)提供します。
