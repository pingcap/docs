---
title: Integrate TiDB Cloud BYOC with Prometheus and Grafana
summary: Learn how to connect Grafana to your TiDB Cloud BYOC metrics endpoint and import dashboards to monitor instances and resource pools.
---

# Integrate TiDB Cloud BYOC with Prometheus and Grafana

TiDB Cloud BYOC provides a Prometheus-compatible metrics endpoint in your cloud environment. You can connect Grafana directly to this endpoint to monitor your BYOC instances and resource pools.

A single Prometheus data source provides access to instance, resource pool, and infrastructure metrics. This document describes how to configure network connectivity, add the data source in Grafana, and import the BYOC dashboards for deployments on AWS.

## Prerequisites

Before you begin, make sure that you have:

- A Grafana instance running version 10 or later. Version 11.3.1 or later is recommended.
- AWS permissions to view load balancers in the account and Region that host your BYOC deployment, including `elasticloadbalancing:DescribeLoadBalancers`.
- If network connectivity is not already configured, AWS permissions to configure the relevant VPC peering or PrivateLink resources, route tables, security groups, and network ACLs.
- Network access from your Grafana environment to the BYOC metrics endpoint over HTTPS on TCP port `443`.

## Step 1. Get the metrics endpoint

Each AWS BYOC deployment region has a regional metrics read load balancer whose name starts with `ngx-r-`. You can find its DNS name using either the AWS console or AWS CLI.

Select the AWS account and Region that host your target BYOC deployment. You do not need to know the complete load balancer name.

<SimpleTab>
<div label="AWS Console">

1. Sign in to the AWS account that hosts your BYOC deployment and select the target AWS Region.
2. Open the **EC2** console. In the navigation pane, under **Load Balancing**, choose **Load Balancers**.
3. Filter the load balancer list by name and search for the prefix `ngx-r-`.
4. Select the matching load balancer and confirm that its state is **Active**.
5. In the **Details** section, copy the **DNS name**. Use this value as `<metrics-ingress-host>` in the following steps.

</div>
<div label="AWS CLI">

Make sure that the AWS CLI is installed and configured with credentials for the account that hosts your BYOC deployment.

1. Set your AWS CLI profile and target Region:

    ```bash
    BYOC_AWS_PROFILE="<your-aws-profile>"
    BYOC_AWS_REGION="<aws-region>"
    ```

2. List load balancers whose names start with `ngx-r-`:

    ```bash
    aws elbv2 describe-load-balancers \
      --profile "${BYOC_AWS_PROFILE}" \
      --region "${BYOC_AWS_REGION}" \
      --query "LoadBalancers[?starts_with(LoadBalancerName, 'ngx-r-')].[LoadBalancerName,DNSName,State.Code]" \
      --output table
    ```

3. Identify the load balancer for your BYOC deployment and confirm that its state is `active`.
4. Copy its `DNSName` value. Use this value as `<metrics-ingress-host>` in the following steps.

</div>
</SimpleTab>

If no matching load balancer is returned, verify the AWS account, Region, and your permission to describe load balancers.

If multiple matching load balancers are listed, use their VPC IDs and deployment information to identify the correct one, or ask your BYOC administrator to confirm it.

## Step 2. Configure network connectivity

Your Grafana environment must be able to resolve the metrics endpoint DNS name and access the endpoint over HTTPS on TCP port `443`.

Keep the metrics endpoint accessible only from trusted monitoring environments. Configure security groups and network connectivity to allow only the required monitoring traffic, and do not expose the endpoint to the public internet.

### Same VPC

If Grafana and the BYOC observability (O11Y) endpoint are in the same VPC:

- Allow outbound TCP `443` from Grafana to the metrics endpoint.
- Ensure that network ACLs allow requests and return traffic.

### Cross-VPC: same or different AWS accounts

Choose one of the following connection methods:

