# KubeOps Challenge
This is a proposed solution to the KubeOps challenge.

## Requirements
In order to run this solution you'll need:
- A Github account
- A Docker Hub account
- Minikube with the ingress controller. You can install it with `minikube addons enable ingress`.
- ArgoCD

You can install and run argocd on minikube, and forward the argocd port to a localhost port:
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd port-forward svc/argocd-server 8080:443
```


## Configure the environment
Follow these instructions to configure your environment.

### Docker Hub
Generate an Access Token in Account Settings -> Security

### Github
1. Fork the repository https://github.com/dvdjaco/ktx-kubeops
2. In the new repo, go to Settings -> Secrets and variables -> Actions
3. Create two new "Repository secrets", DOCKER_USERNAME and DOCKER_KEY, with the information from your Docker Hub account.
4. Go to Actions -> General
5. In the "Workflow permissions" section, select "Read and write permissions"

### ArgoCD
You can retrieve the admin password with:
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

1. Open https://localhost:8080 in your browser.
2. Log in and click on "+ NEW APP"
3. Fill in these fields:
- Application name: KubeOps
- Project Name: default
- SYNC POLICY: AUTOMATIC , and check on "SELF HEAL"
- Repository URL: The URL of your fork
- Path: helm
- Cluster URL: https://kubernetes.default.svc
- Namespace: default
- VALUES FILES: values.yaml

Click on "CREATE" and the Application will be created. In a few seconds you should see the Status as "Healthy" and "Synced".

Check the IP Address of minikube with `minikube ip`. Open the URL `http://minikube_ip:30005` and you will see the message:
```
 "Kubeops :: Hello, world! :: VERSION"
```
, showing the app version.

## Discussion
If you want to trigger the deployment of a new version of the app:
1. Make your changes to the repository. The code of the app is in the `hello_world.py` file.
2. Change the version in the `version` file.
3. Commit the changes and `git push` them.
4. The change in the `version` file will trigger the Github Action defined in `.github/workflows/cd.yaml`
5. The Action will build the Docker image using the version as the tag and push it to Docker Hub.
6. The Action will change the value of APP_VERSION in `helm/values.yaml` and commit the change.
7. ArgoCD will detect the change in the helm directory.
8. The change in the APP_VERSION affects the deployment defined in `helm/templates/deployment.yaml`
9. The update in the deployment triggers a rollout using a rolling update strategy. Since the deployment has 3 replicas, there will be no downtime.

## Improvements
This solution could be improved a lot!

### Multi environments
To deploy to different environments (e.g. PRE and PRO) we could create the PRE and PRO namespaces in kubernetes. We would have two different helm directories in our repo, one for each environment (e.g. helm_pre and helm_pro). We would change the APP_VERSION value in helm_pre for every version change, but only for specific tags in helm_pro. Then we would define two Applications in ArgoCD, each one of them configured like the one in this solution with a different source path and a different namespace.

## ArgoCD configuration
We should keep application definitions in source control instead of creating them manually.
