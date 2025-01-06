---
title: System Variable Reference
summary: A list of all TiDB system variables and their references in the documentation.
---

<!-- Note: The content of the reference lists in this file is organized in the following order:
- Put non-release-notes docs ahead of release notes.
- For non-release-notes docs, put them in alphabetical order.
- For release notes docs, put them in reverse order by version number. -->

# System Variable Reference

This document lists all TiDB system variables and the files that reference them in the documentation. View the [System Variables](/system-variables.md) for more details of each variable.

## Variable reference

### allow_auto_random_explicit_insert

Referenced in:

- [AUTO_RANDOM](/auto-random.md)
- [Insert Data](/develop/dev-guide-insert-data.md)
- [SESSION_VARIABLES](/information-schema/information-schema-session-variables.md)
- [VARIABLES_INFO](/information-schema/information-schema-variables-info.md)
- [TiDB 4.0.3 Release Notes](/releases/release-4.0.3.md)

### authentication_ldap_sasl_auth_method_name

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_bind_base_dn

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_bind_root_dn

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_bind_root_pwd

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_ca_path

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_init_pool_size

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_max_pool_size

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_server_host

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_server_port

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_sasl_tls

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_auth_method_name

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_bind_base_dn

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_bind_root_dn

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_bind_root_pwd

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_ca_path

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_init_pool_size

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_max_pool_size

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_server_host

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_server_port

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### authentication_ldap_simple_tls

Referenced in:

- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### auto_increment_increment

Referenced in:

- [AUTO_INCREMENT](/auto-increment.md)
- [AUTO_RANDOM](/auto-random.md)
- [Bidirectional Replication](/ticdc/ticdc-bidirectional-replication.md)
- [Error Codes and Troubleshooting](/error-codes.md)
- [TiDB 7.1.6 Release Notes](/releases/release-7.1.6.md)
- [TiDB 6.5.10 Release Notes](/releases/release-6.5.10.md)
- [TiDB 3.0.9 Release Notes](/releases/release-3.0.9.md)

### auto_increment_offset

Referenced in:

- [AUTO_INCREMENT](/auto-increment.md)
- [AUTO_RANDOM](/auto-random.md)
- [Bidirectional Replication](/ticdc/ticdc-bidirectional-replication.md)
- [Error Codes and Troubleshooting](/error-codes.md)
- [TiDB 7.1.6 Release Notes](/releases/release-7.1.6.md)
- [TiDB 6.5.10 Release Notes](/releases/release-6.5.10.md)
- [TiDB 3.0.9 Release Notes](/releases/release-3.0.9.md)

### autocommit

Referenced in:

- [Non-Transactional DML Statements](/non-transactional-dml.md)
- [Transaction Overview](/transaction-overview.md)
- [Pessimistic Transaction Mode](/pessimistic-transaction.md)
- [Temporary Tables](/temporary-tables.md)
- [Connect to TiDB with Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)
- [Connect to TiDB with MySQL Connector/Python](/develop/dev-guide-sample-application-python-mysql-connector.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 6.5.3 Release Notes](/releases/release-6.5.3.md)

### block_encryption_mode

Referenced in:

- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)

### character_set_client

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [Dumpling Overview](/dumpling-overview.md)
- [GBK Character Set](/character-set-gbk.md)
- [SET [NAMES|CHARACTER SET]](/sql-statements/sql-statement-set-names.md)
- [Use Views](/develop/dev-guide-use-views.md)
- [Views](/views.md)
- [`VIEWS` INFORMATION_SCHEMA Table](/information-schema/information-schema-views.md)

### character_set_connection

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [Dumpling Overview](/dumpling-overview.md)
- [GBK Character Set](/character-set-gbk.md)
- [SET [NAMES|CHARACTER SET]](/sql-statements/sql-statement-set-names.md)

### character_set_database

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [SET [NAMES|CHARACTER SET]](/sql-statements/sql-statement-set-names.md)

### character_set_results

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [SET [NAMES|CHARACTER SET]](/sql-statements/sql-statement-set-names.md)
- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)
- [TiDB 2.1 RC1 Release Notes](/releases/release-2.1-rc.1.md)

### character_set_server

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [SET [NAMES|CHARACTER SET]](/sql-statements/sql-statement-set-names.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)

### collation_connection

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [String Functions](/functions-and-operators/string-functions.md)
- [Use Views](/develop/dev-guide-use-views.md)
- [Views](/views.md)
- [`VIEWS` INFORMATION_SCHEMA Table](/information-schema/information-schema-views.md)

### collation_database

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)

### collation_server

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)
- [TiDB 5.0.2 Release Notes](/releases/release-5.0.2.md)

### cte_max_recursion_depth

Referenced in:

- [Highly Concurrent Write Best Practices](/best-practices/high-concurrency-best-practices.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)

### datadir

Referenced in:

- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)

### ddl_slow_threshold

Referenced in:

- [SHOW [GLOBAL|SESSION] VARIABLES](/sql-statements/sql-statement-show-variables.md)

### default_authentication_plugin

Referenced in:

- [TiDB Features](/basic-features.md)
- [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 5.2.0 Release Notes](/releases/release-5.2.0.md)

### default_collation_for_utf8mb4

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [TiDB 8.1.2 Release Notes](/releases/release-8.1.2.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)

### default_password_lifetime

Referenced in:

- [Password Management](/password-management.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### default_week_format

Referenced in:

- [Date and Time Functions](/functions-and-operators/date-and-time-functions.md)
- [TiDB 4.0.11 Release Notes](/releases/release-4.0.11.md)
- [TiDB 2.1.7 Release Notes](/releases/release-2.1.7.md)

### disconnect_on_expired_password

Referenced in:

- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### div_precision_increment

Referenced in:

- [Numeric Functions and Operators](/functions-and-operators/numeric-functions-and-operators.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)

### error_count

Referenced in:

- [TiDB 2.1 RC1 Release Notes](/releases/release-2.1-rc.1.md)

### foreign_key_checks

Referenced in:

- [FOREIGN KEY Constraints](/foreign-key.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)

### group_concat_max_len

Referenced in:

- [Aggregate (GROUP BY) Functions](/functions-and-operators/aggregate-group-by-functions.md)
- [TiDB 4.0.13 Release Notes](/releases/release-4.0.13.md)

### have_openssl

Referenced in:

- [Certificate-Based Authentication for Login](/certificate-authentication.md)

### have_ssl

Referenced in:

- [Certificate-Based Authentication for Login](/certificate-authentication.md)

### hostname

Referenced in:

- [Best Practices for Using HAProxy in TiDB](/best-practices/haproxy-best-practices.md)
- [The `mysql.user` Table](/mysql-schema/mysql-schema-user.md)

### identity

Referenced in:

- [Configure SSO for TiDB Dashboard](/dashboard/dashboard-session-sso.md)
- [Enable TLS Between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md)
- [Password Management](/password-management.md)
- [Secure TiDB Dashboard](/dashboard/dashboard-ops-security.md)

### init_connect

Referenced in:

- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)
- [TiDB 5.0.4 Release Notes](/releases/release-5.0.4.md)
- [TiDB 4.0.14 Release Notes](/releases/release-4.0.14.md)

### innodb_lock_wait_timeout

Referenced in:

- [Pessimistic Transaction Model](/pessimistic-transaction.md)
- [TiKV Configuration File](/tikv-configuration-file.md)
- [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md)
- [TiDB 3.0.6 Release Notes](/releases/release-3.0.6.md)

### interactive_timeout

Referenced in:

- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [TiDB Cluster Management FAQs](/faq/manage-cluster-faq.md)
- [Timeouts in TiDB](/develop/dev-guide-timeouts-in-tidb.md)
- [TiDB 3.0 GA Release Notes](/releases/release-3.0-ga.md)
- [TiDB 3.0 Beta Release Notes](/releases/release-3.0-beta.md)

### last_insert_id

Referenced in:

- [AUTO_RANDOM](/auto-random.md)
- [Connect to TiDB with mysql2](/develop/dev-guide-sample-application-ruby-mysql2.md)
- [Information Functions](/functions-and-operators/information-functions.md)
- [SQL Prepared Execution Plan Cache](/sql-prepared-plan-cache.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 3.1.0-rc Release Notes](/releases/release-3.1.0-rc.md)
- [TiDB 2.1.17 Release Notes](/releases/release-2.1.17.md)
- [TiDB 2.1 RC2 Release Notes](/releases/release-2.1-rc.2.md)

### last_plan_from_binding

Referenced in:

- [SQL Plan Management (SPM)](/sql-plan-management.md)
- [TiDB 4.0.12 Release Notes](/releases/release-4.0.12.md)

### last_plan_from_cache

Referenced in:

- [Index Selection](/choose-index.md)
- [SQL Non-Prepared Execution Plan Cache](/sql-non-prepared-plan-cache.md)
- [SQL Prepared Execution Plan Cache](/sql-prepared-plan-cache.md)
- [TiDB 4.0.2 Release Notes](/releases/release-4.0.2.md)

### last_sql_use_alloc

Referenced in:

- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### license

Referenced in:

- [TiDB Data Migration Overview](/dm/dm-overview.md)

### max_allowed_packet

Referenced in:

