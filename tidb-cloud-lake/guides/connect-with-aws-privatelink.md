---
title: Connecting to TiDB Cloud Lake with AWS PrivateLink
summary: PrivateLink-style private endpoints offered by major clouds (AWS PrivateLink, Azure Private Link, Google Private Service Connect, etc.) let you reach TiDB Cloud Lake through private IP addresses inside your own network boundary, so no traffic has to traverse the public internet. That keeps your datasets, credentials, and admin actions on the provider's backbone and aligned with the network policies you already operate.
---

# Connecting to TiDB Cloud Lake with AWS PrivateLink

PrivateLink-style private endpoints offered by major clouds (AWS PrivateLink, Azure Private Link, Google Private Service Connect, etc.) let you reach {{{ .lake }}} through private IP addresses inside your own network boundary, so no traffic has to traverse the public internet. That keeps your datasets, credentials, and admin actions on the provider's backbone and aligned with the network policies you already operate.

## Benefits

- Network isolation: traffic never leaves your VPC/VPN boundary, removing exposure to public endpoints.
- Compliance ready: easier to satisfy internal audits and industry requirements that forbid internet egress.
- Stable performance: traffic follows the cloud provider backbone instead of unpredictable internet routes.
- Simplified controls: reuse your existing security groups, route tables, and monitoring to govern access.

## How it works

Grab the PrivateLink service name from the **Connect to {{{ .lake }}}** dialog, then create a private endpoint that points to it. The cloud provider automatically allocates private IP addresses and accepts the endpoint, and once private DNS is enabled, your {{{ .lake }}} domains resolve to those addresses so every session stays on the secure, private path.

## How to setup AWS PrivateLink

1. Verify your VPC settings.

    Ensure `Enable DNS resolution` and `Enable DNS hostnames` are checked.

2. Get the service name to connect to from the **Connect to {{{ .lake }}}** dialog:

    For example: `com.amazonaws.vpce.us-east-2.vpce-svc-0123456789abcdef0`.

3. Prepare a security group with tcp 443 port open:

   ![Security Group](/media/tidb-cloud-lake/security-group.png)

4. Go to the [VPC endpoints page](https://us-east-2.console.aws.amazon.com/vpcconsole/home?region=us-east-2#Endpoints) in the AWS Management Console.

    1. Click **Create endpoint**.

        ![Create Endpoint Button](/media/tidb-cloud-lake/create-endpoint-1.png)

    2. In **Endpoint settings**, fill in a name tag if needed, and then select **Endpoint services that use NLBs and GWLBs**.

        ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

    3. In **Service settings**, paste the service name copied in step 2 into **Service name**, and then click **Verify service**.

    4. In **Network settings**, select your VPC.

    5. In **Subnets**, select the availability zones and subnets where you want to create the VPC endpoint.

    6. In **Security groups**, select the security group you prepared in step 3.

        ![Create Endpoint SG](/media/tidb-cloud-lake/create-endpoint-3.png)

    7. Click **Create endpoint**.

5. Wait for the PrivateLink creation.

6. Modify private DNS name setting:

    ![DNS Menu](/media/tidb-cloud-lake/dns-1.png)

    Enable private DNS names:

    ![DNS Sheet](/media/tidb-cloud-lake/dns-2.png)

    Wait for changes to apply.

7. Verify accessing {{{ .lake }}} via PrivateLink:

    Gateway domain is resolved to VPC internal IP address.

    > **Note:**
    >
    > Congratulations! You have successfully connected to {{{ .lake }}} with AWS PrivateLink.
