---
title: UUID Functions
---

This page provides reference information for the UUID-related functions in Databend. These functions generate and work with Universally Unique Identifiers (UUIDs).

## UUID Generation Functions

| Function | Description | Example |
|----------|-------------|--------|
| [GEN_RANDOM_UUID](gen-random-uuid.md) | Generates a random UUID (version 7 from v1.2.658, version 4 before) | `GEN_RANDOM_UUID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |
| [UUID](uuid.md) | Alias for GEN_RANDOM_UUID | `UUID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |

## Usage Examples

### Generating Primary Keys

```sql
-- Create a table with UUID primary key
CREATE TABLE users (
  id UUID DEFAULT GEN_RANDOM_UUID(),
  username VARCHAR,
  email VARCHAR,
  PRIMARY KEY(id)
);

-- Insert data without specifying UUID
INSERT INTO users (username, email) 
VALUES ('johndoe', 'john@example.com');

-- Query to see the auto-generated UUID
SELECT * FROM users;
```

### Creating Unique Identifiers for Distributed Systems

```sql
-- Generate multiple UUIDs for distributed event tracking
SELECT 
  GEN_RANDOM_UUID() AS event_id,
  'user_login' AS event_type,
  NOW() AS event_time
FROM numbers(5);
```

### UUID Version Information

Databend's UUID implementation has evolved:

- **Version 1.2.658 and later**: Uses UUID version 7, which includes timestamp information for chronological sorting
- **Prior to version 1.2.658**: Used UUID version 4, which was purely random
