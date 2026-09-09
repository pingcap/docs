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

5. Verify the endpoint connection from an ECS instance in your VPC.

    1. On the TiDB Cloud Lake home page, click **Connect**. In the **Connect to TiDB Cloud** dialog, copy the **Host** value under **Connection Information**.

        ![Copy the TiDB Cloud Lake host from the connection information](/media/tidb-cloud-lake/alibaba-privatelink-connection-host.png)

    2. Set `LAKE_HOST` to the host you copied, and then run the following commands:

        ```shell
        LAKE_HOST='<your-tidb-cloud-lake-host>'

        getent ahostsv4 "$LAKE_HOST"

        curl --noproxy '*' -sS -o /dev/null \
          -w 'remote_ip=%{remote_ip}\ntls_verify=%{ssl_verify_result}\n' \
          "https://$LAKE_HOST"
        ```

    3. In the Alibaba Cloud VPC console, open the endpoint details page and find the private IP addresses assigned to the endpoint elastic network interfaces (ENIs). If the hostname resolves to one or more of these addresses and `remote_ip` matches one of them, traffic to TiDB Cloud Lake is routed through Alibaba Cloud PrivateLink without traversing the public Internet. `tls_verify=0` indicates that the HTTPS certificate was verified successfully.

    4. Check the health of the regional gateway:

        ```shell
        curl --noproxy '*' -sS \
          https://gw.aliyun-ap-northeast-1.default.lake.tidbcloud.com/status | jq
        ```

        If the response contains `"status": "ok"`, the regional gateway is available.
