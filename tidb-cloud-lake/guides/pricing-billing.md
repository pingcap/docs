---
title: Pricing & Billing
summary: Understand the pricing model and billing details for TiDB Cloud Lake.
---

# Pricing & Billing

Your costs on {{{ .lake }}} consist of the following components: warehouses, storage, and cloud service fees. This page contains information about the pricing of each component and how the billing works.

## {{{ .lake }}} Pricing

This section provides pricing information on warehouse, storage, and cloud service.

### Warehouse Pricing

Your warehouses incur costs when they are running (specifically, when in the Running state). The cost depends on the warehouse's size and running time. **Billing is calculated on a per-second basis**. For example, if you have a warehouse running for three seconds, you will be charged for that exact duration.

The size of a warehouse refers to the maximum number of concurrent queries it can handle, and prices vary based on the different sizes available and the {{{ .lake }}} edition you use.

| Size    | EC2                     | Personal Tier Listing Price ($/h) | Business Tier Listing Price ($/h) |
|---------|-------------------------|-----------------------------------|-----------------------------------|
| XSmall  | r8g.2xlarge 8c 64 GiB   | 1.6                               | 2.4                               |
| Small   | r8g.4xlarge 16c 128 GiB | 3.2                               | 4.8                               |
| Medium  | 32c 256 GiB             | 6.4                               | 9.6                               |
| Large   | r8g.16xlarge 64c 512 GiB| 12.8                              | 19.2                              |
| XLarge  | 128c                    | 25.6                              | 38.4                              |
| 2XLarge | 256c                    | 51.2                              | 76.8                              |
| 3XLarge | 512c                    | 102.4                             | 153.6                             |
| 4XLarge | 1024c                   | 204.8                             | 307.2                             |
| 5XLarge | 2048c                   | 409.6                             | 614.4                             |
| 6XLarge | 4096c                   | 819.2                             | 1228.8                            |

A suspended warehouse does not consume any resources. By default, {{{ .lake }}} automatically suspends a warehouse after five minutes of inactivity to save resources and costs. You can adjust or disable this automatic suspension feature according to your preferences.

### Storage Pricing

Your data in {{{ .lake }}} is physically stored in Amazon S3. Storage costs in {{{ .lake }}} are based on Amazon S3's pricing. Currently, both the Personal Edition and Business Edition are priced at $23.00 per month per terabyte (TB).

| Edition          | Price per TB per Month |
| ---------------- | ---------------------- |
| Personal Edition | $23.00                 |
| Business Edition | $23.00                 |

### Cloud Service Pricing

The cloud service fee currently includes fees for the API requests. Each time you run a SQL query with {{{ .lake }}}, a REST API request is sent to the `databend-query` through the {{{ .lake }}} HTTP handler. In the Personal Edition, you are billed $1 for every 10,000 API requests, while in the Business Edition, the cost is $2 for every 10,000 API requests.

| Edition          | Cost per 10,000 API Requests |
| ---------------- | ---------------------------- |
| Personal Edition | $1.00                        |
| Business Edition | $2.00                        |

## Example-1

**Usage Scenario:** A user is using an XSmall warehouse (Business) and occasionally queries data. This specific query took 5 minutes and 20 seconds, and the data storage size is 100GB.

| Cost | Formula | Amount |
|------|---------|--------|
| Compute | $0.000416667 × (5×60+20) | $0.13 |
| Storage | $23 ÷ 1024 ÷ 30 × 100 | $0.75 |
| **Daily Total** | | **$0.88** |
| **Monthly Total** | | **$26.40** |

## Example-2

**Usage Scenario:** A user is using an XSmall warehouse (Business) to continuously import data into {{{ .lake }}}. The warehouse runs 24 hours a day with 1TB storage, using Task service for minute-by-minute data loading. The estimated number of API calls is 50,000.

| Cost | Formula | Amount |
|------|---------|--------|
| Compute | $1.50 × 24h | $36.00/day |
| Storage | $23 ÷ 30 | $0.77/day |
| Cloud Service | $2 × 5 | $10.00/day |
| **Daily Total** | | **$46.77** |
| **Monthly Total** | | **$1,403.10** |

## {{{ .lake }}} Billing

The billing period is set for every calendar month, starting from the 1st day to the last day of the month. For your first month, the billing period will begin on the day your organization was created.

To check your billing details, go to **Manage** and then click on **Billing**. From there, you can review your bills and link a credit card for payment.

When billing users, {{{ .lake }}} applies vouchers first. If multiple vouchers are available, the system prioritizes deduction from the voucher with the earliest expiration date. Please ensure vouchers are used before their expiration date.
