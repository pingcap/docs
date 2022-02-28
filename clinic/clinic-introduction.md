---
title:  Overview of TiDB Clinic Diagnostic Service
summary: Learn about the Clinic Diagnostic Service, including tool components, user scenarios, and implementation principles.
---

## Overview of TiDB Clinic Diagnostic Service

TiDB Clinic Diagnostic Service (TiDB Clinic) is a diagnostic service provided by PingCAP for TiDB clusters that are deployed using either TiUP or TiDB Operator. This service helps to troubleshoot cluster problems remotely and provides a quick check of cluster status locally. With TiDB Clinic, you can ensure the stable operation of your TiDB cluster for its full life-cycle, predict potential issues, reduce the probability of issues, troubleshoot problems quickly, and fix problems.

TiDB Clinic is currently in the Beta testing stage, so only the invited users can use the service. The service provides the following two components to diagnose clusters:

- Diag: a diagnostic tool deployed on the cluster side. Diag is used to collect cluster diagnostic data, upload diagnostic data to the Clinic Server, and perform a quick health check locally on the cluster. For a full list of diagnostic data collected by Diag, see [Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md).

    > **Note:**
    >
    > - Diag temporarily **does not support** collecting data from the clusters with the TLS encryption enabled and the clusters deployed using TiDB Ansible.
    > - TiDB Clinic is currently in the Beta testing stage for invited users only. If you need to upload data to the Clinic Server using Diag, contact [PingCAP technical support](https://en.pingcap.com/contact-us/) to get a trial account first.

- Clinic Server: a cloud service deployed in the cloud. By providing diagnostic services in the SaaS model, the Clinic Server can not only receive uploaded diagnostic data but also work as an online diagnostic environment to store data, view data, and provide cluster diagnostic reports.

    > **Note:**
    >
    > For the Clinic Beta version, external users cannot use the features of the Clinic Server. After you upload collected data to the Clinic Server and get a data link using Diag, only authorized PingCAP technical support staff can access the link and view the data.

## User scenarios

- Troubleshoot cluster problems remotely:

    When your cluster has some issues that cannot be fixed quickly, you can ask for help at TiDB Community or contact PingCAP technical support. When applying technical support for remote assistance, you need to save various diagnostic data from the cluster and forward the data to them. In this case, you can use Diag to collect diagnostic data with one click. Diag helps you to collect complete diagnostic data quickly, which can replace complex manual data collection operations. After collecting data, you need to upload the data to the Clinic Server for PingCAP technical support staff. The Clinic Server provides secure storage for diagnostic data and supports the online diagnosis, improving the efficiency of troubleshooting.

- Perform a quick check for the cluster status locally:

    Even if your cluster runs stably now, it is necessary to periodically check the cluster for potential stability risks. You can check the potential health risks of a cluster using the local quick check feature provided by the Clinic diagnostic service. The Clinic Beta version provides a rationality check on cluster configuration items to discover unreasonable configurations and provide modification suggestions.

## Implementation principles

This section introduces the implementation principles about how Diag (a cluster-side tool provided by the Clinic service) collects diagnostic data of a cluster.

First, Diag gets cluster topology information from the deployment tool TiUP (tiup-cluster) or TiDB Operator (tidb-operator). Then, Diag collects different types of diagnostic data through various data collection methods as follows:

- Transfer server files through SCP

    For clusters deployed using TiUP, Diag can collect log files and configuration files directly from the nodes of the target component through the secure copy protocol (SCP).

- Collect data by running commands remotely through SSH

    For clusters deployed using TiUP, Diag can connect to the target component system through SSH (Secure Shell), and run commands (such as Insight) to obtain system information, including kernel logs, kernel parameters, and basic information of the system and the hardware.

- Collect data through HTTP call

    - By calling the HTTP interface of TiDB components, Diag can get the real-time configuration sampling information and the real-time performance sampling information of TiDB, TiKV, PD, and other components.
    - By calling the HTTP interface of Prometheus, Diag can get alert information and monitoring metrics data.

- Query database parameters through SQL statements

    Using SQL statements, Diag can query the system variables and other information of the TiDB database. To use this method, you need to **additionally provide** the username and password to access the TiDB database when collecting data.

## Next step

 - [Use Clinic](/clinic/clinic-data-instruction-for-tiup.md)
 - [Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md)