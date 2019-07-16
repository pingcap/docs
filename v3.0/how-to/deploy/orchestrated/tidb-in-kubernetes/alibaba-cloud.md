---
title: Deploy TiDB on Alibaba Cloud Kubernetes
summary: Learn how to deploy a TiDB cluster on Alibaba Cloud Kubernetes.
category: how-to
---

# Deploy TiDB on Alibaba Cloud Kubernetes

This document describes how to deploy a TiDB cluster on Alibaba Cloud Kubernetes with your laptop (Linux or macOS) for development or testing.

## Prerequisites

- [aliyun-cli](https://github.com/aliyun/aliyun-cli) >= 3.0.15 and [configure aliyun-cli](https://www.alibabacloud.com/help/doc-detail/90766.htm?spm=a2c63.l28256.a3.4.7b52a893EFVglq)

    > **Note:**
    > 
    > The access key used must be granted permissions to control resources.

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.12
- [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.1 and <= 2.11.0
- [jq](https://stedolan.github.io/jq/download/) >= 1.6
- [terraform](https://learn.hashicorp.com/terraform/getting-started/install.html) 0.11.*

### Privileges

To deploy a TiDB cluster, make sure you have the following privileges: 

- AliyunECSFullAccess
- AliyunESSFullAccess
- AliyunVPCFullAccess
- AliyunSLBFullAccess
- AliyunCSFullAccess
- AliyunEIPFullAccess
- AliyunECIFullAccess
- AliyunVPNGatewayFullAccess
- AliyunNATGatewayFullAccess

## Overview

The default setup creates:

- A new VPC
- An ECS instance as the bastion machine
- A managed ACK (Alibaba Cloud Kubernetes) cluster with the following ECS instance worker nodes:

    - An auto-scaling group of 2 * instances (2c2g) as ACK mandatory workers for system service like CoreDNS
    - An auto-scaling group of 3 * `ecs.g5.xlarge` instances for PD
    - An auto-scaling group of 3 * `ecs.i2.2xlarge` instances for TiKV
    - An auto-scaling group of 2 * `ecs.c5.4xlarge` instances for TiDB
    - An auto-scaling group of 1 * `ecs.c5.xlarge` instance for monitoring components

In addition, the monitoring node mounts a 100GB cloud disk as data volume. All the instances except ACK mandatory workers span in multiple available zones to provide cross-AZ high availability.

The auto-scaling group ensures the desired number of healthy instances, so the cluster can auto-recover from node failure or even available zone failure.

## Deploy

Configure the target region and credential (you can also set these variables in `terraform` command prompt):

{{< copyable "shell-regular" >}}

```shell
export TF_VAR_ALICLOUD_REGION=<YOUR_REGION> && \
export TF_VAR_ALICLOUD_ACCESS_KEY=<YOUR_ACCESS_KEY> && \
export TF_VAR_ALICLOUD_SECRET_KEY=<YOUR_SECRET_KEY>
```

The `variables.tf` file contains default settings of variables used for deploying the cluster, you can change it or use `-var` option to override a specific variable to fit your need.

Use the following commands to set up the cluster.

Get the code from Github:

{{< copyable "shell-regular" >}}

```shell
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator/deploy/aliyun
```

Apply the configs, note that you must answer "yes" to `terraform apply` to continue:

{{< copyable "shell-regular" >}}

```shell
terraform init
```

{{< copyable "shell-regular" >}}

```shell
terraform apply
```

If you get an error while running `terraform apply`, fix the error (for example, lack of permission) according to the description and run `terraform apply` again.

`terraform apply` takes 5 to 10 minutes to create the whole stack, once complete, basic cluster information is printed:

```
Apply complete! Resources: 3 added, 0 changed, 1 destroyed.

Outputs:

bastion_ip = 47.96.174.214
cluster_id = c2d9b20854a194f158ef2bc8ea946f20e
kubeconfig_file = /tidb-operator/deploy/aliyun/credentials/kubeconfig
monitor_endpoint = 121.199.195.236:3000
region = cn-hangzhou
ssh_key_file = /tidb-operator/deploy/aliyun/credentials/my-cluster-keyZ.pem
tidb_endpoint = 172.21.5.171:4000
tidb_version = v3.0.0
vpc_id = vpc-bp1v8i5rwsc7yh8dwyep5
```

> **Note:**
>
> You can use the `terraform output` command to get the output again.

You can then interact with the ACK cluster using `kubectl` and `helm` (`cluster_name` is `my-cluster` by default):

{{< copyable "shell-regular" >}}

```shell
export KUBECONFIG=$PWD/credentials/kubeconfig_<cluster_name>
```

{{< copyable "shell-regular" >}}

```shell
kubectl version
```

{{< copyable "shell-regular" >}}

```shell
helm ls
```

## Access the database

You can connect the TiDB cluster via the bastion instance, all necessary information are in the output printed after installation is finished (replace the `<>` parts with values from the output):

{{< copyable "shell-regular" >}}

```shell
ssh -i credentials/<cluster_name>-bastion-key.pem root@<bastion_ip>
```

{{< copyable "shell-regular" >}}

```shell
mysql -h <tidb_slb_ip> -P <tidb_port> -u root
```

## Monitor

Visit `<monitor_endpoint>` to view the grafana dashboards. You can find this information in the output of installation.

The initial login credentials are:

- User: admin
- Password: admin

> **Warning:**
>
> It is strongly recommended to set `monitor_slb_network_type` to `intranet` in `variables.tf` for security if you already have a VPN connecting to your VPC or plan to setup one.

## Upgrade

To upgrade TiDB cluster, modify `tidb_version` variable to a higher version in `variables.tf` and run `terraform apply`.

This may take a while to complete, watch the process using command:

{{< copyable "shell-regular" >}}

```shell
kubectl get pods --namespace tidb -o wide --watch
```

## Scale

To scale the TiDB cluster, modify `tikv_count` or `tidb_count` to your desired numbers, and then run `terraform apply`.

## Destroy

It may take some while to finish destroying the cluster.

{{< copyable "shell-regular" >}}

```shell
terraform destroy
```

Alibaba cloud terraform provider does not handle kubernetes creation error properly, which causes an error when destroying. In that case, you can remove the kubernetes resource from the local state manually and proceed to destroy the rest resources:

{{< copyable "shell-regular" >}}

```shell
terraform state list
```

{{< copyable "shell-regular" >}}

```shell
terraform state rm module.ack.alicloud_cs_managed_kubernetes.k8s
```

> **Note:**
> 
> You have to manually delete the cloud disk used by monitoring node in Aliyun's console after destroying if you don't need it anymore.

## Customize

### Customize TiDB Operator

To customize TiDB Operator, change the variables in `variables.tf` according to their descriptions. It is worth noting that the `operator_helm_values` variable allows you provide a customized `values.yaml` for TiDB Operator, for example:

```hcl
variable "operator_helm_values" {
  default = file("my-operator-values.yaml")
}
```

By default, the terraform script will create a new VPC. You can use an existing VPC by setting `vpc_id` to use an existing VPC. Note that kubernetes node will only be created in available zones that has vswitch existed when using existing VPC.

### Customize TiDB cluster

The TiDB cluster uses `./my-cluster.yaml` as the `values.yaml` file, so you can customize the TiDB cluster by editing this file. Refer to [TiDB in Kubernetes cluster configuration](/reference/configuration/tidb-in-kubernetes/cluster-configuration.md) for available configuration options.

## Manage Multiple TiDB clusters

If you want to manage multiple TiDB clusters in one Kubernetes cluster, you can edit the `./main.tf` to add the declaration of `tidb-cluster` module as needed, for example:

```hcl
module "tidb-cluster-dev" {
  source = "../modules/aliyun/tidb-cluster"
  providers = {
    helm = helm.default
  }

  cluster_name = "another-cluster"
  ack          = module.tidb-operator

  pd_count                   = 1
  tikv_count                 = 1
  tidb_count                 = 1
  override_values            = file("dev-cluster.yaml")
}

module "tidb-cluster-staging" {
  source = "../modules/aliyun/tidb-cluster"
  providers = {
    helm = helm.default
  }

  cluster_name = "another-cluster"
  ack          = module.tidb-operator

  pd_count                   = 3
  tikv_count                 = 3
  tidb_count                 = 2
  override_values            = file("staging-cluster.yaml")
}
```

Note that the `cluster_name` must be unique accross the clusters. The availabel configuration options of `tidb-cluster` module are as follows:

| 参数名 | 说明 | 默认值 |
| :----- | :---- | :----- |
| `ack` | An object that encapsulates the information of Kubernetes cluster | `nil` |
| `cluster_name` | TiDB cluster name, must be unique | `nil` |
| `tidb_version` | TiDB cluster version | `v3.0.0` |
| `tidb_cluster_chart_version` | version of the `tidb-cluster` helm chart | `v1.0.0-beta.3"` |
| `pd_count` | PD replica number | 3 |
| `pd_instance_type` | PD instance type | `ecs.g5.large` |
| `tikv_count` | TiKV replica number | 3 |
| `tikv_instance_type` | TiKV instance type | `ecs.i2.2xlarge` |
| `tidb_count` | TiDB replica number | 2 |
| `tidb_instance_type` | TiDB instance type | `ecs.c5.4xlarge` |
| `monitor_instance_type` | Monitor node instance type | `ecs.c5.xlarge` |
| `override_values` | The content of `values.yaml` for TiDB cluster, it is recommend to read it from a file via the `file()` function call | `nil` |
| `local_exec_interpreter` | Interpreter to execute local command | `["/bin/sh", "-c"]` |

## Manage Multiple Kubernetes Clusters

It is recommended to use a separate Terraform module for each Kubernetes cluster (a Terraform module is a directory containing `.tf` scripts).

Actually, the `deploy/aliyun` module composes several reusable modules under the `deploy/modules` directory. When managing multiple Kubernetes clusters, you can compose these modules in a new directory as per your requirements. Steps are as follows:

1. Create a directory for each Kubernetes cluster：

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p deploy/aliyun/aliyun-staging
    ```

2. Refer to the `deploy/aliyun/main.tf` to write your own Terraform script, here is a simple example：

    ```hcl
    provider "alicloud" {
        region     = <YOUR_REGION>
        access_key = <YOUR_ACCESS_KEY>
        secret_key = <YOUR_SECRET_KEY>
    }

    module "tidb-operator" {
        source     = "../modules/aliyun/tidb-operator"

        region          = <YOUR_REGION>
        access_key      = <YOUR_ACCESS_KEY>
        secret_key      = <YOUR_SECRET_KEY>
        cluster_name    = "example-cluster"
        key_file        = "ssh-key.pem"
        kubeconfig_file = "kubeconfig"
    }

    provider "helm" {
        alias    = "default"
        insecure = true
        install_tiller = false
        kubernetes {
            config_path = module.tidb-operator.kubeconfig_filename
        }
    }

    module "tidb-cluster" {
        source = "../modules/aliyun/tidb-cluster"
        providers = {
            helm = helm.default
        }

        cluster_name = "example-cluster"
        ack          = module.tidb-operator
    }

    module "bastion" {
        source = "../modules/aliyun/bastion"

        bastion_name             = "example-bastion"
        key_name                 = module.tidb-operator.key_name
        vpc_id                   = module.tidb-operator.vpc_id
        vswitch_id               = module.tidb-operator.vswitch_ids[0]
        enable_ssh_to_worker     = true
        worker_security_group_id = module.tidb-operator.security_group_id
    }
    ```

You can customize the above script as needed, for example, you can remove the `bastion` section if you don't need a bastion machine.

Optionally, you can copy and edit the `deploy/aliyun` directory, but note that you cannot copy the directory which you have already run `terraform apply` against. It is recommended to clone a new repository before copying to ensure the Terraform state of the directory is clean.

## Limitations

You cannot change `pod cidr`, `service cidr` and worker instance types once the cluster is created.
