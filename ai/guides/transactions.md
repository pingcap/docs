---
title: Transactions
summary: Learn how to use transactions in your application.
---

# Transaction

TiDB supports ACID transactions, which ensure data consistency and reliability.

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

- [TiDB Develop Guide - Transaction](https://docs.pingcap.com/tidbcloud/dev-guide-transaction-overview/)
- [TiDB Docs- SQL Reference - Transactions](https://docs.pingcap.com/tidbcloud/transaction-overview/)