- **VPC Peering**: establish peering between the Grafana VPC and the VPC that hosts the BYOC metrics endpoint. Update the route tables on both sides to allow traffic between the relevant subnets.
- **AWS PrivateLink**: use a private endpoint connection to access the BYOC metrics service. This option is recommended for environments with strict network isolation requirements.

For either method, ensure that:

- Your Grafana environment can resolve the metrics endpoint DNS name to an address reachable through the configured connection.
- Security groups allow the required outbound HTTPS traffic.
- Network ACLs permit requests and return traffic.

In the default PingCAP-managed BYOC setup, you do not need to modify the O11Y-side managed ingress security group.

## Step 3. Verify connectivity

Before configuring the Grafana data source, run the following commands from the Grafana host or its runtime environment.

1. Verify DNS resolution:

    ```bash
    nslookup <metrics-ingress-host>
    ```

    Confirm that the name resolves to an address reachable from your Grafana environment.

2. Verify the metrics read endpoint:

    ```bash
    curl -sS -G \
      "https://<metrics-ingress-host>/multitenant/metrics/api/v1/query" \
      --data-urlencode 'query=count(tidb_server_maxprocs) by (component)'
    ```

    A successful request returns HTTP `200` and a Prometheus-compatible JSON response with `"status": "success"`. An empty `result` means that the query did not match any metric series; it does not indicate a network connection failure.

If DNS resolution or the request fails, check the network connection, route tables, security groups, and network ACLs before continuing.

## Step 4. Add a Prometheus data source in Grafana

1. In Grafana, go to **Connections** > **Data sources** > **Add data source**.
2. Select **Prometheus**.
3. Enter a name for the data source.
4. Set the Prometheus server URL to:

    ```text
    https://<metrics-ingress-host>/multitenant/metrics
    ```

5. Click **Save & test**. Confirm that Grafana reports that the data source is working.
6. Open **Explore**, select the new data source, and run the following query:

    ```promql
    count(tidb_server_maxprocs) by (component)
    ```

    Review the returned series to verify that Grafana can retrieve metrics.

## Step 5. Import the BYOC dashboards

The BYOC dashboard JSON templates contain predefined panels, queries, and filters. Import them into Grafana to view metrics without creating each panel manually.

Both templates use the Prometheus data source configured in Step 4.

| Dashboard | Description | Download |
|:---|:---|:---|
| Instance dashboard | Displays metrics for individual BYOC instances. Use the **Instance ID** filter to select the instance to monitor. | [Instance dashboard JSON](https://github.com/pingcap/docs/tree/release-8.5/tidb-cloud/byoc/metrics-dashboard-instance.json) |
| Resource Pool dashboard | Displays resource pool metrics. Use the **Resource Pool ID** filter to select the resource pool to monitor. | [Resource Pool dashboard JSON](https://github.com/pingcap/docs/tree/release-8.5/tidb-cloud/byoc/metrics-dashboard-resource-pool.json) |

To import a dashboard:

1. Open the corresponding JSON file using the download link, and save its raw contents as a `.json` file.
2. In Grafana, go to **Dashboards** > **New** > **Import**.
3. Upload the downloaded JSON file.
4. When prompted to select a **Prometheus** data source, select the data source created in Step 4.
5. Click **Import**.
6. Select the target **Instance ID** or **Resource Pool ID**, and choose a time range to view the metrics.

Repeat these steps to import the other dashboard if needed. You do not need to manually edit data source UIDs in either template.

You can customize the imported dashboards by adding or removing panels and adjusting display options.

## Troubleshooting

### Grafana cannot connect to the metrics endpoint

Verify that the endpoint DNS name resolves from the Grafana environment and that HTTPS traffic can reach the endpoint. For cross-VPC connections, check the VPC peering or PrivateLink configuration, route tables where applicable, security groups, and network ACLs.

### The dashboard shows no data

- Confirm that the dashboard uses the correct Prometheus data source.
- Select the correct **Instance ID** or **Resource Pool ID**.
- Choose a time range in which the target instance or resource pool was running.
- Use **Explore** to check whether the data source returns metrics.

If you cannot resolve the issue, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
