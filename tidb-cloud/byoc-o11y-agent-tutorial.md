This document explains how to quickly deploy the O11y Agent to collect Metrics/Logs/Diagnosis data and push them to the O11y backend for viewing on the Clinic page.

The basic deployment steps are:

1. Prepare a basic Kubernetes cluster with TiDB already deployed.
2. Create cloud resources required by the O11y Agent.
3. Create the O11y backend cluster.
4. Deploy the O11y Agent Operator.
5. Deploy the O11y Agent.
6. Verify O11y data.
7. Maintain the O11y Agent.

# Step 1: Prepare a Kubernetes Cluster

If you already have a Kubernetes cluster with TiDB deployed, you can skip this section.

If you need to create a Kubernetes + TiDB cluster from scratch, please refer to:

- [Deploy TiDB Cluster on AWS EKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks/)
- [Deploy TiDB Cluster on Google Cloud GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke/)
- [Deploy TiDB Cluster on Azure AKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-azure-aks/)

Note: Since O11y relies on cloud provider features like IAM and PrivateLink, it cannot work properly on locally created test Kubernetes clusters. For example, O11y is not suitable for Kubernetes + TiDB clusters created following this tutorial: [Quick Start with TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/).

# Step 2: Create Required Cloud Resources for O11y Agent

O11y Agent requires the following two types of cloud resources to ensure secure data transmission and permission management:

1. **IAM Role**: Provides credentials for the O11y Agent running in Kubernetes Pods, authorizing it to write monitoring data to AWS services (e.g., S3) on the O11y side.
2. **Private Link**: Establishes a private connection with the O11y backend service to avoid transmitting monitoring data over public networks.

Additionally, as an optional step, you can create a dedicated Kubernetes node group for O11y Agent to isolate it from other Pods.

## IAM Role

### AWS

#### Prerequisites

Ensure your EKS cluster has IAM OIDC identity provider enabled. If not, please refer to the [AWS official documentation](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html) to complete the configuration.

#### Steps

1. Log in to AWS IAM Console

Sign in to the [IAM Console](https://console.aws.amazon.com/iam/) using your account, ensuring it has IAM management permissions.

2. Create IAM Role

- In the left navigation pane, select **Roles** > **Create Role**.
- **Trusted entity type**: Select **Web identity**.
- **Identity provider**: From the dropdown, select the OIDC provider in the format `oidc.eks.<region>.amazonaws.com/id/<ClusterID>` (corresponding to your EKS cluster).
- **Audience**: Enter `sts.amazonaws.com` (default value, no modification needed).
- Click **Next**.
- Create IAM Role - Select Web Identity.

3. Attach AssumeRole Permission Policy

Click **Create policy (opens in new tab)**, select the **JSON** tab.

Enter the following policy content:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "*"
        }
    ]
}
```

Click **Next**, name the policy `O11yAgentAssumeRolePolicy`, and complete the creation.

Return to the role creation page, refresh and select `O11yAgentAssumeRolePolicy`, then click **Next**.

4. Set Role Name and Tags

- Enter a role name (e.g. `O11yAgentAssumeRole`)
- (Optional) Add tags (e.g. `Environment=Prod`)

Click **Create Role**.

5. Bind Kubernetes Service Account (Optional)

After creating the role, record its ARN (format: `arn:aws:iam::<ACCOUNT_ID>:role/O11yAgentAssumeRole`).

When deploying O11y Agent later, you need to specify this ARN in the Kubernetes ServiceAccount annotations. Here is an example:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: o11y-agent
  annotations:
    eks.amazonaws.com/role-arn: "arn:aws:iam::<ACCOUNT_ID>:role/O11yAgentAssumeRole"
```

This AWS IAM Role will be specified when creating the O11y backend cluster to complete the authorization of this IAM Role by the O11y backend.

For more details about creating IAM Roles in AWS Web Console, please refer to the [official documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html).