- [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md)
- [Handle Errors in TiDB Data Migration](/dm/dm-error-handling.md)
- [Limited SQL features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB Data Migration FAQs](/dm/dm-faq.md)
- [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [TiDB 5.2.4 Release Notes](/releases/release-5.2.4.md)
- [TiDB 3.0.2 Release Notes](/releases/release-3.0.2.md)
- [TiDB 2.1.5 Release Notes](/releases/release-2.1.5.md)
- [TiDB 2.1 RC2 Release Notes](/releases/release-2.1-rc.2.md)
- [TiDB 2.0.6 Release Notes](/releases/release-2.0.6.md)

### max_connections

Referenced in:

- [Integrate TiDB with ProxySQL](/develop/dev-guide-proxysql-integration.md)
- [Modify Configuration Dynamically](/dynamic-config.md)
- [Precheck Errors, Migration Errors, and Alerts for Data Migration](https://docs.pingcap.com/tidbcloud/tidb-cloud-dm-precheck-and-troubleshooting)
- [TiDB Cluster Management FAQs](/faq/manage-cluster-faq.md)
- [TiDB Configuration File](/tidb-configuration-file.md)

### max_execution_time

Referenced in:

- [Best Practices for Developing Java Applications with TiDB](/best-practices/java-app-best-practices.md)
- [Connection Pools and Connection Parameters](/develop/dev-guide-connection-parameters.md)
- [Optimizer Hints](/optimizer-hints.md)
- [SQL FAQs](/faq/sql-faq.md)
- [SQL Plan Management (SPM)](/sql-plan-management.md)
- [SQL Prepared Execution Plan Cache](/sql-prepared-plan-cache.md)
- [Timeouts in TiDB](/develop/dev-guide-timeouts-in-tidb.md)
- [Troubleshoot TiDB OOM Issues](/troubleshoot-tidb-oom.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)
- [TiDB 4.0.2 Release Notes](/releases/release-4.0.2.md)
- [TiDB 2.1.14 Release Notes](/releases/release-2.1.14.md)

### max_prepared_stmt_count

Referenced in:

- [The `PREPARE` SQL Statement](/sql-statements/sql-statement-prepare.md)
- [Troubleshoot TiDB OOM Issues](/troubleshoot-tidb-oom.md)
- [TiDB 6.5.2 Release Notes](/releases/release-6.5.2.md)

### mpp_exchange_compression_mode

Referenced in:

- [Explain Statements in the MPP Mode](/explain-mpp.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)

### mpp_version

Referenced in:

- [Explain Statements in the MPP Mode](/explain-mpp.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)

### password_history

Referenced in:

- [Password Management](/password-management.md)
- [The `mysql` Schema](/mysql-schema/mysql-schema.md)
- [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### password_reuse_interval

Referenced in:

- [Password Management](/password-management.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### pd_enable_follower_handle_region

Referenced in:

- [Tune Region Performance](/tune-region-performance.md)
- [TiDB Features](/basic-features.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)

### plugin_dir

Referenced in:

- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)

### plugin_load

Referenced in:

- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)

### port

Referenced in:

- [Migrate Data from SQL Files to TiDB](/migrate-from-sql-files-to-tidb.md)
- [TiFlash Deployment Topology](/tiflash-deployment-topology.md)
- [TSO Configuration File](/tso-configuration-file.md)

<!-- ### rand_seed1

Referenced in:

- No direct references found

### rand_seed2

Referenced in:

- No direct references found -->

### require_secure_transport

Referenced in:

<CustomContent platform="tidb-cloud">

- [Limited SQL features on TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB Cloud Release Notes in 2022](/tidb-cloud/release-notes-2022.md)
- [TLS Connections to TiDB Cloud Dedicated](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)

</CustomContent>

<CustomContent platform="tidb">

- [Enable TLS Between Clients and Servers](/enable-tls-between-clients-and-servers.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)
- [TiDB 7.5.1 Release Notes](/releases/release-7.5.1.md)
- [TiDB 7.1.2 Release Notes](/releases/release-7.1.2.md)
- [TiDB 6.5.6 Release Notes](/releases/release-6.5.6.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

</CustomContent>

<!-- ### skip_name_resolve

Referenced in:

- No direct references found -->

### socket

Referenced in:

- [Best Practices for Using HAProxy in TiDB](/best-practices/haproxy-best-practices.md)
- [SHOW CONFIG](/sql-statements/sql-statement-show-config.md)

### sql_mode

Referenced in:

- [Aggregate (GROUP BY) Functions](/functions-and-operators/aggregate-group-by-functions.md)
- [Date and Time Types](/data-type-date-and-time.md)
- [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md)
- [Handle Unstable Result Set Errors](/develop/dev-guide-unstable-result-set.md)
- [Maintain DM Clusters Using OpenAPI](/dm/dm-open-api.md)
- [Miscellaneous Functions](/functions-and-operators/miscellaneous-functions.md)
- [Partitioning](/partitioned-table.md)
- [Precision Math](/functions-and-operators/precision-math.md)
- [Privilege Management](/privilege-management.md)
- [Schema Object Names](/schema-object-names.md)
- [`SET [GLOBAL|SESSION] <variable>`](/sql-statements/sql-statement-set-variable.md)
- [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md)
- [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)
- [SQL FAQs](/faq/sql-faq.md)
- [SQL Mode](/sql-mode.md)
- [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md)
- [TiFlash Query Result Materialization](/tiflash/tiflash-results-materialization.md)
- [User Account Management](/user-account-management.md)
- [Use TiDB to Read TiFlash Replicas](/tiflash/use-tidb-to-read-tiflash.md)

### sql_require_primary_key

Referenced in:

- [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### sql_select_limit

Referenced in:

- [SQL Prepared Execution Plan Cache](/sql-prepared-plan-cache.md)
- [TiDB 4.0.2 Release Notes](/releases/release-4.0.2.md)

### ssl_ca

Referenced in:

- [Certificate-Based Authentication for Login](/certificate-authentication.md)
- [Connect to TiDB with Django](/develop/dev-guide-sample-application-python-django.md)
- [Connect to TiDB with MySQL Connector/Python](/develop/dev-guide-sample-application-python-mysql-connector.md)
- [Connect to TiDB with mysql2](/develop/dev-guide-sample-application-ruby-mysql2.md)
- [Connect to TiDB with mysql.js](/develop/dev-guide-sample-application-nodejs-mysqljs.md)
- [Connect to TiDB with node-mysql2](/develop/dev-guide-sample-application-nodejs-mysql2.md)
- [Connect to TiDB with peewee](/develop/dev-guide-sample-application-python-peewee.md)
- [Connect to TiDB with Prisma](/develop/dev-guide-sample-application-nodejs-prisma.md)
- [Connect to TiDB with PyMySQL](/develop/dev-guide-sample-application-python-pymysql.md)
- [Connect to TiDB with SQLAlchemy](/develop/dev-guide-sample-application-python-sqlalchemy.md)
- [Connect to TiDB with TypeORM](/develop/dev-guide-sample-application-nodejs-typeorm.md)
- [Get Started with TiDB + AI via Python](/vector-search-get-started-using-python.md)
- [Integrate TiDB Vector Search with Jina AI Embeddings API](/vector-search-integrate-with-jinaai-embedding.md)
- [Integrate Vector Search with LangChain](/vector-search-integrate-with-langchain.md)
- [Integrate Vector Search with LlamaIndex](/vector-search-integrate-with-llamaindex.md)
- [Integrate Vector Search with SQLAlchemy](/vector-search-integrate-with-sqlalchemy.md)

### ssl_cert

Referenced in:

- [Certificate-Based Authentication for Login](/certificate-authentication.md)

### ssl_key

Referenced in:

- [Certificate-Based Authentication for Login](/certificate-authentication.md)

### system_time_zone

Referenced in:

- [Configure Time Zone](/configure-time-zone.md)
- [TiDB 3.0.8 Release Notes](/releases/release-3.0.8.md)

### time_zone

Referenced in:

- [Configure Time Zone](/configure-time-zone.md)
- [Date and Time Types](/data-type-date-and-time.md)
- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [SQL Prepared Execution Plan Cache](/sql-prepared-plan-cache.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)
- [TiDB 2.1.8 Release Notes](/releases/release-2.1.8.md)

### tidb_adaptive_closest_read_threshold

Referenced in:

- [Follower Read](/follower-read.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### tidb_allow_tiflash_cop

Referenced in:

- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)

### tidb_allow_batch_cop

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs. v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)
- [TiDB 4.0.3 Release Notes](/releases/release-4.0.3.md)
- [TiDB 4.0.0-rc.2 Release Notes](/releases/release-4.0.0-rc.2.md)

### tidb_allow_fallback_to_tikv

Referenced in:

- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)

### tidb_allow_function_for_expression_index

Referenced in:

- [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB Features](/basic-features.md)

### tidb_allow_mpp

Referenced in:

- [Explain Statements in the MPP Mode](/explain-mpp.md)
- [Explore HTAP](/explore-htap.md)
- [TiDB TPC-H Performance Test Report -- v5.4](/benchmark/v5.4-performance-benchmarking-with-tpch.md)
- [TiFlash Query Result Materialization](/tiflash/tiflash-results-materialization.md)
- [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### tidb_allow_remove_auto_inc

Referenced in:

- [Auto-increment](/auto-increment.md)
- [Known Incompatibility Issues with Third-Party Tools](/develop/dev-guide-third-party-tools-compatibility.md)
- [MySQL Compatibility](/mysql-compatibility.md)
- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.4 Release Notes](/releases/release-3.0.4.md)
- [TiDB 2.1.18 Release Notes](/releases/release-2.1.18.md)

### tidb_analyze_column_options

Referenced in:

- [How to Run CH-benCHmark Test on TiDB](/benchmark/benchmark-tidb-using-ch.md)
- [Stress Test TiDB Using TiUP Bench Component](/tiup/tiup-bench.md)
- [TiDB Performance Tuning Configuration](/tidb-performance-tuning-config.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)

### tidb_analyze_distsql_scan_concurrency

Referenced in:

- [TiDB 8.2.0 Release Notes](/releases/release-8.2.0.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)

### tidb_analyze_partition_concurrency

Referenced in:

- [Statistics](/statistics.md)
- [TiDB 8.4.0 Release Notes](/releases/release-8.4.0.md)
- [TiDB 8.2.0 Release Notes](/releases/release-8.2.0.md)
- [TiDB 8.1.1 Release Notes](/releases/release-8.1.1.md)
- [TiDB 7.5.3 Release Notes](/releases/release-7.5.3.md)
- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)

### tidb_analyze_version

Referenced in:

- [ANALYZE_STATUS](/information-schema/information-schema-analyze-status.md)
- [SHOW ANALYZE STATUS](/sql-statements/sql-statement-show-analyze-status.md)
- [Statistics](/statistics.md)
- [TiDB Memory Control](/configure-memory-usage.md)
- [Troubleshoot TiDB OOM Issues](/troubleshoot-tidb-oom.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)
- [TiDB 5.2.4 Release Notes](/releases/release-5.2.4.md)
- [TiDB 5.1.4 Release Notes](/releases/release-5.1.4.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)

### tidb_analyze_skip_column_types

Referenced in:

- [Statistics](/statistics.md)
- [TiDB 8.2.0 Release Notes](/releases/release-8.2.0.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)

### tidb_auto_analyze_end_time

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [Statistics](/statistics.md)
- [TiDB Troubleshooting Map](/tidb-troubleshooting-map.md)
- [Troubleshoot Increased Read and Write Latency](/troubleshoot-cpu-issues.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)

### tidb_auto_analyze_partition_batch_size

Referenced in:

- [Statistics](/statistics.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_auto_analyze_ratio

Referenced in:

- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)
- [TiDB 2.1.8 Release Notes](/releases/release-2.1.8.md)

### tidb_auto_analyze_start_time

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [Statistics](/statistics.md)
- [TiDB Troubleshooting Map](/tidb-troubleshooting-map.md)
- [Troubleshoot Increased Read and Write Latency](/troubleshoot-cpu-issues.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)

### tidb_auto_build_stats_concurrency

Referenced in:

- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### tidb_backoff_lock_fast

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)

