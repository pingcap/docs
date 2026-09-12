---
title: 使用 AWS PrivateLink 连接到 TiDB Cloud Lake
summary: 主流云厂商提供的 PrivateLink 风格私有端点（AWS PrivateLink、Azure Private Link、Google Private Service Connect 等）使你能够通过自身网络边界内的私有 IP 地址访问 TiDB Cloud Lake，因此流量无需遍历公共互联网。这可以让你的数据集、凭证和管理操作始终保留在云服务商骨干网络中，并与现有网络策略保持一致。
---

# 使用 AWS PrivateLink 连接到 TiDB Cloud Lake

主流云厂商提供的 PrivateLink 风格私有端点（AWS PrivateLink、Azure Private Link、Google Private Service Connect 等）使你能够通过自身网络边界内的私有 IP 地址访问 {{{ .lake }}}，因此流量无需遍历公共互联网。这可以让你的数据集、凭证和管理操作始终保留在云服务商骨干网络中，并与现有网络策略保持一致。

## 优势 {#benefits}

- 网络隔离：流量始终不会离开你的 VPC/VPN 边界，从而避免暴露到公共端点。
- 合规就绪：更容易满足禁止互联网出口的内部审计和行业要求。
- 稳定的性能：流量通过云服务商骨干网络传输，而不是不可预测的互联网路由。
- 简化控制：复用现有的安全组、路由表和监控来管理访问。

## 工作原理 {#how-it-works}

从 **Connect to {{{ .lake }}}** 对话框中获取 PrivateLink 服务名称，然后创建一个指向该服务的私有端点。云服务商会自动分配私有 IP 地址并接受该端点；启用私有 DNS 后，你的 {{{ .lake }}} 域名会解析到这些地址，因此每个会话都会通过安全的私有路径进行。

## 如何设置 AWS PrivateLink {#how-to-setup-aws-privatelink}

1. 验证你的 VPC 设置。

    确保已勾选 `Enable DNS resolution` 和 `Enable DNS hostnames`。

2. 从 **Connect to {{{ .lake }}}** 对话框中获取要连接的服务名称：

    例如：`com.amazonaws.vpce.us-east-2.vpce-svc-0123456789abcdef0`。

3. 准备一个开放 tcp 443 端口的安全组：

   ![Security Group](/media/tidb-cloud-lake/security-group.png)

4. 前往 AWS Console：

   <https://us-east-2.console.aws.amazon.com/vpcconsole/home?region=us-east-2#Endpoints>：

   点击 `Create endpoint`：

   ![Create Endpoint Button](/media/tidb-cloud-lake/create-endpoint-1.png)

   ![Create Endpoint Sheet](/media/tidb-cloud-lake/create-endpoint-2.png)

   选择之前创建的安全组 `HTTPS`：

   ![Create Endpoint SG](/media/tidb-cloud-lake/create-endpoint-3.png)

5. 等待 PrivateLink 创建完成。

6. 修改私有 DNS 名称设置：

    ![DNS Menu](/media/tidb-cloud-lake/dns-1.png)

    启用私有 DNS 名称：

    ![DNS Sheet](/media/tidb-cloud-lake/dns-2.png)

    等待更改生效。

7. 验证通过 PrivateLink 访问 {{{ .lake }}}：

    Gateway 域名会解析为 VPC 内部 IP 地址。

    > **Note:**
    >
    > 恭喜！你已成功通过 AWS PrivateLink 连接到 {{{ .lake }}}。