#### Steps (CLI Version)

1. Install and configure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) with administrator privileges.

2. Create AssumeRole policy

```bash
# Generate AssumeRole policy json file
cat > assume-role-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "*"
        }
    ]
}
EOF

# Create IAM policy
POLICY_ARN=$(aws iam create-policy \
  --policy-name O11yAgentAssumeRolePolicy \
  --policy-document file://assume-role-policy.json \
  --query 'Policy.Arn' \
  --output text)
```

3. Create IAM Role

```bash
# Generate trust polocy json file
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/oidc.eks.<region>.amazonaws.com/id/<CLUSTER_ID>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.<region>.amazonaws.com/id/<CLUSTER_ID>:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
EOF

# Create IAM Role
ROLE_ARN=$(aws iam create-role \
  --role-name O11yAgentAssumeRole \
  --assume-role-policy-document file://trust-policy.json \
  --query 'Role.Arn' \
  --output text)

# Attach IAM policy to IAM role
aws iam attach-role-policy \
  --role-name O11yAgentAssumeRole \
  --policy-arn $POLICY_ARN
```

4. Verify IAM Configuration

```bash
# Check AssumeRolePolicyDocument
aws iam get-role --role-name O11yAgentAssumeRole --query 'Role.AssumeRolePolicyDocument'

# Check attached policies
aws iam list-attached-role-policies --role-name O11yAgentAssumeRole
```

This AWS IAM Role will be configured when creating the O11y backend cluster to grant the O11y backend access permissions for this IAM Role.

