---
title:  Security FAQs
summary: Learn about the most frequently asked security questions (FAQs) relating to TiDB Cloud.
---

#  Security FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked security questions about TiDB Cloud.

## How does TiDB Cloud classify customer data？

Customer data is that customer app sends to the TiDB cluster for analysis, processing, storage by TiDB Cloud in connection with the customer's account. TiDB Cloud defines customer data as follows:

- Business data (including consumer data and table data)
- Database files (including database backups and snapshots)
- Logs (including SQL logs and )
- Consumer personally identifiable information (PII) （including consumer personally identifiable information，but don't include relevant PII information when customers register and log in to TiDB Cloud）

For example, customer data includes data that a customer or their consumers store in TiKV or Tiflash, which are located in S3 buckets or EBS of AWS.

Customer data does not include TiDB Cloud operational, diagnosis, and metadata as follows:

- Operational data includes TiDB Cloud control plane logs, runtime metrics, usage policies, and service ticket-related information
- Diagnosis data includes TiDB cluster logs (including logs, error logs, and slow query logs), metrics (including usage and runtime metrics), configuration (including TiDB cluster configuration items, node IPs, and values), monitoring, and alert-related information.
- Metadata includes TiDB Cloud account registration information (including email, company name, phone number, and IP address), permissions, endpoint services, devices, versions, and tag-related information.

For more information about TiDB Cloud operational data, see [TiDB Cloud Privacy Policy](https://www.pingcap.com/privacy-policy/) and [TiDB Cloud Data Processing Agreement](https://www.pingcap.com/legal/data-processing-agreement-for-tidb-cloud-services/).

## Who owns customer Data？

As a customer, you own your data and have the right to choose which TiDB Cloud cluster can process, store, and host it. TiDB Cloud will not access or use your data without your permission. 

## Who has control over customer data？

As a customer, you have full control of your data:

- You decide where your data will be stored, including the type of storage and geographic location.

- You determine the level of security of your data based on your industry's data security and privacy policies. TiDB Cloud offers encryption features to protect your data either in transit or stored at different security levels.

- You manage access to your data, as well as access to the TiDB Cloud databases and tools, through users, roles, and credentials that you control.

## Where is Customer Data stored？

In TiDB Cloud, you have the flexibility to choose how and where you want to run your TiDB database. When you do, you will have access to the same database tools, storage locations, regional control planes, APIs, Chat2Query, and other database services. If you want to run your database globally, you can choose from various regions on AWS or GCP.

As a customer, you can decide in which AWS or GCP region your data will be stored by deploying your TiDB cluster in the target region that meets your geographic needs. For example, if you are in the USA and you want to store all your data only in the USA, you can choose to deploy a TiDB cluster exclusively in the AWS Oregon (us-west-2) region.

You can also replicate and back up your data in multiple AWS or GCP regions. PingCAP will not move or replicate your data outside of your chosen AWS or GCP region without your agreement.

## What is my role in securing customer data？

When you assess the security and compliance of roles and responsibilities, it is crucial to differentiate between the security role of TiDB Cloud and the security role of your own in using TiDB Cloud. 

TiDB Cloud is responsible for implementing and maintaining its own security measures, while you are responsible for ensuring the security and compliance of your TiDB cluster within the TiDB Cloud environment. Your security role in TiDB Cloud involves implementing and managing any security features and measures related to your use of TiDB Cloud.

## Who can access customer data in TiDB Cloud？

At TiDB Cloud, our highest priority is securing our customer's data, and we implement rigorous contractual,technical and organizational measures to protect TiDB Cloud confidentiality,integrity,and availability regardless of which TiDB Cloud region a customer has selected.

TiDB Cloud provides a multi-tenant SaaS database service platform, follows the multi-tenant isolation architecture and best practices of AWS and GCP SaaS applications, and designs isolation measures and security features for accounts, authentication, authorization, VPC access control, multiple encryption, and auditing.

TiDB Cloud has designed a secure and credible database SAAS platform, which limits the access of internal employees to the TiDB Cloud infrastructure in accordance with the principle of least privilege. For any technical support, PingCAP developers and operation employees can only access TiDB Cloud infrastructure through strict approval processes and Bastion on time, and any privileged users' behavior of login and operation is monitored and alerted on time.

TiDB Cloud has designed an internal operation account permission isolation structure to prevent any internal personnel from accessing TiDB clusters using privileged service accounts. The service account is only invoked when the customer initiates the TiDB cluster through the TiDB Cloud console or command line. Upon completion of the TiDB initialization, the customer becomes the owner of the most privileged root account and the service account is transferred to their control. PingCAP employees do not have access to the service account credentials or permissions that are initialized by TiDB.

## How does TiDB Cloud encrypts customer data？

TiDB Cloud uses storage volume encryption by default for customer data at rest, including both database data and backup data. TiDB Cloud requires TLS encryption for customer data in transit, and also requires component-level TLS encryption for data in your Dedicated Tier cluster between TiDB, PD, TiKV, and TiFlash.

For more details, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## How do I configure a secure TiDB cluster？

In TiDB Cloud, you can use either a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster or a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) cluster according to your needs.

For Dedicated Tier clusters, TiDB Cloud ensures cluster security with the following measures:

- Creates independent sub-accounts and VPCs for each cluster.

- Set up firewall rules to isolate external connections.

- Creates server-side TLS certificates and component-level TLS certificates for each cluster to encrypt cluster data in transit.

- Allows you to [configure an IP access list](/tidb-cloud/configure-ip-access-list.md) for each cluster to filter the IP addresses that can access your cluster.

For Serverless Tier clusters, TiDB Cloud ensures cluster security with the following measures:

- Creates independent sub-accounts for each cluster.

- Set up firewall rules to isolate external connections.

- Provides cluster server TLS certificates to encrypt cluster data in transit.

## Can I run TiDB Cloud in my own VPC?

No. TiDB Cloud is Database-as-a-Service (DBaaS) and runs only in the TiDB Cloud VPC. As a cloud computing managed service, TiDB Cloud provides access to a database without requiring the setup of physical hardware and the installation of software.
