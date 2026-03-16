---
title: "Connecting to Databend Cloud with AWS PrivateLink"
sidebar_label: "AWS PrivateLink"
---

# Connecting to Databend Cloud with AWS PrivateLink

PrivateLink-style private endpoints offered by major clouds (AWS PrivateLink, Azure Private Link, Google Private Service Connect, etc.) let you reach Databend Cloud through private IP addresses inside your own network boundary, so no traffic has to traverse the public internet. That keeps your datasets, credentials, and admin actions on the provider's backbone and aligned with the network policies you already operate.

## Benefits

- Network isolation: traffic never leaves your VPC/VPN boundary, removing exposure to public endpoints.
- Compliance ready: easier to satisfy internal audits and industry requirements that forbid internet egress.
- Stable performance: traffic follows the cloud provider backbone instead of unpredictable internet routes.
- Simplified controls: reuse your existing security groups, route tables, and monitoring to govern access.

## How it works

After Databend Cloud approves the cloud account or project you plan to connect, you create a private endpoint that points to the Databend PrivateLink service for your region. The cloud provider automatically allocates private IP addresses and, once private DNS is enabled, your Databend Cloud domains resolve to those addresses so every session stays on the secure, private path.

## How to setup AWS PrivateLink

1. Provide the AWS account ID you are planning to connect to Databend Cloud:

   For example: `123456789012`

2. Verify your VPC settings

   ![VPC Settings](/img/cloud/privatelink/aws/vpc-settings.png)

   Ensure `Enable DNS resolution` and `Enable DNS hostnames` are checked.

3. Wait for cloud admin adding your account to whitelist, and get a service name for the cluster to connect to:

   For example: `com.amazonaws.vpce.us-east-2.vpce-svc-0123456789abcdef0`

4. Prepare a security group with tcp 443 port open:

   ![Security Group](/img/cloud/privatelink/aws/security-group.png)

5. Goto AWS Console:

   https://us-east-2.console.aws.amazon.com/vpcconsole/home?region=us-east-2#Endpoints:

   Click `Create endpoint`:

   ![Create Endpoint Button](/img/cloud/privatelink/aws/create-endpoint-1.png)

   ![Create Endpoint Sheet](/img/cloud/privatelink/aws/create-endpoint-2.png)

   Select the previously created security group `HTTPS`

   ![Create Endpoint SG](/img/cloud/privatelink/aws/create-endpoint-3.png)

   ![Create Endpoint Done](/img/cloud/privatelink/aws/create-endpoint-4.png)

6. Wait for cloud admin approving your connect request:

   ![Request](/img/cloud/privatelink/aws/request.png)

7. Wait for the PrivateLink creation:

   ![Creation](/img/cloud/privatelink/aws/creation.png)

8. Modify private DNS name setting:

   ![DNS Menu](/img/cloud/privatelink/aws/dns-1.png)

   Enable private DNS names:

   ![DNS Sheet](/img/cloud/privatelink/aws/dns-2.png)

   Wait for changes to apply.

9. Verify accessing Databend Cloud via PrivateLink:

   ![Verify DNS](/img/cloud/privatelink/aws/verify-1.png)

   ![Verify Response](/img/cloud/privatelink/aws/verify-2.png)

   Gateway domain is resolved to VPC internal IP address.

:::info
Congratulations! You have successfully connected to Databend Cloud with AWS PrivateLink.
:::