For more details about creating IAM Roles using AWS CLI, please refer to the [official documentation](https://docs.aws.amazon.com/cli/latest/reference/iam/).

### GCP

#### Steps

1. Enable Workload Identity

- Go to [GKE Console](https://console.cloud.google.com/kubernetes/)
- Select target cluster > **Details** > **Edit**
- Under **Security** section:
  - Enable **Workload Identity**
  - Set Identity namespace (default format: `<PROJECT_ID>.svc.id.goog`)
- Click **Save**

2. Create Project Service Account

- Navigate to [IAM & Admin Console](https://console.cloud.google.com/iam-admin/serviceaccounts)
- Click **Create Service Account**
- Enter name: `o11y-agent`
- Click **Create and Continue** > **Done**

3. Bind Kubernetes Service Account (Optional)

- Create ServiceAccount in GKE cluster:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
name: o11y-agent
annotations:
    iam.gke.io/gcp-service-account: "o11y-agent@<PROJECT_ID>.iam.gserviceaccount.com"
```

This GCP Service Account will be configured when creating the O11y backend cluster to authorize the O11y backend's access to this Service Account.

For more details about creating Service Accounts in GCP Web Console, please refer to the [official documentation](https://cloud.google.com/iam/docs/service-account-overview).

#### Steps (CLI Version)

1. Install and configure [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)

2. Ensure you have obtained the following information:

- **Project ID**: `<PROJECT_ID>`
- **GKE Cluster Name**: `<CLUSTER_NAME>` 
- **VPC Network Name**: `<VPC_NAME>`
- **Subnet Name**: `<SUBNET_NAME>`

3. Enable Workload Identity

```bash
# Get cluster location information (replace <REGION> or <ZONE>)
gcloud container clusters describe <CLUSTER_NAME> \
  --region <REGION> \
  --format="value(location)"

# Enable Workload Identity  
gcloud container clusters update <CLUSTER_NAME> \
  --region <REGION> \
  --workload-pool=<CLIENT_PROJECT_ID>.svc.id.goog
```

4. Create Service Account

```bash
# Create service account
gcloud iam service-accounts create o11y-agent \
  --project=<PROJECT_ID> \
  --display-name="O11y Agent SA"
```

This GCP Service Account will be configured when setting up the O11y backend cluster to grant the O11y backend access permissions for this Service Account.

For more details about creating Service Accounts using gcloud CLI, see the [official documentation](https://cloud.google.com/iam/docs/service-account-overview).

## Private Link

### AWS

#### Steps

1. Sign in to AWS Management Console

Log in to the [VPC Console](https://console.aws.amazon.com/vpc/) using your AWS account.

2. Create an Endpoint

- In the left navigation pane, select **Endpoints** > **Create Endpoint**
- **Service category**: Choose Other endpoint services
- **Service name**: Enter the service name provided by the O11y team
- **VPC**: Select the VPC to connect to
- **Subnets**: Check at least two private subnets across different Availability Zones
- **Enable DNS name**: Keep enabled
- **Security group**: Select a security group that allows HTTP/HTTPS outbound traffic

For more details about creating Private Link in AWS Web Console, refer to the [official documentation](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html)

#### Steps (CLI Version)

1. Get Subnet ID List

```bash
SUBNET_IDS=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=<VPC_ID>" \
  --query 'Subnets[].SubnetId' \
  --output text | tr '\n' ' ')
```

2. Create Interface Endpoint

```bash
ENDPOINT_ID=$(aws ec2 create-vpc-endpoint \
  --vpc-id <VPC_ID> \
  --service-name $ENDPOINT_SERVICE \
  --vpc-endpoint-type Interface \
  --subnet-ids $SUBNET_IDS \
  --security-group-ids <SECURITY_GROUP_ID> \
  --query 'VpcEndpoint.VpcEndpointId' \
  --output text)
```

3. Wait for Endpoint to Become Available

```bash
aws ec2 wait vpc-endpoint-available --vpc-endpoint-ids $ENDPOINT_ID
```

For more details on creating Private Link using AWS CLI, see the [official documentation](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-vpc-endpoint.html).

### GCP

#### Steps

1. Access Private Service Connect

- Navigate to **Network Services** > **Private Service Connect**
- Click **CONNECTED ENDPOINTS** > **Create Endpoint**

2. Configure Endpoint Parameters

- **Endpoint name**: o11y-psc-endpoint
- **Target service**: Enter the service attachment ID provided by O11y team  
- **Network**: Select your VPC network
- **Subnet**: Choose the subnet where GKE cluster resides  
- **Auto-assign IP**: Enabled
- **Global access**: Select based on cross-region requirements

3. Configure Workload Identity

- Navigate to **Kubernetes Engine** > **Clusters**
- Select GKE cluster, enable **Workload Identity**
- Record **Workload Pool ID** (format: <PROJECT_ID>.svc.id.goog)

For more details about creating Private Service Connect in GCP Web Console, refer to the [official documentation](https://cloud.google.com/vpc/docs/private-service-connect).

#### Steps (CLI Version)

1. Create Private Service Connect Endpoint

```bash
# Reserve internal IP
gcloud compute addresses create psc-ip \
  --region=${REGION} \
  --subnet=${CLIENT_SUBNET} \
  --purpose=PRIVATE_SERVICE_CONNECT

# Create PSC endpoint
gcloud compute forwarding-rules create psc-endpoint \
  --region=${REGION} \
  --load-balancing-scheme=EXTERNAL \
  --address=psc-ip \
  --target-service-attachment=projects/${O11Y_PROJECT}/regions/${REGION}/serviceAttachments/${SA_ID} \
  --allow-psc-global-access
```

2. Configure Workload Identity

```bash
# Enable Workload Identity
gcloud container clusters update ${CLUSTER_NAME} \
  --region=${REGION} \
  --workload-pool=${CLIENT_PROJECT}.svc.id.goog
```

For more details about creating Private Service Connect using GCP CLI, refer to the [official documentation](https://cloud.google.com/vpc/docs/private-service-connect).

## Node Group (Optional)

### AWS

#### Steps

1. Access EKS Console

- Sign in to [AWS Management Console](https://console.aws.amazon.com/)
- Navigate to **Elastic Kubernetes Service** > **Clusters** and select target cluster
- Under Compute tab, click **Add Node Group**

2. Configure Basic Node Group Parameters

- **Node group name**: o11y-agent-nodes  
- **Node IAM role**: Select existing role or create new (must include EKS worker node policies)
- **Instance type**: c5.xlarge (adjust based on monitoring workload)
- **Scaling policy**: Fixed count of 2 instances (minimum 2 nodes recommended for HA)

3. Configure Advanced Settings

Add node labels:

```
workload=o11y-agent
component=observability
```

Add node taints:

```
dedicated=o11y-agent:NoSchedule
```

4. Complete Creation

- Review all configurations and click **Create**
- Wait for node status to change to **Active** (approximately 5-10 minutes)

5. Configure O11y Agent Scheduling Policy (Example)

Use the following configuration to schedule O11y Agent on the dedicated node group:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "o11y-agent"
        effect: "NoSchedule"
      nodeSelector:
        workload: "o11y-agent"
```

For additional details about creating Node Groups in AWS Web Console, see the [official documentation](https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html).

#### Steps (CLI Version)

1. Prepare Node Group Configuration

```bash
# Define environment variables
CLUSTER_NAME="o11y-cluster"
NODEGROUP_NAME="o11y-agent-nodes"
REGION="us-west-2"
SUBNETS="subnet-0123456789abcdef0,subnet-0fedcba9876543210"
INSTANCE_TYPE="c5.xlarge"
MIN_SIZE=2
MAX_SIZE=5
DESIRED_SIZE=2

# Generate node role ARN (requires pre-created IAM role)
NODE_ROLE_ARN=$(aws iam get-role --role-name AmazonEKSNodeRole --query 'Role.Arn' --output text)
```

2. Create Node Group with Labels and Taints

```bash
aws eks create-nodegroup \
  --cluster-name $CLUSTER_NAME \
  --nodegroup-name $NODEGROUP_NAME \
  --subnets $SUBNETS \
  --node-role $NODE_ROLE_ARN \
  --ami-type AL2_x86_64 \
  --instance-types $INSTANCE_TYPE \
  --scaling-config minSize=$MIN_SIZE,maxSize=$MAX_SIZE,desiredSize=$DESIRED_SIZE \
  --labels workload=o11y-agent,component=observability \
  --taints '[{"key":"dedicated","value":"o11y-agent","effect":"NO_SCHEDULE"}]' \
  --region $REGION
```

3. Verify Node Group Status

```bash
# Check creation status
aws eks describe-nodegroup \
  --cluster-name $CLUSTER_NAME \
  --nodegroup-name $NODEGROUP_NAME \
  --query 'nodegroup.status' \
  --region $REGION

# Wait for status to become ACTIVE (~5-10 minutes)
aws eks wait nodegroup-active \
  --cluster-name $CLUSTER_NAME \
  --nodegroup-name $NODEGROUP_NAME \
  --region $REGION
```

4. Configure O11y Agent Scheduling Policy (Example)

Use the following configuration to schedule O11y Agent on the dedicated node group:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "o11y-agent"
        effect: "NoSchedule"
      nodeSelector:
        workload: "o11y-agent"
```

For more details about creating Node Groups using AWS CLI, refer to the [official documentation](https://docs.aws.amazon.com/cli/latest/reference/eks/create-nodegroup.html).

### GCP

#### Steps

1. Access GKE Console

- Sign in to [GCP Console](https://console.cloud.google.com/)
- Navigate to **Kubernetes Engine** > **Clusters**
- Select target cluster, click **Node Pools** tab
- Click **Create Node Pool**

2. Configure Basic Parameters

- **Node pool name**: o11y-agent-pool
- **Number of nodes**: 2
- **Machine type**: e2-standard-4 (adjust based on monitoring workload)
- **Operating system**: Container-Optimized OS
- **Boot disk size**: 100 GB

3. Set Advanced Configuration

Node **Metadata** > **Labels**:

```
workload: o11y-agent
component: observability
```

Node **Taints**:

```
Key: dedicated
Value: o11y-agent
Effect: NoSchedule
```

Network Configuration:

- Select same VPC network as GKE cluster
- Enable **Use only private IP**

4. Complete Creation

- Click **Create** button
- Wait for node pool status to change to **Ready** (~5-10 minutes)

5. Configure O11y Agent Scheduling Policy (Example)

Use the following configuration to schedule O11y Agent on the dedicated node pool:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "o11y-agent"
        effect: "NoSchedule"
      nodeSelector:
        workload: "o11y-agent"
```

For additional details about creating Node Pools in GCP Web Console, refer to the [official documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/node-pools).

#### Steps (CLI Version)

1. Prepare Environment Variables

```bash
# Basic configuration
CLUSTER_NAME="o11y-cluster"
NODE_POOL_NAME="o11y-agent-pool"
ZONE="us-central1-a"
MACHINE_TYPE="e2-standard-4"
DISK_SIZE="100"
NUM_NODES=2

# Network configuration
NETWORK="default"
SUBNETWORK="default"
```

2. Create Node Pool with Labels and Taints

```bash
gcloud container node-pools create ${NODE_POOL_NAME} \
  --cluster=${CLUSTER_NAME} \
  --zone=${ZONE} \
  --machine-type=${MACHINE_TYPE} \
  --num-nodes=${NUM_NODES} \
  --disk-size=${DISK_SIZE} \
  --node-labels="workload=o11y-agent,component=observability" \
  --node-taints="dedicated=o11y-agent:NoSchedule" \
  --image-type="COS_CONTAINERD" \
  --network=${NETWORK} \
  --subnetwork=${SUBNETWORK}
```

3. Verify Node Pool Status

```bash
# Check node pool status
gcloud container node-pools describe ${NODE_POOL_NAME} \
  --cluster=${CLUSTER_NAME} \
  --zone=${ZONE} \
  --format="value(status)"

# Get node instance list
gcloud compute instances list \
  --filter="metadata.items.cluster-name=${CLUSTER_NAME} AND metadata.items.node-pool-name=${NODE_POOL_NAME}"
```

4. Configure O11y Agent Scheduling Policy (Example)

Use the following configuration to schedule O11y Agent on the dedicated node pool:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "o11y-agent"
        effect: "NoSchedule"
      nodeSelector:
        workload: "o11y-agent"
```

For more details about creating Node Pools using GCP CLI, see the [official documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/node-pools).

# Step 3: Create the O11y Backend Cluster

> Follow the Clinic UI Guide to fill required parameters and create O11y backend cluster.

# Step 4: Deploy the O11y Agent Operator

The O11y Agent consists of the Victoria Metrics Agent (VMAgent) and the Vector Agent. Since the current Vector Agent Operator is not officially supported and has low maintenance, we deploy the Vector Agent using Helm chart. Therefore, the O11y Agent Operator specifically refers to the Victoria Metrics Operator.

## Prerequisites

- Kubernetes cluster 1.20.9
- [Helm 3](https://helm.sh/docs/intro/install/)
- [kubectl 1.21+](https://kubernetes.io/docs/tasks/tools/)

## Steps

### Add VictoriaMetrics Helm Repository

To install VictoriaMetrics components, first add the VictoriaMetrics Helm repository by executing:

```bash
helm repo add vm https://victoriametrics.github.io/helm-charts/
```

Update helm repository:

```bash
helm repo update
```

You can run the following command to verify that all contents are set up correctly:

```bash
helm search repo vm/
```

The expected output would be:

```bash
NAME                            CHART VERSION   APP VERSION DESCRIPTION
vm/victoria-metrics-agent       0.7.20          v1.62.0     Victoria Metrics Agent - collects metrics from ...
vm/victoria-metrics-alert       0.3.34          v1.62.0     Victoria Metrics Alert - executes a list of giv...
vm/victoria-metrics-auth        0.2.23          1.62.0      Victoria Metrics Auth - is a simple auth proxy ...
vm/victoria-metrics-cluster     0.8.32          1.62.0      Victoria Metrics Cluster version - high-perform...
vm/victoria-metrics-k8s-stack   0.2.9           1.16.0      Kubernetes monitoring on VictoriaMetrics stack....
vm/victoria-metrics-operator    0.1.17          0.16.0      Victoria Metrics Operator
vm/victoria-metrics-single      0.7.5           1.62.0      Victoria Metrics Single version - high-performa...
```

### Install VM Operator from Helm Chart

```bash
helm install vmoperator vm/victoria-metrics-operator
```

The expected output would be:

```bash
NAME: vmoperator
LAST DEPLOYED: Thu Sep 30 17:30:30 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
victoria-metrics-operator has been installed. Check its status by running:
  kubectl --namespace default get pods -l "app.kubernetes.io/instance=vmoperator"

Get more information on https://github.com/VictoriaMetrics/helm-charts/tree/master/charts/victoria-metrics-operator.
See "Getting started guide for VM Operator" on https://docs.victoriametrics.com/guides/getting-started-with-vm-operator.html.
```

Run the following command to check if the VM Operator has started and is running:

```bash
kubectl --namespace default get pods -l "app.kubernetes.io/instance=vmoperator"
```

The expected output would be:

```bash
NAME                                                    READY   STATUS    RESTARTS   AGE
vmoperator-victoria-metrics-operator-67cff44cd6-s47n6   1/1     Running   0          77s
```

For more details on using the Victoria Metrics Operator, please refer to the [official documentation](https://docs.victoriametrics.com/guides/getting-started-with-vm-operator/)

# Step 5: Deploy the O11y Agent

As mentioned earlier, the O11y Agent consists of two types of agents: the Victoria Metrics Agent and the Vector Agent. Specifically, it can be divided into four deployment types:

- **TiDB Victoria Metrics Agent**: [Victoria Metrics Agent](https://docs.victoriametrics.com/vmagent/) for collecting TiDB Metrics, deployed once per TiDB Cluster with a Kubernetes resource of `Deployment`.
- **Kubernetes Victoria Metrics Agent**: [Victoria Metrics Agent](https://docs.victoriametrics.com/vmagent/) for collecting Kubernetes Metrics, deployed once per Kubernetes cluster with a Kubernetes resource of `Deployment`.
- **TiDB Vector Agent**: [Vector Agent](https://vector.dev/) for collecting TiDB SQL diagnostic data, deployed once per TiDB Cluster with a Kubernetes resource of `Deployment`.
- **Kubernetes Vector Agent**: [Vector Agent](https://vector.dev/) for collecting all Logs, deployed once per Node with a Kubernetes resource of `DaemonSet`.

## TiDB Victoria Metrics Agent

### Functional Description

**TiDB Victoria Metrics Agent** is specifically designed to collect monitoring metrics from TiDB clusters. Each TiDB Cluster requires one deployed instance.

### Prepare Resource File

Deploying VMAgent requires preparing a VMAgent CR resource file. The key parameters are `remoteWrite.url` and `additionalScrapeConfigs` - the former specifies where to push collected metrics data, while the latter describes how metrics should be collected.

Basic resource template:

```yaml
apiVersion: operator.victoriametrics.com/v1beta1
kind: VMAgent
metadata:
  # Recommended to distinguish by tidb naming
  name: tidb-vmagent
  namespace: monitoring
spec:
  # Version
  image:
    repository: victoriametrics/vmagent
    tag: v1.102.1  # Keep consistent with TiDB Cloud
    pullPolicy: IfNotPresent
  # Scrape interval. Recommended 15s for TiDB VMAgent
  scrapeInterval: 15s
  # Metric labels, can be added as needed
  externalLabels:
    cluster: "my-k8s-cluster"
    region: "us-west-1"
  # Remote write target - sending data to O11y backend
  remoteWrite:
    - url: <VMAGENT_REMOTE_WRITE_URL>
  # VMAgent replica count
  replicaCount: 1
  # Resource limits, adjust according to cluster size
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1024Mi"
      cpu: "500m"
  # Scrape configuration
  additionalScrapeConfigs:
    # ...
    # (Example)
    - job_name: 'node-exporter'
      static_configs:
        - targets: ['node-exporter-service.monitoring.svc:9100']
```

The `remoteWrite.url` can be obtained after creating the O11y backend cluster as mentioned earlier - simply fill in the corresponding value.

For standard TiDB clusters, we provide an `additionalScrapeConfigs` template to collect metrics from all TiDB components. Please refer to [TiDB VMAgent Config](/tidb-cloud/byoc-o11y-agent-vmagent-config-tidb.md).

### Deployment

Deploy using `kubectl` with the prepared resource file:

```bash
kubectl apply -f tidb-vmagent.yaml
```

Verify vmagent is running properly:

```bash
# Check VMAgent CR status
kubectl get vmagent -n monitoring

# Check Pod status
kubectl get pods -n monitoring -l app.kubernetes.io/name=tidb-vmagent

# Check logs
kubectl logs -n monitoring -l app.kubernetes.io/name=tidb-vmagent --tail=50
```

## Kubernetes Victoria Metrics Agent

### Functional Description

**Kubernetes Victoria Metrics Agent** is specifically designed to collect fundamental Kubernetes cluster metrics. One instance should be deployed per Kubernetes cluster.

### Prepare Resource File

Similar to the TiDB VMAgent, you need to prepare a dedicated Custom Resource (CR) definition file for the Kubernetes VMAgent.

Basic resource template:

```yaml
apiVersion: operator.victoriametrics.com/v1beta1
kind: VMAgent
metadata:
  name: k8s-vmagent
  namespace: monitoring
spec:
  # Version
  image:
    repository: victoriametrics/vmagent
    tag: v1.102.1  # Keep consistent with TiDB Cloud
    pullPolicy: IfNotPresent
  # Scrape interval. Recommended 30s for Kubernetes VMAgent
  scrapeInterval: 30s
  # Metric labels, can be added as needed
  externalLabels:
    cluster: "my-k8s-cluster"
    region: "us-west-1"
  # Remote write target - sending data to O11y backend.
  remoteWrite:
    - url: <VMAGENT_REMOTE_WRITE_URL>
  # VMAgent replica count
  replicaCount: 1
  # Resource limits, adjust according to cluster size
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1024Mi"
      cpu: "500m"
  # Scrape configuration
  additionalScrapeConfigs:
    # ...
    # (Example)
    - job_name: 'node-exporter'
      static_configs:
        - targets: ['node-exporter-service.monitoring.svc:9100']
```

The `remoteWrite.url` can be obtained after creating the O11y backend cluster as mentioned earlier - simply fill in the corresponding value.

For Kubernetes VMAgent, we provide an `additionalScrapeConfigs` template to collect metrics from all Kubernetes components. Please refer to [Kubernetes VMAgent Config](/tidb-cloud/byoc-o11y-agent-vmagent-config-k8s.md).

### Deployment

Apply the prepared resource file using `kubectl`:

```bash
kubectl apply -f k8s-vmagent.yaml
```

Verify VMAgent is running properly:

```bash
# Check VMAgent CR status
kubectl get vmagent -n monitoring

# Check Pod status
kubectl get pods -n monitoring -l app.kubernetes.io/name=k8s-vmagent

# Check logs
kubectl logs -n monitoring -l app.kubernetes.io/name=k8s-vmagent --tail=50
```

## Kubernetes Vector Agent

### Functional Description

**Kubernetes Vector Agent** is responsible for collecting Pod logs from node system disks, with one instance deployed per Kubernetes node.

### Prepare Resource File

For Kubernetes Vector Agent, we provide a Helm Values template to collect all necessary logs. Please refer to the following links for configuration:

- [Node Vector Agent for AWS](/tidb-cloud/byoc-o11y-agent-vector-config-k8s-aws.md)
- [Node Vector Agent for GCP](/tidb-cloud/byoc-o11y-agent-vector-config-k8s-gcp.md)

> Note: Please replace the variables in the `${VAR}` format in the configuration appropriately.

### Deployment

Add Vector Agent Helm repository:

```bash
helm repo add vector https://helm.vector.dev
helm repo update
```

Install Kubernetes Vector Agent:

```bash
helm install vector vector/vector \
  --namespace monitoring \
  --create-namespace \
  -f k8s-vector.yaml
```

Verify deployment:

```bash
# Check Pod status
kubectl get pods -n monitoring -l app.kubernetes.io/instance=k8s-vector

# Check logs
kubectl logs -n monitoring -l app.kubernetes.io/instance=k8s-vector --tail=50
```

## TiDB Vector Agent

### Functional Description

**TiDB Vector Agent** is responsible for collecting TiDB SQL diagnostic data, with one instance deployed per TiDB Cluster.

### Prepare Resource File

Since TiDB Vector Agent doesn't follow the conventional `DaemonSet` deployment pattern, we deploy it directly using native Kubernetes resources.

We need to prepare the following resources:

1. Reference the previously created `ServiceAccount`, which is already bound to the corresponding IAM Role:

```yaml
# tidb-vector-sa.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: o11y-agent
  annotations:
    eks.amazonaws.com/role-arn: "arn:aws:iam::<ACCOUNT_ID>:role/O11yAgentAssumeRole"
```

2. Configuration file in `ConfigMap`:

```yaml
# tidb-vector-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tidb-vector
  namespace: monitoring
data:
  config.toml: |
    ...
```

The content of `config.toml` can be referenced from [TiDB Vector Config](/tidb-cloud/byoc-o11y-agent-vector-config-tidb.md).

3. `Deployment` resource definition file:

```yaml
# tidb-vector-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  # Adjust naming according to your TiDB cluster
  name: tidb-vector
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tidb-vector
  template:
    metadata:
      labels:
        app: tidb-vector
    spec:
      serviceAccountName: o11y-agent
      containers:
      - name: vector
        image: timberio/vector:0.34.0-distroless-libc
        args: ["--config", "/etc/vector/config.toml"]
        resources:
          requests:
            cpu: "1"
            memory: 1Gi
        volumeMounts:
        - name: config
          mountPath: /etc/vector
      volumes:
      - name: config
        configMap:
          name: tidb-vector
```

### Deployment

Deploy TiDB Vector Agent:

```bash
kubectl apply -f tidb-vector-sa.yaml
kubectl apply -f tidb-vector-cm.yaml
kubectl apply -f tidb-vector-deploy.yaml
```

Verify deployment:

```bash
# Check Pod status
kubectl get pods -n monitoring -l app.kubernetes.io/instance=tidb-vector

# Check logs
kubectl logs -n monitoring -l app.kubernetes.io/instance=tidb-vector --tail=50
```

# Step 6: Verify O11y data

> Follow the Clinic UI Guide to browse and validate O11y data on the Clinic web console.

# Step 7: Maintain the O11y Agent

For O11y Agent maintenance operations, refer to the following docs:

- [Victoria Metrics Operator Docs](https://docs.victoriametrics.com/guides/getting-started-with-vm-operator/)
- [Kubernetes Docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Helm Docs](https://helm.sh/docs/)
