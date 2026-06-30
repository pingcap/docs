---
title: Security & Reliability
summary: "{{{ .lake }}} offers enterprise-grade security and reliability features that safeguard your data throughout its lifecycle. From controlling who can access your data to protecting against network threats and recovering from operational errors, {{{ .lake }}}'s multi-layered security approach helps you maintain data integrity, compliance, and business continuity."
---

# Security & Reliability

{{{ .lake }}} offers **enterprise-grade security and reliability features** that safeguard your data throughout its lifecycle. From controlling who can access your data to protecting against network threats and recovering from operational errors, {{{ .lake }}}'s **multi-layered security approach** helps you maintain data integrity, compliance, and business continuity.

| Security Feature | Purpose | When to Use |
|-----------------|---------|------------|
| [**Access Control**](/tidb-cloud-lake/guides/access-control.md) | Manage user permissions | When you need to control data access with role-based security and object ownership |
| [**Data Protection Policies**](/tidb-cloud-lake/guides/data-protection-policies.md) | Protect sensitive data at row and column level | When you need row-level filtering, column-level masking, or both |
| [**Audit Trail**](/tidb-cloud-lake/guides/audit-trail.md) | Track database activities | When you need comprehensive audit trails for security monitoring, compliance, and performance analysis |
| [**Network Policy**](/tidb-cloud-lake/guides/network-policy.md) | Restrict network access | When you want to limit connections to specific IP ranges even with valid credentials |
| [**Password Policy**](/tidb-cloud-lake/guides/password-policy.md) | Set password requirements | When you need to enforce password complexity, rotation, and account lockout rules |
| [**Authenticate with AWS IAM Role**](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) | Use AWS IAM roles for authentication | When you want to leverage AWS IAM for secure access to {{{ .lake }}} |
| [**Compliance & Security**](/tidb-cloud-lake/guides/compliance-security.md) | Ensure regulatory compliance | When you need to adhere to industry standards and regulations |
| [**Fail-Safe**](/tidb-cloud-lake/guides/fail-safe.md) | Prevent data loss | When you need to recover accidentally deleted data from S3-compatible storage |
| [**Recovery from Errors**](/tidb-cloud-lake/guides/recovery-from-operational-errors.md) | Fix operational mistakes | When you need to recover from dropped databases/tables or incorrect data modifications |