### tidb_backoff_weight

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.3 Release Notes](/releases/release-3.0.3.md)

### tidb_batch_commit

Referenced in:

- [TiDB 3.0 GA Release Notes](/releases/release-3.0-ga.md)
- [TiDB 3.0 Beta Release Notes](/releases/release-3.0-beta.md)

### tidb_batch_delete

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)

### tidb_batch_insert

Referenced in:

- [TiDB 2.0.6 Release Notes](/releases/release-2.0.6.md)

<!-- ### tidb_batch_pending_tiflash_count

Referenced in:

- No direct references found -->

### tidb_broadcast_join_threshold_count

Referenced in:

- [Explain Statements in the MPP Mode](/explain-mpp.md)
- [Tune TiFlash Performance](/tiflash/tune-tiflash-performance.md)
- [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### tidb_broadcast_join_threshold_size

Referenced in:

- [Explain Statements in the MPP Mode](/explain-mpp.md)
- [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)
- [Tune TiFlash Performance](/tiflash/tune-tiflash-performance.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### tidb_build_stats_concurrency

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [Statistics](/statistics.md)
- [TiDB Cloud TPC-C Performance Test Report for TiDB v8.1.0](https://docs.pingcap.com/tidbcloud/v8.5-performance-benchmarking-with-tpcc)
- [TiDB Cloud TPC-C Performance Test Report for TiDB v7.5.0](https://docs.pingcap.com/tidbcloud/v7.5-performance-benchmarking-with-tpcc)
- [TiDB Cloud TPC-C Performance Test Report for TiDB v7.1.3](https://docs.pingcap.com/tidbcloud/v7.1-performance-benchmarking-with-tpcc)
- [TiDB Cloud TPC-C Performance Test Report for TiDB v6.5.6](https://docs.pingcap.com/tidbcloud/v6.5-performance-benchmarking-with-tpcc)
- [TiDB TPC-H Performance Test Report — v4.0 vs. v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)
- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)

### tidb_build_sampling_stats_concurrency

Referenced in:

- [Statistics](/statistics.md)
- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)

### tidb_capture_plan_baselines

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [SQL Plan Management (SPM)](/sql-plan-management.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB 4.0.0-rc.1 Release Notes](/releases/release-4.0.0-rc.1.md)

### tidb_cdc_write_source

Referenced in:

- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### tidb_check_mb4_value_in_utf8

Referenced in:

- [Character Sets and Collations](/character-set-and-collation.md)
- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [Upgrade and After Upgrade FAQs](/faq/upgrade-faq.md)

### tidb_checksum_table_concurrency

Referenced in:

- [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md)
- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)

### tidb_committer_concurrency

Referenced in:

<CustomContent platform="tidb">

- [TiDB Monitoring Metrics](/grafana-tidb-dashboard.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [TiDB Cloud Release Notes in 2022](/tidb-cloud/release-notes-2022.md)

</CustomContent>

### tidb_config

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)
- [TiDB 1.1 Beta Release Notes](/releases/release-1.1-beta.md)

### tidb_constraint_check_in_place

Referenced in:

- [COMMIT](/sql-statements/sql-statement-commit.md)
- [Constraints](/constraints.md)
- [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md)
- [Error Codes and Troubleshooting](/error-codes.md)
- [Pessimistic Transaction Mode](/pessimistic-transaction.md)
- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [Transaction Overview](/transaction-overview.md)
- [TiDB 2.1.5 Release Notes](/releases/release-2.1.5.md)

### tidb_constraint_check_in_place_pessimistic

Referenced in:

- [Constraints](/constraints.md)
- [Error Codes and Troubleshooting](/error-codes.md)
- [Modify Configuration Dynamically](/dynamic-config.md)
- [Pessimistic Transaction Mode](/pessimistic-transaction.md)
- [SAVEPOINT](/sql-statements/sql-statement-savepoint.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### tidb_cost_model_version

Referenced in:

- [TiDB Cost Model](/cost-model.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)

### tidb_current_ts

Referenced in:

- [Timestamp Oracle in TiDB](/tso.md)
- [External Timestamp in TiDB](/tidb-external-ts.md)
- [Disaster Recovery Secondary Cluster](/dr-secondary-cluster.md)
- [TiDB Specific Functions](/functions-and-operators/tidb-functions.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [FLASHBACK CLUSTER | TiDB SQL Statement Reference](/sql-statements/sql-statement-flashback-cluster.md)
- [Check Upstream and Downstream Versions](/ticdc/ticdc-upstream-downstream-check.md)
- [SHOW BUILTINS | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-builtins.md)
- [TiCDC FAQs](/ticdc/ticdc-faq.md)

### tidb_ddl_disk_quota

Referenced in:

- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [TiDB Distributed Execution Framework](/tidb-distributed-execution-framework.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### tidb_ddl_enable_fast_reorg

Referenced in:

- [Basic Features](/basic-features.md)
- [Hardware and Software Requirements](/hardware-and-software-requirements.md)
- [IMPORT INTO | TiDB SQL Statement Reference](/sql-statements/sql-statement-import-into.md)
- [ADMIN SHOW DDL | TiDB SQL Statement Reference](/sql-statements/sql-statement-admin-show-ddl.md)
- [CREATE INDEX | TiDB SQL Statement Reference](/sql-statements/sql-statement-create-index.md)
- [TiDB Distributed Execution Framework](/tidb-distributed-execution-framework.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [Check Environment Before Deployment](/check-before-deployment.md)
- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)
- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 8.1.2 Release Notes](/releases/release-8.1.2.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### tidb_ddl_error_count_limit

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [SQL FAQs](/faq/sql-faq.md)
- [TiDB Distributed Execution Framework](/tidb-distributed-execution-framework.md)

### tidb_ddl_flashback_concurrency

Referenced in:

- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_ddl_reorg_batch_size

Referenced in:

- [TiDB DDL](/ddl-introduction.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [CREATE INDEX | TiDB SQL Statement Reference](/sql-statements/sql-statement-create-index.md)
- [ADMIN ALTER DDL | TiDB SQL Statement Reference](/sql-statements/sql-statement-admin-alter-ddl.md)
- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [SQL FAQs](/faq/sql-faq.md)
- [TiDB Distributed Execution Framework](/tidb-distributed-execution-framework.md)
- [SQL Plan Management Best Practices](/explain-walkthrough.md)

### tidb_ddl_reorg_priority

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [CREATE INDEX | TiDB SQL Statement Reference](/sql-statements/sql-statement-create-index.md)
- [Limited SQL Features on TiDB Cloud](https://docs.pingcap.com/tidbcloud/limited-sql-features)
- [SQL FAQs](/faq/sql-faq.md)
- [TiDB Distributed Execution Framework](/tidb-distributed-execution-framework.md)

### tidb_ddl_reorg_worker_cnt

Referenced in:

- [TiDB DDL](/ddl-introduction.md)
- [Troubleshoot CPU Issues](/troubleshoot-cpu-issues.md)
- [CREATE INDEX | TiDB SQL Statement Reference](/sql-statements/sql-statement-create-index.md)
- [ADMIN SHOW DDL | TiDB SQL Statement Reference](/sql-statements/sql-statement-admin-show-ddl.md)
- [ADMIN ALTER DDL | TiDB SQL Statement Reference](/sql-statements/sql-statement-admin-alter-ddl.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [SQL Plan Management Best Practices](/explain-walkthrough.md)
- [SQL FAQs](/faq/sql-faq.md)
- [TiDB Cloud Limited SQL Features](/tidb-cloud/limited-sql-features.md)
- [SQL Best Practices](/develop/dev-guide-optimize-sql-best-practices.md)
- [TiDB Distributed Execution Framework](/tidb-distributed-execution-framework.md)
- [Online Workloads and ADD INDEX Operations](/benchmark/online-workloads-and-add-index-operations.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)
- [TiDB 2.1.4 Release Notes](/releases/release-2.1.4.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)
- [TiDB 3.0.3 Release Notes](/releases/release-3.0.3.md)

### tidb_ddl_reorg_max_write_speed

Referenced in:

- [ADMIN ALTER DDL | TiDB SQL Statement Reference](/sql-statements/sql-statement-admin-alter-ddl.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)

### tidb_enable_dist_task

Referenced in:

- [TiDB 8.1.0 Release Notes](/releases/release-8.1.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [Upgrade TiDB Using TiUP](/smooth-upgrade-tidb.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)
- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)
- [IMPORT INTO | TiDB SQL Statement Reference](/sql-statements/sql-statement-import-into.md)
- [ADMIN SHOW DDL | TiDB SQL Statement Reference](/sql-statements/sql-statement-admin-show-ddl.md)
- [ADMIN ALTER DDL | TiDB SQL Statement Reference](/sql-statements/sql-statement-admin-alter-ddl.md)
- [TiDB Global Sort](/tidb-global-sort.md)
- [TiDB Distributed Execution Framework](/tidb-distributed-execution-framework.md)

### tidb_cloud_storage_uri

Referenced in:

- [TiDB 8.1.1 Release Notes](/releases/release-8.1.1.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)
- [IMPORT INTO | TiDB SQL Statement Reference](/sql-statements/sql-statement-import-into.md)
- [TiDB Global Sort](/tidb-global-sort.md)

### tidb_default_string_match_selectivity

Referenced in:

- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)

### tidb_disable_txn_auto_retry

Referenced in:

- [TiDB Optimistic Transaction Model](/optimistic-transaction.md)
- [TiDB Transaction Overview](/transaction-overview.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.0-rc.2 Release Notes](/releases/release-3.0.0-rc.2.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)
- [TiDB 3.0 GA Release Notes](/releases/release-3.0-ga.md)
- [TiDB 2.1 GA Release Notes](/releases/release-2.1-ga.md)
- [TiDB 2.0.5 Release Notes](/releases/release-2.0.5.md)
- [TiDB 2.1 Beta Release Notes](/releases/release-2.1-beta.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)
- [TiDB TPC-C Performance Test Report -- v3.0 vs v2.1](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)
- [How to Test TiDB Using Sysbench](/benchmark/benchmark-tidb-using-sysbench.md)
- [TiDB TPC-C Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpcc.md)

### tidb_distsql_scan_concurrency

Referenced in:

- [TiDB Best Practices](/best-practices/tidb-best-practices.md)
- [Dumpling Overview](/dumpling-overview.md)
- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md)
- [INFORMATION_SCHEMA SLOW_QUERY Table](/information-schema/information-schema-slow-query.md)
- [Statistics in TiDB](/statistics.md)
- [Configure Memory Usage](/configure-memory-usage.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [SQL FAQs](/faq/sql-faq.md)
- [TiDB Cloud v8.1 TPC-C Performance Test Report](/tidb-cloud/v8.1-performance-benchmarking-with-tpcc.md)
- [TiDB Cloud v7.5 TPC-C Performance Test Report](/tidb-cloud/v7.5-performance-benchmarking-with-tpcc.md)
- [TiDB Cloud v7.1 TPC-C Performance Test Report](/tidb-cloud/v7.1-performance-benchmarking-with-tpcc.md)
- [TiDB Cloud v6.5 TPC-C Performance Test Report](/tidb-cloud/v6.5-performance-benchmarking-with-tpcc.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_dml_batch_size

Referenced in:

- [LOAD DATA | TiDB SQL Statement Reference](/sql-statements/sql-statement-load-data.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)
- [TiDB 4.0.0-beta Release Notes](/releases/release-4.0.0-beta.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)

### tidb_dml_type

Referenced in:

- [Identify Slow Queries](/identify-expensive-queries.md)
- [TiDB Performance Tuning Methods](/tidb-performance-tuning-config.md)
- [IMPORT INTO vs TiDB Lightning](/tidb-lightning/import-into-vs-tidb-lightning.md)
- [Basic Features](/basic-features.md)
- [Configure Memory Usage](/configure-memory-usage.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)
- [TiDB 8.4.0 Release Notes](/releases/release-8.4.0.md)
- [TiDB 8.1.0 Release Notes](/releases/release-8.1.0.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)

### tidb_enable_1pc

Referenced in:

- [Transaction Overview](/transaction-overview.md)
- [Basic Features](/basic-features.md)
- [TiDB Cluster Management FAQs](/faq/manage-cluster-faq.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB Sysbench Performance Test Report - v5.0 vs. v4.0](/benchmark/benchmark-sysbench-v5-vs-v4.md)
- [TiDB Sysbench Performance Test Report - v5.4.0 vs. v5.3.0](/benchmark/benchmark-sysbench-v5.4.0-vs-v5.3.0.md)
- [TiDB Sysbench Performance Test Report - v5.1.0 vs. v5.0.2](/benchmark/benchmark-sysbench-v5.1.0-vs-v5.0.2.md)
- [TiDB Sysbench Performance Test Report - v6.2.0 vs. v6.1.0](/benchmark/benchmark-sysbench-v6.2.0-vs-v6.1.0.md)
- [TiDB Sysbench Performance Test Report - v6.0.0 vs. v5.4.0](/benchmark/benchmark-sysbench-v6.0.0-vs-v5.4.0.md)
- [TiDB Sysbench Performance Test Report - v6.1.0 vs. v6.0.0](/benchmark/benchmark-sysbench-v6.1.0-vs-v6.0.0.md)
- [TiDB v5.4 TPC-C Performance Test Report](/benchmark/v5.4-performance-benchmarking-with-tpcc.md)
- [TiDB v5.2 TPC-C Performance Test Report](/benchmark/v5.2-performance-benchmarking-with-tpcc.md)
- [TiDB v5.3 TPC-C Performance Test Report](/benchmark/v5.3-performance-benchmarking-with-tpcc.md)
- [TiDB v5.0 TPC-C Performance Test Report](/benchmark/v5.0-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report - v5.3.0 vs. v5.2.2](/benchmark/benchmark-sysbench-v5.3.0-vs-v5.2.2.md)
- [TiDB v5.1 TPC-C Performance Test Report](/benchmark/v5.1-performance-benchmarking-with-tpcc.md)
- [TiDB v6.2 TPC-C Performance Test Report](/benchmark/v6.2-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report - v5.2.0 vs. v5.1.1](/benchmark/benchmark-sysbench-v5.2.0-vs-v5.1.1.md)
- [TiDB v6.0 TPC-C Performance Test Report](/benchmark/v6.0-performance-benchmarking-with-tpcc.md)
- [TiDB v6.1 TPC-C Performance Test Report](/benchmark/v6.1-performance-benchmarking-with-tpcc.md)

### tidb_enable_async_commit

Referenced in:

- [Transaction Overview](/transaction-overview.md)
- [Basic Features](/basic-features.md)
- [TiDB Cluster Management FAQs](/faq/manage-cluster-faq.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 5.0.0-rc Release Notes](/releases/release-5.0.0-rc.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB Sysbench Performance Test Report - v5.0 vs. v4.0](/benchmark/benchmark-sysbench-v5-vs-v4.md)
- [TiDB Sysbench Performance Test Report - v5.4.0 vs. v5.3.0](/benchmark/benchmark-sysbench-v5.4.0-vs-v5.3.0.md)
- [TiDB Sysbench Performance Test Report - v5.1.0 vs. v5.0.2](/benchmark/benchmark-sysbench-v5.1.0-vs-v5.0.2.md)
- [TiDB Sysbench Performance Test Report - v6.2.0 vs. v6.1.0](/benchmark/benchmark-sysbench-v6.2.0-vs-v6.1.0.md)
- [TiDB Sysbench Performance Test Report - v6.0.0 vs. v5.4.0](/benchmark/benchmark-sysbench-v6.0.0-vs-v5.4.0.md)
- [TiDB Sysbench Performance Test Report - v6.1.0 vs. v6.0.0](/benchmark/benchmark-sysbench-v6.1.0-vs-v6.0.0.md)
- [TiDB v5.4 TPC-C Performance Test Report](/benchmark/v5.4-performance-benchmarking-with-tpcc.md)
- [TiDB v5.2 TPC-C Performance Test Report](/benchmark/v5.2-performance-benchmarking-with-tpcc.md)
- [TiDB v5.3 TPC-C Performance Test Report](/benchmark/v5.3-performance-benchmarking-with-tpcc.md)
- [TiDB v5.0 TPC-C Performance Test Report](/benchmark/v5.0-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report - v5.3.0 vs. v5.2.2](/benchmark/benchmark-sysbench-v5.3.0-vs-v5.2.2.md)
- [TiDB v5.1 TPC-C Performance Test Report](/benchmark/v5.1-performance-benchmarking-with-tpcc.md)
- [TiDB v6.2 TPC-C Performance Test Report](/benchmark/v6.2-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report - v5.2.0 vs. v5.1.1](/benchmark/benchmark-sysbench-v5.2.0-vs-v5.1.1.md)
- [TiDB v6.0 TPC-C Performance Test Report](/benchmark/v6.0-performance-benchmarking-with-tpcc.md)
- [TiDB v6.1 TPC-C Performance Test Report](/benchmark/v6.1-performance-benchmarking-with-tpcc.md)

### tidb_enable_analyze_snapshot

Referenced in:

- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)

### tidb_enable_auto_analyze

Referenced in:

- [TiDB Performance Tuning Methods](/tidb-performance-tuning-config.md)
- [SQL Plan Replayer User Guide](/sql-plan-replayer.md)
- [Statistics in TiDB](/statistics.md)
- [SQL FAQs](/faq/sql-faq.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_enable_auto_analyze_priority_queue

Referenced in:

- [Statistics in TiDB](/statistics.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)
- [TiDB 8.4.0 Release Notes](/releases/release-8.4.0.md)
- [TiDB 8.2.0 Release Notes](/releases/release-8.2.0.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)
- [TiDB 8.1.0 Release Notes](/releases/release-8.1.0.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)

### tidb_enable_auto_increment_in_generated

Referenced in:

- [CREATE INDEX | TiDB SQL Statement Reference](/sql-statements/sql-statement-create-index.md)
- [TiDB 5.2.0 Release Notes](/releases/release-5.2.0.md)

### tidb_enable_batch_dml

Referenced in:

- [TiDB Cloud Release Notes - 2022](/tidb-cloud/release-notes-2022.md)

### tidb_enable_cascades_planner

Referenced in:

- [Basic Features](/basic-features.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0 Beta Release Notes](/releases/release-3.0-beta.md)

### tidb_enable_check_constraint

Referenced in:

- [INFORMATION_SCHEMA TIDB_CHECK_CONSTRAINTS Table](/information-schema/information-schema-tidb-check-constraints.md)
- [INFORMATION_SCHEMA CHECK_CONSTRAINTS Table](/information-schema/information-schema-check-constraints.md)
- [Constraints](/constraints.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)

### tidb_enable_chunk_rpc

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_enable_clustered_index

Referenced in:

- [Clustered Indexes](/clustered-indexes.md)
- [Backup & Restore Overview](/br/backup-and-restore-overview.md)
- [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 5.0.0-rc Release Notes](/releases/release-5.0.0-rc.md)
- [TiDB 5.0 GA Release Notes](/releases/release-5.0.0.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)
- [Schema Design Overview](/develop/dev-guide-schema-design-overview.md)
- [Create a Table](/develop/dev-guide-create-table.md)
- [TiDB TPC-C Performance Test Report -- v6.1 vs. v6.0](/benchmark/v6.1-performance-benchmarking-with-tpcc.md)
- [TiDB TPC-C Performance Test Report -- v5.3 vs. v5.2](/benchmark/v5.3-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report -- v6.0.0 vs. v5.4.0](/benchmark/benchmark-sysbench-v6.0.0-vs-v5.4.0.md)
- [TiDB Sysbench Performance Test Report -- v5.4.0 vs. v5.3.0](/benchmark/benchmark-sysbench-v5.4.0-vs-v5.3.0.md)
- [TiDB Sysbench Performance Test Report -- v5.1.0 vs. v5.0.2](/benchmark/benchmark-sysbench-v5.1.0-vs-v5.0.2.md)
- [TiDB Sysbench Performance Test Report -- v5.0 vs. v4.0](/benchmark/benchmark-sysbench-v5-vs-v4.md)
- [TiDB Sysbench Performance Test Report -- v6.2.0 vs. v6.1.0](/benchmark/benchmark-sysbench-v6.2.0-vs-v6.1.0.md)
- [TiDB TPC-C Performance Test Report -- v5.4 vs. v5.3](/benchmark/v5.4-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report -- v6.1.0 vs. v6.0.0](/benchmark/benchmark-sysbench-v6.1.0-vs-v6.0.0.md)
- [TiDB TPC-C Performance Test Report -- v5.2 vs. v5.1](/benchmark/v5.2-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report -- v5.3.0 vs. v5.2.2](/benchmark/benchmark-sysbench-v5.3.0-vs-v5.2.2.md)
- [TiDB TPC-C Performance Test Report -- v5.0 vs. v4.0](/benchmark/v5.0-performance-benchmarking-with-tpcc.md)
- [TiDB TPC-C Performance Test Report -- v5.1 vs. v5.0](/benchmark/v5.1-performance-benchmarking-with-tpcc.md)

### tidb_enable_ddl

Referenced in:

- [Dynamic Configuration](/dynamic-config.md)
- [Topology Reference](/tiup/tiup-cluster-topology-reference.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB Configuration File](/tidb-configuration-file.md)

### tidb_enable_collect_execution_info

Referenced in:

- [Dynamic Configuration](/dynamic-config.md)
- [INFORMATION_SCHEMA TIDB_INDEX_USAGE Table](/information-schema/information-schema-tidb-index-usage.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Identify Slow Queries](/identify-slow-queries.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 7.5.1 Release Notes](/releases/release-7.5.1.md)
- [TiDB 4.0.2 Release Notes](/releases/release-4.0.2.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)

### tidb_enable_column_tracking

Referenced in:

- [TiDB 8.2.0 Release Notes](/releases/release-8.2.0.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)

### tidb_enable_enhanced_security

Referenced in:

- [TiDB Dashboard User Guide](/dashboard/dashboard-user.md)
- [Basic Features](/basic-features.md)
- [BACKUP | TiDB SQL Statement Reference](/sql-statements/sql-statement-backup.md)
- [IMPORT INTO | TiDB SQL Statement Reference](/sql-statements/sql-statement-import-into.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)

### tidb_enable_exchange_partition

Referenced in:

- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### tidb_enable_extended_stats

Referenced in:

- [Extended Statistics](/extended-statistics.md)

### tidb_enable_external_ts_read

Referenced in:

- [External Timestamp Read](/tidb-external-ts.md)
- [Secondary Cluster for Disaster Recovery](/dr-secondary-cluster.md)
- [Check Data Consistency Between Upstream and Downstream](/ticdc/ticdc-upstream-downstream-check.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_enable_fast_analyze

Referenced in:

- [Basic Features](/basic-features.md)
- [Extended Statistics](/extended-statistics.md)
- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)
- [TiDB 3.0.0-rc.1 Release Notes](/releases/release-3.0.0-rc.1.md)

### tidb_enable_fast_table_check

Referenced in:

- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)

### tidb_enable_foreign_key

Referenced in:

- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)

### tidb_enable_gc_aware_memory_track

Referenced in:

- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### tidb_enable_global_index

Referenced in:

- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)
- [TiDB 8.4.0 Release Notes](/releases/release-8.4.0.md)

### tidb_enable_lazy_cursor_fetch

Referenced in:

- [Best Practices for Developing Java Applications with TiDB](/best-practices/java-app-best-practices.md)
- [Connection Parameters](/develop/dev-guide-connection-parameters.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)

### tidb_enable_non_prepared_plan_cache

Referenced in:

- [Performance Tuning Methods](/tidb-performance-tuning-config.md)
- [Non-Prepared Plan Cache](/sql-non-prepared-plan-cache.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)

### tidb_enable_non_prepared_plan_cache_for_dml

Referenced in:

- [Non-Prepared Plan Cache](/sql-non-prepared-plan-cache.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### tidb_enable_noop_functions

Referenced in:

- [Information Functions](/functions-and-operators/information-functions.md)
- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [SELECT](/sql-statements/sql-statement-select.md)
- [Pessimistic Transaction Model](/pessimistic-transaction.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)

### tidb_enable_noop_variables

Referenced in:

- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)

### tidb_enable_null_aware_anti_join

Referenced in:

- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)

### tidb_enable_outer_join_reorder

Referenced in:

- [Join Reorder](/join-reorder.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 6.1.1 Release Notes](/releases/release-6.1.1.md)

### tidb_enable_parallel_apply

Referenced in:

- [TiDB 7.1.1 Release Notes](/releases/release-7.1.1.md)
- [TiDB 6.5.4 Release Notes](/releases/release-6.5.4.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)
- [TiDB 5.4.1 Release Notes](/releases/release-5.4.1.md)

### tidb_enable_pipelined_window_function

Referenced in:

- [Window Functions](/functions-and-operators/window-functions.md)

### tidb_enable_plan_replayer_capture

Referenced in:

- [SQL Plan Management](/sql-plan-replayer.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)

### tidb_enable_plan_replayer_continuous_capture

Referenced in:

- [SQL Plan Management](/sql-plan-replayer.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)

### tidb_enable_prepared_plan_cache

Referenced in:

- [Prepared Plan Cache](/sql-prepared-plan-cache.md)
- [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md)
- [TiDB Cloud Release Notes - 2022](/tidb-cloud/release-notes-2022.md)
- [TiDB 7.5.1 Release Notes](/releases/release-7.5.1.md)
- [TiDB 7.1.4 Release Notes](/releases/release-7.1.4.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [How to Test TiDB Using Sysbench](/benchmark/benchmark-tidb-using-sysbench.md)

### tidb_enable_prepared_plan_cache_memory_monitor

Referenced in:

- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_enable_pseudo_for_outdated_stats

Referenced in:

- [SQL FAQs](/faq/sql-faq.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### tidb_enable_rate_limit_action

Referenced in:

- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md)
- [Configure Memory Usage](/configure-memory-usage.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### tidb_enable_reuse_chunk

Referenced in:

- [TiDB 6.5.1 Release Notes](/releases/release-6.5.1.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_enable_row_level_checksum

Referenced in:

- [TiDB Functions](/functions-and-operators/tidb-functions.md)
- [Data Integrity Check](/ticdc/ticdc-integrity-check.md)
- [TiDB 7.5.1 Release Notes](/releases/release-7.5.1.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)

### tidb_enable_slow_log

Referenced in:

- [TiDB Dashboard Slow Query Page](/dashboard/dashboard-slow-query.md)
- [Identify Slow Queries](/identify-slow-queries.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Dynamic Configuration](/dynamic-config.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB Configuration File](/tidb-configuration-file.md)

### tidb_enable_stmt_summary

Referenced in:

- [SQL Plan Management](/sql-plan-management.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Statement Summary Tables](/statement-summary-tables.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 3.0.4 Release Notes](/releases/release-3.0.4.md)

### tidb_enable_strict_double_type_check

Referenced in:

- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)

### tidb_enable_table_partition

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.8 Release Notes](/releases/release-3.0.8.md)
- [TiDB 4.0.13 Release Notes](/releases/release-4.0.13.md)
- [TiDB 8.4.0 Release Notes](/releases/release-8.4.0.md)

### tidb_enable_telemetry

Referenced in:

- [TiDB 6.1.5 Release Notes](/releases/release-6.1.5.md)
- [TiDB 6.5.1 Release Notes](/releases/release-6.5.1.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)
- [TiDB 8.1.0 Release Notes](/releases/release-8.1.0.md)

### tidb_enable_tiflash_read_for_write_stmt

Referenced in:

- [Use TiDB to Read TiFlash](/tiflash/use-tidb-to-read-tiflash.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### tidb_enable_top_sql

Referenced in:

- [Top SQL](/dashboard/top-sql.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)

### tidb_enable_tso_follower_proxy

Referenced in:

- [PD Microservices](/pd-microservices.md)
- [Basic Features](/basic-features.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)
- [TiDB 5.3.0 Release Notes](/releases/release-5.3.0.md)

### tidb_enable_vectorized_expression

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 5.0.6 Release Notes](/releases/release-5.0.6.md)
- [TiDB 5.1.4 Release Notes](/releases/release-5.1.4.md)
- [TiDB 4.0.16 Release Notes](/releases/release-4.0.16.md)
- [TiDB 5.2.4 Release Notes](/releases/release-5.2.4.md)
- [TiDB 5.4.1 Release Notes](/releases/release-5.4.1.md)

### tidb_enforce_mpp

Referenced in:

- [TiFlash Results Materialization](/tiflash/tiflash-results-materialization.md)
- [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)
- [Troubleshoot TiFlash](/tiflash/troubleshoot-tiflash.md)
- [Tune TiFlash Performance](/tiflash/tune-tiflash-performance.md)
- [Stale Read](/stale-read.md)
- [Explore HTAP](/explore-htap.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)
- [TiDB 5.0.4 Release Notes](/releases/release-5.0.4.md)
- [TiDB 5.1.5 Release Notes](/releases/release-5.1.5.md)
- [TiDB 5.4.2 Release Notes](/releases/release-5.4.2.md)

### tidb_executor_concurrency

Referenced in:

- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)
- [TiDB 8.2.0 Release Notes](/releases/release-8.2.0.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)

### tidb_expensive_query_time_threshold

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Identify Slow Queries](/identify-expensive-queries.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [Dynamic Configuration](/dynamic-config.md)
- [TiDB Configuration File](/tidb-configuration-file.md)

### tidb_external_ts

Referenced in:

- [External Timestamp Read](/tidb-external-ts.md)
- [Secondary Cluster for Disaster Recovery](/dr-secondary-cluster.md)
- [Stale Read](/stale-read.md)
- [Check Data Consistency Between Upstream and Downstream](/ticdc/ticdc-upstream-downstream-check.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_force_priority

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [SQL FAQs](/faq/sql-faq.md)
- [Dynamic Configuration](/dynamic-config.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 2.1.5 Release Notes](/releases/release-2.1.5.md)
- [TiDB 2.1 RC3 Release Notes](/releases/release-2.1-rc.3.md)

### tidb_gc_concurrency

Referenced in:

- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [GC Configuration](/garbage-collection-configuration.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)

### tidb_gc_enable

Referenced in:

- [TiDB Troubleshooting Map](/tidb-troubleshooting-map.md)
- [Migrate Data from TiDB to TiDB](/migrate-from-tidb-to-tidb.md)
- [Secondary Cluster for Disaster Recovery](/dr-secondary-cluster.md)
- [Migrate Data from TiDB to MySQL](/migrate-from-tidb-to-mysql.md)
- [Replicate Data Between Primary and Secondary Clusters](/replicate-between-primary-and-secondary-clusters.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [Migrate from Self-Hosted TiDB to TiDB Cloud](/tidb-cloud/migrate-from-op-tidb.md)
- [GC Configuration](/garbage-collection-configuration.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)

### tidb_gc_life_time

Referenced in:

- [TiKV In-Memory Engine](/tikv-in-memory-engine.md)
- [TiDB Troubleshooting Map](/tidb-troubleshooting-map.md)
- [Error Codes and Troubleshooting](/error-codes.md)
- [Dumpling Overview](/dumpling-overview.md)
- [Back up and Restore Incrementally](/br/br-incremental-guide.md)
- [Read Historical Data](/read-historical-data.md)
- [FLASHBACK TABLE | TiDB SQL Statement Reference](/sql-statements/sql-statement-flashback-table.md)
- [FLASHBACK DATABASE | TiDB SQL Statement Reference](/sql-statements/sql-statement-flashback-database.md)
- [FLASHBACK CLUSTER | TiDB SQL Statement Reference](/sql-statements/sql-statement-flashback-cluster.md)
- [SQL FAQs](/faq/sql-faq.md)
- [Create a Changefeed with TiDB Cloud as Downstream](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)
- [Replicate Data to Kafka](/ticdc/ticdc-sink-to-kafka.md)
- [TiCDC FAQs](/ticdc/ticdc-faq.md)
- [Create a Changefeed with MySQL as Downstream](/tidb-cloud/changefeed-sink-to-mysql.md)
- [GC Configuration](/garbage-collection-configuration.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB 6.1.1 Release Notes](/releases/release-6.1.1.md)
- [Use Stale Read](/develop/dev-guide-use-stale-read.md)
- [Timeouts in TiDB](/develop/dev-guide-timeouts-in-tidb.md)

### tidb_gc_run_interval

Referenced in:

- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [GC Configuration](/garbage-collection-configuration.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)

### tidb_gc_scan_lock_mode

Referenced in:

- [GC Overview](/garbage-collection-overview.md)
- [Basic Features](/basic-features.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [GC Configuration](/garbage-collection-configuration.md)
- [TiDB 5.0.4 Release Notes](/releases/release-5.0.4.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)

### tidb_general_log

Referenced in:

- [TiDB Data Migration FAQs](/dm/dm-faq.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Command-Line Flags](/command-line-flags-for-tidb-configuration.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)

<!-- ### tidb_hash_exchange_with_new_collation

Referenced in:

- No direct references found -->

### tidb_hash_join_concurrency

Referenced in:

- [Three Nodes Hybrid Deployment](/best-practices/three-nodes-hybrid-deployment.md)
- [Analyze Slow Queries](/analyze-slow-queries.md)
- [Explain Joins](/explain-joins.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)

### tidb_hashagg_final_concurrency

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB v5.1 TPC-C Performance Test Report](/benchmark/v5.1-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report - v6.1.0 vs. v6.0.0](/benchmark/benchmark-sysbench-v6.1.0-vs-v6.0.0.md)
- [TiDB Sysbench Performance Test Report - v5.0 vs. v4.0](/benchmark/benchmark-sysbench-v5-vs-v4.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)
- [TiDB TPC-C Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpcc.md)
- [TiDB v5.0 TPC-C Performance Test Report](/benchmark/v5.0-performance-benchmarking-with-tpcc.md)

### tidb_hashagg_partial_concurrency

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB v5.1 TPC-C Performance Test Report](/benchmark/v5.1-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report - v6.1.0 vs. v6.0.0](/benchmark/benchmark-sysbench-v6.1.0-vs-v6.0.0.md)
- [TiDB Sysbench Performance Test Report - v5.0 vs. v4.0](/benchmark/benchmark-sysbench-v5-vs-v4.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)
- [TiDB TPC-C Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpcc.md)
- [TiDB v5.0 TPC-C Performance Test Report](/benchmark/v5.0-performance-benchmarking-with-tpcc.md)

<!-- ### tidb_host_lookup_max_retries

Referenced in:

- No direct references found -->

### tidb_ignore_prepared_cache_close_stmt

Referenced in:

- [TiDB Performance Tuning Methods](/tidb-performance-tuning-config.md)
- [Prepared Plan Cache](/sql-prepared-plan-cache.md)
- [Performance Tuning Best Practices](/performance-tuning-practices.md)
- [Performance Tuning Methods](/performance-tuning-methods.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)

<!-- ### tidb_ignore_index_hint

Referenced in:

- No direct references found -->

### tidb_index_join_batch_size

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Explain Joins](/explain-joins.md)

### tidb_index_lookup_concurrency

Referenced in:

- [TiDB Best Practices](/best-practices/tidb-best-practices.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)

### tidb_index_lookup_join_concurrency

Referenced in:

- [Three Nodes Hybrid Deployment](/best-practices/three-nodes-hybrid-deployment.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Explain Joins](/explain-joins.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)

### tidb_index_lookup_size

Referenced in:

- [TiDB Best Practices](/best-practices/tidb-best-practices.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_index_serial_scan_concurrency

Referenced in:

- [TiDB Best Practices](/best-practices/tidb-best-practices.md)
- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md)
- [Statistics in TiDB](/statistics.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Cloud v6.5 TPC-C Performance Test Report](/tidb-cloud/v6.5-performance-benchmarking-with-tpcc.md)
- [TiDB Cloud v7.1 TPC-C Performance Test Report](/tidb-cloud/v7.1-performance-benchmarking-with-tpcc.md)
- [TiDB Cloud v7.5 TPC-C Performance Test Report](/tidb-cloud/v7.5-performance-benchmarking-with-tpcc.md)
- [TiDB Cloud v8.1 TPC-C Performance Test Report](/tidb-cloud/v8.1-performance-benchmarking-with-tpcc.md)

### tidb_init_chunk_size

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Transaction Isolation Levels](/transaction-isolation-levels.md)
- [TiDB 3.0 Beta Release Notes](/releases/release-3.0-beta.md)

### tidb_isolation_read_engines

Referenced in:

- [TiUP Bench Reference](/tiup/tiup-bench.md)
- [Use TiDB to Read TiFlash](/tiflash/use-tidb-to-read-tiflash.md)
- [Use FastScan](/tiflash/use-fastscan.md)
- [TiFlash Compatibility](/tiflash/tiflash-compatibility.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [Use HTAP Cluster](/tidb-cloud/use-htap-cluster.md)
- [TiDB 4.0.2 Release Notes](/releases/release-4.0.2.md)
- [TiDB v5.4 TPC-H Performance Test Report](/benchmark/v5.4-performance-benchmarking-with-tpch.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)

<!-- ### tidb_last_txn_info

Referenced in:

- No direct references found -->

### tidb_max_auto_analyze_time

Referenced in:

- [Statistics in TiDB](/statistics.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_max_chunk_size

Referenced in:

- [TiDB Performance Tuning Methods](/tidb-performance-tuning-config.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Transaction Isolation Levels](/transaction-isolation-levels.md)
- [TiDB 2.0.9 Release Notes](/releases/release-2.0.9.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)
- [TiDB 7.1.3 Release Notes](/releases/release-7.1.3.md)
- [TiDB 6.5.7 Release Notes](/releases/release-6.5.7.md)
- [TiDB 7.5.1 Release Notes](/releases/release-7.5.1.md)

### tidb_max_delta_schema_count

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [SQL FAQs](/faq/sql-faq.md)
- [TiDB 2.1.18 Release Notes](/releases/release-2.1.18.md)
- [TiDB 3.0.5 Release Notes](/releases/release-3.0.5.md)

<!-- ### tidb_max_disk_usage

Referenced in:

- No direct references found

### tidb_max_disk_quota

Referenced in:

- No direct references found

### tidb_max_txn_ttl

Referenced in:

- No direct references found -->

### tidb_mem_oom_action

Referenced in:

- [Configure Memory Usage](/configure-memory-usage.md)
- [Non-transactional DML](/non-transactional-dml.md)
- [TiDB Cloud Release Notes - 2022](/tidb-cloud/release-notes-2022.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [TiDB 8.1.0 Release Notes](/releases/release-8.1.0.md)

### tidb_mem_quota_analyze

Referenced in:

- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md)
- [Statistics in TiDB](/statistics.md)
- [TiDB 7.1.6 Release Notes](/releases/release-7.1.6.md)
- [TiDB 7.5.2 Release Notes](/releases/release-7.5.2.md)
- [TiDB 6.5.10 Release Notes](/releases/release-6.5.10.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [TiDB 8.1.0 Release Notes](/releases/release-8.1.0.md)

<!-- ### tidb_mem_quota_apply_cache

Referenced in:

- No direct references found -->

### tidb_mem_quota_binding_cache

Referenced in:

- [SQL Plan Management](/sql-plan-management.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)

### tidb_mem_quota_indexlookupjoin

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)

### tidb_mem_quota_nestedloopapply

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_mem_quota_query

Referenced in:

- [Enable Disk Spill Encryption](/enable-disk-spill-encrypt.md)
- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md)
- [TiDB Troubleshooting Map](/tidb-troubleshooting-map.md)
- [Error Codes and Troubleshooting](/error-codes.md)
- [Contribute to TiDB Documentation](/CONTRIBUTING.md)
- [TiFlash Results Materialization](/tiflash/tiflash-results-materialization.md)
- [Identify Slow Queries](/identify-expensive-queries.md)
- [Explain Joins](/explain-joins.md)
- [Configure Memory Usage](/configure-memory-usage.md)
- [Non-transactional DML](/non-transactional-dml.md)
- [Optimizer Hints](/optimizer-hints.md)
- [TiDB Cloud Release Notes - 2022](/tidb-cloud/release-notes-2022.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 4.0.10 Release Notes](/releases/release-4.0.10.md)
- [TiDB 7.1.6 Release Notes](/releases/release-7.1.6.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)
- [TiDB 6.5.7 Release Notes](/releases/release-6.5.7.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 8.1.2 Release Notes](/releases/release-8.1.2.md)
- [TiDB 7.6.0 Release Notes](/releases/release-7.6.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)
- [TiDB 6.5.4 Release Notes](/releases/release-6.5.4.md)
- [TiDB 7.1.4 Release Notes](/releases/release-7.1.4.md)
- [TiDB 7.1.1 Release Notes](/releases/release-7.1.1.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)
- [TiDB 6.5.11 Release Notes](/releases/release-6.5.11.md)
- [TiDB 7.5.4 Release Notes](/releases/release-7.5.4.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_mem_quota_sort

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)

### tidb_merge_join_concurrency

Referenced in:

- [System Variables](/system-variables.md)

### tidb_merge_partition_stats_concurrency

Referenced in:

- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)
- [TiDB 7.1.4 Release Notes](/releases/release-7.1.4.md)
- [TiDB 6.5.9 Release Notes](/releases/release-6.5.9.md)

### tidb_metric_query_range_duration

Referenced in:

- [Monitoring API](/metrics-schema.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)

### tidb_metric_query_step

Referenced in:

- [Monitoring API](/metrics-schema.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)

### tidb_multi_statement_mode

Referenced in:

- [Error Codes and Troubleshooting](/error-codes.md)
- [TiDB 5.1.1 Release Notes](/releases/release-5.1.1.md)
- [TiDB 7.1.4 Release Notes](/releases/release-7.1.4.md)
- [TiDB 5.2.0 Release Notes](/releases/release-5.2.0.md)
- [Integrate TiDB Cloud with n8n](/tidb-cloud/integrate-tidbcloud-with-n8n.md)
- [TiDB 5.0.3 Release Notes](/releases/release-5.0.3.md)
- [TiDB 4.0.14 Release Notes](/releases/release-4.0.14.md)
- [TiDB 6.5.8 Release Notes](/releases/release-6.5.8.md)
- [TiDB 7.5.1 Release Notes](/releases/release-7.5.1.md)

### tidb_nontransactional_ignore_error

Referenced in:

- [Non-transactional DML](/non-transactional-dml.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_opt_agg_push_down

Referenced in:

- [TiDB Performance Tuning Methods](/tidb-performance-tuning-config.md)
- [Tune TiFlash Performance](/tiflash/tune-tiflash-performance.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 5.4.2 Release Notes](/releases/release-5.4.2.md)
- [TiDB 6.1.7 Release Notes](/releases/release-6.1.7.md)
- [TiDB 5.1.5 Release Notes](/releases/release-5.1.5.md)
- [TiDB 6.5.4 Release Notes](/releases/release-6.5.4.md)
- [TiDB 7.1.1 Release Notes](/releases/release-7.1.1.md)
- [TiDB 4.0 GA Release Notes](/releases/release-4.0-ga.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)

<!-- ### tidb_opt_broadcast_cartesian_join

Referenced in:

- No direct references found -->

### tidb_opt_concurrency_factor

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_opt_correlation_exp_factor

Referenced in:

- [Extended Statistics](/extended-statistics.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.0-rc.1 Release Notes](/releases/release-3.0.0-rc.1.md)

### tidb_opt_correlation_threshold

Referenced in:

- [Extended Statistics](/extended-statistics.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_opt_desc_factor

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_opt_distinct_agg_push_down

Referenced in:

- [TiDB Performance Tuning Methods](/tidb-performance-tuning-config.md)
- [Tune TiFlash Performance](/tiflash/tune-tiflash-performance.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Distinct Optimization](/agg-distinct-optimization.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)

### tidb_opt_enable_correlation_adjustment

Referenced in:

- [TiDB 5.2.0 Release Notes](/releases/release-5.2.0.md)

### tidb_opt_insubq_to_join_and_agg

Referenced in:

- [Subquery Optimization](/subquery-optimization.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Optimizer Hints](/optimizer-hints.md)
- [TiDB 3.0 Beta Release Notes](/releases/release-3.0-beta.md)

### tidb_opt_join_reorder_threshold

Referenced in:

- [Join Reorder](/join-reorder.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.0-rc.1 Release Notes](/releases/release-3.0.0-rc.1.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_opt_limit_push_down_threshold

Referenced in:

- [TiDB 5.2.0 Release Notes](/releases/release-5.2.0.md)

### tidb_opt_memory_factor

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_opt_network_factor

Referenced in:

- [Choose Indexes](/choose-index.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_opt_objective

Referenced in:

- [TiDB 8.0.0 Release Notes](/releases/release-8.0.0.md)
- [TiDB 7.5.2 Release Notes](/releases/release-7.5.2.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)

### tidb_opt_prefix_index_single_scan

Referenced in:

- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_opt_range_max_size

Referenced in:

- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)

### tidb_opt_scan_factor

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_opt_seek_factor

Referenced in:

- [Choose Indexes](/choose-index.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_opt_skew_distinct_agg

Referenced in:

- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)

<!-- ### tidb_opt_tiflash_concurrency_factor

Referenced in:

- No direct references found -->

### tidb_opt_write_row_id

Referenced in:

- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 2.1 RC5 Release Notes](/releases/release-2.1-rc.5.md)

### tidb_optimizer_selectivity_level

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)

### tidb_partition_prune_mode

Referenced in:

- [Prepared Plan Cache](/sql-prepared-plan-cache.md)
- [Partitioned Table](/partitioned-table.md)
- [Use MPP Mode](/tiflash/use-tiflash-mpp-mode.md)
- [TiDB 8.1.0 Release Notes](/releases/release-8.1.0.md)
- [TiDB 5.1.0 Release Notes](/releases/release-5.1.0.md)
- [TiDB 8.5.0 Release Notes](/releases/release-8.5.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiFlash Upgrade Guide](/tiflash-upgrade-guide.md)

### tidb_pprof_sql_cpu

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 3.0.10 Release Notes](/releases/release-3.0.10.md)

### tidb_prepared_plan_cache_memory_guard_ratio

Referenced in:

- [Prepared Plan Cache](/sql-prepared-plan-cache.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_prepared_plan_cache_size

Referenced in:

- [TiDB Cloud Release Notes - 2022](/tidb-cloud/release-notes-2022.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [TiDB 6.4.0 Release Notes](/releases/release-6.4.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB v6.2 TPC-C Performance Test Report](/benchmark/v6.2-performance-benchmarking-with-tpcc.md)
- [TiDB v6.1 TPC-C Performance Test Report](/benchmark/v6.1-performance-benchmarking-with-tpcc.md)
- [TiDB Sysbench Performance Test Report - v6.1.0 vs. v6.0.0](/benchmark/benchmark-sysbench-v6.1.0-vs-v6.0.0.md)
- [TiDB Sysbench Performance Test Report - v6.2.0 vs. v6.1.0](/benchmark/benchmark-sysbench-v6.2.0-vs-v6.1.0.md)

### tidb_projection_concurrency

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 5.0.0 Release Notes](/releases/release-5.0.0.md)
- [TiDB TPC-H Performance Test Report -- v4.0 vs v3.0](/benchmark/v4.0-performance-benchmarking-with-tpch.md)

### tidb_query_log_max_len

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Identify Slow Queries](/identify-slow-queries.md)
- [TiDB Cloud Release Notes - 2022](/tidb-cloud/release-notes-2022.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)
- [TiDB 2.1 RC5 Release Notes](/releases/release-2.1-rc.5.md)
- [TiDB 2.1 GA Release Notes](/releases/release-2.1-ga.md)

### tidb_read_staleness

Referenced in:

- [Stale Read](/stale-read.md)
- [Read Historical Data Using tidb_read_staleness](/tidb-read-staleness.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)
- [Use Stale Read](/develop/dev-guide-use-stale-read.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)

### tidb_replica_read

Referenced in:

- [Best Practices for TiDB Read-Only Nodes Deployment](/best-practices/readonly-nodes.md)
- [Three Data Centers Deployment Solution with Local Read](/best-practices/three-dc-local-read.md)
- [Best Practices for TiDB on Public Cloud Platforms](/best-practices-on-public-cloud.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Follower Read](/follower-read.md)
- [Optimizer Hints](/optimizer-hints.md)
- [Use Follower Read to Ensure Strongly Consistent Reads](/develop/dev-guide-use-follower-read.md)
- [TiDB 3.1.0-beta.2 Release Notes](/releases/release-3.1.0-beta.2.md)
- [TiDB 4.0.2 Release Notes](/releases/release-4.0.2.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)

### tidb_retry_limit

Referenced in:

- [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md)
- [TiDB Optimistic Transaction Model](/optimistic-transaction.md)
- [TiDB Transaction Overview](/transaction-overview.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md)
- [TiDB 2.1 GA Release Notes](/releases/release-2.1-ga.md)
- [TiDB 2.1 Beta Release Notes](/releases/release-2.1-beta.md)

### tidb_row_format_version

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.0-rc.1 Release Notes](/releases/release-3.0.0-rc.1.md)

### tidb_scatter_region

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 2.1 RC5 Release Notes](/releases/release-2.1-rc.5.md)

### tidb_schema_cache_size

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_session_alias

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_skip_ascii_check

Referenced in:

- [Character Set and Collation](/character-set-and-collation.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Configuration File](/tidb-configuration-file.md)

### tidb_skip_isolation_level_check

Referenced in:

- [Transaction Isolation Levels](/transaction-isolation-levels.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 3.0.0-rc.1 Release Notes](/releases/release-3.0.0-rc.1.md)

### tidb_skip_utf8_check

Referenced in:

- [Character Set and Collation](/character-set-and-collation.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 2.1 RC5 Release Notes](/releases/release-2.1-rc.5.md)

### tidb_slow_log_threshold

Referenced in:

- [Slow Query Page](/dashboard/dashboard-slow-query.md)
- [Identify Slow Queries](/identify-slow-queries.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 3.0.0-rc.1 Release Notes](/releases/release-3.0.0-rc.1.md)

### tidb_slow_query_file

Referenced in:

- [Identify Slow Queries](/identify-slow-queries.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Configuration File](/tidb-configuration-file.md)

### tidb_snapshot

Referenced in:

- [Read Historical Data](/read-historical-data.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [Stale Read](/stale-read.md)
- [Use Stale Read](/develop/dev-guide-use-stale-read.md)
- [TiDB 2.1 RC5 Release Notes](/releases/release-2.1-rc.5.md)

### tidb_stmt_summary_history_size

Referenced in:

- [Statement Summary Tables](/statement-summary-tables.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 4.0.0-rc.2 Release Notes](/releases/release-4.0.0-rc.2.md)

### tidb_stmt_summary_internal_query

Referenced in:

- [Statement Summary Tables](/statement-summary-tables.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 4.0.0-rc.2 Release Notes](/releases/release-4.0.0-rc.2.md)

### tidb_stmt_summary_max_sql_length

Referenced in:

- [Statement Summary Tables](/statement-summary-tables.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 4.0.0-rc.2 Release Notes](/releases/release-4.0.0-rc.2.md)

### tidb_stmt_summary_max_stmt_count

Referenced in:

- [Statement Summary Tables](/statement-summary-tables.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 4.0.0-rc.2 Release Notes](/releases/release-4.0.0-rc.2.md)

### tidb_stmt_summary_refresh_interval

Referenced in:

- [Statement Summary Tables](/statement-summary-tables.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 4.0.0-rc.2 Release Notes](/releases/release-4.0.0-rc.2.md)

### tidb_store_limit

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [TiDB 3.0.0-rc.1 Release Notes](/releases/release-3.0.0-rc.1.md)

### tidb_tbl_cache_size

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_tmp_table_max_size

Referenced in:

- [Temporary Tables](/temporary-tables.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 6.1.0 Release Notes](/releases/release-6.1.0.md)

### tidb_top_sql_max_meta_count

Referenced in:

- [Top SQL](/dashboard/top-sql.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)

### tidb_top_sql_max_time_series_count

Referenced in:

- [Top SQL](/dashboard/top-sql.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 5.4.0 Release Notes](/releases/release-5.4.0.md)

### tidb_txn_mode

Referenced in:

- [TiDB Transaction Overview](/transaction-overview.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md)
- [TiDB 3.0.8 Release Notes](/releases/release-3.0.8.md)

### tidb_use_plan_baselines

Referenced in:

- [SQL Plan Management](/sql-plan-management.md)
- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 4.0.0-rc.1 Release Notes](/releases/release-4.0.0-rc.1.md)

### tidb_wait_split_region_finish

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 2.1 RC5 Release Notes](/releases/release-2.1-rc.5.md)

### tidb_wait_split_region_timeout

Referenced in:

- [SHOW VARIABLES | TiDB SQL Statement Reference](/sql-statements/sql-statement-show-variables.md)
- [TiDB 2.1 RC5 Release Notes](/releases/release-2.1-rc.5.md)

### tidb_window_concurrency

Referenced in:

- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)

