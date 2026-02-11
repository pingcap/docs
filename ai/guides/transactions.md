---
title: Transactions
summary: アプリケーションでトランザクションを使用する方法を学びます。
---

# 取引 {#transactions}

TiDB は、データの一貫性と信頼性を確保するためにACIDトランザクションをサポートします。

## 基本的な使い方 {#basic-usage}

```python
with client.session() as session:
    initial_total_balance = session.query("SELECT SUM(balance) FROM players").scalar()

    # Transfer 10 coins from player 1 to player 2
    session.execute("UPDATE players SET balance = balance - 10 WHERE id = 1")
    session.execute("UPDATE players SET balance = balance + 10 WHERE id = 2")

    session.commit()
    # or session.rollback()

    final_total_balance = session.query("SELECT SUM(balance) FROM players").scalar()
    assert final_total_balance == initial_total_balance
```

## 参照 {#see-also}

-   [TiDB 開発者ガイド - トランザクション](/develop/dev-guide-transaction-overview.md)
-   [TiDB ドキュメント - SQL リファレンス - トランザクション](/transaction-overview.md)
