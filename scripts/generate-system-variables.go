package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/pingcap/tidb/sessionctx/variable"
)

func fmtDuration(d time.Duration) string {
	return d.String()
}

func ByteCountIEC(s string) string {
	b, _ := strconv.Atoi(s)
	const unit = 1024
	if b < unit {
		return fmt.Sprintf("%d B", b)
	}
	div, exp := int64(unit), 0
	for n := b / unit; n >= unit; n /= unit {
		div *= unit
		exp++
	}
	return fmt.Sprintf("%.0f %ciB",
		float64(b)/float64(div), "KMGTPE"[exp])
}

func formatDefaultValue(sv *variable.SysVar) string {
	switch sv.Name {
	case variable.SystemTimeZone:
		return "(system dependent)"
	case variable.Hostname:
		return "(system hostname)"
	case variable.Version:
		return "`5.7.25-TiDB-`(tidb version)"
	case variable.VersionComment:
		return "(string)"
	case variable.Socket:
		return `""` // TODO: need to fix this in the code.
	case variable.TiDBEnable1PC, variable.TiDBEnableAsyncCommit:
		return "`ON`" // These are OFF in the source, which is for OLD versions. For NEW its on.
	case variable.TiDBRowFormatVersion:
		return "`2`" // Same story, for old clusters it is 1.
	case variable.TiDBTxnMode:
		return "`pessimistic`"
	case variable.TiDBMemQuotaApplyCache, variable.TiDBMemQuotaQuery, variable.TiDBQueryLogMaxLen, variable.TiDBBCJThresholdSize:
		return fmt.Sprintf("`%s` (%s)", sv.Value, ByteCountIEC(sv.Value))
	case variable.DataDir:
		return "/tmp/tidb"
	case variable.LastInsertID:
		return "`0`"
	case variable.PluginDir:
		return `""`
	}
	if sv.Value == "" {
		return `""` // make it easier to read that it's an empty string default
	}
	return fmt.Sprintf("`%s`", sv.Value)
}

func skipSv(sv *variable.SysVar) bool {

	if sv.IsNoop {
		return true // don't document noops.
	}
	// These svs have no documentation yet.
	switch sv.Name {
	case variable.ErrorCount, variable.LowerCaseTableNames, variable.MaxPreparedStmtCount,
		variable.TiDBBatchCommit, variable.TiDBBatchDelete, variable.TiDBBatchInsert, variable.TiDBEnableChangeMultiSchema,
		variable.TiDBEnableExchangePartition, variable.TiDBEnableExtendedStats, variable.TiDBEnablePointGetCache,
		variable.TiDBEnableStreaming, variable.TiDBGuaranteeLinearizability, variable.TiDBTxnScope, variable.TiDBTxnReadTS,
		variable.TxnIsolationOneShot, variable.TiDBLastQueryInfo, variable.TiDBLastTxnInfo,
		variable.TiDBMemQuotaHashJoin, variable.TiDBStreamAggConcurrency, variable.TiDBTrackAggregateMemoryUsage, variable.TiDBOptBCJ,
		variable.TiDBOptConcurrencyFactor, variable.TiDBOptCopCPUFactor, variable.TiDBEnableIndexMergeJoin,
		variable.TiDBMemQuotaIndexLookupJoin, variable.TiDBMemQuotaIndexLookupReader, variable.TiDBMemQuotaMergeJoin,
		variable.TiDBEnableAlterPlacement, variable.TiDBSlowLogMasking, variable.TiDBShardAllocateStep, variable.TiDBMemQuotaTopn,
		variable.TiDBMemQuotaSort, variable.TiDBMergeJoinConcurrency, variable.TiDBOptCPUFactor, variable.TiDBOptDescScanFactor,
		variable.TiDBOptDiskFactor, variable.TiDBOptJoinReorderThreshold, variable.TiDBOptMemoryFactor, variable.TiDBOptNetworkFactor,
		variable.TiDBOptScanFactor, variable.TiDBOptTiFlashConcurrencyFactor, variable.TiDBOptimizerSelectivityLevel,
		variable.TiDBOptSeekFactor, variable.TiDBEnableTopSQL, variable.TiDBTopSQLPrecisionSeconds,
		variable.TiDBTopSQLMaxStatementCount, variable.TiDBEnableGlobalTemporaryTable, variable.TiDBEnablePipelinedWindowFunction, variable.TiDBOptCartesianBCJ,
		variable.TiDBEnableLocalTxn, variable.TiDBTopSQLMaxCollect, variable.TiDBTopSQLReportIntervalSeconds,
		variable.TiDBOptMPPOuterJoinFixedBuildSide, variable.TiDBRestrictedReadOnly, variable.TiDBMPPStoreFailTTL, variable.TiDBHashExchangeWithNewCollation,
		variable.TiDBEnableOrderedResultMode, variable.TiDBReadStaleness,
		variable.TiDBEnableMPPBalanceWithContinuousRegion, variable.TiDBEnableMPPBalanceWithContinuousRegionCount,
		"version_compile_os", "version_compile_machine":

		return true
	}
	return false
}

func printWarning(sv *variable.SysVar) string {

	switch sv.Name {
	case variable.TiDBHashJoinConcurrency, variable.TiDBHashAggFinalConcurrency, variable.TiDBHashAggPartialConcurrency,
		variable.TiDBIndexLookupConcurrency, variable.TiDBIndexLookupJoinConcurrency, variable.TiDBWindowConcurrency, variable.TiDBProjectionConcurrency:
		return "> **Warning:**\n>\n> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.\n\n"
	case variable.TiDBEnableListTablePartition:
		return "> **Warning:**\n>\n> Currently, List partition and List COLUMNS partition are experimental features. It is not recommended that you use it in the production environment.\n\n"
	case variable.TiDBGCScanLockMode:
		return "> **Warning:**\n>\n> Currently, Green GC is an experimental feature. It is not recommended that you use it in the production environment.\n\n"
	case variable.TiDBPartitionPruneMode:
		return "> **Warning:**\n\n> Currently, the dynamic pruning mode for partitioned tables is an experimental feature. It is not recommended that you use it in the production environment.\n\n"
	case variable.TiDBEnableCascadesPlanner:
		return "> **Warning:**\n>\n> Currently, cascades planner is an experimental feature. It is not recommended that you use it in the production environment.\n\n"
	case variable.TiDBEnableFastAnalyze:
		return "> **Warning:**\n>\n> Currently, `Fast Analyze` is an experimental feature. It is not recommended that you use it in the production environment.\n\n"

	}
	return ""
}

func printUnits(sv *variable.SysVar) string {
	switch sv.Name {
	case variable.TiDBMemQuotaApplyCache, variable.TiDBMemQuotaQuery, variable.TiDBQueryLogMaxLen, variable.TiDBBCJThresholdSize, variable.TMPTableSize, variable.MaxAllowedPacket:
		return "- Unit: Bytes\n"
	case variable.TiDBSlowLogThreshold, variable.MaxExecutionTime, variable.TiDBDDLSlowOprThreshold:
		return "- Unit: Milliseconds\n"
	case variable.InteractiveTimeout, variable.WaitTimeout, variable.TiDBStmtSummaryRefreshInterval, variable.TiDBWaitSplitRegionTimeout, variable.InnodbLockWaitTimeout,
		variable.TiDBMetricSchemaRangeDuration, variable.TiDBMetricSchemaStep, variable.TiDBEvolvePlanTaskMaxTime,
		variable.TiDBExpensiveQueryTimeThreshold:
		return "- Unit: Seconds\n"
	case variable.SQLSelectLimit, variable.TiDBBCJThresholdCount, variable.TiDBDDLReorgBatchSize,
		variable.TiDBDMLBatchSize, variable.TiDBIndexJoinBatchSize, variable.TiDBIndexLookupSize,
		variable.TiDBInitChunkSize, variable.TiDBMaxChunkSize:
		return "- Unit: Rows\n"
	case variable.TiDBBuildStatsConcurrency, variable.TiDBChecksumTableConcurrency, variable.TiDBDDLReorgWorkerCount,
		variable.TiDBDistSQLScanConcurrency, variable.TiDBExecutorConcurrency, variable.TiDBGCConcurrency, variable.TiDBHashJoinConcurrency,
		variable.TiDBHashAggFinalConcurrency, variable.TiDBHashAggPartialConcurrency, variable.TiDBIndexLookupConcurrency, variable.TiDBIndexLookupJoinConcurrency,
		variable.TiDBIndexSerialScanConcurrency, variable.TiDBProjectionConcurrency, variable.TiDBWindowConcurrency:
		return "- Unit: Threads\n"
	}
	return ""
}

func formatScope(sv *variable.SysVar) string {
	// Manually cater for "INSTANCE" scope, which is not a native concept.
	switch sv.Name {
	case variable.TiDBDDLSlowOprThreshold, variable.TiDBCheckMb4ValueInUTF8, variable.TiDBEnableCollectExecutionInfo,
		variable.TiDBEnableSlowLog, variable.TiDBExpensiveQueryTimeThreshold, variable.TiDBForcePriority, variable.TiDBGeneralLog,
		variable.TiDBSlowLogThreshold, variable.TiDBPProfSQLCPU, variable.TiDBQueryLogMaxLen, variable.TiDBRecordPlanInSlowLog,
		variable.TiDBMemoryUsageAlarmRatio, variable.PluginDir, variable.PluginLoad:
		return "INSTANCE"
	case variable.TiDBStoreLimit:
		return "INSTANCE | GLOBAL"
	}

	if sv.HasNoneScope() {
		return "NONE"
	}
	if sv.HasSessionScope() && sv.HasGlobalScope() {
		return "SESSION | GLOBAL"
	}
	if sv.HasGlobalScope() {
		return "GLOBAL"
	}
	return "SESSION"
}