<!-- ### tidb_window_pipelined_threshold

Referenced in:

- No direct references found

### tidb_window_pipelined_threshold_size

Referenced in:

- No direct references found

### tidb_window_size

Referenced in:

- No direct references found -->

### tiflash_fastscan

Referenced in:

- [Use FastScan to Accelerate TiFlash Queries](/tiflash/use-fastscan.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)
- [TiDB 6.3.0 Release Notes](/releases/release-6.3.0.md)

### tiflash_fine_grained_shuffle_batch_size

Referenced in:

- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)

### tiflash_fine_grained_shuffle_stream_count

Referenced in:

- [Tune TiFlash Performance](/tiflash/tune-tiflash-performance.md)
- [TiDB 6.2.0 Release Notes](/releases/release-6.2.0.md)

### tiflash_mem_quota_query_per_node

Referenced in:

- [TiFlash Disk Spill](/tiflash/tiflash-spill-disk.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)

### tiflash_query_spill_ratio

Referenced in:

- [TiFlash Disk Spill](/tiflash/tiflash-spill-disk.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)

### tiflash_replica_read

Referenced in:

- [Basic Features](/basic-features.md)
- [Create TiFlash Replicas](/tiflash/create-tiflash-replicas.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)

### tiflash_hashagg_preaggregation_mode

