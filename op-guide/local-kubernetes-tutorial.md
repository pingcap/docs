---
title: Deploy TiDB to Kubernetes on your laptop
summary: Deploy TiDB to Kubernetes on your laptop
category: operations
---


# Deploy TiDB, a distributed MySQL compatible database, to Kubernetes on your laptop

[TiDB](www.pingcap.com) is a scale-out distributed MySQL database.
Scale-out means that when you have high usage of CPU, RAM, or disk, you just add another node to your cluster.
This is much easier to administer at scale. But we need deployment to be simple from day one. We have an [ansible based deployment]() that works in almost any environment. However, if we commit to deploying to Kubernetes, we can provide an even better experience.

For this tutorial we will deploy to a laptop Kubernetes, but this can be done on any Kubernetes cluster.


## TIDB architecture

Lets review what we will be deploying.

* TiKV
* PD
* TIDB SQL

The scale-out property of TIDB is provided by [TikV](), a distributed key-value store.
The TiKV cluster itself requires deploying a PD cluster. PD stands for placement driver, which controls where data is stored in TiKV.
MySQL compatibility is provided by a separatly deployed TIDB SQL component that works on top of TiKV.


## Kubernetes architecture

TiKV and PD maintain database state on disk, and are thus mapped to a [StatefulSet]() with a PersistentVolume Claim.
TiDB SQL is also mapped to a StateFulSet, but it does not make any PersistentVolume Claims.

These are wrapped together in a helm chart called tidb-cluster.
Additionally, we provide [tidb-operator](), a Kubernetes operator. This program monitors the status of TiDB in your Kubernetes cluster and provides a gateway to administrative duties.


### Installing a Kubernetes cluster on your laptop

First we need to run a Kubernetes cluster. minikube is the popular option for that. However, minikube only creates one Kubernetes node. To run TiDB, we need multiple Kubernetes nodes. There are a few options f
or this, but we have found a way to make DinD (Docker in Docker) work.

DinD (Docker in Docker) allows running the docker daemon inside a top-level docker container. This means the top-level container to simulate a Kubernetes node and have containers launched inside it. The kubeadm-
dind-cluster project starts multiple docker containers as a k8s nodes on a standalone machine through DinD, and then start a k8s cluster by using docker to start k8s components on these nodes.

First [install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
Next, bring up the DinD K8s. This takes a while: now is a good time to stretch and drink some water.

    wget https://cdn.rawgit.com/kubernetes-sigs/kubeadm-dind-cluster/master/fixed/dind-cluster-v1.10.sh
    chmod +x dind-cluster-v1.10.sh
    NUM_NODES=4 ./dind-cluster-v1.10.sh up
    kubectl config use-context dind

Ensure the DinD cluster works:

    kubectl get node,componentstatus
    kubectl get pod -n kube-system

If you would like, you can now [view the dashboard](http://localhost:8001/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy/) once you start the proxy with:

    kubectl proxy

Local Persistent volumes don't work right in DinD so we need to provision them manually ourselves

    cd ..
    git clone https://github.com/pingcap/tidb-operator
    # temporary directory until repo switch happens
    cd tidb-operator/new-operator
    ./manifests/local-dind/pv-hosts.sh
    kubectl apply -f manifests/local-storageclass.yaml


### Running TIDB

This process is the same regardless of how you created a Kubernetes cluster. First we launch the operator:

You need to have helm installed and tiller running.

    curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > helm.sh
    bash helm.sh
    helm init


Use helm to launch tidb-operator

    cd ..
    git clone https://github.com/pingcap/tidb-operator
    cd tidb-operator/new-operator
    helm install charts/tidb-operator --name tidb-operator --namespace=tidb-operator

Now we need to wait for the operator to come up. This can be done with:

    while kubectl get pods --namespace tidb-operator -l app=tidb-operator --no-headers | grep -v Running ; do sleep 2 ; echo "\nwaiting for tidb operator to startup" ; done

Now we can launch TiDB itself:

    kubectl apply -f manifests/crd.yaml
    helm install charts/tidb-cluster --name tidb-cluster --namespace=tidb

You now have a distributed database running on Kubernetes! It should take less than a minute for all the services to come up, but you can watch this process with:

    watch kubectl get pods --namespace tidb

We can connect to it with MySQL

    kubectl port-forward svc/demo-cluster-tidb 4000:4000 -n tidb
    mysql -u root -h 127.0.0.1 -P 4000

If you don't have MySQL installed, you can run it from a container:

    docker run --rm -it --net host jbergknoff/mysql-client mysql -u root -h 127.0.0.1 -P 4000

Similarly, you can open the [Grafana dashboard](http://localhost:3000/dashboard/db/tidb-cluster-pd) for operational metrics after forwarding the grafana port

    kubectl port-forward svc/demo-cluster-grafana 3000:3000 -n tidb
