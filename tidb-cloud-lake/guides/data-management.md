---
title: Data Management
---

# Data Management

| Category | Description | Key Features | Common Operations |
|----------|-------------|--------------|------------------|
| **[Data Lifecycle](./01-data-lifecycle.md)** | Create and manage objects | • Database & Table <br/>• External Tables<br/>• Streams & Views<br/>• Indexes & Stages | • CREATE/DROP/ALTER<br/>• SHOW TABLES<br/>• DESCRIBE TABLE |
| **[Data Recovery](./02-data-recovery.md)** | Access and restore past data | • Time Travel<br/>• Flashback Tables<br/>• Backup & Restore<br/>• AT & UNDROP | • SELECT ... AT<br/>• FLASHBACK TABLE<br/>• BENDSAVE BACKUP |
| **[Data Protection](./03-data-protection.md)** | Secure access and prevent loss | • Network Policies<br/>• Access Control<br/>• Time Travel & Fail-safe<br/>• Data Encryption | • NETWORK POLICY<br/>• GRANT/REVOKE<br/>• USER/ROLE |
| **[Data Recycle](./04-data-recycle.md)** | Free up storage space | • VACUUM Commands<br/>• Retention Policies<br/>• Orphan File Cleanup<br/>• Temporary File Management | • VACUUM TABLE<br/>• VACUUM DROP TABLE<br/>• DATA_RETENTION_TIME |