func formatPossibleValues(sv *variable.SysVar) string {
	tmp := strings.Join(sv.PossibleValues, "`, `")
	return fmt.Sprintf("`%s`", tmp)
}

func formatSpecialVersionComment(sv *variable.SysVar) string {
	switch sv.Name {
	case variable.TiDBAllowAutoRandExplicitInsert:
		return ` <span class="version-mark">New in v4.0.3</span>`
	case variable.TiDBFoundInPlanCache, variable.TiDBFoundInBinding, variable.TiDBCapturePlanBaseline, variable.TiDBEnableChunkRPC,
		variable.TiDBEnableIndexMerge, variable.TiDBEnableNoopFuncs, variable.TiDBEnableVectorizedExpression, variable.TiDBAllowBatchCop,
		variable.TiDBEvolvePlanBaselines, variable.TiDBEvolvePlanTaskMaxTime, variable.TiDBEvolvePlanTaskStartTime, variable.TiDBEvolvePlanTaskEndTime,
		variable.TiDBIsolationReadEngines, variable.TiDBMetricSchemaRangeDuration, variable.TiDBMetricSchemaStep, variable.TiDBPProfSQLCPU,
		variable.TiDBReplicaRead, variable.TiDBStmtSummaryHistorySize, variable.TiDBStmtSummaryInternalQuery, variable.TiDBStmtSummaryMaxSQLLength,
		variable.TiDBStmtSummaryMaxStmtCount, variable.TiDBStmtSummaryRefreshInterval, variable.TiDBUsePlanBaselines, variable.TiDBWindowConcurrency:
		return ` <span class="version-mark">New in v4.0</span>`
	case variable.SQLSelectLimit, variable.TiDBEnableTelemetry:
		return ` <span class="version-mark">New in v4.0.2</span>`
	case variable.TiDBAllowFallbackToTiKV, variable.TiDBAllowMPPExecution, variable.TiDBBCJThresholdCount, variable.TiDBBCJThresholdSize,
		variable.TiDBEnableAsyncCommit, variable.TiDBEnable1PC, variable.TiDBEnableClusteredIndex, variable.TiDBEnableParallelApply,
		variable.TiDBEnableStrictDoubleTypeCheck, variable.TiDBEnableListTablePartition, variable.TiDBExecutorConcurrency,
		variable.TiDBGCEnable, variable.TiDBGCRunInterval, variable.TiDBGCLifetime, variable.TiDBGCConcurrency, variable.TiDBGCScanLockMode,
		variable.TiDBMemQuotaApplyCache, variable.TiDBOptPreferRangeScan, variable.TiDBSkipASCIICheck:
		return ` <span class="version-mark">New in v5.0</span>`
	case variable.TiDBAllowRemoveAutoInc:
		return ` <span class="version-mark">New in v2.1.18 and v3.0.4</span>`
	case variable.TiDBEnableAmendPessimisticTxn:
		return ` <span class="version-mark">New in v4.0.7</span>`
	case variable.TiDBEnableStmtSummary:
		return ` <span class="version-mark">New in v3.0.4</span>`
	case variable.TiDBMaxDeltaSchemaCount:
		return ` <span class="version-mark">New in v2.1.18 and v3.0.5</span>`
	case variable.TiDBMultiStatementMode:
		return ` <span class="version-mark">New in v4.0.11</span>`
	case variable.TiDBStoreLimit:
		return ` <span class="version-mark">New in v3.0.4 and v4.0</span>`
	case variable.TiDBPartitionPruneMode, variable.TiDBEnforceMPPExecution:
		return ` <span class="version-mark">New in v5.1</span>`
	case variable.TiDBAnalyzeVersion:
		return ` <span class="version-mark">New in v5.1.0</span>`
	case variable.SkipNameResolve:
		return ` <span class="version-mark">New in v5.2.0</span>`
	default:
		return ""
	}
}

