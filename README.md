# **Keycloak Auth Proxy**

A FastAPI-based Authentication Proxy (Auth Proxy) service that secures backend services using Keycloak authentication. It integrates with a reverse proxy (Traefik, Nginx, or Envoy) to validate requests before forwarding them to backend services. Supports dynamic routing via Kubernetes/OpenShift DNS.

## **Features**
- **Authentication enforcement** with Keycloak  
- **Dynamic request routing** via environment variables  
- **Optimized for Kubernetes/OpenShift deployment**  
- **Fully asynchronous implementation** using `httpx`  
- **Podman-ready containerization**  
- **Proper Keycloak logout flow**  


## **Installation & Local Development**

### **Prerequisites**
- Python 3.8+  
- Podman or Docker (for containerized deployment)  

### **Setup**
1. **Clone the repository**
   ```bash
   git clone https://github.com/omar-massfih/keycloak-auth-proxy.git
   cd keycloak-auth-proxy
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Copy the environment configuration file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your **Keycloak settings** and **backend service routes**.

4. **Run the application locally**
   ```bash
   uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
   ```

## **Helm Chart Deployment**
You can also deploy the Keycloak Auth Proxy using the official Helm chart:  
➡️ [keycloak-auth-proxy-chart](https://github.com/omar-massfih/keycloak-auth-proxy-chart)  
The chart allows easy configuration of image, environment variables, and routing for Kubernetes and OpenShift clusters.

## **Configuration**
Set up environment variables in `.env`.

### **Example `.env` File**
```ini
# Keycloak Configuration
KEYCLOAK_ISSUER=https://keycloak.example.com/auth/realms/myrealm
KEYCLOAK_CLIENT_ID=my-client-id
KEYCLOAK_CLIENT_SECRET=my-client-secret
KEYCLOAK_SCOPE="openid email profile"

# Service Routing
SERVICE_ROUTES_JSON={" /": "http://frontend:3000", "/api": "http://backend:8080"}

# Redirect URLs
FRONTEND_URL=https://frontend.example.com
REDIRECT_URL=https://frontend.example.com/callback

# CORS Settings
ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOW_HEADERS=Authorization,Content-Type
```


## **Documentation**
- **[Configure environment variables](https://omar-massfih.github.io/keycloak-auth-proxy/configuration/env/)**  
- **[Deploy to a container](https://omar-massfih.github.io/keycloak-auth-proxy/deployment/container/)**  
- **[Deploy to OpenShift](https://omar-massfih.github.io/keycloak-auth-proxy/deployment/openshift/)**  
- **[Deploy to Kubernetes](https://omar-massfih.github.io/keycloak-auth-proxy/deployment/kubernetes/)**  
- **[View API endpoints](https://omar-massfih.github.io/keycloak-auth-proxy/api/endpoints/)**  
- **[Contribute to the project](https://omar-massfih.github.io/keycloak-auth-proxy/contributing/)**  
- **[Read the license](https://omar-massfih.github.io/keycloak-auth-proxy/license/)**  


## **How It Works**
### **1. Request Handling**
- The reverse proxy listens on **port 8000**.
- Routes incoming requests based on the `SERVICE_ROUTES_JSON` configuration.
- Ensures authentication before forwarding requests.

### **2. Authentication Flow**
#### **User Accesses a Protected Resource**
- If **authenticated**, the request is forwarded to the appropriate backend service.
- If **not authenticated**, the user is redirected to **Keycloak for login**.

#### **Keycloak Callback (`/callback`)**
1. The user is redirected to Keycloak and logs in.
2. Keycloak sends an **authorization code** back to the proxy.
3. The proxy exchanges the code for an **access token**.
4. The **access token** is stored in an **HTTP-only cookie**.
5. The user is redirected to the frontend.

#### **Logout (`/logout`)**
1. The proxy receives a logout request.
2. It **clears session cookies** (`access_token`, `id_token`).
3. The user is redirected to **Keycloak's logout endpoint**.

### **3. Request Forwarding**
- **Authenticated requests** are forwarded to the appropriate backend service.
- Uses **asynchronous HTTP requests** (`httpx`) for efficient handling.
- Supports **multiple backend services dynamically**.

#### **Reverse Proxy (`/{full_path:path}`)**
1. Extracts the **requested path** from the request.
2. Matches the path to a backend service using `SERVICE_ROUTES_JSON`.
3. Ensures the request contains a valid **JWT access token**.
   - If valid, forwards the request to the appropriate backend.
   - If invalid or missing, redirects the user to **Keycloak login**.


## **Contributing**
PRs are welcome!  
Before submitting a PR, read the **[contribution guide](https://omar-massfih.github.io/keycloak-auth-proxy/contributing/)**.


## **License**
This project is licensed under the **MIT License**.


## **Next Steps**
- **Set up environment variables** → [Configuration Guide](https://omar-massfih.github.io/keycloak-auth-proxy/configuration/env/)  
- **Deploy the proxy on Kubernetes** → [Kubernetes Deployment](https://omar-massfih.github.io/keycloak-auth-proxy/deployment/kubernetes/)  
- **Run locally in a container** → [Container Setup](https://omar-massfih.github.io/keycloak-auth-proxy/deployment/container/)