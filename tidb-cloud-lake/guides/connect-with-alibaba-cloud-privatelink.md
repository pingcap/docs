---
title: Connect to TiDB Cloud Lake with Alibaba Cloud PrivateLink
summary: Configure an Alibaba Cloud private endpoint, enable its custom domain name, and verify private connectivity to TiDB Cloud Lake.
---

# Connect to TiDB Cloud Lake with Alibaba Cloud PrivateLink

This document describes how to configure an Alibaba Cloud private endpoint, enable its custom domain name, and verify private connectivity to TiDB Cloud Lake.

## Set up Alibaba Cloud PrivateLink

1. Get the endpoint service name from the **Connect to {{{ .lake }}}** dialog.

    For example: `com.aliyuncs.privatelink.ap-northeast-1.epsrv-6weddzcbkanrx5sc2zv4`.

2. Prepare a security group that allows inbound TCP traffic on port 443.

    ![Security group allowing HTTPS traffic](/media/tidb-cloud-lake/alibaba-privatelink-security-group.png)

3. In the [Alibaba Cloud VPC console](https://vpc.console.aliyun.com/endpoint/ap-northeast-1/endpoints/new), create an endpoint. This example uses Japan (Tokyo).

    Enter the endpoint service name from Step 1 and click **Verify**.

    ![Create an endpoint with the Lake endpoint service name](/media/tidb-cloud-lake/alibaba-privatelink-create-endpoint.png)

    Confirm the settings and click the create button at the bottom of the page.

4. On the endpoint details page, enable **Custom Domain Name**.

    ![Enable the custom domain name](/media/tidb-cloud-lake/alibaba-privatelink-custom-domain-name.png)

5. Verify the endpoint connection from your VPC:

    ```shell
    curl -v https://gw.aliyun-ap-northeast-1.default.lake.tidbcloud.com/status | jq
    ```

    Check that the gateway hostname resolves to the endpoint's private IP address. If the response contains `"status": "ok"`, the endpoint connection is available.
