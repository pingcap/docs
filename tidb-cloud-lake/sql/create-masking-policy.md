---
title: CREATE MASKING POLICY
sidebar_position: 1
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.845"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='MASKING POLICY'/>

Creates a new masking policy in Databend.

## Syntax

```sql
CREATE [ OR REPLACE ] MASKING POLICY [ IF NOT EXISTS ] <policy_name> AS 
    ( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )
    RETURNS <arg_type_to_mask> -> <expression_on_arg_name>
    [ COMMENT = '<comment>' ]
```

| Parameter               | Description |
|------------------------|-------------|
| `policy_name`          | Name of the masking policy to be created. |
| `arg_name_to_mask`     | Parameter that represents the column being masked. This argument must appear first and automatically binds to the column referenced in `SET MASKING POLICY`. |
| `arg_type_to_mask`     | Data type of the masked column. It must match the data type of the column where the policy is applied. |
| `arg_1 ... arg_n`      | Optional extra parameters for additional columns that the policy logic depends on. Provide these columns through the `USING` clause when you attach the policy. |
| `arg_type_1 ... arg_type_n` | Data types for each optional parameter. They must match the columns listed in the `USING` clause. |
| `expression_on_arg_name` | Expression that determines how the input columns should be treated to generate the masked data. |
| `comment`              | Optional comment that stores notes about the masking policy. |

:::note
Ensure that *arg_type_to_mask* matches the data type of the column where the masking policy will be applied. When your policy defines multiple parameters, list each referenced column in the same order within the `USING` clause of `ALTER TABLE ... SET MASKING POLICY`.
:::

## Access Control Requirements

| Privilege | Description |
|:----------|:------------|
| CREATE MASKING POLICY | Required to create or replace a masking policy. Typically granted on `*.*`. |

Databend automatically grants OWNERSHIP on the new masking policy to the current role so that it can manage the policy with others.

## Examples

This example illustrates the process of setting up a masking policy to selectively reveal or mask sensitive data based on user roles.

```sql
-- Create a table and insert sample data
CREATE TABLE user_info (
    user_id INT,
    phone  VARCHAR,
    email VARCHAR
);

INSERT INTO user_info (user_id, phone, email) VALUES (1, '91234567', 'sue@example.com');
INSERT INTO user_info (user_id, phone, email) VALUES (2, '81234567', 'eric@example.com');

-- Create a role
CREATE ROLE 'MANAGERS';
GRANT ALL ON *.* TO ROLE 'MANAGERS';

-- Create a user and grant the role to the user
CREATE USER manager_user IDENTIFIED BY 'databend';
GRANT ROLE 'MANAGERS' TO 'manager_user';

-- Create a masking policy that expects an extra column
CREATE MASKING POLICY contact_mask
AS
  (contact_val nullable(string), phone_ref nullable(string))
  RETURNS nullable(string) ->
  CASE
  WHEN current_role() IN ('MANAGERS') THEN
    contact_val
  WHEN phone_ref LIKE '91%'
  THEN
    contact_val
  ELSE
    '*********'
  END
  COMMENT = 'mask contact data with phone check';

-- Associate the masking policy with the 'email' column
ALTER TABLE user_info
MODIFY COLUMN email SET MASKING POLICY contact_mask USING (email, phone);

-- Associate the masking policy with the 'phone' column
ALTER TABLE user_info
MODIFY COLUMN phone SET MASKING POLICY contact_mask USING (phone, phone);

-- Query with the Root user
SELECT user_id, phone, email FROM user_info ORDER BY user_id;

     user_id     │        phone     │       email      │
 Nullable(Int32) │ Nullable(String) │ Nullable(String) │
─────────────────┼──────────────────┼──────────────────┤
               1 │ 91234567         │ sue@example.com  │
               2 │ *********        │ *********        │

```
