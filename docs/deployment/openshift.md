## Deploying to OpenShift

### 1. Create an OpenShift Project
```bash
oc new-project myproject
```

### 2. Define Configuration via ConfigMap
Create a `ConfigMap` to store environment variables.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: keycloak-auth-proxy-config
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
oc apply -f keycloak-auth-proxy-config.yaml
```

➡️ **For detailed environment variable setup, see**: [Configuration](../configuration/env.md)

### 3. Deploy the Reverse Proxy
Create a deployment configuration.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keycloak-auth-proxy
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
oc apply -f keycloak-auth-proxy-deployment.yaml
```

### 4. Expose the Reverse Proxy as a Service
Create a service for internal communication.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: keycloak-auth-proxy
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
oc apply -f keycloak-auth-proxy-service.yaml
```

### 5. Create an OpenShift Route
Expose the service externally using an OpenShift Route.
```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: keycloak-auth-proxy-route
spec:
  host: proxy.myproject.com
  to:
    kind: Service
    name: keycloak-auth-proxy
  port:
    targetPort: 8000
  tls:
    termination: edge
```
Apply the route:
```bash
oc apply -f keycloak-auth-proxy-route.yaml
```
Now, the reverse proxy is accessible at:
```
https://proxy.myproject.com
```