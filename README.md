# ECK

ECK (Elastic Cloud on Kubernetes) encompasses the Elasticsearch operator.

## Deploy ECK

1. Create the elasticsearch namespace:

```
kubectl create namespace elasticsearch
```

2. Install ECK

```
kubectl apply -f https://download.elastic.co/downloads/eck/0.9.0/all-in-one.yaml
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
kubectl get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode
```

2. Portforward
```
kubectl port-forward service/quickstart-es-http 9200
```

3. Call the endpoint
```
curl -u "elastic:<password>" -k "https://localhost:9200"
```
