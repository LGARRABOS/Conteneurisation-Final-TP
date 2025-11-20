# 🛠️ Runbook – Déploiement, exploitation & rollback

## 🎯 Objectif
Guide opérationnel pour :
- installer,
- déployer,
- tester,
- diagnostiquer,
- rollback l’application 3-tiers.

---

# 🚀 1. Déploiement complet

## 1️⃣ Prérequis
- Docker installé
- Minikube installé
- NGINX ingress activable
- kubectl configuré
- GitHub Actions (CI/CD) fonctionnel

---

## 2️⃣ Démarrer Minikube + Ingress

```sh
minikube start
minikube addons enable ingress
```

⚠️ Sur Windows, l’ingress nécessite le mode LoadBalancer (voir section 4).

## 3️⃣ Appliquer les manifests Kubernetes

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/app-config.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/back-service.yaml
kubectl apply -f k8s/back-deployment.yaml
kubectl apply -f k8s/front-service.yaml
kubectl apply -f k8s/front-deployment.yaml
kubectl apply -f k8s/ingress.yaml

## 4️⃣ (Windows) Activer le LoadBalancer pour l’ingress

```sh
kubectl edit svc ingress-nginx-controller -n ingress-nginx
# type: NodePort → LoadBalancer
````
Puis: 
```sh
minikube tunnel
```

## 5️⃣ Ajouter l’entrée dans /etc/hosts (Windows)
```sh
127.0.0.1    projet-final.local
```