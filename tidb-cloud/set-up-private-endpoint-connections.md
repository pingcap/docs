---
title: Set Up Private Endpoint Connections
summary: Learn how to set up private endpoint connections in TiDB Cloud.
---

# Set Up Private Endpoint Connections

This document introduces what is a private endpoint, how to use it in TiDB Cloud, the limitations of it, and the billing information.

TiDB Cloud supports using a private endpoint to privately connect your virtual private cloud (VPC) to the TiDB Cloud service hosted in an AWS VPC via the AWS PrivateLink, as if the service were in your own VPC. This TiDB Cloud service is called an endpoint service.

Powered by [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), this endpoint connection is secure and private, and does not expose your data to the public internet.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

The cloud vendor AWS generates a specific DNS hostname for your endpoint service. Before you grant permissions to service consumers or specific AWS principals (AWS accounts, IAM users, and IAM roles) by default, they do not have access to your endpoint service. For more detailed definitions of the private endpoint and private endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

The relationship of a TiDB cluster in TiDB Cloud, an endpoint service, and a private endpoint is as follows:

- Each TiDB cluster corresponds to one private endpoint service, and each private endpoint service corresponds to one TiDB cluster.
- Each endpoint service corresponds to one or multiple private endpoints.
- Each TiDB cluster corresponds to one or multiple private endpoints.

## Why should I use private endpoint

- Enhanced security: The private endpoint connection uses a private IP and does not expose your traffic to the public internet, which avoids the risk of data leakage.
- Ease of network management: The private endpoint is easy to create and manage. You do not need to use an internet gateway, NAT device, public IP address, Amazon Direct Connect connection, or Amazon Site-to-Site VPN connection to allow communication with the service from your private subnets.

## Limitations

- Currently, TiDB Cloud supports private endpoint connection only when the endpoint service is hosted in AWS. If the service is hosted in Google Cloud Platform (GCP), the private endpoint is not supported.
- The private endpoint support is provided only for the TiDB Cloud Dedicated Tier, not for the Developer Tier.
- Private endpoint connection across regions is not supported.

## How to use private endpoint

This section describes how to create, edit, delete or terminate a private endpoint, and how to connect to a private endpoint service.

### Create a private endpoint

### Edit a private endpoint

### Delete or terminate a private endpoint

### Connect to a private endpoint service

## Billing information

## Status information of private endpoint and private endpoint service

