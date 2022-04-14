---
title: TiDB Dashboard Instance Profiling - Continuous Profiling
summary: Learn how to collect performance data from TiDB, TiKV and PD continuously to reduce MTTR.
---

# TiDB Dashboard Instance Profiling - Continuous Profiling

> **Note:**
>
> This feature is designed for database experts. For non-expert users, it is recommended to use this feature under the guidance of PingCAP technical supports.

Continuous Profiling allows collecting performance data **continuously** from each TiDB, TiKV and PD instance. The collected performance data can be visualized as FlameGraph or DAG.

With these performance data, experts can analyze resource consumption details like instance's CPU and memory, to help pinpoint sophisticated performance problems at any time, such as high CPU overhead, high memory usage, process stalls, and so on. Even for problems cannot be reproduced, experts can dig deep into the problem by viewing the historical performance data collected at that moment. In this way, MTTR can be reduced effectively.

## Compare with Manual Profiling

Continuous Profiling is an enhanced feature of [Manual Profiling](/dashboard/dashboard-profiling.md). They can be both used to collect and analyze different kind of performance data for each instance, with the main differences as follows:

- Manual Profiling only collects performance data for a short period of time (e.g. 30 seconds) at the moment when user initiates the profiling, while Continuous Profiling collects continuously when it is enabled.
- Manual Profiling can only be used to analyze current occurring problems, while Continuous Profiling can be used to analyze both the current and historical problems.
- Manual Profiling allows to collect specific performance data for specific instances, while Continuous Profiling collects all performance data for all instances.
- Continuous Profiling stores more performance data, therefore it takes up more disk space.
- Continuous Profiling currently does not collect performance data from TiFlash due to the impact to the stability when profiling is performed frequently.

## Supported Performance Data

All performance data in [Manual Profiling](/dashboard/dashboard-profiling.md#supported-performance-data) is collected except for TiFlash CPU data, which is not collected due to stability reasons.

- CPU: The CPU overhead of each internal function on TiDB, TiKV and PD instances

  > The CPU overhead of TiKV instances is currently not supported in ARM architecture.

- Heap: The memory consumption of each internal function on TiDB and PD instances

- Mutex: The mutex contention states on TiDB and PD instances

- Goroutine: The the running state and call stack of all goroutines on TiDB and PD instances

## Access the page

You can access the Continuous Profiling page using either of the following methods:

- After logging into TiDB Dashboard, click **Advanced Debugging** > **Profiling Instances** > **Continuous Profiling** on the left navigation bar.

  ![Access page](/media/dashboard/dashboard-conprof-access.png)

- Visit <http://127.0.0.1:2379/dashboard/#/continuous_profiling> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Enable Continuous Profiling

> **Note:**
>
> To use Continuous Profiling, your cluster should be deployed or upgraded with a recent version of TiUP (v1.9.0 and above) or TiDB Operator (v1.3.0 and above). If your cluster was upgraded with an older version, see [FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown) for instructions.

Continuous Profiling is not enabled by default. When enabled, performance data will be continuously collected in the background. You do not need to keep the web page open. The collected data can be kept for a certain period of time and old data will be automatically expired.

To enable this feature:

1. Visit the [Continuous Profiling page](#access-the-page).
2. Click **Open Settings**. In the **Settings** area on the right, switch **Enable Feature** on, and modify the default value of **Retention Duration** if necessary.
3. Click **Save**.

![Enable feature](/media/dashboard/dashboard-conprof-start.png)

## View Current Performance Data

Manual Profiling cannot be initiated on clusters that have Continuous Profiling enabled. To view the performance data at the current moment, just click on the most recent profiling result.

## View Historical Performance Data

You can see all collected performance data since the feature was enabled in the list page.

![History results](/media/dashboard/dashboard-conprof-history.png)

## Download Performance Data

On the profiling result page, you can click **Download Profiling Result** in the upper-right corner to download all profiling results.

![Download profiling result](/media/dashboard/dashboard-conprof-download.png)

You can also click an individual instance in the table to view its profiling result. Alternatively, you can hover on ... to download raw data.

![View profiling result](/media/dashboard/dashboard-conprof-single.png)

## Disable Continuous Profiling

1. Visit the [Continuous Profiling page](#access-the-page).
2. Click the **Gear icon** in the upper right corner to open the settings page. Switch **Enable Feature** off.
3. Click **Save**.
4. In the popped-up dialog box, click **Disable**.

![Disable feature](/media/dashboard/dashboard-conprof-stop.png)

## Frequently Asked Questions

**1. Feature cannot be enabled as the UI displays "required component NgMonitoring is not started"**.

See [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown).

**2. Is there any performance impact when enabled?**

According to our benchmark, the average performance impact is less than 1% when the feature is enabled.

**3. What is the status of this feature?**

This is a generally available feature and can be used in production environments.
