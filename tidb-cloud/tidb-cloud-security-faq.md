---
title:  Security FAQs
summary: Learn about the most frequently asked security questions (FAQs) relating to TiDB Cloud.
---

#  Security FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked security questions about TiDB Cloud.

## How does TiDB Cloud protect my data privacy？
 
At TiDB Cloud, customer trust is our top priority. TiDB Cloud continually monitors the evolving privacy regulatory and legislative landscape to identify changes and determine what tools our customers might need to meet their compliance needs. Maintaining customer trust is an ongoing commitment. We strive to inform you of the privacy and data security policies, practices, and technologies we’ve put in place. Our commitments include:

- Access: As a customer, you maintain full control of your content that you upload to the TiDB Cloud under your TiDB Cloud  account, and responsibility for configuring access to TiDB Cloud and resources. We provide an advanced set of access, encryption, and logging features to help you do this effectively (e.g., https://docs.pingcap.com/tidbcloud/set-up-private-endpoint-connections,https://docs.pingcap.com/tidbcloud/manage-user-access and https://docs.pingcap.com/tidbcloud/tidb-cloud-auditing). We do not access or use your content for any purpose without your agreement. 

- Storage: You choose the TiDB Cloud  Regions in which your content is stored. You can replicate and back up your content in more than one TiDB Cloud  Regions. We will not move or replicate your content outside of your chosen TiDB Cloud Regions except as agreed with you.

- Disclosure of customer content:We will not disclose customer content as governed by the Privacy Policy. (For details about TiDB Cloud's Privacy Policy) unless we're required to do so to comply with the law or a binding order of a government body. If a governmental body sends TiDB Cloud  a demand for your customer content, we will attempt to redirect the governmental body to request that data directly from you. If compelled to disclose your customer content to a government body, we will give you reasonable notice of the demand to allow the customer to seek a protective order or other appropriate remedy unless TiDB Cloud is legally prohibited from doing so.

## How does TiDB Cloud classify customer information？

We define customer data as your business data, database files (including backups and snapshots), logs, and customer PII that a customer sends to the TiDB cluster for analysis, processing, storage, or hosting by TiDB Cloud in connection with the customer's account. For example, customer data includes data that a customer or their consumers store in TiKV or Tiflash, which are located in S3 buckets or EBS of AWS.

Customer data does not include TiDB Cloud operational, clinic, and meta data（For details about TiDB Cloud's Privacy Policy）:

- Operational data includes TiDB Cloud control plane logs, runtime metrics, usage policies, and service ticket-related information.

- Clinic data includes TiDB Cluster logs (including logs, error logs, and slow query logs), metrics (including usage and runtime metrics), configuration (including TiDB Cluster config items, node IPs, and values), monitoring, and alert-related information.

- Meta data includes TiDB Cloud customer register accounts (including email, company name, phone number, and IP address), permissions, endpoint services, devices, versions, and tag-related information.

TiDB Cloud operational data is described in [TiDB Cloud Privacy Policy](https://www.pingcap.com/privacy-policy/) and [TiDB Cloud Data Processing Agreement](https://www.pingcap.com/legal/data-processing-agreement-for-tidb-cloud-services/).

## Who owns customer Data？

As a customer, you own your customer data and have the right to choose which TiDB Cloud can process, store, and host it. TiDB Cloud will not access or use your customer data without your permission. 

## Who has control over customer data？

As a customer, you have control over your customer data:

- You decide where your customer data will be stored, including the type of storage and geographic location.

- You determine the level of security for your customer data based on your industry's data security and privacy policies. TiDB Cloud offers hosting encryption features to protect your customer data in transit and when stored at different security levels.

- You manage access to your customer data, as well as access to the TiDB Cloud database and tools, through users, roles, and credentials that you control.

## Where is Customer Data stored？

With TiDB Cloud, you have the flexibility to choose how and where you want to run your TiDB database. When you do, you will have access to the same database tools, storage locations, regional control planes, APIs, Chat2query, and other database services. If you want to run your database globally, you can choose from 7 regions on AWS or GCP.

As a customer, you decide in which AWS/GCP region your customer data will be stored, allowing you to deploy your TiDB cluster in the locations that meet your specific geographic needs. For example, if a TiDB Cloud customer in the USA wants to store their customer data only in the USA, they can choose to deploy their TiDB cluster exclusively in the US West (Oregon) AWS Region.

You can replicate and back up your customer data in multiple AWS/GCP regions. We will not move or replicate your customer data outside of your chosen AWS/GCP region without your agreement.

## What is my role in securing customer Data？

When assessing the security and compliance of roles and responsibilities, it is crucial to differentiate between the security role of TiDB Cloud and your own security role in using the TiDB Cloud. TiDB Cloud is responsible for implementing and maintaining its own security measures, while you are responsible for ensuring the security and compliance of your TiDB cluster within the TiDB Cloud environment. Your security role in the TiDB Cloud involves implementing and managing any security features and measures related to your use of the TiDB Cloud.

## Who can access customer data in TiDB Cloud？

At TiDB Cloud, our highest priority is securing our customer's data, and we implement rigorous contractual,technical and organizational measures to protect TiDB Cloud confidentiality,integrity,and availability regardless of which TiDB Cloud region a customer has selected.

TiDB Cloud provides a multi-tenant TiDB Cloud SaaS database service platform, follows the multi-tenant isolation architecture and best practices of AWS and GCP SaaS applications, and designs isolation measures and security features for account, authentication,authorization, VPC access control, multiple encryption, and auditing.

TiDB Cloud has designed customers with a secure and credible database SAAS platform. We limit the access and time of internal employees to the TiDB Cloud infrastructure in accordance with the principle of least privilege. Any internal Oncall , developers, and operation employees only access TiDB Cloud infrastructure through strict approval processes and Bastion on time, and any privileged users behavior who login and operate is monitored and alert on time.

TiDB Cloud has designed an internal operations account permission isolation structure to prevent any internal personnel from accessing TiDB clusters using privileged service accounts. The service account is only invoked when the customer initiates the TiDB cluster initialization through the Console or command line. Upon completion of the TiDB initialization, the customer becomes the owner of the most privileged root account and the service account is transferred to their control. TiDB Cloud employees do not have access to the service account credentials or permissions that are initialized by TiDB.

## Could customer run TiDB Cloud in my VPC?

No. TiDB Cloud is Database-as-a-Service (DBaaS) and runs only in the TiDB Cloud VPC. As a cloud computing managed service, TiDB Cloud provides access to a database without requiring the setup of physical hardware and the installation of software.

## How to encrypt customer data in TiDB Cloud？

TiDB Cloud uses storage volume encryption by default for customer data at rest, including your database data and backup data. TiDB Cloud requires TLS encryption for customer data in transit, and also requires component-level TLS encryption for data in your dedicated TIDB cluster between TiDB, PD, TiKV, and TiFlash.For more detial information, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## How to configure a secure TiDB Cluster？

In TiDB Cloud, you can use either a Dedicated Tier cluster or a Serverless Tier cluster according to your needs.

For Dedicated Tier clusters, TiDB Cloud ensures cluster security with the following measures:

- Creates independent sub-accounts and VPCs for each cluster.

- Set up firewall rules to isolate external connections.

- Creates server-side TLS certificates and component-level TLS certificates for each cluster to encrypt cluster data in transit.

- Provide IP access rules for each cluster to ensure that only allowed source IP addresses can access your cluster.

For Serverless Tier clusters, TiDB Cloud ensures cluster security with the following measures:

- Creates independent sub-accounts for each cluster.

- Set up firewall rules to isolate external connections.

- Provides cluster server TLS certificates to encrypt cluster data in transit.