func getExtendedDescription(sv *variable.SysVar) string {

	switch sv.Name {
	case variable.TiDBAllowAutoRandExplicitInsert:
		return "- Determines whether to allow explicitly specifying the values of the column with the `AUTO_RANDOM` attribute in the `INSERT` statement."
	case variable.AutoIncrementIncrement:
		return "- Controls the step size of `AUTO_INCREMENT` values to be allocated to a column. It is often used in combination with `auto_increment_offset`."
	case variable.AutoIncrementOffset:
		return "- Controls the initial offset of `AUTO_INCREMENT` values to be allocated to a column. This setting is often used in combination with `auto_increment_increment`. For example:\n" +
			"\n" +
			"```sql\n" +
			"mysql> CREATE TABLE t1 (a int not null primary key auto_increment);\n" +
			"Query OK, 0 rows affected (0.10 sec)\n" +
			"\n" +
			"mysql> set auto_increment_offset=1;\n" +
			"Query OK, 0 rows affected (0.00 sec)\n" +
			"\n" +
			"mysql> set auto_increment_increment=3;\n" +
			"Query OK, 0 rows affected (0.00 sec)\n" +
			"\n" +
			"mysql> INSERT INTO t1 VALUES (),(),(),();\n" +
			"Query OK, 4 rows affected (0.04 sec)\n" +
			"Records: 4  Duplicates: 0  Warnings: 0\n" +
			"\n" +
			"mysql> SELECT * FROM t1;\n" +
			"+----+\n" +
			"| a  |\n" +
			"+----+\n" +
			"|  1 |\n" +
			"|  4 |\n" +
			"|  7 |\n" +
			"| 10 |\n" +
			"+----+\n" +
			"4 rows in set (0.00 sec)\n" +
			"```"
	case variable.AutoCommit:
		return "- Controls whether statements should automatically commit when not in an explicit transaction. See [Transaction Overview](/transaction-overview.md#autocommit) for more information."
	case "ddl_slow_threshold":
		return "- Log DDL operations whose execution time exceeds the threshold value."
	case variable.ForeignKeyChecks:
		return "- For compatibility, TiDB returns foreign key checks as `OFF`."
	case variable.Hostname:
		return "- The hostname of the TiDB server as a read-only variable."
	case variable.InnodbLockWaitTimeout:
		return "- The lock wait timeout for pessimistic transactions (default)."
	case variable.InteractiveTimeout:
		return "- This variable represents the idle timeout of the interactive user session. Interactive user session refers to the session established by calling [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API using the `CLIENT_INTERACTIVE` option (for example, MySQL Shell and MySQL Client). This variable is fully compatible with MySQL."
	case variable.TiDBFoundInBinding:
		return "- This variable is used to show whether the execution plan used in the previous statement was influenced by a [plan binding](/sql-plan-management.md)"
	case variable.TiDBFoundInPlanCache:
		return "- This variable is used to show whether the execution plan used in the previous `execute` statement is taken directly from the plan cache."
	case variable.MaxExecutionTime:
		return "- The maximum execution time of a statement. The default value is unlimited (zero).\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> Unlike in MySQL, the `max_execution_time` system variable currently works on all kinds of statements in TiDB, not only restricted to the `SELECT` statement. The precision of the timeout value is roughly 100ms. This means the statement might not be terminated in accurate milliseconds as you specify."
	case variable.Port:
		return "- The port that the `tidb-server` is listening on when speaking the MySQL protocol."
	case variable.Socket:
		return "- The local unix socket file that the `tidb-server` is listening on when speaking the MySQL protocol."
	case variable.SQLModeVar:
		return "- This variable controls a number of MySQL compatibility behaviors. See [SQL Mode](/sql-mode.md) for more information."
	case variable.SQLSelectLimit:
		return "- The maximum number of rows returned by the `SELECT` statements."
	case variable.SystemTimeZone:
		return "- This variable shows the system time zone from when TiDB was first bootstrapped. See also [`time_zone`](#time_zone)."
	case variable.WaitTimeout:
		return "- This variable controls the idle timeout of user sessions. A zero-value means unlimited."
	case variable.WindowingUseHighPrecision:
		return "- This variable controls whether to use the high precision mode when computing the window functions."
	case variable.TiDBAllowBatchCop:
		return "- This variable is used to control how TiDB sends a coprocessor request to TiFlash. It has the following values:\n" +
			"\n" +
			"    * `0`: Never send requests in batches\n" +
			"    * `1`: Aggregation and join requests are sent in batches\n" +
			"    * `2`: All coprocessor requests are sent in batches"
	case "tidb_allow_fallback_to_tikv":
		return `- This variable is used to specify a list of storage engines that might fall back to TiKV. If the execution of a SQL statement fails due to a failure of the specified storage engine in the list, TiDB retries executing this SQL statement with TiKV. This variable can be set to "" or "tiflash". When this variable is set to "tiflash", if the execution of a SQL statement fails due to a failure of TiFlash, TiDB retries executing this SQL statement with TiKV.`
	case "tidb_allow_mpp":
		return "- Controls whether to use the MPP mode of TiFlash to execute queries. The value options are as follows:\n" +
			"    - `0` or `OFF`, which means that the MPP mode will not be used.\n" +
			"    - `1` or `ON`, which means that the optimizer determines whether to use the MPP mode based on the cost estimation (by default).\n\n" +
			"MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [Control whether to select the MPP mode](/tiflash/use-tiflash.md#control-whether-to-select-the-mpp-mode)."
	case variable.TiDBAllowRemoveAutoInc:
		return "- This variable is used to set whether the `AUTO_INCREMENT` property of a column is allowed to be removed by executing `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default."
	case variable.TiDBAutoAnalyzeEndTime:
		return "- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`."
	case variable.TiDBAutoAnalyzeRatio:
		return "- This variable is used to set the threshold when TiDB automatically executes [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) in a background thread to update table statistics. For example, a value of 0.5 means that auto-analyze is triggered when greater than 50% of the rows in a table have been modified. Auto-analyze can be restricted to only execute during certain hours of the day by specifying `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> Only when the `run-auto-analyze` option is enabled in the starting configuration file of TiDB, the `auto_analyze` feature can be triggered."
	case variable.TiDBAutoAnalyzeStartTime:
		return "- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`."
	case variable.TiDBBackoffLockFast:
		return "- This variable is used to set the `backoff` time when the read request meets a lock."
	case variable.TiDBBackOffWeight:
		return "- This variable is used to increase the weight of the maximum time of TiDB `backoff`, that is, the maximum retry time for sending a retry request when an internal network or other component (TiKV, PD) failure is encountered. This variable can be used to adjust the maximum retry time and the minimum value is 1.\n" +
			"\n" +
			"    For example, the base timeout for TiDB to take TSO from PD is 15 seconds. When `tidb_backoff_weight = 2`, the maximum timeout for taking TSO is: *base time \\* 2 = 30 seconds*.\n" +
			"\n" +
			"    In the case of a poor network environment, appropriately increasing the value of this variable can effectively alleviate error reporting to the application end caused by timeout. If the application end wants to receive the error information more quickly, minimize the value of this variable."
	case variable.TiDBBCJThresholdCount:
		return "- If the objects of the join operation belong to a subquery, the optimizer cannot estimate the size of the subquery result set. In this situation, the size is determined by the number of rows in the result set. If the estimated number of rows in the subquery is less than the value of this variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used."
	case variable.TiDBBCJThresholdSize:
		return "- If the table size is less than the value of the variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used."
	case variable.TiDBBuildStatsConcurrency:
		return "- This variable is used to set the concurrency of executing the `ANALYZE` statement.\n- When the variable is set to a larger value, the execution performance of other queries is affected."
	case variable.TiDBCapturePlanBaseline:
		return "- This variable is used to control whether to enable the [baseline capturing](/sql-plan-management.md#baseline-capturing) feature. This feature depends on the statement summary, so you need to enable the statement summary before you use baseline capturing.\n- After this feature is enabled, the historical SQL statements in the statement summary are traversed periodically, and bindings are automatically created for SQL statements that appear at least twice."
	case variable.TiDBCheckMb4ValueInUTF8:
		return "- This variable is used to enforce that the `utf8` character set only stores values from the [Basic Multilingual Plane (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane). To store characters outside the BMP, it is recommended to use the `utf8mb4` character set.\n- You might need to disable this option when upgrading your cluster from an earlier version of TiDB where the `utf8` checking was more relaxed. For details, see [FAQs After Upgrade](/faq/upgrade-faq.md)."
	case variable.TiDBChecksumTableConcurrency:
		return "- This variable is used to set the scan index concurrency of executing the `ADMIN CHECKSUM TABLE` statement.\n- When the variable is set to a larger value, the execution performance of other queries is affected."
	case variable.TiDBConfig:
		return "- This variable is read-only. It is used to obtain the configuration information of the current TiDB server."
	case variable.TiDBConstraintCheckInPlace:
		return "- This setting only applies to optimistic transactions. When this variable is set to `OFF`, checking for duplicate values in UNIQUE indexes is deferred until the transaction commits. This helps improve performance, but might be an unexpected behavior for some applications. See [Constraints](/constraints.md) for details.\n" +
			"\n" +
			"    - When set to zero and using optimistic transactions:\n" +
			"\n" +
			"        ```sql\n" +
			"        tidb> create table t (i int key);\n" +
			"        tidb> insert into t values (1);\n" +
			"        tidb> begin optimistic;\n" +
			"        tidb> insert into t values (1);\n" +
			"        Query OK, 1 row affected\n" +
			"        tidb> commit; -- Check only when a transaction is committed.\n" +
			"        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'\n" +
			"        ```\n" +
			"\n" +
			"    - When set to 1 and using optimistic transactions:\n" +
			"\n" +
			"        ```sql\n" +
			"        tidb> set @@tidb_constraint_check_in_place=1;\n" +
			"        tidb> begin optimistic;\n" +
			"        tidb> insert into t values (1);\n" +
			"        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'\n" +
			"        ```\n" +
			"\n" +
			"Constraint checking is always performed in place for pessimistic transactions (default)."
	case variable.TiDBCurrentTS:
		return "- This variable is read-only. It is used to obtain the timestamp of the current transaction."
	case variable.TiDBDDLErrorCountLimit:
		return "- This variable is used to set the number of retries when the DDL operation fails. When the number of retries exceeds the parameter value, the wrong DDL operation is canceled."
	case variable.TiDBDDLReorgBatchSize:
		return "- This variable is used to set the batch size during the `re-organize` phase of the DDL operation. For example, when TiDB executes the `ADD INDEX` operation, the index data needs to backfilled by `tidb_ddl_reorg_worker_cnt` (the number) concurrent workers. Each worker backfills the index data in batches.\n" +
			"    - If many updating operations such as `UPDATE` and `REPLACE` exist during the `ADD INDEX` operation, a larger batch size indicates a larger probability of transaction conflicts. In this case, you need to adjust the batch size to a smaller value. The minimum value is 32.\n" +
			"    - If the transaction conflict does not exist, you can set the batch size to a large value. This can increase the speed of the backfilling data, but the write pressure on TiKV also becomes higher."
	case variable.TiDBDDLReorgPriority:
		return "- This variable is used to set the priority of executing the `ADD INDEX` operation in the `re-organize` phase.\n- You can set the value of this variable to `PRIORITY_LOW`, `PRIORITY_NORMAL` or `PRIORITY_HIGH`."
	case variable.TiDBDDLReorgWorkerCount:
		return "- This variable is used to set the concurrency of the DDL operation in the `re-organize` phase."
	case variable.TiDBDisableTxnAutoRetry:
		return "- This variable is used to set whether to disable the automatic retry of explicit optimistic transactions. The default value of `ON` means that transactions will not automatically retry in TiDB and `COMMIT` statements might return errors that need to be handled in the application layer.\n" +
			"\n" +
			"    Setting the value to `OFF` means that TiDB will automatically retry transactions, resulting in fewer errors from `COMMIT` statements. Be careful when making this change, because it might result in lost updates.\n" +
			"\n" +
			"    This variable does not affect automatically committed implicit transactions and internally executed transactions in TiDB. The maximum retry count of these transactions is determined by the value of `tidb_retry_limit`.\n" +
			"\n" +
			"    For more details, see [limits of retry](/optimistic-transaction.md#limits-of-retry).\n" +
			"\n" +
			"    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is controlled by [`max_retry_count`](/tidb-configuration-file.md#max-retry-count)."
	case variable.TiDBDistSQLScanConcurrency:
		return "- This variable is used to set the concurrency of the `scan` operation.\n" +
			"- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.\n" +
			"- For OLAP scenarios, the maximum value should not exceed the number of CPU cores of all the TiKV nodes.\n" +
			"- If a table has a lot of partitions, you can reduce the variable value appropriately to avoid TiKV becoming out of memory (OOM)."
	case variable.TiDBDMLBatchSize:
		return "- When this value is greater than `0`, TiDB will batch commit statements such as `INSERT` or `LOAD DATA` into smaller transactions. This reduces memory usage and helps ensure that the `txn-total-size-limit` is not reached by bulk modifications.\n" +
			"- Only the value `0` provides ACID compliance. Setting this to any other value will break the atomicity and isolation guarantees of TiDB."
	case variable.TiDBEnableAmendPessimisticTxn:
		return "- This variable is used to control whether to enable the `AMEND TRANSACTION` feature. If you enable the `AMEND TRANSACTION` feature in a pessimistic transaction, when concurrent DDL operations and SCHEMA VERSION changes exist on tables associated with this transaction, TiDB attempts to amend the transaction. TiDB corrects the transaction commit to make the commit consistent with the latest valid SCHEMA VERSION so that the transaction can be successfully committed without getting the `Information schema is changed` error. This feature is effective on the following concurrent DDL operations:\n" +
			"\n" +
			"    - `ADD COLUMN` or `DROP COLUMN` operations.\n" +
			"    - `MODIFY COLUMN` or `CHANGE COLUMN` operations which increase the length of a field.\n" +
			"    - `ADD INDEX` or `DROP INDEX` operations in which the index column is created before the transaction is opened.\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> Currently, this feature is incompatible with TiDB Binlog in some scenarios and might cause semantic changes on a transaction. For more usage precautions of this feature, refer to [Incompatibility issues about transaction semantic](https://github.com/pingcap/tidb/issues/21069) and [Incompatibility issues about TiDB Binlog](https://github.com/pingcap/tidb/issues/20996)."
	case variable.TiDBEnableAsyncCommit:
		return "- This variable controls whether to enable the async commit feature for the second phase of the two-phase transaction commit to perform asynchronously in the background. Enabling this feature can reduce the latency of transaction commit.\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.\n" +
			"> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead.\n" +
			"> - Enabling this parameter only means that Async Commit becomes an optional mode of transaction commit. In fact, the most suitable mode of transaction commit is determined by TiDB."
	case variable.TiDBEnable1PC:
		return "- This variable is used to specify whether to enable the one-phase commit feature for transactions that only affect one Region. Compared with the often-used two-phase commit, one-phase commit can greatly reduce the latency of transaction commit and increase the throughput.\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.\n" +
			"> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead.\n" +
			"> - Enabling this parameter only means that one-phase commit becomes an optional mode of transaction commit. In fact, the most suitable mode of transaction commit is determined by TiDB."
	case variable.TiDBEnableCascadesPlanner:
		return "- This variable is used to control whether to enable the cascades planner."
	case variable.TiDBEnableChunkRPC:
		return "- This variable is used to control whether to enable the `Chunk` data encoding format in Coprocessor."
	case variable.TiDBEnableClusteredIndex:
		return "- This variable is used to control whether to create the primary key as a [clustered index](/clustered-indexes.md) by default." +
			` "By default" here means that the statement does not explicitly specify the keyword` +
			" `CLUSTERED`/`NONCLUSTERED`. Supported values are `OFF`, `ON`, and `INT_ONLY`:\n" +
			"    - `OFF` indicates that primary keys are created as non-clustered indexes by default.\n" +
			"    - `ON` indicates that primary keys are created as clustered indexes by default.\n" +
			"    - `INT_ONLY` indicates that the behavior is controlled by the configuration item `alter-primary-key`. If `alter-primary-key` is set to `true`, all primary keys are created as non-clustered indexes by default. If it is set to `false`, only the primary keys which consist of an integer column are created as clustered indexes."
	case variable.TiDBEnableCollectExecutionInfo:
		return "- This variable controls whether to record the execution information of each operator in the slow query log."
	case variable.TiDBEnableFastAnalyze:
		return "- This variable is used to set whether to enable the statistics `Fast Analyze` feature.\n" +
			"- If the statistics `Fast Analyze` feature is enabled, TiDB randomly samples about 10,000 rows of data as statistics. When the data is distributed unevenly or the data size is small, the statistics accuracy is low. This might lead to a non-optimal execution plan, for example, selecting a wrong index. If the execution time of the regular `Analyze` statement is acceptable, it is recommended to disable the `Fast Analyze` feature."
	case variable.TiDBEnableIndexMerge:
		return "- This variable is used to control whether to enable the index merge feature."
	case variable.TiDBEnableNoopFuncs:
		return "- By default, TiDB returns an error when you attempt to use the syntax for functionality that is not yet implemented. When the variable value is set to `ON`, TiDB silently ignores such cases of unavailable functionality, which is helpful if you cannot make changes to the SQL code.\n" +
			"- Enabling `noop` functions controls the following behaviors:\n" +
			"    * `get_lock` and `release_lock` functions\n" +
			"    * `LOCK IN SHARE MODE` syntax\n" +
			"    * `SQL_CALC_FOUND_ROWS` syntax\n" +
			"    * `START TRANSACTION READ ONLY` and `SET TRANSACTION READ ONLY` syntax\n" +
			"    * The `tx_read_only`, `transaction_read_only`, `offline_mode`, `super_read_only`, `read_only` and `sql_auto_is_null` system variables\n" +
			"\n" +
			"> **Warning:**\n" +
			">\n" +
			"> Only the default value of `OFF` can be considered safe. Setting `tidb_enable_noop_functions=1` might lead to unexpected behaviors in your application, because it permits TiDB to ignore certain syntax without providing an error. For example, the syntax `START TRANSACTION READ ONLY` is permitted, but the transaction remains in read-write mode."
	case variable.TiDBEnableParallelApply:
		return "- This variable controls whether to enable concurrency for the `Apply` operator. The number of concurrencies is controlled by the `tidb_executor_concurrency` variable. The `Apply` operator processes correlated subqueries and has no concurrency by default, so the execution speed is slow. Setting this variable value to `1` can increase concurrency and speed up execution. Currently, concurrency for `Apply` is disabled by default."
	case variable.TiDBEnableRateLimitAction:
		return "- This variable controls whether to enable the dynamic memory control feature for the operator that reads data. By default, this operator enables the maximum number of threads that [`tidb_disql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) allows to read data. When the memory usage of a single SQL statement exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) each time, the operator that reads data stops one thread.\n" +
			"- When the operator that reads data has only one thread left and the memory usage of a single SQL statement continues to exceed [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors, such as [spilling data to disk](/tidb-configuration-file.md#spilled-file-encryption-method)."
	case variable.TiDBEnableSlowLog:
		return "- This variable is used to control whether to enable the slow log feature."
	case variable.TiDBEnableStmtSummary:
		return "- This variable is used to control whether to enable the statement summary feature. If enabled, SQL execution information like time consumption is recorded to the `information_schema.STATEMENTS_SUMMARY` system table to identify and troubleshoot SQL performance issues."
	case variable.TiDBEnableStrictDoubleTypeCheck:
		return "- This variable is used to control if tables can be created with invalid definitions of type `DOUBLE`. This setting is intended to provide an upgrade path from earlier versions of TiDB, which were less strict in validating types.\n" +
			"- The default value of `ON` is compatible with MySQL.\n" +
			"\n" +
			"For example, the type `DOUBLE(10)` is now considered invalid because the precision of floating point types is not guaranteed. After changing `tidb_enable_strict_double_type_check` to `OFF`, the table is created:\n" +
			"\n" +
			"```sql\n" +
			"mysql> CREATE TABLE t1 (id int, c double(10));\n" +
			"ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use\n" +
			"\n" +
			"mysql> SET tidb_enable_strict_double_type_check = 'OFF';\n" +
			"Query OK, 0 rows affected (0.00 sec)\n" +
			"\n" +
			"mysql> CREATE TABLE t1 (id int, c double(10));\n" +
			"Query OK, 0 rows affected (0.09 sec)\n" +
			"```\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> This setting only applies to the type `DOUBLE` since MySQL permits precision for `FLOAT` types. This behavior is deprecated starting with MySQL 8.0.17, and it is not recommended to specify precision for either `FLOAT` or `DOUBLE` types."

	case variable.TiDBEnableTablePartition:
		return "- This variable is used to set whether to enable the `TABLE PARTITION` feature:\n" +
			"    - `ON` indicates enabling Range partitioning, Hash partitioning, and Range column partitioning with one single column.\n" +
			"    - `AUTO` functions the same way as `ON` does.\n" +
			"    - `OFF` indicates disabling the `TABLE PARTITION` feature. In this case, the syntax that creates a partition table can be executed, but the table created is not a partitioned one."
	case variable.TiDBEnableListTablePartition:
		return "- This variable is used to set whether to enable the `LIST (COLUMNS) TABLE PARTITION` feature."
	case variable.TiDBEnableTelemetry:
		return "- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled. By setting the value to `OFF`, the telemetry collection is disabled. If the [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB configuration item is set to `false` on all TiDB instances, the telemetry collection is always disabled and this system variable will not take effect. See [Telemetry](/telemetry.md) for details."
	case variable.Version:
		return "- This variable returns the MySQL version, followed by the TiDB version. For example '5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253'."
	case variable.VersionComment:
		return "- This variable returns additional details about the TiDB version. For example, 'TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible'."
	case variable.TransactionIsolation:
		return "- This variable sets the transaction isolation. TiDB advertises `REPEATABLE-READ` for compatibility with MySQL, but the actual isolation level is Snapshot Isolation. See [transaction isolation levels](/transaction-isolation-levels.md) for further details."
	case variable.TimeZone:
		return "- This variable returns the current time zone. Values can be specified as either an offset such as '-8:00' or a named zone 'America/Los_Angeles'.\n- The value `SYSTEM` means that the time zone should be the same as the system host, which is available via the [`system_time_zone`](#system_time_zone) variable."
	case variable.TiDBWindowConcurrency:
		return "- This variable is used to set the concurrency degree of the window operator.\n- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead."
	case variable.TiDBEnableWindowFunction:
		return "- This variable is used to control whether to enable the support for window functions. Note that window functions may use reserved keywords. This might cause SQL statements that could be executed normally cannot be parsed after upgrading TiDB. In this case, you can set `tidb_enable_window_function` to `OFF`."
	case variable.TiDBEnableVectorizedExpression:
		return "- This variable is used to control whether to enable vectorized execution."
	case variable.TiDBEvolvePlanBaselines:
		return "- This variable is used to control whether to enable the baseline evolution feature. For detailed introduction or usage , see [Baseline Evolution](/sql-plan-management.md#baseline-evolution).\n" +
			"- To reduce the impact of baseline evolution on the cluster, use the following configurations:\n" +
			"    - Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is 600s.\n" +
			"    - Set `tidb_evolve_plan_task_start_time` and `tidb_evolve_plan_task_end_time` to limit the time window. The default values are respectively `00:00 +0000` and `23:59 +0000`."
	case variable.TiDBEvolvePlanTaskEndTime:
		return "- This variable is used to set the end time of baseline evolution in a day."
	case variable.TiDBEvolvePlanTaskMaxTime:
		return "- This variable is used to limit the maximum execution time of each execution plan in the baseline evolution feature."
	case variable.TiDBEvolvePlanTaskStartTime:
		return "- This variable is used to set the start time of baseline evolution in a day."
	case variable.TiDBExecutorConcurrency:
		return "\nThis variable is used to set the concurrency of the following SQL operators (to one value):\n" +
			"\n" +
			"- `index lookup`\n" +
			"- `index lookup join`\n" +
			"- `hash join`\n" +
			"- `hash aggregation` (the `partial` and `final` phases)\n" +
			"- `window`\n" +
			"- `projection`\n" +
			"\n" +
			"`tidb_executor_concurrency` incorporates the following existing system variables as a whole for easier management:\n" +
			"\n" +
			"+ `tidb_index_lookup_concurrency`\n" +
			"+ `tidb_index_lookup_join_concurrency`\n" +
			"+ `tidb_hash_join_concurrency`\n" +
			"+ `tidb_hashagg_partial_concurrency`\n" +
			"+ `tidb_hashagg_final_concurrency`\n" +
			"+ `tidb_projection_concurrency`\n" +
			"+ `tidb_window_concurrency`\n" +
			"\n" +
			"Since v5.0, you can still separately modify the system variables listed above (with a deprecation warning returned) and your modification only affects the corresponding single operators. After that, if you use `tidb_executor_concurrency` to modify the operator concurrency, the separately modified operators will not be affected. If you want to use `tidb_executor_concurrency` to modify the concurrency of all operators, you can set the values of all variables listed above to `-1`.\n" +
			"\n" +
			"For a system upgraded to v5.0 from an earlier version, if you have not modified any value of the variables listed above (which means that the `tidb_hash_join_concurrency` value is `5` and the values of the rest are `4`), the operator concurrency previously managed by these variables will automatically be managed by `tidb_executor_concurrency`. If you have modified any of these variables, the concurrency of the corresponding operators will still be controlled by the modified variables."
	case variable.TiDBExpensiveQueryTimeThreshold:
		return "- This variable is used to set the threshold value that determines whether to print expensive query logs. The difference between expensive query logs and slow query logs is:\n" +
			"    - Slow logs are printed after the statement is executed.\n" +
			"    - Expensive query logs print the statements that are being executed, with execution time exceeding the threshold value, and their related information."
	case variable.TiDBForcePriority:
		return "- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.\n- You can set the value of this variable to `NO_PRIORITY`, `LOW_PRIORITY`, `DELAYED` or `HIGH_PRIORITY`."
	case variable.TiDBGCConcurrency:
		return "- Specifies the number of threads in the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) step of GC. A value of `-1` means that TiDB will automatically decide the number of garbage collection threads to use."
	case variable.TiDBGCEnable:
		return "- Enables garbage collection for TiKV. Disabling garbage collection will reduce system performance, as old versions of rows will no longer be purged."
	case variable.TiDBGCLifetime:
		return "- The time limit during which data is retained for each GC, in the format of Go Duration. When a GC happens, the current time minus this value is the safe point.\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> - In scenarios of frequent updates, a large value (days or even months) for `tidb_gc_life_time` may cause potential issues, such as:\n" +
			">     - Larger storage use\n" +
			">     - A large amount of history data may affect performance to a certain degree, especially for range queries such as `select count(*) from t`\n" +
			"> - If there is any transaction that has been running longer than `tidb_gc_life_time`, during GC, the data since `start_ts` is retained for this transaction to continue execution. For example, if `tidb_gc_life_time` is configured to 10 minutes, among all transactions being executed, the transaction that starts earliest has been running for 15 minutes, GC will retain data of the recent 15 minutes."
	case variable.TiDBGCRunInterval:
		return "- Specifies the GC interval, in the format of Go Duration, for example, `\"1h30m\"`, and `\"15m\"`"
	case variable.TiDBGCScanLockMode:
		return "    - `LEGACY`: Uses the old way of scanning, that is, disable Green GC.\n    - `PHYSICAL`: Uses the physical scanning method, that is, enable Green GC.\n" +
			"- This variable specifies the way of scanning locks in the Resolve Locks step of GC. When the variable value is set to `LEGACY`, TiDB scans locks by Regions. When the value `PHYSICAL` is used, it enables each TiKV node to bypass the Raft layer and directly scan data, which can effectively mitigate the impact of GC wakening up all Regions when the [Hibernate Region](/tikv-configuration-file.md#hibernate-regions) feature is enabled, thus improving the execution speed in the Resolve Locks step."
	case variable.TiDBGeneralLog:
		return "- This variable is used to set whether to record all SQL statements in the [log](/tidb-configuration-file.md#logfile). This feature is disabled by default. If maintenance personnel needs to trace all SQL statements when locating issues, they can enable this feature.\n" +
			"- To see all records of this feature in the log, query the `\"GENERAL_LOG\"` string. The following information is recorded:\n" +
			"    - `conn`: The ID of the current session.\n" +
			"    - `user`: The current session user.\n" +
			"    - `schemaVersion`: The current schema version.\n" +
			"    - `txnStartTS`: The timestamp at which the current transaction starts.\n" +
			"    - `forUpdateTS`: In the pessimistic transactional model, `forUpdateTS` is the current timestamp of the SQL statement. When a write conflict occurs in the pessimistic transaction, TiDB retries the SQL statement currently being executed and updates this timestamp. You can configure the number of retries via [`max-retry-count`](/tidb-configuration-file.md#max-retry-count). In the optimistic transactional model, `forUpdateTS` is equivalent to `txnStartTS`.\n" +
			"    - `isReadConsistency`: Indicates whether the current transactional isolation level is Read Committed (RC).\n" +
			"    - `current_db`: The name of the current database.\n" +
			"    - `txn_mode`: The transactional mode. Value options are `OPTIMISTIC` and `PESSIMISTIC`.\n" +
			"    - `sql`: The SQL statement corresponding to the current query."
	case variable.TiDBHashJoinConcurrency:
		return "- This variable is used to set the concurrency of the `hash join` algorithm.\n- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead."
	case variable.TiDBHashAggFinalConcurrency:
		return "- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `final` phase.\n- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.\n- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead."
	case variable.TiDBHashAggPartialConcurrency:
		return "- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `partial` phase.\n- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.\n- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead."
	case variable.TiDBIndexLookupConcurrency:
		return "- This variable is used to set the concurrency of the `index lookup` operation.\n- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.\n- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead."
	case variable.TiDBIndexLookupJoinConcurrency:
		return "- This variable is used to set the concurrency of the `index lookup join` algorithm.\n- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead."
	case variable.TiDBIndexLookupSize:
		return "- This variable is used to set the batch size of the `index lookup` operation.\n- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios."
	case variable.TiDBIndexSerialScanConcurrency:
		return "- This variable is used to set the concurrency of the `serial scan` operation.\n- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios."
	case variable.TiDBInitChunkSize:
		return "- This variable is used to set the number of rows for the initial chunk during the execution process."
	case variable.TiDBMultiStatementMode:
		return "- This variable controls whether to allow multiple queries to be executed in the same `COM_QUERY` call.\n" +
			"- To reduce the impact of SQL injection attacks, TiDB now prevents multiple queries from being executed in the same `COM_QUERY` call by default. This variable is intended to be used as part of an upgrade path from earlier versions of TiDB. The following behaviors apply:\n" +
			"\n" +
			"| Client setting            | `tidb_multi_statement_mode` value | Multiple statements permitted? |\n" +
			"| ------------------------- | --------------------------------- | ------------------------------ |\n" +
			"| Multiple Statements = ON  | OFF                               | Yes                            |\n" +
			"| Multiple Statements = ON  | ON                                | Yes                            |\n" +
			"| Multiple Statements = ON  | WARN                              | Yes                            |\n" +
			"| Multiple Statements = OFF | OFF                               | No                             |\n" +
			"| Multiple Statements = OFF | ON                                | Yes                            |\n" +
			"| Multiple Statements = OFF | WARN                              | Yes (+warning returned)        |\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> Only the default value of `OFF` can be considered safe. Setting `tidb_multi_statement_mode=ON` might be required if your application was specifically designed for an earlier version of TiDB. If your application requires multiple statement support, it is recommended to use the setting provided by your client library instead of the `tidb_multi_statement_mode` option. For example:\n" +
			">\n" +
			"> * [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) (`multiStatements`)\n" +
			"> * [Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html) (`allowMultiQueries`)\n" +
			"> * PHP [mysqli](https://dev.mysql.com/doc/apis-php/en/apis-php-mysqli.quickstart.multiple-statement.html) (`mysqli_multi_query`)"
	case variable.TiDBIsolationReadEngines:
		return "- This variable is used to set the storage engine list that TiDB can use when reading data."
	case variable.TiDBTxnMode:
		return "- This variable is used to set the transaction mode. TiDB 3.0 supports the pessimistic transactions. Since TiDB 3.0.8, the [pessimistic transaction mode](/pessimistic-transaction.md) is enabled by default.\n" +
			"- If you upgrade TiDB from v3.0.7 or earlier versions to v3.0.8 or later versions, the default transaction mode does not change. **Only the newly created clusters use the pessimistic transaction mode by default**.\n" +
			"- If this variable is set to \"optimistic\" or \"\", TiDB uses the [optimistic transaction mode](/optimistic-transaction.md)."
	case variable.TiDBLowResolutionTSO:
		return "- This variable is used to set whether to enable the low precision TSO feature. After this feature is enabled, new transactions use a timestamp updated every 2 seconds to read data.\n- The main applicable scenario is to reduce the overhead of acquiring TSO for small read-only transactions when reading old data is acceptable."
	case variable.TiDBMaxChunkSize:
		return "- This variable is used to set the maximum number of rows in a chunk during the execution process. Setting to too large of a value may cause cache locality issues."
	case variable.TiDBMaxDeltaSchemaCount:
		return "- This variable is used to set the maximum number of schema versions (the table IDs modified for corresponding versions) allowed to be cached. The value range is 100 ~ 16384."
	case variable.TiDBMemQuotaQuery:
		return "- This variable is used to set the threshold value of memory quota for a query.\n- If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file. The initial value of this variable is configured by [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query)."
	case variable.TiDBMemQuotaApplyCache:
		return "- This variable is used to set the memory usage threshold of the local cache in the `Apply` operator.\n- The local cache in the `Apply` operator is used to speed up the computation of the `Apply` operator. You can set the variable to `0` to disable the `Apply` cache feature."
	case variable.TiDBMemoryUsageAlarmRatio:
		return "- TiDB triggers an alarm when the percentage of the memory it takes exceeds a certain threshold. For the detailed usage description of this feature, see [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).\n- You can set the initial value of this variable by configuring [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409)."
	case variable.TiDBOptAggPushDown:
		return "- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join, Projection, and UnionAll.\n- When the aggregate operation is slow in query, you can set the variable value to ON."
	case variable.TiDBOptDistinctAggPushDown:
		return "- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function with `distinct` (such as `select count(distinct a) from t`) to Coprocessor.\n" +
			"- When the aggregate function with the `distinct` operation is slow in the query, you can set the variable value to `1`.\n" +
			"\n" +
			"In the following example, before `tidb_opt_distinct_agg_push_down` is enabled, TiDB needs to read all data from TiKV and execute `distinct` on the TiDB side. After `tidb_opt_distinct_agg_push_down` is enabled, `distinct a` is pushed down to Coprocessor, and a `group by` column `test.t.a` is added to `HashAgg_5`.\n" +
			"\n" +
			"```sql\n" +
			"mysql> desc select count(distinct a) from test.t;\n" +
			"+-------------------------+----------+-----------+---------------+------------------------------------------+\n" +
			"| id                      | estRows  | task      | access object | operator info                            |\n" +
			"+-------------------------+----------+-----------+---------------+------------------------------------------+\n" +
			"| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |\n" +
			"| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |\n" +
			"|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |\n" +
			"+-------------------------+----------+-----------+---------------+------------------------------------------+\n" +
			"3 rows in set (0.01 sec)\n" +
			"\n" +
			"mysql> set session tidb_opt_distinct_agg_push_down = 1;\n" +
			"Query OK, 0 rows affected (0.00 sec)\n" +
			"\n" +
			"mysql> desc select count(distinct a) from test.t;\n" +
			"+---------------------------+----------+-----------+---------------+------------------------------------------+\n" +
			"| id                        | estRows  | task      | access object | operator info                            |\n" +
			"+---------------------------+----------+-----------+---------------+------------------------------------------+\n" +
			"| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |\n" +
			"| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |\n" +
			"|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |\n" +
			"|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |\n" +
			"+---------------------------+----------+-----------+---------------+------------------------------------------+\n" +
			"4 rows in set (0.00 sec)\n" +
			"```"
	case variable.TiDBOptInSubqToJoinAndAgg:
		return "- This variable is used to set whether to enable the optimization rule that converts a subquery to join and aggregation.\n" +
			"- For example, after you enable this optimization rule, the subquery is converted as follows:\n" +
			"\n" +
			"    ```sql\n" +
			"    select * from t where t.a in (select aa from t1)\n" +
			"    ```\n" +
			"\n" +
			"    The subquery is converted to join as follows:\n" +
			"\n" +
			"    ```sql\n" +
			"    select * from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa\n" +
			"    ```\n" +
			"\n" +
			"    If `t1` is limited to be `unique` and `not null` in the `aa` column. You can use the following statement, without aggregation.\n" +
			"\n" +
			"    ```sql\n" +
			"    select * from t, t1 where t.a=t1.a\n" +
			"    ```"
	case variable.TiDBOptPreferRangeScan:
		return "- After you set the value of this variable to `ON`, the optimizer always prefers range scans over full table scans.\n" +
			"- In the following example, before you enable `tidb_opt_prefer_range_scan`, the TiDB optimizer performs a full table scan. After you enable `tidb_opt_prefer_range_scan`, the optimizer selects an index range scan.\n" +
			"\n" +
			"```sql\n" +
			"explain select * from t where age=5;\n" +
			"+-------------------------+------------+-----------+---------------+-------------------+\n" +
			"| id                      | estRows    | task      | access object | operator info     |\n" +
			"+-------------------------+------------+-----------+---------------+-------------------+\n" +
			"| TableReader_7           | 1048576.00 | root      |               | data:Selection_6  |\n" +
			"| └─Selection_6           | 1048576.00 | cop[tikv] |               | eq(test.t.age, 5) |\n" +
			"|   └─TableFullScan_5     | 1048576.00 | cop[tikv] | table:t       | keep order:false  |\n" +
			"+-------------------------+------------+-----------+---------------+-------------------+\n" +
			"3 rows in set (0.00 sec)\n" +
			"\n" +
			"set session tidb_opt_prefer_range_scan = 1;\n" +
			"\n" +
			"explain select * from t where age=5;\n" +
			"+-------------------------------+------------+-----------+-----------------------------+-------------------------------+\n" +
			"| id                            | estRows    | task      | access object               | operator info                 |\n" +
			"+-------------------------------+------------+-----------+-----------------------------+-------------------------------+\n" +
			"| IndexLookUp_7                 | 1048576.00 | root      |                             |                               |\n" +
			"| ├─IndexRangeScan_5(Build)     | 1048576.00 | cop[tikv] | table:t, index:idx_age(age) | range:[5,5], keep order:false |\n" +
			"| └─TableRowIDScan_6(Probe)     | 1048576.00 | cop[tikv] | table:t                     | keep order:false              |\n" +
			"+-------------------------------+------------+-----------+-----------------------------+-------------------------------+\n" +
			"3 rows in set (0.00 sec)\n" +
			"```"
	case variable.TiDBSkipUTF8Check:
		return "- This variable is used to set whether to skip UTF-8 validation.\n" +
			"- Validating UTF-8 characters affects the performance. When you are sure that the input characters are valid UTF-8 characters, you can set the variable value to `ON`."
	case variable.TiDBSlowLogThreshold:
		return "- This variable is used to output the threshold value of the time consumed by the slow log. When the time consumed by a query is larger than this value, this query is considered as a slow log and its log is output to the slow query log.\n" +
			"\n" +
			"Usage example:\n" +
			"\n" +
			"```sql\n" +
			"SET tidb_slow_log_threshold = 200;\n" +
			"```"
	case variable.TiDBSlowQueryFile:
		return "- When `INFORMATION_SCHEMA.SLOW_QUERY` is queried, only the slow query log name set by `slow-query-file` in the configuration file is parsed. The default slow query log name is \"tidb-slow.log\". To parse other logs, set the `tidb_slow_query_file` session variable to a specific file path, and then query `INFORMATION_SCHEMA.SLOW_QUERY` to parse the slow query log based on the set file path. For details, see [Identify Slow Queries](/identify-slow-queries.md)."
	case variable.TiDBQueryLogMaxLen:
		return "- The maximum length of the SQL statement output. When the output length of a statement is larger than the `tidb_query-log-max-len` value, the statement is truncated to output.\n" +
			"\n" +
			"Usage example:\n" +
			"\n" +
			"```sql\n" +
			"SET tidb_query_log_max_len = 20\n" +
			"```"
	case variable.TiDBRecordPlanInSlowLog:
		return "- This variable is used to control whether to include the execution plan of slow queries in the slow log."
	case variable.TiDBReplicaRead:
		return "- This variable is used to control where TiDB reads data. Here are three options:\n" +
			"    - leader: Read only from leader node\n" +
			"    - follower: Read only from follower node\n" +
			"    - leader-and-follower: Read from leader or follower node\n" +
			"- See [follower reads](/follower-read.md) for additional details."
	case variable.TiDBEnableEnhancedSecurity:
		return "- This variable indicates whether the TiDB server you are connected to has the Security Enhanced Mode (SEM) enabled. To change its value, you need to modify the value of `enable-sem` in your TiDB server configuration file and restart the TiDB server.\n" +
			"- SEM is inspired by the design of systems such as [Security-Enhanced Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux). It reduces the abilities of users with the MySQL `SUPER` privilege and instead requires `RESTRICTED` fine-grained privileges to be granted as a replacement. These fine-grained privileges include:\n" +
			"    - `RESTRICTED_TABLES_ADMIN`: The ability to write data to system tables in the `mysql` schema and to see sensitive columns on `information_schema` tables.\n" +
			"    - `RESTRICTED_STATUS_ADMIN`: The ability to see sensitive variables in the command `SHOW STATUS`.\n" +
			"    - `RESTRICTED_VARIABLES_ADMIN`: The ability to see and set sensitive variables in `SHOW [GLOBAL] VARIABLES` and `SET`.\n" +
			"    - `RESTRICTED_USER_ADMIN`: The ability to prevent other users from making changes or dropping a user account."
	case variable.TiDBIndexJoinBatchSize:
		return "- This variable is used to set the batch size of the `index lookup join` operation.\n- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios."
	case variable.TiDBMetricSchemaRangeDuration:
		return "- This variable is used to set the range duration of the Prometheus statement generated when querying `METRICS_SCHEMA`."
	case variable.TiDBMetricSchemaStep:
		return "- This variable is used to set the step of the Prometheus statement generated when querying `METRICS_SCHEMA`."
	case variable.TiDBOptCorrelationExpFactor:
		return "- When the method that estimates the number of rows based on column order correlation is not available, the heuristic estimation method is used. This variable is used to control the behavior of the heuristic method.\n" +
			"    - When the value is 0, the heuristic method is not used.\n" +
			"    - When the value is greater than 0:\n" +
			"        - A larger value indicates that an index scan will probably be used in the heuristic method.\n" +
			"        - A smaller value indicates that a table scan will probably be used in the heuristic method."
	case variable.TiDBOptCorrelationThreshold:
		return "- This variable is used to set the threshold value that determines whether to enable estimating the row count by using column order correlation. If the order correlation between the current column and the `handle` column exceeds the threshold value, this method is enabled."
	case variable.TiDBOptWriteRowID:
		return "- This variable is used to control whether to allow `INSERT`, `REPLACE`, and `UPDATE` statements to operate on the `_tidb_rowid` column. This variable can be used only when you import data using TiDB tools."
	case variable.TiDBPProfSQLCPU:
		return "- This variable is used to control whether to mark the corresponding SQL statement in the profile output to identify and troubleshoot performance issues."
	case variable.TiDBProjectionConcurrency:
		return "- This variable is used to set the concurrency of the `Projection` operator.\n- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead."
	case variable.TiDBRedactLog:
		return "- This variable controls whether to hide user information in the SQL statement being recorded into the TiDB log and slow log.\n- When you set the variable to `1`, user information is hidden. For example, if the executed SQL statement is `insert into t values (1,2)`, the statement is recorded as `insert into t values (?,?)` in the log."
	case variable.TiDBRetryLimit:
		return "- This variable is used to set the maximum number of the retries for optimistic transactions. When a transaction encounters retryable errors (such as transaction conflicts, very slow transaction commit, or table schema changes), this transaction is re-executed according to this variable. Note that setting `tidb_retry_limit` to `0` disables the automatic retry. This variable only applies to optimistic transactions, not to pessimistic transactions."
	case variable.TiDBRowFormatVersion:
		return "- Controls the format version of the newly saved data in the table. In TiDB v4.0, the [new storage row format](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md) version `2` is used by default to save new data.\n" +
			"- If you upgrade from a TiDB version earlier than 4.0.0 to 4.0.0, the format version is not changed, and TiDB continues to use the old format of version `1` to write data to the table, which means that **only newly created clusters use the new data format by default**.\n" +
			"- Note that modifying this variable does not affect the old data that has been saved, but applies the corresponding version format only to the newly written data after modifying this variable."
	case variable.TiDBScatterRegion:
		return "- By default, Regions are split for a new table when it is being created in TiDB. After this variable is enabled, the newly split Regions are scattered immediately during the execution of the `CREATE TABLE` statement. This applies to the scenario where data need to be written in batches right after the tables are created in batches, because the newly split Regions can be scattered in TiKV beforehand and do not have to wait to be scheduled by PD. To ensure the continuous stability of writing data in batches, the `CREATE TABLE` statement returns success only after the Regions are successfully scattered. This makes the statement's execution time multiple times longer than that when you disable this variable."
	case variable.TiDBSkipASCIICheck:
		return "- This variable is used to set whether to skip ASCII validation.\n- Validating ASCII characters affects the performance. When you are sure that the input characters are valid ASCII characters, you can set the variable value to `ON`."
	case variable.TiDBSkipIsolationLevelCheck:
		return "- After this switch is enabled, if an isolation level unsupported by TiDB is assigned to `tx_isolation`, no error is reported. This helps improve compatibility with applications that set (but do not depend on) a different isolation level.\n\n" +
			"```sql\n" +
			"tidb> set tx_isolation='serializable';\n" +
			"ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error\n" +
			"tidb> set tidb_skip_isolation_level_check=1;\n" +
			"Query OK, 0 rows affected (0.00 sec)\n" +
			"\n" +
			"tidb> set tx_isolation='serializable';\n" +
			"Query OK, 0 rows affected, 1 warning (0.00 sec)\n" +
			"```"
	case variable.TiDBSnapshot:
		return "- This variable is used to set the time point at which the data is read by the session. For example, when you set the variable to \"2017-11-11 20:20:20\" or a TSO number like \"400036290571534337\", the current session reads the data of this moment."
	case variable.TiDBStmtSummaryHistorySize:
		return "- This variable is used to set the history capacity of [statement summary tables](/statement-summary-tables.md)."
	case variable.TiDBStmtSummaryInternalQuery:
		return "- This variable is used to control whether to include the SQL information of TiDB in [statement summary tables](/statement-summary-tables.md)."
	case variable.TiDBStmtSummaryMaxStmtCount:
		return "- This variable is used to set the maximum number of statements that [statement summary tables](/statement-summary-tables.md) store in memory."
	case variable.TiDBStmtSummaryRefreshInterval:
		return "- This variable is used to set the refresh time of [statement summary tables](/statement-summary-tables.md)."
	case variable.TiDBStoreLimit:
		return "- This variable is used to limit the maximum number of requests TiDB can send to TiKV at the same time. 0 means no limit."
	case variable.TiDBStmtSummaryMaxSQLLength:
		return "- This variable is used to control the length of the SQL string in [statement summary tables](/statement-summary-tables.md)."
	case variable.TiDBUsePlanBaselines:
		return "- This variable is used to control whether to enable the execution plan binding feature. It is enabled by default, and can be disabled by assigning the `OFF` value. For the use of the execution plan binding, see [Execution Plan Binding](/sql-plan-management.md#create-a-binding)."
	case variable.TiDBWaitSplitRegionFinish:
		return "- It usually takes a long time to scatter Regions, which is determined by PD scheduling and TiKV loads. This variable is used to set whether to return the result to the client after all Regions are scattered completely when the `SPLIT REGION` statement is being executed:\n" +
			"    - `ON` requires that the `SPLIT REGIONS` statement waits until all Regions are scattered.\n" +
			"    - `OFF` permits the `SPLIT REGIONS` statement to return before finishing scattering all Regions.\n" +
			"- Note that when scattering Regions, the write and read performances for the Region that is being scattered might be affected. In batch-write or data importing scenarios, it is recommended to import data after Regions scattering is finished."
	case variable.TiDBWaitSplitRegionTimeout:
		return "- This variable is used to set the timeout for executing the `SPLIT REGION` statement. If a statement is not executed completely within the specified time value, a timeout error is returned."
	case variable.WarningCount:
		return "- This read-only variable indicates the number of warnings that occurred in the statement that was previously executed."
	case variable.CTEMaxRecursionDepth:
		return "- Controls the maximum recursion depth in Common Table Expressions."
	case variable.InitConnect:
		return "- The `init_connect` feature permits a SQL statement to be automatically executed when you first connect to a TiDB server. If you have the `CONNECTION_ADMIN` or `SUPER` privileges, this `init_connect` statement will not be executed. If the `init_connect` statement results in an error, your user connection will be terminated."
	case variable.TiDBPartitionPruneMode:
		return "- Specifies whether to enable `dynamic` mode for partitioned tables. For details about the dynamic pruning mode, see [Dynamic Pruning Mode for Partitioned Tables](/partitioned-table.md#dynamic-pruning-mode)."
	case variable.TiDBEnforceMPPExecution:
		return "- To change this default value, modify the [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) configuration value.\n" +
			"- Controls whether to ignore the optimizer's cost estimation and to forcibly use TiFlash's MPP mode for query execution. The value options are as follows:\n" +
			"    - `0` or `OFF`, which means that the MPP mode is not forcibly used (by default).\n" +
			"    - `1` or `ON`, which means that the cost estimation is ignored and the MPP mode is forcibly used. Note that this setting only takes effect when `tidb_allow_mpp=true`.\n\n" +
			"MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [Control whether to select the MPP mode](/tiflash/use-tiflash.md#control-whether-to-select-the-mpp-mode)."
	case variable.CharacterSetClient:
		return "- The character set for data sent from the client. See [Character Set and Collation](/character-set-and-collation.md) for details on the use of character sets and collations in TiDB. It is recommended to use [`SET NAMES`](/sql-statements/sql-statement-set-names.md) to change the character set when needed."
	case variable.CharacterSetConnection:
		return "- The character set for string literals that do not have a specified character set."
	case variable.CharsetDatabase:
		return "- This variable indicates the character set of the default database in use. **It is NOT recommended to set this variable**. When a new default database is selected, the server changes the variable value."
	case variable.CharacterSetResults:
		return "- The character set that is used when data is sent to the client."
	case variable.CharacterSetServer:
		return "- The default character set for the server."
	case variable.DataDir:
		return "- This variable indicates the location where data is stored. This location can be a local path or point to a PD server if the data is stored on TiKV.\n" +
			"- A value in the format of `ip_address:port` indicates the PD server that TiDB connects to on startup."
	case variable.DefaultAuthPlugin:
		return "- This variable sets the authentication method that the server advertises when the server-client connection is being established. Possible values for this variable are documented in [Authentication plugin status](/security-compatibility-with-mysql.md#authentication-plugin-status).\n" +
			"- Value options: `mysql_native_password` and `caching_sha2_password`. For more details, see [Authentication plugin status](/security-compatibility-with-mysql.md#authentication-plugin-status)."
	case "license":
		return "- This variable indicates the license of your TiDB server installation."
	case variable.TiDBAnalyzeVersion:
		return "- Controls how TiDB collects statistics.\n" +
			"- In versions before v5.1.0, the default value of this variable is `1`. In v5.1.0, the default value of this variable is `2`, which serves as an experimental feature. For detailed introduction, see [Introduction to Statistics](/statistics.md)."
	case variable.TiDBOptLimitPushDownThreshold:
		return "- This variable is used to set the threshold that determines whether to push the Limit or TopN operator down to TiKV.\n" +
			"- If the value of the Limit or TopN operator is smaller than or equal to this threshold, these operators are forcibly pushed down to TiKV. This variable resolves the issue that the Limit or TopN operator cannot be pushed down to TiKV partly due to wrong estimation."
	case variable.TiDBOptEnableCorrelationAdjustment:
		return "- This variable is used to control whether the optimizer estimates the number of rows based on column order correlation"
	case variable.TiDBEnableAutoIncrementInGenerated:
		return "- This variable is used to determine whether to include the `AUTO_INCREMENT` columns when creating a generated column or an expression index."
	case variable.TMPTableSize:
		return "- Indicates the maximum size of a temporary table."
	case variable.Timestamp:
		return "- A non-empty value of this variable indicates the UNIX epoch that is used as the timestamp for `CURRENT_TIMESTAMP()`, `NOW()`, and other functions. This variable might be used in data restore or replication."
	case "ssl_key":
		return "- The location of the private key file (if there is one) that is used for SSL/TLS connections."
	case "ssl_cert":
		return "- The location of the certificate file (if there is a file) that is used for SSL/TLS connections."
	case variable.MaxAllowedPacket:
		return "- The maximum size of a packet for the MySQL protocol."
	case variable.BlockEncryptionMode:
		return "- Defines the encryption mode for the `AES_ENCRYPT()` and `AES_DECRYPT()` functions."
	case variable.CollationConnection:
		return "- This variable indicates the collation for string literals that do not have a specified collation."
	case variable.CollationDatabase:
		return "- This variable indicates the collation of the default database in use. **It is NOT recommended to set this variable**. When a new default database is selected, the server changes the variable value."
	case variable.CollationServer:
		return "- The default collation for the server."
	case variable.DefaultWeekFormat:
		return "- Sets the week format used by the `WEEK()` function."
	case variable.GroupConcatMaxLen:
		return "- The maximum buffer size for items in the `GROUP_CONCAT()` function."
	case "have_openssl":
		return "- A read-only variable for MySQL compatibility. Set to `YES` by the server when the server has TLS enabled."
	case "have_ssl":
		return "- A read-only variable for MySQL compatibility. Set to `YES` by the server when the server has TLS enabled."
	case variable.PluginDir:
		return "- Indicates the directory to load plugins as specified by a command-line flag."
	case variable.PluginLoad:
		return "- Indicates the plugins to load when TiDB is started. These plugins are specified by a command-line flag and separated by commas."
	case variable.SkipNameResolve:
		return "- This variable controls whether the `tidb-server` instance resolves hostnames as a part of the connection handshake.\n" +
			"- When the DNS is unreliable, you can enable this option to improve network performance.\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> When `skip_name_resolve=ON`, users with a hostname in their identity will no longer be able to log into the server. For example:\n" +
			">\n" +
			"> ```sql\n" +
			"> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';\n" +
			"> ```\n" +
			">\n" +
			"> In this example, it is recommended to replace `apphost` with an IP address or the wildcard (`%`)."
	case variable.LogBin:
		return "- This variable indicates whether [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is used."
	case variable.LastInsertID:
		return "- This variable returns the last `AUTO_INCREMENT` or `AUTO_RANDOM` value generated by an insert statement.\n" +
			"- The value of `last_insert_id` is the same as the value returned by the function `LAST_INSERT_ID()`."
	case variable.SQLLogBin:
		return "- Indicates whether to write changes to [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) or not.\n" +
			"\n" +
			"> **Note:**\n" +
			">\n" +
			"> It is not recommended to set `sql_log_bin` as a global variable because the future versions of TiDB might only allow setting this as a session variable."
	case "ssl_ca":
		return "- The location of the certificate authority file (if there is one)."
	default:
		return "- No documentation is currently available for this variable."
	}
}

