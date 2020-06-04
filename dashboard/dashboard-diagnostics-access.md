---
title: TiDB Dashboard Cluster Diagnostics Page
summary: Learn how to use the cluster diagnostics.
category: how-to
---

# TiDB Dashboard Cluster Diagnostics Page

The cluster diagnostics feature in TiDB Dashboard diagnoses the problems that might exist in a cluster within a specified time range, and summarizes the diagnostic results and the cluster-related load monitoring information into a diagnostic report. This diagnostic report is in the form of a web page. You can browse and circulate this page offline after saving it using a browser.

> **Note:**
>
> The cluster diagnostics feature depends on the Prometheus monitoring component deployed in the cluster. See [TiUP](/tiup/tiup-overview.md) or [TiDB Ansible](/online-deployment-using-ansible.md) deployment document to learn how to deploy the monitoring component. If no monitoring component is deployed in the cluster, the generated diagnostic report will indicate a failure.

## Access the page

You can use one of the following two methods to access the cluster diagnostics page:

* After logging into TiDB Dashboard, click **Cluster Diagnostics** on the left navigation menu:

    ![Access Cluster Diagnostics page](/media/dashboard/dashboard-diagnostics-access.png)

* Visit <http://127.0.0.1:2379/dashboard/#/diagnose> in your browser. Replace `127.0.0.1:2379` with the actual PD address and port.

## Generate diagnostic report

To diagnose a cluster within a time range and check the cluster load, you can take these steps to generate a diagnostic report over a period of time:

1. Set the start time of range, such as `2020-05-21 14:40:00`.
2. Set the length of the range, such as `10 min`.
3. Click **Start**.

![Generate diagnostic report](/media/dashboard/dashboard-diagnostics-gen-report.png)

> **Note:**
>
> It is recommended that you set the time range of the report between 1 minute and 60 minutes, and it is currently not recommended to generate reports that exceed 1 hour.

The steps above generate a diagnostic report for the time range from `2020-05-21 14:40:00` to `2020-05-21 14:50:00`. After clicking **Start**, you can see the interface below. **Progress** is the progress bar for generating the report. After the report is generated, click **View Full Report**.

![Report progress](/media/dashboard/dashboard-diagnostics-gen-process.png)

## Generate comparison diagnostic report

If the system is abnormal at a certain point, such as QPS jitter or the latency becomes higher, a diagnostic report can be generated that compares the system in the abnormal time range with the system in the normal time range. For example:

* Abnormal time range: `2020-05-21 14:40:00` ~ `2020-05-21 14:45:00`. Within this time range, the system is abnormal.
* Normal time range: `2020-05-21 14:30:00` ~ `2020-05-21 14:35:00`. Within this time range, the system is normal.

You can take the following steps to generate a comparison report for the two time ranges above:

1. Set the start time of the range, which is the start time of the range in which the system is abnormal, such as `2020-05-21 14:40:00`.
2. Set the range duration. Generally, this duration is the duration of system anomalies, such as 5 minutes.
3. Enable **Compare by baseline**.
4. Set the baseline start time, which is the start time of the range (to compare) in which the system is normal, such as `2020-05-21 14:30:00`.
5. **Click Start**.

![Generate comparison report](/media/dashboard/dashboard-diagnostics-gen-compare-report.png)

Then wait for the report to be generated and click **View Full Report**.

In addition, the generated diagnostic report is displayed in the list on the main page of the diagnostic report. You can click to view the previously generated reports which do not need to be generated for a second time.
