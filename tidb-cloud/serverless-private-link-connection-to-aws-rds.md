# Set Up Private Link Connection Connect to AWS RDS

The document describes how to connect to an AWS RDS, using AWS Endpoint Service private link connection.

## Prerequisites

1. Ensure that you have the following authorization to set up a RDS in your own AWS account.

    - Manage RDS instances
    - Manage security groups

2. Ensure that you have the following authorization to set up a load balancer and endpoint service in your own AWS account.

    - Manage security groups
    - Manage load balancer
    - Manage endpoint services

3. Get the {{.essential}} account ID and available zones, save the information for later use.

    1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
    2. On the **Private Link Connection For Dataflow**, Click **Create Private Link Connection**.
    3. You can find the AWS account ID and available zones information.

## Set up RDS instance

### Create a new RDS instance


### Check an existing RDS instance