# Customer-Ordering-System Api

A simple customer ordering system api built using Django rest framework.


## Features

  ### 1. Authentication and authorization
  - Account Creation: Users create an account by providing necessary information such as username, email, and password.
  - User Login: Upon successful login, a token is generated. This token is set as a cookie in the user's browser and can also be passed in the
    header of subsequent requests to authorize the user.
  - User Logout: When a user chooses to log out, the authorization token is revoked. This ensures that the user is no longer authenticated
    and cannot access protected resources.

  ### 2. Products and categories
  - System admins add products and categories to the system
  - customers/buyers can view all available products.

  ### 3. Order management
  - Order Creation:
      1. Users can create orders and add products to them.
      2. When adding products to an order, users specify the quantity they wish to purchase.

  - Stock Verification:
      1. The system ensures that the order quantity does not exceed the available stock for each product.
      2. If the requested quantity exceeds the available stock, the user is notified and prevents the order from being placed.

  - Order Total Cost Calculation:
      1. Upon completing the order, users receive the total cost of their orders.
      2. The total cost includes the prices of all products in the order, considering the quantities specified.

  - Order Items Details:
      1. Users can view the details of each order, including the items contained within it.
      2. For each item in an order, users can see the product details and the quantity ordered.

  - Order Filtering:
      1. Users can filter orders based on their status (e.g., pending, processing, completed).
      2. This filtering functionality allows users to easily track the status of their orders and manage them efficiently.

  - Checkout
      1. Users can checkout a pending order, after which the system sends an SMS to the user containing the order number for easier tracking
        and total cost of the order, and subsequently sets the order status to "placed".

## Technologies Used
1. Django Rest Framework
2. PostgreSQL
4. Docker and Docker compose
5. Nginx and Gunicorn
6. Google Cloud Platform , Google Kubernetes Engine
7. Kubernetes
8. Drf spectacular, Swagger UI, and Rapidoc
9. CI/CD - Jenkins

## Running the app Locally
Clone this repository to your machine

```
https://github.com/Kihara-Njoroge/Order-Management-System-API.git
```

Rename the ```.env.example``` and ```.env.db.example``` file found in the project's root directory to ```.env``` & ```.env.db``` and update the variables.

Ensure you have Docker, docker-compose, Minikube, kubectl, Jenkins installed.

## Build and Run:
 ### Locally
```
docker compose build
docker compose up

```
 - Navigate to http://localhost/api/v1/docs to view the API endpoints documentation.

 ### Production
```
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

```
```
docker-compose -f docker-compose.prod.yml up

```


#### Preview of the documentation UI
![Screenshot from 2024-02-23 09-01-29](https://github.com/Kihara-Njoroge/Order-Management-System-API/assets/46190291/540940b1-7f8f-442e-8f18-0f2a658e4e96)


## Set Up Minikube Kubernetes Cluster
 - Provisioning a Minikube cluster for local development.

    ### Start Minikube cluster
    ```
    minikube start --driver=docker

    ```

    ### Set kubectl context to Minikube

    ```
    kubectl config use-context minikube

    ```

    ### Deploy the App on Minikube Kubernetes

    - You can use the already defined Kubernetes YAML files for deployment, service, and ingress or define your own.

    ### Apply Kubernetes configurations

    ```
    kubectl apply -f k8s/secret.yaml
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    kubectl apply -f k8s/ingress.yaml

    ```

    ### Expose the application
    ```
    kubectl expose service order-management-api-service --type=NodePort --target-port=8000 --name=order-management-api-service-ext
    minikube service order-management-api-service-

    ```

## Implement Jenkins CI/CD Pipeline
  - Set up Jenkins and configure a CI/CD pipeline to automate Docker builds and Kubernetes deployments. The jenkins pipeline builds
    and pushes the builds to docker hub then deploys to github.
  - Use GitHub webhooks to trigger Jenkins build jobs:
      1. In your GitHub repository settings, navigate to Webhooks.
      2. Add a new webhook and specify the payload URL of your Jenkins server, along with the appropriate endpoint (e.g., /github-webhook/).
      3. Select the events that should trigger the webhook (e.g., push events, pull request events).

    ### CI/CD Pipeline Workflow:
      1. Checkout: Checkout source code from GitHub
      2. Build and Push Docker Image: Build the Docker image from the application code, Push Docker image to Docker Hub
      3. Run Tests: Validate the application's functionality.
      4. Deploy to MinikubeGKE: Deploy the application to the GKE/Minikube Kubernetes cluster.


## Monitoring and Logging Setup.

  ## Overview
  Guide for setting up monitoring and centralized logging in a Minikube environment. The setup includes the following components:

  - **Monitoring:** Utilizing Prometheus for metric collection and Grafana for visualization.
  - **Logging:** Implementing centralized logging with Elasticsearch for log storage and Kibana for log visualization.


  ## Monitoring Setup

  ### Step 1: Start Minikube if not already started

  ```
  minikube start --driver=docker

  ```
  ### Step 2: Add Helm Repositories
  ```
  kubectl create namespace monitoring

  ```
  ### Step 3: Install Prometheus and Grafana
  ```
  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  helm repo update
  helm install prometheus prometheus-community/prometheus
  kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-ext
  minikube service prometheus-server-ext

  ```

  ```
  helm repo add grafana https://grafana.github.io/helm-charts
  helm repo update
  helm install grafana grafana/grafana
  kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-ext
  minikube service grafana-ext

  kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

  ```

  - Login to grafana and n the Welcome to Grafana Home page, click Add your first data source, select Prometheus and add the URL where your Prometheus application
    is running. Click on “Save & test” to save your changes.

  - You can create your dashboards from scratch or import those that Grafana already offers.
  - To import a Grafana Dashboard, follow these steps:
     - Get the Grafana Dashboard ID from https://grafana.com/grafana/dashboards/
     - search for Kubernetes (look for Kubernetes cluster monitoring (via Prometheus) dashboard).
     - Select Dashboard and copy the Dashboard ID:
     - Go Back to Grafana and click Home on the top left corner On the menu, click Dashboards > Click New > Import
     - Add the Grafana ID: You will add the Grafana ID that you have copied and click Load


### Clean up

```
minikube stop
minikube delete
```
