---
title: Data Management
summary: An overview of data management in TiDB Cloud Lake, covering data lifecycle, recovery, protection, and recycling.
---
# Data Management

| Category | Description | Key Features | Common Operations |
|----------|-------------|--------------|------------------|
| **[Data Lifecycle](/tidb-cloud-lake/guides/data-lifecycle.md)** | Create and manage objects | • Database & Table <br/>• External Tables<br/>• Streams & Views<br/>• Indexes & Stages | • CREATE/DROP/ALTER<br/>• SHOW TABLES<br/>• DESCRIBE TABLE |
| **[Data Recovery](/tidb-cloud-lake/guides/data-recovery.md)** | Access and restore past data | • Time Travel<br/>• Flashback Tables<br/>• Backup & Restore<br/>• AT & UNDROP | • SELECT ... AT<br/>• FLASHBACK TABLE<br/>• BENDSAVE BACKUP |
| **[Data Protection](/tidb-cloud-lake/guides/data-protection.md)** | Secure access and prevent loss | • Network Policies<br/>• Access Control<br/>• Time Travel & Fail-safe<br/>• Data Encryption | • NETWORK POLICY<br/>• GRANT/REVOKE<br/>• USER/ROLE |
| **[Data Recycle](/tidb-cloud-lake/guides/data-purge-and-recycle.md)** | Free up storage space | • VACUUM Commands<br/>• Retention Policies<br/>• Orphan File Cleanup<br/>• Temporary File Management | • VACUUM TABLE<br/>• VACUUM DROP TABLE<br/>• DATA_RETENTION_TIME |
