---
title: Network Policy
summary: Network policies control who can log in to Databend based on the client IP. Even if the credentials are correct, a connection request is rejected when its IP does not satisfy the policy, giving you an extra security layer beyond username and password.
---
Network policies control who can log in to Databend based on the client IP. Even if the credentials are correct, a connection request is rejected when its IP does not satisfy the policy, giving you an extra security layer beyond username and password.

## How It Works

- `ALLOWED_IP_LIST` accepts single IPv4 addresses or CIDR blocks such as `10.0.0.0/24`. Only addresses in the list are allowed to log in.
- `BLOCKED_IP_LIST` (optional) lets you carve out explicit deny rules from the allowed ranges. Databend checks the blocked list first, so an IP that exists in both lists is still denied.
- A user can reference at most one network policy at a time, but the same policy can be shared across many users for easier management.
- If the server cannot determine a client IP or the IP does not match the allowed list, Databend immediately returns `AuthenticateFailure`.

## End-to-End Example

The following walkthrough covers the typical lifecycle: create a policy, attach it to users, confirm its status, update it centrally, and finally detach and drop it.

### 1. Create and Inspect a Policy

```sql
CREATE NETWORK POLICY corp_vpn_policy
    ALLOWED_IP_LIST=('10.1.0.0/16', '172.16.8.12/32')
    BLOCKED_IP_LIST=('10.1.10.25')
    COMMENT='Only VPN ranges';

SHOW NETWORK POLICIES;

Name            |Allowed Ip List           |Blocked Ip List|Comment          |
----------------+--------------------------+---------------+-----------------+
corp_vpn_policy |10.1.0.0/16,172.16.8.12/32|10.1.10.25     |Only VPN ranges  |
```

### 2. Attach the Policy to Users

```sql
CREATE USER alice IDENTIFIED BY 'Str0ngPass!' WITH SET NETWORK POLICY='corp_vpn_policy';
CREATE USER bob IDENTIFIED BY 'An0therPass!';

-- Apply the policy to an existing user
ALTER USER bob WITH SET NETWORK POLICY='corp_vpn_policy';
```

### 3. Verify Enforcement

```sql
DESC USER alice;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │       auth_type      │ default_role │ roles │ disabled │   network_policy  │ password_policy │ must_change_password │
├────────┼──────────┼──────────────────────┼──────────────┼───────┼──────────┼───────────────────┼─────────────────┼──────────────────────┤
│ alice  │ %        │ double_sha1_password │              │       │ false    │ corp_vpn_policy   │                 │ NULL                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

DESC NETWORK POLICY corp_vpn_policy;

Name            |Allowed Ip List           |Blocked Ip List|Comment         |
----------------+--------------------------+---------------+----------------+
corp_vpn_policy |10.1.0.0/16,172.16.8.12/32|10.1.10.25     |Only VPN ranges |
```

### 4. Update and Reuse the Policy

Use [ALTER NETWORK POLICY](/tidb-cloud-lake/sql/network-policy-sql.md) to adjust the allowed or blocked IPs without touching each user:

```sql
ALTER NETWORK POLICY corp_vpn_policy
    SET ALLOWED_IP_LIST=('10.1.0.0/16', '10.2.0.0/16')
        BLOCKED_IP_LIST=('10.1.10.25', '10.2.5.5')
        COMMENT='VPN + DR site';

DESC NETWORK POLICY corp_vpn_policy;

Name            |Allowed Ip List             |Blocked Ip List          |Comment          |
----------------+----------------------------+-------------------------+-----------------+
corp_vpn_policy |10.1.0.0/16,10.2.0.0/16     |10.1.10.25,10.2.5.5      |VPN + DR site    |
```

Every user referencing the policy automatically picks up the new IP ranges.

### 5. Detach and Clean Up

```sql
ALTER USER bob WITH UNSET NETWORK POLICY;
DROP NETWORK POLICY corp_vpn_policy;
```

Confirm that no users depend on the policy before dropping it; otherwise, their logins will fail.

---

For full syntax details, see the [Network Policy SQL reference](/tidb-cloud-lake/sql/network-policy-sql.md), which covers `CREATE`, `ALTER`, `SHOW`, `DESC`, and `DROP`.
