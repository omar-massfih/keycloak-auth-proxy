## **Deploying to Kubernetes**

This section provides steps to deploy the FastAPI Reverse Proxy with Keycloak authentication in a **Kubernetes** environment.

---

### **1. Create a Namespace**
Namespaces help isolate resources.
```bash
kubectl create namespace keycloak-proxy
```

---

### **2. Create a ConfigMap**
Store environment variables in a ConfigMap.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: keycloak-auth-proxy-config
  namespace: keycloak-proxy
data:
  SERVICE_ROUTES_JSON: '{"/": "http://frontend:3000", "/api": "http://backend:8080"}'
  KEYCLOAK_ISSUER: "https://keycloak.example.com/auth/realms/myrealm"
  KEYCLOAK_CLIENT_ID: "my-client-id"
  KEYCLOAK_CLIENT_SECRET: "my-client-secret"
  FRONTEND_URL: "https://frontend.example.com"
  REDIRECT_URL: "https://frontend.example.com/callback"
```
Apply the `ConfigMap`:
```bash
kubectl apply -f keycloak-auth-proxy-config.yaml
```

➡️ **For detailed environment variable setup, see**: [Configuration](../configuration/env.md)
---

### **3. Deploy the Reverse Proxy**
Create a Kubernetes Deployment.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keycloak-auth-proxy
  namespace: keycloak-proxy
spec:
  replicas: 2
  selector:
    matchLabels:
      app: keycloak-auth-proxy
  template:
    metadata:
      labels:
        app: keycloak-auth-proxy
    spec:
      containers:
      - name: keycloak-auth-proxy
        image: your-docker-registry/keycloak-auth-proxy:latest
        ports:
          - containerPort: 8000
        envFrom:
          - configMapRef:
              name: keycloak-auth-proxy-config
```
Apply the deployment:
```bash
kubectl apply -f keycloak-auth-proxy-deployment.yaml
```

---

### **4. Expose the Reverse Proxy as a Service**
Create a service to allow communication between pods.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: keycloak-auth-proxy
  namespace: keycloak-proxy
spec:
  selector:
    app: keycloak-auth-proxy
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```
Apply the service:
```bash
kubectl apply -f keycloak-auth-proxy-service.yaml
```

---

### **5. Expose the Reverse Proxy Using an Ingress**
Use an **Ingress resource** to expose the proxy externally.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: keycloak-auth-proxy-ingress
  namespace: keycloak-proxy
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - proxy.myproject.com
    secretName: keycloak-proxy-tls
  rules:
  - host: proxy.myproject.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: keycloak-auth-proxy
            port:
              number: 80
```
Apply the ingress:
```bash
kubectl apply -f keycloak-auth-proxy-ingress.yaml
```

Now, the reverse proxy is accessible at:
```
https://proxy.myproject.com
```