Referenced in:

- [TiDB 8.3.0 Release Notes](/releases/release-8.3.0.md)

### tikv_client_read_timeout

Referenced in:

- [TiDB 7.5.1 Release Notes](/releases/release-7.5.1.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)

### time_zone

Referenced in:

- [Date and Time Types](/data-type-date-and-time.md)
- [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
- [Prepared Plan Cache](/sql-prepared-plan-cache.md)
- [Configure Time Zone](/configure-time-zone.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)
- [TiDB 2.1.8 Release Notes](/releases/release-2.1.8.md)
- [TiDB 3.0.8 Release Notes](/releases/release-3.0.8.md)

### timestamp

Referenced in:

- [Log Redaction](/log-redaction.md)
- [Time Service Overview](/tso.md)
- [Analyze Slow Queries](/analyze-slow-queries.md)
- [TiDB Optimistic Transaction Model](/optimistic-transaction.md)
- [Time To Live (TTL)](/time-to-live.md)
- [Dumpling Overview](/dumpling-overview.md)
- [Partitioned Table](/partitioned-table.md)
- [Back up and Restore a Snapshot of TiDB Cluster Data](/br/br-snapshot-manual.md)
- [Point-in-Time Recovery](/br/br-pitr-manual.md)
- [Back up and Restore Incremental Data](/br/br-incremental-guide.md)

### transaction_isolation

Referenced in:

- [SET TRANSACTION](/sql-statements/sql-statement-set-transaction.md)
- [Third-Party Tool Compatibility](/develop/dev-guide-third-party-tools-compatibility.md)
- [TiDB 6.0.0-DMR Release Notes](/releases/release-6.0.0-dmr.md)

### tx_isolation

Referenced in:

- [Performance Tuning Package](/performance-tuning-practices.md)

### txn_scope

Referenced in:

- [Resource Control](/tidb-resource-control.md)
- [TiDB Configuration File](/tidb-configuration-file.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)

### validate_password.check_user_name

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### validate_password.dictionary

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### validate_password.enable

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### validate_password.length

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)

