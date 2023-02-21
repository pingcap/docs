---
title: Security FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud security.
---

# Security FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Cloud security.

## How does TiDB Cloud classify customer data?

Customer data refers to the data that customer applications send to TiDB Cloud clusters for analysis, processing, and storage under their accounts. TiDB Cloud classifies customer data into the following categories:

- Business data (including consumer data and table data)
- Database files (including database backups and snapshots)
- SQL logs
- Personally identifiable information (PII) of customers' consumers (excluding TiDB Cloud account registration and login information)

Customer data includes data that customers or their consumers store in TiKV or TiFlash, which is located in the cloud providers' storage (such as S3 buckets or EBS of AWS).

Customer data does not include TiDB Cloud's operational, diagnosis, or metadata:

- Operational data: TiDB Cloud control plane logs, runtime metrics, usage policies, and service ticket-related information.
- Diagnosis data: TiDB cluster logs (including logs, error logs, and slow query logs), metrics (including usage and runtime metrics), configuration (including TiDB cluster configuration items, node IP addresses, and values), monitoring, and alert-related information.
- Metadata: TiDB Cloud account registration information (including email, company name, phone number, and IP address), permissions, endpoint services, devices, versions, and tag-related information.

For more information about the operational data, see [TiDB Cloud Privacy Policy](https://www.pingcap.com/privacy-policy/) and [TiDB Cloud Data Processing Agreement](https://www.pingcap.com/legal/data-processing-agreement-for-tidb-cloud-services/).

## Who owns customer data?

As a customer, you have full ownership of your data and can choose which TiDB Cloud cluster can process, store, and host your data. TiDB Cloud will not access or use your data without your permission.

## Who has control over customer data?

As a customer, you have complete control over your data:

- You can choose how to protect your data using TiDB Cloud, which offers encryption at rest and in transit to safeguard your data. Additionally, you have the option to manage your encryption key. If you prefer to bring your key, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

- You can manage access to your data, as well as the TiDB Cloud databases and tools, through users, roles, and credentials that you control.

## Where is customer data stored?

In TiDB Cloud, you have the flexibility to choose how and where you want to run your TiDB database. This grants you access to TiDB database tools, storage locations, regional control planes, APIs, Chat2Query, and other database services. If you want to run your database globally, you can select from various regions on AWS or GCP.

As a customer, you can choose in which AWS or GCP region you want to store your data by creating your TiDB cluster in the desired region that meets your geographic needs. For instance, if you are in the USA and prefer to store your data only in the USA, you can deploy a TiDB cluster exclusively in the AWS Oregon (us-west-2) region.

## What are the responsibility in securing customer data?

When it comes to securing customer data, it is important to understand the roles and responsibilities of both TiDB Cloud and customers.

TiDB Cloud is responsible for ensuring the sustainable, safe, stable, and compliant operation of the TiDB Cloud service, including the TiDB Cloud underlying infrastructure and the control plane.

Customers are responsible for the security and compliance of your TiDB cluster, including managing access controls, implementing security features, and monitoring the security posture of your cluster. You are also responsible for the security and compliance of any data that you store, process, and transmit through your TiDB cluster. It is important to ensure that your TiDB cluster is configured to meet your security and compliance requirements.

## Who can access customer data in TiDB Cloud?

TiDB Cloud places the highest priority on customer data security. Regardless of the region selected, TiDB Cloud implements technical, contractual, and organizational measures to ensure data confidentiality, integrity, and availability.

TiDB Cloud has achieved SOC2 Type II, General Data Protection Regulation (GDPR), Payment Card Industry Data Security Standard (PCI DSS), and Health Insurance Portability and Accountability Act of 1996 (HIPAA) certification and verification. Additionally, third-party auditors are invited to review the certified standards annually. For more information, see the [PingCAP Trust Center](https://www.pingcap.com/trust-compliance-center).

In TiDB Cloud, data access is secured with the following measures:

- TiDB Cloud has designed a multi-tenant architecture for its database service platform that follows best practices of AWS and GCP SaaS applications. The security functions and isolation mechanisms include multi-tenant authentication and authorization, network access control, data encryption, and auditing.

- TiDB Cloud has designed a secure technical architecture that prohibits insiders from directly accessing the TiDB Cloud infrastructure. No PingCAP staff can directly access the TiDB Cloud infrastructure where customer data resides. If PingCAP technical personnel need to monitor and maintain the TiDB Cloud infrastructure, they must go through a strict approval process, obtain minimum permissions, and pass the Bastion audit. All operational behaviors are recorded and audited, and monitoring and alarms are configured for unauthorized access.

## How is customer data encrypted in TiDB Cloud?

At TiDB Cloud, the security of customer data is a top priority. Here's how TiDB Cloud encrypts customer data:

- Encryption at rest: TiDB Cloud uses storage volume encryption by default to encrypt all customer data at rest, including database data and backup data. This encryption ensures that data is protected.

- Encryption in transit: TiDB Cloud requires Transport Layer Security (TLS) encryption for all customer data in transit. Additionally, TiDB Cloud requires component-level TLS encryption for data in your Dedicated Tier cluster between TiDB, TiKV, and TiFlash. This encryption ensures that all data transmitted between components is encrypted and protected against interception and unauthorized access.

For more details, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Can I run TiDB Cloud in my own VPC?

No, it is not possible to run TiDB Cloud in your own VPC. TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that only runs in the TiDB Cloud VPC. This cloud computing managed service allows you to access a database without the need for physical hardware or software installation.
