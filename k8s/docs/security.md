# 🔐 Security – Projet Final Kubernetes

## 🎯 Objectif
Documenter les mesures de sécurité indispensables du projet :
- gestion des secrets,
- sécurisation des images,
- ressources,
- isolation réseau,
- bonnes pratiques CI/CD.

---

# 1️⃣ Secrets & Données sensibles

## 🔹 Stockage des secrets
- Aucun mot de passe n’est présent en clair dans le dépôt Git.
- Le mot de passe PostgreSQL est créé via :

```sh
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_PASSWORD="xxxx" \
  -n projet-final
````

* Le Secret est nommé `postgres-secret`.

## 🔹 Informations non sensibles

Stockées dans `ConfigMap` :

* nom DB,
* host DB,
* port DB,
* user DB.

---

# 2️⃣ Sécurité des images

### 🔹 Backend

* Basée sur `python:3.12-slim` (slim = attaque de surface réduite)
* Utilisateur non-root :

```dockerfile
RUN useradd -m appuser
USER appuser
```

### 🔹 Front

* Image `nginx:alpine` (distribution minimaliste)
* Ports 80 seulement, pas de modules dynamiques.

---

# 3️⃣ Sécurité Kubernetes

### 🔹 Présence des probes

Garantit que Kubernetes élimine automatiquement les pods défaillants :

Backend :

```yaml
readinessProbe:
  httpGet: { path: "/health", port: 8000 }
```

Front :

```yaml
livenessProbe:
  httpGet: { path: "/", port: 80 }
```

### 🔹 Ressources (anti DoS)

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

→ Empêche un pod de consommer toute la machine.

### 🔹 Isolation réseau

* Services internes en **ClusterIP** (non accessibles depuis l’extérieur)
* Seul l’Ingress expose l’application

---

# 4️⃣ Sécurité CI/CD

### 🔹 Secrets GitHub

* Token Docker Hub dans `DOCKERHUB_TOKEN`
* Username dans `DOCKERHUB_USERNAME`
* kubeconfig dans `KUBE_CONFIG`

### 🔹 Actions utilisées

* `docker/build-push-action` (scan des metadata)
* `actions/checkout`
* `actions/setup-python`

### 🔹 Bonnes pratiques respectées

* Aucune clé dans le repository
* Pas de push d’image sans test
* Pas de permission superflue

---

# ✔️ 5. Conclusion

Le projet respecte les exigences de sécurité du sujet :
gestion correcte des secrets, exécution non-root, limites de ressources, isolation réseau, CI/CD sécurisé, et images minimales.
Ces mesures garantissent un déploiement robuste, cohérent et sûr en environnement Kubernetes.