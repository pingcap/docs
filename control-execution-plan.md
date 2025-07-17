---
title: 控制执行计划
summary: 本章介绍在 TiDB 中控制执行计划生成的方法，包括使用 hints、SQL 计划管理以及优化规则的 blocklist。此外，还可以通过修改系统变量和 `tidb_opt_fix_control` 变量来控制执行计划。这些方法有助于防止集群升级后由于优化器行为变化引起的性能回归。
---

# 控制执行计划

SQL 调优的前两章介绍了如何理解 TiDB 的执行计划以及 TiDB 如何生成执行计划。本章将介绍在确定执行计划存在问题时，可以采用哪些方法来控制执行计划的生成。本章主要包括以下三个方面：

- 在 [Optimizer Hints](/optimizer-hints.md) 中，你将学习如何使用 hints 来引导 TiDB 生成执行计划。
- 但 hints 会对 SQL 语句进行侵入式修改。在某些场景下，不能简单地插入 hints。在 [SQL Plan Management](/sql-plan-management.md) 中，你将了解 TiDB 如何使用另一种语法非侵入式地控制执行计划的生成，以及后台自动执行计划演化的方法。这种方法有助于解决由版本升级引起的执行计划不稳定和集群性能下降等问题。
- 最后，你将学习如何使用 [Blocklist of Optimization Rules and Expression Pushdown](/blocklist-control-plan.md) 中的 blocklist。

<CustomContent platform="tidb">

除了上述方法外，执行计划还受到一些系统变量的影响。通过在系统级或会话级修改这些变量，你可以控制执行计划的生成。从 v6.5.3 和 v7.1.0 开始，TiDB 引入了一个较为特殊的变量 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)。该变量可以接受多个控制项，以更细粒度地控制优化器的行为，从而防止集群升级后优化器行为变化引起的性能回归。有关更详细的介绍，请参考 [Optimizer Fix Controls](/optimizer-fix-controls.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

除了上述方法外，执行计划还受到一些系统变量的影响。通过在系统级或会话级修改这些变量，你可以控制执行计划的生成。从 v6.5.3 和 v7.1.0 开始，TiDB 引入了一个较为特殊的变量 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)。该变量可以接受多个控制项，以更细粒度地控制优化器的行为，从而防止集群升级后优化器行为变化引起的性能回归。有关更详细的介绍，请参考 [Optimizer Fix Controls](https://docs.pingcap.com/tidb/v7.2/optimizer-fix-controls)。

</CustomContent>