---
title: Clinic Diagnostic Service Overview
summary: Introduces the Clinic diagnostic service, including tool components, usage scenarios, and implementation principles.
---

## Clinic Diagnostic Service Overview

Clinic is a diagnostic service provided by PingCAP for TiDB clusters. To the clusters deployed using TiUP and TiDB Operator, this service provides remote troubleshooting and local quick check for the cluster status. Using the service, you can ensure the stable operation of your TiDB cluster for its full life-cycle, predict potential issues, reduce the probability of the issues, quickly troubleshoot, and fix issues.

The Clinic diagnostic service is currently in Beta testing stage, so only the invited users can use the service. The service provides the following two components to diagnose clusters:

- Diag: The tool deployed on the cluster side. Diag is used to collect cluster diagnostic data, upload the diagnostic data to Clinic Server, and perform quick health check locally on the cluster. For the list of diagnostic data collected by Diag, see [Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md).

    > **Note:**
    >
    > - Diag temporarily **does not support** collecting data in the clusters with TLS encryption enabled and the clusters deployed using TiDB Ansible.
    > - The Clinic diagnostic service is currently in Beta testing stage, so only the invited users can use the service. If you need to upload data to Clinic Server using Diag, you should get a trial account from the PingCAP technical support you contacted before.

- Clinic Server: The cloud service deployed in the cloud. By providing diagnostic services in SaaS mode, Clinic Server can not only receive the diagnostic data uploaded to the Clinic Server, but also store the data, view and diagnose the uploaded data online, and provide cluster diagnostic reports.

    > **Note:**
    >
    > In Beta version of Clinic diagnostic service, external users cannot use the features of the Clinic server. After you upload the collected data to the Clinic Server and get the data link, only authorized PingCAP technical supports can access the link and view the data.

## Usage scenarios

- Troubleshoot a cluster remotely:

    When you cluster has some issues that cannot be fixed quickly, you can ask for help at TiDB Community or contact PingCAP technical support. When applying technical support for remote assistance, you need to save various diagnostic data from the cluster and forward the data to them. In this case, you can use Diag to collect diagnostic data with one click. Diag helps you to collect complete diagnostic data quickly, which can replace complex manual data collection operations. After collecting data, you need to upload the data to the Clinic Server for PingCAP technical support. The Clinic Server provides secure storage for diagnostic data and supports online diagnosis, improving the efficiency of troubleshooting.

- Quick check for cluster status locally:

    Even if your cluster can run normally, it is necessary to periodically check the cluster for potential stability risks. You can check the potential health risks of the cluster using the local quick check feature provided by the Clinic diagnostic service. Clinic Beta version mainly provides a rationality check for cluster configuration items to discover unreasonable configurations and provide modification suggestions.

## Implementation Principles

This section mainly introduces the implementation principles of Diag, a cluster-side tool provided by the Clinic service, to collect diagnostic data of a cluster.

First, Diag needs to get cluster topology information from the deployment tool TiUP (tiup-cluster) or TiDB Operator (tidb-operator). Then, Diag collects different types of diagnostic data through various data collection methods as follows:

- Transfer server files through SCP

    For clusters deployed using TiUP, Diag can collect log files and configuration files directly from the nodes of the target component through SCP (Secure copy protocol).

- Collect data by running commands remotely through SSH

    For clusters deployed using TiUP, Diag can connect to the target component system through SSH (Secure Shell), and run commands (such as Insight) to obtain system information, including kernel logs, kernel parameters, and basic information of the system and the hardware.

- Collect data through HTTP call

    - By calling the HTTP interface of TiDB components, Diag can get the real-time configuration sampling information and the real-time performance sampling information of TiDB, TiKV, PD, and other components.
    - By calling the HTTP interface of Prometheus, Diag can get alert information and metrics monitoring data.

- Query database parameters through SQL statements

    Using SQL statements, Diag can query the system parameters and other information of the TiDB database. To use this method, you need to **additionally provide** the username and password to access the TiDB database when collecting data.

## See also

 - [Use Clinic](/clinic/clinic-data-instruction-for-tiup.md)
 - [Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md)