### validate_password.mixed_case_count

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### validate_password.number_count

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### validate_password.policy

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### validate_password.special_char_count

Referenced in:

- [TiDB Password Management](/password-management.md)
- [Encryption and Compression Functions](/functions-and-operators/encryption-and-compression-functions.md)
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)

### version

Referenced in:

- [TiDB Tools User Guide](/ecosystem-tool-user-guide.md)
- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md)
- [Upgrade Monitoring Services](/upgrade-monitoring-services.md)
- [Foreign Key](/foreign-key.md)

<!-- ### version_compile_machine

Referenced in:

- No direct references found

### version_compile_os

Referenced in:

- No direct references found -->

### wait_timeout

Referenced in:

- [Best Practices for Java Applications](/best-practices/java-app-best-practices.md): Discusses setting wait_timeout for Java applications
- [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md): Mentions wait_timeout in context of lock wait timeouts
- [Troubleshoot Out of Memory Errors](/troubleshoot-tidb-oom.md): Suggests adjusting wait_timeout for connection pools
- [TiDB Cluster Management FAQs](/faq/manage-cluster-faq.md): Lists wait_timeout as a supported timeout
- [Connection Pools and Connection Parameters](/develop/dev-guide-connection-parameters.md): Details about wait_timeout configuration
- [Limited SQL Features in TiDB Cloud](/tidb-cloud/limited-sql-features.md): Notes read-only status in TiDB Cloud
- [Timeouts in TiDB](/develop/dev-guide-timeouts-in-tidb.md): Explains wait_timeout usage
- [TiDB 3.0 GA Release Notes](/releases/release-3.0-ga.md): Added wait_timeout system variable
- [TiDB 3.0 Beta Release Notes](/releases/release-3.0-beta.md): Added support for wait_timeout
- [TiProxy Overview](/tiproxy/tiproxy-overview.md): Describes connection handling with wait_timeout

### warning_count

Referenced in:

- [TiDB 2.1 RC1 Release Notes](/releases/release-2.1-rc.1.md)

### windowing_use_high_precision

Referenced in:

- [Window Functions](/functions-and-operators/window-functions.md)
