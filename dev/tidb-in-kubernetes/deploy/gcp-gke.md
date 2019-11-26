---
title: Deploy TiDB on GCP GKE
summary: Learn how to deploy a TiDB cluster on GCP GKE.
category: how-to
---

# Deploy TiDB on GCP GKE

<!-- markdownlint-disable MD029 -->

This document describes how to deploy a TiDB cluster on GCP GKE with your laptop (Linux or macOS) for development or testing.

> **Warning:**
>
> The GKE support for multiple disks per node has [known issues](https://github.com/pingcap/tidb-operator/issues/684) that make it not ready for production usage. We are working to get GKE to resolve this issue.

## Prerequisites

First of all, make sure the following items are installed on your machine:

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [Terraform](https://www.terraform.io/downloads.html) >= 0.12
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) >= 1.14
* [Helm](https://helm.sh/docs/using_helm/#installing-the-helm-client) >= 2.9.0 and < 3.0.0
* [jq](https://stedolan.github.io/jq/download/)

## Configure

To guarantee a smooth deployment, you need to do some configuration. Before configuring Google Cloud SDK, API, and Terraform, download the following resource:

{{< copyable "shell-regular" >}}

```bash
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator/deploy/gcp
```

### Configure Cloud SDK

After installing Google Cloud SDK, run `gcloud init` to [perform initial setup tasks](https://cloud.google.com/sdk/docs/initializing).

### Configure APIs

If the GCP project that you use is a new one, make sure the following APIs are enabled:

{{< copyable "shell-regular" >}}

```bash
gcloud services enable cloudresourcemanager.googleapis.com \
cloudbilling.googleapis.com iam.googleapis.com \
compute.googleapis.com container.googleapis.com
```

### Configure Terraform

To execute the Terraform script, you need to configure the following three variables. You can configure them as prompted by Terraform, or define them in a `.tfvars` file.

* `GCP_CREDENTIALS_PATH`: Path to a valid GCP credentials file.

    - It is recommended for you to create a separate service account to be used by Terraform. See [Creating and managing service accounts](https://cloud.google.com/iam/docs/creating-managing-service-accounts) for more information. `./create-service-account.sh` will create such a service account with minimal permissions.
    - See [Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for information on creating service account keys. The steps in the script below detail how to do this using a script provided in the `deploy/gcp` directory, alternatively if creating the service account and key yourself, choose `JSON` key type during creation. The downloaded `JSON` file that contains the private key is the credentials file you need.

* `GCP_REGION`: The Region in which to create the resources, for example: `us-west1`.
* `GCP_PROJECT`: The GCP project in which everything will be created.

To configure Terraform with the three variables above, perform the following steps:

1. Replace the `GCP_REGION` with your GCP Region.

    {{< copyable "shell-regular" >}}

    ```bash
    echo GCP_REGION=\"us-west1\" >> terraform.tfvars
    ```

2. Replace the `GCP_PROJECT` with your GCP project name. Make sure you are connected to the correct project.

    {{< copyable "shell-regular" >}}

    ```bash
    echo "GCP_PROJECT=\"$(gcloud config get-value project)\"" >> terraform.tfvars
    ```

3. Initialize Terraform.

    {{< copyable "shell-regular" >}}

    ```bash
    terraform init
    ```

4. Create a service account for Terraform with restricted permissions and set the credentials path.

    {{< copyable "shell-regular" >}}

    ```bash
    ./create-service-account.sh
    ```

Terraform automatically loads and populates variables from the files matching `terraform.tfvars` or `*.auto.tfvars`. For more information, see the [Terraform documentation](https://learn.hashicorp.com/terraform/getting-started/variables.html). The steps above will populate `terraform.tfvars` with `GCP_REGION` and `GCP_PROJECT`, and `credentials.auto.tfvars` with `GCP_CREDENTIALS_PATH`.

## Deploy a TiDB cluster

This section describes how to deploy a TiDB cluster.

1. Decide on instance types.

    - If you just want to get a feel for a TiDB deployment and lower your cost, use the small settings:

        {{< copyable "shell-regular" >}}

        ```bash
        cat small.tfvars >> terraform.tfvars
        ```

    - If you want to benchmark a production deployment, use the production settings:

        {{< copyable "shell-regular" >}}

        ```bash
        cat prod.tfvars >> terraform.tfvars
        ```

        The `prod.tfvars` setup creates a new VPC, two subnetworks, and an f1-micro instance as a bastion machine. This setup is created with the following instance types as worker nodes:

        * 3 n1-standard-4 instances for PD
        * 3 n1-highmem-8 instances for TiKV
        * 3 n1-standard-16 instances for TiDB
        * 3 n1-standard-2 instances for monitor

        The production setup, as listed above, requires at least 91 CPUs which exceed the default CPU quota of a GCP project. To increase your project's quota, follow these [instructions](https://cloud.google.com/compute/quotas). You need more CPUs if you need to scale out.

    > **Note:**
    >
    > The number of worker nodes created depends on the number of Availability Zones in the specified Region. Most Regions have 3 zones, but `us-central1` has 4 zones. See [Regions and Zones](https://cloud.google.com/compute/docs/regions-zones/) for more information and see the [Customize](#customize) section on how to customize node pools in a regional cluster.

2. Execute the script to deploy the TiDB cluster.

    {{< copyable "shell-regular" >}}

    ```bash
    terraform apply
    ```

    > **Note:**
    >
    > If you have not set the three variables above ahead of time, you might be prompted to set them when you run `terraform apply`. See [Configure Terraform](#configure-terraform) for details.

    It might take 10 minutes or more to finish the process. A successful deployment gives the output like:

    ```
    Apply complete! Resources: 23 added, 0 changed, 0 destroyed.

    Outputs:

    how_to_connect_to_default_cluster_tidb_from_bastion = mysql -h 172.31.252.20 -P 4000 -u root
    how_to_ssh_to_bastion = gcloud compute ssh tidb-cluster-bastion --zone us-west1-b
    how_to_set_reclaim_policy_of_pv_for_default_tidb_cluster_to_delete = kubectl --kubeconfig /.../credentials/kubeconfig_tidb-cluster get pvc -n tidb-cluster -o jsonpath='{.items[*].spec.volumeName}'|fmt -1 | xargs -I {} kubectl --kubeconfig /.../credentials/kubeconfig_tidb-cluster patch pv {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
    kubeconfig_file = ./credentials/kubeconfig_tidb-cluster
    monitor_lb_ip = 35.227.134.146
    monitor_port = 3000
    region = us-west1
    tidb_version = v3.0.1
    ```

## Access the TiDB database

After `terraform apply` is successful executed, perform the following steps to access the TiDB cluster. Replace the `<>` section with the output of running `terraform apply` above.

1. Connect to the bastion machine by using `ssh`.

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute ssh <gke-cluster-name>-bastion --zone <zone>
    ```

2. Access the TiDB cluster via a MySQL client. (Replace the `<>` parts with values from the output):

    {{< copyable "shell-regular" >}}

    ```bash
    mysql -h <tidb_ilb_ip> -P 4000 -u root
    ```

    > **Note:**
    >
    > You need to install the MySQL client before you connect to TiDB via MySQL.

## Interact with the GKE cluster

You can interact with the GKE cluster by using `kubectl` and `helm` with the `credentials/kubeconfig_<gke_cluster_name>` kubeconfig file in the following two ways.

> **Note:**
>
> The default `gke_cluster_name` is `tidb-cluster`, which can be modified by changing `gke_name` in the `variables.tf` file.

- Specify the `--kubeconfig` option:

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl --kubeconfig credentials/kubeconfig_<gke_cluster_name> get po -n <tidb_cluster_name>
    ```

    > **Note:**
    >
    > The `--kubeconfig` option used by the following command requires Helm 2.10.0 or later versions.

    {{< copyable "shell-regular" >}}

    ```bash
    helm --kubeconfig credentials/kubeconfig_<gke_cluster_name> ls
    ```

- Set the `KUBECONFIG` environment variable:

    {{< copyable "shell-regular" >}}

    ```bash
    export KUBECONFIG=$PWD/credentials/kubeconfig_<gke_cluster_name>
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl get po -n <tidb_cluster_name>
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    helm ls
    ```

## Upgrade the TiDB cluster

To upgrade the TiDB cluster, perform the following steps:

1. Modify the `tidb_version` variable to a higher version in the `variables.tf` file.
2. Run `terraform apply`.

For example, to upgrade the cluster to the 3.0.0-rc.2 version, modify the `tidb_version` to `v3.0.0-rc.2`:

```
variable "tidb_version" {
  description = "TiDB version"
  default     = "v3.0.0-rc.2"
}
```

The upgrading does not finish immediately. You can run `kubectl --kubeconfig credentials/kubeconfig_<gke_cluster_name> get po -n tidb --watch` to verify that all pods are in `Running` state. Then you can [access the database](#access-the-tidb-database) and use `tidb_version()` to see whether the cluster has been upgraded successfully:

{{< copyable "sql" >}}

```sql
select tidb_version();
```

```
*************************** 1. row ***************************
tidb_version(): Release Version: v3.0.0-rc.2
Git Commit Hash: 06f3f63d5a87e7f0436c0618cf524fea7172eb93
Git Branch: HEAD
UTC Build Time: 2019-05-28 12:48:52
GoVersion: go version go1.12 linux/amd64
Race Enabled: false
TiKV Min Version: 2.1.0-alpha.1-ff3dd160846b7d1aed9079c389fc188f7f5ea13e
Check Table Before Drop: false
1 row in set (0.001 sec)
```

## Manage multiple TiDB clusters

An instance of a `tidb-cluster` module corresponds to a TiDB cluster in the GKE cluster. To add a new TiDB cluster, perform the following steps:

1. Edit the `tidbclusters.tf` file and add a `tidb-cluster` module.

    For example:

    {{< copyable "" >}}

    ```hcl
    module "example-tidb-cluster" {
    providers = {
        helm = "helm.gke"
    }
    source                     = "../modules/gcp/tidb-cluster"
    cluster_id                 = module.tidb-operator.cluster_id
    tidb_operator_id           = module.tidb-operator.tidb_operator_id
    gcp_project                = var.GCP_PROJECT
    gke_cluster_location       = local.location
    gke_cluster_name           = <gke-cluster-name>
    cluster_name               = <example-tidb-cluster>
    cluster_version            = "v3.0.1"
    kubeconfig_path            = local.kubeconfig
    tidb_cluster_chart_version = "v1.0.0"
    pd_instance_type           = "n1-standard-1"
    tikv_instance_type         = "n1-standard-4"
    tidb_instance_type         = "n1-standard-2"
    monitor_instance_type      = "n1-standard-1"
    pd_node_count              = 1
    tikv_node_count            = 2
    tidb_node_count            = 1
    monitor_node_count         = 1
    }
    ```

    > **Note:**
    >
    > - `cluster_name` must be unique for each cluster.
    > - The total number of nodes actually created for each component is equal to the number of nodes in the configuration file multiplied by the number of Availability Zones in the Region.

    You can use `kubectl` to get the addresses for the TiDB cluster created and its monitoring service. If you want the Terraform script to print this information, add an `output` section in `outputs.tf` as follows:

    {{< copyable "" >}}

    ```hcl
    output "how_to_connect_to_example_tidb_cluster_from_bastion" {
    value = module.example-tidb-cluster.how_to_connect_to_tidb_from_bastion
    }
    ```

    This above configuration enables this script to print out the exact command used to connect to the TiDB cluster.

2. After you finish modification, execute `terraform init` and `terraform apply` to create the cluster.

## Scale the TiDB cluster

To scale the TiDB cluster, perform the following steps:

1. Modify the `tikv_count` or `tidb_count` variable in the `variables.tf` file to your desired count.
2. Run `terraform apply`.

> **Warning:**
>
> Currently, scaling in is not supported because it cannot be determined which node will be removed. Scaling in by modifying `tikv_count` can lead to data loss.

Scaling out needs a few minutes to complete, you can watch the scaling-out process by running the following command:

```bash
kubectl --kubeconfig credentials/kubeconfig_<gke_cluster_name> get po -n <tidb_cluster_name> --watch
```

For example, to scale out the cluster, you can modify the number of TiDB instances (`tidb_count`) from 1 to 2:

```hcl
variable "tidb_count" {
  description = "Number of TiDB nodes per availability zone"
  default     = 2
}
```

> **Note:**
>
> Incrementing the node count creates a node per GCP Availability Zone.

## Customize

While you can change the default values in the `variables.tf` file, such as the cluster name or image version, it is recommended that you specify values in `terraform.tfvars` or another file of your choice.

### Customize GCP resources

In GCP, you can attach a local SSD to any instance type that is `n1-standard-1` or greater, which provides good customizability.

### Customize TiDB parameters

The Terraform scripts provide proper default settings for the TiDB cluster in GKE. You can also specify `override_values` or `override_values_file` variables in the `tidbclusters.tf` file for each TiDB cluster. If both variables are configured, then `override_values` is enabled and overrides the default settings. For example:

{{< copyable "" >}}

```
override_values = <<EOF
discovery:
  image: pingcap/tidb-operator:v1.0.1
  imagePullPolicy: IfNotPresent
  resources:
    limits:
      cpu: 250m
      memory: 150Mi
    requests:
      cpu: 30m
      memory: 30Mi
EOF
```

{{< copyable "" >}}

```
override_values_file = "./test-cluster.yaml"
```

By default, the cluster uses `values/default.yaml` in the `deploy/modules/gcp/tidb-cluster` module as the overriding values file.

In GKE, some configuration items are not customizable in `values.yaml`, such as the cluster version, the number of replicas, `NodeSelector`, and `Tolerations`. `NodeSelector` and `Tolerations` are controlled by Terraform to ensure consistency between the infrastructure and TiDB clusters.

To customize the cluster version and the number of replicas, directly modify arguments of the `tidb-cluster` module in the `clusters.tf` file.

> **Note:**
>
> It is not recommended to include the following configurations (default configurations of the `tidb-cluster` module) in the customized `values.yaml`.

```
pd:
  storageClassName: pd-ssd
tikv:
  stroageClassName: local-storage
 tidb:
  service:
    type: LoadBalancer
    annotations:
      cloud.google.com/load-balancer-type: "Internal"
  separateSlowLog: true
monitor:
  storageClassName: pd-ssd
  persistent: true
  grafana:
    config:
      GF_AUTH_ANONYMOUS_ENABLED: "true"
    service:
      type: LoadBalancer
```

### Customize TiDB Operator

You can customize TiDB Operator by specifying overriding values through the `operator_helm_values` variable or specifying an overriding values file through the `operator_helm_values_file` variable. If both variables are configured, then `operator_helm_values` will be enabled and its value will be passed into the `tidb-cluster` module.

{{< copyable "" >}}

```
operator_helm_values = <<EOF
controllerManager:
  resources:
    limits:
      cpu: 250m
      memory: 150Mi
    requests:
      cpu: 30m
      memory: 30Mi
EOF
```

{{< copyable "" >}}

```
operator_helm_values_file = "./test-operator.yaml"
```

### Customize logging

GKE uses Fluentd as its default log collector, which then forwards logs to Stackdriver. The Fluentd process can be quite resource hungry and consume a non-trivial share of CPU and RAM.
Fluent Bit is a more performant and less resource intensive alternative. It is recommended to use Fluent Bit over Fluentd for a production set up. See [this repository](https://github.com/pingcap/k8s-fluent-bit-stackdriver) for an example of how to set up Fluent Bit on a GKE cluster.

### Customize node pools

The cluster is created as a regional, as opposed to a zonal cluster. This means that GKE replicates node pools to each Availability Zone. This is desired to maintain high availability, however, for the monitoring services, like Grafana, this is potentially unnecessary. It is possible to manually remove nodes if desired via `gcloud`.

> **Note:**
>
> GKE node pools are managed instance groups, so a node deleted by `gcloud compute instances delete` will be automatically recreated and added back to the cluster.

Suppose that you need to delete a node from the monitor pool. You can perform the following steps:

1. Get the managed instance group and the Available Zone.

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed list | grep monitor
    ```

    The output is something like this:

    ```
    gke-tidb-monitor-pool-08578e18-grp  us-west1-b  zone   gke-tidb-monitor-pool-08578e18  0     0            gke-tidb-monitor-pool-08578e18  no
    gke-tidb-monitor-pool-7e31100f-grp  us-west1-c  zone   gke-tidb-monitor-pool-7e31100f  1     1            gke-tidb-monitor-pool-7e31100f  no
    gke-tidb-monitor-pool-78a961e5-grp  us-west1-a  zone   gke-tidb-monitor-pool-78a961e5  1     1            gke-tidb-monitor-pool-78a961e5  no
    ```

    The first column is the name of the managed instance group, and the second column is the Available Zone where it is created.

2. Get the name of the instance in that instance group.

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed list-instances <the-name-of-the-managed-instance-group> --zone <zone>
    ```

    For example:

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed list-instances gke-tidb-monitor-pool-08578e18-grp --zone us-west1-b
    ```

    The output is something like this:

    ```
    NAME                                       ZONE        STATUS   ACTION  INSTANCE_TEMPLATE                     VERSION_NAME  LAST_ERROR
    gke-tidb-monitor-pool-08578e18-c7vd  us-west1-b  RUNNING  NONE    gke-tidb-monitor-pool-08578e18
    ```

3. Delete the instance by specifying the name of the managed instance group and the name of the instance.

    For example,

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed delete-instances gke-tidb-monitor-pool-08578e18-grp --instances=gke-tidb-monitor-pool-08578e18-c7vd --zone us-west1-b
    ```

## Destroy a TiDB cluster

When you are done, the infrastructure can be torn down by running the following command:

{{< copyable "shell-regular" >}}

```bash
terraform destroy
```

> **Note:**
>
> When `terraform destroy` is running, an error with the following message might occur: `Error reading Container Cluster "tidb": Cluster "tidb" has status "RECONCILING" with message""`. This happens when GCP is upgrading the Kubernetes master node, which it does automatically at times. While this is happening, it is not possible to delete the cluster. When it is done, run `terraform destroy` again.

### Delete disks after use

If you no longer need the data and would like to delete the disks in use, you can choose one of the following two ways:

- Manual deletion: do this either in Google Cloud Console or using the `gcloud` command-line tool.

- Setting the Kubernetes persistent volume reclaiming policy to `Delete` prior to executing `terraform destroy`: Do this by running the following `kubectl` command before `terraform destroy`.

    ```bash
    kubectl --kubeconfig /path/to/kubeconfig/file get pvc -n namespace-of-tidb-cluster -o jsonpath='{.items[*].spec.volumeName}'|fmt -1 | xargs -I {} kubectl --kubeconfig /path/to/kubeconfig/file patch pv {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
    ```

    This command gets the persistent volume claims (PVCs) in the TiDB cluster namespace and sets the reclaiming policy of the persistent volumes to `Delete`. When the PVCs are deleted during `terraform destroy` execution, the disks are deleted as well.

    The following `change-pv-reclaimpolicy.sh` script simplifies the above process in the `deploy/gcp` directory comparing to the root directory of the repository.

    ```bash
    ./change-pv-reclaimpolicy.sh /path/to/kubeconfig/file tidb-cluster-namespace
    ```

## Manage multiple Kubernetes clusters

This section describes the best practices for managing multiple Kubernetes clusters, each with one or more TiDB clusters installed.

The Terraform module in TiDB typically combines the following sub-modules:

- `tidb-operator`: provisions the [Kubernetes Control Plane](https://kubernetes.io/docs/concepts/#kubernetes-control-plane) and TiDB Operator for TiDB clusters
- `tidb-cluster`: creates the resource pool in the target Kubernetes cluster and deploys the TiDB cluster
- A `vpc` module, a `bastion` module, and a `project-credentials` module: dedicated to TiDB clusters on GKE

The best practices for managing multiple Kubernetes clusters are as follows:

- Creating a new directory for each of your Kubernetes clusters.
- Combining the above modules according to your needs via Terraform scripts.

If you use the best practices, the Terraform states among clusters do not interfere with each other, and it is convenient to manage multiple Kubernetes clusters. Here's an example (assume you are in the project root directory):

{{< copyable "shell-regular" >}}

```shell
mkdir -p deploy/gcp-staging &&
vim deploy/gccp-staging/main.tf
```

The content of `deploy/gcp-staging/main.tf` could be:

```hcl
provider "google" {
  credentials = file(var.GCP_CREDENTIALS_PATH)
  region      = var.GCP_REGION
  project     = var.GCP_PROJECT
}

// required for taints on node pools
provider "google-beta" {
  credentials = file(var.GCP_CREDENTIALS_PATH)
  region      = var.GCP_REGION
  project     = var.GCP_PROJECT
}

locals {
  gke_name        = "another-gke-name"
  credential_path = "${path.cwd}/credentials"
  kubeconfig      = "${local.credential_path}/kubeconfig_${var.gke_name}"
}


module "project-credentials" {
  source = "../modules/gcp/project-credentials"

  path = local.credential_path
}

module "vpc" {
  source              = "../modules/gcp/vpc"
  create_vpc          = true
  gcp_project         = var.GCP_PROJECT
  gcp_region          = var.GCP_REGION
  vpc_name            = "${locals.gke_name}-vpc-network"
  private_subnet_name = "${locals.gke_name}-private-subnet"
  public_subnet_name  = "${locals.gke_name}-public-subnet"
}

module "tidb-operator" {
  source                = "../modules/gcp/tidb-operator"
  gke_name              = locals.gke_name
  vpc_name              = module.vpc.vpc_name
  subnetwork_name       = module.vpc.private_subnetwork_name
  gcp_project           = var.GCP_PROJECT
  gcp_region            = var.GCP_REGION
  kubeconfig_path       = local.kubeconfig
  tidb_operator_version = "v1.0.0"
}

module "bastion" {
  source             = "../modules/gcp/bastion"
  vpc_name           = module.vpc.vpc_name
  public_subnet_name = module.vpc.public_subnetwork_name
  gcp_project        = var.GCP_PROJECT
  bastion_name       = "${locals.gke_name}-tidb-bastion"
}

# HACK: enforces Helm to depend on the GKE cluster
data "local_file" "kubeconfig" {
  depends_on = [module.tidb-operator.cluster_id]
  filename   = module.tidb-operator.kubeconfig_path
}
resource "local_file" "kubeconfig" {
  depends_on = [module.tidb-operator.cluster_id]
  content    = data.local_file.kubeconfig.content
  filename   = module.tidb-operator.kubeconfig_path
}

provider "helm" {
  alias          = "gke"
  insecure       = true
  install_tiller = false
  kubernetes {
    config_path = local_file.kubeconfig.filename
  }
}
module "tidb-cluster-a" {
  providers = {
    helm = "helm.gke"
  }
  source                     = "../modules/gcp/tidb-cluster"
  gcp_project                = var.GCP_PROJECT
  gke_cluster_location       = var.GCP_REGION
  gke_cluster_name           = locals.gke_name
  cluster_name               = "tidb-cluster-a"
  cluster_version            = "v3.0.1"
  kubeconfig_path            = module.tidb-operator.kubeconfig_path
  tidb_cluster_chart_version = "v1.0.0"
  pd_instance_type           = "n1-standard-1"
  tikv_instance_type         = "n1-standard-4"
  tidb_instance_type         = "n1-standard-2"
  monitor_instance_type      = "n1-standard-1"
}

module "tidb-cluster-b" {
  providers = {
    helm = "helm.gke"
  }
  source                     = "../modules/gcp/tidb-cluster"
  gcp_project                = var.GCP_PROJECT
  gke_cluster_location       = var.GCP_REGION
  gke_cluster_name           = locals.gke_name
  cluster_name               = "tidb-cluster-b"
  cluster_version            = "v3.0.1"
  kubeconfig_path            = module.tidb-operator.kubeconfig_path
  tidb_cluster_chart_version = "v1.0.0"
  pd_instance_type           = "n1-standard-1"
  tikv_instance_type         = "n1-standard-4"
  tidb_instance_type         = "n1-standard-2"
  monitor_instance_type      = "n1-standard-1"
}

output "how_to_ssh_to_bastion" {
  value= module.bastion.how_to_ssh_to_bastion
}

output "connect_to_tidb_cluster_a_from_bastion" {
  value = module.tidb-cluster-a.how_to_connect_to_default_cluster_tidb_from_bastion
}

output "connect_to_tidb_cluster_b_from_bastion" {
  value = module.tidb-cluster-b.how_to_connect_to_default_cluster_tidb_from_bastion
}

```

As shown in the code above, you can omit several parameters in each of the module calls because there are reasonable defaults, and it is easy to customize the configuration. For example, just delete the bastion module call if you do not need it.

To customize a field, use one of the following two methods:

- Modify the parameter configuration of `module` in the `*.tf` file directly.
- Refer to the `variables.tf` file of each module for all the modifiable parameters and set custom values in `terraform.tfvars`.

> **Note:**
>
> * When creating a new directory, pay attention to its relative path to Terraform modules, which affects the `source` parameter during module calls.
> * If you want to use these modules outside the tidb-operator project, make sure you copy the whole `modules` directory and keep the relative path of each module inside the directory unchanged.
> * Due to limitation [hashicorp/terraform#2430](https://github.com/hashicorp/terraform/issues/2430#issuecomment-370685911) of Terraform, the `# HACK: enforces Helm to depend on the GKE cluster` section is added in the above example to deal with the Helm provider. If you write your own `tf` file, you need to include this section.

If you are unwilling to write Terraform code, you can also copy the `deploy/gcp` directory to create new Kubernetes clusters. But note that do not copy a directory that you have already run `terraform apply` against. In this case, it is recommended that you re-clone the tidb-operator repository before copying the directory.
