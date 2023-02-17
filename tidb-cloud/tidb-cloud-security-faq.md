---
title: Security FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud security.
---

# Security FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Cloud security.

## How does TiDB Cloud classify customer data?

Customer data is the data sent from customer applications to TiDB Cloud clusters for analysis, processing, and storage with customers' accounts. TiDB Cloud classifies customer data as follows:

- Business data (including consumer data and table data)
- Database files (including database backups and snapshots)
- SQL logs
- Consumer personally identifiable information (PII) (not including TiDB Cloud account registration and login information)

Customer data includes data that a customer or their consumers store in TiKV or TiFlash, which is located in Amazon S3 buckets or EBS of AWS.

Customer data does not include TiDB Cloud operational, diagnosis, or metadata:

- Operational data: TiDB Cloud control plane logs, runtime metrics, usage policies, and service ticket-related information.
- Diagnosis data: TiDB cluster logs (including logs, error logs, and slow query logs), metrics (including usage and runtime metrics), configuration (including TiDB cluster configuration items, node IP addresses, and values), monitoring, and alert-related information.
- Metadata: TiDB Cloud account registration information (including email, company name, phone number, and IP address), permissions, endpoint services, devices, versions, and tag-related information.

For more information about TiDB Cloud operational data, see [TiDB Cloud Privacy Policy](https://www.pingcap.com/privacy-policy/) and [TiDB Cloud Data Processing Agreement](https://www.pingcap.com/legal/data-processing-agreement-for-tidb-cloud-services/).

## Who owns customer data?

As a customer, you own your data and have the right to choose which TiDB Cloud cluster can process, store, and host the data. TiDB Cloud will not access or use your data without your permission. 

## Who has control over customer data?

As a customer, you have full control of your data:

- You determine the level of security of your data based on your industry's data security and privacy policies. TiDB Cloud offers encryption features to protect your data either in transit or stored at different security levels.

- You manage access to your data, as well as access to the TiDB Cloud databases and tools through users, roles, and credentials that you control.

## Where is customer data stored?

In TiDB Cloud, you have the flexibility to choose how and where you want to run your TiDB database. When you do, you have access to your TiDB database tools, storage locations, regional control planes, APIs, Chat2Query, and other database services. If you want to run your database globally, you can choose from various regions on AWS or GCP.

As a customer, you can decide in which AWS or GCP region your data will be stored by creating your TiDB cluster in the target region that meets your geographic needs. For example, if you are in the USA and you want to store all your data only in the USA, you can choose to deploy a TiDB cluster exclusively in the AWS Oregon (us-west-2) region.

You can also replicate and back up your data in multiple AWS or GCP regions. PingCAP will not move or replicate your data outside of your chosen AWS or GCP region without your permission.

## What are the roles in securing customer data?

When you assess the security and compliance of roles and responsibilities, it is crucial to differentiate between the security role of TiDB Cloud and the security role of your own in using TiDB Cloud. 

TiDB Cloud is mainly responsible for implementing and maintaining the sustainable, safe, stable, and compliant operation of TiDB Cloud.

As a customer, you are your database owner, and you take the administrative and operational role of your database. You are primarily responsible for ensuring the security and compliance of your TiDB cluster within the TiDB Cloud. And your role in TiDB Cloud also involves implementing and managing any security features and access control policies of your own TiDB cluster.

## Who can access customer data in TiDB Cloud?

The security of customer data is the highest priority for TiDB Cloud. Regardless of which TiDB Cloud region you have selected, TiDB Cloud implements rigorous technical, contractual, and organizational measures to safeguard your data confidentiality, integrity, and availability.

TiDB Cloud has passed the standard certification and verification of SOC2 Type II, General Data Protection Regulation (GDPR), Payment Card Industry Data Security Standard (PCI DSS), and Health Insurance Portability and Accountability Act of 1996 (HIPAA), and PingCAP invites third-party auditors to audit the certified standards every year. For details, see [PingCAP Trust Center](https://www.pingcap.com/trust-compliance-center).

In TiDB Cloud, the data access security measures includes the following:

- TiDB Cloud has designed a multi-tenant TiDB Cloud database service platform that follows the multi-tenant isolation architecture and best practices of AWS and GCP SaaS applications. The security functions and isolation mechanisms include multi-tenant authentication and authorization, network access control, data encryption, and auditing, focusing on protecting customer data with ongoing security and compliance.

- TiDB Cloud has designed a secure and trusted TiDB Cloud technical architecture. The architecture effectively isolates and prohibits any insiders from directly accessing the TiDB Cloud infrastructure. No PingCAP staff can directly access the TiDB Cloud infrastructure where customer data resides. If internal technical personnel needs to monitor and maintain the TiDB Cloud infrastructure, they must go through a strict approval process, obtain minimum permissions, and pass the Bastion audit to complete the approved operation and maintenance within a limited time. Moreover, all operational behaviors will be recorded and audited, and TiDB Cloud also configures monitoring and alarms for unauthorized operation and maintenance.

- TiDB Cloud has designed an isolation structure for internal operation account permissions to prevent internal personnel from using a privileged service account to access TiDB clusters. The service account is only used for initializing Serverless Tier and Dedicated Tier through the TiDB Cloud service gateway, and PingCAP staff do not have access and permissions to credentials of this service account. After TiDB Cloud is initialized, you have the maximum authority over your TiDB clusters.

## How does TiDB Cloud encrypt customer data?

TiDB Cloud uses storage volume encryption by default for customer data at rest, including both database data and backup data. TiDB Cloud requires TLS encryption for customer data in transit, and also requires component-level TLS encryption for data in your Dedicated Tier cluster between TiDB, TiKV, and TiFlash.

For more details, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Can I run TiDB Cloud in my own VPC?

No. TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) and runs only in the TiDB Cloud VPC. As a cloud computing managed service, TiDB Cloud provides access to a database without requiring the setup of physical hardware and the installation of software.
