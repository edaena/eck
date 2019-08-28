# Elastic Cloud on Kubernetes - ECK

ECK (Elastic Cloud on Kubernetes) encompasses the Elasticsearch operator.

## Deploy ECK

1. Create the elasticsearch namespace:

```
kubectl create namespace elasticsearch
```

2. Install ECK

```
kubectl apply -f all-in-one.yaml
```

3. Deploy Elasticsearch
```
kubectl -n elasticsearch apply -f elasticsearch-cluster.yaml
```

Once `elasticsearch-cluster.yaml` is deployed, ECK will create the instance


More information about deploying ECK can be found [here](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-quickstart.html#k8s-deploy-eck)

### Verify elasticsearch
You can verify the deployment succeeded by calling the elasticsearch API.

1. Fetch the elasticsearch password

```
kubectl -n elasticsearch get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode
```

2. Portforward
```
kubectl -n elasticsearch port-forward service/quickstart-es-http 9200
```

3. Call the endpoint
```
curl -u "elastic:<password>" -k "https://localhost:9200"
```

## Deploy Portworx

1. Install Portworx

```
kubectl apply -f px-gen-spec.yml
```

2. Deploy a Portworx Storage Class

```
kubectl apply -f eck-portworx-sc.yaml
```

Once `elasticsearch-cluster.yaml` is deployed, ECK will create the volumes managed by Portworx

### Verify Portworx

You can use the `pxctl` command Portworx provides to obtain metrics on how the volumes are being used: 
1. First get the name of a Portworx pod.

> `kubectl get pods -n=kube-system -l name=portworx`

2. Now you are able to view the provisioned Portworx disks dedicated for each node. 

> `kubectl exec <portworx_pod_name> -n kube-system -- /opt/pwx/bin/pxctl status`

```
nmrose@DESKTOP-NU43M7R:/mnt/c/Users/naros/Desktop/Microsoft/fy20/stateful/elasticsearch/portworx/eck$ kubectl exec portworx-88gn7 -n kube-system -- /opt/pwx/bin/pxctl status
Status: PX is operational
License: Trial (expires in 31 days)
Node ID: 03f5b844-3849-4157-94b0-1acef392c1d4
        IP: 10.240.0.6
        Local Storage Pool: 1 pool
        POOL    IO_PRIORITY     RAID_LEVEL      USABLE  USED    STATUS  ZONE    REGION
        0       LOW             raid0           150 GiB 9.6 GiB Online  1       westus2
        Local Storage Devices: 1 device
        Device  Path            Media Type              Size            Last-Scan
        0:1     /dev/sdc        STORAGE_MEDIUM_MAGNETIC 150 GiB         28 Aug 19 20:02 UTC
        total                   -                       150 GiB
Cluster Summary
        Cluster ID: pxcluster-00bede14-da12-4df8-88bf-5f73b3f2577e
        Cluster UUID: 544286a5-2dfb-4fee-b5d3-46392172c997
        Scheduler: kubernetes
        Nodes: 3 node(s) with storage (3 online)
        IP              ID                                      SchedulerNodeName               StorageNode     Used   Capacity                                                                                                                       Status   StorageStatus   Version         Kernel                  OS
        10.240.0.4      fc6a0b8e-74c7-4726-8211-418b9308e6ca    aks-agentpool-38370153-1        Yes             9.6 GiB                                                                                                                               150 GiB          Online  Up              2.1.2.0-21409c7 4.15.0-1055-azure       Ubuntu 16.04.6 LTS
        10.240.0.5      0ee1445b-f5c4-446e-a4c1-5ab0190ee8b3    aks-agentpool-38370153-0        Yes             9.6 GiB                                                                                                                               150 GiB          Online  Up              2.1.2.0-21409c7 4.15.0-1052-azure       Ubuntu 16.04.6 LTS
        10.240.0.6      03f5b844-3849-4157-94b0-1acef392c1d4    aks-agentpool-38370153-2        Yes             9.6 GiB                                                                                                                               150 GiB          Online  Up (This node)  2.1.2.0-21409c7 4.15.0-1055-azure       Ubuntu 16.04.6 LTS
Global Storage Pool
        Total Used      :  29 GiB
        Total Capacity  :  450 GiB
```

3. **Once your storage class definition is applied and you provision PVCs from your application (in this case ECK)**, next grab the Portworx volume list which will give details on the provisioned volumes deployed.

> `kubectl exec <portowrx_pod_name> -n kube-system -- /opt/pwx/bin/pxctl volume list`

```
ID                      NAME                                            SIZE    HA      SHARED  ENCRYPTED       IO_PRIORITY       STATUS                          SNAP-ENABLED
811479554253316890      pvc-073f7692-c9da-11e9-8240-7640108c780b        80 GiB  2       no      no              LOW      up - attached on 10.240.0.5      no
```

4. Now grab the volume state details for a portworx disk. 

> `kubectl exec <portworx_pod>-n kube-system -- /opt/pwx/bin/pxctl volume inspect <volume_id>`

```
Volume  :  811479554253316890
        Name                     :  pvc-073f7692-c9da-11e9-8240-7640108c780b
        Group                    :  elastic_master_vg
        Size                     :  80 GiB
        Format                   :  ext4
        HA                       :  2
        IO Priority              :  LOW
        Creation time            :  Aug 28 21:23:11 UTC 2019
        Shared                   :  no
        Status                   :  up
        State                    :  Attached: 0ee1445b-f5c4-446e-a4c1-5ab0190ee8b3 (10.240.0.5)
        Device Path              :  /dev/pxd/pxd811479554253316890
        Labels                   :  fg=false,group=elastic_master_vg,namespace=elastic-system,pvc=px-storage-elastic-operator-0,repl=2
        Reads                    :  40
        Reads MS                 :  92
        Bytes Read               :  389120
        Writes                   :  2603
        Writes MS                :  30192
        Bytes Written            :  1342476288
        IOs in progress          :  0
        Bytes used               :  4.7 MiB
        Replica sets on nodes:
                Set 0
                  Node           : 10.240.0.6 (Pool 0)
                  Node           : 10.240.0.4 (Pool 0)
        Replication Status       :  Up
        Volume consumers         :
                - Name           : elastic-operator-0 (078feed7-c9da-11e9-8240-7640108c780b) (Pod)
                  Namespace      : elastic-system
                  Running on     : aks-agentpool-38370153-0
                  Controlled by  : elastic-operator (StatefulSet)
```

## Velero
To setup and deploy Velero to the Kubernetes cluster refer to the [velero fabrikate definition](https://github.com/microsoft/fabrikate-definitions/tree/master/definitions/fabrikate-velero) instructions.

Configure the `component.yaml` file to add the backup for elasticsearch:
```
schedules:
  hourly-elasticsearch-backup:
    schedule: "0 * * * *"
    template:
    includedNamespaces:
    - "*"
    labelSelector:
        matchLabels:
        namespace: "elasticsearch"
    snapshotVolumes: true
    ttl: "720h0m0s"
```