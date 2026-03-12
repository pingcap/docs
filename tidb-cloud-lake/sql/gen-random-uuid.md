---
title: GEN_RANDOM_UUID
---

Generates a random UUID based on version 7, starting from version 1.2.658. Previously, this function generated UUIDs based on version 4.

## Syntax

```sql
GEN_RANDOM_UUID()
```

## Aliases

- [UUID](uuid.md)

## Why Use UUID v7?

- **Time-Based Ordering**: UUID v7 includes a timestamp, allowing events or records to be ordered chronologically by the time they were created. This is especially useful when you need to track the sequence of actions.
  
- **Chronological Sorting**: UUID v7 ensures that UUIDs are sorted by creation time, which is ideal for scenarios where sorting events by time is necessary, such as event logging or maintaining audit trails.

## Version Information

- Version 1.2.658 and later: UUID version upgraded from v4 to v7.
- Version prior to 1.2.658: UUID generation was based on v4.

## Examples

In an application where events are logged, maintaining the correct sequence of actions is essential. UUID v7 ensures that each event is time-ordered, making it easy to track actions chronologically.

```sql
-- Log a user logging in
SELECT GEN_RANDOM_UUID(), 'User logged in' AS event, CURRENT_TIMESTAMP AS event_time;

-- Log a user making a purchase
SELECT GEN_RANDOM_UUID(), 'User made a purchase' AS event, CURRENT_TIMESTAMP AS event_time;
```

The results from these queries might look like this:
```sql
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│           gen_random_uuid()          │         event        │         event_time         │
├──────────────────────────────────────┼──────────────────────┼────────────────────────────┤
│ 019329e6-26a2-7b01-b9f5-1c3c02600578 │ User logged in       │ 2024-11-14 08:59:29.313906 │
│ 019329e6-329e-73c3-b0a8-a413ce298607 │ User made a purchase │ 2024-11-14 08:59:32.381497 │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

Notice that the `gen_random_uuid()` values are generated in the order that the events occurred, making it easy to maintain chronological order.