func getSysVarsByOrder() []string {
	var svs []string
	for name := range variable.GetSysVars() {
		svs = append(svs, name)
	}
	sort.Strings(svs)
	return svs
}

func main() {

	fmt.Printf("---\n" +
		"title: System Variables\n" +
		"summary: Use system variables to optimize performance or alter running behavior.\n" +
		"aliases: ['/tidb/dev/tidb-specific-system-variables','/docs/dev/system-variables/','/docs/dev/reference/configuration/tidb-server/mysql-variables/', '/docs/dev/tidb-specific-system-variables/','/docs/dev/reference/configuration/tidb-server/tidb-specific-variables/']\n" +
		"---\n" +
		"\n" +
		"# System Variables\n" +
		"\n" +
		"TiDB system variables behave similar to MySQL with some differences, in that settings might apply on a `SESSION`, `INSTANCE`, or `GLOBAL` scope, or on a scope that combines `SESSION`, `INSTANCE`, or `GLOBAL`.\n" +
		"\n" +
		"- Changes to `GLOBAL` scoped variables **only apply to new connection sessions with TiDB**. Currently active connection sessions are not affected. These changes are persisted and valid after restarts.\n" +
		"- Changes to `INSTANCE` scoped variables apply to all active or new connection sessions with the current TiDB instance immediately after the changes are made. Other TiDB instances are not affected. These changes are not persisted and become invalid after TiDB restarts.\n" +
		"- Variables can also have `NONE` scope. These variables are read-only, and are typically used to convey static information that will not change after a TiDB server has started.\n" +
		"\n" +
		"Variables can be set with the [`SET` statement](/sql-statements/sql-statement-set-variable.md) on a per-session, instance or global basis:\n" +
		"\n" +
		"```sql\n" +
		"# These two identical statements change a session variable\n" +
		"SET tidb_distsql_scan_concurrency = 10;\n" +
		"SET SESSION tidb_distsql_scan_concurrency = 10;\n" +
		"\n" +
		"# These two identical statements change a global variable\n" +
		"SET @@global.tidb_distsql_scan_concurrency = 10;\n" +
		"SET  GLOBAL tidb_distsql_scan_concurrency = 10;\n" +
		"```\n" +
		"\n" +
		"> **Note:**\n" +
		">\n" +
		"> Executing `SET GLOBAL` applies immediately on the TiDB server where the statement was issued. A notification is then sent to all TiDB servers to refresh their system variable cache, which will start immediately as a background operation. Because there is a risk that some TiDB servers might miss the notification, the system variable cache is also refreshed automatically every 30 seconds. This helps ensure that all servers are operating with the same configuration.\n" +
		">\n" +
		"> TiDB differs from MySQL in that `GLOBAL` scoped variables **persist** through TiDB server restarts. Additionally, TiDB presents several MySQL variables as both readable and settable. This is required for compatibility, because it is common for both applications and connectors to read MySQL variables. For example, JDBC connectors both read and set query cache settings, despite not relying on the behavior.\n" +
		"\n" +
		"## Variable Reference\n\n")

	for _, name := range getSysVarsByOrder() {

		sv := variable.GetSysVar(name)

		if skipSv(sv) {
			continue
		}

		// Print title
		fmt.Printf("### %s", sv.Name)

		// Is there a specific version this was introduced?
		fmt.Printf("%s\n\n", formatSpecialVersionComment(sv))

		// Is there a warning such as deprecatd or experimental?
		fmt.Print(printWarning(sv))

		if sv.Name == variable.TxnIsolation {
			fmt.Println("This variable is an alias for `transaction_isolation`.")
			fmt.Println("")
			continue
		}
		if sv.Name == variable.Identity {
			fmt.Println("This variable is an alias for `last_insert_id`.")
			fmt.Println("")
			continue
		}

		fmt.Printf("- Scope: %s\n", formatScope(sv))
		fmt.Printf("- Default value: %s\n", formatDefaultValue(sv))

		if sv.Type == variable.TypeDuration {
			min := time.Duration(sv.MinValue)
			max := time.Duration(sv.MaxValue)
			fmt.Printf("- Range: `[%s, %s]`\n", fmtDuration(min), fmtDuration(max))
		}

		// If the type is an integer, always print the range
		if sv.Type == variable.TypeInt || sv.Type == variable.TypeUnsigned {
			fmt.Printf("- Range: `[%d, %d]`\n", sv.MinValue, sv.MaxValue)
		}

		// If it's an ENUM, always print the possible values.
		if sv.Type == variable.TypeEnum {
			fmt.Printf("- Possible values: %s\n", formatPossibleValues(sv))
		}

		fmt.Print(printUnits(sv))

		// This is the main description
		fmt.Println(getExtendedDescription(sv))

		if sv.Name != variable.WindowingUseHighPrecision {
			fmt.Print("\n")
		}

	}

}
