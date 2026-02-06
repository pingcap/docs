---
title: Transactions
summary: Learn how to use transactions in your application.
---

# Transactions

TiDB supports ACID transactions to ensure data consistency and reliability.

## Basic usage

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

## See also

- [TiDB Developer Guide - Transactions](/develop/dev-guide-transaction-overview.md)
- [TiDB Documentation - SQL Reference - Transactions](/transaction-overview.md)