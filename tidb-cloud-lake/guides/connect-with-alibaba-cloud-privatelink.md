---
title: 使用 Alibaba Cloud PrivateLink 连接到 TiDB Cloud Lake
summary: 配置 Alibaba Cloud 私有端点，启用其自定义域名，并验证到 TiDB Cloud Lake 的私有连接。
---

# 使用 Alibaba Cloud PrivateLink 连接到 TiDB Cloud Lake

本文档介绍如何配置 Alibaba Cloud 私有端点、启用其自定义域名，并验证到 TiDB Cloud Lake 的私有连接。

## 设置 Alibaba Cloud PrivateLink {#set-up-alibaba-cloud-privatelink}

1. 从 **Connect to {{{ .lake }}}** 对话框中获取端点服务名称。

    例如：`com.aliyuncs.privatelink.ap-northeast-1.epsrv-6weddzcbkanrx5sc2zv4`

2. 准备一个安全组，允许入站 TCP 流量通过 443 端口。

    ![允许 HTTPS 流量的安全组](/media/tidb-cloud-lake/alibaba-privatelink-security-group.png)

3. 在 [Alibaba Cloud VPC 控制台](https://vpc.console.aliyun.com/endpoint/ap-northeast-1/endpoints/new)中创建一个端点。本示例使用 Japan (Tokyo)。

    输入步骤 1 中的端点服务名称，然后点击 **Verify**。

    ![使用 Lake 端点服务名称创建端点](/media/tidb-cloud-lake/alibaba-privatelink-create-endpoint.png)

    确认设置后，点击页面底部的创建按钮。

4. 在端点详情页面，启用 **Custom Domain Name**。

    ![启用自定义域名](/media/tidb-cloud-lake/alibaba-privatelink-custom-domain-name.png)

5. 从你的 VPC 中的 Elastic Compute Service (ECS) 实例验证端点连接。

    1. 在 TiDB Cloud Lake 首页，点击 **Connect**。在 **Connect to TiDB Cloud** 对话框中，复制 **Connection Information** 下的 **Host** 值。

        ![从连接信息中复制 TiDB Cloud Lake 主机](/media/tidb-cloud-lake/alibaba-privatelink-connection-host.png)

    2. 将 `LAKE_HOST` 设置为你复制的主机，然后运行以下命令：

        ```shell
        LAKE_HOST='<your-tidb-cloud-lake-host>'

        getent ahostsv4 "$LAKE_HOST"

        curl --noproxy '*' -4 -sS -o /dev/null \
          -w 'remote_ip=%{remote_ip}\ntls_verify=%{ssl_verify_result}\n' \
          "https://$LAKE_HOST"
        ```

    3. 在 Alibaba Cloud VPC 控制台中，打开端点详情页面，找到分配给端点弹性网卡（ENI）的私有 IP 地址。确认 `getent ahostsv4` 返回的每个 IPv4 地址都是端点 ENI 的私有 IP 地址，并且 `remote_ip` 与其中一个地址匹配。这表明已测试的到 TiDB Cloud Lake 的连接使用的是 Alibaba Cloud PrivateLink，而不会遍历公共互联网。`tls_verify=0` 表示 HTTPS 证书验证成功。

    4. 检查区域网关的健康状态。以 Japan (Tokyo) Region 为例：

        ```shell
        curl --noproxy '*' -sS \
          https://gw.aliyun-ap-northeast-1.default.lake.tidbcloud.com/status
        ```

        如果响应中包含 `"status": "ok"`，则表示该区域网关可用。